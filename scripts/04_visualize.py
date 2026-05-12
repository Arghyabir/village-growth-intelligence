"""
04_visualize.py
===============
Village Economic Growth Intelligence — Visualization Script
Kritter Software Technologies Candidate Assignment

Produces:
  1. Interactive Folium map  → outputs/village_growth_map.html
  2. Bar chart (Top 20)      → outputs/top20_bar_chart.png
  3. State distribution pie  → outputs/state_distribution.png
  4. Signal scatter plot     → outputs/ntl_vs_ndvi_scatter.png

Run: python scripts/04_visualize.py
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")  # headless rendering
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

# ─── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR  = Path(__file__).resolve().parent.parent
OUT_DIR   = BASE_DIR / "outputs"
PROC_DIR  = BASE_DIR / "data" / "processed"
OUT_DIR.mkdir(parents=True, exist_ok=True)

TOP100_PATH = OUT_DIR / "top_100_villages.csv"
ALL_PATH    = PROC_DIR / "all_villages_scored.csv"

# ─── Color Palette ────────────────────────────────────────────────────────────
COLORS = {
    "exceptional": "#1A535C",
    "very_high":   "#4ECDC4",
    "high":        "#F7B731",
    "moderate":    "#FC5C65",
    "bg":          "#F8F9FA",
    "accent":      "#2C3E50",
}
TIER_COLORS = {
    "Exceptional": COLORS["exceptional"],
    "Very High":   COLORS["very_high"],
    "High":        COLORS["high"],
    "Moderate":    COLORS["moderate"],
}


# ─── 1. Interactive Folium Map ────────────────────────────────────────────────

def make_folium_map(top100: pd.DataFrame, all_df: pd.DataFrame):
    try:
        import folium
        from folium.plugins import MarkerCluster
    except ImportError:
        print("[MAP] folium not installed. Run: pip install folium")
        return

    print("[MAP] Building interactive map ...")

    m = folium.Map(
        location=[22.5, 82.5],
        zoom_start=5,
        tiles="CartoDB positron",
    )

    # Background: all villages as tiny grey dots (sample 5000 for performance)
    sample = all_df.sample(min(5000, len(all_df)), random_state=42)
    for _, row in sample.iterrows():
        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=1,
            color="#CCCCCC",
            fill=True,
            fill_color="#CCCCCC",
            fill_opacity=0.3,
            weight=0,
        ).add_to(m)

    # Top 100 as coloured circles
    for _, row in top100.iterrows():
        tier = row.get("growth_tier", "Moderate")
        color = TIER_COLORS.get(tier, "#999999")
        radius = 4 + (row["cvgi_score"] / 20)  # size by score

        popup_html = f"""
        <div style="font-family:Arial;min-width:200px">
          <b style="font-size:14px">#{int(row['rank'])} {row['village_name']}</b><br>
          <hr style="margin:4px 0">
          <b>State:</b> {row['state']}<br>
          <b>District:</b> {row['district']}<br>
          <b>Population (2011):</b> {int(row['population_2011']):,}<br>
          <b>CVGI Score:</b> <span style="color:{color};font-weight:bold">{row['cvgi_score']:.1f}</span><br>
          <b>Tier:</b> {tier}<br>
          <b>Main Driver:</b> {row.get('dominant_signal','—')}<br>
          <b>Est. Sector:</b> {row.get('est_sector','—')}<br>
          <hr style="margin:4px 0">
          <small>NTL Growth: {row['ntl_growth_rate']:.1f}%</small>
        </div>
        """
        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=radius,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.85,
            weight=1.5,
            popup=folium.Popup(popup_html, max_width=260),
            tooltip=f"#{int(row['rank'])} {row['village_name']} — {row['state']} (Score: {row['cvgi_score']:.1f})",
        ).add_to(m)

    # Legend
    legend_html = """
    <div style="position:fixed;bottom:30px;left:30px;z-index:9999;
                background:white;padding:12px 16px;border-radius:8px;
                box-shadow:0 2px 8px rgba(0,0,0,0.2);font-family:Arial;font-size:12px">
      <b style="font-size:13px">CVGI Growth Tier</b><br>
      <div style="margin-top:6px">
        <span style="background:#1A535C;display:inline-block;width:12px;height:12px;border-radius:50%;margin-right:6px"></span>Exceptional (80+)<br>
        <span style="background:#4ECDC4;display:inline-block;width:12px;height:12px;border-radius:50%;margin-right:6px"></span>Very High (65–80)<br>
        <span style="background:#F7B731;display:inline-block;width:12px;height:12px;border-radius:50%;margin-right:6px"></span>High (50–65)<br>
        <span style="background:#FC5C65;display:inline-block;width:12px;height:12px;border-radius:50%;margin-right:6px"></span>Moderate (&lt;50)<br>
        <span style="background:#CCCCCC;display:inline-block;width:12px;height:12px;border-radius:50%;margin-right:6px"></span>All other villages
      </div>
      <div style="margin-top:6px;color:#666">Circle size ∝ CVGI Score</div>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))

    out_path = OUT_DIR / "village_growth_map.html"
    m.save(str(out_path))
    print(f"[MAP] Saved → {out_path}")


