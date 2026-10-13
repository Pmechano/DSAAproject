"""Reproduce the report: sharp integer-moment bounds, witnesses, and LP checks.

Run from the repository root: python experiments/verify.py
The LP implementations do not use the analytic formula as a constraint.
"""
from __future__ import annotations

import csv
import itertools
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parents[1]
TOL = 2e-8


def certificates(k):
    """Coefficients of 1, s, s(s-1), for odd k >= 3."""
    if k < 3 or k % 2 != 1:
        raise ValueError("k must be odd and at least 3")
    m = k // 2
    d = k * (k - m)
    out = [("zero", np.array([0., 0., 0.])),
           ("bridge", np.array([0., -(m - 1) / d, 1 / d]))]
    for j in range(m + 1, k):
        d = (j - m) * (j + 1 - m)
        out.append((f"adjacent_{j}",
                    np.array([1 - j * (j + 1) / d, 2 * j / d, -1 / d])))
    return out


def feasible(k, mu, nu):
    a = min(k, max(0, math.floor(mu)))
    return (-TOL <= mu <= k + TOL and
            2 * a * mu - a * (a + 1) - TOL <= nu <= (k - 1) * mu + TOL)


def lower_by_certificates(k, mu, nu):
    if not feasible(k, mu, nu):
        raise ValueError("infeasible count moments")
    moments = np.array([1., mu, nu])
    return max(float(c @ moments) for _, c in certificates(k))


def lower(k, mu, nu):
    """Constant-time evaluation; independent of the certificate enumeration."""
    if k < 3 or k % 2 != 1 or not feasible(k, mu, nu):
        raise ValueError("invalid k or infeasible count moments")
    m = k // 2
    bridge = (nu - (m - 1) * mu) / (k * (k - m))
    d = mu - m
    if d <= 0:
        return max(0., bridge)
    v = nu - (2 * m - 1) * mu + m * m
    a = max(1, min(m, math.floor(v / d)))
    adjacent = ((2 * a + 1) * d - v) / (a * (a + 1))
    return max(0., bridge, adjacent)


def interval(k, p, rho):
    r = p * p + rho * p * (1 - p)
    mu, nu = k * p, k * (k - 1) * r
    return (lower(k, mu, nu),
            1 - lower(k, k - mu, k * (k - 1) - 2 * (k - 1) * mu + nu))


def witness(k, mu, nu):
    """Find barycentric weights in the explicit fan triangulation, no LP."""
    m = k // 2
    supports = [(0, m, k)]
    supports += [(m, j, j + 1) for j in range(m + 1, k)]
    supports += [(0, j, j + 1) for j in range(1, m)]
    target = np.array([1., mu / k, nu / (k * (k - 1))])
    bound = lower(k, mu, nu)
    for support in supports:
        s = np.array(support, dtype=float)
        matrix = np.array([np.ones(3), s / k, s * (s - 1) / (k * (k - 1))])
        q = np.linalg.solve(matrix, target)
        if q.min() >= -TOL and abs(q @ (s > m) - bound) < TOL:
            result = np.zeros(k + 1)
            result[list(support)] = q
            return result
    raise AssertionError(f"No fan witness for {(k, mu, nu)}")


