#!/usr/bin/env python3
"""repowiki 小节级「语义抽验」：核对「章节来源」给的坐标区间是否真的支撑该节论述。

为什么用行内 `code` 而非普通英文词做判据：
  content 页约定所有代码实体（函数 / 结构 / 字段 / 文件名 / GUC）都写成行内 `code` 或链接标签。
  若换成「任意 ≥4 字符英文单词」，`index` / `table` / `cache` 这类词在源码注释里遍地都是，
  交集恒不为空，判据失效。取行内 `code` 作为「本节引用的代码实体」，噪声最低。

机器判据：
  对每个带「章节来源」的 H2 小节：
    ① 取**正文散文**（剔除 `图表来源`/`章节来源` 链接块、mermaid 块、`<cite>`）
       中每个行内 `code` 片段里的标识符与文件名 basename → 本节实体集合 E；
    ② 取该节所有 `file://<p>#L<a>-L<b>` 坐标区间的源码 → 源码标识符集合 S（全标识符，不做过滤）；
    ③ |E ∩ S| = 0 → **零交集节**（可疑，需回源判读）；占比 < 50% → **偏窄节**（只覆盖部分论点）。

零交集 ≠ 错误：`故障排查指南` / `依赖关系分析` 这类节天然是「一句话一条 + 一条粗坐标」的
指针式溯源，坐标只覆盖其中一条也属正常。脚本只负责把可疑节列出来，判读由人做。
退出码恒为 0。

用法：
    python3 _validate_semantic.py                    # 全库 content 汇总
    python3 _validate_semantic.py --list             # 打印零交集节明细
    python3 _validate_semantic.py --narrow           # 打印偏窄节明细
    python3 _validate_semantic.py <某页.md> [...]
"""
import collections
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _validate_coords as V

_HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(_HERE))
CONTENT = os.path.join(PROJ, 'wiki', 'repowiki', 'zh', 'content')

SECTION_SRC = re.compile(r'file://([^#\s\)]+)#L(\d+)(?:-L(\d+))?')
IDENT = re.compile(r'[A-Za-z_][A-Za-z0-9_]{2,}')
FNAME = re.compile(r'[\w./-]+\.(?:c|h|y|l|sql|am|dat|control|spec|pl|pm|py|sh|in|ac|mk)\b')
LINK_BLOCK = re.compile(r'(?m)^- \[[^\]]*\]\(file://[^)]+\)\s*$')
CODE_SPAN = re.compile(r'`([^`\n]+)`')


def strip_noise(body):
    """剔除 mermaid 块、`图表来源`/`章节来源` 链接块与行内坐标 URL，只留散文。"""
    body = re.sub(r'```mermaid.*?```', '', body, flags=re.S)
    body = LINK_BLOCK.sub('', body)
    body = re.sub(r'\(file://[^)]+\)', '', body)
    return body


def entities(prose):
    """从行内 `code` 片段抽「本节引用的代码实体」。"""
    out = set()
    for span in CODE_SPAN.findall(prose):
        for m in FNAME.findall(span):
            out.add(os.path.basename(m))
        out |= set(IDENT.findall(span))
    # 去掉明显不是实体的（SQL 关键字、纯数字、过短）
    out = {x for x in out if not x.isdigit()}
    return out


def src_idents(text):
    return set(IDENT.findall(text))


def sections(text):
    lines = text.split('\n')
    heads = [(i, l[3:].strip()) for i, l in enumerate(lines) if l.startswith('## ')]
    return [(name, '\n'.join(lines[i + 1:(heads[idx + 1][0] if idx + 1 < len(heads)
                                             else len(lines))]))
            for idx, (i, name) in enumerate(heads)]


def check(files, show_zero, show_narrow):
    stats = collections.Counter()
    zero, narrow = [], []
    for f in files:
        text = open(f, encoding='utf-8').read()
        rel = os.path.relpath(f, CONTENT)
        for name, body in sections(text):
            if '章节来源' not in body:
                continue
            stats['sections'] += 1
            coords = [(p, int(a), int(b or a)) for p, a, b in SECTION_SRC.findall(body)]
            if not coords:
                continue
            ent = entities(strip_noise(body))
            if not ent:
                stats['no_entity'] += 1
                continue
            buf, cited_names = [], set()
            for p, a, b in coords:
                cited_names.add(os.path.basename(p))
                full = os.path.join(V.REPO, p)
                if not os.path.exists(full):
                    stats['missing_file'] += 1
                    continue
                ls = V.read_lines(full)
                buf += ls[max(0, a - 1):min(len(ls), b)]
            # 文件名实体：命中判据是「被本节坐标引用」，而不是在源码正文里出现
            e_file = {x for x in ent if '.' in x and FNAME.fullmatch(x)}
            e_id = ent - e_file
            hit = (e_id & src_idents('\n'.join(buf))) | (e_file & cited_names)
            if not hit:
                stats['zero'] += 1
                zero.append((rel, name, sorted(e_id)[:8] or sorted(e_file)[:8], len(coords)))
            elif len(hit) / len(ent) < 0.5:
                stats['narrow'] += 1
                narrow.append((rel, name, f'{len(hit)}/{len(ent)}', len(coords)))
            else:
                stats['ok'] += 1
    print(f'带「章节来源」的 H2 小节           : {stats["sections"]}')
    print(f'  正文未引任何行内实体（判据不适用）: {stats["no_entity"]}')
    print(f'  零交集（可疑）                    : {stats["zero"]}')
    print(f'  偏窄（实体命中 < 50%）            : {stats["narrow"]}')
    print(f'  支撑（命中 ≥ 50%）                : {stats["ok"]}')
    if show_zero:
        print('\n-- 零交集节 --')
        for rel, name, ent, c in sorted(zero):
            print(f'   {rel}  「{name}」  坐标 {c} 条  实体 {ent}')
    if show_narrow:
        print('\n-- 偏窄节 --')
        for rel, name, r, c in sorted(narrow):
            print(f'   {rel}  「{name}」  命中 {r} / 坐标 {c} 条')
    return stats


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    files = args or sorted(glob.glob(os.path.join(CONTENT, '**', '*.md'), recursive=True))
    print(f'扫描 {len(files)} 篇\n')
    check(files, '--list' in sys.argv, '--narrow' in sys.argv)
    return 0


if __name__ == '__main__':
    sys.exit(main())
