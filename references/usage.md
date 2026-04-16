# IEEE PDF Reader Usage

## Dependencies

Best results come from having all three PDF backends available:

- `pypdf`
- `pdfplumber`
- `pdfminer.six`

The script is designed to continue to the next backend when one dependency is missing, but full installation gives the most reliable behavior.

## Command Pattern

Resolve the script path relative to the installed skill directory.

Linux or macOS example:

```bash
python "/path/to/IEEE-pdf-reader/scripts/read_ieee_pdf.py" "/absolute/path/to/paper.pdf" --pages 7-10
```

Windows example:

```bash
python -X utf8 "C:\path\to\IEEE-pdf-reader\scripts\read_ieee_pdf.py" "C:\path\to\paper.pdf" --pages 7-10
```

Read one page:

```bash
python "/path/to/IEEE-pdf-reader/scripts/read_ieee_pdf.py" "/absolute/path/to/paper.pdf" --pages 5
```

Read a small range:

```bash
python "/path/to/IEEE-pdf-reader/scripts/read_ieee_pdf.py" "/absolute/path/to/paper.pdf" --pages 7-10
```

Read the whole paper:

```bash
python "/path/to/IEEE-pdf-reader/scripts/read_ieee_pdf.py" "/absolute/path/to/paper.pdf" --all
```

## Output

Successful extraction is page-delimited:

```text
=== PAGE X/TOTAL ===
```

This format is intended to make downstream reading easier.

## Troubleshooting

### File not found

If the script prints `ERROR: File not found`, verify the PDF path first.

### Missing dependencies

If one or more extractors are unavailable, install the missing libraries and rerun the command.

### All extractors fail

Try a smaller page range first. If the PDF is image-only or heavily scanned, this skill does not guarantee OCR support.

## Reading Strategy

- For journal papers, experiments are often found around pages 7-12.
- For conference papers, experiments are often found around pages 4-7.
- Read in small chunks before expanding to a larger range.
