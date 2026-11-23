#!/usr/bin/env python3
"""Static site generator for the LAPP Muller relaunch concept.

All content lives in this file (CONTENT section). Run:

    python3 build.py

and the complete site is written to ./docs (ready for GitHub Pages).
Only the Python standard library is used.
"""
from __future__ import annotations

import html
import json
import math
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"
OUT = ROOT / "docs"
BASE_URL = "https://lappmuller.lappgroup.com/en"  # canonical target after go-live

# ---------------------------------------------------------------------------
# COMPANY FACTS (single source of truth)
# ---------------------------------------------------------------------------
CO = {
    "name": "LAPP Muller",
    "legal": "LAPP MULLER SAS",
    "street": "Z.A. du Grand Pont, 518 avenue du Caucadis",
    "zip": "83310",
    "city": "Grimaud",
    "country": "France",
    "phone": "+33 4 94 56 65 00",
    "phone_href": "+33494566500",
    "email": "contact.fr.lmg@lapp.com",
    "since": "2003",
    "hours": [("Monday to Thursday", "08:30 to 12:30 and 13:30 to 17:00"),
              ("Friday", "08:30 to 12:30 and 13:30 to 15:30")],
    "linkedin": "https://www.linkedin.com/company/lapp-muller/",
    "youtube": "https://www.youtube.com/@LAPPGroup",
    "group": "https://www.lappgroup.com",
    "fr_site": "https://lappmuller.lappgroup.com/",
}

CDN = "https://t3.lappcdn.com/fileadmin/DAM/Lapp_Muller"

# ---------------------------------------------------------------------------
# DRAWINGS: cable cross-sections are the visual signature of the site
# ---------------------------------------------------------------------------

def cross_section(conductors=3, fibres=0, armour=True, screen=False, pairs=0,
                  size=420, callouts=False, label="Cable cross-section", cls="xsection"):
    """Return an inline SVG of a cable cross-section.

    The layout is computed, so every industry gets its own drawing.
    """
    w = 560 if callouts else size
    h = size
    cx = 200 if callouts else size / 2
    cy = h / 2
    R = (h / 2) - 22
    parts = []
    # outer sheath
    parts.append(f'<circle class="ring" cx="{cx}" cy="{cy}" r="{R:.1f}" fill="#fff" stroke="#1c2b33" stroke-width="3"/>')
    r_arm = R * 0.88
    if armour:
        parts.append(f'<circle class="ring" cx="{cx}" cy="{cy}" r="{r_arm:.1f}" fill="none" stroke="#5b7480" stroke-width="7" stroke-dasharray="3 5"/>')
    r_in = R * 0.79
    parts.append(f'<circle class="ring" cx="{cx}" cy="{cy}" r="{r_in:.1f}" fill="#f2f4f3" stroke="#1c2b33" stroke-width="1.5"/>')
    if screen:
        parts.append(f'<circle class="ring" cx="{cx}" cy="{cy}" r="{r_in*0.96:.1f}" fill="none" stroke="#c0703f" stroke-width="1" stroke-dasharray="1 2"/>')

    core = []
    # central strength member
    r_c = R * 0.13
    core.append(f'<circle cx="{cx}" cy="{cy}" r="{r_c:.1f}" fill="#5b7480"/>')
    core.append(f'<circle cx="{cx}" cy="{cy}" r="{r_c*0.45:.1f}" fill="#c7d0d2"/>')
    # conductors on a pitch circle
    elements = [("c", i) for i in range(conductors)] + [("f", i) for i in range(fibres)] + [("p", i) for i in range(pairs)]
    n = max(len(elements), 1)
    pitch = R * 0.46
    r_el = min(R * 0.2, pitch * math.sin(math.pi / n) * 0.86) if n > 1 else R * 0.22
    for k, (kind, _) in enumerate(elements):
        a = -math.pi / 2 + 2 * math.pi * k / n
        x = cx + pitch * math.cos(a)
        y = cy + pitch * math.sin(a)
        if kind == "c":
            core.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r_el:.1f}" fill="#fff" stroke="#1c2b33" stroke-width="1.5"/>')
            core.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r_el*0.66:.1f}" fill="#c0703f"/>')
            # strands
            for s in range(6):
                sa = 2 * math.pi * s / 6
                core.append(f'<circle cx="{x + r_el*0.36*math.cos(sa):.1f}" cy="{y + r_el*0.36*math.sin(sa):.1f}" r="{r_el*0.17:.1f}" fill="#d98b5c"/>')
        elif kind == "f":
            core.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r_el*0.8:.1f}" fill="#fff" stroke="#1c2b33" stroke-width="1.5"/>')
            for s in range(3):
                sa = 2 * math.pi * s / 3
                core.append(f'<circle cx="{x + r_el*0.3*math.cos(sa):.1f}" cy="{y + r_el*0.3*math.sin(sa):.1f}" r="{r_el*0.13:.1f}" fill="#f39200"/>')
        else:  # twisted pair
            core.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r_el*0.82:.1f}" fill="#fff" stroke="#1c2b33" stroke-width="1.2"/>')
            for s in (-1, 1):
                core.append(f'<circle cx="{x + s*r_el*0.33:.1f}" cy="{y:.1f}" r="{r_el*0.3:.1f}" fill="#c0703f" stroke="#1c2b33" stroke-width=".8"/>')
    parts.append('<g class="core">' + "".join(core) + "</g>")

    if callouts:
        labels = [
            (R, -40, ["Outer sheath", "PUR, PE or halogen-free"]),
            (r_arm, -12, ["Armour or aramid braid", "for tension and impact"]),
            (pitch, 20, ["Power and signal", "conductors, any section"]),
            (r_c, 52, ["Strength member", "or fibre unit at the centre"]),
        ]
        ys = [70, 160, 250, 340]
        for (rad, ang, lines), ly in zip(labels, ys):
            a = math.radians(ang)
            px, py = cx + rad * math.cos(a), cy + rad * math.sin(a)
            lx = 392
            parts.append(
                f'<g class="callout"><circle class="dot" cx="{px:.1f}" cy="{py:.1f}" r="3.5"/>'
                f'<path class="leader" d="M{px:.1f} {py:.1f} L{lx-12} {ly} L{lx-2} {ly}"/>'
                f'<text x="{lx}" y="{ly-4}"><tspan font-weight="700">{lines[0]}</tspan>'
                f'<tspan x="{lx}" dy="17" fill="#3d4f59">{lines[1]}</tspan></text></g>')

    return (f'<svg class="{cls}" viewBox="0 0 {w} {h}" role="img" aria-label="{html.escape(label)}" '
            f'xmlns="http://www.w3.org/2000/svg">' + "".join(parts) + "</svg>")


def mini(cfg, label):
    return cross_section(size=120, cls="mini", label=label, **cfg)


def cable_run(kind="tow"):
    """Wide line illustration used for case study headers."""
    if kind == "tow":
        body = ('<path d="M40 70 h150 a20 20 0 0 1 0 40 h-150 a20 20 0 0 1 0-40z" fill="#3d4f59"/>'
                '<path d="M190 90 C 320 90, 360 160, 520 150 S 760 120, 880 170" fill="none" stroke="#f39200" stroke-width="5"/>'
                '<rect x="870" y="160" width="60" height="18" rx="9" fill="#c7d0d2"/>')
    else:
        body = ('<path d="M0 170 Q 240 150 480 172 T 960 160 V220 H0z" fill="#3d4f59"/>'
                '<rect x="420" y="120" width="120" height="44" rx="6" fill="#c7d0d2"/>'
                '<path d="M480 120 C 480 60, 560 40, 640 30 S 860 20, 960 24" fill="none" stroke="#f39200" stroke-width="5"/>')
    return f'<svg viewBox="0 0 960 220" preserveAspectRatio="xMidYMid slice" aria-hidden="true" xmlns="http://www.w3.org/2000/svg">{body}</svg>'


