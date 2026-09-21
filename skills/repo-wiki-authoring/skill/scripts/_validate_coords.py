#!/usr/bin/env python3
"""repowiki 坐标校验器：核对 wiki 页面里引用的源码坐标是否真实。

两类检查：
  A. file:// 链接坐标 —— 解析 `file://<path>#L<a>-L<b>`，检查文件存在且行号不越界。
  B. 「入口链」代码块里的裸行号 —— 代码块内以 `文件名.c:NN` 建立当前文件上下文，
     随后出现的 `:NN` 视为对该文件的引用，逐条打印其真实内容供人工/自动比对。

用法：
    python3 _validate_coords.py <wiki.md> [<wiki.md> ...]
    python3 _validate_coords.py --dir <目录>        # 递归扫描目录下所有 .md

退出码：0 = 无 A 类问题；1 = 存在 A 类问题。
"""
import re
import os
import sys

# ── 路径定位 ─────────────────────────────────────────────────
# 本脚本位于 notes-hub/projects/postgres/wiki/scripts/。源码仓按 project.yaml
# 的 source_repo（基准 = notes-hub 仓根）解析，换机器只需同级 clone 即可复用。
_HERE = os.path.dirname(os.path.abspath(__file__))       # .../wiki/scripts
PROJ = os.path.dirname(os.path.dirname(_HERE))           # .../projects/postgres
NOTES = os.path.dirname(os.path.dirname(PROJ))           # notes-hub 仓根


def _source_repo():
    rel = '../postgres'
    try:
        for line in open(os.path.join(PROJ, 'project.yaml'), encoding='utf-8'):
            m = re.match(r'\s*source_repo:\s*(\S+)', line)
            if m:
                rel = m.group(1)
                break
    except OSError:
        pass
    return os.path.normpath(os.path.join(NOTES, rel))


REPO = _source_repo()
COORD_RE = re.compile(r'file://([^#\s\)]+)#L(\d+)(?:-L(\d+))?')
ANCHOR_RE = re.compile(r'(?<![\w.\-])([A-Za-z0-9_.\-]+\.(?:c|h|sql|control|y|l)):(\d+)')
NUMLINE_RE = re.compile(r':(\d+)')

# 裸文件名 -> 真实路径（源码树内按 basename 索引；重名时先出现者胜）
_INDEX = {}


def build_index():
    if _INDEX:
        return _INDEX
    for base in ('contrib', 'src'):
        root = os.path.join(REPO, base)
        if not os.path.isdir(root):
            continue
        for dp, _dn, fn in os.walk(root):
            for f in fn:
                _INDEX.setdefault(f, os.path.join(dp, f))
    return _INDEX


def read_lines(path):
    with open(path, encoding='utf-8', errors='replace') as fh:
        return fh.read().split('\n')


def check_links(wiki):
    """A 类：file:// 坐标的文件存在性与越界。"""
    text = open(wiki, encoding='utf-8').read()
    seen, bad = {}, []
    for m in COORD_RE.finditer(text):
        p, a, b = m.group(1), int(m.group(2)), int(m.group(3) or m.group(2))
        if a > b:
            a, b = b, a
        seen[(p, a, b)] = True
    for (p, a, b) in seen:
        full = os.path.join(REPO, p)
        if not os.path.exists(full):
            bad.append(f'MISSING  {p}#L{a}')
            continue
        n = len(read_lines(full))
        if b > n:
            bad.append(f'OOB      {p}#L{a}-L{b}  (file has {n} lines)')
    return len(seen), bad


def _emit(idx, fname, n):
    """校验单个 `文件:行号` 坐标，返回 (kind, 描述)。"""
    full = idx.get(fname)
    if not full:
        return ('miss', f'{fname}:{n}  (未在源码树中找到)')
    src = read_lines(full)
    if n < 1 or n > len(src):
        return ('oob', f'{fname}:{n}  越界 (file has {len(src)} lines)')
    return ('ok', f'{fname}:{n:<5} | {src[n-1].strip()[:66]}')


