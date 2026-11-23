# Oudra's floor conjectures and related counting formulas

Haobo Ma (ChronoAI Pte Ltd, Singapore), then Wenlin Zhang (National University of Singapore; ChronoAI Pte Ltd, Singapore).

The note proves Ridouane Oudra's cubic conjecture in OEIS A248186, revision 18, FORMULA (October 6, 2023), and his quadratic conjecture in A248183, revision 19, FORMULA (September 6, 2023). An integer-target inversion gives both a general reciprocal threshold formula and alternative proofs of the tetrahedral formulas contributed by Oudra and Chai Wah Wu. The cubic and quadratic jump sequences have exact formulas and complementary densities. The cubic jumps have an exact zero--one discrepancy test against the associated Beatty sequence.

## Build the PDF

Use Tectonic 0.17.0:

```sh
tectonic --untrusted note.tex
```

Alternatively, run the following twice:

```sh
pdflatex -interaction=nonstopmode -halt-on-error note.tex
```

The bibliography is embedded. No BibTeX pass or external mathematical input files are needed. The LaTeX packages are geometry, amsmath, amssymb, amsthm, booktabs, array, longtable and hyperref.

## Exact finite checks

Use Python 3.10 or later, standard library only:

```sh
python3 verify.py --limit 10000 --output checks.json
```

The expected status is `ALL_CHECKS_OK`. The program uses integer inequalities and rational root enclosures, not floating point. It compares both floor conjectures with independently computed least positive indices, checks both zero--one increment assertions and the first 1000 jump positions of each sequence, and confirms the A248188 comparison through 655 and the values 948 versus 949 at 656. It also checks the integer-target inversion and the general reciprocal threshold through target 10000, both tetrahedral formulas through input 10000, the Beatty discrepancy test through jump 10000, and 100 telescoping identities for each residual. Formula comparisons additionally cover input 10001 to bound the final increment; `checks.json` states the advertised ranges through 10000.

## Mathematical coverage

- Lemma 1 proves the integer-target cubic inversion for every positive integer target.
- Theorem 2 proves existence and the cubic conjecture for every integer input greater than two, and the general reciprocal integer-target threshold.
- Corollaries 3--6 give written proofs of the cubic jumps/densities, Beatty discrepancy criterion, quadratic formula and jumps/densities, and the earlier tetrahedral formulas.
- In the [pinned Lean source](https://github.com/the-omega-institute/trureturing/blob/f1c20718fca66e9ef0a4cb5f4f6a9a55badd1ab5/D5/S3/ArithSums/OudraA248186CubicFloor.lean), `D5.S3.ArithSums.OudraA248186CubicFloor.result` proves existence of a natural-valued sequence of least positive admissible indices at all positive inputs and the cubic floor formula for every such sequence at every input greater than two. The general integer-target statement and the corollaries have the written proofs just specified.
- The finite comparisons in `checks.json` are separate from those unbounded statements. Natural densities follow from the counting arguments in the note, not from finite numerical estimates.

The coverage table distinguishes the actual source assertions from additional consequences and the finite Beatty comparison. The complement-name corrections identify the correct complementary pairs. A248189 is a different divisibility question and has no conclusion here. A074279 is cited as an earlier repeated-term result of Wu, not as a newly settled conjecture.

## Attribution and license

The exact primary posing locator is [A248186, revision 18, FORMULA](https://oeis.org/A248186/internal). Clark Kimberling introduced the entry; Ridouane Oudra is credited on the conjecture line. Earlier tetrahedral formulas are credited to Oudra (2021, 2022) and Wu (2024). Wu's published article is [Algorithms for Complementary Sequences, Integers 25 (2025), A95](https://doi.org/10.5281/zenodo.17535229), Section 4, p.22; the corresponding repeated-term treatment is already in [arXiv version 8 (November 3, 2024)](https://arxiv.org/abs/2409.05844v8), Section 4. No priority claim is made.

Copyright 2026 Haobo Ma and Wenlin Zhang. CC BY 4.0 (`cc-by-4.0`).
