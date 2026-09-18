# -*- coding: utf-8 -*-
"""
把六次 ChatGPT 分享快照，重建成"六阶段"存档。
数据源：六份原始 HTML（保真），不依赖任何中间产物。

依赖：阶段四、阶段六的生成器需要 PyYAML。请用装好 pyyaml 的解释器运行：
      C:\\Users\\zhang\\.workbuddy\\binaries\\python\\envs\\default\\Scripts\\python.exe -X utf8 build_archive.py

各阶段构建方式（这是理解本脚本的关键）：
  阶段一/二/三  shell heredoc 逐文件写入（cat > f <<'EOF'），再叠后置编辑
  阶段四       沙箱内自包含 python 生成器（执行代码本身，最保真）
  阶段五       shell heredoc 一次性从零生成 12 个文件（整包重写，大幅瘦身）
  阶段六       先把阶段四的 v0.4 整包复制成基线，再依次执行两个 python 脚本做增量合并
               （[347] 写 15 个文件 / 覆写 2 个；[353] 追加 SHA-256 基线清单并升级完整性测试）
               —— 唯一一个「不重写、只合并」的版本
"""
import json, re, os, shutil, zipfile, datetime, traceback, sys, ast

HERE = os.path.dirname(os.path.abspath(__file__))
LOG = open(os.path.join(HERE, "_build_archive.log"), "w", encoding="utf-8")
def p(*a): LOG.write(" ".join(str(x) for x in a) + "\n"); LOG.flush()

def _excepthook(et, ev, tb):
    LOG.write("\n!!! 异常 !!!\n" + "".join(traceback.format_exception(et, ev, tb)) + "\n")
    LOG.close()
sys.excepthook = _excepthook

# ============================================================
# 一、解析器：从 SSR 页面里还原 React Router 的索引压缩数据
# ============================================================
def extract_chunks(h):
    res, key, pos = [], "streamController.enqueue(", 0
    while True:
        i = h.find(key, pos)
        if i < 0: break
        j = i + len(key)
        while j < len(h) and h[j] in " \t\r\n": j += 1
        if h[j] != '"':
            pos = j; continue
        k = j + 1; buf = []
        while k < len(h):
            c = h[k]
            if c == '\\': buf.append(h[k:k+2]); k += 2; continue
            if c == '"': break
            buf.append(c); k += 1
        res.append(json.loads('"' + "".join(buf) + '"'))
        pos = k
    return res

def load_route(html_path):
    html = open(html_path, encoding="utf-8").read()
    flat = None
    for c in extract_chunks(html):
        try:
            v = json.loads(c)
        except Exception:
            continue
        if isinstance(v, list) and len(v) > 100:
            flat = v; break
    assert flat is not None, "no flat payload in " + html_path

    cache = {}
    def resolve(i, depth=0):
        if depth > 400: return "<<deep>>"
        if i is None or isinstance(i, bool): return i
        if isinstance(i, int):
            if i < 0: return None
            if i in cache: return cache[i]
            if i >= len(flat): return None
            cache[i] = None
            cache[i] = build(flat[i], depth + 1)
            return cache[i]
        return build(i, depth + 1)

    def build(v, depth=0):
        if isinstance(v, dict):
            if v and all(isinstance(k, str) and re.fullmatch(r"_\d+", k) for k in v):
                o = {}
                for k, vi in v.items():
                    o[str(resolve(int(k[1:]), depth + 1))] = resolve(vi, depth + 1)
                return o
            return {k: resolve(x, depth + 1) for k, x in v.items()}
        if isinstance(v, list):
            return [resolve(x, depth + 1) for x in v]
        return v

    root = resolve(0)
    ld = root["loaderData"]
    rk = [k for k in ld if "share" in k][0]
    return ld[rk]["serverResponse"]["data"], html

# ============================================================
# 二、heredoc 写入抽取
# ============================================================
HEREDOC_NEW = re.compile(r"cat\s*>\s*(\"[^\"]+\"|\S+)\s*<<\s*'EOF'\n(.*?)\nEOF\n", re.S)
HEREDOC_APP = re.compile(r"cat\s*>>\s*(\"[^\"]+\"|\S+)\s*<<\s*'EOF'\n(.*?)\nEOF\n", re.S)

def relpath(path, root=None):
    """把沙箱绝对路径折算成包内相对路径。
    root 是脚本里的 $ROOT 值；v0.5 的根目录带 -v0.5 后缀，
    只靠 rfind("source-code-reading-skill/") 会失手，所以优先用 root 前缀切。"""
    if root:
        r = root.strip().strip('"').rstrip("/")
        if r and path.startswith(r + "/"):
            return path[len(r) + 1:]
    key = "source-code-reading-skill/"
    i = path.rfind(key)
    if i >= 0: return path[i + len(key):]
    return path.lstrip("/")

def writes_of(text):
    root = None
    m = re.search(r"^ROOT=(.+)$", text, re.M)
    if m: root = m.group(1).strip()
    d = {}
    for mt in HEREDOC_NEW.finditer(text):
        raw = mt.group(1).strip().strip('"')
        path = raw.replace("${ROOT}", root or "").replace("$ROOT", root or "")
        d[relpath(path, root)] = mt.group(2)
    return d

def appends_of(text):
    root = None
    m = re.search(r"^ROOT=(.+)$", text, re.M)
    if m: root = m.group(1).strip()
    d = {}
    for mt in HEREDOC_APP.finditer(text):
        raw = mt.group(1).strip().strip('"')
        path = raw.replace("${ROOT}", root or "").replace("$ROOT", root or "")
        d[relpath(path, root)] = mt.group(2)
    return d

def code_nodes(lc):
    out = []
    for i, n in enumerate(lc):
        m = n.get("message")
        if not m: continue
        c = m.get("content") or {}
        if c.get("content_type") == "code":
            out.append((i, c.get("text") or ""))
    return out

# ============================================================
# 三、重建各阶段技能包（纯函数：仅依赖该快照自身的数据）
# ============================================================
def build_v01(nodes):
    """v0.1 = 那个一次性写入 15 个文件的 bundle 节点"""
    cands = [(i, t, writes_of(t)) for i, t in nodes
             if "version: 0.1.0" in t and "lock-manager-plan.yaml" in t and len(t) > 20000]
    assert len(cands) >= 1, "v0.1 bundle node not found"
    i, t, w = max(cands, key=lambda x: len(x[2]))
    p(f"  [v0.1] bundle 节点 = [{i}]  写入 {len(w)} 文件")
    return w, i

def build_overwrites(nodes):
    """v0.2 覆写集 = 写入 version 0.2.0 的 SKILL.md 的那个节点"""
    cands = []
    for i, t in nodes:
        w = writes_of(t)
        if "SKILL.md" in w and "version: 0.2.0" in w["SKILL.md"]:
            cands.append((i, t, w))
    assert len(cands) == 1, f"expect exactly 1 v0.2 overwrite node, got {[c[0] for c in cands]}"
    i, t, w = cands[0]
    p(f"  [v0.2] 覆写节点 = [{i}]  覆写/新增 {sorted(w)}")
    return w, i

def build_mid(nodes):
    """v0.2 的中间修订节点：写了 diagram-catalog 但没写 SKILL.md 的那个
    —— 它的产出因 [100] 从 v0.1.zip 重新解压当底本而被整批丢弃"""
    mid, idxs = {}, []
    for i, t in nodes:
        w = writes_of(t)
        if "references/diagrams/diagram-catalog.md" in w and "SKILL.md" not in w:
            mid.update(w); idxs.append(i)
    p(f"  [中间修订] 节点 = {idxs}  写入 {sorted(mid)}")
    return mid, idxs

def build_ks(nodes):
    """v0.3 新增 = knowledge-sources/ 的四次 heredoc 写入"""
    merged, idxs = {}, []
    for i, t in nodes:
        w = writes_of(t)
        ks = {k: v for k, v in w.items() if k.startswith("knowledge-sources/")}
        if ks:
            merged.update(ks); idxs.append(i)
    assert len(merged) == 4, f"expect 4 knowledge-sources files, got {sorted(merged)}"
    p(f"  [v0.3] knowledge-sources 写入节点 = {idxs}  文件 {sorted(merged)}")
    return merged, idxs