# ---------------------------------------------------------------------------
# CONTENT
# ---------------------------------------------------------------------------
INDUSTRIES = [
    {
        "slug": "defence",
        "name": "Defence and naval",
        "short": "Tow cables, umbilicals and power cables for submarines, surface ships and subsea systems.",
        "lead": "Cables for naval platforms that have to survive pressure, repeated bending over sheaves and decades in service, built to your specification and qualified with you.",
        "svg": dict(conductors=4, fibres=2, armour=True, screen=True),
        "apps": ["Dynamic outboard tow cables for submarines", "Umbilicals for subsea burial and mine countermeasure systems",
                 "Ship power, control and instrumentation cables", "Sonar and hydrophone cables",
                 "Cable assemblies with connectors and terminations"],
        "why": ["Hybrid designs that combine power, signal, fibre and strength members in one cable",
                "Small series and one-off lengths for qualification and prototypes",
                "Programmes handled under confidentiality agreements",
                "Certification organised with the certifying body your programme requires"],
        "spec": [("Construction", "Hybrid: electrical, optical, pneumatic, hydraulic, strength members"),
                 ("Mechanical", "Dynamic bending, torsion, high tensile load, crush resistance"),
                 ("Environment", "Seawater, hydrostatic pressure, UV, hydrocarbons"),
                 ("Lengths", "From a few metres for prototypes to full deployment lengths")],
        "cases": ["submarine-tow-cable", "elodie-burial-machine"],
    },
    {
        "slug": "electrification",
        "name": "Electrification",
        "short": "Shore power cables for ports and 400 Hz ground power cables for aircraft.",
        "lead": "Port and airport electrification needs cables that are handled every day, dragged across quays and aprons, and still deliver safe power. That is the brief for STS-Flex and MULL'AIR 400.",
        "svg": dict(conductors=4, pairs=2, armour=False, screen=True),
        "apps": ["Shore power and charging for all types of vessels", "400 Hz ground power for parked aircraft",
                 "Reeling and festoon systems", "Cable sets with plugs for port and apron equipment"],
        "why": ["Helps ports and operators meet EU requirements for shore-side electricity",
                "Flexible, abrasion-resistant sheaths for daily handling",
                "Complete sets: cable, connectors and terminations from one supplier",
                "Custom versions alongside the standard ranges"],
        "spec": [("STS-Flex", "1 kV shore power or charging cable for vessels"),
                 ("MULL'AIR 400", "400 Hz ground power cable range for aircraft"),
                 ("Handling", "High flexibility, reeling, drag and abrasion resistance"),
                 ("Options", "Custom cross-sections, lengths and terminations on request")],
        "products": [
            ("STS-Flex 1 kV", "Shore power and charging cable for vessels that connect to quay-side power.",
             f"{CDN}/Brochures/STSflex-1kV-LAPPMuller_EN_09-2023_1__1_.pdf", "Download the STS-Flex data sheet (PDF)"),
            ("MULL'AIR 400", "Ground power cable range for supplying 400 Hz to aircraft on the stand.",
             f"{CDN}/Brochures/flyer_Version_finale.pdf", "Download the MULL'AIR 400 flyer (PDF)"),
        ],
        "cases": [],
    },
    {
        "slug": "nuclear",
        "name": "Nuclear",
        "short": "Radiation-resistant, halogen-free cables for power plants, reprocessing and research.",
        "lead": "Our radiation-resistant cables are installed in EPR reactors and in operating plants in France and abroad, as well as at reprocessing and research sites.",
        "svg": dict(conductors=3, pairs=3, armour=True, screen=True),
        "apps": ["Power, control and command cables for moving bridges and handling equipment",
                 "Drag-chain cables for remote handling", "Instrumentation cables in controlled areas",
                 "Composite cables with aramid reinforcement"],
        "why": ["Halogen-free and fire-retardant (C1/SH) constructions",
                "Designs made to French nuclear specifications such as SGN",
                "Experience on EPR projects in Finland, France and the UK",
                "Documentation and traceability for each delivery"],
        "spec": [("Typical rating", "Up to 600 V"),
                 ("Temperature", "-20 °C to +80 °C (typical range)"),
                 ("Fire behaviour", "Halogen-free, C1/SH fire retardant"),
                 ("Reference sites", "EPR projects, EDF 900 and 1300 MW plants, ORANO La Hague, CERN")],
        "cases": [],
    },
    {
        "slug": "marine-subsea",
        "name": "Marine and subsea",
        "short": "ROV tethers, umbilicals, floating cables and sonar cables for the underwater world.",
        "lead": "A complete range of watertight cables for ROVs, underwater machines and offshore equipment, from neutrally buoyant tethers to armoured lift cables.",
        "svg": dict(conductors=3, fibres=3, armour=True),
        "apps": ["Floating ROV tethers with optical fibres or coaxials", "Main lift cables for ROVs",
                 "Umbilicals with power, video, command and hoses", "Diving bell and diver umbilicals",
                 "Mooring line and rig mast cables", "Seafarm, fishing and pool robot cables"],
        "why": ["Buoyancy, weight in water and breaking load tuned to your vehicle",
                "Watertight constructions in special polyolefin compounds",
                "Connectors, terminations and fittings supplied with the cable",
                "Thousands of proven subsea designs to start from"],
        "spec": [("Elements", "Power, control, signal, fibre optics, coaxials, hoses, strength members"),
                 ("Buoyancy", "Floating, neutral or heavy, defined per project"),
                 ("Environment", "Seawater, pressure, abrasion, UV"),
                 ("Catalogue", "Marine and underwater cable solutions (PDF)")],
        "cases": ["elodie-burial-machine"],
    },
    {
        "slug": "oil-gas",
        "name": "Oil and gas",
        "short": "Offshore umbilicals and onshore instrumentation, control and power cables.",
        "lead": "Together with our sister company Camuna Cavi, we supply cables for offshore operations and for onshore process plants, including extreme-temperature series.",
        "svg": dict(conductors=2, pairs=4, armour=True, screen=True),
        "apps": ["Offshore umbilicals and floating power and signal cables", "Onshore instrumentation and control cables",
                 "Power and thermocouple cables", "Data and bus cables in copper and fibre"],
        "why": ["Resistant to hydrocarbons, drilling muds and extreme climates",
                "Selection lists for fast specification of standard needs",
                "Custom designs when the standard range does not fit",
                "Offshore and onshore from the LAPP Group"],
        "spec": [("Offshore", "Umbilicals, floating cables, sonar and lift cables"),
                 ("Onshore", "Instrumentation, control, power, thermocouple, data"),
                 ("Environment", "Hydrocarbons, mud, low and high temperatures"),
                 ("Partner", "Camuna Cavi, LAPP Group")],
        "cases": [],
    },
    {
        "slug": "robotics-automation",
        "name": "Robotics and automation",
        "short": "Extra-flexible torsion and drag-chain cables for robots and moving machines.",
        "lead": "Robot arms and drag chains move millions of times. Our extra-flexible cables are built with class 6 conductors and special polymers to keep up.",
        "svg": dict(conductors=6, pairs=2, armour=False, screen=True),
        "apps": ["Bending and torsion cables for industrial robots", "Drag-chain power and control cables",
                 "Miniaturised cables for compact automation", "Screened signal cables for motion control"],
        "why": ["Extra-flexible class 6 conductors to IEC 60228 and NF C 32-013",
                "Tinned copper braid screens with high optical coverage",
                "Miniaturised designs in special polymers",
                "Screened or unscreened, to your motion profile"],
        "spec": [("Rated voltage", "300 V to 1 kV"),
                 ("Temperature", "-30 °C to +80 °C (typical range)"),
                 ("Conductors", "Extra-flexible plain or tinned copper, class 6"),
                 ("Movement", "Bending, torsion, drag chain")],
        "cases": [],
    },
    {
        "slug": "medical",
        "name": "Medical",
        "short": "Cables for imaging, life support, therapy and surgical robots.",
        "lead": "Medical devices need cables that are small, flexible, reliable and easy to clean. We build them for scanners, ventilators, medical lasers and surgical robots.",
        "svg": dict(conductors=4, fibres=1, pairs=2, armour=False, screen=True),
        "apps": ["Imaging and scanner cables", "Intensive-care ventilator cables",
                 "Medical laser and therapy equipment", "Surgical robot cables"],
        "why": ["Miniaturised, very flexible constructions",
                "Materials chosen for cleaning and skin contact requirements",
                "Prototype quantities for device development",
                "Stable series supply once your device is approved"],
        "spec": [("Construction", "Hybrid power, signal, coaxial and fibre"),
                 ("Size", "Miniaturised cross-sections"),
                 ("Materials", "Selected per device and cleaning regime"),
                 ("Quantities", "Prototypes to series")],
        "cases": [],
    },
    {
        "slug": "harsh-environments",
        "name": "Mountain, handling and inspection",
        "short": "Reeling, flat, mountain, fibre and inspection cables for extreme duty.",
        "lead": "For cables under high mechanical stress, we build strong designs that resist abrasion and extreme climatic and chemical conditions, from ski lifts to pipe inspection.",
        "svg": dict(conductors=5, fibres=1, armour=True),
        "apps": ["Mountain cables for lifts and snow equipment", "Reeling and flat cables for handling equipment",
                 "Fibre optic cables for harsh routes", "Inspection cables for cameras and crawlers"],
        "why": ["High tensile strength with aramid or steel reinforcement",
                "Abrasion, cold and chemical resistant sheaths",
                "Hybrid copper and fibre in one cable",
                "Any length, including short runs"],
        "spec": [("Mechanical", "Tension, abrasion, reeling, crush"),
                 ("Climate", "Cold, UV, moisture"),
                 ("Elements", "Power, signal, fibre, strength members"),
                 ("Lengths", "Short lengths to long reels")],
        "cases": [],
    },
]
IND = {i["slug"]: i for i in INDUSTRIES}

