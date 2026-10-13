# DSAA2011 Project 2 — Sharp Guarantees for Ensemble Voting

本项目在原题模型内研究：已知成员准确率和两两相关性时，多数投票的准确率能被限制到什么程度，什么时候能够**保证**优于单个成员。

## 本轮实质改进

- 保留 Part I 的独立情形、相同/不同边际准确率的精确界，以及 Part II 的完整三分类器答案。
- 对任意奇数 `K`、相同 `p` 和相同两阶矩，用整数二次证书和三角形分割给出精确区间与达到界的分布。
- 相邻证书作差后，只需一次取整和常数次运算求精确界，无须调用 LP。
- 给出 `A_min > p` 的必要且充分相关性阈值，并构造边界及阈值以上的反例。
- 将相对 C-bound 的改进分为正确失败阈值修正、整数支撑修正；同时与 shifted Cantelli 比较。
- 例：`p=0.6, rho=0` 时，`K=25` 的最差准确率为 `0.6`，首个严格保证收益的奇数规模是 `K=27`。

**贡献定位：**离散矩界、对称化和少量支撑点的极端分布属于经典方法。本项目提供初等、统一的推导及显式推论，不宣称首次发现这些概率界。六篇相关论文已取得原文并阅读相关章节；Boros–Prékopa (1989) 只核对了元数据和摘要，尚未逐式比较。详见阅读笔记。

## 阅读入口

- [report.pdf](report.pdf)：NeurIPS 2026 格式，8 页正文，参考文献和附录另计（共 10 页）。
- [report.tex](report.tex)：报告源文件。
- [presentation.pdf](presentation.pdf) / [presentation.tex](presentation.tex)：13 页演示稿及源文件。
- [notes/literature.md](notes/literature.md)：中文阅读笔记、具体章节、已有结果与项目贡献的对应关系。
- [notes/derivation.md](notes/derivation.md)：中文推导笔记，包括常数时间公式及达到性证明。
- [notes/sources.json](notes/sources.json)：原文链接、访问/阅读状态与下载文件 SHA-256；不在仓库分发第三方论文 PDF。
- [project.ipynb](project.ipynb)：已实际执行的复现 notebook。
- [experiments/verify.py](experiments/verify.py)：公式、达到界的构造和独立 LP 检查。
- [results/verification.json](results/verification.json)、[results/comparison.csv](results/comparison.csv)：本次验证统计与表格原始数据。
- [project2.md](project2.md)、[Requirements.md](Requirements.md)：原始任务及课程提交要求。

## 重现

使用 Python 3.12。建议把环境放在仓库外；已测试的主要依赖版本为 NumPy 2.3.5、SciPy 1.17.0、Matplotlib 3.10.8，完整直接依赖见 `requirements.txt`。

```bash
python3 -m venv /tmp/dsaa-venv
. /tmp/dsaa-venv/bin/activate
python -m pip install -r requirements.txt
python experiments/verify.py
python experiments/plot.py
```

验证固定种子为 `20261013`，包括 702 组计数 LP、41 组完整二元联合分布 LP（均验证上下端点）、720 组阈值检查、2,576 个逐点证书值和 36 个不可行输入。独立 LP 与公式的最大误差约 `2.6e-14`。

每个数值表格均从同一结果自动生成，包括 `results/comparison_table.tex`，避免手抄数值不一致。数值验证不能代替报告中的证明。

如需重新执行并保存 notebook 的真实输出：

```bash
python experiments/execute_notebook.py
```

该命令使用当前 Python 环境启动内核；需要 `requirements.txt` 中的 notebook 依赖。六个代码单元已执行成功，包含完整验证和图形生成。

PDF 构建需要 `latexmk`、pdfLaTeX、常用 AMS/graphics 包和 Beamer。已测试 latexmk 4.86、TeX Live 2025/dev/Debian。

```bash
mkdir -p /tmp/dsaa-pdf
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=/tmp/dsaa-pdf report.tex
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=/tmp/dsaa-pdf presentation.tex
```

生成的新 PDF 在 `/tmp/dsaa-pdf`。确认后再替换仓库中发布的 PDF；辅助文件不进入 Git。

`neurips_2026.sty` 保持原样。其来源为 [WuizaKaseiyo/paper-templates 的 NeurIPS 2026 模板](https://github.com/WuizaKaseiyo/paper-templates/tree/92f04364e028736d9f2988c9a2cac6f094961241/neurips2026)，SHA-256 为 `0c1ad36961fcd9198dcc2558cf2793e1df39973bde8264fd701f5e7970672757`。报告使用 `main,final`，没有使用 preprint 选项。

## 提交前仍需团队完成

真实成员姓名、每人的准确贡献声明和 GroupID 尚未提供，因此保留明确占位。AI 使用声明已写入报告，需要按最终实际工作核对。

按 `Requirements.md`，将最终文件命名为：

- `report_GroupID_taskB-project2.pdf`
- `presentation_GroupID_taskB-project2.pdf`
- `project_GroupID_taskB-project2.ipynb`
- `requirements_GroupID_taskB-project2.txt`

为了让 notebook 的导入可重现，提交 ZIP 还应包含 `experiments/`、`results/`、`figures/` 和 README（保持相对目录）；不要只提交一个依赖外部脚本的 notebook。团队应在最终提交前理解并核查所有证明，尤其是对称化、二次证书、阈值 iff 条件和有限样本局限。
