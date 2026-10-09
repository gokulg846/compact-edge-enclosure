# Original concept review / Rev B

Scores use1=poor,5=strong; weights sum1.00. They are engineering judgment, not measurements. See concept_matrix.png and results/concepts.json.

| Criterion | Weight | A CNC tray + integral thermal lid | B bent sheet + spreader | C printed shell + metal insert |
|---|---:|---:|---:|---:|
| Packaging | .15 | 5 | 4 | 5 |
| Thermal path | .20 | 4 | 3 | 2 |
| Manufacturability | .20 | 3 | 5 | 4 |
| Serviceability | .15 | 5 | 3 | 4 |
| Assembly complexity | .10 | 4 | 3 | 4 |
| Inspection | .10 | 4 | 3 | 4 |
| Cost / iteration | .10 | 3 | 5 | 5 |
| Weighted total | 1.00 | **4.00** | **3.75** | **3.85** |

A wins narrowly because repeatable machined datums and a one-piece thermal path support the portfolio objective. C is the fastest fit prototype, so it remains the validation precursor. B reduces material removal but introduces bends, seams and bracket stack-ups. Weight sensitivity matters: assigning more weight to iteration cost can select C; the score is not proof of universal superiority.

## Recorded design iterations

| Revision | Original issue | Change | Expected effect | Verification and evidence |
|---|---|---|---|---|
| A, packaging baseline | A generic sealed plastic shell provides no defined metal thermal path | Split tray and removable aluminum thermal lid; integral30 × 24 pedestal plus six fins | Repeatable lid removal; eliminates loose-sink retention uncertainty | Final geometry generated; nominal contact stack calculated. No physical performance claim. Baseline configuration retained in cad/revisions/ |
| B, manufacturing / inspection | Cylindrical lid bosses meeting straight walls create difficult cutter junctions; PCB supports near corners reduce tool passage; thermal interface tolerances not controlled | Rounded stepped cavity with 10 mm corner islands/R3 transitions; PCB holes moved to 64 × 34 pitch; critical Z stack documented | Better end-mill access and measurable contact gap | B-rep and nominal intersection checks run; full cutter sweep and pad force still unverified |
| B, cooling option | Nominal passive calculation exceeds 80°C at 8 W/35°C | Add removable40 mm fan on6 mm spacers; retain passive baseline for comparison | Predicted case 61.4°C if assumed forced-air resistance2 K/W is achieved | Calculated only; high resistance corner86.2°C still fails. Fan increases hardware clearance envelope to 38 mm |

Revision A JSON is a retained early parameter state, not a claim that a physical first article existed. The current builder applies Rev B cavity construction to all parameter files; reconstructing exact early cylindrical corner geometry requires the documented baseline patch in cad/revisions/README.md. Rev C keeps the nominal geometry and supersedes this document with the executed comparison in [design-study.md](design-study.md).

## Risks (severity and likelihood1..5, ordinal judgments)

| Risk | S | L | Mitigation | Verification |
|---|---:|---:|---|---|
| Effective convection too weak; fan bypass/recirculation | 5 | 4 | Prototype metal lid; test orientation/flow; derate load | Controlled heater test and measured Rθ |
| Pad compression overloads PCB or loses contact | 5 | 4 | Measure gap; select vendor pressure curve; adjust pedestal/shims | Contact imprint, force/deflection check, thermal repeat |
| CNC plate warp and small-tool access | 4 | 3 | Supported nests; light finishing; toolholder/stock simulation | Unclamped inspection + machinist/CAM review |
| Blind-tap breakthrough / insufficient thread | 4 | 3 | Verify full drill diameter vs tip, bottoming depth, screw length | Depth/plug gauge; trial coupon |
| Printed connector sag / insert failure | 3 | 4 | Bridge/hole coupon, support tuning, measured insert redesign | Unpowered fit trials |
| Fixture shifts or squeezes part | 3 | 3 | Clean6 contacts; controlled lateral force; verify gravity seat |20 reinstall trials + force sensitivity |
| Real board/connector differs from assumed envelope | 4 | 4 | Measure actual electronics before ordering aluminum | Interface audit and parameter update |
| Fan wires/fasteners interfere | 3 | 3 | Select actual parts; complete hardware/lead model | Hands-on assembly and clearance check |

## Future physical handoff (outside current digital scope)

1. Buy/measure a board or make a dimensioned unpowered coupon; resolve connector and underside keepouts. Select pad/fan/fasteners; review thread depths and machining plan with operator.
2. Print tray/fit lid and a hole/bridge coupon. Log settings, inspect, photograph and perform five assemble/disassemble cycles. Revise shrink/insert interfaces using observations.
3. Build/inspect fixture; complete20 reinstall trials with two operators. Confirm clamping does not bend the tray.
4. Program and simulate actual CAM; machine a metal thermal lid and tray under shop supervision. Inspect critical heights and contact surfaces before assembly.
5. Measure pad gap/pressure, then perform guarded heater tests with explicit stops. Report raw logs and stopped runs. Only afterward evaluate more demanding vibration or installation requirements.
