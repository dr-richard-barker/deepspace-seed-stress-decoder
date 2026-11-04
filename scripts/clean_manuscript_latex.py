#!/usr/bin/env python3
"""
Clean all raw LaTeX math and unrendered citation syntax in report/manuscript_npj_microgravity.md.
"""

from pathlib import Path

TARGET = Path("report/manuscript_npj_microgravity.md")

REPLACEMENTS = [
    # LaTeX math expressions -> clean UTF-8 text and semantic HTML
    (r"($56.5\text{ kPa} / 8.2\text{ psia}$, $34\%\ \text{O}_2$)", "(56.5 kPa / 8.2 psia, 34% O₂)"),
    (r"at $56.5\text{ kPa}$", "at 56.5 kPa"),
    (r"($50\text{ kPa}$)", "(50 kPa)"),
    (r"($10\text{ kPa}$)", "(10 kPa)"),
    (r"($\text{NES} = +1.98$)", "(NES = +1.98)"),
    (r"($\text{NES} = +1.98, \text{FDR} = 0.0007$)", "(NES = +1.98, FDR = 0.0007)"),
    (r"($\text{NES} = +2.04, \text{FDR} < 0.0001$)", "(NES = +2.04, FDR < 0.0001)"),
    (r"($\text{NES} = +2.30$)", "(NES = +2.30)"),
    (r"($\text{NES} = -2.09$)", "(NES = -2.09)"),
    (r"($\text{NES} = +1.59$)", "(NES = +1.59)"),
    (r"($\mu g$)", "(µg)"),
    (r"$\gamma$-rays", "γ-rays"),
    (r"(~$45\ \mu\text{T}$)", "(~45 µT)"),
    (r"($< 1\ \text{nT}$)", "(< 1 nT)"),
    (r"($< 40\ \text{nT}$)", "(< 40 nT)"),
    (r"($50\text{ kPa}$, $21\ \text{kPa}\ pO_2$)", "(50 kPa, 21 kPa pO₂)"),
    (r"($0.16\text{ g}$ Moon, $0.38\text{ g}$ Mars)", "(0.16 g Moon, 0.38 g Mars)"),
    (r"($\log_2\text{FC}$ indexed", "(log₂FC indexed"),
    (r"($|\text{NES}| \ge 1.5, \text{FDR} < 0.25$)", "(|NES| ≥ 1.5, FDR < 0.25)"),
    (r"($50\text{ kPa}$ Norm$O_2$)", "(50 kPa NormO₂)"),
    (r"($50\text{ kPa}$ Norm$O_2$, $50\text{ kPa}$ Air, $10\text{ kPa}$ extreme)", "(50 kPa NormO₂, 50 kPa Air, 10 kPa extreme)"),
    (r"pressure $\times$ hypoxia", "pressure × hypoxia"),
    (r"baro $\times$ hypoxia", "baro × hypoxia"),
    (r"($\log_2 \text{err\_ratio}$ across 20,869 loci)", "(log₂ error ratio across 20,869 loci)"),
    (r"($H_2O_2$, ozone $O_3$, methyl viologen / superoxide)", "(H₂O₂, ozone O₃, methyl viologen / superoxide)"),
    (r"(NMF $z = +7.96$)", "(NMF *z* = +7.96)"),
    (r"($z = +7.96$)", "(*z* = +7.96)"),
    (r"NMF localization $|z| \ge 2.0$", "NMF localization |z| ≥ 2.0"),
    (r"NMF localization panel, $|z| \ge 2.0$", "NMF localization panel, |z| ≥ 2.0"),
    (r"$\ge 20$", "≥ 20"),
    (r"$\beta_{\text{hypobaria}}$ (pure barosensory effect), $\beta_{\text{hypoxia}}$ (pure hypoxia effect), and $\beta_{\text{interaction}}$",
     "β_hypobaria (pure barosensory effect), β_hypoxia (pure hypoxia effect), and β_interaction"),
    (r"$\log_2(\text{err\_spaceflight} / \text{err\_ground})$", "log₂(err_spaceflight / err_ground)"),
    (r"to $\log_2\text{FC}$", "to log₂FC"),
    (r"($pfp$)", "(*pfp*)"),
    (r"FDR $q$-values", "FDR *q*-values"),
    (r"achieved $|\text{NES}| \ge 1.5$ and $\text{FDR} < 0.25$", "achieved |NES| ≥ 1.5 and FDR < 0.25"),
    (r"($|\text{NES}| \ge 1.5, \text{FDR} < 0.25$;", "(|NES| ≥ 1.5, FDR < 0.25;"),
    (r"FDR $< 0.05$", "FDR < 0.05"),
    (r"($0 \le n \le 15$)", "(0 ≤ n ≤ 15)"),

    # Citations -> clean academic standard
    (r"[@paul2017spaceflight; @ferl2015spaceflight]", "(Paul et al., 2017; Ferl & Paul, 2015)"),
    (r"[@zupanska2019spaceflight; @barker2020cross]", "(Zupanska et al., 2019; Barker et al., 2020)"),
    (r"[@paul2012arabidopsis; @ferl2015spaceflight]", "(Paul et al., 2012; Ferl & Paul, 2015)"),
    (r"[@parmagnani2022biomolecules; @agliassa2021scirep]", "(Parmagnani et al., 2022; Agliassa & Maffei, 2021)"),
    (r"[@hollmann2025nature]", "(Hollmann et al., 2025)"),
    (r"[@martin2026natureplants]", "(Martin et al., 2026)"),
    (r"[@liew2024natureplants]", "(Liew et al., 2024)"),
    (r"[@reina2009plantj]", "(Reina-Pinto et al., 2009)"),
]

def main():
    content = TARGET.read_text(encoding="utf-8")
    for old, new in REPLACEMENTS:
        if old not in content:
            print(f"NOT FOUND: {old}")
        else:
            content = content.replace(old, new)
            print(f"REPLACED: {old[:40]} -> {new[:40]}")

    TARGET.write_text(content, encoding="utf-8")
    print("\nWrote cleaned content to", TARGET)

    # Check for remaining dollars
    remaining = [line for line in content.splitlines() if "$" in line]
    print(f"Remaining lines with $: {len(remaining)}")
    for r in remaining:
        print("  ", r[:100])

if __name__ == "__main__":
    main()