# ─── 2. Bar Chart: Top 20 Villages ────────────────────────────────────────────

def make_bar_chart(top100: pd.DataFrame):
    print("[CHART] Top 20 bar chart ...")
    top20 = top100.head(20).copy()
    top20["label"] = top20.apply(
        lambda r: f"#{int(r['rank'])}  {r['village_name']}\n{r['state']}", axis=1
    )
    colors = [TIER_COLORS.get(t, "#999") for t in top20["growth_tier"]]

    fig, ax = plt.subplots(figsize=(12, 8))
    fig.patch.set_facecolor(COLORS["bg"])
    ax.set_facecolor(COLORS["bg"])

    bars = ax.barh(
        top20["label"][::-1],
        top20["cvgi_score"][::-1],
        color=colors[::-1],
        edgecolor="white",
        linewidth=0.8,
        height=0.7,
    )

    # Value labels
    for bar, score in zip(bars, top20["cvgi_score"][::-1]):
        ax.text(
            bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2,
            f"{score:.1f}", va="center", ha="left", fontsize=9,
            color=COLORS["accent"], fontweight="bold"
        )

    ax.set_xlabel("CVGI Score (0–100)", fontsize=11, color=COLORS["accent"])
    ax.set_title(
        "Top 20 Economically Growing Villages in India\n"
        "Composite Village Growth Index (CVGI) — 2019 to 2024",
        fontsize=14, fontweight="bold", color=COLORS["accent"], pad=14
    )
    ax.set_xlim(0, top20["cvgi_score"].max() * 1.12)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="both", colors=COLORS["accent"], labelsize=8)
    ax.xaxis.grid(True, linestyle="--", alpha=0.4, color="#CCCCCC")
    ax.set_axisbelow(True)

    # Legend
    patches = [
        mpatches.Patch(color=v, label=k)
        for k, v in TIER_COLORS.items()
    ]
    ax.legend(
        handles=patches, loc="lower right", frameon=True,
        framealpha=0.9, fontsize=9, title="Growth Tier",
        title_fontsize=9
    )

    plt.tight_layout()
    out_path = OUT_DIR / "top20_bar_chart.png"
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"[CHART] Saved → {out_path}")


# ─── 3. State Distribution ────────────────────────────────────────────────────

def make_state_chart(top100: pd.DataFrame):
    print("[CHART] State distribution ...")
    state_counts = top100["state"].value_counts()

    # Group states with < 3 into "Others"
    top_states = state_counts[state_counts >= 3]
    others = state_counts[state_counts < 3].sum()
    if others > 0:
        top_states["Others"] = others

    cmap = plt.colormaps.get_cmap("tab20")
    colors_list = [cmap(i / len(top_states)) for i in range(len(top_states))]

    fig, ax = plt.subplots(figsize=(9, 9))
    fig.patch.set_facecolor(COLORS["bg"])

    wedges, texts, autotexts = ax.pie(
        top_states.values,
        labels=top_states.index,
        autopct="%1.0f%%",
        startangle=140,
        colors=colors_list,
        pctdistance=0.78,
        wedgeprops={"linewidth": 1.5, "edgecolor": "white"},
    )
    for t in texts:
        t.set_fontsize(9)
    for at in autotexts:
        at.set_fontsize(8)
        at.set_color("white")
        at.set_fontweight("bold")

    ax.set_title(
        "State-wise Distribution of Top 100 Growing Villages",
        fontsize=13, fontweight="bold", color=COLORS["accent"], pad=14
    )
    plt.tight_layout()
    out_path = OUT_DIR / "state_distribution.png"
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"[CHART] Saved → {out_path}")


