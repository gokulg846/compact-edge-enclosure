# Six contacts, two gentle lateral clamps

Fixture plate: X-15..115, Y-15..85, Z-10..-4. Part remains at assembly origin. Three Ø6 support buttons at (18,12),(82,12),(50,58) have top Z0. Their noncollinear contacts constrain Z, roll and pitch. Two Ø6 side buttons at (20,-3),(80,-3), extending to Z5, contact Y0 and constrain Y/yaw. One at (-3,35) contacts X0 and constrains X. All six have Ø3 simplified mounting stems through Ø3.3 plate holes; secure with underside washers/nuts and add calibrated shims under button shoulders. Provide a raised bench support or pocket below plate for nuts (not modeled).

Lateral clamp blocks sit at rear and right. Two Ø4.5 mounting holes per block mate to M4 tapped plate locations: rear (42,78),(58,78); right (108,27),(108,43). Horizontal M4 pilots drive replaceable pads against the two free faces at Z1.5, close to the supported floor. Buy/select swivel-tip screws after checking travel and pad attachment. CAD shows blocks/pads/bores; screws, nuts and bench feet are simplified/omitted. A light removable hold-down strap over the exposed rim is needed for upside-down use or significant assembly torque; not yet designed. The present jig is for gentle bench inspection with gravity seating, not a machining fixture.

Assembly: deburr plate → mount/shim three A supports to equal height → mount B1/B2/C1 → mount two clamp blocks → verify unclamped tray drops freely onto all supports → bias toward B and C → apply only enough lateral force to seat → check A contact with thin paper at each support. Record clamp setting and operator sequence; do not squeeze walls. Exposed top allows lid screw access; front opening is between the B stops. Remove part from jig for underside inspection.

The OpenSCAD companion includes plate and six locating buttons only; the CadQuery STEP/STL and fixture drawing include the complete modeled clamp blocks/pads.

## Repeatability protocol (no results yet)

1. Calibrated 0.01 mm indicators or better on three accessible tray targets; fixture secured to a clean surface plate. Warm equipment and record ambient. Establish a baseline without rezeroing between trials.
2. Operator A removes the part completely, wipes contacts, reinstalls with the documented clamp sequence, and records X/Y/Z. Repeat ten times. Operator B performs ten independent cycles.
3. Use `results/fixture_trials_template.csv` and `scripts/repeatability.py`. Record real values only. Compute per-operator mean, sample standard deviation and max-min range, plus pooled ranges and between-operator mean shifts.
4. Proposed screening acceptance: each operator and pooled X/Y/Z range ≤0.05 mm; inter-operator mean shifts ≤0.03 mm. These are demonstrator targets, not capability claims. Investigate contamination, unequal pads, clamp-force sensitivity and part warp if exceeded.
5. Repeat at three clamp settings once a force-controlled method exists; verify that the fixture does not distort the tray. A range below target alone does not prove measurement accuracy. Qualify the fixture against a reference part before using it for acceptance inspection.