CASES = [
    {
        "slug": "submarine-tow-cable",
        "title": "Dynamic outboard tow cable for a submarine",
        "industry": "defence",
        "art": "tow",
        "summary": "A towed cable that is paid out, recovered and bent over sheaves again and again, while carrying power and data under pressure.",
        "facts": [("Sector", "Naval defence"), ("Cable type", "Dynamic hybrid tow cable"), ("Scope", "Design, qualification, production")],
        "challenge": "The customer needed an outboard tow cable that could be deployed and recovered from a submarine many times without losing signal integrity. The cable had to resist hydrostatic pressure, high tensile load and continuous bending over the handling system.",
        "approach": "Our engineers combined conductors, signal elements and a strength member in one compact construction, chose sheath materials for seawater and abrasion, and validated the design with the customer before series production.",
        "result": "A cable built for the exact handling system and mission profile, supplied in the lengths the programme needed.",
    },
    {
        "slug": "elodie-burial-machine",
        "title": "Umbilical for the ELODIE burial machine",
        "industry": "marine-subsea",
        "art": "burial",
        "summary": "An umbilical that powers and controls a subsea burial machine working on the seabed.",
        "facts": [("Sector", "Subsea and defence"), ("Cable type", "Subsea umbilical"), ("Scope", "Custom design and supply")],
        "challenge": "A burial machine working on the seabed needs power, control and data from the surface vessel through one cable that is dragged, lifted and exposed to abrasion and seawater for long periods.",
        "approach": "We designed an umbilical that brings the required electrical and signal functions together with the mechanical strength for lifting and towing, and matched it to the machine's handling equipment.",
        "result": "One umbilical for power, control and data, sized for the machine and the vessel it operates from.",
    },
]
CASE = {c["slug"]: c for c in CASES}

PROCESS = [
    ("Tell us the job", "Share your application, environment and constraints online or with our sales team."),
    ("Engineering study", "Our design office proposes a construction, materials and a drawing."),
    ("Prototype", "We produce a sample or short length so you can test it in real conditions."),
    ("Qualification", "Tests and certification with the body your project requires."),
    ("Production", "Manufacturing in Grimaud, in the length and quantity you need."),
    ("Delivery and support", "Delivery with documentation, and support for repeat orders."),
]

DOWNLOADS = [
    ("Catalogues and brochures", [
        ("General brochure (French)", "Overview of LAPP Muller and its markets", "https://lappmuller.lappgroup.com/fileadmin/DAM/Lapp_Oil_Gas/brochures/Brochure_g%C3%A9nerale_FR.pdf"),
        ("Marine and underwater cable solutions", "Catalogue: ROV, umbilicals, floating and lift cables", f"{CDN}/asm_anglais_LIGHT.pdf"),
    ]),
    ("Data sheets", [
        ("STS-Flex 1 kV", "Shore power and charging cable for vessels", f"{CDN}/Brochures/STSflex-1kV-LAPPMuller_EN_09-2023_1__1_.pdf"),
        ("MULL'AIR 400", "400 Hz ground power cable range for aircraft", f"{CDN}/Brochures/flyer_Version_finale.pdf"),
    ]),
    ("Commercial documents", [
        ("Terms of trade", "General terms and conditions of sale", "https://lappmuller.lappgroup.com/en/terms-of-trade.html"),
        ("Needs analysis sheet", "Prefer paper? Use the online project request instead, it covers the same questions.", "start-a-project.html"),
    ]),
]

# ---------------------------------------------------------------------------
# LAYOUT
# ---------------------------------------------------------------------------

def rel(depth: int) -> str:
    return "../" * depth


