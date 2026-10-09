"""Generate three portfolio PDFs from actual validation outputs and CAD renders."""

import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle,
    PageBreak,
    KeepTogether,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import letter

INK = colors.HexColor("#172c45")
TEAL = colors.HexColor("#008d92")
MUTED = colors.HexColor("#53677e")
PALE = colors.HexColor("#edf3f7")
ORANGE = colors.HexColor("#d88329")
styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        name="TitleE",
        fontName="Helvetica-Bold",
        fontSize=27,
        leading=30,
        textColor=INK,
        spaceAfter=14,
    )
)
styles.add(
    ParagraphStyle(
        name="HeadingE",
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=INK,
        spaceAfter=12,
    )
)
styles.add(
    ParagraphStyle(
        name="BodyE",
        fontName="Helvetica",
        fontSize=9.5,
        leading=13.3,
        textColor=INK,
        spaceAfter=8,
    )
)
styles.add(
    ParagraphStyle(
        name="SmallE",
        fontName="Helvetica",
        fontSize=8,
        leading=10.5,
        textColor=MUTED,
        spaceAfter=6,
    )
)
styles.add(
    ParagraphStyle(
        name="CellE", fontName="Helvetica", fontSize=8, leading=10.5, textColor=INK
    )
)
styles.add(
    ParagraphStyle(
        name="TagE",
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=14,
        textColor=TEAL,
        spaceAfter=10,
    )
)
W = 528


def para(text, kind="BodyE"):
    return Paragraph(text, styles[kind])


def pic(name, maxh=260):
    path = ROOT / "images" / f"{name}.png"
    w, h = ImageReader(str(path)).getSize()
    scale = min(W / w, maxh / h)
    return Image(str(path), width=w * scale, height=h * scale)


def table(rows, widths=None):
    cells = [[para(str(v), "CellE") for v in row] for row in rows]
    t = Table(
        cells,
        colWidths=widths or [W / len(rows[0])] * len(rows[0]),
        hAlign="LEFT",
        repeatRows=1,
    )
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), PALE),
                ("TEXTCOLOR", (0, 0), (-1, 0), INK),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("LINEBELOW", (0, 0), (-1, 0), 1, TEAL),
                ("LINEBELOW", (0, 1), (-1, -1), 0.3, colors.HexColor("#d9e2ea")),
            ]
        )
    )
    return t


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(TEAL)
    canvas.rect(42, 752, 24, 3, fill=1, stroke=0)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(
        74, 750, "COMPACT ENCLOSURE    |    DIGITAL DESIGN STUDY    |    REV C"
    )
    canvas.setStrokeColor(colors.HexColor("#d9e2ea"))
    canvas.line(42, 38, 570, 38)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(
        42, 25, "Gokul Gopalakrishnan   /   Digital mechanical-design study"
    )
    canvas.drawRightString(570, 25, str(doc.page))
    canvas.restoreState()


def pdf(path, story, title):
    SimpleDocTemplate(
        str(ROOT / path),
        pagesize=letter,
        rightMargin=42,
        leftMargin=42,
        topMargin=61,
        bottomMargin=48,
        title=title,
        author="Gokul Gopalakrishnan",
    ).build(story, onFirstPage=footer, onLaterPages=footer)


def page(story, title, tag=None):
    if story:
        story.append(PageBreak())
    if tag:
        story.append(para(tag, "TagE"))
    story.append(para(title, "HeadingE"))


def check_reviewed_inputs(cad_inputs=None, analysis_inputs=None):
    """Human-reviewed drawing tables apply only to these exact input snapshots."""
    current_cad = (
        json.loads((ROOT / "cad/parameters.json").read_text())
        if cad_inputs is None
        else cad_inputs
    )
    current_analysis = (
        json.loads((ROOT / "analysis/assumptions.json").read_text())
        if analysis_inputs is None
        else analysis_inputs
    )
    approved_cad = json.loads((ROOT / "cad/revisions/rev-c.json").read_text())
    approved_analysis = json.loads(
        (ROOT / "cad/revisions/rev-c-analysis.json").read_text()
    )
    if current_cad != approved_cad or current_analysis != approved_analysis:
        raise ValueError(
            "Report inputs differ from reviewed Rev C. Review drawing tables and narrative before updating the revision snapshots."
        )


