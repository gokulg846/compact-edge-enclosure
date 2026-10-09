# Thermal model and physical validation plan

Governing equation: ΔT = Q × Rθ. Steady state, single dominant path, no transient capacitance model. Temperature is **component case**, not silicon junction. Assumed path: case → compressed pad/contact interfaces (0.8 K/W) → aluminum pedestal/spreading (0.5 K/W) → finned lid/air (passive 6.0 or forced 2.0 K/W). Case-to-junction resistance is unknown and excluded. Parallel radiation, tray conduction and PCB convection are absorbed into an effective air resistance estimate, not independently calculated or double-counted.

Nominal at Q=8 W, ambient 35°C: passive Rtotal7.3 K/W, ΔT58.4°C, Tcase93.4°C (**above 80°C target**); forced Rtotal3.3 K/W, ΔT26.4°C, Tcase61.4°C. At 35°C, predicted heat ceilings at 80°C are6.16 W passive and 13.64 W forced; these are analytical screening values, not product ratings. Passive test must stop before8 W if the hardware approaches80°C.

Plausibility only: six fins add approximately 2 × 6 × 0.006 × 0.024 =0.00173 m² of side area to an approximately0.007 m² lid plan area; edge/pedestal exposure and blocked areas change this estimate. Rair6 implies an effective conductance0.167 W/K. Convection coefficients, radiation, orientation, bypass and efficiency remain unmeasured, so no geometry-derived h or supplier-verified resistance is claimed. Forced2 is a hypothesis to test, not a fan datasheet value.

Sensitivity plot bands sweep contact 0.4..1.6, spreading 0.3..0.8, passive air 4..10 and forced air 1..4 K/W. At 8 W/35°C, corner predictions are passive 72.6..134.2°C and forced 48.6..86.2°C. The forced high corner also fails. Bands are deterministic corners, not statistical confidence intervals.

## Bench test

Use a metal lid and representative board coupon with a rated low-voltage heater mounted on a20 × 20 dummy component block. Use an isolated, current-limited supply, suitable fused leads, independent thermal cutoff and a noncombustible bench. A competent operator selects ratings and cutoff hardware before energizing. No automotive power or vehicle integration is needed.

Measure heater voltage and current at the heater terminals; log Q=VI rather than supply setpoint. Attach calibrated temperature sensors to the dummy case adjacent to the TIM, pedestal/lid and ambient shielded from the thermal plume. Do not put a thick sensor in the pad contact plane. Record sensor type, attachment, calibration uncertainty, sampling interval and exact fan model/voltage. Guard the fan and secure leads before running.

1. Inspect flatness and measure actual gap. Verify pad pressure/temperature specification, contact imprint and board deflection with no power. If contact is incomplete or the board bends, revise shim/pedestal/pad first.
2. At ambient 25±2°C and 35±2°C in a controlled enclosure, test passive at 2,4,6 W, then8 W only if previous stage leaves margin. Repeat forced condition at the same levels with fan axis blowing onto the fins and exhaust channels unobstructed. Record orientation; repeat rotated90° if practical.
3. Sample at 1 Hz. Treat steady state as |slope|<0.1°C/min over 10 min and stable ambient within 1°C. Cap each stage at 45 min and label nonsteady runs. Use a second run after cool-down to test repeatability.
4. **Stop immediately** at any case sensor≥80°C, accessible metal≥60°C, unexpected odor/smoke, pad damage, unstable fixture, sensor loss, fan stoppage during a forced run, or lower component/supply rating. Cut heater power first; allow guarded cool-down. Configure an independent cutoff to prevent exceeding the selected hardware's lower rated limit.
5. Calculate Rmeasured=(Tcase-Tambient)/Q only for stable stages; compare against assumptions and document uncertainty. Do not silently extrapolate stopped tests. Raw template is empty until measurements exist.

No physical temperatures, confidence intervals, transient response, CFD or FEA results are present in this repository.