def count_lp(k, mu, nu, maximize=False):
    s = np.arange(k + 1, dtype=float)
    objective = (s > k // 2).astype(float)
    sign = -1 if maximize else 1
    result = linprog(sign * objective,
                     A_eq=[np.ones(k + 1), s / k, s * (s - 1) / (k * (k - 1))],
                     b_eq=[1, mu / k, nu / (k * (k - 1))],
                     bounds=(0, None), method="highs")
    if not result.success:
        raise AssertionError(result.message)
    return sign * result.fun


def binary_lp(k, p, r, maximize=False):
    z = np.array(list(itertools.product([0., 1.], repeat=k)))
    pairs = [z[:, i] * z[:, j] for i, j in itertools.combinations(range(k), 2)]
    matrix = np.vstack([np.ones(2 ** k), z.T, *pairs])
    rhs = np.array([1.] + [p] * k + [r] * len(pairs))
    objective = (z.sum(axis=1) > k // 2).astype(float)
    sign = -1 if maximize else 1
    result = linprog(sign * objective, A_eq=matrix, b_eq=rhs,
                     bounds=(0, None), method="highs")
    if not result.success:
        raise AssertionError(result.message)
    return sign * result.fun


def threshold(k, p):
    if not 0.5 < p < 1:
        raise ValueError("strict benefit threshold requires 1/2 < p < 1")
    m = k // 2
    x = (k * p - (1 - p) * m) / p
    j = min(k - 1, math.floor(x))
    nu = (1 - p) * m * (m - 1) + p * (2 * j * x - j * (j + 1))
    rho = (nu / (k * (k - 1)) - p * p) / (p * (1 - p))
    q = np.zeros(k + 1)
    q[m], q[j], q[j + 1] = 1 - p, p * (j + 1 - x), p * (x - j)
    return rho, nu, q


def check_close(a, b, label):
    if abs(a - b) > TOL:
        raise AssertionError(f"{label}: {a} != {b}")


def verify():
    rng = np.random.default_rng(20261013)
    counts = dict(certificate_values=0, count_lp_cases=0, binary_lp_cases=0,
                  threshold_cases=0, rejected_infeasible=0)
    max_gap = 0.
    for k in [3, 5, 7, 9, 11, 15, 21, 31, 51]:
        s = np.arange(k + 1, dtype=float)
        moment_matrix = np.array([np.ones(k + 1), s, s * (s - 1)])
        for name, c in certificates(k):
            assert np.max(c @ moment_matrix - (s > k // 2)) < TOL, (k, name)
            counts["certificate_values"] += k + 1
        laws = list(np.eye(k + 1))
        laws += [rng.dirichlet(np.full(k + 1, .3)) for _ in range(35)]
        for _ in range(25):
            q = np.zeros(k + 1)
            q[rng.choice(k + 1, size=3, replace=False)] = rng.dirichlet(np.ones(3))
            laws.append(q)
        for n, law in enumerate(laws):
            mu, nu = law @ s, law @ (s * (s - 1))
            lo = lower(k, mu, nu)
            check_close(lo, lower_by_certificates(k, mu, nu), "constant-time evaluation")
            hi = 1 - lower(k, k - mu, k * (k - 1) - 2 * (k - 1) * mu + nu)
            lo_lp, hi_lp = count_lp(k, mu, nu), count_lp(k, mu, nu, True)
            check_close(lo, lo_lp, "lower count LP")
            check_close(hi, hi_lp, "upper count LP")
            max_gap = max(max_gap, abs(lo - lo_lp), abs(hi - hi_lp))
            q = witness(k, mu, nu)
            assert q.min() >= -TOL
            assert np.max(np.abs(moment_matrix @ q - [1, mu, nu])) < TOL
            check_close(q @ (s > k // 2), lo, "witness accuracy")
            counts["count_lp_cases"] += 1
            if k <= 7 and n % 5 == 0:
                p, r = mu / k, nu / (k * (k - 1))
                check_close(binary_lp(k, p, r), lo, "lower binary LP")
                check_close(binary_lp(k, p, r, True), hi, "upper binary LP")
                counts["binary_lp_cases"] += 1
            if k == 3:
                p, r = mu / 3, nu / 6
                check_close(lo, 3 * r - 2 * min(r, 1 - 3 * p + 3 * r), "K=3 lower")
                check_close(hi, 3 * r - 2 * max(0, 2 * r - p), "K=3 upper")
        for mu, nu in [(-1, 0), (k + 1, 0), (k / 2, -1), (k / 2, k * k)]:
            try:
                lower(k, mu, nu)
            except ValueError:
                counts["rejected_infeasible"] += 1
            else:
                raise AssertionError("Accepted infeasible moments")
        ps = list(np.linspace(.501, .999, 70)) + [.6, .75, .9]
        # x an integer: p=m/(K+m-x), so the two adjacent cells coalesce.
        ps += [k // 2 / (k + k // 2 - x) for x in range(k // 2 + 2, k)]
        for p in ps:
            rho, nu, q = threshold(k, p)
            check_close(q.sum(), 1, "threshold normalization")
            assert q.min() >= -TOL
            check_close(q @ s, k * p, "threshold mean")
            check_close(q @ (s * (s - 1)), nu, "threshold second moment")
            check_close(q @ (s > k // 2), p, "threshold accuracy")
            check_close(lower(k, k * p, nu), p, "threshold sharpness")
            # Check the strict lower side by the LP, not just the same formula.
            a = math.floor(k * p)
            nu_min = 2 * a * k * p - a * (a + 1)
            delta = min(1e-3, (nu - nu_min) / 2)
            assert delta > 0
            assert count_lp(k, k * p, nu - delta) > p + 1e-10
            # The midpoint mixture proves failure of strict benefit above threshold.
            comonotone = np.zeros(k + 1)
            comonotone[0], comonotone[k] = 1 - p, p
            mix = (q + comonotone) / 2
            check_close(mix @ (s > k // 2), p, "above-threshold counterexample")
            assert lower(k, k * p, mix @ (s * (s - 1))) <= p + TOL
            if k == 3:
                check_close(rho, 1 - 2 / (3 * p), "K=3 threshold")
            counts["threshold_cases"] += 1
    counts["max_absolute_lp_gap"] = max_gap
    counts["seed"] = 20261013
    return counts


def outputs(summary):
    (ROOT / "results").mkdir(exist_ok=True)
    (ROOT / "results/verification.json").write_text(json.dumps(summary, indent=2) + "\n")
    rows = []
    for k in [3, 5, 7, 11, 21, 23, 25, 27, 31, 51, 101]:
        p = .6
        lo, hi = interval(k, p, 0.)
        rho, _, _ = threshold(k, p)
        independent = sum(math.comb(k, s) * p ** s * (1 - p) ** (k - s)
                          for s in range(k // 2 + 1, k + 1))
        rows.append(dict(K=k, p=p, rho=0, exact_lower=lo, exact_upper=hi,
                         independent=independent, c_bound=k / (k + 24),
                         shifted_cantelli=(k*p-k//2)**2/((k*p-k//2)**2+k*p*(1-p)),
                         critical_rho=rho))
    with (ROOT / "results/comparison.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    selected = {3, 5, 7, 23, 25, 27, 31}
    table = []
    for row in rows:
        if row['K'] in selected:
            values = [row[key] for key in ['exact_lower', 'exact_upper', 'independent',
                                           'c_bound', 'shifted_cantelli']]
            table.append(str(row['K']) + ' & ' + ' & '.join(f'{x:.6f}' for x in values) + ' ' + chr(92) * 2)
    bs = chr(92)
    table = [bs + 'begin{tabular}{@{}rrrrrr@{}}', bs + 'toprule',
             '$K$ & Exact min & Exact max & Independent & C-bound & Shifted Cantelli' +
             bs * 2 + bs + 'midrule'] + table + [bs + 'bottomrule', bs + 'end{tabular}']
    (ROOT / 'results/comparison_table.tex').write_text('\n'.join(table) + '\n')
    print(json.dumps(summary, indent=2))
    for row in rows:
        print(f"K={row['K']:3d}: [{row['exact_lower']:.6f}, {row['exact_upper']:.6f}], "
              f"rho*={row['critical_rho']:.6f}")


if __name__ == "__main__":
    outputs(verify())