def build_edits(nodes):
    """v0.3 的后置编辑：SKILL.md / README.md 的 python 插入 + index.yaml 的替换 + 追加块"""
    skill_insert = skill_contract = readme_add = None
    name_repls = None
    sed_ver = sed_url = append_block = None
    for i, t in nodes:
        m = re.search(r"insert = '''(.*?)'''", t, re.S)
        if m and "External knowledge sources" in m.group(1):
            skill_insert = m.group(1)
            rest = re.findall(r"s \+= '''(.*?)'''", t, re.S)
            for r in rest:
                if "Knowledge-source registry contract" in r: skill_contract = r
                elif "External learning registry" in r: readme_add = r
            p(f"  [v0.3] SKILL.md 插入块来源 = [{i}]  ({len(skill_insert)} chars)")
        if "s.replace('    name: Documenting" in t:
            # 源码里是字面 \n 转义，还原成真换行才能命中 YAML
            name_repls = [(a.replace("\\n", "\n"), b.replace("\\n", "\n"))
                          for a, b in re.findall(r"s=s\.replace\('(.*?)', '(.*?)'\)\n", t)]
            p(f"  [v0.3] index.yaml 名称加引号 = [{i}]  {len(name_repls)} 条")
            for a, b in name_repls:
                p("        -", repr(a), "=>", repr(b))
        if "sed -i 's/version: 0.2.0/version: 0.3.0/'" in t:
            sed_ver = True
            for a in HEREDOC_APP.finditer(t):
                if "Decision tree" in a.group(2):
                    append_block = a.group(2)
            m = re.search(r"sed -i 's#([^#]+)#([^#]+)#' knowledge-sources/index.yaml", t)
            if m: sed_url = (m.group(1), m.group(2))
            p(f"  [v0.3] sed 版本号 + 追加决策树 = [{i}]  ({len(append_block or '')} chars)")
    assert all(x is not None for x in
               (skill_insert, skill_contract, readme_add, name_repls, sed_ver, sed_url, append_block)), \
        "v0.3 编辑链抽取不完整"
    # 这三段来自 python 源码里的 '''...''' 字面量，\n 是两字符转义，需还原成真换行
    # （append_block 来自 shell heredoc，本身已是真换行，不能动）
    def unesc(s): return s.replace("\\n", "\n").replace("\\t", "\t")
    skill_insert, skill_contract, readme_add = unesc(skill_insert), unesc(skill_contract), unesc(readme_add)
    p(f"    换行还原后：insert {len(skill_insert)} / contract {len(skill_contract)} / readme {len(readme_add)}")
    return dict(skill_insert=skill_insert, skill_contract=skill_contract, readme_add=readme_add,
                name_repls=name_repls, sed_url=sed_url, append_block=append_block)

def apply_v03(v02, ks, ed):
    f = dict(v02)
    f.update(ks)

    # (1) [159] SKILL.md：在 "# Six-stage execution" 前插入外部知识源章节
    s = f["SKILL.md"]
    marker = "\n# Six-stage execution\n"
    assert marker in s, "marker '# Six-stage execution' not found in v0.2 SKILL.md"
    s = s.replace(marker, ed["skill_insert"] + "# Six-stage execution\n", 1)
    s += ed["skill_contract"]
    assert re.search(r"^## External knowledge sources$", s, re.M), "插入章标题未成行"
    assert re.search(r"^# Six-stage execution$", s, re.M), "Six-stage 标记未成行"
    assert re.search(r"^## Knowledge-source registry contract$", s, re.M), "contract 段未成行"
    # (3) [172] sed 版本号
    s = s.replace("version: 0.2.0", "version: 0.3.0")
    f["SKILL.md"] = s

    # (2) [159] README.md 追加
    r = f["README.md"]
    if "knowledge-sources/" not in r:
        r += ed["readme_add"]
    assert re.search(r"^## External learning registry$", r, re.M), "README 追加段未成行"
    f["README.md"] = r

    # (4) [163] index.yaml 5 处名称加引号（str.replace 未命中时静默失效 → 忠实复现）
    y = f["knowledge-sources/index.yaml"]
    for old, new in ed["name_repls"]:
        hit = old in y
        if hit: y = y.replace(old, new)
        p(("    [163] 命中  " if hit else "    [163] 未命中(静默失效) ") + old.strip()[:70])
    # (5) [172] sed URL
    y = y.replace(ed["sed_url"][0], ed["sed_url"][1])
    f["knowledge-sources/index.yaml"] = y

    # (6) [172] resource-advisor.md 追加决策树
    adv = f["knowledge-sources/resource-advisor.md"]
    adv += ed["append_block"]
    f["knowledge-sources/resource-advisor.md"] = adv
    return f

# ============================================================
# 四、会话全文 Markdown
# ============================================================
def parts_text(m):
    c = m.get("content") or {}
    if c.get("content_type") == "code":
        return c.get("text") or ""
    buf = []
    for x in (c.get("parts") or []):
        if isinstance(x, str): buf.append(x)
        elif isinstance(x, dict): buf.append(x.get("text") or json.dumps(x, ensure_ascii=False))
        else: buf.append(str(x))
    return "\n".join(buf)

def ts(t):
    return datetime.datetime.fromtimestamp(t).strftime("%Y-%m-%d %H:%M:%S") if t else ""

def stats_of(lc):
    st = dict(nodes=len(lc), user=0, assistant=0, tool=0, system=0, code=0, redacted=0, web=0, turns=0)
    for n in lc:
        m = n.get("message")
        if not m: continue
        role = (m.get("author") or {}).get("role")
        ct = (m.get("content") or {}).get("content_type")
        if role: st[role] = st.get(role, 0) + 1
        if ct == "code": st["code"] += 1
        if role == "tool" and m.get("is_redacted"): st["redacted"] += 1
        if m.get("recipient") == "web.run": st["web"] += 1
        if role == "user": st["turns"] += 1
    return st

def render_md(data, st, phase, subtitle, share_id):
    lc = data["linear_conversation"]
    b = []
    b.append(f"# {data['title']} — 会话全文存档\n")
    b.append(f"**{phase}｜{subtitle}**\n")
    b.append("> 来源：ChatGPT 分享会话（私有会话的公开只读快照）  ")
    b.append(f"> 分享链接：https://chatgpt.com/share/{share_id}  ")
    b.append(f"> 原始私有会话：https://chatgpt.com/c/{data.get('backing_conversation_id','')}  ")
    b.append(f"> 模型：{data.get('default_model_slug')} ｜ 快照生成：{ts(data['update_time'])}  ")
    b.append(f"> 导出：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  ")
    b.append(f"> 规模：{st['nodes']} 节点 ｜ {st['turns']} 轮提问 ｜ {st['assistant']} 条助手回复 "
             f"｜ {st['tool']} 条工具消息 ｜ {st['code']} 段工具调用\n")
    b.append("---\n")

    turn = 0
    for n in lc:
        m = n.get("message")
        if not m: continue
        role = (m.get("author") or {}).get("role")
        ct = (m.get("content") or {}).get("content_type")
        txt = parts_text(m).strip()

        if role == "user":
            turn += 1
            b.append(f"\n## 👤 用户 · 第 {turn} 轮\n")
            b.append(f"*{ts(m.get('create_time'))}*\n")
            b.append(txt + "\n")
        elif role == "assistant":
            if ct == "code":
                b.append(f"\n### 🛠 工具调用 · `{m.get('recipient')}`\n")
                b.append("```bash"); b.append(txt); b.append("```\n")
            elif ct in ("model_editable_context", "reasoning_recap", "thoughts"):
                continue
            elif txt:
                b.append("\n### 🤖 ChatGPT\n")
                b.append(txt + "\n")
            elif m.get("recipient") == "web.run":
                b.append("\n> 🌐 *（联网检索调用，内容未随分享保留）*\n")
        elif role == "tool":
            b.append(f"> ⚠️ 工具返回被 ChatGPT 标记为 redacted：`{txt}`\n")
    return "\n".join(b)

def build_v04(nodes, workdir):
    """v0.4 的构建方式与前三个版本完全不同：不再用 shell heredoc 逐个写文件，
    而是在沙箱里写了一个**自包含的 python 生成器** /tmp/build_skill.py，
    由它一次性产出全部 35 个文件并打包。生成器不读任何旧版本文件。

    所以最忠实的复现方式就是：把那段代码原样抽出来、应用后续补丁、然后执行它。
    返回 (files dict, 生成器源码, 后续补丁源码)。
    """
    gen_raw = None
    for i, t in nodes:
        if "cat > /tmp/build_skill.py <<'PY'" in t:
            k = "cat > /tmp/build_skill.py <<'PY'\n"
            gen_raw = t[t.index(k) + len(k): t.rindex("\nPY\n")]
            p(f"  [v0.4] 生成器节点 = [{i}]  ({len(gen_raw)} 字符)")
    assert gen_raw, "v0.4 生成器节点未找到"

    patch_raw, patch_body = None, None
    for i, t in nodes:
        if "old block not found" in t and "build_skill.py" in t:
            k = "python - <<'PY'\n"
            if k in t:
                patch_body = t[t.index(k) + len(k): t.index("\nPY\n", t.index(k))]
                patch_raw = t
                p(f"  [v0.4] 补丁节点 = [{i}]  ({len(patch_body)} 字符)")
    assert patch_body, "v0.4 补丁节点未找到"

    # 用 ast 精确取出补丁里的 old/new 字面量（避免手工转换义符）
    old = new = None
    for node in ast.parse(patch_body).body:
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Constant) \
           and isinstance(node.targets[0], ast.Name):
            if node.targets[0].id == "old": old = node.value.value
            if node.targets[0].id == "new": new = node.value.value
    assert old and new, "补丁 old/new 未取出"
    p(f"  [v0.4] 补丁尺寸: old {len(old)} 字符 / new {len(new)} 字符")
    assert old in gen_raw, "补丁目标块未在生成器中出现"

    code = gen_raw.replace(old, new)

    # 沙箱路径 /mnt/data/... 在 Windows 上会落到 C:\mnt，显式改道到工作区
    dest = os.path.join(workdir, "source-code-reading-skill-v0.4")
    dst = dest.replace("\\", "/")
    n = code.count("/mnt/data/source-code-reading-skill-v0.4")
    code = code.replace("/mnt/data/source-code-reading-skill-v0.4", dst)
    p(f"  [v0.4] 路径改道 {n} 处 -> {dst}")

    os.makedirs(workdir, exist_ok=True)
    g = {"__name__": "__main__", "__file__": "build_skill_v04.py"}
    try:
        exec(compile(code, "build_skill_v04.py", "exec"), g)
    except ImportError as e:
        raise SystemExit(f"需要 PyYAML 才能复现 v0.4：{e}\n"
                         f"请用 ...\\python\\envs\\default\\Scripts\\python.exe 运行本脚本")
    files = g["files"]
    p(f"  [v0.4] 生成 {len(files)} 个文件")
    return files, gen_raw, code


