#!/usr/bin/env python3
"""
IEEE PDF Reader - Extract text from IEEE papers (including PDFs that fail in the built-in reader).
"""

import argparse
import os
import sys


DETERMINISTIC_ERROR_MESSAGES = {
    "document has no pages",
    "Failed to decrypt with empty password",
}


def configure_stdio():
    """Prefer UTF-8 output when the runtime supports it."""
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        if stream is not None and hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")


def parse_page_range(value):
    """Parse a single page like 5 or a range like 7-10."""
    if "-" in value:
        parts = value.split("-", 1)
        if not parts[0] or not parts[1]:
            raise argparse.ArgumentTypeError("page range must look like START-END")
        try:
            start_page = int(parts[0])
            end_page = int(parts[1])
        except ValueError as exc:
            raise argparse.ArgumentTypeError(
                "page range values must be integers"
            ) from exc
    else:
        try:
            start_page = int(value)
            end_page = int(value)
        except ValueError as exc:
            raise argparse.ArgumentTypeError("page value must be an integer") from exc

    if start_page < 1 or end_page < 1:
        raise argparse.ArgumentTypeError("page numbers must be greater than or equal to 1")
    if start_page > end_page:
        raise argparse.ArgumentTypeError(
            "start page must be less than or equal to end page"
        )

    return start_page, end_page


def normalize_range(total_pages, start_page=None, end_page=None):
    """Clamp and validate the requested page range against the document size."""
    if total_pages < 1:
        return None, "document has no pages"

    if start_page is None:
        start_page = 1
    if end_page is None:
        end_page = total_pages

    if start_page > total_pages:
        return None, f"start page {start_page} exceeds total pages {total_pages}"

    end_page = min(end_page, total_pages)
    return (start_page, end_page), None


def build_page_output(page_chunks, total_pages):
    """Join page text into a consistent page-delimited string."""
    rendered_pages = []
    for page_number, text in page_chunks:
        if text and text.strip():
            rendered_pages.append(f"=== PAGE {page_number}/{total_pages} ===\n{text.strip()}")

    if rendered_pages:
        return "\n\n".join(rendered_pages), None
    return None, "No text extracted"


def classify_error(message):
    """Classify failures for cleaner final reporting."""
    if message in DETERMINISTIC_ERROR_MESSAGES:
        return "deterministic"
    if message.startswith("start page "):
        return "deterministic"
    return "backend"


def build_failure_result(backend, message):
    """Normalize backend failures into a structured result."""
    normalized_message = message or "Unknown error"
    return {
        "backend": backend,
        "kind": classify_error(normalized_message),
        "message": normalized_message,
    }


def summarize_failures(failures):
    """Choose between collapsed deterministic output and detailed backend output."""
    deterministic_failures = [
        failure for failure in failures if failure["kind"] == "deterministic"
    ]
    if deterministic_failures:
        return {
            "mode": "collapsed",
            "primary_error": deterministic_failures[0]["message"],
            "backend_count": len(failures),
            "suppressed_count": max(0, len(failures) - 1),
        }
    return {
        "mode": "detailed",
        "failures": failures,
    }


def build_next_step(summary):
    """Return a concise next-step hint for the current failure mode."""
    if summary["mode"] == "collapsed":
        primary_error = summary["primary_error"]
        if primary_error.startswith("start page "):
            return "Next step: retry a smaller page range."
        if primary_error == "document has no pages":
            return "Next step: verify the PDF is not empty or corrupted."
        if primary_error == "Failed to decrypt with empty password":
            return "Next step: verify the PDF can be opened without a password in another reader."
    return "Next steps: verify the file path, install missing dependencies, or retry a smaller page range."


def read_with_pypdf(pdf_path, start_page=None, end_page=None):
    """Read PDF using pypdf."""
    try:
        from pypdf import PdfReader
    except ImportError:
        return None, "pypdf not installed"

    try:
        reader = PdfReader(pdf_path)
        if reader.is_encrypted:
            result = reader.decrypt("")
            if result == 0:
                return None, "Failed to decrypt with empty password"

        total_pages = len(reader.pages)
        page_range, range_error = normalize_range(total_pages, start_page, end_page)
        if range_error:
            return None, range_error

        page_chunks = []
        normalized_start, normalized_end = page_range
        for index in range(normalized_start - 1, normalized_end):
            page_text = reader.pages[index].extract_text()
            page_chunks.append((index + 1, page_text or ""))

        return build_page_output(page_chunks, total_pages)
    except Exception as exc:
        return None, f"pypdf error: {exc}"


