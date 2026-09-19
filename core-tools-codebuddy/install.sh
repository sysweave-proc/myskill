#!/usr/bin/env bash
# 把 agent-alchemy-core-tools（CodeBuddy 移植版）安装进本机 CodeBuddy。
#
# 行为：
#   1. 先跑目标版本的 verify.sh 校准基准（不通过就中止，避免装入未经校验的产物）
#   2. 备份 ~/.codebuddy 下的两个配置文件
#   3. 建本地市场目录并放入 plugin/ 快照
#   4. 注册市场（known_marketplaces.json）+ 启用插件（settings.json）
#   5. 校验 JSON 与安装件完整性，并打印后续步骤
#
# 幂等：可重复执行（会覆盖市场内的插件快照与清单，不动其它市场）。
# 用法： bash install.sh [版本号]        # 默认 v0.2.3-cb.1
# 卸载： bash install.sh --uninstall

set -euo pipefail

PLUGIN_NAME="agent-alchemy-core-tools"
MKT_NAME="agent-alchemy-local"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CFG="$HOME/.codebuddy/plugins/known_marketplaces.json"
SET="$HOME/.codebuddy/settings.json"
MKT="$HOME/.codebuddy/plugins/marketplaces/$MKT_NAME"

if [ "${1:-}" = "--uninstall" ]; then
  echo "== 卸载 $PLUGIN_NAME =="
  python3 - "$CFG" "$SET" "$MKT_NAME" "$PLUGIN_NAME" <<'PY'
import json, sys
cfg, st, mkt, plugin = sys.argv[1:5]
for path, keys in ((cfg, [mkt]), (st, [f"{plugin}@{mkt}"])):
    try:
        d = json.load(open(path))
    except FileNotFoundError:
        print(f"  {path} 不存在，跳过")
        continue
    for k in keys:
        if k in d:
            d.pop(k); print(f"  已从 {path} 移除 {k}")
        elif "enabledPlugins" in d and k in d["enabledPlugins"]:
            d["enabledPlugins"].pop(k); print(f"  已从 {path} 停用 {k}")
    json.dump(d, open(path, "w"), ensure_ascii=False, indent=2)
PY
  echo "  市场目录保留在 $MKT（如不再需要可手动删除）"
  echo "  重启 CodeBuddy 生效"
  exit 0
fi

VERSION="${1:-v0.2.3-cb.1}"
SRC="$HERE/versions/$VERSION/plugin"

echo "== 0. 校准基准 $VERSION =="
if [ -x "$HERE/versions/$VERSION/verify.sh" ]; then
  bash "$HERE/versions/$VERSION/verify.sh" >/dev/null && echo "  基准校准通过" \
    || { echo "  ✗ 基准校准未通过，中止安装"; exit 1; }
  else
  echo "  未找到 verify.sh，跳过校准"
fi

echo "== 1. 备份配置 =="
STAMP="$(date +%Y%m%d-%H%M%S)"
for f in "$CFG" "$SET"; do
  [ -f "$f" ] || continue
  cp "$f" "$f.bak-$STAMP" && echo "  $f → $(basename "$f").bak-$STAMP"
done

echo "== 2. 放入本地市场 =="
mkdir -p "$MKT/.codebuddy-plugin" "$MKT/plugins"
rm -rf "$MKT/plugins/$PLUGIN_NAME"
cp -r "$SRC" "$MKT/plugins/$PLUGIN_NAME"
echo "  $PLUGIN_NAME → $MKT/plugins/$PLUGIN_NAME（$(find "$MKT/plugins/$PLUGIN_NAME" -type f | wc -l) 文件）"

V="$(python3 -c "import json,sys;print(json.load(open('$SRC/.codebuddy-plugin/plugin.json'))['version'])")"
cat > "$MKT/.codebuddy-plugin/marketplace.json" <<JSON
{
  "name": "$MKT_NAME",
  "description": "本地插件市场：agent-alchemy core-tools 的 CodeBuddy 移植版",
  "owner": { "name": "local" },
  "plugins": [
    {
      "name": "$PLUGIN_NAME",
      "description": "代码库分析、多智能体深度探索、交互式访谈、语言模式与技术图表基座（agent-alchemy core-tools v0.2.3 的 CodeBuddy 移植版）",
      "version": "$V",
      "source": "./plugins/$PLUGIN_NAME",
      "license": "MIT"
    }
  ]
}
JSON
echo "  写入 $MKT/.codebuddy-plugin/marketplace.json（version=$V）"

echo "== 3. 注册市场 + 启用插件 =="
python3 - "$CFG" "$SET" "$MKT" "$MKT_NAME" "$PLUGIN_NAME" <<'PY'
import json, os, sys
cfg, st, mkt, mkt_name, plugin = sys.argv[1:6]
os.makedirs(os.path.dirname(cfg), exist_ok=True)
try:
    d = json.load(open(cfg))
except FileNotFoundError:
    d = {}
d[mkt_name] = {
    "type": "directory",
    "source": {"source": "directory", "path": mkt},
    "installLocation": mkt,
    "description": f"Local marketplace: {mkt_name}",
    "isBuiltIn": False,
}
json.dump(d, open(cfg, "w"), ensure_ascii=False, indent=2)
try:
    s = json.load(open(st))
except FileNotFoundError:
    s = {}
s.setdefault("enabledPlugins", {})[f"{plugin}@{mkt_name}"] = True
json.dump(s, open(st, "w"), ensure_ascii=False, indent=2)
print(f"  {cfg}  + {mkt_name}")
print(f"  {st}  + {plugin}@{mkt_name} = true")
PY

echo "== 4. 校验 =="
python3 -c "
import json,sys
for p in ['$CFG','$SET','$MKT/.codebuddy-plugin/marketplace.json','$MKT/plugins/$PLUGIN_NAME/.codebuddy-plugin/plugin.json']:
    json.load(open(p))
print('  JSON 全部合法')"

echo
echo "完成。接下来："
echo "  1) 重启 CodeBuddy（插件在会话启动时加载）"
echo "  2) 用 /plugin list 确认出现 $(printf '%s@%s' "$PLUGIN_NAME" "$MKT_NAME")"
echo "  3) 若未出现，改用 IDE 界面添加本地市场，或 /plugin marketplace add $MKT"
echo "  4) 之后即可用 /deep-analysis、/codebase-analysis、/interview-me"
echo
echo "注意：用户级 \(~/.codebuddy/skills/\) 若已有同名 skill（如 codebase-analysis），"
echo "      会与本插件的同名 skill 冲突，建议先改名或移走。"
echo "卸载： bash install.sh --uninstall"