def header(p: str, section: str) -> str:
    mega = "".join(
        f'<a href="{p}industries/{i["slug"]}.html"><strong>{i["name"]}</strong><span>{i["short"]}</span></a>'
        for i in INDUSTRIES)
    def item(key, href, label):
        cur = ' aria-current="page"' if section == key else ""
        return f'<li><a href="{p}{href}"{cur}>{label}</a></li>'
    ind_cls = ' class="nav-item is-section"' if section == "industries" else ' class="nav-item"'
    return f"""
<a class="skip" href="#main">Skip to content</a>
<div class="concept-bar"><div class="wrap">Redesign concept for review. Not the official LAPP Muller website.</div></div>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="{p}index.html" aria-label="LAPP Muller home"><span class="brand-lapp">LAPP</span><span class="brand-muller">MULLER</span></a>
    <button class="menu-toggle" aria-expanded="false" aria-controls="site-nav">Menu</button>
    <nav class="nav" id="site-nav" aria-label="Main">
      <ul>
        <li{ind_cls}>
          <button class="nav-trigger" aria-expanded="false" aria-controls="mega-industries">Industries
            <svg class="chev" viewBox="0 0 10 10" aria-hidden="true"><path d="M1 3l4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.6"/></svg></button>
          <div class="mega" id="mega-industries">{mega}<a class="mega-all" href="{p}industries/index.html"><strong>All industries</strong></a></div>
        </li>
        {item("capabilities", "capabilities.html", "Capabilities")}
        {item("cases", "case-studies/index.html", "Case studies")}
        {item("about", "about.html", "About us")}
        {item("careers", "careers.html", "Careers")}
        {item("downloads", "downloads.html", "Downloads")}
        {item("contact", "contact.html", "Contact")}
      </ul>
      <div class="lang"><span class="visually-hidden">Language: </span><a href="#" aria-current="true">EN</a> <a href="{CO['fr_site']}" hreflang="fr" lang="fr">FR</a></div>
      <a class="btn btn-primary" href="{p}start-a-project.html">Start a project</a>
    </nav>
  </div>
</header>"""


def footer(p: str) -> str:
    ind = "".join(f'<li><a href="{p}industries/{i["slug"]}.html">{i["name"]}</a></li>' for i in INDUSTRIES[:6])
    return f"""
<footer class="site-footer">
  <div class="wrap">
    <div class="title-block">
      <div>
        <div class="footer-brand"><span class="brand-lapp">LAPP</span><span class="brand-muller">MULLER</span></div>
        <address>{CO['legal']}<br>{CO['street']}<br>{CO['zip']} {CO['city']}, {CO['country']}</address>
        <p style="margin-top:.75rem"><a href="tel:{CO['phone_href']}">{CO['phone']}</a><br><a href="mailto:{CO['email']}">{CO['email']}</a></p>
      </div>
      <div><h2>Industries</h2><ul>{ind}<li><a href="{p}industries/index.html">All industries</a></li></ul></div>
      <div><h2>Company</h2><ul>
        <li><a href="{p}about.html">About us</a></li>
        <li><a href="{p}about.html#sustainability">Sustainability</a></li>
        <li><a href="{p}about.html#compliance">Compliance</a></li>
        <li><a href="{p}careers.html">Careers</a></li>
        <li><a href="{p}case-studies/index.html">Case studies</a></li></ul></div>
      <div><h2>Work with us</h2><ul>
        <li><a href="{p}start-a-project.html">Start a project</a></li>
        <li><a href="{p}contact.html">Contact and opening hours</a></li>
        <li><a href="{p}downloads.html">Downloads</a></li>
        <li><a href="{CO['linkedin']}" rel="noopener">LinkedIn</a></li>
        <li><a href="{CO['youtube']}" rel="noopener">YouTube</a></li></ul></div>
    </div>
    <div class="footer-legal">
      <span>© 2026 {CO['legal']}, a company of the <a href="{CO['group']}" rel="noopener">LAPP Group</a></span>
      <ul>
        <li><a href="{p}legal.html#notice">Legal notice</a></li>
        <li><a href="{p}legal.html#privacy">Privacy policy</a></li>
        <li><a href="{p}downloads.html#commercial-documents">Terms of trade</a></li>
        <li><button type="button" data-cookie-settings>Cookie settings</button></li>
        <li><a href="{p}sitemap.xml">Sitemap</a></li>
      </ul>
    </div>
  </div>
</footer>"""


def cta_band(p: str, title="Have a cable that does not exist yet?",
             text="Describe the application in a few minutes. An engineer replies within two working days.",
             industry: str | None = None) -> str:
    q = f"?industry={industry}" if industry else ""
    return f"""
<section class="cta-band" aria-labelledby="cta-title">
  <div class="wrap">
    <div><h2 id="cta-title">{title}</h2><p>{text}</p></div>
    <div class="btn-row"><a class="btn btn-dark" href="{p}start-a-project.html{q}">Start a project</a>
    <a class="btn btn-ghost" href="tel:{CO['phone_href']}">Call {CO['phone']}</a></div>
  </div>
</section>"""


def crumbs(p: str, trail: list[tuple[str, str | None]]) -> str:
    items = [f'<li><a href="{p}index.html">Home</a></li>']
    for label, href in trail:
        items.append(f'<li><a href="{p}{href}">{label}</a></li>' if href else f'<li aria-current="page">{label}</li>')
    return f'<nav class="crumbs" aria-label="Breadcrumb"><ol>{"".join(items)}</ol></nav>'


def page_hero(p, trail, h1, lead, art="", extra=""):
    cls = "page-hero" if art else "page-hero no-art"
    return f"""
<section class="{cls}">
  <div class="wrap">
    <div>{crumbs(p, trail)}<h1>{h1}</h1><p class="lead">{lead}</p>{extra}</div>
    {art}
  </div>
</section>"""


PAGES: list[str] = []


def write_page(path: str, title: str, description: str, body: str, section: str = "", jsonld: dict | None = None):
    depth = path.count("/")
    p = rel(depth)
    canonical = f"{BASE_URL}/{path}".replace("/index.html", "/")
    ld = f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>' if jsonld else ""
    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="en" href="{canonical}">
<link rel="alternate" hreflang="fr" href="{CO['fr_site']}">
<meta property="og:type" content="website">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(description)}">
<meta property="og:url" content="{canonical}">
<meta name="theme-color" content="#1c2b33">
<link rel="icon" href="{p}assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{p}assets/css/main.css">
{ld}
</head>
<body>
{header(p, section)}
<main id="main">
{body.replace("{p}", p)}
</main>
{footer(p)}
<script src="{p}assets/js/main.js" defer></script>
</body>
</html>
"""
    target = OUT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(doc, encoding="utf-8")
    if path != "404.html":
        PAGES.append(path)


# ---------------------------------------------------------------------------
# PAGES
# ---------------------------------------------------------------------------

def industry_tiles(featured=False):
    lis = "".join(
        f'<li><a href="{{p}}industries/{i["slug"]}.html">{mini(i["svg"], i["name"] + " cable cross-section")}'
        f'<h3>{i["name"]}</h3><p>{i["short"]}</p></a></li>' for i in INDUSTRIES)
    return f'<ul class="industry-list{" featured" if featured else ""}">{lis}</ul>'


def process_list():
    return '<ol class="process">' + "".join(f"<li><h3>{t}</h3><p>{d}</p></li>" for t, d in PROCESS) + "</ol>"


def case_cards(slugs=None):
    items = [CASE[s] for s in slugs] if slugs else CASES
    return '<div class="cases">' + "".join(
        f'<a class="case" href="{{p}}case-studies/{c["slug"]}.html"><div class="case-art">{cable_run(c["art"])}</div>'
        f'<div class="case-body"><p class="tag">{IND[c["industry"]]["name"]}</p><h3>{c["title"]}</h3><p>{c["summary"]}</p></div></a>'
        for c in items) + "</div>"


def build_home():
    hero_svg = cross_section(conductors=3, fibres=2, armour=True, screen=True, callouts=True,
                             label="Cross-section of a hybrid special cable with sheath, armour, conductors, fibres and strength member")
    body = f"""
