import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------------------------
# External logic
# -------------------------------------------------
from preprocessing import preprocess_input
from recommendation_logic import (
    interpret_z_mb,
    diagnostic_zone,
    recommended_action
)

# -------------------------------------------------
# Page configuration
# -------------------------------------------------
st.set_page_config(
    page_title="Mass Balance Diagnostic Dashboard",
    layout="wide"
)

st.title("🔬 Mass Balance Diagnostic Framework")
st.caption(
    "Forced Degradation Studies • Uncertainty-Aware • Regulator-Aligned Decision Support"
)

# -------------------------------------------------
# Sample data option
# -------------------------------------------------
use_sample = st.checkbox("👁️ Preview using sample dataset")

raw_df = None

# -------------------------------------------------
# Safe file reader
# -------------------------------------------------
def load_data(file):
    try:
        if file.name.endswith(".csv"):
            return pd.read_csv(file, encoding="latin1")
        return pd.read_excel(file)
    except Exception as e:
        st.error(f"❌ Failed to read file: {e}")
        return None

# -------------------------------------------------
# Load data (sample OR upload)
# -------------------------------------------------
if use_sample:
    try:
        raw_df = pd.read_csv("sample_data.csv")
        st.success("✅ Sample dataset loaded")
    except Exception as e:
        st.error(f"❌ Failed to load sample data: {e}")
        st.stop()
else:
    uploaded_file = st.file_uploader(
        "📤 Upload Forced Degradation Dataset (CSV / Excel)",
        type=["csv", "xlsx"]
    )

    if uploaded_file is None:
        st.info("Upload a dataset or enable sample data.")
        st.stop()

    raw_df = load_data(uploaded_file)

# -------------------------------------------------
# Validate data
# -------------------------------------------------
if raw_df is None or raw_df.empty:
    st.error("Dataset is empty or unreadable.")
    st.stop()

st.success("✅ Data loaded successfully")

# -------------------------------------------------
# Raw input view
# -------------------------------------------------
st.subheader("📄 Raw Input Data")
st.dataframe(raw_df, use_container_width=True)

# -------------------------------------------------
# Preprocessing
# -------------------------------------------------
try:
    clean_df, issues_df = preprocess_input(raw_df)
except Exception as e:
    st.error(f"❌ Preprocessing failed: {e}")
    st.stop()

st.subheader("🧹 Normalized & Cleaned Data")
st.dataframe(clean_df, use_container_width=True)

# -------------------------------------------------
# Data quality report
# -------------------------------------------------
st.subheader("⚠️ Data Quality Report")

if issues_df.empty:
    st.success("No data quality issues detected.")
else:
    st.warning("Potential data inconsistencies detected")
    st.dataframe(issues_df, use_container_width=True)

# -------------------------------------------------
# Interpretation logic
# -------------------------------------------------
clean_df["Z_MB Interpretation"] = clean_df["Z_MB"].apply(
    lambda z: interpret_z_mb(z)[0]
)

clean_df["Diagnostic Zone"] = clean_df.apply(
    lambda r: diagnostic_zone(r["AMB"], r["RMB"], r["Z_MB"]),
    axis=1
)

clean_df["Recommended Action"] = clean_df["Diagnostic Zone"].apply(
    recommended_action
)

# -------------------------------------------------
# Final results table
# -------------------------------------------------
st.subheader("📊 Final Diagnostic Results")

result_df = clean_df[
    [
        "api_name",
        "api_code",
        "stress_type",
        "time_months",
        "api_assay",
        "total_degradants",
        "AMB",
        "AMBD",
        "RMB",
        "RMBD",
        "Z_MB",
        "Z_MB Interpretation",
        "Diagnostic Zone",
        "Recommended Action"
    ]
].rename(columns={
    "api_name": "API Name",
    "api_code": "API Code",
    "stress_type": "Stress Type",
    "time_months": "Time (Months)",
    "api_assay": "API Assay (%)",
    "total_degradants": "Total Degradants (%)"
})

st.dataframe(result_df, use_container_width=True)

