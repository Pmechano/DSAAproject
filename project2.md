# Project 2: Ensemble Voting Beyond Independence

**Question.** If we combine many individually accurate models, how much can dependence between their errors help or hurt the final prediction?

## Setup

Let $K$ be odd. For a random binary classification example $(X,Y)$, let $f_1,\ldots,f_K$ be fixed classifiers and define

$$
Z_i=\mathbf{1}\{f_i(X)=Y\},\qquad \mathbb{P}(Z_i=1)=p_i.
$$

The ensemble predicts by majority vote, so its accuracy is

$$
A=\mathbb{P}\!\left(\sum_{i=1}^{K}Z_i\geq\frac{K+1}{2}\right).
$$

## Part I: From independence to worst-case dependence

First study the usual independent case. In particular, understand how ensemble accuracy changes with $K$ when all models have the same accuracy $p$.

Then remove the independence assumption completely. Suppose only the marginal accuracies $p_1,\ldots,p_K$ are known.

Define

$$
A_-(p_1,\ldots,p_K)
=\inf\mathbb{P}\!\left(\sum_{i=1}^{K}Z_i\geq\frac{K+1}{2}\right),
$$

where the infimum is over all joint distributions with the specified marginals.

1. Solve the equal-accuracy case $p_1=\cdots=p_K=p$ as sharply as possible. Prove your bound and determine whether it can be attained.
2. Compare the answer with the independent case. Does adding more individually good models necessarily improve the worst-case ensemble?
3. Explore what changes when the $p_i$ are different.

## Part II: Is correlation enough?

A natural measure of diversity is

$$
\rho_{ij}=\operatorname{Corr}(Z_i,Z_j).
$$

Investigate whether knowing all $p_i$ and all pairwise correlations $\rho_{ij}$ is enough to determine majority-vote accuracy.

For the main special case, take

$$
K=3,\qquad p_1=p_2=p_3=p,\qquad \rho_{12}=\rho_{13}=\rho_{23}=\rho.
$$

Determine the smallest and largest majority-vote accuracies compatible with these quantities. More generally, formulate the extremal problem over all joint distributions on $\{0,1\}^{K}$.

**Main insight.** The project should explain clearly what information individual accuracy, independence, pairwise correlation, and the full joint distribution provide about an ensemble.

Small numerical experiments may be used to verify extremal constructions, but the main results should be mathematical.

**Possible extension.** A stronger project may replace simple majority voting by a weighted voting rule and ask how the weights should be chosen when the marginal accuracies are known but the dependence structure is uncertain. It is sufficient to solve a small, well-defined case such as $K=3$ or $K=5$. More general results beyond these settings are also very welcome, and we strongly encourage you to explore broader formulations when possible.
