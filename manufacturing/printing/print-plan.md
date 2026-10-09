# Room-temperature print prototype

> Future handoff material. Physical execution is outside the current digital-only project scope.


Purpose: validate packaging, tool access, cable clearance and assembly sequence before aluminum machining. No physical print has been made. Use a calibrated FDM printer with PETG as the initial fit-material candidate; actual thermal/mechanical capability depends on the selected filament and settings. Do not use a printed thermal lid for an 8 W heater test.

- Base STL: translate to bed Z0; underside down, cavity up. Initial settings: 0.2 mm layers, 0.4 mm nozzle, 4 perimeters, 5 top/bottom layers, 30–40% infill. These are trial settings, not qualified process parameters.
- Connector opening bridges 16 mm across its upper edge; add local removable support or verify a bridge coupon first. Keep support scars away from datum faces and connector fit surfaces.
- Thermal lid dummy: printing in assembly orientation requires broad supports under the plate around the pedestal. Prefer split fit mockups or supported print with pedestal side down; inspect flatness after support removal. The delivered integral STL is not automatically support-free. A separately machined metal lid preserves the thermal path for later tests.
- Pilot holes in the CNC model are intentionally undersize for threads. For a fit print, drill/tap gently for low-load assembly after cooling. Print a hole coupon first. Prefer measured heat-set insert redesign before repeated use; **no unselected insert geometry has been claimed compatible**. Support the part while reaming and use low hand force. Do not infer threaded plastic strength from metal geometry.
- Starting dimensional acceptance: external envelope ±0.30 mm, hole center coordinates ±0.30 mm, minimum wall ≥2.5 mm. PCB seating and lid clearance must pass by hand without force. CNC geometric tolerances do not apply to this print.

Assembly: inspect/deburr → try mount bolts with PCB absent → install dummy PCB using four M2.5 screws → check connector and cable coupon → place unpowered pad dummy → lower lid without rocking → install four M3 screws with light alternating hand snugging → verify access and reopening. No torque value is released without thread/fastener selection.

First-print revisions: measure X/Y shrinkage; compensate holes using coupons; redesign for chosen inserts; evaluate front bridge sag and cover flatness; check screwdriver sweep and head clearances; inspect cable bend and connector corner fit. Record photos with scale, settings, material lot and failed features. Do not replace dimensions with guessed shrink factors.

| Property | Printed fit prototype | Machined aluminum |
|---|---|---|
| Iteration | Fast local shape changes; calibration dependent | More setup effort; predictable inspection surfaces |
| Thermal | Polymer lid invalidates metal resistance model | Continuous metal path; still needs heater validation |
| Threads | Weak/unqualified tapped plastic; insert redesign likely | Tapped bosses planned; engagement/torque untested |
| Tolerance | Initial ±0.30 screening, then measure | Critical heights ±0.03 proposal; shop review required |
| Finish | Layer anisotropy, support scars | Deburring, distortion and tool access concerns |
| Evidence | Print test pending | Machining and CAM simulation pending |
