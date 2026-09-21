#!/usr/bin/env python3
"""官方扩展集「全章统一校验」：骨架一致 / 坐标不越界 / 交叉引用可解析。

三项检查：
  1. 骨架一致 —— 全章各篇的 h2 标题序列是否统一（以出现最多的骨架为基准）、
     是否都有 `<cite>` 引用头、`## 目录` 的 TOC 项数是否等于 h2 数 - 1。
  2. 坐标不越界 —— A 类 `file://path#L<a>-L<b>` 链接；
     B 类 入口链代码块内的 `文件.c:NN` 锚点与裸 `:NN`（上下文按锚点切换，跨行继承）。
  3. 交叉引用可解析 —— `## 目录` 里的 `#锚点` 能否落到本页某个标题；
     指向同目录其他 .md 的相对链接是否存在。
  4. 溯源完备 —— 每张 mermaid 后紧跟 `图表来源`；链接标签的行号与 `#L<a>-L<b>`
     片段一致；`<cite>` 内文件存在；实质小节（`项目结构`/`核心组件`/`详细组件分析`/
     `依赖关系分析`/`故障排查指南`）必须有 `章节来源`；占位小节（`性能考量`/`结论`/
     `附录`）必须有 `[本节为…]` 收尾句。豁免规则取自全库既有 210 篇的落地惯例：
     `目录`、`简介`、`架构总览` 允许两者皆无（`简介` 207/210 篇不带 `章节来源`）。

可选：--semantic 追加入口链「语义抽验」——检查该行标注的函数名是否真的出现在
源码那一行。此项存在**已知误报**（PG 的 `static void` / `Datum` 单独成行定义风格、
以及入口链里引用注释行），输出只作人工判读线索，不计入退出码。

用法：
    python3 _validate_chapter.py                     # 校验默认章节
    python3 _validate_chapter.py --dir <目录>
    python3 _validate_chapter.py --semantic

退出码：0 = 三项检查全部通过；1 = 存在问题。
"""
import os
import re
import sys
import glob
import collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _validate_coords as V

# 路径按脚本位置推导（本脚本位于 notes-hub/projects/postgres/wiki/scripts/）
_PROJ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEFAULT_DIR = os.path.join(_PROJ, 'wiki', 'repowiki', 'zh', 'content',
                           '扩展系统', '官方扩展集')


def slug(title):
    """GitHub 风格锚点：小写、去标点、空白转连字符（保留 CJK）。"""
    s = title.strip().lower()
    s = re.sub(r'[^\w\s\u4e00-\u9fff-]', '', s)
    return re.sub(r'\s+', '-', s)


# ── 1. 骨架一致 ──────────────────────────────────────────────
def check_skeleton(files):
    print('== 1. 骨架一致 ==')
    sigs, problems = {}, []
    for f in files:
        t = open(f, encoding='utf-8').read()
        h1 = re.findall(r'(?m)^# (.+)$', t)
        h2 = [h.strip() for h in re.findall(r'(?m)^## (.+)$', t)]
        sigs[f] = tuple(h2)
        if len(h1) != 1:
            problems.append(f'{os.path.basename(f)}: h1 数量 {len(h1)}（应为 1）')
        if '<cite>' not in t:
            problems.append(f'{os.path.basename(f)}: 缺少 <cite> 引用头')
        toc = re.search(r'(?ms)^## 目录\n(.*?)(?=^## )', t)
        n_toc = len(re.findall(r'\]\(#', toc.group(1))) if toc else -1
        if n_toc != len(h2) - 1:
            problems.append(
                f'{os.path.basename(f)}: 目录 TOC {n_toc} 项 != h2 数-1 {len(h2) - 1}')

    cnt = collections.Counter(sigs.values())
    base, base_n = cnt.most_common(1)[0]
    print(f'  基准骨架（{base_n}/{len(files)} 篇共享，{len(base)} 个 h2）: '
          + ' / '.join(base))
    for sig, n in cnt.most_common():
        if sig == base:
            continue
        diff = [h for h in sig if h not in base] + [h for h in base if h not in sig]
        problems.append(f'{n} 篇骨架与基准不同，差异: {diff}')
    print(f'  {"OK " if not problems else "BAD"} 骨架一致：{len(files)} 篇，'
          f'{len(problems)} 处异常')
    for p in problems:
        print('      ', p)
    return len(problems)


