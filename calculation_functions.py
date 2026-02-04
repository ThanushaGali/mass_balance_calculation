import numpy as np

# -------------------------------
# Core Mass Balance Metrics
# -------------------------------

def calculate_amb(api_assay, total_degradants):
    """Absolute / Simple Mass Balance (%)"""
    return api_assay + total_degradants


def calculate_ambd(amb):
    """Absolute Mass Balance Deviation"""
    return abs(amb - 100)


def calculate_rmb(api_assay, total_degradants):
    api_loss = 100 - api_assay
    if api_loss <= 0:
        return float("nan")
    return total_degradants / api_loss


def calculate_rmbd(rmb):
    """Relative Mass Balance Deviation"""
    if np.isnan(rmb):
        return np.nan
    return abs(rmb - 1)


# -------------------------------
# Uncertainty & Z_MB
# -------------------------------

def calculate_combined_uncertainty(assay_rsd, impurity_rsd):
    """Analytical variability (σ)"""
    return np.sqrt(assay_rsd**2 + impurity_rsd**2)


def calculate_z_mb(amb, uncertainty):
    """SIGNED Z_MB"""
    if uncertainty == 0:
        return np.nan
    return (amb - 100) / uncertainty


# -------------------------------
# Stress Severity (contextual)
# -------------------------------

def calculate_stress_severity(temperature_c, time_months, stress_factor=1):
    """
    Stress Severity Index
    (Used ONLY for contextual analysis, not acceptance)
    """
    return temperature_c * time_months * stress_factor