<section class="hero">
  <div class="wrap">
    <div>
      <h1>Cables built for one job, in any length.</h1>
      <p class="lead">LAPP Muller designs and manufactures special cables for defence, nuclear, subsea and electrification projects, from a single prototype metre to full series.</p>
      <div class="btn-row"><a class="btn btn-primary" href="{{p}}start-a-project.html">Start a project</a>
      <a class="btn btn-ghost" href="{{p}}industries/index.html">See industries</a></div>
      <dl class="hero-facts">
        <div><dt>LAPP Group technology centre</dt><dd>Since {CO['since']}</dd></div>
        <div><dt>special cable designs on record</dt><dd>~60,000</dd></div>
        <div><dt>minimum order length</dt><dd>None</dd></div>
      </dl>
    </div>
    {hero_svg}
  </div>
</section>

<section class="section" aria-labelledby="ind-title">
  <div class="wrap">
    <div class="section-head">
      <h2 id="ind-title">Where our cables work</h2>
      <p class="muted">Every cable starts from your application. Choose your industry to see typical designs, reference projects and specifications.</p>
    </div>
    {industry_tiles(featured=True)}
  </div>
</section>

<section class="section section-dark on-dark" aria-labelledby="ref-title">
  <div class="wrap refs">
    <div>
      <h2 id="ref-title">Trusted where failure is not an option</h2>
      <p class="lead">Our radiation-resistant and subsea cables are installed at sites with the strictest requirements.</p>
      <div class="btn-row"><a class="btn btn-ghost" href="{{p}}case-studies/index.html">Read the case studies</a></div>
    </div>
    <ul class="ref-list">
      <li>EPR reactors<span>Finland, France and the United Kingdom</span></li>
      <li>EDF power plants<span>900 and 1300 MW units</span></li>
      <li>ORANO La Hague<span>Nuclear fuel reprocessing</span></li>
      <li>CERN<span>Research infrastructure</span></li>
      <li>Naval programmes<span>Tow cables and umbilicals</span></li>
      <li>Ports and airports<span>Shore power and 400 Hz ground power</span></li>
    </ul>
  </div>
</section>

<section class="section" aria-labelledby="proc-title">
  <div class="wrap">
    <div class="section-head">
      <h2 id="proc-title">From brief to delivery in six steps</h2>
      <p class="muted">One project team in Grimaud follows your cable from the first question to repeat orders.</p>
    </div>
    {process_list()}
  </div>
</section>

<section class="section section-paper" aria-labelledby="why-title">
  <div class="wrap split">
    <div>
      <h2 id="why-title">Why engineers come to us</h2>
      <p class="lead">Standard catalogues stop where your application starts. Our design office, R&amp;D and production sit under one roof, so a special cable is our normal job.</p>
      <p><a href="{{p}}capabilities.html">See our capabilities</a></p>
    </div>
    <ul class="checklist">
      <li>Fully custom constructions: electrical, optical, pneumatic, hydraulic and strength elements in one cable</li>
      <li>Short lengths and prototypes, from miniaturised to large cross-sections</li>
      <li>Short lead times thanks to streamlined processes</li>
      <li>Connectors, terminations and cable equipment supplied ready to install</li>
      <li>Certification with the body your project requires</li>
      <li>The resources of the LAPP Group behind every order</li>
    </ul>
  </div>
</section>

<section class="section" aria-labelledby="case-title">
  <div class="wrap">
    <div class="section-head">
      <h2 id="case-title">Recent projects</h2>
      <p class="muted">How we solved two demanding subsea and naval briefs.</p>
    </div>
    {case_cards()}
  </div>
</section>
{cta_band("{p}")}
"""
    ld = {
        "@context": "https://schema.org", "@type": "Organization", "name": CO["name"], "legalName": CO["legal"],
        "url": BASE_URL + "/", "email": CO["email"], "telephone": CO["phone"], "foundingDate": CO["since"],
        "parentOrganization": {"@type": "Organization", "name": "LAPP Group", "url": CO["group"]},
        "address": {"@type": "PostalAddress", "streetAddress": CO["street"], "postalCode": CO["zip"],
                    "addressLocality": CO["city"], "addressCountry": "FR"},
        "sameAs": [CO["linkedin"], CO["youtube"]],
    }
    write_page("index.html", "LAPP Muller: custom special cables for extreme environments",
               "Custom special cables for defence, nuclear, subsea and electrification, made in Grimaud, France. Any length, from prototype to series.",
               body, "home", ld)


def build_industries():
    body = f"""
{page_hero("{p}", [("Industries", None)], "Industries we serve",
           "Eight fields, one approach: we start from the conditions your cable will face and design backwards from there.")}
<section class="section"><div class="wrap">{industry_tiles()}</div></section>
<section class="section section-paper"><div class="wrap split">
  <div><h2>Not on the list?</h2><p class="lead">Most of our projects begin with a question nobody has asked before. If your cable has to survive something unusual, we want to hear about it.</p></div>
  <div class="aside-box"><h3>What helps us answer fast</h3><ul class="checklist">
    <li>Where the cable is installed and how it moves</li><li>Electrical, optical or fluid functions it carries</li>
    <li>Temperature, media and standards to meet</li><li>Length, quantity and target date</li></ul>
    <div class="btn-row"><a class="btn btn-primary" href="{{p}}start-a-project.html">Start a project</a></div></div>
</div></section>
{cta_band("{p}")}
"""
    write_page("industries/index.html", "Industries: defence, nuclear, subsea, electrification | LAPP Muller",
               "Special cables for defence, electrification, nuclear, marine and subsea, oil and gas, robotics, medical and harsh environments.",
               body, "industries")

    for i in INDUSTRIES:
        apps = "".join(f"<li>{a}</li>" for a in i["apps"])
        why = "".join(f"<li>{w}</li>" for w in i["why"])
        rows = "".join(f'<tr><th scope="row">{k}</th><td>{v}</td></tr>' for k, v in i["spec"])
        products = ""
        if i.get("products"):
            products = '<section class="section section-paper" aria-labelledby="prod-title"><div class="wrap"><h2 id="prod-title">Product ranges</h2><div class="products">' + "".join(
                f'<article class="product"><h3>{n}</h3><p>{d}</p><a href="{u}" rel="noopener">{l}</a></article>' for n, d, u, l in i["products"]) + "</div></div></section>"
        cases = ""
        if i["cases"]:
            cases = f'<section class="section" aria-labelledby="c-title"><div class="wrap"><h2 id="c-title">Case studies</h2>{case_cards(i["cases"])}</div></section>'
        others = [o for o in INDUSTRIES if o["slug"] != i["slug"]][:4]
        other_links = " ".join(f'<a href="{{p}}industries/{o["slug"]}.html">{o["name"]}</a>,' for o in others).rstrip(",")
        art = cross_section(size=300, label=f"Example cross-section of a {i['name'].lower()} cable", **i["svg"])
        body = f"""
{page_hero("{p}", [("Industries", "industries/index.html"), (i["name"], None)], i["name"] + " cables", i["lead"], art,
           f'<div class="btn-row"><a class="btn btn-primary" href="{{p}}start-a-project.html?industry={i["slug"]}">Request a design</a></div>')}
<section class="section"><div class="wrap split wide-left">
  <div class="prose">
    <h2>Typical applications</h2><ul>{apps}</ul>
    <h2>What you get</h2><ul class="checklist">{why}</ul>
  </div>
  <div>
    <table class="spec"><caption>Design envelope</caption><tbody>{rows}</tbody></table>
    <p class="spec-note">Indicative values. Each cable is specified for your project and confirmed in a drawing and data sheet.</p>
  </div>
