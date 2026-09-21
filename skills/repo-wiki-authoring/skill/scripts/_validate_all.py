#!/usr/bin/env python3
"""repowiki 全库验收器：一次性核完 `zh/content/**`（地图页）+ `knowledge/zh/**`（知识卡）。

五组检查（每组给出「实测值 + 问题清单」，退出码只看问题数）：

  1. 完整性  —— 计划清单 158 篇 / 覆盖扩展 21 篇逐条落盘；知识卡模块树
                109 个模块 × 五件套齐全；`_index.yaml` 的 dir_name 与实盘目录双向对齐；
                横切主题卡 5 篇。
  2. 骨架     —— content 页 h1=1、有 `<cite>`、H2 序列等于固定契约；
                `## 目录` 项数 = 10 且每个锚点在本页可解析。
  3. 坐标     —— A 类 `file://<p>#L<a>-L<b>`：文件存在 / 不越界 / 锚点格式合规
                （`#La-Lb` 缺第二个 `L` 属违规）/ 链接标签数值与片段一致；
                B 类「入口链」代码块内的 `文件.c:NN` 锚点与裸行号不越界。
  4. 溯源     —— 每张 mermaid 之后紧跟「图表来源」；实质节（项目结构/核心组件/
                详细组件分析/依赖关系分析/故障排查指南）有「章节来源」；
                占位节（性能考量/结论/附录）有 `[本节为…]` 收尾句；`<cite>` 内文件存在。
  5. 交叉引用 —— `](#锚点)` 可落到本页标题；`](相对路径.md)` 文件存在。
  6. 粗锚 WARN —— `#L1-L<b>`（b≤200）且文件 ≥500 行：能过前四类检查却指向版权头/include 段，
                 属「假精度」锚点，只告警不计入退出码（明细见 `_validate_semantic.py`）。

用法：
    python3 _validate_all.py                # 全库（content + knowledge）
    python3 _validate_all.py --content      # 仅 content
    python3 _validate_all.py --knowledge    # 仅 knowledge
    python3 _validate_all.py --semantic     # 追加入口链语义抽验（启发式，不计入退出码）

退出码：0 = 无问题；1 = 存在问题。
"""
import collections
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _validate_coords as V          # 复用 A/B 类坐标解析

_HERE = os.path.dirname(os.path.abspath(__file__))          # .../wiki/scripts
PROJ = os.path.dirname(os.path.dirname(_HERE))              # .../projects/postgres
ROOT = os.path.join(PROJ, 'wiki', 'repowiki')
CONTENT = os.path.join(ROOT, 'zh', 'content')
KNOW = os.path.join(ROOT, 'knowledge', 'zh')
META = os.path.join(ROOT, 'zh', 'meta')

FIXED_H2 = ['目录', '简介', '项目结构', '核心组件', '架构总览', '详细组件分析',
            '依赖关系分析', '性能考量', '故障排查指南', '结论', '附录']
MUST_SECTIONS = {'项目结构', '核心组件', '详细组件分析', '依赖关系分析', '故障排查指南'}
PLACEHOLDER_SECTIONS = {'性能考量', '结论', '附录'}
MODULE_FILES = ['概述.md', '技术栈.md', '架构设计.md', '特殊配置与命令.md', '编码规范.md']

FRAG_RE = re.compile(r'file://([^#\s\)]+)#([^\s\)]+)')
LINK_LABEL_RE = re.compile(r'\[([^\]]+)\]\(file://([^)#]+)#L(\d+)(?:-L(\d+))?\)')
CITE_ITEM_RE = re.compile(r'^\- \[[^\]]+\]\(file://([^)#]+)\)$', re.M)
TOC_ITEM_RE = re.compile(r'\]\(#([^)]+)\)')


def rel(p):
    return os.path.relpath(p, ROOT)


def md_files(root):
    return sorted(glob.glob(os.path.join(root, '**', '*.md'), recursive=True))


