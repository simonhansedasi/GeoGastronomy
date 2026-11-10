"""Single-page iPoster PDF (36x24 in) from the poster figures. Numbers come from data/matched.json."""
import json, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt, matplotlib.image as mi

m = json.load(open('data/matched.json')); hb = json.load(open('data/headroom_bootstrap.json'))
INK, RED, MUTE = '#1f1f1f', '#c1440e', '#666666'
W, H = 36, 24
fig = plt.figure(figsize=(W, H)); fig.patch.set_facecolor('white')

def place(path, x, y, w):                      # inches from bottom-left; height from aspect
    im = mi.imread(path); h = w * im.shape[0] / im.shape[1]
    ax = fig.add_axes([x/W, y/H, w/W, h/H]); ax.imshow(im); ax.axis('off'); return h

def txt(x, y, s, **k):
    k.setdefault('color', INK); fig.text(x/W, y/H, s, **k)

txt(1.5, 22.3, 'Bounded Ground', fontsize=78, fontweight='bold', va='center')
txt(1.5, 20.9, 'When terrain limits invert climate-only suitability projections', fontsize=40, va='center', color=MUTE)
txt(34.5, 22.3, 'Simon-Hans Edasi', fontsize=34, ha='right', va='center')
txt(34.5, 21.2, 'AGU Fall Meeting 2026  ·  GC002', fontsize=24, ha='right', va='center', color=MUTE)

txt(1.5, 19.1, f"Climate alone says Hawaiian coffee ground holds steady ({m['C_change_pooled_2045']:+.1f}%).\n"
               f"Add the terrain it grows on, and {abs(m['F_change_pooled_2045']):.1f}% disappears at +1.35 \u00b0C.",
    fontsize=34, fontweight='bold', va='center', color=RED, linespacing=1.3)
place('figures/poster/A_filmstrip.png', 0.8, 9.3, 23.0)
txt(12.3, 8.9, 'Coffee-feasible ground on Hawai\u02bbi Island at 0, +1.00 \u00b0C (2035) and +1.35 \u00b0C (2045). Rust = feasible today, lost after warming.',
    fontsize=19, color=MUTE, va='center', ha='center')
_b = mi.imread('figures/poster/B_squeeze.png'); _hB = 10.8 * _b.shape[0] / _b.shape[1]
place('figures/poster/B_squeeze.png', 24.5, 17.4 - _hB, 10.8)
txt(24.8, 18.2, 'Where the loss falls', fontsize=28, fontweight='bold', va='center')
place('figures/poster/C_matched.png', 1.0, 0.4, 9.5)
txt(1.0, 8.3, 'Same statistic, screen off vs on', fontsize=28, fontweight='bold', va='center')

def card(x, w, title, body, fc='#f2f2f2', ec='#999999', tc=INK):
    ax = fig.add_axes([x/W, 0.4/H, w/W, 7.4/H]); ax.axis('off')
    ax.add_patch(plt.Rectangle((0, 0), 1, 1, transform=ax.transAxes, fc=fc, ec=ec, lw=3))
    ax.text(.05, .90, title, fontsize=32, fontweight='bold', color=tc, va='center', transform=ax.transAxes)
    ax.text(.05, .44, body, fontsize=26, color=INK, va='center', linespacing=1.4, transform=ax.transAxes)

card(11.4, 11.6, 'What we did',
     "Feasible ground F(\u0394T) = C(\u0394T) \u2229 S:\na thermal window C that climbs with\nwarming, intersected with terrain S\nthat does not move.\n\n471 coffee farm cells, Kona + Ka\u02bbu\n(indistinguishable, so pooled).\n\nMatched statistic: the same quantity\nwith the terrain screen off vs on.")
card(23.6, 11.7, 'Open question',
     f"Why? +1.35 \u00b0C pushes the window\n~{m['displacement_m_2045']:.0f} m upslope; terrain headroom\nis {m['headroom_m_kona']:.0f} m (Kona), {m['headroom_m_kau']:.0f} m (Ka\u02bbu).\n\nRatios {m['displacement_over_headroom_kona']:.2f} and {m['displacement_over_headroom_kau']:.2f}, but bootstrap\n95% CIs include 1: promising,\nnot proven.\n\nNext: tighten the footprint's\nupper boundary.",
     fc='#f7f1ec', ec=RED, tc=RED)

fig.savefig('figures/poster/AGU26_iPoster.pdf'); fig.savefig('figures/poster/AGU26_iPoster_preview.png', dpi=40)
print('ok')
