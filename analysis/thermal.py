"""Lumped steady-state thermal model; assumptions, NOT measured performance."""

from pathlib import Path
import json
import math

ROOT = Path(__file__).resolve().parents[1]


def temperature(q, ambient, r_contact, r_spreading, r_air):
    values = [q, ambient, r_contact, r_spreading, r_air]
    if not all(math.isfinite(v) for v in values):
        raise ValueError("finite inputs required")
    if q < 0 or min(r_contact, r_spreading, r_air) < 0:
        raise ValueError("heat and resistance must be nonnegative")
    return ambient + q * (r_contact + r_spreading + r_air)


def inputs():
    """Read the explicit analysis assumptions; none are supplier-qualified ratings."""
    return json.loads((ROOT / "analysis/assumptions.json").read_text())


def calculate(p=None):
    import sys

    sys.path.insert(0, str(ROOT))
    from cad.model import parameters, derived

    p = parameters() if p is None else p
    geometry = derived(p)
    a = inputs()
    q, ambient = a["heat_W"], a["ambient_C"]
    out = {
        "status": "CALCULATED FROM ASSUMPTIONS; NOT TESTED",
        "heat_W": q,
        "ambient_C": ambient,
        "limit_case_C": a["case_limit_C"],
        "R_contact_K_W": a["contact_K_W"],
        "R_spreading_K_W": a["spreading_K_W"],
        "configurations": {},
    }
    for name, air in a["air_resistance_K_W"].items():
        total = a["contact_K_W"] + a["spreading_K_W"] + air
        case = temperature(q, ambient, a["contact_K_W"], a["spreading_K_W"], air)
        out["configurations"][name] = {
            "R_air_K_W": air,
            "R_total_K_W": total,
            "case_C": case,
            "max_heat_at_80C_W": (a["case_limit_C"] - ambient) / total,
            "target_met_nominal": case <= a["case_limit_C"],
        }
    out["uncertainty_at_8W_35C"] = {}
    for name, air_range in a["air_ranges_K_W"].items():
        low = temperature(
            q,
            ambient,
            a["contact_range_K_W"][0],
            a["spreading_range_K_W"][0],
            air_range[0],
        )
        high = temperature(
            q,
            ambient,
            a["contact_range_K_W"][1],
            a["spreading_range_K_W"][1],
            air_range[1],
        )
        out["uncertainty_at_8W_35C"][name] = {"low_C": low, "high_C": high}
    # Derive nominal contact gap from the same geometry that generates the CAD.
    pedestal_projection = geometry["body"] - geometry["ped_z"]
    gap = (
        geometry["body"]
        - pedestal_projection
        - geometry["board_z"]
        - p["board_thickness"]
        - p["chip_height"]
    )
    tolerances = list(a["stack_tolerances_mm"].values())
    worst = sum(tolerances)
    free_min = p["pad_free"] - a["pad_free_tolerance_mm"]
    free_max = p["pad_free"] + a["pad_free_tolerance_mm"]
    out["pad_stack_mm"] = {
        "nominal_gap": gap,
        "worst_case_sum": worst,
        "gap_min": gap - worst,
        "gap_max": gap + worst,
        "pad_free_min": free_min,
        "pad_free_max": free_max,
        "compression_min_pct": (1 - (gap + worst) / free_min) * 100,
        "compression_max_pct": (1 - (gap - worst) / free_max) * 100,
        "RSS_reference_only": math.sqrt(sum(t * t for t in tolerances)),
    }
    return out


def main():
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np

    data = calculate()
    a = inputs()
    (ROOT / "results/thermal.json").write_text(json.dumps(data, indent=2) + "\n")
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 11,
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    )
    fig, ax = plt.subplots(figsize=(10, 5.4), layout="constrained")
    fig.set_facecolor("#f7f9fc")
    ax.set_facecolor("#f7f9fc")
    q = np.linspace(0, 12, 100)
    for name, c in [("passive", "#d78328"), ("forced", "#077f83")]:
        bounds = [
            a["contact_range_K_W"][i]
            + a["spreading_range_K_W"][i]
            + a["air_ranges_K_W"][name][i]
            for i in (0, 1)
        ]
        r = data["configurations"][name]["R_total_K_W"]
        ax.plot(
            q,
            a["ambient_C"] + q * r,
            color=c,
            lw=2.5,
            label=f"{name.capitalize()} assumption: {r:.1f} K/W total",
        )
        ax.fill_between(
            q,
            a["ambient_C"] + q * bounds[0],
            a["ambient_C"] + q * bounds[1],
            color=c,
            alpha=0.10,
        )
        ax.scatter([a["heat_W"]], [a["ambient_C"] + a["heat_W"] * r], color=c, zorder=4)
    ax.axhline(
        a["case_limit_C"],
        color="#a43838",
        ls="--",
        label=f"{a['case_limit_C']:g} C case screening target",
    )
    ax.axvline(a["heat_W"], color="#6e7d91", ls=":", lw=1)
    ax.set(
        xlabel="Applied heat load [W]",
        ylabel="Estimated component case temperature [C]",
        title=f"Resistance scenarios | {a['ambient_C']:g} C ambient",
        xlim=(0, 12),
        ylim=(30, 160),
    )
    ax.grid(alpha=0.15)
    ax.legend(loc="upper left", fontsize=9)
    fig.text(
        0.99,
        0.01,
        "Bands: assumption corners, not statistical confidence intervals",
        ha="right",
        fontsize=8,
        color="#53647c",
    )
    for ext in ["png", "svg"]:
        fig.savefig(ROOT / "images" / f"thermal_sensitivity.{ext}", dpi=180)
    plt.close(fig)
    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
