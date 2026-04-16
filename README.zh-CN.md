[English](README.md)

# IEEE PDF Reader

`IEEE PDF Reader` 是一个面向 Codex / Claude Code 的 skill，用于在内置 PDF 读取失败或提示受保护时，从 IEEE 论文 PDF 中提取文本。

## 仓库结构

```text
IEEE-pdf-reader/
├── README.md
├── README.zh-CN.md
├── LICENSE
├── .gitignore
├── requirements.txt
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   └── usage.md
└── scripts/
    └── read_ieee_pdf.py
```

## 安装

### Codex

将此 skill 安装到你的全局 Codex skills 目录中，并保持仓库目录名为 `IEEE-pdf-reader`。

```bash
mkdir -p ~/.codex/skills
cd ~/.codex/skills
git clone https://github.com/klay7w/IEEE-pdf-reader.git IEEE-pdf-reader
cd IEEE-pdf-reader
python -m pip install -r requirements.txt
python scripts/read_ieee_pdf.py "/absolute/path/to/paper.pdf" --pages 1
```

最后一条命令用于做一次 CLI 层面的 smoke check，确认 PDF 后端工作正常。

### Claude Code

将此 skill 安装到你的全局 Claude Code skills 目录中，并保持仓库目录名为 `IEEE-pdf-reader`。

```bash
mkdir -p ~/.claude/skills
cd ~/.claude/skills
git clone https://github.com/klay7w/IEEE-pdf-reader.git IEEE-pdf-reader
cd IEEE-pdf-reader
python -m pip install -r requirements.txt
python scripts/read_ieee_pdf.py "/absolute/path/to/paper.pdf" --pages 1
```

如果 `~/.claude/skills` 是在 Claude Code 已经运行后才创建的，请重启 Claude Code，使其开始监视该目录。

### 验证安装

开启一个新的会话，并让 agent 读取一篇 IEEE PDF。如果安装正确，在内置 PDF 读取不可用时，agent 应该会使用 `IEEE PDF Reader`。

## Skill 用法

- 保持仓库目录名为 `IEEE-pdf-reader`。
- 使用 `SKILL.md` 中描述的触发词。
- 读取 `references/usage.md` 获取提取命令和故障排查信息。

## 已验证功能

当前版本已经验证：

- 单页提取
- 页段提取
- 全文提取
- 确定性错误处理
- 后端回退行为

## 限制说明

- 本项目主要面向基于文本的 IEEE PDF。
- 不包含 OCR。
- 对于高度扫描化或纯图片型 PDF，仍可能无法工作。

## 许可证

本仓库采用 MIT License 发布。
