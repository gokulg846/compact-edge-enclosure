# CNC process plan / review issue B

**Planning only. No CAM project, postprocessor, G-code or verified cutter paths are provided.** Reference machine: Haas VF-2, as requested. Actual travels, spindle, controller, toolholders, coolant, probing and shop fixtures must be confirmed on the machine. No feed or speed is released.

## Stock, datums and tools

- Tray: candidate 6061-T6 stock 110 × 80 × 25 mm. Finished body 100 × 70 × 17. Allow 5 mm sacrificial lower grip and 3 mm total facing allowance. Saw/square stock; measure actual blank before setting stock in CAM.
- Thermal lid: candidate 106 × 76 × 20 mm stock. Final maximum local thickness 14.9 mm (pedestal bottom Z10.1 to fin top Z25). Two-sided machining and a dedicated support nest are required; do not clamp on finished fins.
- Fixture plate: 130 × 100 × 6 mm finished. Candidate stock 136 × 106 × 8; steel locator buttons, aluminum clamp blocks and soft replaceable pads.
- Part datum A = finished underside; B = front Y0; C = left X0. Work offsets are not silently reused after flipping. Setup 1 starts from faced stock corner; transfer finished B/C using probing or an edge finder, and finish A in Setup 2.
- Candidate tools: T1 suitable face mill; T2 Ø6 flat end mill, flute length ≥16 mm for 14 mm tray cavity; T3 Ø3 flat end mill for R1.5 connector and 3.6 mm fin channels (reach and deflection reviewed); T4 spot drill; T5 Ø2.5 drill + M3 × 0.5 tap; T6 Ø2.05 drill + M2.5 × 0.45 bottoming tap; T7 Ø3.4 clearance drill; T8 Ø4.5 clearance drill; T9 hand deburr / small chamfer tool. Numbers are planning IDs, not machine tool pocket assignments. Verify tap-drill recommendations against selected tap/material.

## Tray sequence

| Setup / step | Operation and stock condition | Workholding / access | In-process inspection |
|---|---|---|---|
| 1.1 | Square stock; face top to intended Z17 datum surface | Vise/parallels, 5 mm lower sacrificial grip; verify jaw engagement | Face flatness, blank dimensions, vise seating |
| 1.2 | Rough top pocket to floor Z3; leave 0.25 radial / 0.15 axial for finish | Ø6 tool; leave corner screw islands and four PCB islands | Floor remaining stock, island positions |
| 1.3 | Finish cavity, floor and supports to Z6; retain R3 transitions | Finish balanced passes; confirm holder clears rim at 14 mm reach | Floor thickness after datum transfer; support top height/coplanarity |
| 1.4 | Spot/drill/tap four M3 lid sites; four M2.5 support sites | M3 pilot modeled from Z10 to 17; M2.5 pilot from Z2 to 6 | Pilot depth, thread depth, remaining bottom, gauge selected threads |
| 1.5 | Drill two Ø4.5 external mount holes through floor; perimeter rough/finish above grip | Clearance beneath through holes; leave sacrificial foot | Hole size and position, body X/Y dimensions |
| 2.1 | Flip onto custom soft-jaw nest contacting finished rim/islands; add fitted cavity support | Relieve nest for PCB bosses; never squeeze unsupported 3 mm walls | Re-establish B/C and seated Z; indicator check |
| 2.2 | Remove sacrificial grip; face underside to final Z0 | Light, balanced passes to control pocket-floor bow | Height17, floor 3, datum A flatness 0.05; release and recheck warp |
| 2.3 | Deburr external mounting exits and perimeter | Protect cosmetic/inspection faces | No burrs beneath datum A; check rocking on plate |
| 3.1 | Rotate 90° into supported nest to expose front Y0 | Close support behind connector region; part clamped away from slot | Probe opening origin X25/Z7 relative to C/A |
| 3.2 | Mill 16 × 7 rounded opening R1.5 through 3 mm front wall | Ø3 tool, light engagement; backing clearance for breakthrough | Opening size, corner radius, cable insertion coupon |
| 3.3 | Deburr 0.2–0.4; clean and inspect | Protect threads and thermal contacts from chips | Complete inspection plan |

Blind pilots in CAD have flat bottoms. Real drill tips consume extra axial space: program drilling/tapping only after the machinist verifies full-diameter depth, chip space and remaining material. M3 target full thread engagement ≥6 mm, M2.5 ≥3.4 mm. Consider thread milling or shorter screws if a safe blind-hole process cannot preserve the specified floor; do not drill through by assumption.

## Thermal lid sequence

1. Face stock; machine the underside relief to leave the centered 30 × 24 R3 pedestal projecting 6.90 ±0.03 below the mating plane. This plane eventually seats at Z17. Finish pedestal contact and mating rim from the same setup. Contact face is Z10.10 at nominal assembly.
2. Flip into a purpose-made nest relieved for the pedestal. Support the 2 mm plate continuously except at tool breakthroughs. Clamp sacrificial perimeter stock; establish mating plane as the Z reference. A fixture held only by thin unsupported plate is unacceptable.
3. Rough the top, retaining the 30 × 24 fin field. Finish the plate top 2.00 above the mating plane; finish fin tips 8.00 above it. Cut five 3.60 mm channels 6.00 deep with Ø3 tool. Six fins are 2.00 thick. Channel endpoints are open to Y23 and Y47 for radial air exhaust.
4. Drill four lid Ø3.40 through holes at (6,6),(6,64),(94,6),(94,64), and four fan Ø3.40 holes at (34,19),(34,51),(66,19),(66,51). Break edges lightly; no countersinks consuming the plate thickness.
5. Profile 100 × 70 with R3 corners using tabs or relocated clamps reviewed in CAM; remove tabs in secondary supported operation. Inspect thickness, pedestal projection, flatness and hole position after unclamping. Deburr fins without rounding away contact area.

## Failure modes and release checklist

Thin plate distortion → support nest and unclamped flatness check. Tool chatter/fin deflection → short Ø3 tool, finish strategy reviewed against toolmaker guidance. Burrs → magnified inspection and connector coupon. Poor datum transfer → independent check after every reclamp. Tap breakage/breakthrough → verify pilot/full-thread depth and use suitable process. Loose part → actual jaw/contact review and conservative cutting forces. Thermal face damage → protect faces and clean before pad installation.

Before machining: confirm exact machine/post, tool assemblies and lengths, stock, jaws, clamps, offsets, spindle direction, coolant, tool reach, all collisions, safe retracts and limit settings. Simulate with stock removal and full holder/fixture geometry. Have a qualified operator review setup, dry-run above stock and perform controlled first-article prove-out. This package does not claim those steps have happened.
