import pandas as pd
import re

# -------------------------------------------------
# Column normalization helpers (FIXED & EXPANDED)
# -------------------------------------------------

COLUMN_ALIASES = {
    "api_name": [
        "api name", "api_name", "api"
    ],
    "api_code": [
        "api code", "api_code"
    ],
    "stress_type": [
        "stress type", "stress_typ", "stress_type", "stress"
    ],
    "time_months": [
        "time", "time_mon", "time_months", "months", "time_month"
    ],
    "api_assay": [
        "api assay",
        "api_assay",
        "api_assay_percent",
        "api assay percent",
        "assay",
        "assay_percent"
    ],
}

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize column names to internal standard names
    """
    col_map = {}

    for col in df.columns:
        clean = col.strip().lower()

        # Match known aliases
        for std, aliases in COLUMN_ALIASES.items():
            if clean in aliases:
                col_map[col] = std
                break

        # Auto-detect degradants
        if "degradant" in clean:
            col_map[col] = clean.replace(" ", "_")

    return df.rename(columns=col_map)


# -------------------------------------------------
# Degradant detection
# -------------------------------------------------

def detect_degradant_columns(df: pd.DataFrame):
    return [c for c in df.columns if c.startswith("degradant_")]


# -------------------------------------------------
# Validation & sanity checks
# -------------------------------------------------

def validate_and_clean(df: pd.DataFrame):
    issues = []

    for idx, row in df.iterrows():
        row_issues = []

        if not (0 <= row["api_assay"] <= 100):
            row_issues.append("API assay out of range")

        if row["total_degradants"] < 0:
            row_issues.append("Negative degradants")

        if row["api_assay"] + row["total_degradants"] < 90:
            row_issues.append("Suspicious mass loss")

        if row_issues:
            issues.append({
                "Row": idx,
                "Issues": ", ".join(row_issues)
            })

    return df, pd.DataFrame(issues)


# -------------------------------------------------
# MAIN PREPROCESSING PIPELINE
# -------------------------------------------------

def preprocess_input(df_raw: pd.DataFrame):
    """
    Dataset-agnostic preprocessing:
    - Normalize column names
    - Auto-detect degradants
    - Compute AMB, RMB, Z_MB
    - Validate consistency
    """

    df = normalize_columns(df_raw)

    # Mandatory fields
    required = {"api_assay", "stress_type", "time_months"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    # Detect degradants
    degradant_cols = detect_degradant_columns(df)
    if not degradant_cols:
        raise ValueError("No degradant columns detected")

    # Force numeric conversion
    numeric_cols = ["api_assay", "time_months"] + degradant_cols
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(how="all").reset_index(drop=True)

    # -----------------------------
    # Core calculations
    # -----------------------------
    df["total_degradants"] = df[degradant_cols].sum(axis=1)

    df["AMB"] = df["api_assay"] + df["total_degradants"]
    df["AMBD"] = df["AMB"] - 100

    df["RMB"] = df.apply(
        lambda r: (
            r["total_degradants"] / (100 - r["api_assay"])
            if (100 - r["api_assay"]) > 0 else None
        ),
        axis=1
    )

    df["RMBD"] = df["RMB"] - 1

    # Fixed combined uncertainty (industry-typical)
    COMBINED_UNCERTAINTY = 2.5
    df["Z_MB"] = (df["AMB"] - 100) / COMBINED_UNCERTAINTY

    # Validation
    df, issues_df = validate_and_clean(df)

    return df, issues_df