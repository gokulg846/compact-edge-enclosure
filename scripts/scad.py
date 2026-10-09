"""Generate editable OpenSCAD companion from shared JSON; B-rep is release source."""

import sys
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import cadquery as cq
from cad.model import parameters, derived, cavity


def main():
    p = parameters()
    d = derived(p)
    pocket = cavity(p, 1)
    wire = pocket.faces("<Z").val().outerWire()
    points, _ = wire.sample(0.01)
    values = {
        **p,
        **d,
        "pocket_outline": [[round(v.x, 5), round(v.y, 5)] for v in points],
    }
    (ROOT / "cad/generated_parameters.scad").write_text(
        "// Generated from parameters.json by scripts/scad.py. Units mm.\n"
        + "\n".join(k + " = " + json.dumps(v) + ";" for k, v in values.items())
        + "\n"
    )
    print(
        "Generated OpenSCAD parameters and sampled R3 pocket profile; OpenSCAD execution not available."
    )


if __name__ == "__main__":
    main()
