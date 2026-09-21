#!/usr/bin/env python3
"""repowiki 命名/老化筛查器：页面里写的代码实体名，源码里到底有没有？

为什么需要它：
  「坐标存在 + 界内 + 格式 + 标签一致」只能证明**引用的文件**没问题，证明不了
  **正文里写的函数/字段/枚举名**是当前源码里的名字。PG 改名很频繁
  （`heap_page_prune` → `heap_page_prune_and_freeze`、`_bt_recycle` 已删除、
  `StandardChunkHeader` 在 PG 15 前后被 `MemoryChunk` 取代），wiki 很容易留下旧名。

判据：
  ① 建源码词表——扫 `src/` + `contrib/` 下 `.c/.h/.sql/.dat/.y/.l/.am/.control/.spec/.in`
     以及 `Makefile*`/`meson.build`/`.pl/.pm/.sh/.po/.mk/.py`，抽出全部标识符（约 24 万）；
     另建**全量文件名集合**（任意扩展名），用于识别「正文写的是文件名」。
  ② 从页面**行内 `code`** 里抽「代码型」标识符（带下划线 / 全大写 / CamelCase），按下列
     五档归类；只有落在最后一档的才叫**可疑名**：
       ok_lex       在源码词表里
       ok_file      命中源码树文件名
       ok_option    构建开关（`-Ddefault_library` 这类前导 `-D`/`-` 的值）
       ok_prefix    族名通配写法（span 里写的是 `heap_page_prune*`）
       placeholder  刻意占位（`ExecInitXxx`）
       unknown      以上都不符 → 可疑，须回源判读
  ③ 对可疑名给**近邻建议**（源码词表里最相近的名字）与**首现位置**，供人工判读。

注意：
  - 可疑 ≠ 错误。缩写（`BufTable` ← `BufTableHashCode`）、部分名（`SCAN_VAR` ←
    `EEOP_SCAN_VAR`）都会命中，必须逐条判读；但**旧名**（源码已改名/删除）也是落在这里，
    这正是本脚本的价值所在。
  - 退出码恒为 0（启发式筛查，不做门禁）。

用法：
    python3 _validate_names.py                 # 汇总
    python3 _validate_names.py --list          # 可疑名明细（近邻建议 + 首现位置）
    python3 _validate_names.py <某页.md> [...]
"""
import collections
import difflib
import glob
import os
import re
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(_HERE))
ROOT = os.path.join(PROJ, 'wiki', 'repowiki')
import _validate_coords as V          # 复用 source_repo 解析

CONTENT = os.path.join(ROOT, 'zh', 'content')
S = V.REPO

EXTS = {'c', 'h', 'sql', 'dat', 'y', 'l', 'am', 'control', 'spec', 'in',
        'pl', 'pm', 'sh', 'po', 'mk', 'py', 'build', 'txt', 'ac', 'm4'}
EXTRA_NAMES = ('Makefile', 'GNUmakefile', 'meson.build', 'meson_options.txt',
               'configure.ac', 'aclocal.m4')

IDENT_RE = re.compile(r'[A-Za-z_][A-Za-z0-9_]+')
CODE_SPAN = re.compile(r'`([^`\n]+)`')
CODEY = re.compile(r'^(?:[A-Za-z][A-Za-z0-9]*_[A-Za-z0-9_]+|[A-Z][A-Z0-9_]{3,}|[A-Za-z]*[a-z][A-Z]\w*)$')


def build_source_sets():
    """返回 (标识符词表, 全量文件名集合, 排序标识符列表, 反转排序列表〔后缀查询〕)。

    扫**整仓**（含根级 `configure.ac` / `meson.build`），排除 `.git`；否则
    `AC_CONFIG_FILES` 这类只在根级文件里出现的名字会被误判成「源码查无」。
    """
    lex, names = set(), set()
    for f in glob.glob(os.path.join(S, '**', '*'), recursive=True):
        if not os.path.isfile(f) or os.sep + '.git' + os.sep in f + os.sep:
            continue
        b = os.path.basename(f)
        names.add(b)
        names.add(b.rsplit('.', 1)[0])
        if (f.rsplit('.', 1)[-1] in EXTS or b in EXTRA_NAMES
                or b.startswith('Makefile')):
            try:
                lex.update(IDENT_RE.findall(
                    open(f, encoding='utf-8', errors='replace').read()))
            except OSError:
                pass
    return lex, names, sorted(lex), sorted(x[::-1] for x in lex)


