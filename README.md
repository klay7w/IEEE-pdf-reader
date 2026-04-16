[中文说明](README.zh-CN.md)

# IEEE PDF Reader

`IEEE PDF Reader` is a Codex / Claude Code skill for extracting text from IEEE research PDFs when built-in PDF reading fails or reports password-protection issues.

## Repository Structure

```text
IEEE-pdf-reader/
├── README.md
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

## Install

### Codex

Install this skill into your global Codex skills directory. Keep the repository directory name as `IEEE-pdf-reader`.

```bash
mkdir -p ~/.codex/skills
cd ~/.codex/skills
git clone https://github.com/klay7w/IEEE-pdf-reader.git IEEE-pdf-reader
cd IEEE-pdf-reader
python -m pip install -r requirements.txt
python scripts/read_ieee_pdf.py "/absolute/path/to/paper.pdf" --pages 1
```

The final command is a CLI-level smoke check to confirm the PDF backend is working.

### Claude Code

Install this skill into your global Claude Code skills directory. Keep the repository directory name as `IEEE-pdf-reader`.

```bash
mkdir -p ~/.claude/skills
cd ~/.claude/skills
git clone https://github.com/klay7w/IEEE-pdf-reader.git IEEE-pdf-reader
cd IEEE-pdf-reader
python -m pip install -r requirements.txt
python scripts/read_ieee_pdf.py "/absolute/path/to/paper.pdf" --pages 1
```

If `~/.claude/skills` is created after Claude Code is already running, restart Claude Code so it begins watching the directory.

### Verify Installation

Start a new session and ask the agent to read an IEEE PDF. If installation is correct, the agent should use `IEEE PDF Reader` when built-in PDF reading is unavailable.

## Skill Usage

- Keep the repository directory name as `IEEE-pdf-reader`.
- Use the trigger phrases described in `SKILL.md`.
- Read `references/usage.md` for extraction commands and troubleshooting.

## Verified Behavior

The current release has been validated for:

- single-page extraction
- page-range extraction
- full-document extraction
- deterministic error handling
- backend fallback behavior

## Limitations

- This project is intended for text-based IEEE PDFs.
- OCR is not included.
- Highly scanned or image-only PDFs may still fail.

## License

This repository is released under the MIT License.
