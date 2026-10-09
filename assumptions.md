# Assumptions, coordinates and evidence boundaries

## Model and interfaces

Millimetres throughout CAD and drawings. Origin: front-left underside of the tray. +X follows the 100 mm length, +Y follows the 70 mm width toward the rear, +Z is up. Datum A = underside Z0; B = front exterior face Y0; C = left exterior face X0. Drawing tables locate holes from B/C; locate Z heights from A. STEP solids retain these assembly coordinates, including individual part files.

`cad/parameters.json` is the parameter master. `cad/model.py` is the validated editable solid source. The OpenSCAD companion is generated from the same parameters, including a sampled rounded pocket outline. Regenerate its include file after every parameter edit. OpenSCAD execution and equivalence are **not** verified; the B-rep exports are the reviewed geometry.

Base: 100 × 70 × 17; floor/wall 3; external vertical corners R3. The pocket leaves 10 mm corner islands for lid fasteners; transitions R3. Four integral PCB supports rise to Z6. Lid: 2 mm plate at Z17..19, six 2 mm fins to Z25 and a 30 × 24 R3 pedestal down to Z10.1. Pedestal is integral, not a loose heatsink requiring undocumented adhesive retention. Fins run along Y; fan exhaust must escape between fins along Y.

Generic PCB: X10..90, Y10..60, Z6..7.6. Holes at (18,18), (18,52), (82,18), (82,52). Chip: X40..60, Y25..45, Z7.6..9.6. Compressed pad: Z9.6..10.1. Secondary component keepout: X70..82, Y26..44, Z7.6..12.6. The model does not represent every real component, trace, underside component, antenna, camera optical cone, or electrical interface. A real board survey must replace these assumptions.

Connector opening: front wall, X25..41, Z7..14, R1.5. Assumed connector: X25.75..40.25, Y-2..10, Z7.75..13.25. R1.5 corners reduce the local corner margin; exact nominal noninterference is checked by B-rep. Connector support/attachment is assumed part of the board assembly, not modeled electrically. Reserve Y-32..-2 for a plug and cable; a real supplier bend radius is unknown. Housing is 100 × 70 × 25, assembled connector envelope is 100 × 72 × 25, and cable space is additional.

## Hardware and process

Candidate material: 6061-T6 plate, uncoated for initial prototype. No temper certification or stock purchase occurred. Machined surfaces are proposals, not measured capability. Small edge breaks 0.2–0.4 are deburring notes, not modeled. No thread helices: tapped holes are represented by pilots and screw shafts by simplified root diameters. Do not interpret nominal zero intersection as thread engagement verification.

Lid: 4 × M3 × 8, nominal 6 mm engagement; PCB: 4 × M2.5 × 5, nominal 3.4 mm engagement. Tap depths and bottom clearance require shop verification; modeled flat-bottom pilot volumes are not drill-tip geometry. Use a bottoming process and verify the 2 mm remaining PCB-boss floor. No torque, thread strength, pullout, vibration endurance or preload is validated. Fastener head envelopes are assumptions pending actual selection.

External mounting: 2 × M4 button-head bolts through floor to an external bench bracket (not supplied). Reserve head height ≤2.5 mm so PCB underside clearance is ≥0.5 mm, with no underside electronics in these zones. Mount enclosure before installing PCB. The bracket must not obstruct front cable access. This is a bench demonstrator, not an approved vehicle installation.

Optional fan: generic 40 × 40 × 10 frame, 32 mm square hole pitch. Four 6 mm tubular spacers, Ø6 OD / Ø3.4 ID; use M3 through bolts and nuts selected after purchase. Heads, nuts, fan blades, wiring and finger guard are not modeled. Reserve 3 mm above the fan and verify nut clearance beneath lid at X34/66,Y19/51. No specific fan curve, flow, power or acoustics is assumed known. Fan body envelope reaches Z35; hardware reserve reaches Z38.

The printed enclosure is a room-temperature fit prototype, not a thermally equivalent aluminum enclosure. Printed thermal-lid geometry is a dummy. Use a metal lid for powered testing. No finite element analysis, CFD, machining, CAM toolpath simulation, printing or physical measurements were performed.

## Toolchain decision

Environment inspection found no FreeCAD, OpenSCAD, PythonOCC, CadQuery or mesh checker in the default Python. The bundled runtime had NumPy/ReportLab. A project-local Python 3.12 venv successfully installed CadQuery/OCP, trimesh, matplotlib, ReportLab, pypdf and pytest. This enabled real B-rep STEP plus watertight STL exports without a large desktop CAD install. The requested OpenSCAD source is also supplied, but the verified CAD route is CadQuery. No native CAM application was available. Haas VF-2 is a reference machine from the user brief, not a verified machine configuration.

## Rev C digital refinement

The nominal enclosure geometry is unchanged. The obsolete lid_boss_radius parameter has been replaced by corner_island_width, which drives the actual pocket. A B-rep ring test checks 1.5 mm of material around each lid pilot. CAD sources are formatted for readability. Report generation now rejects inputs differing from the reviewed snapshot. See docs/review-notes.md and analysis/design-study.md for the digital audit and area-based comparison. Physical procedures are future handoff material, outside the current digital-only scope.
