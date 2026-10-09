"""Rebuild a small design comparison and connect the thermal assumptions to lid area.

This is a CAD experiment plus an isothermal convection bound, not CFD.
Changing geometry does not magically establish a new fan performance rating.
"""

import csv
import json
import math
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / ".cache/matplotlib"))
import cadquery as cq
from cad.model import parameters, build
from analysis.thermal import inputs
from scripts.validate import intersections


def exposed_area(p):
    """Exposed upper lid and fin area in m², assuming isothermal aluminum.

    Round external corners and eight holes are removed from the plate plan area.
    Four M3 head annuli obscure plate area. Fin top area replaces its footprint,
    so only the two long sides and two ends add area to the original lid plan.
    Lid edge, screw head, enclosure, radiation and PCB paths are excluded.
    """
    plate = p["length"] * p["width"] - (4 - math.pi) * p["corner_radius"] ** 2
    plate -= 4 * math.pi * (p["lid_screw_clearance"] / 2) ** 2 + 4 * math.pi * 1.7**2
    plate -= 4 * math.pi * (2.75**2 - (p["lid_screw_clearance"] / 2) ** 2)
    extra = (
        2 * p["fin_count"] * p["fin_height"] * (p["sink_width"] + p["fin_thickness"])
    )
    return (plate + extra) / 1e6


def area_screen(p, a=None):
    a = inputs() if a is None else a
    area = exposed_area(p)
    internal = a["contact_K_W"] + a["spreading_K_W"]
    air_budget = (a["case_limit_C"] - a["ambient_C"]) / a["heat_W"] - internal
    if air_budget <= 0:
        raise ValueError("Internal resistances consume the temperature budget")
    h = a["area_comparison_h_W_m2K"]
    return {
        "exposed_area_m2": area,
        "required_effective_h_W_m2K": 1 / (air_budget * area),
        "air_resistance_at_common_h_K_W": 1 / (h * area),
        "isothermal_case_at_common_h_C": a["ambient_C"]
        + a["heat_W"] * (internal + 1 / (h * area)),
        "h_implied_by_legacy_passive_R_W_m2K": 1
        / (a["air_resistance_K_W"]["passive"] * area),
        "h_implied_by_legacy_forced_R_W_m2K": 1
        / (a["air_resistance_K_W"]["forced"] * area),
    }


def main():
    baseline = parameters()
    study_exports = ROOT / "exports/studies"
    study_exports.mkdir(parents=True, exist_ok=True)
    candidates = [
        ("six_fins_6mm", {}),
        ("four_fins_6mm", {"fin_count": 4}),
        ("six_fins_10mm", {"fin_height": 10.0, "height": 29.0}),
        ("eight_fins_6mm", {"fin_count": 8}),
    ]
    records = []
    for name, changes in candidates:
        p = {**baseline, **changes}
        row = {
            "candidate": name,
            "changes": changes,
            "within_25mm_target": p["height"] <= 25,
        }
        try:
            parts = build(p)
        except ValueError as exc:
            row.update(status="REJECTED", reason=str(exc))
            records.append(row)
            continue
        if not all(
            part.val().isValid() and len(part.val().Solids()) == 1
            for part in parts.values()
        ):
            raise RuntimeError(f"Candidate {name} contains an invalid solid")
        clashes = intersections(parts)
        if clashes["unintended_intersections"]:
            raise RuntimeError(
                f"Candidate {name} contains unintended overlaps: {clashes}"
            )
        # Preserve each compared lid so a reviewer can inspect the actual alternative.
        export_path = study_exports / f"{name}.step"
        cq.exporters.export(parts["thermal_lid"], str(export_path))
        imported = cq.importers.importStep(str(export_path)).val()
        relative_error = (
            abs(imported.Volume() - parts["thermal_lid"].val().Volume())
            / parts["thermal_lid"].val().Volume()
        )
        if (
            not imported.isValid()
            or len(imported.Solids()) != 1
            or relative_error > 1e-6
        ):
            raise RuntimeError(f"Candidate {name} failed STEP round-trip validation")
        row.update(
            step_file=str(export_path.relative_to(ROOT)),
            step_valid=True,
            step_relative_volume_error=relative_error,
        )
        row.update(
            status="CAD_CHECKED",
            housing_height_mm=p["height"],
            lid_volume_mm3=parts["thermal_lid"].val().Volume(),
            nominal_pair_checks=clashes["pair_count"],
            fin_channel_mm=(p["sink_length"] - p["fin_count"] * p["fin_thickness"])
            / (p["fin_count"] - 1),
            **area_screen(p),
        )
        records.append(row)
    output = {
        "method": "CAD variants + isothermal upper-bound area screen; not CFD or validated convection",
        "inputs": inputs(),
        "candidates": records,
        "decision": "Retain six 6 mm fins as baseline; taller fins break the height target; eight fins break the cutter-width constraint. Cooling remains unresolved.",
    }
    (ROOT / "results/design-study.json").write_text(json.dumps(output, indent=2) + "\n")
    keys = [
        "candidate",
        "status",
        "housing_height_mm",
        "within_25mm_target",
        "lid_volume_mm3",
        "fin_channel_mm",
        "exposed_area_m2",
        "required_effective_h_W_m2K",
        "reason",
    ]
    with (ROOT / "results/design-study.csv").open("w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=keys, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(records)
    plot(records)
    print(json.dumps(output, indent=2))


def plot(rows):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    valid = [r for r in rows if r["status"] == "CAD_CHECKED"]
    names = ["6 fins / 6 mm", "4 fins / 6 mm", "6 fins / 10 mm"]
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.3), layout="constrained")
    colors = ["#137e82", "#647a92", "#b77335"]
    for ax, values, label in [
        (
            axes[0],
            [r["exposed_area_m2"] * 1e4 for r in valid],
            "Exposed lid + fin area [cm²]",
        ),
        (
            axes[1],
            [r["required_effective_h_W_m2K"] for r in valid],
            "Required effective h [W/(m² K)]",
        ),
    ]:
        ax.barh(names, values, color=colors, height=0.55)
        ax.invert_yaxis()
        ax.set_xlabel(label)
        ax.spines[["top", "right"]].set_visible(False)
        ax.set_xlim(0, max(values) * 1.20)
        for i, v in enumerate(values):
            ax.text(v + 0.4, i, f"{v:.1f}", va="center", fontsize=10)
    axes[0].set_title("Geometric change", loc="left")
    axes[1].set_title("To reach 80°C at 8 W, 35°C ambient", loc="left", fontsize=11)
    fig.suptitle("Fin comparison | common isothermal assumption", fontsize=14)
    fig.savefig(ROOT / "images/design_study.png", dpi=190)
    plt.close(fig)


if __name__ == "__main__":
    main()
