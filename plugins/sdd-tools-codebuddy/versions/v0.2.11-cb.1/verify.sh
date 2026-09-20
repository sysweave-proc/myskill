#!/usr/bin/env bash
# 基准校准脚本 —— v0.2.11-cb.1
#
# 校验三件事：
#   1. plugin/ 基准本体未被改动（与 PROVENANCE.md 记录的包指纹一致）
#   2. source.zip 存档与 plugin/ 本体内容一致
#   3. 上游基线仍与记录一致，并复算改造幅度（逐字节一致 / 已改写 / 新增 / 未移植）
#
# 用法： bash verify.sh [上游 sdd-tools 目录]
#   不传参时默认指向本仓镜像 ../../../../external-skills/agent-alchemy-marketplace/sdd-tools
# 退出码： 0 = 全部通过；1 = 有不一致

set -uo pipefail

EXPECT_PKG="7bd5a590e650a9c9b97aae5152baf596"          # 本产物 plugin/ 包指纹
EXPECT_UPSTREAM_PKG="d05f987a0964c02cd90b512a7234fba2" # 上游 sdd-tools 包指纹
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN="$HERE/plugin"
UPSTREAM="${1:-$HERE/../../../../external-skills/agent-alchemy-marketplace/sdd-tools}"

fail=0
ok()   { printf '  \033[32m✓\033[0m %s\n' "$1"; }
bad()  { printf '  \033[31m✗\033[0m %s\n' "$1"; fail=1; }

# 包指纹：只覆盖目录内全部文件，口径与 PROVENANCE.md 一致
pkg_fp() { ( cd "$1" && find . -type f | LC_ALL=C sort | xargs md5sum | md5sum | cut -c1-32 ); }
# 上游口径：额外排除本地新增的 PROVENANCE.md（防自引用）
pkg_fp_upstream() { ( cd "$1" && find . -type f ! -name PROVENANCE.md | LC_ALL=C sort | xargs md5sum | md5sum | cut -c1-32 ); }

echo "== 1. 基准本体 =="
if [ ! -d "$PLUGIN" ]; then
  bad "找不到 $PLUGIN"
else
  got="$(pkg_fp "$PLUGIN")"
  if [ "$got" = "$EXPECT_PKG" ]; then
    ok "plugin/ 包指纹一致（$got，$(find "$PLUGIN" -type f | wc -l) 文件）"
  else
    bad "plugin/ 包指纹不符：期望 $EXPECT_PKG，实际 $got"
  fi
fi

echo "== 2. source.zip 存档 =="
if [ ! -f "$HERE/source.zip" ]; then
  bad "找不到 source.zip"
else
  tmp="$(mktemp -d)"
  if command -v unzip >/dev/null 2>&1; then
    unzip -qo "$HERE/source.zip" -d "$tmp"
  else
    python3 -c "import zipfile,sys; zipfile.ZipFile(sys.argv[1]).extractall(sys.argv[2])" "$HERE/source.zip" "$tmp"
  fi
  if [ -d "$tmp/plugin" ]; then
    got="$(pkg_fp "$tmp/plugin")"
    if [ "$got" = "$EXPECT_PKG" ]; then
      ok "存档解包后指纹与本体一致（$got）"
    else
      bad "存档解包后指纹不符：期望 $EXPECT_PKG，实际 $got"
    fi
  else
    bad "存档内未找到 plugin/ 目录"
  fi
  rm -rf "$tmp"
fi

echo "== 3. 上游基线与改造幅度 =="
if [ ! -d "$UPSTREAM" ]; then
  printf '  \033[33m!\033[0m 未找到上游基线目录，跳过：%s\n' "$UPSTREAM"
else
  got="$(pkg_fp_upstream "$UPSTREAM")"
  if [ "$got" = "$EXPECT_UPSTREAM_PKG" ]; then
    ok "上游包指纹一致（$got）"
  else
    bad "上游包指纹不符：期望 $EXPECT_UPSTREAM_PKG，实际 $got —— 上游可能已更新，需重跑改造"
  fi

  same=0; mod=0; new=0
  while IFS= read -r rel; do
    if [ -f "$UPSTREAM/$rel" ]; then
      if cmp -s "$PLUGIN/$rel" "$UPSTREAM/$rel"; then same=$((same+1)); else mod=$((mod+1)); fi
    else
      new=$((new+1))
    fi
  done < <( cd "$PLUGIN" && find . -type f | sed 's|^\./||' | LC_ALL=C sort )

  printf '  逐字节一致=%s  已改写=%s  新增=%s\n' "$same" "$mod" "$new"
  if [ "$same" = "16" ] && [ "$mod" = "24" ] && [ "$new" = "6" ]; then
    ok "改造幅度与 PROVENANCE.md 记录一致（16 / 24 / 6）"
  else
    bad "改造幅度与记录不符（期望 16 / 24 / 6）"
  fi

  missing=""
  while IFS= read -r rel; do
    rel="${rel#./}"
    [ -f "$PLUGIN/$rel" ] || missing="$missing $rel"
  done < <( cd "$UPSTREAM" && find . -type f ! -name PROVENANCE.md | LC_ALL=C sort )
  missing="$(echo $missing)"
  if [ "$missing" = "hooks/resolve-cross-plugins.sh" ]; then
    ok "未移植项与记录一致（hooks/resolve-cross-plugins.sh，属有意不移植）"
  else
    bad "未移植项与记录不符：[$missing]"
  fi
fi

echo
if [ "$fail" -eq 0 ]; then
  printf '\033[32m校准通过：基准完好。\033[0m\n'
else
  printf '\033[31m校准失败：请核对上方 ✗ 项。\033[0m\n'
fi
exit "$fail"