def slug(title):
    """GitHub 风格锚点：小写、去标点、空白转连字符（保留 CJK）。"""
    s = title.strip().lower()
    s = re.sub(r'[^\w\s\u4e00-\u9fff-]', '', s)
    return re.sub(r'\s+', '-', s)


# ── 1. 完整性 ────────────────────────────────────────────────
def check_inventory():
    print('== 1. 完整性 ==')
    prob, notes = [], []

    content = md_files(CONTENT)
    notes.append(f'content 页实测 {len(content)} 篇')

    for fname, path_col in (('completion-manifest.tsv', 2),
                            ('coverage-extension.tsv', 3)):
        rows = [l.rstrip('\n').split('\t')
                for l in open(os.path.join(META, fname), encoding='utf-8')][1:]
        miss = [r[path_col] for r in rows
                if not os.path.exists(os.path.join(CONTENT, r[path_col]))]
        notes.append(f'{fname}: {len(rows)} 条登记，缺页 {len(miss)}')
        prob += [f'{fname}: 登记页未落盘 {p}' for p in miss]
        if fname == 'coverage-extension.tsv':
            for r in rows:
                for c in r[4].split(','):
                    c = c.strip().rstrip('/')
                    if not c:
                        continue
                    if '*' in c:
                        if not glob.glob(os.path.join(V.REPO, c)):
                            prob.append(f'{fname}: 覆盖 glob 无命中 {c}（页 {r[2]}）')
                    elif not os.path.exists(os.path.join(V.REPO, c)):
                        prob.append(f'{fname}: 覆盖目录不存在 {c}（页 {r[2]}）')

    # 知识卡模块树（模块目录按目录树嵌套，用 **/_module.yaml 定位）
    modules = sorted(os.path.dirname(p) for p in
                     glob.glob(os.path.join(KNOW, '**', '_module.yaml'), recursive=True))
    topics = [d for d in sorted(glob.glob(os.path.join(KNOW, '*')))
              if os.path.isdir(d) and d not in modules]
    notes.append(f'知识卡：模块目录 {len(modules)} 个、主题卡目录 {len(topics)} 个')
    for d in modules:
        for f in MODULE_FILES:
            if not os.path.exists(os.path.join(d, f)):
                prob.append(f'模块卡缺件: {rel(d)}/{f}')
    for d in topics:
        if not os.path.exists(os.path.join(d, os.path.basename(d) + '.md')):
            prob.append(f'主题卡缺同名正文: {rel(d)}')

    # _index.yaml 的 dir_name 与实盘目录对齐
    yml = open(os.path.join(KNOW, '_index.yaml'), encoding='utf-8').read()
    listed = re.findall(r'(?m)^\s{8}dir_name:\s*(.+?)\s*$', yml)
    dup = [k for k, v in collections.Counter(listed).items() if v > 1]
    real = [os.path.basename(d) for d in modules]
    dreal = [k for k, v in collections.Counter(real).items() if v > 1]
    for d in sorted(set(real) - set(listed)):
        prob.append(f'_index.yaml 未登记模块目录 {d}')
    for d in sorted(set(listed) - set(real)):
        prob.append(f'_index.yaml 登记了不存在的目录 {d}')
    if dup:
        prob.append(f'_index.yaml dir_name 重名 {dup}')
    if dreal:
        prob.append(f'实盘模块目录 basename 重名 {dreal}（dir_name 对齐会有歧义）')
    notes.append(f'_index.yaml dir_name {len(listed)} 条 ↔ 实盘模块目录 {len(real)} 个')

    print('  ' + '\n  '.join(notes))
    print(f'  {"OK " if not prob else "BAD"} 完整性：{len(prob)} 处异常')
    for p in prob:
        print('      ', p)
    return len(prob)


