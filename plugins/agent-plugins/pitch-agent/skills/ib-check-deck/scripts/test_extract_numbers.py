#!/usr/bin/env python3
"""Regression check: python test_extract_numbers.py  (no framework, no fixtures)."""
import subprocess, sys, tempfile, pathlib

DECK = """## Slide 3
FY2025 revenue of $500M, EBITDA margin of 22%.

## Slide 8
Revenue reached $500MM in fiscal 2025.

## Slide 15
Revenue of $485M for FY2025 at a 9.7x multiple.
"""

here = pathlib.Path(__file__).parent
with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as f:
    f.write(DECK); path = f.name

out = subprocess.run([sys.executable, str(here / "extract_numbers.py"), path, "--check"],
                     capture_output=True, text=True).stderr

# $500M (slides 3, 8) vs $485M (slide 15) is 3% apart — the headline case.
assert "$485M" in out and "$500M" in out, f"real mismatch not flagged:\n{out}"
# 22% and 9.7x must not be compared against dollar figures.
assert "22%" not in out and "9.7x" not in out, f"unit-crossing false positive:\n{out}"
print("PASS")
