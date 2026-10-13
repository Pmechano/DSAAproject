# 论文阅读笔记与贡献定位

阅读日期：2026-10-14（Asia/Taipei）。下文区分“读过原文相关章节”与“仅核对书目信息”。
这里的阅读不是把每篇论文的全部证明逐行复核；标明了实际使用的章节。
论文 PDF 下载在工作区外部研究目录，不复制进 Git 仓库。下载链接和 SHA-256 见 [sources.json](sources.json)。

## 阅读结论先行

原报告解决了作业，但不能把“相关性不够”“负相关不保证好”“用 LP 优化概率”“最多三个计数状态达到二阶矩界”当作新发现。
这些问题有相当直接的前人工作。改进方向应当是**初等且统一的解法、常数时间求值、精确的有限 K 保证收益阈值及其整数修正**。
报告不宣称这些概率界是文献首创，也不把没有找到相同公式视为不存在先前结果的证据。

## 1. Kuncheva & Whitaker (2003), Measures of Diversity...

原文：[作者网站 PDF](https://lucykuncheva.co.uk/papers/lkml.pdf)。
重点阅读：摘要，§§3–5，§6.3 的枚举例子，§7 总结（期刊 pp.194–195、202–203 尤其直接相关）。

- 讨论十种分类器多样性指标。两两相关性、disagreement、double fault 等不能直接决定整个投票的性能。
- §6.3 使用 K=3、p=0.6、30 个样本的八格枚举。其例子平均相关性为 −0.0648，但多数投票只有约 0.5667，已经低于单个成员。
- §7 已经指出，某些足够高的多样性阈值能保证优于成员。**阈值存在的想法不新**。
- 该文中的平均相关性与“每一对相关性都相同”不是同一假设，引用时不能混淆。

对本项目的作用：提出明确且保守的研究问题——在固定 p、ρ、有限 K 下，给出可达到的精确边界，而不把单个例子重新包装成发现。

## 2. Germain et al. (2015), Risk Bounds for the Majority Vote...

原文：[JMLR PDF](https://jmlr.org/papers/volume16/germain15a/germain15a.pdf)。
重点阅读：§4.1 的 margin、disagreement 对应关系，§4.3 Theorem 11，§4.4.1 Proposition 13（期刊 pp.797–800），§4.4 后续讨论与结论。

设 M=2S/K−1，E M>0。Theorem 11 的 C-bound 对应准确率保证

    P(M>0) ≥ (E M)²/E[M²].

这使用一侧 Chebyshev/Cantelli 不等式。Proposition 13 构造在 0 和 E[M²]/E[M] 上取值的 margin 以说明特定连续矩类下的可达到性。
但奇数 K 的等权二元投票不能产生 margin=0，所以不能直接把该连续可达到性当成当前有限投票格点上的可达到性。

对本项目的作用：

1. 精确说明为什么原 C-bound 可能松。
2. 比较必须公平：先把失败阈值移动到 S≤m，得到 d²/(d²+σ²)，再研究整数支撑还能带来多少改进。
3. 本项目只处理给定人口矩的确定性界，不声称取代该文的 PAC-Bayesian 有限样本与学习算法贡献。

## 3. Masegosa et al. (2020), Second Order PAC-Bayesian Bounds...

原文：[arXiv:2007.13532v2](https://arxiv.org/pdf/2007.13532)。
重点阅读：§§2–3，Theorems 3、5、6，§4 开头关于从 oracle bounds 到经验界的区分。

- Theorem 3 用二阶 Markov 得到风险上界 4 E tandem loss。
- binary 情形里，joint error 可由平均错误率和 disagreement 表达（Lemma 4 / Theorem 5）。
- Theorem 6 的 C-tandem 形式等价于先前的 C-bound。§3.3 明确讨论其 oracle tightness 与估计、优化难度之间的区别。

对本项目的作用：我们使用的是准确已知的 p、r，比较的是 **population/oracle** 界。不能把数值上优于一个 population 下界说成优于整套 PAC-Bayesian 学习方法。权重优化与样本误差均不扩展为本报告主线。

## 4. Bertsimas & Popescu (2005), Optimal Inequalities in Probability Theory...

原文：[MIT 作者主页 PDF](https://www.mit.edu/~dbertsim/papers/MomentProblems/Optimal-inequalities-in-probability-theory-A-convex-optimization-approach-SIAM15.pdf)。
重点阅读：§1、§2 的 primal/dual 形式与 Theorems 2.1–2.2（pp.784–785），§6.2 / Proposition 6.3 的一侧界。

核心做法：在给定矩的分布上优化事件概率；寻找一个逐点控制事件指示函数的多项式，取期望便得到界。匹配的分布证明尖锐性。

对本项目的作用：二次证书与三点支持的思想是经典背景。我们的证明直接逐整数验证二次式、再画二维扇形分割，避免依赖一般强对偶、半正定优化或更深的矩理论。

## 5. 追加：Kuncheva et al. (2003), Limits on the Majority Vote Accuracy...

原文：[作者网站 PDF](https://lucykuncheva.co.uk/papers/lkpaa.pdf)。
重点阅读：§2 的三分类器枚举和 Table 6，§3 的 success/failure patterns，§4.3 和 §5。
作者网站和 PDF 标明正式发表：Pattern Analysis and Applications 6:22–31, 2003。
原报告所引 2003 diversity 论文把它列为 2000 年版本；本项目使用取得的 2003 年发表版本。

- 以 Yule's Q 而不是 Pearson ρ 描述两两依赖。
- 已有相同 p、不同 K 的多数投票上下限和达到特定限值的 success/failure patterns。
- Table 6 的数值阈值面向有限枚举，正文“favorable”的比较对象还包括独立投票；这不等于本文人口矩下“严格优于 p”的完整 iff 条件。
- 本文不能把文献里的 Q 直接替换成 Pearson ρ，更不能把平均 Q 的结论当成所有两阶矩都相等的结论。

对本项目的作用：必须把“极端依赖构造”也列为前人已有思想。本文的阈值应以自己的完整证明为依据，不以该文的图表代替证明。

## 6. 追加：Fontana & Semeraro (2021), Exchangeable Bernoulli Distributions...

原文：[arXiv:2101.07693v1](https://arxiv.org/pdf/2101.07693)。
重点阅读：§2，特别是 (2.1)–(2.5)、Propositions 2.1–2.3；§3 关于可实现的相关性范围。

有限可交换 Bernoulli 分布和计数分布的一一对应是明确的已有结果：若 q_s=P(S=s)，则每个含 s 个 1 的格子分配 q_s/binom(K,s)。
注意“有限可交换”不意味着无限可交换；不能擅自引入 beta-binomial 或 iid 混合假设，否则会排除负相关并缩小题目的可行类。

对本项目的作用：对称化降维必须作为已知工具引用。本文使用随机排列证明极值问题无损，不要求实际分类器原本满足更强的可交换假设。

## 7. 直接相关但未取得原文：Boros & Prékopa (1989)

题名：*Closed Form Two-Sided Bounds for Probabilities that At Least r and Exactly r Out of n Events Occur*。
Mathematics of Operations Research 14(2):317–342，DOI [10.1287/moor.14.2.317](https://doi.org/10.1287/moor.14.2.317)。
Crossref 元数据和摘要核对了题名、年份、页码、DOI 及研究范围；本次没有取得这篇原文，所以**没有逐项核对其公式，也不写“已读全文”**。
其主题已经足以说明，离散事件计数的 closed-form sharp bounds 是成熟问题。本文把自己的精确计数界定位成这一经典问题的初等特化，不主张首次解决。
若以后要提交具有文献首创性声明的研究论文，应首先取得该文并逐式对照，再扩大文献检索。

## 8. 原参考表中的 Bahadur (1961) 与 Hoeffding (1963)

这两项在原报告中分别承担高阶二元交互的历史背景与独立和集中不等式的背景。
本轮未取得并阅读两篇原文，故不把它们列为已读论文。
修订后的主线不依赖 Bahadur 展开；独立情形用二项式、递推差值及初等方差界即可解释，不需要借用未核对的具体定理编号。阅读工作优先覆盖与新增证明最相关的上述六篇原文。

## 贡献对照表

| 内容 | 文献状态 / 本项目定位 |
| --- | --- |
| 两两相关性不足以决定多数投票 | 已知现象；用 K=3 精确区间回应题目 |
| 计数降维、二阶矩优化、多项式证书 | 已知方法，明确引用 |
| 任意奇数 K 的尖锐计数界 | 经典离散矩问题的自包含特化，不宣称首创 |
| 三角形扇形分割的初等达到性证明 | 本项目采用的统一解法；不使用一般强对偶 |
| 相邻证书作差 → 常数时间求值 | 本项目具体的简化推导；不宣称此前无人写出 |
| 严格优于 p 的显式有限 K 阈值与三点反例 | 本项目重点推论和解释，与“阈值存在”区分 |
| 连续阈值修正与整数修正的精确分解 | 本项目重点比较，避免不公平地只对比原 C-bound |
| p=0.6、ρ=0 的首个严格收益奇数 K=27 | 具体可复核结论；不能仅凭新数值称为新理论 |

## 建议的阅读顺序

先看 `derivation.md` 的 K=3 退化结果，再看整数二次式与三角形构造，最后看阈值证明。
带着这些式子读 Germain 的 Proposition 13，可以清楚理解“连续界尖锐”与“固定奇数票数的格点界尖锐”为什么不是同一件事。