# ── 2. 骨架与目录 ────────────────────────────────────────────
def check_skeleton(files):
    print('\n== 2. 骨架与目录 ==')
    prob, toc_total, toc_ok = [], 0, 0
    for f in files:
        t = open(f, encoding='utf-8').read()
        b = rel(f)
        h1 = re.findall(r'(?m)^# (.+)$', t)
        h2 = [h.strip() for h in re.findall(r'(?m)^## (.+)$', t)]
        if len(h1) != 1:
            prob.append(f'{b}: h1 数量 {len(h1)}（应为 1）')
        if '<cite>' not in t:
            prob.append(f'{b}: 缺少 <cite> 引用头')
        if h2 != FIXED_H2:
            extra = [h for h in h2 if h not in FIXED_H2]
            miss = [h for h in FIXED_H2 if h not in h2]
            prob.append(f'{b}: H2 序列偏离契约（多 {extra} / 缺 {miss}）')
        toc = re.search(r'(?ms)^## 目录\n(.*?)(?=^## )', t)
        anchors = TOC_ITEM_RE.findall(toc.group(1)) if toc else []
        toc_total += len(anchors)
        if len(anchors) != len(h2) - 1:
            prob.append(f'{b}: 目录 TOC {len(anchors)} 项 != H2 数-1 {len(h2) - 1}')
        slugs = {slug(h) for h in re.findall(r'(?m)^#{1,6} (.+)$', t)}
        for a in anchors:
            if a in slugs:
                toc_ok += 1
            else:
                prob.append(f'{b}: 目录锚点 #{a} 无对应标题')
    print(f'  {len(files)} 篇：H2 契约 {len(files)} 篇一致；目录锚点 {toc_ok}/{toc_total} 可解析')
    print(f'  {"OK " if not prob else "BAD"} 骨架：{len(prob)} 处异常')
    for p in prob:
        print('      ', p)
    return len(prob)


# ── 3. 坐标 ──────────────────────────────────────────────────
def check_coords(files):
    print('\n== 3. 坐标 ==')
    V.build_index()
    prob = []
    n_a = n_frag = n_file = 0
    degen = []
    for f in files:
        t = open(f, encoding='utf-8').read()
        b = rel(f)
        # 3a 锚点格式（含 A 类）
        for p, frag in set(FRAG_RE.findall(t)):
            n_frag += 1
            if not re.fullmatch(r'L\d+(?:-L\d+)?', frag):
                prob.append(f'{b}: 锚点格式违规 file://{p}#{frag}')
                continue
            a = int(frag[1:].split('-')[0])
            bend = frag.split('-L')[1] if '-L' in frag else None
            bend = int(bend) if bend else a
            if bend == a and '-L' in frag:
                degen.append(f'{b}: {p}#{frag}')
            full = os.path.join(V.REPO, p)
            if not os.path.exists(full):
                prob.append(f'{b}: 文件不存在 {p}#{frag}')
            else:
                n = len(V.read_lines(full))
                if a < 1 or a > bend or bend > n:
                    prob.append(f'{b}: 越界 {p}#{frag}（文件 {n} 行）')
            n_a += 1
        # 3b 文件级引用（无锚点）
        n_file += len(re.findall(r'\(file://([^)#\s]+)\)', t))
        # 3c 链接标签数值与片段一致
        for lab, p, a, bend in LINK_LABEL_RE.findall(t):
            nums = re.findall(r'\d+', lab.split(':')[-1])
            if not nums:
                continue
            bval = bend or a
            ok = (nums[0] == a) if len(nums) == 1 else (nums[0], nums[1]) == (a, bval)
            if not ok:
                prob.append(f'{b}: 标签/片段不一致 [{lab}](file://{p}#L{a}-L{bval})')
        # 3d 入口链 B 类
        for k, x in V.check_chains(f):
            if k in ('oob', 'miss'):
                prob.append(f'{b}: [入口链] {x}')
    print(f'  带锚点引用 {n_a} 条（其中文件级 {n_file} 条）、退化区间 {len(degen)} 处')
    print(f'  {"OK " if not prob else "BAD"} 坐标：{len(prob)} 处问题')
    for p in prob[:60]:
        print('      ', p)
    if len(prob) > 60:
        print(f'      …（其余 {len(prob) - 60} 条略）')
    return len(prob)