</div></section>
{products}
{cases}
<section class="section section-paper"><div class="wrap">
  <h2>How a {i['name'].lower()} project runs</h2>
  <p class="muted" style="margin-bottom:2.5rem">The same six steps for every cable, adapted to the qualification your sector requires.</p>
  {process_list()}
  <p style="margin-top:2.5rem" class="small muted">Also of interest: {other_links}.</p>
</div></section>
{cta_band("{p}", f"Need a {i['name'].lower()} cable?", "Send us your requirements and get a first technical answer within two working days.", i["slug"])}
"""
        write_page(f"industries/{i['slug']}.html", f"{i['name']} cables | LAPP Muller", i["short"] + " Custom designs from LAPP Muller.", body, "industries")


def build_capabilities():
    art = cross_section(conductors=2, fibres=2, pairs=2, size=300, armour=True, screen=True, label="Hybrid cable cross-section")
    body = f"""
{page_hero("{p}", [("Capabilities", None)], "Engineering, production and testing under one roof",
           "We design the cable, make it, terminate it and prove it works. That is how we deliver one-off lengths quickly and series reliably.", art)}
<section class="section"><div class="wrap split wide-left">
  <div class="prose">
    <h2 id="engineering">Custom cable engineering</h2>
    <p>Our design office and R&amp;D team work on electrical, pneumatic, optical, hydraulic and support cables. We combine them into hybrid constructions when one cable has to do the work of several.</p>
    <ul><li>Any length and any size, including short lengths</li><li>From miniaturised conductors to large cross-sections</li>
    <li>Material selection for heat, cold, radiation, seawater, oil and abrasion</li><li>Drawings and data sheets for each design</li></ul>
    <h2 id="assemblies">Connectors, terminations and equipment</h2>
    <p>We deliver cables ready to install: fitted with connectors, terminations and fittings, on reels or in sets, so you receive a working system rather than a cable and a list of parts.</p>
    <ul><li>Connector assembly and overmoulding</li><li>Mechanical terminations and strain relief</li><li>Reels, drums and handling accessories</li></ul>
    <h2 id="testing">Testing and certification</h2>
    <p>Because every solution is custom, we bring in the certifying body your project requires and certify one-off products when needed. Electrical, mechanical and environmental tests are planned with you during the engineering study.</p>
  </div>
  <aside class="aside-box">
    <h3>Ready to brief us?</h3>
    <p>The online project request asks the same questions as our needs analysis sheet and goes straight to the design office.</p>
    <div class="btn-row"><a class="btn btn-primary" href="{{p}}start-a-project.html">Start a project</a></div>
  </aside>
</div></section>
<section class="section section-paper" id="process"><div class="wrap">
  <div class="section-head"><h2>Our process</h2><p class="muted">Six steps, one project team, and a clear decision point after each.</p></div>
  {process_list()}
</div></section>
{cta_band("{p}")}
"""
    write_page("capabilities.html", "Capabilities: engineering, assemblies, testing | LAPP Muller",
               "Custom cable engineering, connectors and terminations, testing and certification, all in Grimaud, France.", body, "capabilities")


def build_cases():
    body = f"""
{page_hero("{p}", [("Case studies", None)], "Case studies", "Real briefs, and how we turned them into cables that work.")}
<section class="section"><div class="wrap">{case_cards()}</div></section>
{cta_band("{p}")}
"""
    write_page("case-studies/index.html", "Case studies | LAPP Muller", "How LAPP Muller solved demanding naval and subsea cable projects.", body, "cases")
    for c in CASES:
        facts = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in c["facts"])
        ind = IND[c["industry"]]
        body = f"""
{page_hero("{p}", [("Case studies", "case-studies/index.html"), (c["title"], None)], c["title"], c["summary"])}
<div class="case-art" style="aspect-ratio:auto;height:clamp(10rem,22vw,16rem)">{cable_run(c["art"])}</div>
<section class="section"><div class="wrap split wide-left">
  <article class="prose">
    <dl class="case-facts">{facts}</dl>
    <!-- EDITORIAL: summary based on public titles; replace with approved case copy before go-live -->
    <h2>The challenge</h2><p>{c['challenge']}</p>
    <h2>Our approach</h2><p>{c['approach']}</p>
    <h2>The result</h2><p>{c['result']}</p>
  </article>
  <aside class="aside-box"><h3>Similar project?</h3><p>See more about our work in <a href="{{p}}industries/{ind['slug']}.html">{ind['name'].lower()}</a>, or brief us directly.</p>
    <div class="btn-row"><a class="btn btn-primary" href="{{p}}start-a-project.html?industry={ind['slug']}">Start a project</a></div></aside>
</div></section>
{cta_band("{p}", industry=ind["slug"])}
"""
        write_page(f"case-studies/{c['slug']}.html", f"{c['title']} | LAPP Muller case study", c["summary"], body, "cases")


def build_about():
    body = f"""
{page_hero("{p}", [("About us", None)], "The LAPP Group's special cable specialist",
           f"Since {CO['since']}, LAPP Muller in Grimaud has been the technology centre of the LAPP Group for cables that do not exist in any catalogue.")}
<section class="section"><div class="wrap split">
  <div class="prose">
    <h2>Who we are</h2>
    <p>Our team in the Var designs and manufactures fully customised cables for industries where conditions are extreme and failure is expensive: defence, nuclear, subsea, energy, robotics and medical.</p>
    <p>We build in any length and size, keep lead times short, and aim to solve problems before they arise. That mission has not changed since the first cable left Grimaud.</p>
  </div>
  <table class="spec"><caption>Company profile</caption><tbody>
    <tr><th scope="row">Company</th><td>{CO['legal']}</td></tr>
    <tr><th scope="row">Site</th><td>{CO['city']}, Var, {CO['country']}</td></tr>
    <tr><th scope="row">Part of LAPP Group</th><td>Since {CO['since']}</td></tr>
    <tr><th scope="row">Sister companies</th><td>Camuna Cavi, Ceam Cavi Speciali, Unika</td></tr>
    <tr><th scope="row">Focus</th><td>Custom special cables and complete cable systems</td></tr>
  </tbody></table>
</div></section>
<section class="section section-paper" id="lapp-group"><div class="wrap split">
  <div><h2>Part of the LAPP Group</h2><p class="lead">The family-owned LAPP Group, headquartered in Stuttgart, is a leading supplier of integrated solutions in cable and connection technology.</p></div>
  <div class="prose"><p>For our customers, that means the engineering focus of a specialist with the purchasing power, global presence and stability of a group. Standard products come from the LAPP catalogue; LAPP Muller takes over where the catalogue ends.</p>
  <p><a href="{CO['group']}" rel="noopener">Visit lappgroup.com</a></p></div>
</div></section>
<section class="section" id="sustainability"><div class="wrap split">
  <div><h2>Thinking innovatively, acting sustainably</h2></div>
  <div class="prose"><p>Long service life is the most sustainable property a cable can have. We design for durability, choose halogen-free materials where possible, and support the electrification of ports and airports with our shore power and 400 Hz ranges.</p>
  <p class="small muted">Group-wide sustainability goals and reports are published by the LAPP Group.</p></div>
</div></section>
<section class="section section-paper" id="compliance"><div class="wrap split">
  <div><h2>Compliance and integrity</h2><p class="muted">We expect the same standards from ourselves and from our business partners.</p></div>
  <ul class="checklist">
    <li>Code of conduct for all employees</li><li>Compliance management system</li>
    <li>Confidential whistleblower system of the LAPP Group</li><li>Compliance requirements for business partners</li>
    <li>Gender equality index published every year, as required in France</li></ul>
