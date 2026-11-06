#!/usr/bin/env python3
"""Wrapper to build the npj Microgravity publication PDF via scripts/build_npj_pdf.py."""
import sys
from pathlib import Path

# Add scripts directory to path and execute build_npj_pdf
scripts_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(scripts_dir))
import build_npj_pdf

if __name__ == "__main__":
    build_npj_pdf.main()
