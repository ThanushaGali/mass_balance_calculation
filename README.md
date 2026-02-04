# Mass Balance Diagnostic Framework Dashboard

A Streamlit-based decision-support dashboard for **context-driven interpretation of mass balance results** in forced degradation studies.

This tool implements the **Mass Balance Diagnostic Framework** described in the accompanying report by integrating:
- Absolute and relative mass balance metrics
- Analytical uncertainty normalization (Z_MB)
- Diagnostic zone classification
- Structured investigation recommendations

The framework aligns with the intent of **ICH Q1A(R2)** and **ICH Q2(R1)** guidance by supporting risk-based, stability-indicating analytical interpretation.

---

## 🔬 Key Features

- **Automatic calculation of mass balance metrics**
  - Absolute Mass Balance (AMB)
  - Absolute Mass Balance Deviation (AMBD)
  - Relative Mass Balance (RMB)
  - Relative Mass Balance Deviation (RMBD)

- **Uncertainty-adjusted evaluation**
  - Z_MB index normalizes mass balance deviation to analytical variability

- **AMB–RMB diagnostic map**
  - Classifies mass balance behavior into diagnostic zones
  - Differentiates analytical variability, missing degradants, physical loss, and overestimation

- **Recommendation matrix**
  - Provides structured investigation guidance based on diagnostic outcome

- **Interactive visualizations**
  - AMB vs RMB diagnostic space
  - Z_MB risk indicator with uncertainty thresholds

---

## 📂 Input Data Format

The dashboard expects a CSV or Excel file with the following columns:

| Column Name | Description |
|------------|------------|
| Stress Condition | Type of stress (acidic, basic, thermal, etc.) |
| API Assay (%) | Remaining API assay |
| Total Degradants (%) | Sum of detected degradants |
| Assay RSD (%) | Assay method variability |
| Impurity RSD (%) | Impurity method variability |
| Temperature (°C) | Stress temperature |
| Time (Months) | Stress duration |

A sample dataset is provided as `sample_data.csv`.

---

## ▶️ How to Run

```bash
pip install -r requirements.txt
streamlit run app.py