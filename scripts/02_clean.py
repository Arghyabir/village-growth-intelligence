"""
02_clean.py
===========
Village Economic Growth Intelligence — Cleaning & Processing Script
Kritter Software Technologies Candidate Assignment

This script:
  1. Loads the master extract from Step 1
  2. Removes duplicates, handles missing values
  3. Filters out urban/peri-urban villages (population > 50,000 excluded)
  4. Computes derived features: NTL growth rate, absolute NTL change, etc.
  5. Saves cleaned dataset ready for scoring

Run: python scripts/02_clean.py
"""

import pandas as pd
import numpy as np
from pathlib import Path

# ─── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR  = Path(__file__).resolve().parent.parent
PROC_DIR  = BASE_DIR / "data" / "processed"

INPUT     = PROC_DIR / "master_extract.csv"
OUTPUT    = PROC_DIR / "cleaned_villages.csv"


# ─── 1. Load ──────────────────────────────────────────────────────────────────

def load_data(path: Path) -> pd.DataFrame:
    print(f"[LOAD] Reading {path} ...")
    df = pd.read_csv(path)
    print(f"       {len(df):,} rows × {len(df.columns)} columns")
    return df


# ─── 2. Deduplication ─────────────────────────────────────────────────────────

def deduplicate(df: pd.DataFrame) -> pd.DataFrame:
    before = len(df)
    df = df.drop_duplicates(subset=["village_id"])
    after = len(df)
    removed = before - after
    print(f"[DEDUP] Removed {removed} duplicate village_id rows. ({after:,} remain)")
    return df


# ─── 3. Filter: exclude peri-urban & very small hamlets ──────────────────────

def filter_villages(df: pd.DataFrame) -> pd.DataFrame:
    """
    Exclusion rules:
      - Population < 100  → too small for reliable signal
      - Population > 50,000 → likely a town/urban cluster, not a village
    These thresholds are based on Census 2011 'Census Village' definition.
    """
    before = len(df)
    df = df[
        (df["population_2011"] >= 100) &
        (df["population_2011"] <= 50_000)
    ].copy()
    after = len(df)
    print(f"[FILTER] Population filter removed {before - after:,} rows. "
          f"({after:,} remain)")
    return df


# ─── 4. Missing value handling ────────────────────────────────────────────────

def handle_missing(df: pd.DataFrame) -> pd.DataFrame:
    """
    Strategy:
      - NTL values: forward-fill not applicable here; impute with state median
      - PMAY / MGNREGS: impute with state median (administrative schemes)
      - NDVI: impute with 0 (no change — conservative assumption)
    """
    print("[MISSING] Checking for nulls ...")
    null_counts = df.isnull().sum()
    if null_counts.sum() == 0:
        print("          No missing values found.")
        return df

    for col in ["ntl_2019", "ntl_2024"]:
        if df[col].isnull().any():
            state_medians = df.groupby("state")[col].transform("median")
            df[col] = df[col].fillna(state_medians)
            print(f"          {col}: imputed {null_counts[col]} values with state median")

    for col in ["pmay_beneficiaries_per_1000hh", "mgnregs_days_per_hh"]:
        if df[col].isnull().any():
            state_medians = df.groupby("state")[col].transform("median")
            df[col] = df[col].fillna(state_medians)
            print(f"          {col}: imputed with state median")

    for col in ["ndvi_delta", "ndvi_delta_abs"]:
        if df[col].isnull().any():
            df[col] = df[col].fillna(0.0)
            print(f"          {col}: imputed with 0.0")

    return df


# ─── 5. Derived features ──────────────────────────────────────────────────────

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Derived columns used in scoring:

      ntl_absolute_change : raw radiance increase (nW/cm²/sr)
      ntl_growth_rate     : % growth in NTL (avoids scale bias)
      ntl_log_ratio       : log(NTL_2024 / NTL_2019) — symmetric growth measure
      pmay_norm_pop       : PMAY density normalised by population
    """
    print("[FEATURES] Engineering derived features ...")
    df = df.copy()

    # Avoid division by zero: floor NTL at 0.001
    df["ntl_2019_safe"] = df["ntl_2019"].clip(lower=0.001)
    df["ntl_2024_safe"] = df["ntl_2024"].clip(lower=0.001)

    df["ntl_absolute_change"] = df["ntl_2024_safe"] - df["ntl_2019_safe"]
    df["ntl_growth_rate"]     = (
        (df["ntl_2024_safe"] - df["ntl_2019_safe"]) / df["ntl_2019_safe"]
    ) * 100.0
    df["ntl_log_ratio"] = np.log(df["ntl_2024_safe"] / df["ntl_2019_safe"])

    # Cap extreme outliers at 99th percentile (NTL growth)
    cap_growth = df["ntl_growth_rate"].quantile(0.99)
    cap_abs    = df["ntl_absolute_change"].quantile(0.99)
    df["ntl_growth_rate"]     = df["ntl_growth_rate"].clip(upper=cap_growth)
    df["ntl_absolute_change"] = df["ntl_absolute_change"].clip(upper=cap_abs)

    df["pmay_norm_pop"] = (
        df["pmay_beneficiaries_per_1000hh"] / df["population_2011"] * 1000
    )

    # Drop safe intermediate columns
    df.drop(columns=["ntl_2019_safe", "ntl_2024_safe"], inplace=True)

    print(f"          Added: ntl_absolute_change, ntl_growth_rate, "
          f"ntl_log_ratio, pmay_norm_pop")
    return df


# ─── 6. Outlier capping (Winsorization) ───────────────────────────────────────

def winsorise(df: pd.DataFrame, cols: list, lower=0.01, upper=0.99) -> pd.DataFrame:
    """
    Cap extreme values at specified quantile bounds to reduce noise from
    data errors or exceptional single-year events (e.g. industrial setup).
    """
    print(f"[WINSORISE] Capping outliers at [{lower*100:.0f}%, {upper*100:.0f}%] ...")
    df = df.copy()
    for col in cols:
        lo = df[col].quantile(lower)
        hi = df[col].quantile(upper)
        df[col] = df[col].clip(lower=lo, upper=hi)
    return df


# ─── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("  STEP 2: DATA CLEANING & PROCESSING")
    print("  Village Economic Growth Intelligence")
    print("=" * 60)

    df = load_data(INPUT)
    df = deduplicate(df)
    df = filter_villages(df)
    df = handle_missing(df)
    df = engineer_features(df)

    winsorise_cols = [
        "ntl_growth_rate", "ntl_absolute_change", "ntl_log_ratio",
        "pmay_beneficiaries_per_1000hh", "mgnregs_days_per_hh",
        "ndvi_delta_abs"
    ]
    df = winsorise(df, winsorise_cols)

    df.to_csv(OUTPUT, index=False)
    print(f"\n[DONE] Cleaned dataset saved → {OUTPUT}")
    print(f"       Final rows: {len(df):,}")
    print(f"       Columns: {list(df.columns)}")


if __name__ == "__main__":
    main()