# ─── 4. Signal Scatter: NTL Growth vs NDVI Change ────────────────────────────

def make_scatter(top100: pd.DataFrame, all_df: pd.DataFrame):
    print("[CHART] NTL vs NDVI scatter ...")

    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor(COLORS["bg"])
    ax.set_facecolor(COLORS["bg"])

    # All villages (grey background)
    sample = all_df.sample(min(3000, len(all_df)), random_state=1)
    ax.scatter(
        sample["ntl_growth_rate"], sample["ndvi_delta_abs"] if "ndvi_delta_abs" in sample.columns else sample["ndvi_delta"].abs(),
        alpha=0.15, s=6, color="#BBBBBB", label="All villages"
    )

    ndvi_col = "ndvi_delta_abs" if "ndvi_delta_abs" in top100.columns else "ndvi_delta"
    all_ndvi_col = "ndvi_delta_abs" if "ndvi_delta_abs" in all_df.columns else "ndvi_delta"

    # Top 100 coloured by tier
    for tier, color in TIER_COLORS.items():
        subset = top100[top100["growth_tier"] == tier]
        ax.scatter(
            subset["ntl_growth_rate"], subset[ndvi_col].abs(),
            alpha=0.85, s=60, color=color, edgecolors="white",
            linewidths=0.6, label=tier, zorder=5
        )

    ax.set_xlabel("NTL Growth Rate (%) — 2019 to 2024",
                  fontsize=11, color=COLORS["accent"])
    ax.set_ylabel("NDVI Absolute Change",
                  fontsize=11, color=COLORS["accent"])
    ax.set_title(
        "Night-time Light Growth vs. Land Use Change\n"
        "Top 100 villages highlighted by CVGI Tier",
        fontsize=13, fontweight="bold", color=COLORS["accent"]
    )
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(colors=COLORS["accent"])
    ax.legend(fontsize=9, framealpha=0.9)
    ax.xaxis.grid(True, linestyle="--", alpha=0.3, color="#CCCCCC")
    ax.yaxis.grid(True, linestyle="--", alpha=0.3, color="#CCCCCC")
    ax.set_axisbelow(True)

    plt.tight_layout()
    out_path = OUT_DIR / "ntl_vs_ndvi_scatter.png"
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"[CHART] Saved → {out_path}")


# ─── 5. CVGI Score Distribution ───────────────────────────────────────────────

def make_score_distribution(all_df: pd.DataFrame, top100: pd.DataFrame):
    print("[CHART] CVGI score distribution ...")

    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor(COLORS["bg"])
    ax.set_facecolor(COLORS["bg"])

    ax.hist(
        all_df["cvgi_score"], bins=80, color="#4ECDC4",
        alpha=0.6, edgecolor="white", linewidth=0.3,
        label="All villages"
    )

    threshold = top100["cvgi_score"].min()
    ax.axvline(
        threshold, color=COLORS["exceptional"], linestyle="--",
        linewidth=2, label=f"Top 100 threshold ({threshold:.1f})"
    )

    # Shade top 100 region
    ax.axvspan(threshold, all_df["cvgi_score"].max(), alpha=0.12,
               color=COLORS["exceptional"], label="Top 100 zone")

    ax.set_xlabel("CVGI Score", fontsize=11, color=COLORS["accent"])
    ax.set_ylabel("Number of Villages", fontsize=11, color=COLORS["accent"])
    ax.set_title(
        "Distribution of CVGI Scores Across All Villages",
        fontsize=13, fontweight="bold", color=COLORS["accent"]
    )
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(fontsize=9)
    ax.tick_params(colors=COLORS["accent"])
    ax.yaxis.grid(True, linestyle="--", alpha=0.3, color="#CCCCCC")
    ax.set_axisbelow(True)

    plt.tight_layout()
    out_path = OUT_DIR / "score_distribution.png"
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"[CHART] Saved → {out_path}")


# ─── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("  STEP 4: VISUALIZATION")
    print("  Village Economic Growth Intelligence")
    print("=" * 60)

    top100 = pd.read_csv(TOP100_PATH)
    all_df = pd.read_csv(ALL_PATH)

    make_bar_chart(top100)
    make_state_chart(top100)
    make_scatter(top100, all_df)
    make_score_distribution(all_df, top100)
    make_folium_map(top100, all_df)

    print("\n[DONE] All visualizations saved to", OUT_DIR)


if __name__ == "__main__":
    main()