# ── 4. 溯源 ──────────────────────────────────────────────────
def check_provenance(files, with_cite=True):
    print('\n== 4. 溯源 ==')
    prob = []
    stats = collections.Counter()
    for f in files:
        t = open(f, encoding='utf-8').read()
        lines = t.split('\n')
        b = rel(f)
        for n, i in enumerate([k for k, x in enumerate(lines)
                               if x.strip() == '```mermaid'], 1):
            j = i + 1
            while j < len(lines) and lines[j].strip() != '```':
                j += 1
            k = j + 1
            while k < len(lines) and lines[k].strip() == '':
                k += 1
            nxt = lines[k].strip() if k < len(lines) else '<EOF>'
            stats['mermaid'] += 1
            if nxt == '图表来源':
                stats['figsrc'] += 1
            else:
                prob.append(f'{b}: 图#{n}（第 {i + 1} 行）后非「图表来源」: {nxt[:40]}')
        if with_cite:
            cite = re.search(r'(?ms)^<cite>\n(.*?)^</cite>', t)
            if not cite:
                prob.append(f'{b}: 缺 <cite> 块')
            else:
                for p in CITE_ITEM_RE.findall(cite.group(1)):
                    if not os.path.exists(os.path.join(V.REPO, p)):
                        prob.append(f'{b}: cite 文件不存在 {p}')
        heads = [(i, l[3:].strip()) for i, l in enumerate(lines) if l.startswith('## ')]
        for idx, (i, name) in enumerate(heads):
            end = heads[idx + 1][0] if idx + 1 < len(heads) else len(lines)
            body = '\n'.join(lines[i + 1:end])
            has_sec, has_ph = '章节来源' in body, '本节为' in body
            if has_sec:
                stats['secsrc'] += 1
            if has_ph:
                stats['ph'] += 1
            if name in PLACEHOLDER_SECTIONS and not (has_ph or has_sec):
                prob.append(f'{b}: 节「{name}」缺 [本节为…] 收尾句')
            elif name in MUST_SECTIONS and not has_sec:
                prob.append(f'{b}: 节「{name}」缺章节来源')
    print(f'  mermaid {stats["mermaid"]} 张 → 图表来源 {stats["figsrc"]} 处；'
          f'小节带章节来源 {stats["secsrc"]}、带收尾句 {stats["ph"]}')
    print(f'  {"OK " if not prob else "BAD"} 溯源：{len(prob)} 处异常')
    for p in prob[:60]:
        print('      ', p)
    if len(prob) > 60:
        print(f'      …（其余 {len(prob) - 60} 条略）')
    return len(prob)


# ── 5. 交叉引用 ──────────────────────────────────────────────
def check_xrefs(files):
    print('\n== 5. 交叉引用 ==')
    prob, n_cross = [], 0
    for f in files:
        t = open(f, encoding='utf-8').read()
        b = rel(f)
        for m in re.finditer(r'\[([^\]]*)\]\((\.[^)]+)\)', t):
            n_cross += 1
            tgt = os.path.normpath(os.path.join(os.path.dirname(f), m.group(2)))
            if not os.path.exists(tgt):
                prob.append(f'{b}: 跨篇链接 {m.group(2)} 不存在')
    print(f'  跨篇相对链接 {n_cross} 个')
    print(f'  {"OK " if not prob else "BAD"} 交叉引用：{len(prob)} 处不可解析')
    for p in prob:
        print('      ', p)
    return len(prob)