def entry_blocks(lines):
    """找出所有「入口链」代码块，返回 [(标题行, 块内行列表)]。

    兼容两种写法：
      ① 标题在代码块**内**首行（```text 后紧跟 `入口链：…`）；
      ② 标题在代码块**外**——正文中以 `**入口链：…**` 起头，后接代码块
         （往前回溯 3 行；这是本 wiki 更常见的写法）。
    """
    out, i, n = [], 0, len(lines)
    while i < n:
        if lines[i].strip().startswith('```'):
            j = i + 1
            buf = []
            while j < n and not lines[j].strip().startswith('```'):
                buf.append(lines[j])
                j += 1
            head = next((x for x in buf if '入口链' in x), None)
            if head is None:
                for k in range(max(0, i - 3), i):
                    if '入口链' in lines[k]:
                        head = lines[k]
                        break
            if head is not None:
                out.append((head, buf))
            i = j + 1
        else:
            i += 1
    return out


def _in_parens(line, pos):
    """锚点是否落在未闭合的括号内。

    入口链常在括号里顺带提及另一个文件，例如
    `…（5 处，宏定义见 c.h:1068）`。这类锚点只是**交叉参考**，不能接管
    后续裸行号的归属 —— 否则后面 `load_external_function(...)  :39-41`
    会被算到 c.h 头上（真实归属是 hstore_plperl.c），从而掩盖真错误。
    """
    pre = line[:pos]
    return pre.count('(') + pre.count('（') > pre.count(')') + pre.count('）')


def check_chains(wiki):
    """B 类：入口链代码块内的坐标（锚点与裸行号），逐条打印真实内容。

    上下文规则：`文件名.c:NN` 锚点自身即一个坐标，同时把其后直到下一个
    锚点之前的裸 `:NN` 归属给该文件；整行无锚点时裸号继承上一行上下文。
    例外：位于括号内（未闭合）的锚点不接管归属，见 `_in_parens`。
    """
    idx = build_index()
    lines = open(wiki, encoding='utf-8').read().split('\n')

    out = []
    for head, b in entry_blocks(lines):
        out.append(('title', head.strip()[:70]))
        curfile = None
        for l in b:
            if '入口链' in l:
                continue
            anchors = list(ANCHOR_RE.finditer(l))
            if not anchors:
                for mm in NUMLINE_RE.finditer(l):
                    if curfile:
                        out.append(_emit(idx, curfile, int(mm.group(1))))
                continue
            for i, am in enumerate(anchors):
                start = am.end()
                end = anchors[i + 1].start() if i + 1 < len(anchors) else len(l)
                # 锚点自带文件名，无论如何都按它自身校验
                out.append(_emit(idx, am.group(1), int(am.group(2))))
                # 括号内顺带提及的文件不接管后续裸行号归属
                if not _in_parens(l, am.start()):
                    curfile = am.group(1)
                for mm in NUMLINE_RE.finditer(l, start, end):
                    if curfile:
                        out.append(_emit(idx, curfile, int(mm.group(1))))
    return out


def collect(targets):
    files = []
    for t in targets:
        if os.path.isdir(t):
            for dp, _dn, fn in os.walk(t):
                files += [os.path.join(dp, f) for f in sorted(fn) if f.endswith('.md')]
        else:
            files.append(t)
    return files


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 2
    if args[0] == '--dir':
        targets = args[1:]
        verbose = False
    else:
        targets, verbose = args, '--chains' in args
        targets = [t for t in targets if t != '--chains']

    total_bad = 0
    for wiki in collect(targets):
        ncoord, bad = check_links(wiki)
        total_bad += len(bad)
        flag = 'OK ' if not bad else 'BAD'
        rel = os.path.relpath(os.path.abspath(wiki), REPO)
        if rel.startswith('..'):
            rel = os.path.basename(wiki)
        print(f'[{flag}] {rel}  {ncoord} coords, {len(bad)} link problems')
        for x in bad:
            print(f'        {x}')
        if verbose:
            for kind, line in check_chains(wiki):
                print(('    ## ' if kind == 'title' else '        ') + line)
    print(f'\n== total link problems: {total_bad}')
    return 1 if total_bad else 0


if __name__ == '__main__':
    sys.exit(main())
