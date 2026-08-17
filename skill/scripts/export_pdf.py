#!/usr/bin/env python3
"""Export a DOCX to PDF with LibreOffice or Microsoft Word."""

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def export_with_libreoffice(docx_path: Path) -> Path:
    soffice = shutil.which("soffice")
    if not soffice:
        raise RuntimeError("LibreOffice (soffice) is not available on PATH.")
    subprocess.run(
        [soffice, "--headless", "--convert-to", "pdf", "--outdir", str(docx_path.parent), str(docx_path)],
        check=True,
    )
    pdf_path = docx_path.with_suffix(".pdf")
    if not pdf_path.exists():
        raise RuntimeError("LibreOffice did not create the PDF.")
    return pdf_path


def export_with_word(docx_path: Path) -> Path:
    if sys.platform != "win32":
        raise RuntimeError("Microsoft Word export is available only on Windows.")
    pdf_path = docx_path.with_suffix(".pdf")
    script = r'''param([string]$InputPath, [string]$OutputPath)
$ErrorActionPreference = 'Stop'
$word = $null
$document = $null
try {
  $word = New-Object -ComObject Word.Application
  $word.Visible = $false
  $document = $word.Documents.Open($InputPath)
  $document.ExportAsFixedFormat($OutputPath, 17)
} finally {
  if ($document) { $document.Close([ref]$false) }
  if ($word) { $word.Quit() }
}'''
    with tempfile.NamedTemporaryFile("w", suffix=".ps1", encoding="utf-8", delete=False) as handle:
        handle.write(script)
        script_path = Path(handle.name)
    try:
        subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(script_path), str(docx_path), str(pdf_path)],
            check=True,
        )
    finally:
        script_path.unlink(missing_ok=True)
    if not pdf_path.exists():
        raise RuntimeError("Microsoft Word did not create the PDF.")
    return pdf_path


def export_pdf(docx_path: Path, engine: str = "auto") -> Path:
    docx_path = docx_path.resolve()
    if not docx_path.exists():
        raise FileNotFoundError(f"DOCX not found: {docx_path}")
    if engine == "libreoffice":
        return export_with_libreoffice(docx_path)
    if engine == "word":
        return export_with_word(docx_path)
    try:
        return export_with_libreoffice(docx_path)
    except RuntimeError as libreoffice_error:
        if sys.platform != "win32":
            raise RuntimeError(
                "Automatic PDF export needs LibreOffice. Install it or export the DOCX manually."
            ) from libreoffice_error
        try:
            return export_with_word(docx_path)
        except Exception as word_error:
            raise RuntimeError(
                "Automatic PDF export needs LibreOffice or Microsoft Word. "
                "Install LibreOffice, use a Windows machine with Word, or export the DOCX manually."
            ) from word_error


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("docx", type=Path)
    parser.add_argument("--engine", choices=("auto", "libreoffice", "word"), default="auto")
    args = parser.parse_args()
    print(f"Created PDF: {export_pdf(args.docx, args.engine)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