def build_v05(nodes):
    """v0.5 的构建方式：又回到 shell heredoc，但**一次从零生成整包 12 个文件**
    （rm -rf 先清空，再 mkdir 4 个子目录，然后 cat > 逐个写）。

    这是全链最激进的一次动作 —— 从 v0.4 的 35 文件 / 2,697 行，
    砍到 12 文件 / 748 行。knowledge-sources/、evolution/、cases/、diagrams/ 全部消失。
    """
    cands = [(i, t, writes_of(t)) for i, t in nodes if "source-code-reading-skill-v0.5" in t]
    cands = [c for c in cands if c[2]]
    assert len(cands) == 1, f"expect exactly 1 v0.5 build node, got {[c[0] for c in cands]}"
    i, t, w = cands[0]
    p(f"  [v0.5] 构建节点 = [{i}]  写入 {len(w)} 文件")
    for k in sorted(w):
        p(f"        {k:<48} {len(w[k]):>6} 字符  {w[k].count(chr(10))+1:>4} 行")
    return w, t


def build_v051(nodes, base4, v03, workdir):
    """v0.5.1 —— 全链唯一一个「不重写、只合并」的版本。

    前五版都是「生成一个新的包」；这一版是把阶段四的 v0.4 **整包复制一份当基线**，
    然后在上面打补丁。会话里分三步：

      [345] cp -a  v0.4 内层目录  →  source-code-reading-skill-v0.5.1/     （基线复制）
      [347] 执行 /tmp/build_v051.py（21,671 字符）：
              新增 11 个文件、覆写 SKILL.md / README.md，
              并从 v0.3 恢复 2 个在 v0.4 里丢掉的文件（exploration-policy.md、knowledge-sources/README.md）
      [353] 执行补丁：写 evolution/v0.4-baseline-manifest.yaml（35 个基线文件的 SHA-256）、
              evolution/approved-changes.yaml，并给 tests/test_skill_integrity.py 加上
              「SHA-256 比对 + 批准变更白名单」

    所以最忠实的复现方式就是照抄这三步：铺基线 → 跑生成器 → 跑补丁。
    返回 (files dict, 生成器原文, 补丁原文, 包外审计报告原文)。
    """
    def pf(p): return p.replace("\\", "/")

    base_snap = os.path.join(workdir, "_baseline_v0.4")
    root = os.path.join(workdir, "source-code-reading-skill-v0.5.1")
    v03snap = os.path.join(workdir, "_v0.3")

    # 基线：v0.4 全量复制两份 —— 一份留作 SHA-256 基准，一份作为待打补丁的包
    dump(base4, base_snap)
    dump(base4, root)
    restored = ["references/tracing/exploration-policy.md", "knowledge-sources/README.md"]
    missing_v03 = [k for k in restored if k not in v03]
    assert not missing_v03, f"v0.3 缺文件 {missing_v03}"
    dump({k: v03[k] for k in restored}, v03snap)
    p(f"  [v0.5.1] 基线 = v0.4 {len(base4)} 文件；待恢复 = {restored}")

    def cut(txt, opener, closer="\nPY\n"):
        i = txt.index(opener) + len(opener)
        return txt[i:txt.rindex(closer)]

    M = "/mnt/data/source-code-reading-skill-v0.5.1"
    P4 = "/mnt/data/skill-unzipped/0.4/source-code-reading-skill-v0.4/source-code-reading-skill"
    P3 = "/mnt/data/skill-unzipped/0.3/source-code-reading-skill"

    gen = pat = audit = None
    gi = pi = ai = None
    for i, t in nodes:
        if "cat > /tmp/build_v051.py <<'PY'" in t:
            gen = cut(t, "cat > /tmp/build_v051.py <<'PY'\n"); gi = i
        if "v0.4-baseline-manifest.yaml" in t and "python3 - <<'PY'" in t:
            pat = cut(t, "python3 - <<'PY'\n"); pi = i
        if "cat > /mnt/data/source-code-reading-skill-evolution-audit.md <<'EOF'" in t:
            audit = cut(t, "cat > /mnt/data/source-code-reading-skill-evolution-audit.md <<'EOF'\n", "\nEOF\n")
            ai = i
    assert gen and pat and audit, "阶段六的三段脚本未全部找到"
    p(f"  [v0.5.1] 生成器 = [{gi}] ({len(gen)} 字符) ｜ "
      f"基线清单补丁 = [{pi}] ({len(pat)} 字符) ｜ 包外审计报告 = [{ai}] ({len(audit)} 字符)")

    gen = gen.replace(M, pf(root)).replace(P3, pf(v03snap))
    pat = pat.replace(M, pf(root)).replace(P4, pf(base_snap))
    for name, code in (("build_v051.py", gen), ("patch_baseline_manifest.py", pat)):
        left = re.findall(r"/mnt/data/[^'\")\s]*", code)
        assert not left, f"{name} 仍有未改道的沙箱路径：{left}"
        exec(compile(code, name, "exec"), {"__name__": "__main__", "__file__": name})
        p(f"  [v0.5.1] 已执行 {name}")

    files = {}
    for r, _, fs in os.walk(root):
        for f in fs:
            fp = os.path.join(r, f)
            rel = os.path.relpath(fp, root).replace("\\", "/")
            with open(fp, encoding="utf-8") as fh:
                files[rel] = fh.read().rstrip("\n")
    expected = len(base4) + 15     # 35 个基线文件 + 15 个新增/恢复文件
    assert len(files) == expected, \
        f"v0.5.1 文件数 {len(files)} != 预期 {expected}，沙箱目录可能残留了旧文件"
    p(f"  [v0.5.1] 产出 {len(files)} 文件（= 基线 {len(base4)} + 新增 15），符合预期")
    return files, gen, pat, audit


def check_skill(skill, ver):
    c = {}
    c["文件数"] = len(skill)
    s = skill.get("SKILL.md", "")
    m = re.search(r"^version:\s*(\S+)", s, re.M)
    c["SKILL.md.version"] = m.group(1) if m else None
    c["frontmatter有description"] = bool(re.search(r"^description:", s, re.M))
    c["description用折叠符>-"] = bool(re.search(r"^description:\s*>-", s, re.M))
    c["总行数"] = sum(v.count("\n") + 1 for v in skill.values())
    # 引用了但包里不存在的文件（broken link 检查）
    refs = set(re.findall(r"`([A-Za-z0-9_\-/]+\.(?:md|yaml|yml|json|txt))`", s))
    c["SKILL.md引用但缺失的文件"] = sorted(r for r in refs
                                        if r not in skill and not r.startswith("http"))
    c["含External knowledge sources"] = "External knowledge sources" in s
    y = skill.get("knowledge-sources/index.yaml")
    if y is not None:
        ids = re.findall(r"^\s*-\s*id:\s*(\S+)", y, re.M)
        c["资源条数"] = len(ids)
        c["id唯一"] = len(set(ids)) == len(ids)
        c["HIPO那条仍未加引号"] = "    name: IBM HIPO archival materials" in y
        c["kernel.org已去版本"] = "docs.kernel.org/locking/lockdep-design.html" in y
    adv = skill.get("knowledge-sources/resource-advisor.md")
    if adv is not None:
        c["advisor含决策树"] = "## Decision tree" in adv
    return c

def hexdump_ok(zp):
    with zipfile.ZipFile(zp) as z:
        bad = z.testzip()
        return len(z.namelist()), bad

# ============================================================
# 五、落盘
# ============================================================
DESK = r"C:\Users\zhang\Desktop"
BASE = "源码阅读知识建模-Skill设计存档-2026-09-17"
OUT = os.path.join(DESK, BASE)

def dump(files, subdir):
    for rel, body in files.items():
        fp = os.path.join(subdir, rel)
        os.makedirs(os.path.dirname(fp) or subdir, exist_ok=True)
        with open(fp, "w", encoding="utf-8", newline="\n") as f:
            f.write(body + "\n")

def make_zip(files, zippath, arcroot="source-code-reading-skill"):
    os.makedirs(os.path.dirname(zippath), exist_ok=True)
    with zipfile.ZipFile(zippath, "w", zipfile.ZIP_DEFLATED) as z:
        for rel in sorted(files):
            z.writestr(f"{arcroot}/{rel}", files[rel] + "\n", compress_type=zipfile.ZIP_DEFLATED)

