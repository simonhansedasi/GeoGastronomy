"""
UTF framework diagram — 6-step pipeline schematic for paper Figure 1.
Saves to ../img/utf_framework.png at 150 dpi.
Run from KushCountry/writing/ or adjust IMG path.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
from pathlib import Path

IMG = Path('../img')
IMG.mkdir(exist_ok=True)

# ── layout ────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(14, 5))
ax.set_xlim(0, 14)
ax.set_ylim(0, 5)
ax.axis('off')

BLUE   = '#2c6fad'
GREEN  = '#3a8c5c'
ORANGE = '#c76b1a'
GRAY   = '#555555'
LIGHT  = '#e8f0f8'

# Step definitions: (x_center, label, sublabel, color)
steps = [
    (1.1,  'Data\nSources',
     'DEM · Sentinel-2 NDVI\nDaymet climate · SoilGrids',
     BLUE),
    (3.2,  'Feature\nAssembly',
     '8,648 hex cells × 23 features\nzonal stats · StandardScaler',
     BLUE),
    (5.3,  'PCA',
     'Dimensionality reduction\nPC1 = coast–interior gradient',
     BLUE),
    (7.4,  'K-Means\nClustering',
     'StandardScaler on PC scores\nK=7 → 7 terrain archetypes',
     GREEN),
    (9.5,  'Within-Zone\nAnalysis',
     'RF regression on NDVI std\nslope dominant (imp. 0.59)',
     GREEN),
    (11.6, 'Validation &\nRobustness',
     'RWQCB enforcement records\nBootstrap ARI · K sensitivity',
     ORANGE),
]

BOX_W, BOX_H = 1.9, 2.6
BOX_Y = 1.2

for x, label, sublabel, color in steps:
    # Box
    rect = mpatches.FancyBboxPatch(
        (x - BOX_W/2, BOX_Y), BOX_W, BOX_H,
        boxstyle='round,pad=0.08',
        facecolor=LIGHT, edgecolor=color, linewidth=1.8
    )
    ax.add_patch(rect)

    # Step label (bold, colored)
    ax.text(x, BOX_Y + BOX_H - 0.28, label,
            ha='center', va='top', fontsize=9.5, fontweight='bold',
            color=color, linespacing=1.3)

    # Sub-label (small, gray)
    ax.text(x, BOX_Y + 0.18, sublabel,
            ha='center', va='bottom', fontsize=7.5, color=GRAY,
            linespacing=1.4)

# Arrows between boxes
for i in range(len(steps) - 1):
    x_start = steps[i][0] + BOX_W/2
    x_end   = steps[i+1][0] - BOX_W/2
    y_mid   = BOX_Y + BOX_H/2
    ax.annotate('',
        xy=(x_end, y_mid), xytext=(x_start, y_mid),
        arrowprops=dict(arrowstyle='->', color='#888888', lw=1.5)
    )

# Phase labels above
ax.text(3.2, 4.15, 'Data Preparation', ha='center', va='bottom',
        fontsize=8.5, color=BLUE, fontstyle='italic')
ax.text(8.45, 4.15, 'UTF Core', ha='center', va='bottom',
        fontsize=8.5, color=GREEN, fontstyle='italic')
ax.text(11.6, 4.15, 'Assessment', ha='center', va='bottom',
        fontsize=8.5, color=ORANGE, fontstyle='italic')

# Phase bracket lines
def bracket(ax, x0, x1, y, color):
    ax.plot([x0, x1], [y, y], color=color, lw=1.2, alpha=0.5)
    for xv in [x0, x1]:
        ax.plot([xv, xv], [y, y - 0.08], color=color, lw=1.2, alpha=0.5)

bracket(ax, 1.1 - BOX_W/2 + 0.05, 5.3 + BOX_W/2 - 0.05, 4.1, BLUE)
bracket(ax, 7.4 - BOX_W/2 + 0.05, 9.5 + BOX_W/2 - 0.05, 4.1, GREEN)
bracket(ax, 11.6 - BOX_W/2 + 0.05, 11.6 + BOX_W/2 - 0.05, 4.1, ORANGE)

# Step numbers
for idx, (x, *_) in enumerate(steps):
    ax.text(x - BOX_W/2 + 0.12, BOX_Y + BOX_H - 0.12,
            f'S{idx+1}', ha='left', va='top',
            fontsize=7, color='#aaaaaa', fontweight='bold')

# Title
ax.text(7.0, 4.75,
        'Unsupervised Terrain Fingerprinting (UTF) — Six-Step Pipeline',
        ha='center', va='center', fontsize=11, fontweight='bold', color='#1a1a1a')

plt.tight_layout(pad=0.3)
out = IMG / 'utf_framework.png'
fig.savefig(out, dpi=150, bbox_inches='tight')
print(f'Saved {out}')