# ── 2. 坐标不越界 ────────────────────────────────────────────
def check_coords(files):
    print('\n== 2. 坐标不越界 ==')
    V.build_index()
    ta = tb = 0
    for f in files:
        n_a, bad_a = V.check_links(f)
        ta += len(bad_a)
        for b in bad_a:
            print(f'      [A] {os.path.basename(f)}: {b}')
        res = V.check_chains(f)
        bad_b = [x for k, x in res if k in ('oob', 'miss')]
        n_b = len([1 for k, _ in res if k == 'ok'])
        tb += len(bad_b)
        for b in bad_b:
            print(f'      [B] {os.path.basename(f)}: {b}')
        print(f'   {os.path.basename(f):<28} A={n_a:<4} B={n_b:<4}')
    print(f'  {"OK " if not (ta + tb) else "BAD"} 坐标：A 类 + B 类共 {ta + tb} 处越界/缺文件')
    return ta + tb


# ── 3. 交叉引用可解析 ────────────────────────────────────────
def check_xrefs(files):
    print('\n== 3. 交叉引用可解析 ==')
    n_anchor = n_ok = 0
    cross, bad = [], []
    for f in files:
        t = open(f, encoding='utf-8').read()
        slugs = {slug(h) for h in re.findall(r'(?m)^#{1,6} (.+)$', t)}
        for a in re.findall(r'\]\(#([^)]+)\)', t):
            n_anchor += 1
            if a in slugs:
                n_ok += 1
            else:
                bad.append(f'{os.path.basename(f)}: 锚点 #{a} 无对应标题')
        for m in re.finditer(r'\[([^\]]*)\]\((\.[^)]+)\)', t):
            tgt = os.path.normpath(os.path.join(os.path.dirname(f), m.group(2)))
            cross.append((os.path.basename(f), m.group(2)))
            if not os.path.exists(tgt):
                bad.append(f'{os.path.basename(f)}: 跨篇链接 {m.group(2)} 不存在')
    print(f'  目录锚点   {n_ok}/{n_anchor} 可解析')
    print(f'  跨篇链接   {len(cross)} 个（' +
          (', '.join(f'{a}→{b}' for a, b in cross) or '无') + '）')
    print(f'  {"OK " if not bad else "BAD"} 交叉引用：{len(bad)} 处不可解析')
    for b in bad:
        print('      ', b)
    return len(bad)


# ── 4. 溯源完备（图表来源 / 标签一致性 / cite 存在 / 小节收尾）──
# 分节要求取自全库既有 210 篇的落地惯例 TERM-less 统计：
MUST_SECTIONS = {'项目结构', '核心组件', '详细组件分析', '依赖关系分析', '故障排查指南'}
PLACEHOLDER_SECTIONS = {'性能考量', '结论', '附录'}
FREE_SECTIONS = {'目录', '简介', '架构总览'}
LINK_LABEL_RE = re.compile(r'\[([^\]]+)\]\(file://([^)#]+)#L(\d+)(?:-L(\d+))?\)')
CITE_ITEM_RE = re.compile(r'^\- \[[^\]]+\]\(file://([^)#]+)\)$', re.M)


def check_provenance(files):
    print('\n== 4. 溯源完备 ==')
    bad = []
    stats = {'mermaid': 0, 'figsrc': 0, 'secsrc': 0, 'ph': 0}
    for f in files:
        text = open(f, encoding='utf-8').read()
        lines = text.split('\n')
        b = os.path.basename(f)

        # 4a 每张 mermaid 之后必须紧跟「图表来源」
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
                bad.append(f'{b}: 图#{n}（第 {i + 1} 行）后紧跟的不是图表来源: {nxt[:40]}')

        # 4b 链接标签行号与 URL 片段一致
        for lab, p, a, bend in LINK_LABEL_RE.findall(text):
            nums = re.findall(r'\d+', lab.split(':')[-1])
            if not nums:
                continue
            bval = bend or a
            ok = (nums[0] == a) if len(nums) == 1 else (nums[0], nums[1]) == (a, bval)
            if not ok:
                bad.append(f'{b}: 标签与片段不一致 '
                           f'[{lab}](file://{p}#L{a}-L{bval})')

        # 4c <cite> 内的文件必须存在
        cite = re.search(r'(?ms)^<cite>\n(.*?)^</cite>', text)
        if cite:
            for p in CITE_ITEM_RE.findall(cite.group(1)):
                if not os.path.exists(os.path.join(V.REPO, p)):
                    bad.append(f'{b}: cite 文件不存在 {p}')

        # 4d 小节收尾
        heads = [(i, l[3:].strip()) for i, l in enumerate(lines) if l.startswith('## ')]
        for idx, (i, name) in enumerate(heads):
            end = heads[idx + 1][0] if idx + 1 < len(heads) else len(lines)
            body = '\n'.join(lines[i + 1:end])
            has_sec, has_ph = '章节来源' in body, '本节为' in body
            if has_sec:
                stats['secsrc'] += 1
            if has_ph:
                stats['ph'] += 1
            if name in FREE_SECTIONS:
                continue
            if name in PLACEHOLDER_SECTIONS and not (has_ph or has_sec):
                bad.append(f'{b}: 节「{name}」缺 [本节为…] 收尾句')
            elif name in MUST_SECTIONS and not has_sec:
                bad.append(f'{b}: 节「{name}」缺章节来源')
    print(f'  mermaid {stats["mermaid"]} 张 → 图表来源 {stats["figsrc"]} 处；'
          f'小节带章节来源 {stats["secsrc"]} 个、带收尾句 {stats["ph"]} 个')
    print(f'  {"OK " if not bad else "BAD"} 溯源完备：{len(bad)} 处异常')
    for x in bad:
        print('      ', x)
    return len(bad)


