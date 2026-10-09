# Build and validation notes

- Initial inspection found an empty/missing workspace and no desktop CAD/CAM installation. The project directory and isolated Python3.12 environment were created for this task.
- CadQuery/OCP solid creation, STEP exports, STL exports and nominal intersections succeeded. Final geometry was rebuilt after moving PCB supports and completing fixture mounting bores/stems.
- An early thermal unit test used exact equality for a floating-point difference; it failed (71.4 -61.4 compared to10). The independent expected value was retained and comparison changed to pytest.approx. Final results/tests.txt and tests.xml record31 passing tests.
- Initial Matplotlib 3D rendering had shading/depth-sorting artifacts. A VTK offscreen probe was unavailable on this host (process abort); no VTK rendering result is claimed. The delivered CAD mesh images use a deterministic orthographic software depth buffer (scripts/raster.py), so hidden surfaces do not show through the model.
- Matplotlib/ezdxf initially warned that their default home caches were unwritable. The full rebuild sets project-local MPLCONFIGDIR and XDG_CACHE_HOME; temporary caches are ignored by Git.
- All three PDFs were rendered with pdftoppm and visually reviewed. Text/page-count checks and DXF/SVG structural checks are automated in package_check.py. Visual review is still required after future edits.
- OpenSCAD was not installed or run. The companion source is delivered, but only the CadQuery route and its exports are validated.
- No physical measurements, prints, machining operations, CAM simulation, CFD, FEA or repeatability trial results exist. CSV measurement templates contain headers only. Synthetic data used by unit tests stays in test temporary directories and is not represented as measurement evidence.
