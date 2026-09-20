#!/usr/bin/env bash
# 把本目录下的 agent-alchemy（CodeBuddy 移植版）插件安装进本机 CodeBuddy 的本地市场。
#
# 本脚本在 agent-alchemy-*-codebuddy 各包内**内容完全一致**：插件名与默认版本都从包内自动读取，
# 因此五个包（core-tools / dev-tools / tdd-tools / claude-tools / sdd-tools）共用同一份安装逻辑。
#
# 行为：
#   1. 自动确定版本（`versions/` 下按版本号最大的一个），先跑其 verify.sh 校准基准（不通过就中止）
#   2. 备份 ~/.codebuddy 下的两个配置文件
#   3. 把 plugin/ 快照放入本地市场 plugins/<插件名>/
#   4. **重建**市场清单：扫描 plugins/ 下所有插件，让清单始终等于"实际装了什么"
#      —— 多个 agent-alchemy 插件可共存于同一市场，互不覆盖
#   5. 注册市场（未见则加）+ 启用本插件（settings.json）
#   6. 校验 JSON 与安装件完整性，并打印后续步骤
#
# 幂等：可重复执行（覆盖市场内的同名插件快照，不动其它插件与其它市场）。
# 用法： bash install.sh [版本号]        # 省略版本号则用 versions/ 下的最新版
# 卸载： bash install.sh --uninstall

set -euo pipefail

MKT_NAME="agent-alchemy-local"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CFG="$HOME/.codebuddy/plugins/known_marketplaces.json"
SET="$HOME/.codebuddy/settings.json"
MKT="$HOME/.codebuddy/plugins/marketplaces/$MKT_NAME"

# 重建市场清单：以 plugins/ 下的 plugin.json 为唯一事实来源
rebuild_manifest() {
  python3 - "$MKT" "$MKT_NAME" <<'PY'
import json, os, sys
mkt, mkt_name = sys.argv[1:3]
pdirs = os.path.join(mkt, "plugins")
entries = []
if os.path.isdir(pdirs):
    for d in sorted(os.listdir(pdirs)):
        pj = os.path.join(pdirs, d, ".codebuddy-plugin", "plugin.json")
        if os.path.isfile(pj):
            j = json.load(open(pj))
            entries.append({
                "name": j.get("name", d),
                "description": j.get("description", ""),
                "version": j.get("version", "0.0.0"),
                "source": f"./plugins/{d}",
                "license": j.get("license", "MIT"),
            })
json.dump({"name": mkt_name,
           "description": "本地插件市场：agent-alchemy 系列的 CodeBuddy 移植版",
           "owner": {"name": "local"}, "plugins": entries},
          open(os.path.join(mkt, ".codebuddy-plugin", "marketplace.json"), "w"),
          ensure_ascii=False, indent=2)
print(f"  清单含 {len(entries)} 个插件：" + ", ".join(f"{e['name']}@{e['version']}" for e in entries))
PY
}

# 默认版本 = versions/ 下 sort -V 最大的目录
default_version() {
  ls -1d "$HERE"/versions/*/ 2>/dev/null | sort -V | tail -1 | xargs -r basename
}

if [ "${1:-}" = "--uninstall" ]; then
  # 卸载需要知道插件名：优先从最新版 plugin.json 读，缺失则从市场内清单反查
  PLUGIN_NAME="$(python3 -c "
import json,glob,os
c=sorted(glob.glob('$HERE/versions/*/plugin/.codebuddy-plugin/plugin.json'))
print(json.load(open(c[-1]))['name'] if c else '')" 2>/dev/null || true)"
  echo "== 卸载 ${PLUGIN_NAME:-（未识别）} =="
  python3 - "$SET" "$MKT" "$MKT_NAME" "$PLUGIN_NAME" <<'PY'
import json, os, shutil, sys
st, mkt, mkt_name, plugin = sys.argv[1:5]
pdir = os.path.join(mkt, "plugins", plugin)
if plugin and os.path.isdir(pdir):
    shutil.rmtree(pdir); print(f"  已删除 {pdir}")
try:
    s = json.load(open(st))
except FileNotFoundError:
    s = {}
if s.get("enabledPlugins", {}).pop(f"{plugin}@{mkt_name}", None) is not None:
    json.dump(s, open(st, "w"), ensure_ascii=False, indent=2)
    print(f"  已从 {st} 停用 {plugin}@{mkt_name}")
PY
  # 复用安装侧的清单重建（剩余插件自动保留）
  bash "$HERE/install.sh" --rebuild-manifest-only
  echo "  重启 CodeBuddy 生效"
  exit 0
fi

if [ "${1:-}" = "--rebuild-manifest-only" ]; then
  mkdir -p "$MKT/.codebuddy-plugin" "$MKT/plugins"
  echo "== 重建市场清单 =="
  rebuild_manifest
  exit 0
fi

VERSION="${1:-$(default_version)}"
if [ -z "$VERSION" ]; then echo "✗ 找不到任何 versions/<版本>/ 目录"; exit 1; fi
SRC="$HERE/versions/$VERSION/plugin"
PLUGIN_NAME="$(python3 -c "import json;print(json.load(open('$SRC/.codebuddy-plugin/plugin.json'))['name'])")"
echo "== 安装 $PLUGIN_NAME（$VERSION）=="

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

echo "== 3. 重建市场清单（多插件共存）=="
rebuild_manifest

echo "== 4. 注册市场 + 启用插件 =="
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

echo "== 5. 校验 =="
python3 -c "
import json
for p in ['$CFG','$SET','$MKT/.codebuddy-plugin/marketplace.json','$MKT/plugins/$PLUGIN_NAME/.codebuddy-plugin/plugin.json']:
    json.load(open(p))
print('  JSON 全部合法')"

echo
echo "完成。接下来："
echo "  1) 重启 CodeBuddy（插件在会话启动时加载）"
echo "  2) /plugin list 确认出现 $PLUGIN_NAME@$MKT_NAME"
if compgen -G "$MKT/plugins/$PLUGIN_NAME/commands/*.md" >/dev/null; then
  echo "  3) 可用命令：$(cd "$MKT/plugins/$PLUGIN_NAME/commands" && ls -1 *.md | sed 's/\.md$//' | sed 's/^/\//' | tr '\n' ' ')"
fi
echo
echo "注意：agent-alchemy 系列插件之间有依赖（core-tools 的 agent/skill 被 dev-tools、tdd-tools、"
echo "      sdd-tools 复用）。要用完整能力，请把依赖的插件也装进同一个市场 $MKT_NAME。"
echo "卸载： bash install.sh --uninstall"
