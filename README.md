# DSAA2011 Project 2

- `project2.md`: Project 2 prompt extracted from the course announcement.
- `Requirements.md`: course requirements and submission instructions.
- `report.tex`: complete mathematical report source.
- `report.pdf`: compiled report in NeurIPS 2026 format. The seven-page main text is followed by references and submission statements.
- `neurips_2026.sty`: style file needed to rebuild the PDF.

Build in this directory with `latexmk -pdf -interaction=nonstopmode -halt-on-error report.tex`. The style file was copied from the [`neurips2026` directory of `WuizaKaseiyo/paper-templates`](https://github.com/WuizaKaseiyo/paper-templates/tree/92f04364e028736d9f2988c9a2cac6f094961241/neurips2026), which describes it as an unmodified copy of the official NeurIPS 2026 style. Its SHA-256 is `0c1ad36961fcd9198dcc2558cf2793e1df39973bde8264fd701f5e7970672757`.

Before submission, replace the generic author name and add each student's actual contribution statement in the appendix. The report does not include presentation slides.
