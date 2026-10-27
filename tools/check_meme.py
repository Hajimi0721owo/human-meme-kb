#!/usr/bin/env python3
"""检查 memes/ 里的梗条目：格式、来源、隐藏内容与提示词注入、个人信息。用法：python3 tools/check_meme.py [文件 ...]（不带参数 = 检查全部）。
只用标准库；PR 的自动检查和 agent 提交前自查跑的都是它。"""
import re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
MEMES = ROOT / 'memes'
CATS = ['AI圈日常', '风控博弈', '全网名场面', '二次元', '程序员黑话', '其他']
KEYS = ['梗', '别名', '分类', '出处', '链接', '投喂', '日期']
NEED_KEYS = ['梗', '分类', '出处', '投喂', '日期']
NEED_SECTIONS = ['是什么', '怎么接', '例句', '来源']
PLACEHOLDERS = ['梗的名字', '你的昵称', '一两句话讲清楚这个梗', '写成一两条', '最早从哪来的']
# 注入 / 隐藏内容：条目会被别人的 AI 当上下文读，正文里只能是对梗的描述
HIDDEN = [(r'[\u200b-\u200f\u202a-\u202e\u2060-\u2064\ufeff]', '零宽或方向控制字符（看不见的文字）'),
          (r'<!--', 'HTML 注释（渲染后看不见）'),
          (r'<\s*/?\s*[A-Za-z][A-Za-z0-9-]*(?:\s[^<>]*)?/?>', 'HTML 标签'),            # 任何标签都不行；<https://…> 这种自动链接不算
          (r'!\[[^\]]*\]\(', '图片'),
          (r'(?i)\b(?:curl|wget)\b[^\n]*\|\s*(?:ba|z)?sh\b', '下载并执行脚本的命令')]
INJECT = [r'(?i)ignore (?:all |the )?(?:previous|above|prior) (?:instructions|prompts?)', r'(?i)disregard (?:all |the )?(?:previous|above)',
          r'(?i)system prompt', r'(?i)you are now\b', r'(?i)\bjailbreak\b', r'(?i)developer mode',
          r'忽略(?:之前|上面|以上|前面|所有)(?:的)?(?:所有)?(?:指令|提示|规则|设定)', r'无视(?:之前|上面|以上|所有)(?:的)?(?:指令|规则|设定)',
          r'(?:系统|系统级)提示词', r'(?:新的|最高优先级的?)指令[:：]', r'(?:请|立即)执行(?:以下|下面)(?:的)?命令']
PRIVATE = [(r'[\w.+-]+@[\w-]+\.[\w.]+', '邮箱'), (r'(?<!\d)1[3-9]\d{9}(?!\d)', '手机号'), (r'(?i)\b(?:sk|ghp|gho|github_pat)_[A-Za-z0-9_]{16,}', '密钥')]


def parse(text):
    m = re.match(r'---\n(.*?)\n---\n(.*)', text, re.S)
    if not m:
        return None, text
    meta = {}
    for line in m.group(1).splitlines():
        if ':' in line:
            k, v = line.split(':', 1)
            meta[k.strip()] = v.strip()
    return meta, m.group(2)


def sections(body):
    out, cur = {}, None
    for line in body.splitlines():
        h = re.match(r'##\s+(.+)', line)
        if h:
            cur = h.group(1).strip(); out[cur] = ''
        elif cur:
            out[cur] += line + '\n'
    return out


def check(path, names):
    errs = []
    text = path.read_text(encoding='utf-8')
    if len(text.encode()) > 20000:
        errs.append('文件太长（> 20KB），一个梗写一页就够')
    meta, body = parse(text)
    if meta is None:
        return ['开头缺少 --- 包起来的信息块（照 memes/_TEMPLATE.md）']
    for k in meta:
        if k not in KEYS:
            errs.append(f'信息块里有不认识的字段"{k}"（只能用：{"、".join(KEYS)}）')
    for k in NEED_KEYS:
        if not meta.get(k):
            errs.append(f'信息块缺"{k}"')
    name = meta.get('梗', '')
    if name and path.stem != name.replace('/', '-'):
        errs.append(f'文件名应该是"memes/{name.replace("/", "-")}.md"')
    if meta.get('分类') and meta['分类'] not in CATS:
        errs.append(f'分类"{meta["分类"]}"不在列表里（{"、".join(CATS)}）')
    if meta.get('日期') and not re.fullmatch(r'\d{4}-\d{2}-\d{2}', meta['日期']):
        errs.append('日期格式应为 YYYY-MM-DD')
    sec = sections(body)
    for s in NEED_SECTIONS:
        if not sec.get(s, '').strip():
            errs.append(f'缺少"## {s}"一节，或者这一节是空的')
    for p in PLACEHOLDERS:
        if p in text:
            errs.append(f'模板里的占位文字没改掉："{p}"')
    for pat, what in HIDDEN:
        if re.search(pat, text):
            errs.append(f'包含{what}，条目里只能是普通文字')
    for pat in INJECT:
        m = re.search(pat, text)                                                # 信息块里也查（别名、出处一样会被 AI 读到）
        if m:
            errs.append(f'疑似提示词注入："{m.group(0)}"——条目是给 AI 读的资料，不能写给 AI 的指令')
    src = sec.get('来源', '')
    if src.strip() and not (re.search(r'https?://', src) or '待核实' in src or '亲历' in src):
        errs.append('"## 来源"里至少给一个链接；实在查不到写"待核实"，亲身经历写"亲历"')
    for pat, what in PRIVATE:
        if re.search(pat, text):
            errs.append(f'疑似包含{what}，请删掉个人信息')
    for alias in [name] + [a.strip() for a in re.split(r'[、,，/]', meta.get('别名', '')) if a.strip()]:
        other = names.get(alias)
        if alias and other and other != path.name:
            errs.append(f'"{alias}"已经收录在 memes/{other}，请改那一条而不是新建')
    return errs


def main(argv):
    files = [pathlib.Path(a) for a in argv] or sorted(MEMES.glob('*.md'))
    files = [f.resolve() for f in files if f.name != '_TEMPLATE.md' and f.suffix == '.md']
    names = {}
    for f in MEMES.glob('*.md'):
        if f.name == '_TEMPLATE.md':
            continue
        meta, _ = parse(f.read_text(encoding='utf-8'))
        if meta and meta.get('梗'):
            names.setdefault(meta['梗'], f.name)
    bad = 0
    for f in files:
        if f.parent != MEMES:
            print(f'✗ {f.name}：梗条目要放在 memes/ 目录下'); bad += 1; continue
        errs = check(f, names)
        if errs:
            bad += 1
            print(f'✗ memes/{f.name}'); [print('   - ' + e) for e in errs]
        else:
            print(f'✓ memes/{f.name}')
    print(f'\n{len(files) - bad}/{len(files)} 条通过')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
