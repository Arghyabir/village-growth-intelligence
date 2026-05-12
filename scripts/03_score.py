"""
03_score.py
===========
Village Economic Growth Intelligence — Scoring & Ranking Script
Kritter Software Technologies Candidate Assignment

Composite Village Growth Index (CVGI):
  Weighted combination of 4 normalised signals:

  Signal                         | Weight | Rationale
  -------------------------------|--------|------------------------------------------
  NTL Growth Rate (%)            |  40%   | Direct proxy for economic activity/lights
  NDVI Absolute Change           |  20%   | Land use intensification (agri or construction)
  PMAY Beneficiaries / 1000 HH   |  20%   | Infrastructure investment
  MGNREGS Days / HH              |  20%   | Rural wage employment

Each signal is Min-Max normalised to [0, 1] before weighting.
Final CVGI ranges 0–100 (scaled for readability).

Run: python scripts/03_score.py
"""

import pandas as pd
import numpy as np
from pathlib import Path

# ─── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR  = Path(__file__).resolve().parent.parent
PROC_DIR  = BASE_DIR / "data" / "processed"
OUT_DIR   = BASE_DIR / "outputs"
OUT_DIR.mkdir(parents=True, exist_ok=True)

INPUT   = PROC_DIR / "cleaned_villages.csv"
OUTPUT  = OUT_DIR / "top_100_villages.csv"
ALL_OUT = PROC_DIR / "all_villages_scored.csv"

# ─── Scoring weights ──────────────────────────────────────────────────────────
WEIGHTS = {
    "ntl_growth_rate":                  0.40,
    "ndvi_delta_abs":                   0.20,
    "pmay_beneficiaries_per_1000hh":    0.20,
    "mgnregs_days_per_hh":              0.20,
}


# ─── Min-Max Normalisation ────────────────────────────────────────────────────

def minmax_normalise(series: pd.Series) -> pd.Series:
    """
    Scale values to [0, 1].
    If all values are identical, returns 0.5 to avoid NaN.
    """
    lo, hi = series.min(), series.max()
    if hi == lo:
        return pd.Series(0.5, index=series.index)
    return (series - lo) / (hi - lo)


# ─── Compute CVGI ─────────────────────────────────────────────────────────────

def compute_cvgi(df: pd.DataFrame) -> pd.DataFrame:
    """
    1. Normalise each signal independently across all villages
    2. Compute weighted sum
    3. Scale to 0–100
    """
    print("[SCORE] Normalising signals ...")
    df = df.copy()

    normalised_cols = []
    for col, weight in WEIGHTS.items():
        norm_col = f"{col}_norm"
        df[norm_col] = minmax_normalise(df[col])
        normalised_cols.append((norm_col, weight))
        print(f"        {col:45s} weight={weight:.0%}  "
              f"range=[{df[col].min():.3f}, {df[col].max():.3f}]")

    print("[SCORE] Computing Composite Village Growth Index (CVGI) ...")
    df["cvgi_raw"] = sum(
        df[norm_col] * weight
        for norm_col, weight in normalised_cols
    )

    # Scale to 0–100
    df["cvgi_score"] = np.round(df["cvgi_raw"] * 100, 2)

    # Rank (1 = highest growth)
    df["rank"] = df["cvgi_score"].rank(ascending=False, method="min").astype(int)

    return df


# ─── Enrich Top 100 ───────────────────────────────────────────────────────────

def enrich_top100(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add human-readable attributes to the top 100 for final output:
      - Growth tier label
      - Dominant growth signal
      - Estimated sector (agricultural / industrial / services)
    """
    df = df.copy()

    # Growth tier
    def tier(score):
        if score >= 80: return "Exceptional"
        if score >= 65: return "Very High"
        if score >= 50: return "High"
        return "Moderate"

    df["growth_tier"] = df["cvgi_score"].apply(tier)

    # Dominant signal: which normalised component contributed most
    norm_cols = [f"{c}_norm" for c in WEIGHTS]
    df["dominant_signal"] = df[norm_cols].idxmax(axis=1).str.replace(
        "_norm", ""
    ).map({
        "ntl_growth_rate":               "Night-time Light",
        "ndvi_delta_abs":                "Land Use Change",
        "pmay_beneficiaries_per_1000hh": "Housing Construction",
        "mgnregs_days_per_hh":           "Rural Employment",
    })

    # Rough sector guess from NTL + NDVI pattern
    def sector(row):
        if row["ndvi_delta"] > 0.05 and row["ntl_growth_rate"] < 50:
            return "Agriculture / Horticulture"
        if row["ntl_growth_rate"] > 80:
            return "Industrial / Commerce"
        if row["pmay_beneficiaries_per_1000hh"] > 150:
            return "Real Estate / Infrastructure"
        return "Mixed / Services"

    df["est_sector"] = df.apply(sector, axis=1)

    return df


# ─── Final output columns ─────────────────────────────────────────────────────

OUTPUT_COLS = [
    "rank",
    "village_id",
    "village_name",
    "state",
    "district",
    "latitude",
    "longitude",
    "population_2011",
    "cvgi_score",
    "growth_tier",
    "dominant_signal",
    "est_sector",
    # Raw signals for transparency
    "ntl_2019",
    "ntl_2024",
    "ntl_growth_rate",
    "ndvi_delta",
    "pmay_beneficiaries_per_1000hh",
    "mgnregs_days_per_hh",
]


# ─── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("  STEP 3: SCORING & RANKING")
    print("  Village Economic Growth Intelligence")
    print("=" * 60)

    df = pd.read_csv(INPUT)
    print(f"[LOAD] {len(df):,} cleaned villages loaded.")

    df = compute_cvgi(df)

    # Save all villages with scores
    df.to_csv(ALL_OUT, index=False)
    print(f"[SAVE] All scored villages → {ALL_OUT}")

    # Extract top 100
    top100 = df[df["rank"] <= 100].copy()
    top100 = enrich_top100(top100)
    top100 = top100.sort_values("rank")[OUTPUT_COLS]
    top100.to_csv(OUTPUT, index=False)

    print(f"[SAVE] Top 100 villages → {OUTPUT}")
    print()
    print("─" * 60)
    print("TOP 10 PREVIEW")
    print("─" * 60)
    preview = top100.head(10)[
        ["rank", "village_name", "state", "cvgi_score",
         "growth_tier", "dominant_signal", "est_sector"]
    ]
    print(preview.to_string(index=False))
    print("─" * 60)

    # Summary stats
    print()
    print("SUMMARY STATISTICS")
    print(f"  Median CVGI (all villages): {df['cvgi_score'].median():.1f}")
    print(f"  Min CVGI (all):             {df['cvgi_score'].min():.1f}")
    print(f"  Max CVGI (all):             {df['cvgi_score'].max():.1f}")
    print(f"  Top 100 score range:        {top100['cvgi_score'].min():.1f} – {top100['cvgi_score'].max():.1f}")
    print()
    print("STATE DISTRIBUTION (Top 100):")
    print(top100["state"].value_counts().to_string())
    print()
    print("SECTOR DISTRIBUTION (Top 100):")
    print(top100["est_sector"].value_counts().to_string())


if __name__ == "__main__":
    main()