PHASES = [
    dict(key="1", dir="阶段一-v0.1-六阶段框架", ver="v0.1", sub="六阶段流程成型，产出首个完整技能包",
         html="share_page.html", share="6aabf46d-c0b0-83ea-b8d0-5deb6ddd7d2c",
         delta="—（起点，15 文件）",
         note="""## 这一阶段发生了什么

用户提出目标：设计一套面向**大型 C/C++ 项目**的源码阅读知识建模规范，并演进为 Skill。
第 1~9 轮把整体拆成六步，逐步执行，最后要求"提供一个 skill 草案，有全量完整的更好"。

**成果：v0.1 完整技能包（15 个文件）**

```
SKILL.md（六阶段主流程）
references/
  knowledge-model.md
  patterns/pattern-catalog.md
  representation/representation-policy.md
  tracing/{trace-policy, claim-verification, exploration-policy}.md
  document-policy.md
  validation/validation-policy.md
templates/{source-reading-note.md, knowledge-model.yaml, review-report.md}
examples/{buffer-manager-plan.yaml, lock-manager-plan.yaml}
README.md
```

## 已知问题

SKILL.md 的 frontmatter 用了 `description: >-`（YAML 折叠符号）。
官方校验器会把 `>` 判为非法字符，**这份包当时装不上**。"""),
    dict(key="2", dir="阶段二-v0.2-图表表达", ver="v0.2", sub="补上图画法谱系与 Mermaid 取舍规则",
         html="share2.html", share="6aabfe86-d7d0-83ea-91a1-155b7e863b83",
         delta="+2 新增、3 覆写（17 文件）",
         note="""## 这一阶段新增了什么

在六阶段之后又聊了 3 轮：

1. 历史上的结构关联图画法有哪些谱系
2. 那些画法是怎么来的、什么时候才适合用
3. 让 Agent 能自己判断该用传统画法还是 Mermaid —— 并写成规则放进 Skill

**成果：v0.2（17 个文件）= v0.1 全部 + 2 个新增 + 3 个覆写**

新增：
- `references/diagrams/diagram-catalog.md`（选择总表 / 决策树 / 传统 vs Mermaid vs 不画 的判定条件）
- `examples/diagram-selection-examples.yaml`

覆写：`SKILL.md`、`references/representation/representation-policy.md`、`README.md`

## ⚠️ `06-未并入的中间产物/` 是怎么来的

构建链在这里断过一次。助手先在一个工作目录里写过一版（改了 pattern-catalog、
representation-policy、diagram-catalog、README，还多建了一个 representation-selection.yaml），
但下一步**又从 v0.1.zip 重新解压当底本**，所以那批改动整批被丢弃。
其中 2 个文件在最终版里没有对应物，单独放在 `06-未并入的中间产物/`：

- `references/patterns/pattern-catalog.md`（3,766 字符，比最终版的 2,791 更详细）
- `examples/representation-selection.yaml`（最终版没有这个文件）

## 已知问题

`description: >-` 依旧没修，仍然装不上。"""),
    dict(key="3", dir="阶段三-v0.3-外部知识源自学", ver="v0.3", sub="补上自我进化机制与 knowledge-sources 资源注册表",
         html="share3.html", share="6aac017a-c060-83ea-888f-2622f5ae448c",
         delta="+knowledge-sources/ 4 文件（21 文件）",
         note="""## 这一阶段新增了什么

又聊了 3 轮，方向从"怎么画图"转到"Agent 怎么自我进化"：

1. 如果图画得不好，让 Agent 如何自我进化？从哪里学？
2. 自我进化依赖的外部素材源、方法论，能不能给出具体地址？
3. 把这些资料整理成 `knowledge-sources/` **资源注册机制** ——
   每个外部资源注明"它教 Agent 什么、什么时候查、可信度如何、能不能直接当事实依据、该提炼成什么规则"

**成果：v0.3（21 个文件）= v0.2 全部 + `knowledge-sources/` 4 个文件 + 3 处后置编辑**

新增目录：
- `knowledge-sources/index.yaml`（**30 条外部资源**的机器可读注册表，最大的单文件）
- `knowledge-sources/resource-advisor.md`（含决策树）
- `knowledge-sources/selection-matrix.md`
- `knowledge-sources/README.md`

后置编辑（都在 SKILL.md / README / index.yaml 上）：
1. SKILL.md 在 `# Six-stage execution` 之前插入 `## External knowledge sources` 一节，
   文末追加 `## Knowledge-source registry contract`
2. README 追加 `## External learning registry`
3. index.yaml 给 5 个含特殊字符的 `name` 加引号 → **实际只命中 4 条**，
   因为第 5 条原文写的是 `IBM HIPO archival materials`，而替换目标写的是
   `HIPO archival materials`，`str.replace` 静默失效（这个坑被原样保留在成品里）
4. SKILL.md 版本号 0.2.0 → 0.3.0；index.yaml 里 kernel.org 的 5.17 URL 去版本化

## 说明

`06-未并入的中间产物/` 在阶段二；v0.3 是在 v0.2 之上叠加的，
所以那 2 个被丢弃的文件**在 v0.3 里依然缺席**。

`description: >-` 到 v0.3 仍然没修。"""),
    dict(key="4", dir="阶段四-v0.4-架构图谱与进化", ver="v0.4", sub="系统架构认知 + 知识图谱 + 自我进化引擎，整包重写",
         html="share4.html", share="6aac08a9-8c68-83e9-9540-9d7689bef346",
         delta="整包重写（35 文件）",
         note="""## 这一阶段新增了什么

又聊了 4 轮，问题从「局部笔记」升到了「**整个系统的认知**」：

1. 面对 Linux / PostgreSQL / MySQL 这种庞然大物，怎么建立好的架构认知，让笔记顺着架构展开？
2. 架构、路径、主题这**三层之间靠什么产生关联**？不该靠符号标记硬凑吧？
3. 那怎么把这些**沉淀成方法**？你是已经知道方法了，能先说清楚吗？
4. 意思是现在已经足够写成一个 skill 了？那就干吧。

**成果：v0.4（35 个文件，2,697 行）—— 这一版不是增量，是彻底重写。**

## 与前三个版本最大的不同：构建方式变了

v0.1~v0.3 都是「一条 `cat > 文件 <<'EOF'` 写一个文件」逐条堆出来的。
v0.4 改成在沙箱里写一个**自包含的 python 生成器** `/tmp/build_skill.py`（约 65,000 字符），
由它一次性产出全部文件并打包 —— 而且它**不读任何旧版本文件**，是从零生成的。

生成器写完后还被打了一次补丁（把 `index.yaml` 的资源列表从 f-string 拼接改为
`yaml.safe_dump` 正式序列化），再重新执行。

## 结构上新增了什么

```
references/architecture-model.md          架构作为全图的坐标系
references/architecture-reconstruction.md 自上而下假设 + 自下而上证据
evolution/evolution-policy.md             反馈 → 分类 → 案例 → 规则 → 回归
evolution/feedback-taxonomy.md
evolution/rule-proposal.md
evolution/case-learning.md
evolution/regression.md
evolution/anti-patterns/                  5 个典型反模式
cases/gold/  cases/failures/              金案例 / 失败案例
templates/feedback.yaml
examples/system-atlas-postgresql.yaml
examples/representation-plan.yaml
examples/evolution-case.yaml
examples/architecture-driven-note.md
```

核心变化有三条：

- **架构是一等公民**：先建一次 System Atlas（长期资产），之后所有主题笔记都挂在它上面
- **Path 成为一级知识对象**：Architecture → Path → Mechanism → Source，
  这样 `BufferDesc`、`LockAcquire()`、`TupleTableSlot` 不再彼此孤立
- **有了进化引擎**：用户反馈不再只是「记一笔」，而是走
  Failure Classification → Case → Rule Proposal → Regression → Adopted Rule

## ⚠️ 这是一次重写，有东西真的丢了

因为是整包从零生成，v0.2/v0.3 的一些文件**在 v0.4 里彻底消失了**，不是被合并：

- `references/tracing/exploration-policy.md`（v0.1~v0.3 一直在，v0.4 没了）
- `knowledge-sources/README.md`（v0.3 有）
- `examples/buffer-manager-plan.yaml`、`lock-manager-plan.yaml`（v0.1 就有的两个示例）
- `examples/diagram-selection-examples.yaml`（v0.2 的产物）

同时 `knowledge-sources/index.yaml` 的资源**从 30 条精简到 22 条** —— 不是补全，是重选了。

## zip 的目录多套了一层

脚本用 `z.write(p, p.relative_to(root.parent.parent))` 打包，而 `root.parent` 是
`source-code-reading-skill-v0.4/`，结果 zip 内路径成了：

```
source-code-reading-skill-v0.4/source-code-reading-skill/...
```

比前三个版本多一层嵌套。解压时会多出一个目录层，这是个实实在在的小瑕疵。

## 校验结果

会话里自述「35 个文件 / 约 2660 行 / 22 个外部知识源」，本地复现得到
**35 文件 / 2,697 行 / 22 条**，基本吻合。

> 行数口径说明：本存档统一按「文件去尾空行后的行数」统计。
> v0.4 / v0.5.1 的生成器写出的文件末尾本身带空行，若按字节原样统计会多出若干行，
> 所以别处若见到略大的数字，多半是口径不同。全存档表格都用同一口径，可横向比较。

`description: >-` **依旧没修** —— 四个版本一脉相承地装不上。"""),
    dict(key="5", dir="阶段五-v0.5-执行闸门与瘦身", ver="v0.5", sub="把「先做什么、做到什么程度停」固化成执行闸门，整包砍到 12 文件",
         html="share5.html", share="6aac0e91-8428-83e9-85ba-be83ff89374d",
         delta="整包重写并大幅瘦身（12 文件，-66%）",
         note="""## ⚠️ 先说清楚：这一份快照来自一个**分支会话**

| | 阶段一~四 | 阶段五 |
|---|---|---|
| `backing_conversation_id` | `6aabef9e-86a0-83ea-a9db-75ee175e065e` | **`6aac0c45-f670-83ea-9236-a7e2155a8801`** |
| 标题 | 源码知识建模 | **分支 · 分支 · 源码知识建模** |

也就是说：对话被**分叉**过一次（标题里两个"分支"），这份分享挂在分叉后的那条线上。

但内容上它是阶段四的**严格超集** —— 前 224 个节点的
`role / content_type / text / parts` **逐字比对全部相同（0 处差异）**，
只有 `message.id`、`request_id`、`create_time` 这类元数据因会话重挂而不同。

所以读起来仍然是一条连续演进链，只是"血缘"上换了个 conversation id。

## 这一阶段新增了什么

又聊了 3 轮，方向变了 —— 不再问"还能加什么"，而是问**"是不是该停了"**：

1. **还有没考虑到的么** → 助手答：缺"怎么长期理解一个活的大型系统"
2. **这些东西还需要落实到文档里么？还是说之前的已经成体系了？** →
   助手答：**不该把所有想到的东西继续堆进一个 Skill**，那样最终会变成一个巨大 Prompt，反而削弱执行力
3. **还需要整理成 skill 么？一定要做好规划，让 agent 知道先干什么后干什么，
   一步一步构建，不要上来就贪多嚼不烂** → 于是有了 v0.5

**成果：v0.5（12 个文件 / 748 行 / 19,313 字符）**

## 这一版的主旨：把"什么时候停"写进 Skill

前面四版一直在回答"源码阅读有哪些东西"；v0.5 问的是
**"现在做什么、做到什么就停、什么时候才允许进入下一层"**。

SKILL.md 新增的核心章节：

```
## Non-negotiable execution rule   —— 绝不在解决当前问题前先去理解整个系统
## Stop / continue gates           —— Gate 0~6，每道闸门都有硬停条件
   Gate 0 Scope → Gate 1 Orient → Gate 2 Minimum Knowledge Model
   → Gate 3 Pattern → Gate 4 Traceability → Gate 5 Representation
   → Gate 6 Validation
## Progressive depth policy        —— L0 定位 / L1 局部模型 / L2 源码溯源 / L3 横切架构
## Anti-overengineering rules      —— 显式反过度设计
## Completion criteria
```

举例一个闸门的写法（Orient）：

> Agent 只需回答"它在哪 / 属于哪个 subsystem / 周围有哪些关键对象 / 入口在哪 /
> 哪条 path 串起来"。一旦能回答"我知道这个 Topic 在系统里的位置了"——**就必须停**。
> 不允许顺手"把整个 PostgreSQL Executor 都研究一下"。

## 结构上：一次非常激进的瘦身

| | v0.4 | **v0.5** |
|---|---|---|
| 文件数 | 35 | **12（-66%）** |
| 总行数 | 2,697 | **748（-72%）** |
| 字符数 | ~137 KB | **19.3 KB（-86%）** |

**整包重写，不是删减**：脚本先 `rm -rf` 清空目标目录，再重建。
下面这些目录在 v0.5 里**整体消失**：

- `knowledge-sources/`（v0.3 的 30 条资源注册表，v0.4 精简为 22 条）→ 全没了，
  只在 SKILL.md 里留了一个 `## External knowledge sources` 章节
- `evolution/` + `cases/`（v0.4 的进化引擎与金案例/失败案例）→ 全没了，
  只在 SKILL.md 里留了一个 `## Self-evolution` 章节
- `references/diagrams/`（v0.2 的图画法谱系）→ 没了
- 目录结构重新收缩为：`references/{patterns,representation}` + `templates/` + `examples/`

换句话说：**前面四版积累的"知识库"被反过来压回了 SKILL.md 的正文里**，
包体只保留执行协议。这正好呼应第 2 轮用户问的"这些还需要落实到文档里么"。

而且这不是简单地"删掉"—— v0.5 的 README 把这件事说成了**刻意的架构切分**：

```text
Source Understanding System
├── Core Skill              ← 这个包只做这一块
│   ├── staged execution + gates
│   ├── architecture foundation
│   ├── canonical knowledge model
│   ├── pattern recognition / traceability / representation / validation
├── Capability Extensions   ← 静态分析 / 运行时观测 / 性能分析 / 测试分析 / 渲染
├── Knowledge Sources       ← 标准 / 方法 / 工具文档 / 项目示例
└── Evolution               ← cases / feedback / anti-patterns / regression
```

README 里有一节标题直接叫 **"What is deliberately not in the core"**：

> Tool manuals, exhaustive diagram catalogs, vendor-specific workflows,
> perf/BPF/VTune procedures, and project-specific rules should remain
> **extensions or knowledge sources**.

也就是说：`knowledge-sources/` 和 `evolution/` 不是被否定了，
而是被判定为**不该待在核心 Skill 里**，应该独立成扩展层。
"一个巨大 Prompt 会削弱 Agent 执行力"是这次瘦身的直接理由。

## 构建方式

又回到 shell heredoc（`cat > "$ROOT/..." <<'EOF'`），但和 v0.1~v0.3 的"逐条增量"不同 ——
v0.5 是**一个脚本一次性从零生成全部 12 个文件**，再 `cd /mnt/data && zip -qr`。

脚本原样保存在 `06-构建脚本/`（20,749 字符），可逐字复现。
另附一个 `v0.5-校验片段.py`：脚本尾部那段统计文件数/行数/`testzip()` 的 python，
它的输出在分享页里同样被 redacted，所以这里单列出来便于自己跑一遍。

## 校验结果

- 本地重建：**12 文件 / 748 行**，zip 内 12 条目、无损坏
- zip 目录层级正常（`source-code-reading-skill-v0.5/…`），**没有** v0.4 那种多套一层的问题

## ⚠️ 装不上的原因变了，但还是装不上

v0.1~v0.4 是 `description: >-` 含 `>` 被拒。v0.5 把 frontmatter 改成了：

```yaml
name: source-code-reading
version: 0.5
summary: A staged, evidence-driven method for ...
```

**`description` 字段直接没了**。官方校验器实测：

```
Missing 'description' in frontmatter   exit=1
```

从"写错了"变成"没写"—— 第五个版本，仍然装不上。"""),
    dict(key="6", dir="阶段六-v0.5.1-非回归修复", ver="v0.5.1",
         sub="以完整 v0.4 为基线做增量合并，把 v0.5 判定为「回归」并修复，同时把「不许静默丢能力」写成硬约束",
         html="share6.html", share="6aac7561-f638-83ea-bf9c-57e481e66240",
         delta="v0.4 全量 + 15 新增（50 文件）",
         note="""## ⚠️ 这一阶段是被「上一份存档」问出来的

这次对话的起点不是新想法，而是**用户把本存档（阶段五那份总览）里的一句话原样贴回给了 ChatGPT**：

> 识别到**阶段四是重写，有东西真的丢了；阶段五把这个趋势走到了极端。** 阶段五的 12 文件包里，
> `knowledge-sources/`、`evolution/`、`cases/`、`references/diagrams/` **全部消失**。丢的这些东西是进化么

ChatGPT 的回答很干脆：**「不是。这不是进化，这是明显的回归（regression）」**，
并承认「我后面为了强调"分阶段执行"，实际上做了一个从头重建 v0.5，结果把之前已经沉淀的能力丢掉了」。

然后用户追问第二轮：

> 那你评估一下之前 1-5 阶段，还丢了哪些，如果是正常演进就算了，如果是丢失重要特性，加上本次对话那补齐吧。

## 助手这次不是靠回忆，是逐文件 diff 了真实包

它在沙箱里把 v0.1~v0.5 的实际 zip 解出来，用 `difflib` 逐文件比对，得到三条结论：

| 演进 | 判断 | 依据 |
|---|---|---|
| v0.1 → v0.2 | ✅ 正常演进 | 图示体系、Representation Policy 明显增强 |
| v0.2 → v0.3 | ✅ 正常演进 | 加入 `knowledge-sources/` 外部知识学习体系 |
| v0.3 → v0.4 | ⚠️ 基本正常但有**隐性回退** | 丢了 `references/tracing/exploration-policy.md`（重要）与 `knowledge-sources/README.md`（次要） |
| v0.4 → v0.5 | ❌ **明显回归** | 35 文件重建成 12 文件，成熟能力资产整体消失 |
| v0.5.1 | ✅ 修复 | 以完整 v0.4 为基线增量合并 |

## v0.5.1 怎么建的：不重写，只合并

**这是六个版本里唯一一个没有"生成新包"的版本。**

```text
[345]  cp -a  v0.4 内层包  →  source-code-reading-skill-v0.5.1/     ← 先整包复制当基线
[347]  python /tmp/build_v051.py                                    ← 打增量补丁（21,671 字符）
[353]  python 补丁：写 SHA-256 基线清单 + 升级完整性测试            ← 再补治理文件
[355]  zip -qr source-code-reading-skill-v0.5.1.zip                 ← 打包
```

生成器做三件事：

1. **恢复**从 v0.3 丢到 v0.4 的 2 个文件（`exploration-policy.md`、`knowledge-sources/README.md`）
2. **覆写** `SKILL.md`（版本号 0.4.0 → 0.5.1，插入渐进执行闸门、Core-vs-Extensions 边界、
   `## Evolution` 里补上「非回归不变量」）与 `README.md`（重写成"v0.5.1 修了什么"）
3. **新增** 11 个文件，其中最重要的是：

```text
references/execution-progressive.md   Gate 0~6 + L0~L3 渐进深度 + 反过度设计
references/extension-boundary.md      Core / Extensions / Knowledge sources / Evolution 四层边界
evolution/baseline-policy.md          合并式演进（merge, not rewrite）+ 删除必须留记录
evolution/capability-inventory.md     逐能力对照表（preserved / added / strengthened）
evolution/approved-removals.yaml      本次批准的删除（空）
templates/capability-inventory.yaml   基线能力清单模板
templates/evolution-change.yaml       版本变更记录模板
examples/progressive-execution-example.md  用 PostgreSQL Buffer Lookup 走一遍闸门
CHANGELOG.md  EVOLUTION_AUDIT.md
  
（补丁 [353] 再加两个）
evolution/v0.4-baseline-manifest.yaml  35 个基线文件的 SHA-256
evolution/approved-changes.yaml        允许改动的基线文件白名单：SKILL.md / README.md / knowledge-sources/README.md
tests/test_skill_integrity.py          完整性回归测试，被升级为「SHA-256 比对 + 白名单」
```

## 机制上真正新增的东西

前五版关心的是「源码阅读该怎么做」；这一版第一次规定了 **Skill 自己该怎么演进**：

```text
Previous release
   +  New capability / correction
   ↓  Capability inventory
   ↓  Baseline comparison
   ↓  Minimal additive merge
   ↓  Integrity regression（文件不许丢）
   ↓  Semantic regression（内容不许缩水）
   ↓  Changelog
New release
```

并且规定：**删除一个已有能力必须显式留记录** ——

```yaml
removal:
  path: ""
  capability: ""
  reason: ""
  replacement: ""
  regression_evidence: []
  approved: false
```

## 校验结果

本地把 [347] + [353] 两段脚本原样跑了一遍：

- **50 个文件 / 3,441 行**，v0.4 基线 **35/35 全部保留、0 缺失**
- 被覆写的基线文件恰好是白名单里的 **2 个**（`SKILL.md`、`README.md`）
- 包内 `tests/test_skill_integrity.py` 实跑通过：
  `PASS: preserved 35 baseline files; changed 2 approved baseline files; added 15 files`

⚠️ 会话里助手自述「新增 15 个…总计 **48** 个文件」，**48 这个数与它自己的 15 对不上**
（35 + 15 = 50），实测就是 **50**。这是本阶段唯一一处数字出入。

（行数口径与全存档一致：去尾空行后统计。按字节原样统计是 3,525 行。）

## ⚠️ 老问题依旧：六个版本全都没修 frontmatter

v0.5.1 的 `SKILL.md` 是从 v0.4 覆写而来，frontmatter 原样继承：

```yaml
name: source-code-reading
version: 0.5.1
description: >-
  A graph-first skill for understanding large C/C++ systems ...
```

官方校验器实测：

```
Description cannot contain angle brackets (< or >)   exit=1
```

六个版本，六次同样的报错。这一版修了「能力回归」，但**没碰**这个从 v0.1 就存在的
描述符问题 —— 也说明它确实是一次「只解决被指出问题」的最小增量修复。"""),
]

