def interpret_z_mb(z_mb):
    if z_mb is None:
        return "Invalid Z_MB", "Check uncertainty inputs"

    if abs(z_mb) <= 2:
        return "Within analytical variability", "Acceptable"
    elif z_mb < -2:
        return "Statistically significant mass loss", "Investigate imbalance"
    else:
        return "Statistically significant over-recovery", "Check response factors"


def diagnostic_zone(amb, rmb, z_mb):
    """
    EXACTLY matches Table 1 in the paper
    """

    if abs(z_mb) <= 2:
        return "Zone 1 – Analytical variability"

    if amb < 98 and rmb < 0.8:
        return "Zone 2 – Missing or undetected degradants"

    if amb < 98 and 0.8 <= rmb <= 1.2:
        return "Zone 3 – Physical loss mechanisms"

    if amb > 102 and rmb > 1.2:
        return "Zone 4 – Overestimation / RF mismatch"

    return "Zone 3 – Method or degradation pathway issue"


def recommended_action(zone):
    if "Zone 1" in zone:
        return "No investigation required"
    if "Zone 2" in zone:
        return "Search for additional degradants / volatility studies"
    if "Zone 3" in zone:
        return "Investigate physical loss or degradation pathways"
    if "Zone 4" in zone:
        return "Review response factors and integration parameters"
    return "Expert review required"