def main():
    check_reviewed_inputs()
    v = json.loads((ROOT / "results/validation.json").read_text())
    t = json.loads((ROOT / "results/thermal.json").read_text())
    x = ET.parse(ROOT / "results/tests.xml").getroot()
    suites = list(x.iter("testsuite"))
    tests = sum(int(s.attrib.get("tests", 0)) for s in suites)
    fail = sum(
        int(s.attrib.get("failures", 0)) + int(s.attrib.get("errors", 0))
        for s in suites
    )
    evidence = f"{len(v['parts'])} component export pairs checked; {tests} tests executed, {fail} failures; {sum(v[k]['pair_count'] for k in ['assembly_interference','forced_air_interference','fixture_interference'])} assembly pair checks."
    story = [
        para("MECHANICAL DESIGN STUDY", "TagE"),
        para("Compact edge-compute<br/>enclosure", "TitleE"),
        para("Packaging, thermal contact and manufacturing review", "BodyE"),
        pic("assembly", 300),
        Spacer(1, 8),
        table(
            [
                ["Envelope", "Thermal path", "Evidence"],
                [
                    "100 × 70 × 25 mm housing",
                    "Chip / pad / integral Al lid / air",
                    v["status"] + " nominal digital checks",
                ],
            ],
            [150, 210, 168],
        ),
        Spacer(1, 14),
        para(
            "A small enclosure for an assumed electronics board. The removable aluminum lid also acts as its heat sink. This report explains the geometry, the manufacturing approach, the calculations and the decisions that remain unresolved."
        ),
        para(
            "Independent demonstrator. Not a comma.ai design or replica. No physical prototype, machining, measured thermal performance, CFD or FEA is claimed.",
            "SmallE",
        ),
    ]
    page(
        story,
        "Fin alternatives and the size constraint",
        "01 / DIGITAL DESIGN COMPARISON",
    )
    study = json.loads((ROOT / "results/design-study.json").read_text())
    rows = [["Candidate", "Height / area", "Engineering consequence"]]
    for r in study["candidates"]:
        if r["status"] == "REJECTED":
            rows.append(
                [
                    "Eight fins, 6 mm",
                    "Not built",
                    "2 mm channels violate the chosen 3 mm cutter constraint.",
                ]
            )
        else:
            rows.append(
                [
                    r["candidate"].replace("_", " "),
                    f"{r['housing_height_mm']:.0f} mm / {r['exposed_area_m2']*1e4:.2f} cm²",
                    (
                        "Exceeds 25 mm target"
                        if not r["within_25mm_target"]
                        else "Within height target; nominal CAD fit checked"
                    ),
                ]
            )
    story += [
        para(
            "The tray and board stay fixed. Three fin candidates are rebuilt and checked for nominal interference; a fourth is rejected by the machining constraint. This replaces a purely subjective comparison with an executed digital experiment."
        ),
        pic("design_study", 225),
        table(rows, [165, 130, 233]),
        Spacer(1, 12),
        para(
            "More area is useful only if it can exchange heat. The area comparison assumes an isothermal lid and uniform effective convection. It excludes radiation and parallel tray/PCB paths. Wider channels can change actual airflow, which this model does not calculate."
        ),
        para(
            "Retain the six-fin, 25 mm baseline. Taller fins add area but violate the size target; eight fins require revisiting tooling. Raw inputs, results and derivation: analysis/design-study.md and results/design-study.json.",
            "SmallE",
        ),
    ]
    page(story, "The four layers of the assembly", "02 / PACKAGING")
    story += [
        pic("exploded", 325),
        table(
            [
                ["Layer / interface", "Nominal geometry"],
                [
                    "Tray",
                    "3 mm floor/wall; 17 mm rim; corner islands and integral PCB supports",
                ],
                [
                    "PCB and keepouts",
                    "80 × 50 × 1.6 at Z6; generic 20 × 20 × 2 chip; separate connector/component envelopes",
                ],
                [
                    "Thermal lid",
                    "2 mm plate at Z17..19; pedestal to Z10.1; six fins to Z25",
                ],
                [
                    "Hardware",
                    "Simplified M3 × 8 lid / M2.5 × 5 PCB screws; actual threads, fan wiring and nuts not fully modeled",
                ],
            ],
            [125, 403],
        ),
        Spacer(1, 10),
        para(
            "The integral pedestal removes loose-heatsink retention ambiguity. Removing the lid separates the thermal interface, so every service cycle requires inspecting and, where the supplier requires it, replacing the pad. All PCB dimensions must be replaced with measured interfaces before ordering metal."
        ),
    ]
    page(story, "Proposed machining sequence", "03 / MANUFACTURING")
    story += [
        pic("cnc_setups", 230),
        table(
            [
                ["Workpiece", "Stock / operation / hold"],
                [
                    "Tray",
                    "110 × 80 × 25 candidate blank. Grip sacrificial foot, pocket from top, flip into supported soft jaws, then rotate for connector opening.",
                ],
                [
                    "Thermal lid",
                    "106 × 76 × 20 blank. Machine pedestal side, flip into relieved support nest, finish 2 mm plate and 6 mm fins. Protect against bow.",
                ],
                [
                    "Tools",
                    "Candidate Ø6 rougher, Ø3 fin/connector finisher, spot/drill/tap tools. Verify reach and holder geometry in actual CAM.",
                ],
                [
                    "Print precursor",
                    "PETG fit print, underside down. Front opening may need bridge support. Printed lid is an unpowered dummy, not a heat sink.",
                ],
            ],
            [104, 424],
        ),
        Spacer(1, 12),
        para(
            "Haas VF-2 is the requested reference machine. The actual configuration, postprocessor, offsets, tool assemblies, clamps and safe simulation remain open. No G-code or production-ready toolpaths are supplied."
        ),
        para(
            "Rev B replaced cylindrical corner-boss junctions with a rounded stepped cavity and moved support holes inward. This improves nominal tool access; full swept-tool/holder collision verification is still required.",
            "SmallE",
        ),
    ]
    page(story, "The thermal-pad gap", "04 / INSPECTION & STACK-UP")
    story += [
        pic("dimensioned_section", 235),
        table(
            [
                ["Stack term", "Nominal [mm]", "Tolerance [mm]"],
                ["Base rim from A", "17.00", "±0.03"],
                ["Minus pedestal projection", "6.90", "±0.03"],
                ["Minus PCB support height", "6.00", "±0.03"],
                ["Minus PCB thickness / chip height", "1.60 / 2.00", "±0.05 / ±0.05"],
                ["Resulting gap", "0.50", "Worst case 0.31..0.69"],
            ],
            [262, 133, 133],
        ),
        Spacer(1, 10),
        para(
            "A free pad 1.00±0.05 mm would see 27.4..70.5% compression. This is not a released specification: select a supplier pressure curve, measure the real stack and revise the pedestal or shims before loading the board."
        ),
        para(
            "A/B/C locate the base. Proposed support height ±0.03 and flatness 0.05 control seating. Hole position uses an actual cylindrical zone and CMM/qualified mandrel inspection; caliper coordinates alone do not certify it. Full dimensions and acceptance methods are in the drawing package.",
            "SmallE",
        ),
    ]
    page(
        story,
        "What the thermal calculation does and does not show",
        "05 / THERMAL ENGINEERING",
    )
    story += [
        pic("thermal_sensitivity", 265),
        table(
            [
                ["At 8 W /35°C ambient", "Passive", "Forced hypothesis"],
                ["Total thermal resistance", "7.3 K/W", "3.3 K/W"],
                [
                    "Predicted case temperature",
                    "93.4°C / exceeds 80°C",
                    "61.4°C / nominally below 80°C",
                ],
                ["Uncertainty corner range", "72.6..134.2°C", "48.6..86.2°C"],
            ],
            [208, 160, 160],
        ),
        Spacer(1, 12),
        para(
            "ΔT = Q × Rθ. The network assumes 0.8 K/W pad/contact,0.5 K/W spreading, and 6.0 or 2.0 K/W effective air resistance. It estimates case temperature, not junction temperature. Bands are assumption corners, not confidence intervals."
        ),
        para(
            "The baseline exposed area is 87.33 cm². Its original 6 K/W air resistance implies an effective h of 19.1 W/(m² K); reaching the screening target through the modeled lid path needs about 26.5 W/(m² K). Neither value is established for this geometry. Full derivation: analysis/design-study.md.",
            "SmallE",
        ),
    ]
    page(story, "The separate inspection fixture", "06 / FIXTURE & VALIDATION")
    story += [
        pic("fixture", 285),
        table(
            [
                ["Constraint", "Implementation"],
                ["Z / roll / pitch", "Three noncollinear support buttons on datum A"],
                ["Y / yaw", "Two front side buttons touching datum B"],
                ["X", "One left button touching datum C"],
                [
                    "Bias / retention",
                    "Two gentle lateral screw pads near the floor; gravity seating. Not a machining clamp.",
                ],
            ],
            [115, 413],
        ),
        Spacer(1, 10),
        para(
            "Use ten complete remove-and-reinstall trials per operator, two operators, with indicators left at the original zero. Proposed per-operator and pooled range ≤0.05 mm; between-operator mean shift ≤0.03 mm. Raw templates intentionally contain no fabricated data."
        ),
        para(
            "Replaceable locator buttons can be shimmed; block mounting bores and lateral screw pilots are modeled. Selected screws, nuts, bench feet and a torque-resisting hold-down remain completion items. Do not use this inspection jig for cutting forces.",
            "SmallE",
        ),
    ]
    page(story, "Scope, evidence and how to review the work", "07 / DIGITAL REVIEW")
    story += [
        para(evidence, "TagE"),
        table(
            [
                ["Evidence", "Meaning"],
                [
                    "CAD and exports",
                    "Nominal shapes are valid, exported solids reimport, meshes close, and modeled assemblies have no unintended overlap.",
                ],
                [
                    "Executed design study",
                    "Three fin variants rebuilt; eight-fin alternative rejected for cutter clearance. Area comparison uses a stated simplified model.",
                ],
                [
                    "Tolerances and temperature",
                    "Calculated from declared dimensions and assumptions. No physical temperature or pad-pressure measurement is implied.",
                ],
                [
                    "Manufacturing and fixture",
                    "Specific review proposals. No CAM simulation, machine prove-out or repeatability result.",
                ],
            ],
            [130, 398],
        ),
        Spacer(1, 16),
        para("What changed in this review", "HeadingE"),
        para(
            "The obsolete boss-radius parameter was replaced by a real corner-island dimension. Lid-pilot material is now checked against the actual solid. The pad gap follows CAD inputs. Report generation refuses unreviewed input changes. A short reading guide explains the design before exposing the generated files."
        ),
        para("Digital scope", "HeadingE"),
        para(
            "The current deliverable is a digital mechanical-design study. Physical fabrication is outside its scope. Further digital work can adapt measured or published board interfaces, use selected pad/fan data, or add machine-specific CAM when a real setup is specified. Cooling, pad force and manufacturing capability remain open engineering questions."
        ),
        para("Read and reproduce", "HeadingE"),
        para(
            "Start with START_HERE.md, then analysis/design-study.md. CAD inputs: cad/parameters.json. Calculation assumptions: analysis/assumptions.json. Run <b>python scripts/rebuild.py</b>. AI assistance was used to develop the source and documentation; the assumptions and decisions are exposed for owner review."
        ),
        para(
            "Public context and sources: report/sources.md. No comma.ai geometry was imported. This is not an official product design.",
            "SmallE",
        ),
    ]
    pdf(
        "report/engineering-report.pdf",
        story,
        "Compact Edge-Compute Enclosure | Engineering Report",
    )
    # One-page portfolio.
    one = [
        para("DIGITAL MECHANICAL DESIGN", "TagE"),
        para("A compact enclosure<br/>with a thermal lid.", "TitleE"),
        pic("assembly", 210),
        table(
            [
                ["100 × 70 × 25 mm", "Two custom enclosure parts", "8 W thermal study"],
                [
                    "Parametric passive housing",
                    "Tray and removable lid",
                    "Passive limit exposed",
                ],
            ],
            [176, 176, 176],
        ),
        Spacer(1, 12),
        para(
            "<b>What I designed.</b> An independent generic compute enclosure with removable finned aluminum lid, integral thermal pedestal, CNC/print plans, dimensioned interfaces, an inspection fixture and rerunnable validation."
        ),
        para(
            "<b>Engineering judgment.</b> The assumed passive case reaches 93.4°C at 35°C ambient, missing an 80°C target. A fan hypothesis reaches 61.4°C but needs testing. The 0.31–0.69 mm pad-gap stack makes supplier compression data and real board measurements the next design inputs."
        ),
        para("<b>Evidence.</b> " + evidence),
        para(
            "<b>Digital comparison.</b> Three fin alternatives were rebuilt. Taller fins add area but exceed the height target; eight fins violate the selected cutter-width constraint. Cooling remains conditional on unverified heat-transfer assumptions."
        ),
        para(
            "Gokul Gopalakrishnan | Mechanical engineering / Purdue Master of Engineering Management<br/>Digital design and manufacturing planning. No completed fabrication or physical test is claimed.",
            "SmallE",
        ),
        para(
            '<link href="https://github.com/gokulg846/compact-edge-enclosure" color="#008d92">github.com/gokulg846/compact-edge-enclosure</link>',
            "SmallE",
        ),
    ]
    pdf(
        "report/portfolio-summary.pdf",
        one,
        "Compact Edge-Compute Enclosure | Portfolio Summary",
    )
    # Five drawing/operation sheets with coordinate tables.
    dr = []
    page(dr, "E01 / Base enclosure", "DRAWING PACKAGE / REV C / REVIEW ISSUE / mm")
    dr += [
        pic("base_drawing", 285),
        table(
            [
                ["Feature / nominal", "Location / requirement"],
                [
                    "Envelope 100 × 70 × 17",
                    "X/Y±0.10; height ±0.03 from datum A; exterior R3",
                ],
                [
                    "Pocket / floor",
                    "Wall 3.00 min nominal; floor 3.00±0.10; cavity R3;10 mm corner islands",
                ],
                [
                    "L1..L4 / M3 × 0.5",
                    "(6,6),(6,64),(94,6),(94,64); position Ø0.10 to A/B/C; target full engagement 6",
                ],
                [
                    "P1..P4 / M2.5 × 0.45",
                    "(18,18),(18,52),(82,18),(82,52); support top Z6.00±0.03; position Ø0.10",
                ],
                [
                    "M1..M2 / Ø4.50 +0.10/-0",
                    "(25,35),(75,35); through floor; position Ø0.20 to A/B/C",
                ],
                [
                    "Front opening",
                    "X25..41, Z7..14, R1.50; size+0.15/-0, location±0.10",
                ],
            ],
            [185, 343],
        ),
        Spacer(1, 10),
        para(
            "Datums: A underside Z0; B front Y0; C left X0. Proposed A flatness 0.05; support coplanarity 0.05. CNC 6061-T6; edge break 0.2–0.4 not modeled. Thread pilots omit real drill-point geometry: shop must verify blind depth and remaining floor.",
            "SmallE",
        ),
    ]
    page(dr, "E02 / Integral thermal lid", "CNC 6061-T6 / ALL DIMENSIONS mm")
    dr += [
        pic("thermal_lid_drawing", 270),
        table(
            [
                ["Feature", "Dimension / control"],
                ["Outer profile", "100 × 70±0.10; vertical corners R3"],
                [
                    "Mating plane D",
                    "Assembly Z17; flatness 0.05; front E / left F locate X/Y",
                ],
                ["Plate thickness", "2.00±0.05 above D; top Z19"],
                [
                    "Pedestal underside",
                    "30 × 24, R3, centered (50,35);6.90±0.03 below D; contact flatness 0.03",
                ],
                [
                    "Fin field",
                    "X35..65, Y23..47; six 2.00±0.10 fins,6.00±0.10 high;3.60 channels",
                ],
                [
                    "Four lid holes",
                    "Ø3.40 +0.10/-0 at (6,6),(6,64),(94,6),(94,64); position Ø0.15 to D/E/F",
                ],
                [
                    "Four fan holes",
                    "Ø3.40 +0.10/-0 at (34,19),(34,51),(66,19),(66,51); position Ø0.20 to D/E/F",
                ],
            ],
            [170, 358],
        ),
        Spacer(1, 10),
        para(
            "Flatness controls seating/contact; position controls simultaneous screw assembly. Inspect with calibrated height/plane tools and qualified hole-center measurement. Support the 2 mm plate while machining. No specified surface-roughness result is claimed; supplier pad requirements must set the contact finish before release.",
            "SmallE",
        ),
    ]
    page(
        dr,
        "E03 / Assembly section & fits",
        "NOMINAL ASSEMBLY / NOT A PHYSICAL MEASUREMENT",
    )
    dr += [
        pic("dimensioned_section", 245),
        table(
            [
                ["Interface", "Nominal / acceptance proposal"],
                ["Board", "80 × 50 × 1.6; lower Z6; holes Ø2.7 assumed; chip top Z9.6"],
                [
                    "TIM",
                    "Compressed gap 0.50; worst case 0.31..0.69; supplier force curve unresolved",
                ],
                [
                    "Secondary components",
                    "Top Z12.6 vs underside lid Z17 =>4.4 nominal clearance outside pedestal",
                ],
                [
                    "Connector",
                    "0.75 nominal XZ bounding-box margin; R1.5 opening corner checked in B-rep",
                ],
                [
                    "External mount",
                    "M4 head height ≤2.5 above floor Z3; reserve underside-board keepouts",
                ],
                [
                    "Fasteners",
                    "Lid M3 × 8; PCB M2.5 × 5; simplified heads/roots; threads not explicitly modeled",
                ],
                [
                    "Fan option",
                    "40 × 40 × 10 frame at Z25..35; four 6 mm spacers; reserve hardware to Z38",
                ],
            ],
            [174, 354],
        ),
        Spacer(1, 12),
        para(
            "Stack g =17.00-6.90-6.00-1.60-2.00. Worst case±0.19. M3 lid clearance radial allowance 0.20; nominal base/lid position radii consume 0.125. Printed fits require independent calibration and are not subject to CNC acceptance tolerances.",
            "SmallE",
        ),
    ]
    page(dr, "F01 / Inspection fixture", "3-2-1 / GRAVITY-SEATED BENCH INSPECTION")
    dr += [
        pic("fixture_layout", 285),
        table(
            [
                ["Element", "Coordinates / geometry"],
                ["Plate", "130 × 100 × 6; origin corner (-15,-15,-10); top Z-4"],
                ["Three support buttons", "(18,12),(82,12),(50,58);Ø6; top Z0"],
                ["Two B / one C stops", "(20,-3),(80,-3),(-3,35);Ø6; top Z5"],
                [
                    "Mounting stems",
                    "Simplified Ø3 to Z-14 through Ø3.3 plate holes; underside nuts/washers required",
                ],
                [
                    "Clamp block mounts",
                    "M4 plate pilots at (42,78),(58,78),(108,27),(108,43); blocks Ø4.5 clearance",
                ],
            ],
            [153, 375],
        ),
        Spacer(1, 10),
        para(
            "Locator coordinates±0.10 initial fabrication target; calibrate with a reference tray. Shim A buttons to≤0.02 height range before repeatability study. Horizontal M4 screw pilots drive replaceable pads; screws/feet/hold-down not fully modeled. Do not use as a machining fixture.",
            "SmallE",
        ),
    ]
    page(dr, "M01 / CNC setup reference", "PLANNING ARTIFACT / NO VERIFIED TOOLPATHS")
    dr += [
        pic("cnc_setups", 260),
        table(
            [
                ["Operation", "Review before cutting"],
                [
                    "Top pocket",
                    "Sacrificial grip 5 mm;6 mm rougher,14 mm cavity depth; maintain islands",
                ],
                [
                    "Flip / underside",
                    "Cavity support nest; confirm B/C transfer; measure A flatness after unclamping",
                ],
                [
                    "Front opening",
                    "90-degree supported nest;3 mm cutter through wall; inspect burrs/corner clearance",
                ],
                [
                    "Two-sided lid",
                    "Relieved support nest; clamp outside finished thin plate; review fin tool reach",
                ],
                [
                    "Machine prove-out",
                    "Verify exact machine/post, tools, offsets, clamps, collisions, retracts and first-article inspection",
                ],
            ],
            [170, 358],
        ),
        Spacer(1, 15),
        para(
            "These diagrams explain workholding intent; they are not to scale and do not establish safe clamping forces. The complete operation sequence and checklist are in manufacturing/cnc/setup-plan.md. A qualified shop must generate and simulate the actual CAM setup.",
            "SmallE",
        ),
    ]
    pdf(
        "drawings/drawing-package.pdf",
        dr,
        "Compact Edge-Compute Enclosure | Drawing Package",
    )
    print("Generated engineering report, one-page summary and drawing package.")


if __name__ == "__main__":
    main()