# ── 可选：语义抽验 ───────────────────────────────────────────
def _classify(src, ln, cand):
    """判定坐标与标注函数名的关系。

    hit  坐标行本身就含该函数名
    cont 续行定义：PG 把返回类型单独成行（`Datum` / `static char *`），
         坐标指向定义起始行、函数名在紧随的 1~2 行内 —— 合法写法
    near 邻近：函数在坐标 ±10 行内（入口链常标「调用点附近」或「声明 / 定义」两处）
    susp 三者都不符，才需要人工判读
    """
    if cand in src[ln - 1]:
        return 'hit'
    for k in range(ln, min(len(src), ln + 2)):
        if cand in src[k]:
            return 'cont'
    for k in range(max(0, ln - 11), min(len(src), ln + 10)):
        if cand in src[k]:
            return 'near'
    return 'susp'


def check_semantic(files):
    print('\n== 4. 语义抽验（启发式，仅供人工判读，不计入退出码）==')
    idx = V.build_index()
    susp, near, n = [], [], 0
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
                    # 锚点自带文件名，照常按它自身抽验
                    segs.append((am.group(1), l, am.start(), am.end()))
                    # 括号里顺带提及的文件（`见 c.h:1068`）不接管后续归属
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
                        # 候选名取坐标「前面最近」的函数名，而不是整行所有函数名：
                        # 入口链常写 `A → B   file.c:N1 / :N2`（一跳多目标），
                        # 取整行会把 A、B 都当成 N1 的期望函数，造成大量误报。
                        pre = l2[:s + mm.start()]
                        cands = re.findall(r'([A-Za-z_][A-Za-z0-9_]{3,})\s*\(', pre)
                        if not cands:
                            continue
                        n += 1
                        cand = cands[-1]
                        k = _classify(src, ln, cand)
                        if k == 'susp':
                            susp.append((os.path.basename(f), f'{cf}:{ln}',
                                         cand, src[ln - 1].strip()[:64]))
                        elif k == 'near':
                            near.append((os.path.basename(f), f'{cf}:{ln}', cand))
    print(f'  抽验 {n} 条：行内命中 / 续行定义 均视为正常，'
          f'邻近命中 {len(near)} 条，可疑 {len(susp)} 条')
    for fn, coord, cand, srcline in susp:
        print(f'      {fn}  {coord}  标注 {cand}()')
        print(f'          实际: {srcline}')
    if near:
        print(f'  （邻近命中明细：{len(near)} 条，多为「调用点 / 声明-定义」两处标注）')
        for fn, coord, cand in near:
            print(f'      near  {fn}  {coord}  {cand}()')


def main():
    args = sys.argv[1:]
    d = DEFAULT_DIR
    if '--dir' in args:
        d = args[args.index('--dir') + 1]
    files = sorted(glob.glob(os.path.join(d, '*.md')))
    print(f'全章目录: {d}\n篇章数  : {len(files)}\n')
    if not files:
        print('未找到 .md')
        return 1
    n = (check_skeleton(files) + check_coords(files)
         + check_xrefs(files) + check_provenance(files))
    if '--semantic' in args:
        check_semantic(files)
    print(f'\n=== 总计问题: {n} ===')
    return 1 if n else 0


if __name__ == '__main__':
    sys.exit(main())
