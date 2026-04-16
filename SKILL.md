---
name: IEEE-pdf-reader
description: This skill should be used when the user asks to "read IEEE paper", "read PDF paper", "read reference paper", "read TIFS paper", "read IoT paper", or mentions "read XXX paper", "read XXX reference", "read XXX article". Extracts text from IEEE-downloaded PDFs that the built-in Read tool cannot open due to DRM protection.
---

# IEEE PDF Reader

Extract text from IEEE-style research PDFs when the built-in PDF reader cannot open them or returns a password-protected error.

## When to Use

Use this skill when:
- the user wants to read an IEEE paper or a similar research PDF
- the built-in PDF reader cannot open the file
- the user wants a specific page range from a paper
- the user wants to study a paper stored under a local `ref/` or `papers/` directory

## Workflow

1. Locate the target PDF.
2. Read `references/usage.md` for dependencies, command examples, and troubleshooting.
3. Run `scripts/read_ieee_pdf.py` with `--pages` for small ranges or `--all` only when full extraction is really necessary.
4. Read the page-delimited output and continue with the relevant sections only.

## Notes

- Prefer `--pages` for 3-5 page chunks.
- The script tries `pypdf`, `pdfplumber`, and `pdfminer.six` in that order.
- Missing dependencies or backend failures should fall through to the next extractor instead of crashing immediately.
