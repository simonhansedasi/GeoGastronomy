"""Poster figures: static, image-first. Reuses pipeline.py; no new statistics."""
import warnings; warnings.filterwarnings('ignore')
import numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt, matplotlib.patches as mp
from matplotlib.colors import ListedColormap, BoundaryNorm
import pipeline as P

OUT = 'figures/poster'
import os; os.makedirs(OUT, exist_ok=True)
GRAY, RED, GREEN, NOTF = '#cfcfcf', '#c1440e', '#7fb069', '#f2f2f2'
plt.rcParams.update({'font.size': 15, 'axes.spines.top': False, 'axes.spines.right': False})

isl = P.load_island(); FT, FTemp, reg, xy = P.load_farms(isl)
idx = np.arange(len(FT)); s = P.screen(FT, reg, isl['X'], idx)
rr, cc = np.where(isl['land'])
r0, r1, c0, c1 = max(0, rr.min()-3), rr.max()+4, max(0, cc.min()-3), cc.max()+4
flatpos = np.where(isl['land'].ravel())[0]
_, u0 = P.pooled_union(isl, FT, FTemp, reg, dt=0.0)

def grid(code):
    g = np.full(isl['land'].shape, np.nan); g.ravel()[flatpos] = code
    return g[r0:r1, c0:c1]

# A: filmstrip -- same island, same colour key, three warming levels
fig, axes = plt.subplots(1, 3, figsize=(15, 6))
cm = ListedColormap([NOTF, GRAY, GREEN, RED])
for ax, dt in zip(axes, (0.0, 1.0, 1.35)):
    n, u = P.pooled_union(isl, FT, FTemp, reg, dt=dt)
    code = np.full(len(isl['X']), 0.5); code[isl['farmable']] = 1.5
    code[u] = 2.5; code[u0 & ~u] = 3.5
    ax.imshow(grid(code), cmap=cm, norm=BoundaryNorm([0, 1, 2, 3, 4], 4), interpolation='nearest')
    ax.set_axis_off()
    ax.set_title(f'+{dt:.2f} °C' if dt else 'today', fontsize=22, pad=6)
    ax.text(0.5, -0.04, f'{100*n/u0.sum():.0f}% of coffee ground', transform=ax.transAxes,
            ha='center', va='top', fontsize=17)
axes[0].legend(handles=[mp.Patch(color=GREEN, label='feasible'), mp.Patch(color=RED, label='lost'),
                        mp.Patch(color=GRAY, label='farmable, not feasible'),
                        mp.Patch(color=NOTF, label='not farmable')],
               frameon=False, fontsize=12, loc='upper left', bbox_to_anchor=(0.55, 0.2))
fig.tight_layout(); fig.savefig(f'{OUT}/A_filmstrip.png', dpi=200, bbox_inches='tight'); plt.close(fig)

# B: the squeeze -- real feasible sets by elevation: retained / lost / gained at +1.35 C
z = isl['X'][:, 0]
belt = isl['farmable'] & (s['kona_like'] | s['kau_like'])
_, u45 = P.pooled_union(isl, FT, FTemp, reg, dt=P.DT_HORIZON['2045'])
bins = np.arange(0, np.nanmax(z[belt])+50, 50)
parts = [('feasible today and at +1.35 °C', u0 & u45, GREEN), ('lost', u0 & ~u45, RED),
         ('gained', ~u0 & u45, '#4a8aa0'), ('terrain only, never in the window', belt & ~u0 & ~u45, GRAY)]
fig, ax = plt.subplots(figsize=(10, 6.5)); left = np.zeros(len(bins)-1)
for lbl, m, col in parts:
    h, _ = np.histogram(z[m], bins); ax.barh(bins[:-1]+25, h, 46, left=left, color=col, label=lbl); left += h
ztop = np.percentile(z[belt], 97.5); ax.axhline(ztop, color='k', lw=1.5, ls='--')
ax.text(left.max()*.98, ztop+10, 'terrain ceiling (97.5th pct.)', ha='right', va='bottom', fontsize=15)
ax.set_ylabel('elevation (m)'); ax.set_xlabel('coffee-capable terrain (500 m cells per 50 m of elevation)')
ax.set_xlim(0, 480); ax.legend(frameon=False, fontsize=13, loc='lower right')
fig.tight_layout(); fig.savefig(f'{OUT}/B_squeeze.png', dpi=200); plt.close(fig)

# C: matched curve -- one axis, both indexed to ΔT=0
def pooled_C(dt):
    u = np.zeros(len(isl['X']), bool)
    for r in ('kona', 'kau'):
        mu, sg = P.envelope(FTemp, reg, idx, r)
        u |= isl['farmable'] & (np.abs(isl['T']+dt-mu) <= P.HW*sg)
    return u.sum()
dts = np.linspace(0, 1.5, 16)
C = np.array([pooled_C(d) for d in dts]); F = np.array([P.pooled_union(isl, FT, FTemp, reg, dt=d)[0] for d in dts])
fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(dts, 100*C/C[0], color='#555555', lw=2.5); ax.plot(dts, 100*F/F[0], color=RED, lw=2.5)
ax.axvspan(1.0, 1.35, color=RED, alpha=.08, lw=0)
ax.text(0.05, 103, 'climate only', color='#333333', ha='left', fontsize=17)
ax.text(0.05, 87, 'climate ∩ terrain', color=RED, ha='left', va='top', fontsize=17, rotation=-14)
import json; m = json.load(open('data/matched.json'))
for key, y0, col in (('C_change_pooled_2045', 100, '#555555'), ('F_change_pooled_2045', 100, RED)):
    v = 100 + m[key]; ax.plot([1.35], [v], 'o', color=col, ms=9)
    ax.text(1.39, v + (4 if 'C_' in key else 0), f'{m[key]:+.1f}%', color=col, fontsize=18, fontweight='bold', va='center')
ax.text(1.175, 108, '2035-2045', ha='center', fontsize=13, color='#555555')
ax.set_ylim(60, 110); ax.set_xlim(-0.03, 1.62); ax.set_xlabel('warming (°C)'); ax.set_ylabel('coffee ground (% of today)')
fig.tight_layout(); fig.savefig(f'{OUT}/C_matched.png', dpi=200); plt.close(fig)
print('C@1.35:', np.interp(1.35, dts, 100*C/C[0]), 'F@1.35:', np.interp(1.35, dts, 100*F/F[0]))
