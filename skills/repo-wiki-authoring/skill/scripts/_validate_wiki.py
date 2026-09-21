import os, re

# 路径按脚本位置推导（本脚本位于 notes-hub/projects/postgres/wiki/scripts/），
# 源码仓按 project.yaml 的 source_repo 解析，换机器只需同级 clone 即可复用。
_HERE = os.path.dirname(os.path.abspath(__file__))       # .../wiki/scripts
PROJ = os.path.dirname(os.path.dirname(_HERE))           # .../projects/postgres
NOTES = os.path.dirname(os.path.dirname(PROJ))           # notes-hub 仓根
C = os.path.join(PROJ, 'wiki', 'repowiki', 'zh', 'content')
T = os.path.join(PROJ, 'wiki', 'repowiki', 'zh', 'meta', 'coverage-extension.tsv')

_rel, _line = '../postgres', None
try:
    for _line in open(os.path.join(PROJ, 'project.yaml'), encoding='utf-8'):
        _m = re.match(r'\s*source_repo:\s*(\S+)', _line)
        if _m:
            _rel = _m.group(1)
            break
except OSError:
    pass
S = os.path.normpath(os.path.join(NOTES, _rel))

import sys
rows = [l.rstrip('\n').split('\t') for l in open(T, encoding='utf-8')][1:]
targets = set(sys.argv[1:]) or {'19', '20', '21'}
prob = []
for r in rows:
    if r[0] not in targets:
        continue
    p = os.path.join(C, r[3])
    if not os.path.exists(p):
        prob.append((r[0], 'MISSING_PAGE', p))
        continue
    t = open(p, encoding='utf-8').read()
    h2 = len(re.findall(r'(?m)^## ', t))
    mermaid = len(re.findall(r'```mermaid', t))
    figsrc = len(re.findall(r'(?m)^图表来源', t))
    refs = re.findall(r'\(file://([^)#]+)#L(\d+)-L(\d+)\)', t)
    # covers 命中
    cover_miss = [c for c in r[4].split(',') if not os.path.exists(os.path.join(S, c.strip()))]
    missf = sorted({f for f, _, _ in refs if not os.path.exists(os.path.join(S, f))})
    oob = []
    for f, a, b in refs:
        fp = os.path.join(S, f)
        if os.path.exists(fp):
            n = sum(1 for _ in open(fp, encoding='utf-8', errors='replace'))
            if int(a) < 1 or int(a) > int(b) or int(b) > n:
                oob.append((f, a, b, n))
    if h2 != 11:
        prob.append((r[0], 'H2=%d' % h2))
    if mermaid > figsrc:
        prob.append((r[0], 'MERMAID>图表来源', mermaid, figsrc))
    if missf:
        prob.append((r[0], 'MISSFILE', missf[:5]))
    if oob:
        prob.append((r[0], 'OOB', oob[:5]))
    if cover_miss:
        prob.append((r[0], 'COVERS_MISS', cover_miss))
    print('idx%-3s %-28s h2=%d mermaid=%d 图表来源=%d refs=%d' % (r[0], r[2], h2, mermaid, figsrc, len(refs)))

print('---')
print('TOTAL PROBLEMS:', len(prob))
for x in prob:
    print(x)
