# Engineering requirements / Rev B

All dimensions below are design-study assumptions. No real board or comma hardware was measured.

| ID | Requirement | Rationale | Target | Verification | Status |
|---|---|---|---|---|---|
| R01 | Compact housing | Desk-scale packaging exercise | 100 × 70 × 25 mm passive | B-rep bounding box | CAD checked; connector adds 2 mm at front |
| R02 | Configurable board | Adapt to a measured board later | 80 × 50 × 1.6 mm; four Ø2.7 holes, 64 × 34 pitch | Parameter checks, solid intersections | CAD checked; board assumed |
| R03 | Robust structure | Rapid machining/printing | Wall/floor ≥2.5 mm; default 3 mm | Parameter and model review | Nominal checked; no strength qualification |
| R04 | Service access | Remove PCB without destructive disassembly | Four M3 lid screws; four M2.5 PCB screws | CAD access review, physical timed assembly | Access proposed; physical test pending |
| R05 | Controlled thermal path | Avoid undocumented air gaps | 20 × 20 chip → pad → integral Al pedestal → fins | Stack analysis; pad imprint test | Calculated; pad selection pending |
| R06 | Thermal screening | Evaluate cooling adequacy | Case ≤80°C at 8 W, 35°C ambient | Lumped model + heater test | Passive predicted FAIL; forced nominal predicted PASS, unverified |
| R07 | Connector access | Avoid shell interference | 16 × 7 opening, R1.5; nominal 0.75 mm envelope margin; 30 mm cable keepout | Solid intersection; cable trial | Nominal CAD checked; cable assumption |
| R08 | CNC tool access | Ordinary 3-axis work | Main cavity R3, 6 mm rougher; 3.6 mm fin channels, 3 mm finish tool | Radius checks, CAM review | Geometric checks only; no CAM simulation |
| R09 | External mounting | Secure bench interface | Two Ø4.5 holes at (25,35), (75,35) | Hole table, bolt access trial | CAD checked; board removed for mounting |
| R10 | Thermal-pad gap | Maintain contact without excessive force | 0.50 nominal; 0.31–0.69 mm worst case | Stack + height measurements | Calculated; force/board strain unknown |
| R11 | Repeatable location | Reduce handling variation | 3-2-1 fixture; trial range ≤0.05 mm in X/Y/Z | Ten remove/reinstall cycles per operator | Target only; no measurement |
| R12 | Editable deliverables | Review and reproduce | Source + STEP/STL + drawing/report PDFs | Regeneration, STEP reimport, STL topology | See results/validation.json and tests.txt |
| R13 | Optional cooling | Isolate size/complexity tradeoff | 40 × 40 × 10 fan at Z25..35; reserve to Z38 with fasteners | Variant CAD + future airflow test | CAD checked; fan is generic envelope |
| R14 | Honest evidence | Credible portfolio | Separate facts, assumptions, calculations and physical results | Documentation review | No machining, printing, thermal or repeatability results claimed |
