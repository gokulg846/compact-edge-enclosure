# Working with the repository

For the engineering explanation, read [Start here](../START_HERE.md). This page is for changing or rebuilding the files.

## Sources versus generated results

| Folder | Purpose | Edit it? |
|---|---|---|
| `cad/` | Dimensions and geometric construction | Yes: parameter master and Python source. SCAD include is generated. |
| `analysis/` | Calculation inputs, methods and engineering interpretation | Yes. Inputs are declared assumptions. |
| `manufacturing/`, `fixture/` | Process proposals and tooling rationale | Yes, when changing a design decision. |
| `scripts/` | Export, rendering, reporting and validation utilities | Only to change how results are produced. |
| `tests/` | Checks for bad inputs and independently expected results | When behavior or requirements change. |
| `exports/` | Five convenient STEP models; component, mesh and profile subfolders | Generated. Change the CAD source instead. |
| `images/` | Figures produced from CAD or calculations | Generated. |
| `results/` | Executed checks, design-study results, logs and hashes | Generated, except explicitly empty future measurement templates. |
| `report/`, `drawings/` | PDFs and supporting explanations | PDFs are generated; narrative documents are editable. |

The two custom enclosure parts are the tray and thermal lid. Most of the other exported solids are simplified board/hardware envelopes. The inspection fixture is a separate tooling concept.

## Rebuild

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/rebuild.py
```

The sequence is CAD/export → SCAD include → thermal calculation → geometry validation → software tests → digital design comparison → figures → PDFs → package checks. A failed step stops the build. CI runs the same sequence on Linux.

For geometry-only work:

```bash
python scripts/build.py
python scripts/validate.py
```

For analysis-only work:

```bash
python analysis/thermal.py
python analysis/design_study.py
```

Formatting is optional for building: `python -m pip install -r requirements-dev.txt`, then `python -m black cad analysis scripts tests`.

## Parameter changes and report consistency

`cad/parameters.json` drives the model. `analysis/assumptions.json` holds heat load, resistance scenarios and tolerance assumptions. The pad-gap calculation derives its nominal dimensions from the CAD parameters.

The human-reviewed drawing tables contain a specific design revision. The PDF generator compares current CAD and analysis inputs with the reviewed Rev C snapshots. If they differ, it stops instead of silently printing stale dimensions. To issue a design revision: rebuild/check the geometry, review the narrative and tables, update the snapshots deliberately, generate the PDFs and visually inspect them. Do not bypass the check just to obtain a green build.

Useful parameters to study are fin count, fin height, board envelope and corner-island size. Not every arbitrary parameter combination is supported. Features such as actual screw-head envelopes, a real connector, fan leads and pad compression data still require explicit engineering choices.

## Optional and historical material

The OpenSCAD source is a companion, not the validated CAD path. It has not been executed here and includes a simpler fixture. Use the CadQuery source and STEP models for review. Historical Rev A/B parameter files are records of an earlier schema; they are not accepted as current configurations without migration.

Physical-test procedures and empty CSV templates are retained for completeness. They are future handoff material, not unfinished requirements for this digital-only study. No blank template is treated as a passing test.
