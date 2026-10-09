# Five-minute hardware-manager walkthrough

**0:00–0:35 — Frame the problem.** “I wanted a compact, serviceable enclosure for a generic compute board. I set an arbitrary100 × 70 × 25 mm housing target, then made board interfaces, wall thickness and heat load explicit assumptions. This is independent work, not comma geometry.” Open the README assembly image.

**0:35–1:20 — Show editable geometry.** Open `cad/parameters.json`, then `exports/assembly.step` in a CAD viewer. “The base carries four PCB supports and four lid interfaces. The removable aluminum lid includes an integral pedestal and six fins. The connector and component envelopes are modeled independently. I can regenerate from these parameters.” Show the exploded image and change an envelope parameter only in a copy if demonstrating live.

**1:20–2:05 — Explain manufacturing judgment.** Open the CNC setup diagram. “A top pocket leaves corner islands and R3 transitions. I moved PCB supports away from the corner features. The tray needs a flip to remove sacrificial grip and a side setup for the connector. The thin thermal lid needs a support nest on its second side. This is a reviewable process plan, not verified CAM or G-code.” Mention the blind drill-tip/tap-depth risk.

**2:05–2:50 — Explain the critical interface.** Show the center section and pad stack. “Seat height minus pedestal projection minus board/chip stack gives a 0.50 mm gap; worst case is0.31–0.69. That is too much uncertainty to pick a pad by thickness alone. I need a compression-force curve, real board measurements and a contact imprint before heating.” Do not claim a selected pad or tested preload.

**2:50–3:35 — Show an unfavorable result.** Open thermal sensitivity plot. “At 8 W and 35°C ambient, assumed passive resistance predicts 93.4°C, missing my80°C case target. Forced airflow predicts 61.4°C nominal, but the high uncertainty corner still fails. The model tells me what to measure, not that the product is qualified.” Point to the stop conditions and raw-log template.

**3:35–4:15 — Show verification evidence.** Open `results/validation.json` and `results/tests.txt`. “These files come from executed checks: valid solids, STEP round trips, STL topology, nominal intersections, invalid-parameter tests and thermal arithmetic. They do not verify wiring, manufacturing tolerances, actual airflow or strength.” Use actual counts printed in the current results, rather than memorizing a stale count.

**4:15–5:00 — Close with the physical next step.** Show the fixture image. “Three bottom contacts, two front stops and one side stop establish repeatable location. I would print a fit article, measure it, perform 20 reinstalls across two operators, then make the metal thermal path and run a guarded heater test. I have not yet fabricated this. The repository makes that next day of shop work concrete and measurable.”
