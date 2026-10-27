<p align="center"><img src="docs/social.png" alt="人类梗知识库 · 一只猫读不完，全人类一起写" width="720"></p>

<h1 align="center">人类梗知识库 · Human Meme KB</h1>

<p align="center">哈基米在 B 站评论区秒接梗，靠的是这本书。<br>一只猫读不完人类的梗——那就全人类一起写。</p>

<p align="center">
  <a href="#用你的-ai-读它">用你的 AI 读它</a> ·
  <a href="#投喂一个梗">投喂一个梗</a> ·
  <a href="#里面有什么">里面有什么</a> ·
  <a href="AGENTS.md">给 AI agent 用</a> ·
  <a href="CONTRIBUTORS.md">投喂名单</a>
</p>

---

## 用你的 AI 读它

把仓库下载到电脑上，在这个文件夹里打开你的 AI 编程助手（Claude Code、Codex、Cursor、Gemini CLI 都行），它会自己读仓库里的说明：

```sh
git clone https://github.com/Hajimi0721owo/human-meme-kb.git
cd human-meme-kb
```

没装 git 的话，点页面上方绿色的 **Code → Download ZIP**，解压后打开那个文件夹也一样。

然后直接跟它说，比如：

> 这是啥？我能拿它做什么？
>
> "断不了情根"是什么梗？哈基米会怎么接？
>
> 评论区有人回我"这里不送猫娘"，这是什么意思？

这里只有文字，没有要运行的程序。问梗、查出处，你的 AI 只需要读文件；只有你让它投喂时，它才会上网查证、写文件、在 GitHub 上帮你提交。

## 投喂一个梗

<img src="docs/feed.png" alt="投喂一个梗：梗 · 出处 · 怎么接" width="100%">

格式很简单，三样东西：

```text
梗：断不了情根
出处：抖音 AI 视频模板
怎么接：先看清照片里是谁
```

收录后会署上你的昵称。三种投喂方式，挑一个顺手的：

### 1. 让你的 AI 帮你提交（一句话）

在 Claude Code、Codex、Cursor 这类能用终端的 AI agent 里说：

> 帮我把"梗名"这个梗投喂到 Hajimi0721owo/human-meme-kb，出处是……，一般这样接：……，署名写"你的昵称"。

它会读仓库里的 [AGENTS.md](AGENTS.md)，自己上网核实出处、查重、按格式写好、做安全自查、跑检查、提 PR，最后把链接给你。你说得不全也没关系，它会去查。电脑上装了 [GitHub CLI](https://cli.github.com/) 并登录过（`gh auth login`）最顺；没有的话，它会给你一个填好的投喂表链接，点一下提交就行。

### 2. 填表

[点这里打开投喂表](https://github.com/Hajimi0721owo/human-meme-kb/issues/new?template=meme.yml)，填梗、出处、怎么接，提交就好。维护者会帮你整理进库。

### 3. 自己提 PR

复制 [`memes/_TEMPLATE.md`](memes/_TEMPLATE.md) 成 `memes/梗名.md`，填好（记得在"来源"里放链接）后跑一下检查再提交：

```sh
python3 tools/check_meme.py memes/梗名.md
```

范例：[`memes/断不了情根.md`](memes/断不了情根.md)。

> 评论区直接留言也算投喂，会尽量收录。

## 里面有什么

<img src="docs/book.png" alt="里面有什么" width="100%">

| 位置 | 内容 |
| --- | --- |
| [`memes/`](memes/) | **社区投喂的梗**，一梗一文件：是什么、怎么接、例句 |
| [`meme-lab/`](meme-lab/README.md) | 四卷梗考据：DeepSeek 社区名场面、技术梗、大厂互动梗、全网经典梗 |

## 给 AI agent 用

<img src="docs/agent.png" alt="给 AI agent 用：一句话投喂" width="100%">

加载知识库、帮用户一句话投喂（上网核实 → 写条目 → 安全自查 → 格式检查 → 提 PR）的完整说明都在 [AGENTS.md](AGENTS.md)。

## 收录规则

- 一个梗一个文件，写短写准，附上来源链接；查不到的写"待核实"，不编。
- 条目会被 AI 当资料读，所以只写对梗的描述：不写给 AI 的指令、不藏文字、不放要人运行的命令。每个 PR 都会自动检查。
- 不收任何人的真实姓名、联系方式等个人信息；只收文字，不收图片。
- 已经收录过的梗，请补充原条目，不要重复新建。

## 致谢与许可

- AI 娘角色原案来自 B 站画师 [@ZipZipPipe](https://space.bilibili.com/4168597)（草履虫没有记忆），角色与设定归原作者所有。
- 每一位投喂者都记在 [CONTRIBUTORS.md](CONTRIBUTORS.md)。
- 本仓库的文字内容以 [CC BY-NC-SA 4.0](LICENSE) 共享：转载请署名、非商业、相同方式共享。第三方作品与商标说明见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。
