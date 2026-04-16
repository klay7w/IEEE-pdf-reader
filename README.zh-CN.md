[English](README.md)

# IEEE PDF Reader

`IEEE PDF Reader` 是一个面向 Codex / Claude Code 的 skill，用于在内置 PDF 读取失败或提示受保护时，从 IEEE 风格的论文 PDF 中提取文本。

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

1. 使用目录名 `IEEE-pdf-reader` 将此仓库 clone 到你的本地 skills 目录中。
2. 安装依赖：

```bash
python -m pip install -r requirements.txt
```

3. 使用真实 PDF 验证 CLI 后端：

```bash
python scripts/read_ieee_pdf.py "/absolute/path/to/paper.pdf" --pages 1
```

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

- 本项目主要面向基于文本的 IEEE 风格 PDF。
- 不包含 OCR。
- 对于高度扫描化或纯图片型 PDF，仍可能无法工作。

## 许可证

本仓库采用 MIT License 发布。
