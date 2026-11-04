#!/usr/bin/env python3
"""
Clean up raw LaTeX/math formatting artifacts in GitHub Pages markdown files (docs/*.md).
Replaces LaTeX syntax with clean, standard UTF-8 and HTML subscripts/superscripts.
Preserves all numbers, names, and biological accuracy.
"""

import sys
from pathlib import Path

DOCS_DIR = Path("docs")

REPLACEMENTS = {
    # docs/index.md and docs/stimuli_decoders_synthesis.md
    r"$50\text{--}56.5\text{ kPa}$": "50–56.5 kPa",
    r"($50\text{--}56.5\text{ kPa}$ hypobaria)": "(50–56.5 kPa hypobaria)",
    r"($56.5\text{ kPa} / 8.2\text{ psia}$, $34\%\ \text{O}_2$)": "(56.5 kPa / 8.2 psia, 34% O₂)",
    r"($P_{\text{total}}$)": "(*P*<sub>total</sub>)",
    r"($pO_2$)": "(*p*O₂)",
    r"($50\text{ kPa}$ Norm$O_2$ and Hypo$O_2$)": "(50 kPa NormO₂ and HypoO₂)",
    r"($50\text{ kPa}$ Norm$O_2$, $50\text{ kPa}$ Hypo$O_2$)": "(50 kPa NormO₂, 50 kPa HypoO₂)",
    r"($50\text{ kPa}$ Norm$O_2$)": "(50 kPa NormO₂)",
    r"$50\text{ kPa}$ Norm$O_2$ and Hypo$O_2$ profiles": "50 kPa NormO₂ and HypoO₂ profiles",
    r"$\rightarrow$": "→",
    r"Contrasts ($N$)": "Contrasts (*N*)",
    r"acute $\gamma$": "acute γ",
    r"(Acute $\gamma$)": "(Acute γ)",
    r"($\log_2 \text{err\_ratio}$)": "(log₂ error ratio)",
    r"$H_2O_2$": "H₂O₂",
    r"$^1\text{O}_2$": "¹O₂",
    r"$O_3$": "O₃",
    r"($\beta=0.5$)": "(β = 0.5)",
    r"49 contrasts $\times$ 123 panels": "49 contrasts × 123 panels",
    r"($4^\circ\text{C}$ at 3 h and 24 h)": "(4 °C at 3 h and 24 h)",
    r"(IAA, $1\,\mu\text{M}$ for 3 h)": "(IAA, 1 µM for 3 h)",
    r"$\text{GA}_3$": "GA₃",
    r"(BL, $10\,\text{nM}$ for 3 h)": "(BL, 10 nM for 3 h)",
    r"($<30\text{ nT}$ NMF)": "(< 30 nT NMF)",
    r"($<30\text{ nT}$)": "(< 30 nT)",
    r"($|\text{NES}| \ge 1.5$, $\text{FDR} < 0.05$)": "(|NES| ≥ 1.5, FDR < 0.05)",
    r"(expression localization $z = +7.96$, $P = 8.7 \times 10^{-16}$)": "(expression localization *z* = +7.96, *P* = 8.7 × 10⁻¹⁶)",
    r"($\text{NES} = +1.98$)": "(NES = +1.98)",
    r"($\text{NES} = +2.30$)": "(NES = +2.30)",
    r"($z = +7.96$)": "(*z* = +7.96)",
    r"($\mu g$)": "(µg)",
    r"($2\,g$)": "(2 g)",
    r"Python $\ge 3.10$, R $\ge 4.4$": "Python ≥ 3.10, R ≥ 4.4",
}

def clean_file(path: Path):
    content = path.read_text(encoding="utf-8")
    original = content
    changes_made = 0

    for old, new in REPLACEMENTS.items():
        if old in content:
            count = content.count(old)
            content = content.replace(old, new)
            print(f"  [{path.name}] Replaced '{old}' -> '{new}' ({count}x)")
            changes_made += count

    # Check for any remaining dollar signs
    lines_with_dollar = [
        (i + 1, line)
        for i, line in enumerate(content.splitlines())
        if "$" in line and not line.strip().startswith("$") and not "```" in line
    ]

    if lines_with_dollar:
        print(f"  [{path.name}] WARNING: Found {len(lines_with_dollar)} remaining lines with '$':")
        for line_no, text in lines_with_dollar:
            print(f"    Line {line_no}: {text}")

    if content != original:
        path.write_text(content, encoding="utf-8")
        print(f"Updated {path} ({changes_made} replacements).")
    else:
        print(f"No changes needed for {path}.")

def main():
    md_files = sorted(DOCS_DIR.glob("*.md"))
    if not md_files:
        print("No markdown files found in docs/")
        sys.exit(1)

    for md_file in md_files:
        print(f"Processing {md_file}...")
        clean_file(md_file)

if __name__ == "__main__":
    main()