# 出于文件安全策略（不允许一次性批量删除 50 个以上文件），
# 本脚本**不整体删除**存档目录，而是就地重建：同名文件直接覆盖。
# 若某个文件在新版本中不再生成，需要手工清理 —— 目前只有总览改过名，单独处理。
os.makedirs(OUT, exist_ok=True)
_legacy = os.path.join(OUT, "00-总览与五阶段对照.md")
if os.path.exists(_legacy):
    p("清理旧版总览（已更名）:", _legacy)
    os.remove(_legacy)

summary = []
v01_cache = v02_cache = None
V03 = None
V04 = None
V05 = None
V051 = None

for ph in PHASES:
    p("=" * 70)
    p("阶段", ph["key"], ph["dir"])
    data, html = load_route(os.path.join(HERE, ph["html"]))
    lc = data["linear_conversation"]
    st = stats_of(lc)
    nodes = code_nodes(lc)
    p("  节点", st["nodes"], "轮次", st["turns"], "助手", st["assistant"],
      "工具", st["tool"], "code", st["code"], "redacted", st["redacted"], "web", st["web"])

    root = os.path.join(OUT, ph["dir"])
    os.makedirs(root, exist_ok=True)
    zip_src = None
    zip_arcroot = "source-code-reading-skill"

    if ph["key"] == "1":
        v01, _ = build_v01(nodes)
        v01_cache = v01
        skill = v01
    elif ph["key"] == "2":
        v01, _ = build_v01(nodes)
        ov, _ = build_overwrites(nodes)
        mid, _ = build_mid(nodes)
        v01_cache = v01
        v02_cache = dict(v01); v02_cache.update(ov)
        skill = v02_cache
        # 孤儿 = 中间修订产出、但既没被 [104] 重新覆盖、又与 v0.1 原版不同的文件
        orphans = {k: v for k, v in mid.items() if k not in ov and v != v01.get(k)}
        dump(orphans, os.path.join(root, "06-未并入的中间产物"))
        p("  孤儿文件:", sorted(orphans))
    elif ph["key"] == "3":
        v01, _ = build_v01(nodes)
        ov, _ = build_overwrites(nodes)
        mid, _ = build_mid(nodes)
        v02_cache = dict(v01); v02_cache.update(ov)
        ks, _ = build_ks(nodes)
        ed = build_edits(nodes)
        skill = apply_v03(v02_cache, ks, ed)
        V03 = skill
        p("  v0.3 文件数:", len(skill))
    elif ph["key"] == "4":
        # === 阶段四：v0.4 由自包含生成器产出，直接执行会话里那段代码 ===
        work = os.path.join(HERE, "_sandbox4")
        # 沙箱目录同样只创建、不删除（文件安全策略不允许批量删除）：
        # 生成器不读旧文件，而且 files 来源是内存 dict，残留文件不影响结果。
        os.makedirs(work, exist_ok=True)
        skill, gen_raw, gen_patched = build_v04(nodes, work)
        zip_src = os.path.join(work, "source-code-reading-skill-v0.4.zip")
        assert os.path.exists(zip_src), "生成器未产出 zip"
        # 保留生成器与打补丁后的最终版，便于复现
        d_gen = os.path.join(root, "06-构建脚本")
        os.makedirs(d_gen, exist_ok=True)
        open(os.path.join(d_gen, "build_skill.py"), "w", encoding="utf-8", newline="\n").write(gen_patched)
        open(os.path.join(d_gen, "build_skill_原始未打补丁.py"), "w", encoding="utf-8", newline="\n").write(gen_raw)
        p("  生成器与补丁版已归入 06-构建脚本/")
        if V03 is not None:
            gone = sorted(set(V03) - set(skill))
            added = sorted(set(skill) - set(V03))
            p(f"  相对 v0.3 丢失 {len(gone)} 个文件: {gone}")
            p(f"  相对 v0.3 新增 {len(added)} 个文件: {added}")
        p("  v0.4 文件数:", len(skill))
        V04 = skill
    elif ph["key"] == "5":
        # === 阶段五：v0.5 由一个 shell 脚本从零生成 12 个文件 ===
        skill, script = build_v05(nodes)
        # 原始脚本是 cd /mnt/data && zip -qr ...-v0.5.zip source-code-reading-skill-v0.5
        # 所以 zip 内的根目录名带 -v0.5 后缀，这里保持一致
        zip_arcroot = "source-code-reading-skill-v0.5"
        d_gen = os.path.join(root, "06-构建脚本")
        os.makedirs(d_gen, exist_ok=True)
        open(os.path.join(d_gen, "build_v0.5.sh"), "w", encoding="utf-8", newline="\n").write(script)
        # 脚本尾部那段自校验 python（输出在分享页里是 redacted 的），单列出来
        k = "python - <<'PY'\n"
        if k in script:
            body = script[script.index(k) + len(k):]
            j = body.rfind("\nPY")
            if j >= 0: body = body[:j]
            open(os.path.join(d_gen, "v0.5-校验片段.py"), "w", encoding="utf-8",
                 newline="\n").write(body.strip("\n") + "\n")
            p("  校验片段已抽出：", len(body), "字符")
        else:
            p("  !! 未找到校验片段")
        p("  构建脚本 + 校验片段已归入 06-构建脚本/")
        if V04 is not None:
            gone = sorted(set(V04) - set(skill))
            added = sorted(set(skill) - set(V04))
            p(f"  相对 v0.4 丢失 {len(gone)} 个文件:")
            for g in gone: p("        -", g)
            p(f"  相对 v0.4 新增 {len(added)} 个文件: {added}")
            p(f"  行数：v0.4 {sum(v.count(chr(10))+1 for v in V04.values())} -> "
              f"v0.5 {sum(v.count(chr(10))+1 for v in skill.values())}")
        p("  v0.5 文件数:", len(skill))
        V05 = skill
    else:
        # === 阶段六：v0.5.1 —— 唯一一个「复制基线 + 增量合并」的版本 ===
        work = os.path.join(HERE, "_sandbox6")
        # 注意：沙箱目录只在缺失时创建，不做删除 —— 复用同一个目录时，
        # dump() 会覆盖全部同名文件，收集前用文件数断言兜底。
        os.makedirs(work, exist_ok=True)
        skill, gen6, pat6, audit6 = build_v051(nodes, V04, V03, work)
        zip_arcroot = "source-code-reading-skill-v0.5.1"
        d_gen = os.path.join(root, "06-构建脚本")
        os.makedirs(d_gen, exist_ok=True)
        for fn, body in (("build_v051.py", gen6),
                         ("patch_baseline_manifest.py", pat6),
                         ("v0.1-v0.5-演进审计报告.md", audit6)):
            open(os.path.join(d_gen, fn), "w", encoding="utf-8", newline="\n").write(body + "\n")
        p("  生成器 + 基线清单补丁 + 包外审计报告已归入 06-构建脚本/")
        if V04 is not None:
            gone = sorted(set(V04) - set(skill))
            added = sorted(set(skill) - set(V04))
            p(f"  相对 v0.4 丢失 {len(gone)} 个文件（应为 0）: {gone}")
            p(f"  相对 v0.4 新增 {len(added)} 个文件: {added}")
            p(f"  行数：v0.4 {sum(v.count(chr(10))+1 for v in V04.values())} -> "
              f"v0.5.1 {sum(v.count(chr(10))+1 for v in skill.values())}")
        if V05 is not None:
            p(f"  相对 v0.5（回归版）恢复 {len(sorted(set(skill) - set(V05)))} 个文件"
              f"（v0.5 只有 {len(V05)} 个文件，v0.5.1 有 {len(skill)} 个）")
        p("  v0.5.1 文件数:", len(skill))
        V051 = skill

    # 03-Skill 成品
    dump(skill, os.path.join(root, f"03-Skill-{ph['ver']}"))
    # 04-技能包
    zip_out = os.path.join(root, "04-技能包", f"source-code-reading-skill-{ph['ver']}.zip")
    if zip_src:
        os.makedirs(os.path.dirname(zip_out), exist_ok=True)
        shutil.copyfile(zip_src, zip_out)
        p("  技能包来自生成器自打的 zip（保留原始目录层级）")
    else:
        make_zip(skill, zip_out, arcroot=zip_arcroot)
    # 01/02
    md = render_md(data, st, ph["dir"], ph["sub"], ph["share"])
    open(os.path.join(root, "01-会话全文.md"), "w", encoding="utf-8", newline="\n").write(md)
    json.dump(data, open(os.path.join(root, "02-会话原始数据.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    # 05-原始页面快照
    shutil.copyfile(os.path.join(HERE, ph["html"]), os.path.join(root, "05-原始页面快照.html"))

    # 00-本阶段说明
    head = (f"# {ph['dir']}\n\n"
            f"**分享链接**：https://chatgpt.com/share/{ph['share']}  \n"
            f"**快照时间**：{ts(data['update_time'])} ｜ **模型**：{data.get('default_model_slug')}  \n"
            f"**规模**：{st['nodes']} 节点 ｜ {st['turns']} 轮提问 ｜ {st['assistant']} 条助手回复 "
            f"｜ {st['tool']} 条工具消息 ｜ {st['code']} 段工具调用\n\n"
            "## 目录\n\n"
            "| 文件 | 内容 |\n|---|---|\n"
            "| `00-本阶段说明.md` | 本文件 |\n"
            f"| `01-会话全文.md` | 逐轮全文（{len(md):,} 字符） |\n"
            "| `02-会话原始数据.json` | 页面内嵌的结构化数据，保真备份 |\n"
            f"| `03-Skill-{ph['ver']}/` | 该阶段技能包完整文件树（{len(skill)} 个文件） |\n"
            f"| `04-技能包/` | 打包好的 zip |\n"
            "| `05-原始页面快照.html` | 分享页原始 HTML（最后防线，链接失效后仍可重新解析） |\n"
            + {"2": "| `06-未并入的中间产物/` | 被构建链丢弃、未进最终版的文件 |\n",
               "4": "| `06-构建脚本/` | v0.4 的 python 生成器（补丁版 + 原始版），可逐字复现 |\n",
               "5": "| `06-构建脚本/` | v0.5 的 shell 生成脚本 + 脚本尾部自校验片段 |\n",
               "6": "| `06-构建脚本/` | v0.5.1 的增量合并生成器 + 基线 SHA-256 清单补丁 + 包外审计报告 |\n"}
              .get(str(ph["key"]), "")
            + "\n---\n\n" + ph["note"] + "\n")
    open(os.path.join(root, "00-本阶段说明.md"), "w", encoding="utf-8", newline="\n").write(head)

    # 校验
    chk = check_skill(skill, ph["ver"])
    p("  校验:", chk)

    zip_path = os.path.join(root, "04-技能包", f"source-code-reading-skill-{ph['ver']}.zip")
    zn, bad = hexdump_ok(zip_path)
    p(f"  zip 内 {zn} 条目，损坏项={bad}")
    summary.append(dict(ph=ph, st=st, files=len(skill), md=len(md),
                        zip=os.path.getsize(zip_path), chk=chk,
                        ph_time=data["update_time"]))
    p(f"  技能包 {len(skill)} 文件；全文 {len(md)} 字符")

json.dump(summary, open(os.path.join(HERE, "_summary.json"), "w", encoding="utf-8"),
          ensure_ascii=False, default=str, indent=1)

# ---------------- 根目录总览 ----------------
lines = []
lines.append("# 源码阅读知识建模 — Skill 设计存档（六阶段）\n")
lines.append("同一场 ChatGPT 对话的六个**历史快照**。分享链接每次生成都会把当时的最新状态冻结一份，"
             "所以这些目录不是六份不同文档，而是**同一条演进链上的六个截面**，越往后内容越全。\n")
lines.append("原始私有会话：https://chatgpt.com/c/6aabef9e-86a0-83ea-a9db-75ee175e065e  ")
lines.append("对话标题：源码知识建模 ｜ "
             f"导出时间：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
lines.append("""
> **关于血缘：这条对话被分叉过两次，六个阶段挂在三条 conversation id 上。**
>
> | 阶段 | `backing_conversation_id` | 标题 |
> |---|---|---|
> | 一 ~ 四 | `6aabef9e-…` | 源码知识建模 |
> | 五 | `6aac0c45-…` | 分支 · 分支 · 源码知识建模 |
> | 六 | `6aac730a-…` | 分支 · 源码知识建模01 |
>
> 但内容上是一条连续链：阶段五前 224 个节点、阶段六前 258 个节点的 `role` + 正文
> 与各自前一阶段**逐字相同（0 处差异）**，所以每一份都是前一份的严格超集。
> 差的只是 `message.id` / `create_time` 这类因会话重挂而变的元数据。
""")
lines.append("---\n")
lines.append("## 六阶段对照\n")
CN = {"1": "一", "2": "二", "3": "三", "4": "四", "5": "五", "6": "六"}
lines.append("| | " + " | ".join(f"阶段{CN.get(s['ph']['key'], s['ph']['key'])}" for s in summary) + " |")
lines.append("|" + "---|" * (len(summary) + 1))
rows = [
    ("目录", lambda s: "`" + s["ph"]["dir"] + "`"),
    ("分享链接", lambda s: f"[share](https://chatgpt.com/share/{s['ph']['share']})"),
    ("快照时间", lambda s: ts(s["ph_time"])),
    ("会话节点数", lambda s: str(s["st"]["nodes"])),
    ("提问轮次", lambda s: str(s["st"]["turns"])),
    ("助手回复", lambda s: str(s["st"]["assistant"])),
    ("工具消息", lambda s: str(s["st"]["tool"])),
    ("工具调用段", lambda s: str(s["st"]["code"])),
    ("联网检索", lambda s: str(s["st"]["web"])),
    ("技能版本", lambda s: s["chk"].get("SKILL.md.version") or "-"),
    ("技能文件数", lambda s: str(s["files"])),
    ("技能总行数", lambda s: f"{s['chk'].get('总行数', 0):,}"),
    ("本阶段变化", lambda s: s["ph"]["delta"]),
    ("全文大小", lambda s: f"{s['md']:,} 字符"),
    ("zip 大小", lambda s: f"{s['zip']/1024:.1f} KB"),
]
for label, fn in rows:
    lines.append("| " + label + " | " + " | ".join(fn(s) for s in summary) + " |")
lines.append("")
lines.append("---\n")
lines.append("## 六个阶段的演进一句话版\n")
lines.append("- **阶段一**：把「读懂大 C/C++ 项目」拆成六阶段流程，产出**首个完整技能包 v0.1**（15 文件）\n")
lines.append("- **阶段二**：补上「图画法与 Mermaid 该怎么选」，v0.2（17 文件），"
             "新增 `references/diagrams/diagram-catalog.md`\n")
lines.append("- **阶段三**：补上「Agent 如何自我进化」，v0.3（21 文件），"
             "新增 `knowledge-sources/` 外部资源注册表（30 条）\n")
lines.append("- **阶段四**：视角抬到「整个系统怎么被理解」，v0.4（35 文件 / 2,697 行），"
             "**整包重写** —— 架构成为一等公民（System Atlas）、Path 成为一级知识对象、"
             "新增进化引擎 `evolution/` + `cases/`\n")
lines.append("- **阶段五**：转向「**什么时候该停**」，v0.5（12 文件 / 748 行），"
             "**又一次整包重写，而且是唯一一次做减法** —— 把前四版的知识库压回 SKILL.md 正文，"
             "包内只留执行协议：Stop/Continue Gates（Gate 0~6）、Progressive Depth（L0~L3）、"
             "Anti-overengineering Rules；"
             "并把 `knowledge-sources/`、`evolution/` 明确划为「核心之外」的扩展层\n")
lines.append("- **阶段六**：用户把上一份存档里「阶段五丢掉了哪些东西」的判断贴回给助手，"
             "助手承认这是**回归**并逐文件比对 v0.1~v0.5 的真实包，"
             "最终产出 v0.5.1（50 文件）—— **六个版本里唯一一次「复制基线 + 增量合并」**，"
             "v0.4 基线 35/35 全保留，新增渐进执行闸门与「不许静默丢能力」的演进纪律\n")
lines.append("**把六个版本串起来看，是一条完整的钟摆曲线，最后回到了起点的高度**：\n")
lines.append("```\n"
             "v0.1  15 文件                —— 建立六阶段框架\n"
             "v0.2  17 文件                —— 加图画法与 Mermaid 取舍\n"
             "v0.3  21 文件                —— 加外部知识源（30 条）\n"
             "v0.4  35 文件 / 2,697 行     —— 整包重写，加架构层与进化引擎（第一次峰值）\n"
             "v0.5  12 文件 /   748 行     —— 整包重写，砍掉 66% 文件、72% 行数（谷值 = 回归）\n"
             "v0.5.1 50 文件 / 3,441 行    —— 回到 v0.4 基线做增量合并（第二次峰值，且不再回落）\n"
             "```\n")
lines.append("v0.4 → v0.5 的转变不是技术性的，是**认知性的**："
             "助手在 v0.5 里明确说「不该把所有想到的东西继续堆进一个 Skill，"
             "那样最终一定会变成一个巨大 Prompt，反而削弱 Agent 的执行能力」。\n")
lines.append("而 v0.5 → v0.5.1 的转变是**工程性的**："
             "「做减法」这个念头本身没错，错的是**做法**——它把做减法实现成了整包重写，"
             "于是被精简掉的不是冗余，而是别人（更早的自己）已经沉淀好的可复用资产。"
             "v0.5.1 把这条教训固化成了 Skill 的硬约束："
             "**新版本默认必须是 merge，不是 rewrite；删任何东西都要留下 reason / replacement / regression evidence**。\n")
lines.append("---\n")
lines.append("## 六个必须留意的诚实声明\n")
lines.append("**1. 所有 zip 都是从会话正文重建的，不是沙箱原始二进制。**\n")
lines.append("分享页里的可下载链接数为 **0** —— ChatGPT 沙箱文件不随分享外泄，"
             "页面中只有 `sandbox:/mnt/data/...` 这样的路径文本（阶段六末尾那两个 `[下载 …zip]` 链接同样打不开）。\n")
lines.append("好在这些版本都把每个文件的完整正文写进了工具调用，因此可以逐字重建，"
             "**内容 1:1 一致**（zip 内部元数据、时间戳不同）。重建分两档：\n")
lines.append("- v0.1~v0.3、v0.5：`cat > 文件 <<'EOF'` 逐字还原\n")
lines.append("- v0.4、**v0.5.1**：构建脚本本身就是可执行的 python 代码，"
             "所以是**把会话里那两段代码原样跑了一遍**得到的 —— 比逐字重建还要保真\n")
lines.append("**2. 工具返回是 ChatGPT 自己抹掉的。** 原文即 `The output of this plugin was redacted.`，"
             "不是抓取失败。阶段六的 98 条工具消息里有 **65 条**是这样的占位，"
             "被抹掉的都是 `ls -lah`、`unzip -l`、`testzip()` 之类的校验回显；"
             "另有若干次联网检索的返回未随分享保留。关键正文都在。\n")
lines.append("**3. 六个版本全都没通过官方校验器，而且失败原因是分两段的。** 实测：\n")
lines.append("```\n"
             "v0.1 / v0.2 / v0.3   Description cannot contain angle brackets (< or >)   exit=1\n"
             "v0.4                 Description cannot contain angle brackets (< or >)   exit=1\n"
             "v0.5                 Missing 'description' in frontmatter                 exit=1\n"
             "v0.5.1               Description cannot contain angle brackets (< or >)   exit=1\n"
             "```\n")
lines.append("v0.1~v0.4 与 v0.5.1 的坑都是 `description: >-`（折叠符号被当成描述正文）；"
             "v0.5 则是把 `description` 字段整个删了、换成 `summary`。"
             "值得注意的是：**v0.5.1 修了能力回归，却没碰这个从 v0.1 就存在的描述符问题** —— "
             "它是一次「只解决被指出问题」的最小增量修复。\n")
lines.append("**4. 阶段四是重写，有东西真的丢了；阶段五把这个趋势走到了极端，阶段六把它修了回来。** "
             "阶段五的 12 文件包里，`knowledge-sources/`、`evolution/`、`cases/`、"
             "`references/diagrams/` **全部消失**；阶段六恢复到 50 文件，"
             "并把 `references/tracing/exploration-policy.md`、`knowledge-sources/README.md` "
             "这两个在 v0.3→v0.4 就丢过一次的文件也一并找回。详见各阶段的 `00-本阶段说明.md`。\n")
lines.append("**5. 阶段五、阶段六都来自分叉会话。** 它们的 conversation id 与阶段一~四不同"
             "（标题分别带「分支 · 分支」和「分支 · …01」），但前一阶段的节点正文逐字一致，"
             "仍是严格超集。\n")
lines.append("**6. 阶段六有一处数字对不上，以及一个时间巧合。** "
             "助手自述「新增 15 个…总计 48 个文件」，但 35 + 15 = **50**，实测也是 **50**；"
             "48 这个数它自己没解释。另外阶段六的快照时间（2026-09-18 07:18）比阶段五晚 7 小时，"
             "而用户恰好在抓取前的几分钟（07:09、07:15）连问两轮 —— 这份分享冻结的正是"
             "「被上一份存档问倒之后」的那段对话。\n")
lines.append("---\n")
lines.append("## 目录约定\n")
lines.append("每个阶段目录内部编号一致，方便横向对比：\n")
lines.append("```\n"
             "00-本阶段说明.md    ← 先看这个\n"
             "01-会话全文.md      ← 逐轮全文还原\n"
             "02-会话原始数据.json ← 页面内嵌结构化数据（保真备份）\n"
             "03-Skill-vX.Y/      ← 该阶段的完整技能文件树\n"
             "04-技能包/          ← 打包好的 zip\n"
             "05-原始页面快照.html ← 分享页原始 HTML（最后防线）\n"
             "06-…                ← 阶段二：被丢弃的中间产物；阶段四/五/六：构建脚本\n"
             "```\n")
lines.append("---\n")
lines.append("## 重建方式\n")
lines.append("本存档由 `99-重建脚本/build_archive.py` 从**六份原始 HTML** 确定性重建。"
             "原始 HTML 保存在各阶段的 `05-原始页面快照.html`。\n")
lines.append("阶段六依赖阶段四与阶段三的产物（v0.5.1 = v0.4 全量 + 增量补丁，"
             "并需要从 v0.3 取回 2 个文件），所以脚本内部按阶段顺序构建、前一阶段的成果直接复用。\n")
lines.append("脚本需用装好 PyYAML 的解释器运行（阶段四、阶段六的生成器需要 yaml）：\n")
lines.append("```\n"
             "C:\\Users\\zhang\\.workbuddy\\binaries\\python\\envs\\default\\Scripts\\python.exe -X utf8 build_archive.py\n"
             "```\n")
open(os.path.join(OUT, "00-总览与六阶段对照.md"), "w", encoding="utf-8", newline="\n").write("\n".join(lines))
p("总览已写入")

# ---------------- 重建脚本一并归档 ----------------
sd = os.path.join(OUT, "99-重建脚本")
os.makedirs(sd, exist_ok=True)
shutil.copyfile(os.path.abspath(__file__), os.path.join(sd, "build_archive.py"))
p("重建脚本已归档")

p("\n完成")
LOG.close()
print("ok")
