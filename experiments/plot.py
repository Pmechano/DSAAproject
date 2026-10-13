"""Generate publication figures from the exact formulas; no Monte Carlo fits."""
import os
os.environ.setdefault("MPLCONFIGDIR", "/tmp/dsaa-matplotlib")
os.environ.setdefault("XDG_CACHE_HOME", "/tmp/dsaa-cache")
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from verify import interval, threshold

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures"
FIG.mkdir(exist_ok=True)
plt.rcParams.update({"font.size": 9, "axes.spines.top": False,
                     "axes.spines.right": False, "pdf.fonttype": 42})

fig, axes = plt.subplots(1, 2, figsize=(6.6, 2.35), layout="constrained")
p, k = .6, 7
m, mu = k // 2, k * p
a = int(mu)
min_nu = 2 * a * mu - a * (a + 1)
rho_min = (min_nu / (k * (k - 1)) - p*p) / (p*(1-p))
rhos = np.linspace(rho_min, 1, 450)
lo, hi = np.array([interval(k, p, r) for r in rhos]).T
var = k*p*(1-p)*(1+(k-1)*rhos)
shifted = (mu-m)**2 / ((mu-m)**2+var)
cb = (2*p-1)**2 / ((2*p-1)**2 + 4*var/k**2)
axes[0].fill_between(rhos, lo, hi, color="#cbdcf0", label="Attainable interval")
axes[0].plot(rhos, lo, color="#194d85", label="Exact lower")
axes[0].plot(rhos, shifted, "--", color="#c57124", label="Shifted Cantelli")
axes[0].plot(rhos, cb, ":", color="#548b55", label="C-bound")
axes[0].axhline(p, color="black", linewidth=.7)
axes[0].axvline(threshold(k,p)[0], color="black", linewidth=.7, linestyle="--")
axes[0].set(xlabel=r"Pairwise correlation $\rho$", ylabel="Accuracy",
            title=r"$K=7,\ p=0.6$", ylim=(0,1.04))
axes[0].legend(fontsize=6.8, loc="upper right")
ks = np.arange(3, 102, 2)
exact = [threshold(int(k), p)[0] for k in ks]
shifted_t = ((ks*p-(ks-1)/2)**2/(ks*p*p)-1)/(ks-1)
cb_t = (ks*(2*p-1)**2/(4*p*p)-1)/(ks-1)
axes[1].plot(ks, exact, color="#194d85", label=r"Exact $\rho_*$")
axes[1].plot(ks, shifted_t, "--", color="#c57124", label="Shifted Cantelli")
axes[1].plot(ks, cb_t, ":", color="#548b55", label="C-bound")
axes[1].axhline(0, color="black", linewidth=.7)
axes[1].axhline((1-1/(2*p))**2, color="gray", linewidth=.7, linestyle="--")
axes[1].set(xlabel="Odd ensemble size K", ylabel="Critical correlation",
            title=r"Guarantee $A>0.6$ below the curve", ylim=(-.2,.04))
axes[1].legend(fontsize=7, loc="lower right")
fig.savefig(FIG / "bounds.pdf")
fig.savefig(FIG / "bounds.png", dpi=170)
plt.close(fig)

fig, ax = plt.subplots(figsize=(4.6, 2.4), layout="constrained")
k,m = 7,3
s=np.arange(k+1)
v=np.column_stack([s,s*(s-1)])
ax.fill(v[[0,m,k],0],v[[0,m,k],1],color="#e8c797",alpha=.8)
for j in range(m+1,k):
    ids=[m,j,j+1]
    ax.fill(v[ids,0],v[ids,1],color="#cbdcf0",alpha=.8,edgecolor="white")
ax.fill(v[:m+1,0],v[:m+1,1],color="#cce3cc",alpha=.8)
ax.plot(np.r_[s,0],np.r_[s*(s-1),0],color="#333333",linewidth=1)
ax.scatter(v[:,0],v[:,1],s=16,color="#333333")
for i in range(k+1):ax.annotate(str(i),v[i],xytext=(3,-10),textcoords="offset points",fontsize=8)
ax.set(xlabel=r"$\mu=\mathbb{E}S$",ylabel=r"$\nu=\mathbb{E}S(S-1)$",
       title="Moment polygon and attaining supports (K=7)")
fig.savefig(FIG/"moment_polygon.pdf")
fig.savefig(FIG/"moment_polygon.png",dpi=170)
plt.close(fig)
print("Generated bounds and moment polygon figures.")