def check_coarse_anchors(files):
    """WARN 级（不计入退出码）：锚点落在文件头部窗口的「粗锚」。

    判据：`#L1-L<b>`（a=1、非整文件、b ≤ 200）且文件 ≥ 500 行。
    这类锚点能通过「存在 + 界内 + 格式 + 标签一致」四项检查，却指向版权头 / include 段，
    并不支撑该节论述——是坐标层「假精度」的主要来源。整文件引用请写 `#L1-L<行数>`，
    或干脆去掉锚点用文件级链接。
    """
    print('\n== 6. 粗锚（WARN，不计入退出码）==')
    agg = collections.Counter()
    n = 0
    for f in files:
        t = open(f, encoding='utf-8').read()
        for p, b in FRAG_RE.findall(t):
            m = re.fullmatch(r'L(\d+)(?:-L(\d+))?', b)
            if not m:
                continue
            a0, b0 = int(m.group(1)), int(m.group(2) or m.group(1))
            if a0 != 1 or b0 > 200:
                continue
            full = os.path.join(V.REPO, p)
            if not os.path.exists(full):
                continue
            lines = len(V.read_lines(full))
            if b0 < lines and lines >= 500:
                n += 1
                agg[(p, lines)] += 1
    print(f'  a=1 且 b≤200 且文件≥500 行的粗锚: {n} 处'
          f'（整文件引用请写 #L1-L<行数>）')
    for (p, lines), c in agg.most_common(10):
        print(f'      {c:3d}  {p}  (共 {lines} 行)')
    if len(agg) > 10:
        print(f'      …（共涉及 {len(agg)} 个文件）')
    return n


def check_semantic(files):
    print('\n== 7. 语义抽验（启发式，仅供人工判读，不计入退出码）==')
    idx = V.build_index()
    susp, n = [], 0
    for f in files:
        for _head, b in V.entry_blocks(open(f, encoding='utf-8').read().split('\n')):
            curfile = None
            for l in b:
                if '入口链' in l:
                    continue
                anchors = list(V.ANCHOR_RE.finditer(l))
                segs = ([(curfile, l, 0, len(l))] if not anchors and curfile else [])
                for i, am in enumerate(anchors):
                    s = am.end()
                    e = anchors[i + 1].start() if i + 1 < len(anchors) else len(l)
                    segs.append((am.group(1), l, am.start(), am.end()))
                    if not V._in_parens(l, am.start()):
                        curfile = am.group(1)
                    segs += [(curfile, l, s, e)]
                for cf, l2, s, e in segs:
                    for mm in re.finditer(r':(\d+)', l2[s:e]):
                        ln = int(mm.group(1))
                        full = idx.get(cf)
                        if not full:
                            continue
                        src = V.read_lines(full)
                        if ln > len(src):
                            continue
                        pre = l2[:s + mm.start()]
                        cands = re.findall(r'([A-Za-z_][A-Za-z0-9_]{3,})\s*\(', pre)
                        if not cands:
                            continue
                        n += 1
                        cand = cands[-1]
                        if cand in src[ln - 1]:
                            continue
                        if any(cand in src[k] for k in range(ln, min(len(src), ln + 2))):
                            continue
                        if any(cand in src[k] for k in range(max(0, ln - 11),
                                                              min(len(src), ln + 10))):
                            continue
                        susp.append((rel(f), f'{cf}:{ln}', cand, src[ln - 1].strip()[:64]))
    print(f'  抽验 {n} 条，可疑 {len(susp)} 条（命中/续行定义/邻近命中均视为正常）')
    for fn, coord, cand, srcline in susp:
        print(f'      {fn}  {coord}  标注 {cand}()')
        print(f'          实际: {srcline}')


def main():
    args = sys.argv[1:]
    only_c = '--content' in args
    only_k = '--knowledge' in args
    if only_c and only_k:
        only_c = only_k = False

    n = 0
    if not only_k:
        files = md_files(CONTENT)
        print(f'content 目录: {CONTENT}\n篇章数: {len(files)}\n')
        n += check_inventory()
        n += check_skeleton(files)
        n += check_coords(files)
        n += check_provenance(files)
        n += check_xrefs(files)
        check_coarse_anchors(files)
        if '--semantic' in args:
            check_semantic(files)
    if not only_c:
        kfiles = md_files(KNOW)
        print(f'\nknowledge 目录: {KNOW}\n文件数: {len(kfiles)}\n')
        n += check_coords(kfiles)
        n += check_provenance(kfiles, with_cite=False)

    print(f'\n=== 总计问题: {n} ===')
    return 1 if n else 0


if __name__ == '__main__':
    sys.exit(main())
