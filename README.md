# Compact electronics enclosure

A digital mechanical-design study of a small aluminum enclosure. The lid also serves as the heat sink.

The question is simple: **can an 80 × 50 mm circuit board fit inside a serviceable 100 × 70 × 25 mm enclosure, with a plausible path for removing 8 W of heat?** Board dimensions and heat load are assumptions for this exercise.

![The tray, circuit board, thermal pad and removable lid](images/exploded.png)

**[Start here: understand the design](START_HERE.md)** · **[Engineering report](report/engineering-report.pdf)** · **[Download the assembled CAD model](exports/assembly.step)**

## What was designed

- **Tray:** holds the board, provides a connector opening and attaches to an external bracket.
- **Thermal lid:** a removable aluminum cover with a raised contact block underneath and cooling fins on top.
- **Inspection fixture:** holds the tray against six locating contacts. It is a separate tooling study, not part of the enclosure.

The circuit board, chip and connector are generic envelopes. This is independent work; it does not reproduce comma.ai hardware.

## What the engineering work tells us

| Question | Result | What that result means |
|---|---|---|
| Do the modeled parts fit together? | No unintended overlap in the nominal assemblies | The chosen shapes fit at their exact CAD dimensions. Manufacturing variation and omitted wiring are separate issues. |
| Is the thermal interface controlled? | The calculated pad gap is 0.31–0.69 mm | A pad cannot be selected by nominal thickness alone; its force/compression behavior matters. |
| Can the assumed cooling be trusted? | The original passive case exceeds the temperature target; the fan case passes only under its assumed resistance | These are sensitivity calculations, not proven hardware temperatures. |
| Would more fins help? | Eight fins violate the 3 mm cutter-width constraint; taller fins exceed the 25 mm housing target | [The digital comparison](analysis/design-study.md) records actual rebuilt candidates and the tradeoffs. |
| Can someone reproduce the work? | The model, checks, figures and PDFs rebuild from source | [CI](https://github.com/gokulg846/compact-edge-enclosure/actions/workflows/validate.yml) runs the same pipeline on a clean machine. |

## Read only these three things first

1. [Start here](START_HERE.md) — what each part does, what was actually done, and how to explain it.
2. [Design comparison](analysis/design-study.md) — the latest engineering investigation and its limits.
3. [Engineering report](report/engineering-report.pdf) — the complete review package in eight pages.

For a short application attachment, use the [one-page summary](report/portfolio-summary.pdf). For dimensions, use the [drawing package](drawings/drawing-package.pdf).

## Digital scope

This project is complete as a **digital design study**, not as a qualified manufactured product. No printing, machining, physical measurement, CFD or FEA is claimed. Manufacturing and test procedures are supporting plans for a future reviewer; completing physical work is not part of the current scope.

The useful next digital questions are actual-board interface adaptation, a supplier-based thermal-pad selection, and machine-specific CAM once a real machine/tooling specification is available. Unspecified hardware is kept explicit rather than filled in with invented details.

## Run it

Python 3.12:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/rebuild.py
```

The editable geometry is [cad/model.py](cad/model.py); its dimensions are in [cad/parameters.json](cad/parameters.json). [Developer notes](docs/development.md) explain the folder structure, individual commands and generated outputs. The report is tied to a reviewed parameter snapshot and refuses to silently publish old drawing dimensions after a parameter change.

[Review notes](docs/review-notes.md) · [Executed checks](results/validation.json) · [Test output](results/tests.txt) · [Assumptions](assumptions.md) · [Manufacturing plan](manufacturing/cnc/setup-plan.md)