def read_with_pdfplumber(pdf_path, start_page=None, end_page=None):
    """Read PDF using pdfplumber."""
    try:
        import pdfplumber
    except ImportError:
        return None, "pdfplumber not installed"

    try:
        with pdfplumber.open(pdf_path) as pdf:
            total_pages = len(pdf.pages)
            page_range, range_error = normalize_range(total_pages, start_page, end_page)
            if range_error:
                return None, range_error

            page_chunks = []
            normalized_start, normalized_end = page_range
            for index in range(normalized_start - 1, normalized_end):
                page_text = pdf.pages[index].extract_text()
                page_chunks.append((index + 1, page_text or ""))

        return build_page_output(page_chunks, total_pages)
    except Exception as exc:
        return None, f"pdfplumber error: {exc}"


def read_with_pdfminer(pdf_path, start_page=None, end_page=None):
    """Read PDF using pdfminer.six one page at a time."""
    try:
        from pdfminer.high_level import extract_pages, extract_text
        from pdfminer.layout import LAParams
    except ImportError:
        return None, "pdfminer.six not installed"

    try:
        total_pages = sum(1 for _ in extract_pages(pdf_path))
        page_range, range_error = normalize_range(total_pages, start_page, end_page)
        if range_error:
            return None, range_error

        laparams = LAParams()
        page_chunks = []
        normalized_start, normalized_end = page_range
        for page_number in range(normalized_start, normalized_end + 1):
            page_text = extract_text(
                pdf_path,
                laparams=laparams,
                page_numbers=[page_number - 1],
            )
            page_chunks.append((page_number, page_text or ""))

        return build_page_output(page_chunks, total_pages)
    except Exception as exc:
        return None, f"pdfminer error: {exc}"


def read_pdf(pdf_path, start_page=None, end_page=None):
    """Try all supported backends in order."""
    methods = [
        ("pypdf", read_with_pypdf),
        ("pdfplumber", read_with_pdfplumber),
        ("pdfminer.six", read_with_pdfminer),
    ]

    errors = []
    for method_name, method in methods:
        text, error = method(pdf_path, start_page, end_page)
        if text:
            return text, None
        errors.append(build_failure_result(method_name, error))

    return None, errors


def build_parser():
    parser = argparse.ArgumentParser(description="Extract text from IEEE PDF papers")
    parser.add_argument("pdf_path", help="Path to the PDF file")
    page_group = parser.add_mutually_exclusive_group(required=True)
    page_group.add_argument(
        "--pages",
        type=parse_page_range,
        help="Page number or range (for example: 5 or 7-10)",
    )
    page_group.add_argument(
        "--all",
        action="store_true",
        help="Read all pages in the document",
    )
    return parser


def main():
    configure_stdio()
    parser = build_parser()
    args = parser.parse_args()

    if not os.path.exists(args.pdf_path):
        print(f"ERROR: File not found: {args.pdf_path}", file=sys.stderr)
        sys.exit(1)

    start_page = None
    end_page = None
    if args.pages:
        start_page, end_page = args.pages

    text, errors = read_pdf(args.pdf_path, start_page, end_page)
    if text:
        print(text)
        return

    summary = summarize_failures(errors)
    if summary["mode"] == "collapsed":
        print(f"ERROR: {summary['primary_error']}", file=sys.stderr)
        if summary["suppressed_count"] > 0:
            print(
                f"Tried {summary['backend_count']} backends; "
                f"{summary['suppressed_count']} additional backend results were suppressed.",
                file=sys.stderr,
            )
    else:
        print("ERROR: All methods failed:", file=sys.stderr)
        for error in summary["failures"]:
            print(f"- {error['backend']}: {error['message']}", file=sys.stderr)
    print(build_next_step(summary), file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
