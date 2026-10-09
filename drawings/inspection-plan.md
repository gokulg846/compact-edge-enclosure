# Inspection and tolerance package / Rev B / mm

Drawings are **review issue**, not released production drawings. Proposed tolerances assume a competent small-part CNC process and require shop agreement. Coordinates are basic nominal locations; hole position is controlled independently as listed. Datum A = tray underside; B = front outside Y0 plane; C = left outside X0 plane. Thermal lid datum D = underside mating plane; E/F = its front/left edges.

| Feature | Nominal | Proposed tolerance / acceptance | Method |
|---|---|---|---|
| Base outline | 100 × 70 | ±0.10 | Caliper; compare at several heights |
| Base rim height from A | 17.00 | ±0.03 | Surface plate + height gauge on A |
| Base floor | 3.00 | ±0.10 | Depth micrometer from rim, subtract measured rim height |
| A flatness | Underside | 0.05 total zone | CMM plane form after unclamping, or full surface-plate indicator sweep; no datum reference on flatness |
| B perpendicularity to A | Front plane | 0.05 over face | CMM or qualified square + indicator sweep, part seated on A |
| C perpendicularity to A/B | Left plane | Proposed 0.05 to A; squareness to B checked separately | CMM aligned A then B; report angular/linear deviation |
| PCB support tops | Z6.00 | ±0.03 each from A; coplanarity range ≤0.05 | Height gauge at all four tops; no rocking dummy PCB |
| PCB mounting holes | (18,18),(18,52),(82,18),(82,52) | M2.5 × 0.45; position Ø0.10 at RFS to A/B/C | CMM threaded center via qualified threaded mandrel or pre-tap pilot center; thread gauge; do not use caliper to claim true position |
| Lid mounting holes | (6,6),(6,64),(94,6),(94,64) | M3 × 0.5; position Ø0.10 at RFS to A/B/C | Same qualified center method; full-thread depth check |
| External mount holes | (25,35),(75,35) | Ø4.50 +0.10/-0; position Ø0.20 at RFS to A/B/C | Pin gauges + CMM |
| Connector opening | X25..41, Z7..14, R1.50 | Width/height +0.15/-0; location ±0.10 to C/A | Optical comparator, pins/radius gauge, connector coupon |
| Lid plate | 2.00 | ±0.05 | Micrometer away from fins/pedestal |
| Lid mating face D | Plane | Flatness0.05 | CMM or sweep on plate; recheck after unclamping |
| Lid clearance sites | Same four corners | Ø3.40 +0.10/-0; position Ø0.15 to D/E/F | Pin gauges + CMM; actual screws must hand assemble |
| Fan holes | (34,19),(34,51),(66,19),(66,51) | Ø3.40 +0.10/-0; position Ø0.20 to D/E/F | Pin gauges + CMM; compare actual purchased fan |
| Pedestal projection from D | 6.90 | ±0.03 | Depth micrometer / height gauge; surface plate |
| Pedestal contact face | 30 × 24 R3 | Flatness0.03; remove burrs, no anodize | CMM form or indicator; inspect pad contact imprint |
| Fins | 2.00 thick; 6.00 high; 3.60 gap | ±0.10 | Micrometer / depth gauge / gauge blocks; no bent fins |
| PCB / chip assumptions | Thickness1.60 / height 2.00 | ±0.05 each, assumed | Replace with measured board and package data |

**Functional clearance checks.** PCB is 80 × 50 within the large pocket, with 7 mm nominal edge-to-straight-wall space. Corner islands and support screw heads are checked with actual CAD intersections; a rectangular bounding box alone is insufficient. Lid registration relies on four screw clearances, not a precision rabbet. M3 nominal shaft versus Ø3.4 clearance gives 0.20 mm radial allowance; base/lid positional error radii 0.05+0.075 =0.125 mm leave nominal 0.075 mm radial margin before screw/size/datum variation. Physical simultaneous assembly remains required. PCB Ø2.7 versus M2.5 gives only 0.10 mm radial allowance; confirm actual board positional tolerances and screw sizes before manufacture.

**Pad stack.** Gap g = 17.00 - 6.90 - 6.00 - 1.60 - 2.00 = 0.50 mm. Worst case ±(0.03+0.03+0.03+0.05+0.05)=±0.19; g=0.31..0.69 mm. For an assumed free pad 1.00±0.05, compression spans 27.4..70.5%. This is a selection envelope, **not an acceptable compression specification for an unspecified pad**. Find a supplier curve that supports the actual gap/pressure, or introduce measured shims / revise pedestal height before applying power. No PCB bending or contact force calculation is possible without pad and board data. RSS≈0.088 mm is informational only; independence and distribution are unknown, so it does not replace the worst-case decision.

Tolerance choices control contact and fit. Position at RFS means no bonus tolerance is assumed. Flatness is form, not position. A general caliper inspection cannot certify a cylindrical position zone; if no CMM/qualified fixture is available, record coordinate measurements as screening and leave positional acceptance open. Prototype fixture repeatability does not establish metrology traceability or substitute for a calibrated datum simulator.