</div></section>
{cta_band("{p}")}
"""
    write_page("about.html", "About LAPP Muller | Special cables from Grimaud, France",
               "LAPP Muller, LAPP Group technology centre for special cables since 2003, based in Grimaud, France.", body, "about")


def build_careers():
    body = f"""
{page_hero("{p}", [("Careers", None)], "Build cables nobody has built before",
           "Join a team of engineers, technicians and makers in Grimaud, between the Massif des Maures and the Gulf of Saint-Tropez.")}
<section class="section"><div class="wrap split">
  <div class="prose">
    <h2>Why LAPP Muller</h2>
    <ul class="checklist"><li>Every project is different: defence, nuclear, subsea, medical</li>
    <li>A site where design office, R&amp;D and production work side by side</li>
    <li>The stability and development paths of a family-owned group</li>
    <li>Apprenticeships and placements for students</li></ul>
  </div>
  <div class="aside-box">
    <h3>Open positions</h3>
    <p>Current vacancies, for example in our design office, are listed on the LAPP careers portal. Most roles require French.</p>
    <div class="btn-row"><a class="btn btn-primary" href="https://lappmuller.lappgroup.com/recrutement/postes-a-pourvoir.html" rel="noopener" hreflang="fr">See open positions</a>
    <a class="btn btn-ghost" href="mailto:{CO['email']}?subject=Spontaneous%20application">Send a spontaneous application</a></div>
  </div>
</div></section>
"""
    write_page("careers.html", "Careers at LAPP Muller | Grimaud, France",
               "Jobs, apprenticeships and placements at LAPP Muller, the LAPP Group special cable centre in Grimaud.", body, "careers")


def build_downloads():
    groups = ""
    for title, items in DOWNLOADS:
        gid = title.lower().replace(" ", "-")
        lis = ""
        for name, desc, url in items:
            ext = url.startswith("http")
            is_pdf = url.lower().endswith(".pdf")
            href = url if ext else "{p}" + url
            label = "Download PDF" if is_pdf else ("Open" if ext else "Start online")
            lis += f'<li><div><strong>{name}</strong><span>{desc}</span></div><a class="btn btn-ghost" href="{href}"{" rel=\"noopener\"" if ext else ""}>{label}<span class="visually-hidden">: {name}</span></a></li>'
        groups += f'<div class="dl-group" id="{gid}"><h2>{title}</h2><ul class="dl-list">{lis}</ul></div>'
    body = f"""
{page_hero("{p}", [("Downloads", None)], "Downloads", "Catalogues, data sheets and commercial documents in one place.")}
<section class="section"><div class="wrap">{groups}</div></section>
{cta_band("{p}", "Can't find a data sheet?", "Most of our cables are custom. Ask us and we will send the documentation for your design.")}
"""
    write_page("downloads.html", "Downloads: catalogues and data sheets | LAPP Muller",
               "LAPP Muller catalogues, data sheets for STS-Flex and MULL'AIR 400, and terms of trade.", body, "downloads")


def build_contact():
    hours = "".join(f"<tr><td>{d}</td><td>{h}</td></tr>" for d, h in CO["hours"])
    topics = ["New project or quotation", "Order or delivery", "Technical question", "Documents and certificates", "Other"]
    opts = "".join(f"<option>{t}</option>" for t in topics)
    body = f"""
{page_hero("{p}", [("Contact", None)], "Talk to the people who build your cable",
           "Sales, international sales and support share one number and one address, so you always reach someone who can help.")}
<section class="section"><div class="wrap">
  <div class="contact-cards">
    <div><h3>Call us</h3><p><a class="big-link" href="tel:{CO['phone_href']}">{CO['phone']}</a></p><table class="hours"><tbody>{hours}</tbody></table><p class="small muted">Times are Central European Time.</p></div>
    <div><h3>Email us</h3><p><a class="big-link" href="mailto:{CO['email']}">{CO['email']}</a></p><p class="small muted">For new projects, the project request form gets you a faster technical answer.</p></div>
    <div><h3>Visit us</h3><address style="font-style:normal">{CO['legal']}<br>{CO['street']}<br>{CO['zip']} {CO['city']}, {CO['country']}</address>
      <p><a href="https://www.openstreetmap.org/search?query=518%20avenue%20du%20Caucadis%2C%2083310%20Grimaud" rel="noopener">Open in map</a></p></div>
  </div>
</div></section>
<section class="section section-paper"><div class="wrap split wide-left">
  <div>
    <form class="form" id="contact-form" novalidate>
      <fieldset>
        <legend>Send us a message</legend>
        <div class="field"><label for="c-name">Name</label><input id="c-name" name="name" autocomplete="name" required><p class="error">Enter your name.</p></div>
        <div class="field"><label for="c-company">Company</label><input id="c-company" name="company" autocomplete="organization" required><p class="error">Enter your company.</p></div>
        <div class="field"><label for="c-email">Work email</label><input id="c-email" name="email" type="email" autocomplete="email" required><p class="error">Enter a valid email address, for example name@company.com.</p></div>
        <div class="field"><label for="c-phone">Phone <span class="hint">Optional, with country code</span></label><input id="c-phone" name="phone" type="tel" autocomplete="tel"></div>
        <div class="field full"><label for="c-topic">Topic</label><select id="c-topic" name="topic">{opts}</select></div>
        <div class="field full"><label for="c-msg">Message</label><textarea id="c-msg" name="message" required></textarea><p class="error">Write a short message so we can route it.</p></div>
        <label class="check full"><input type="checkbox" name="consent" required> <span>I agree that LAPP Muller processes my data to answer this request, as described in the <a href="{{p}}legal.html#privacy">privacy policy</a>.</span></label>
      </fieldset>
      <div><button class="btn btn-primary" type="submit">Send message</button></div>
    </form>
    <div class="form-result" hidden><h2>Your message is ready</h2><p>This concept is not connected to a mail system yet. In production, this message is sent to {CO['email']} and you get a confirmation by email.</p><pre></pre></div>
  </div>
  <aside class="aside-box"><h3>Starting a new cable?</h3><p>Use the project request. It collects the technical details our engineers need and saves a round of questions.</p>
  <div class="btn-row"><a class="btn btn-primary" href="{{p}}start-a-project.html">Start a project</a></div></aside>
</div></section>
"""
    write_page("contact.html", "Contact LAPP Muller | Grimaud, France",
               f"Call {CO['phone']} or email {CO['email']}. LAPP Muller, {CO['street']}, {CO['zip']} {CO['city']}.", body, "contact")


def build_rfq():
    inds = "".join(f'<label class="choice"><input type="radio" name="industry" value="{i["slug"]}"><span>{i["name"]}</span></label>' for i in INDUSTRIES)
    inds += '<label class="choice"><input type="radio" name="industry" value="other"><span>Other</span></label>'
    funcs = "".join(f'<label class="check"><input type="checkbox" name="functions" value="{f}"> <span>{f}</span></label>'
                    for f in ["Power", "Control and signal", "Data or coaxial", "Optical fibre", "Pneumatic or hydraulic", "Tensile strength"])
    move = "".join(f"<option>{m}</option>" for m in ["Fixed installation", "Occasional flexing", "Continuous bending or drag chain", "Torsion", "Reeling or towing", "Not sure yet"])
    body = f"""
{page_hero("{p}", [("Start a project", None)], "Start a cable project",
           "Three short steps, about five minutes. An engineer from our design office replies within two working days, under NDA if you need it.")}
