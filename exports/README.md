# CAD files

Start with these solid models:

| File | What it contains |
|---|---|
| [assembly.step](assembly.step) | The complete nominal enclosure: tray, lid, board envelopes and simplified screws |
| [base.step](base.step) | The custom lower tray |
| [thermal_lid.step](thermal_lid.step) | The custom cover with integral contact pedestal and fins |
| [forced_air_assembly.step](forced_air_assembly.step) | The same enclosure with a generic fan and spacers |
| [fixture_assembly.step](fixture_assembly.step) | The separate locating fixture, without the tray |

`components/` contains individual STEP solids, including simplified hardware. `meshes/` contains corresponding STL files. `profiles/` contains two DXF sections; these are not toolpaths.

Units are mm. Individual files retain assembly coordinates. STEP imports contain solids, not the editable design history: edit `cad/model.py` and `cad/parameters.json` to change the design. Threads are simplified pilots/root envelopes. See `assumptions.md` before using the models for manufacturing.

`studies/` contains the three lid alternatives from the digital comparison, each reimport-checked. They are study outputs, not replacement release parts.
