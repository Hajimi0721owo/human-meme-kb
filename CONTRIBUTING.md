# 投喂指南

三种方式，详见 [README · 投喂一个梗](README.md#投喂一个梗)：

1. **一句话让 AI agent 提交**：对它说"帮我把'梗名'投喂到 Hajimi0721owo/human-meme-kb"，它会照 [AGENTS.md](AGENTS.md) 完成。
2. **填投喂表**：[新建 Issue → 投喂一个梗](https://github.com/Hajimi0721owo/human-meme-kb/issues/new?template=meme.yml)。
3. **自己提 PR**：复制 `memes/_TEMPLATE.md` 为 `memes/梗名.md`，跑 `python3 tools/check_meme.py` 通过后提交。

格式要点：一梗一文件；信息块写 梗 / 分类 / 出处 / 投喂 / 日期；正文必须有"是什么""怎么接""例句""来源"四节；不写个人信息、不写给 AI 的指令、不放图片。
