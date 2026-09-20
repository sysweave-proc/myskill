#!/usr/bin/env bash
# 基准校准脚本 —— v0.2.3-cb.2（cb.1 的增量修订版）
#
# 校验五件事：
#   1. 本版 plugin/ 基准本体未被改动
#   2. 本版 source.zip 存档与本体一致
#   3. **cb.1 基准未被改动**（修订版存在的前提）
#   4. 本版与 cb.1 的差异 = 22 逐字节一致 / 8 已改写 / 0 新增
#   5. 上游基线仍与记录一致
#
# 用法： bash verify.sh [上游 core-tools 目录]
# 退出码： 0 = 全部通过；1 = 有不一致

set -uo pipefail

EXPECT_PKG="e44a2692f51dc2cd3cc6828d5760bece"          # 本产物 plugin/ 包指纹
EXPECT_CB1_PKG="2a25c41b8b418c0e1b1967053412d66e"     # cb.1 基准（必须保持不变）
EXPECT_UPSTREAM_PKG="808192241ec2c53ced9bd83227279279" # 上游 core-tools 包指纹
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN="$HERE/plugin"
CB1="$HERE/../v0.2.3-cb.1/plugin"
UPSTREAM="${1:-$HERE/../../../../external-skills/agent-alchemy-marketplace/core-tools}"

fail=0
ok()   { printf '  \033[32m✓\033[0m %s\n' "$1"; }
bad()  { printf '  \033[31m✗\033[0m %s\n' "$1"; fail=1; }

pkg_fp() { ( cd "$1" && find . -type f | LC_ALL=C sort | xargs md5sum | md5sum | cut -c1-32 ); }
pkg_fp_upstream() { ( cd "$1" && find . -type f ! -name PROVENANCE.md | LC_ALL=C sort | xargs md5sum | md5sum | cut -c1-32 ); }

echo "== 1. 本版基准本体 =="
got="$(pkg_fp "$PLUGIN")"
if [ "$got" = "$EXPECT_PKG" ]; then
  ok "plugin/ 包指纹一致（$got，$(find "$PLUGIN" -type f | wc -l) 文件）"
else
  bad "plugin/ 包指纹不符：期望 $EXPECT_PKG，实际 $got"
fi

echo "== 2. 本版 source.zip 存档 =="
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
    [ "$got" = "$EXPECT_PKG" ] && ok "存档解包后指纹与本体一致（$got）" \
      || bad "存档解包后指纹不符：期望 $EXPECT_PKG，实际 $got"
  else
    bad "存档内未找到 plugin/ 目录"
  fi
  rm -rf "$tmp"
fi

echo "== 3. cb.1 基准未被改动 =="
if [ ! -d "$CB1" ]; then
  bad "找不到 cb.1 基准目录：$CB1"
else
  got="$(pkg_fp "$CB1")"
  if [ "$got" = "$EXPECT_CB1_PKG" ]; then
    ok "cb.1 基准完好（$got）"
  else
    bad "cb.1 基准被改动：期望 $EXPECT_CB1_PKG，实际 $got —— 基准不得原地修改"
  fi
fi

echo "== 4. 本版与 cb.1 的差异 =="
if [ -d "$CB1" ]; then
  same=0; mod=0; new=0
  while IFS= read -r rel; do
    if [ -f "$CB1/$rel" ]; then
      if cmp -s "$PLUGIN/$rel" "$CB1/$rel"; then same=$((same+1)); else mod=$((mod+1)); fi
    else
      new=$((new+1))
    fi
  done < <( cd "$PLUGIN" && find . -type f | sed 's|^\./||' | LC_ALL=C sort )
  printf '  逐字节一致=%s  已改写=%s  新增=%s\n' "$same" "$mod" "$new"
  if [ "$same" = "22" ] && [ "$mod" = "8" ] && [ "$new" = "0" ]; then
    ok "差异与 PROVENANCE.md 记录一致（22 / 8 / 0：7 个 description 追加中文触发 + plugin.json 版本号）"
  else
    bad "差异与记录不符（期望 22 / 8 / 0）"
  fi
fi

echo "== 5. 上游基线 =="
if [ ! -d "$UPSTREAM" ]; then
  printf '  \033[33m!\033[0m 未找到上游基线目录，跳过：%s\n' "$UPSTREAM"
else
  got="$(pkg_fp_upstream "$UPSTREAM")"
  [ "$got" = "$EXPECT_UPSTREAM_PKG" ] && ok "上游包指纹一致（$got）" \
    || bad "上游包指纹不符：期望 $EXPECT_UPSTREAM_PKG，实际 $got —— 上游可能已更新"
fi

echo
if [ "$fail" -eq 0 ]; then
  printf '\033[32m校准通过：基准完好。\033[0m\n'
else
  printf '\033[31m校准失败：请核对上方 ✗ 项。\033[0m\n'
fi
exit "$fail"