def _has_prefix(tok, lex_sorted):
    """词表里是否存在以 tok 开头的标识符（族名通配 / 前缀缩写）。"""
    import bisect
    i = bisect.bisect_left(lex_sorted, tok)
    return i < len(lex_sorted) and lex_sorted[i].startswith(tok)


def _has_suffix(tok, rev_sorted):
    """词表里是否存在以 tok 结尾的标识符（`IsData` ← `GinPageIsData` 这类并写缩写）。"""
    import bisect
    r = tok[::-1]
    i = bisect.bisect_left(rev_sorted, r)
    return i < len(rev_sorted) and rev_sorted[i].startswith(r)


def classify(files, lex, names, lex_sorted, rev_sorted):
    stat = collections.Counter()
    unknown, warn = collections.defaultdict(list), collections.defaultdict(list)
    for f in files:
        rel = os.path.relpath(f, ROOT)
        for ln, line in enumerate(open(f, encoding='utf-8').read().split('\n'), 1):
            for span in CODE_SPAN.findall(line):
                wild = '*' in span
                for tok in IDENT_RE.findall(span):
                    if len(tok) < 4 or not CODEY.match(tok):
                        continue
                    where = (rel, ln, span.strip()[:64])
                    if 'Xxx' in tok or 'xxx' in tok:
                        stat['placeholder'] += 1
                    elif tok in lex:
                        stat['ok_lex'] += 1
                    elif tok.rstrip('s') in lex or tok.rstrip('es') in lex:
                        stat['ok_lex'] += 1
                    elif tok in names:
                        stat['ok_file'] += 1
                    elif len(tok) > 2 and (tok[1:] in lex or tok[1:] in names):
                        stat['ok_option'] += 1        # -Ddefault_library → default_library
                    elif wild and _has_prefix(tok.rstrip('_'), lex_sorted):
                        stat['ok_prefix'] += 1
                    elif (_has_prefix(tok, lex_sorted)
                          and ('/' in span or tok[0].isupper())):
                        # 并写缩写：`GinPageIsLeaf/IsData/IsList`、`MultiExec`←`MultiExecProcNode`
                        stat['ok_partial'] += 1
                    elif _has_suffix(tok, rev_sorted):
                        stat['ok_partial'] += 1
                    elif tok.endswith('_'):
                        stat['truncated'] += 1
                        warn[tok].append(where)
                    else:
                        stat['unknown'] += 1
                        unknown[tok].append(where)
    return stat, unknown, warn


def build_prefix_index(lex):
    idx = collections.defaultdict(list)
    for x in lex:
        idx[x[:3].lower()].append(x)
    return idx


def nearest(name, pref_idx, n=4):
    cands = set()
    for k in {name[:3].lower(), name[1:4].lower(), name.lstrip('_')[:3].lower()}:
        cands |= set(pref_idx.get(k, ()))
    cands.discard(name)
    if not cands:
        return []
    return difflib.get_close_matches(name, sorted(cands), n=n, cutoff=0.55)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    files = args or sorted(glob.glob(os.path.join(CONTENT, '**', '*.md'), recursive=True))
    print(f'扫描 {len(files)} 篇；建源码词表…')
    lex, names, lex_sorted, rev_sorted = build_source_sets()
    stat, unknown, warn = classify(files, lex, names, lex_sorted, rev_sorted)
    total = sum(stat.values())
    print(f'源码词表 {len(lex)} 个标识符 / {len(names)} 个文件名'
          f'；页面行内 code 的代码型标识符 {total} 处')
    for k in ('ok_lex', 'ok_file', 'ok_option', 'ok_prefix', 'placeholder',
              'truncated', 'unknown'):
        print(f'  {k:<12}: {stat[k]}')
    pct = stat['unknown'] / total * 100 if total else 0
    print(f'  → 可疑（unknown）占 {pct:.2f}%，共 {len(unknown)} 种')

    if '--list' in sys.argv:
        pref = build_prefix_index(lex)
        print('\n-- 可疑名明细（按出现次数降序）--')
        for name, hits in sorted(unknown.items(), key=lambda kv: (-len(kv[1]), kv[0])):
            rel, ln, span = hits[0]
            print(f'  {len(hits):3d}× {name:<32} 近邻: {", ".join(nearest(name, pref)) or "（无）"}')
            print(f'       首现 {rel}:{ln}   `{span}`')
        if warn:
            print('\n-- 末尾截断/前缀通配（非可疑，仅备查）--')
            for name, hits in sorted(warn.items(), key=lambda kv: -len(kv[1]))[:15]:
                print(f'  {len(hits):3d}× {name}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