<section class="section"><div class="wrap split wide-left">
  <div>
    <ol class="stepper" aria-label="Progress"><li>Application</li><li>Requirements</li><li>Contact</li></ol>
    <form class="form" id="rfq" novalidate>
      <fieldset class="form-step">
        <legend>What is the cable for?</legend>
        <div class="field full" data-required-group><span class="label" id="ind-l">Industry</span>
          <div class="choice-grid" role="radiogroup" aria-labelledby="ind-l">{inds}</div><p class="error">Choose the industry closest to your application.</p></div>
        <div class="field full"><label for="r-app">Describe the application <span class="hint">Where is the cable installed, what does it connect, how does it move?</span></label>
          <textarea id="r-app" name="application" required></textarea><p class="error">Describe the application in a sentence or two.</p></div>
        <div class="form-nav full"><span></span><button class="btn btn-primary" data-step="next">Continue to requirements</button></div>
      </fieldset>
      <fieldset class="form-step" hidden>
        <legend>What does it have to handle?</legend>
        <div class="field full"><span class="label">Functions in the cable</span><div class="choice-grid">{funcs}</div></div>
        <div class="field"><label for="r-move">Movement</label><select id="r-move" name="movement">{move}</select></div>
        <div class="field"><label for="r-volt">Voltage <span class="hint">For example 600 V or 1 kV</span></label><input id="r-volt" name="voltage"></div>
        <div class="field"><label for="r-tmin">Minimum temperature, °C</label><input id="r-tmin" name="temp_min" inputmode="numeric"></div>
        <div class="field"><label for="r-tmax">Maximum temperature, °C</label><input id="r-tmax" name="temp_max" inputmode="numeric"></div>
        <div class="field full"><label for="r-env">Environment and standards <span class="hint">Seawater, radiation, oils, UV, fire behaviour, required approvals</span></label><textarea id="r-env" name="environment"></textarea></div>
        <div class="field"><label for="r-len">Length per piece, m</label><input id="r-len" name="length" inputmode="decimal"></div>
        <div class="field"><label for="r-qty">Quantity</label><input id="r-qty" name="quantity" inputmode="numeric"></div>
        <div class="field full"><label for="r-file">Drawing or specification <span class="hint">Optional. PDF, DWG, STEP or image, up to 20 MB</span></label><input id="r-file" name="attachment" type="file" accept=".pdf,.dwg,.dxf,.step,.stp,.png,.jpg"></div>
        <div class="form-nav full"><button class="btn btn-ghost" data-step="back">Back</button><button class="btn btn-primary" data-step="next">Continue to contact</button></div>
      </fieldset>
      <fieldset class="form-step" hidden>
        <legend>Where should we reply?</legend>
        <div class="field"><label for="r-name">Name</label><input id="r-name" name="name" autocomplete="name" required><p class="error">Enter your name.</p></div>
        <div class="field"><label for="r-company">Company</label><input id="r-company" name="company" autocomplete="organization" required><p class="error">Enter your company.</p></div>
        <div class="field"><label for="r-email">Work email</label><input id="r-email" name="email" type="email" autocomplete="email" required><p class="error">Enter a valid email address, for example name@company.com.</p></div>
        <div class="field"><label for="r-country">Country</label><input id="r-country" name="country" autocomplete="country-name" required><p class="error">Enter your country so we can assign the right sales team.</p></div>
        <div class="field"><label for="r-date">Target date <span class="hint">Optional</span></label><input id="r-date" name="target_date" type="month"></div>
        <label class="check full"><input type="checkbox" name="nda" value="yes"> <span>Please send us an NDA before we share details</span></label>
        <label class="check full"><input type="checkbox" name="consent" required> <span>I agree that LAPP Muller processes my data to answer this request, as described in the <a href="{{p}}legal.html#privacy">privacy policy</a>.</span></label>
        <div class="form-nav full"><button class="btn btn-ghost" data-step="back">Back</button><button class="btn btn-primary" type="submit">Send project request</button></div>
      </fieldset>
    </form>
    <div class="form-result" hidden><h2>Your request is ready</h2><p>This concept is not connected to a CRM yet. In production, your request goes to the design office and you get a confirmation email with a reference number.</p><pre></pre></div>
  </div>
  <aside class="aside-box">
    <h3>What happens next</h3>
    <ul class="checklist"><li>An engineer reviews your request within two working days</li><li>We call or email with questions, or a first design proposal</li><li>You receive a drawing and quotation</li></ul>
    <p class="small" style="margin-top:1rem">Prefer to talk? Call <a href="tel:{CO['phone_href']}">{CO['phone']}</a>.</p>
  </aside>
</div></section>
"""
    write_page("start-a-project.html", "Start a cable project | LAPP Muller",
               "Request a custom special cable online. Describe your application and get a technical answer within two working days.", body, "rfq")


def build_legal():
    body = f"""
{page_hero("{p}", [("Legal notice and privacy", None)], "Legal notice and privacy policy", "Placeholder in this concept. The legally approved texts from the current site are inserted here before go-live.")}
<section class="section"><div class="wrap prose">
  <h2 id="notice">Legal notice</h2>
  <p>{CO['legal']}<br>{CO['street']}<br>{CO['zip']} {CO['city']}, {CO['country']}<br>Phone {CO['phone']}, email {CO['email']}</p>
  <p class="muted">Company registration, VAT number, publication director and hosting provider: take over from the current legal notice.</p>
  <h2 id="privacy">Privacy policy</h2>
  <p class="muted">Take over the current privacy policy and extend it for the project request and contact forms, including retention periods and the processor that receives form data.</p>
</div></section>
"""
    write_page("legal.html", "Legal notice and privacy | LAPP Muller", "Legal notice and privacy policy of LAPP Muller.", body)


def build_404():
    body = f"""
{page_hero("{p}", [("Page not found", None)], "This page does not exist",
           "The link may be outdated after our website relaunch. Start from one of these pages instead.",
           extra='<div class="btn-row"><a class="btn btn-primary" href="{p}index.html">Go to the homepage</a><a class="btn btn-ghost" href="{p}industries/index.html">See industries</a><a class="btn btn-ghost" href="{p}contact.html">Contact us</a></div>')}
"""
    write_page("404.html", "Page not found | LAPP Muller", "The page you requested does not exist.", body)


def build_meta():
    urls = "".join(f"<url><loc>{BASE_URL}/{p.replace('index.html', '')}</loc></url>" for p in PAGES)
    (OUT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n', encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE_URL}/sitemap.xml\n", encoding="utf-8")
    (OUT / ".nojekyll").write_text("", encoding="utf-8")
    fav = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" fill="#f39200"/>'
           '<circle cx="16" cy="16" r="11" fill="#fff" stroke="#1c2b33" stroke-width="2.5"/>'
           '<circle cx="16" cy="10.5" r="3" fill="#c0703f"/><circle cx="11.2" cy="19" r="3" fill="#c0703f"/><circle cx="20.8" cy="19" r="3" fill="#c0703f"/></svg>')
    (OUT / "assets" / "favicon.svg").write_text(fav, encoding="utf-8")


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(SRC / "assets", OUT / "assets")
    build_home()
    build_industries()
    build_capabilities()
    build_cases()
    build_about()
    build_careers()
    build_downloads()
    build_contact()
    build_rfq()
    build_legal()
    build_404()
    build_meta()
    print(f"Built {len(PAGES) + 1} pages into {OUT.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