# -------------------------------------------------
# Recommendation Matrix (Explicit)
# -------------------------------------------------
st.subheader("🧭 Recommendation Matrix")

rec_matrix = pd.DataFrame({
    "AMB Range": ["98–102", "<98", "<98", ">102"],
    "RMB Range": ["0.8–1.2", "<0.8", "0.8–1.2", ">1.2"],
    "Diagnostic Interpretation": [
        "Analytically consistent recovery",
        "Missing / non-chromophoric degradants",
        "Physical loss (adsorption / volatility)",
        "Overestimation or response factor mismatch"
    ],
    "Recommended Action": [
        "No action required",
        "Orthogonal testing (LC–MS, CAD/ELSD, alternate column)",
        "Investigate physical loss (vial adsorption, headspace)",
        "Verify RRFs, peak purity, and integration parameters"
    ]
})

st.dataframe(rec_matrix, use_container_width=True)

st.caption(
    "Deterministic, regulator-aligned decision rulebook."
)

# -------------------------------------------------
# Visualizations
# -------------------------------------------------
col1, col2 = st.columns(2)

# AMB vs RMB
with col1:
    st.subheader("AMB–RMB Diagnostic Map")

    fig, ax = plt.subplots(figsize=(6, 5))
    ax.scatter(result_df["RMB"], result_df["AMB"], s=80, edgecolor="black")

    ax.axhline(100, linestyle="--")
    ax.axhline(98, linestyle=":", color="gray")
    ax.axhline(102, linestyle=":", color="gray")
    ax.axvline(0.8, linestyle=":", color="gray")
    ax.axvline(1.2, linestyle=":", color="gray")

    ax.set_xlabel("Relative Mass Balance (RMB)")
    ax.set_ylabel("Absolute Mass Balance (AMB %)")
    ax.set_title("Mass Balance Diagnostic Space")
    ax.grid(True, linestyle="--", alpha=0.4)

    st.pyplot(fig)

# Z_MB Risk
with col2:
    st.subheader("Z_MB Risk Indicator")

    fig2, ax2 = plt.subplots(figsize=(6, 5))
    bars = ax2.bar(result_df.index, result_df["Z_MB"], edgecolor="black")

    for bar, z in zip(bars, result_df["Z_MB"]):
        bar.set_color(
            "#4CAF50" if abs(z) <= 2 else "#FFC107" if abs(z) <= 3 else "#F44336"
        )

    ax2.axhline(2, linestyle="--")
    ax2.axhline(-2, linestyle="--")
    ax2.axhline(3, linestyle=":", color="red")
    ax2.axhline(-3, linestyle=":", color="red")

    ax2.set_ylabel("Z_MB")
    ax2.set_title("Uncertainty-Normalized Risk")
    ax2.grid(axis="y", linestyle="--", alpha=0.4)

    st.pyplot(fig2)

# -------------------------------------------------
# Comparative Analysis
# -------------------------------------------------
st.subheader("⚖️ Comparative Analysis: Traditional vs Proposed")

comparison_df = pd.DataFrame({
    "Criterion": [
        "Analytical variability considered",
        "Root-cause diagnosis",
        "False-positive investigations",
        "Decision consistency",
        "Regulatory defensibility"
    ],
    "Traditional Mass Balance": [
        "No",
        "No",
        "High",
        "Low",
        "Limited"
    ],
    "Proposed Diagnostic Framework": [
        "Yes (Z_MB)",
        "Yes (AMB–RMB zones)",
        "Low",
        "High",
        "Strong (ICH-aligned)"
    ]
})

st.dataframe(comparison_df, use_container_width=True)

false_positive_rate = (
    (result_df["Z_MB"].abs() <= 2).sum() / len(result_df)
) * 100

st.metric(
    label="Results Within Analytical Variability",
    value=f"{false_positive_rate:.1f}%",
    delta="Reduced false-positive investigations"
)

# -------------------------------------------------
# Footer
# -------------------------------------------------
st.markdown("---")
st.caption(
    "Mass Balance Diagnostic Framework • "
    "Uncertainty-aware • Mechanistic • Decision-support oriented"
)