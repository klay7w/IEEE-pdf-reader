# IEEE PDF Reader

`IEEE PDF Reader` is a Codex / Claude Code skill for extracting text from IEEE-style research PDFs when built-in PDF reading fails or reports password-protection issues.

It is designed for skill users who want a small, clone-and-use repository rather than a general Python package.

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

1. Clone this repository into your local skills directory using the folder name `IEEE-pdf-reader`.
2. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

3. Verify the CLI backend on a real PDF:

```bash
python scripts/read_ieee_pdf.py "/absolute/path/to/paper.pdf" --pages 1
```

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

- This project is intended for text-based IEEE-style PDFs.
- OCR is not included.
- Highly scanned or image-only PDFs may still fail.

## License

This repository is released under the MIT License.
