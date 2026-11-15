"""
FORGOTTEN IN SPACE: EVERY MISSION LEAVES A STORY
=================================================
Target Challenge: NASA Space Apps Challenge — "Off-World Artifacts"
Target Audience: School-Age Space Enthusiasts (Ages 12-18)
Core Framework: Python 3.11+, Streamlit 1.63+, Three.js WebGL (Cinematic NASA Textures & 3D GLB Models), NASA APIs, Gemini AI
"""

import os
import json
import base64
import streamlit as st
import streamlit.components.v1 as components

# Synchronize Streamlit Cloud secrets to os.environ for cloud deployment
try:
    if hasattr(st, "secrets"):
        for k, v in st.secrets.items():
            if isinstance(v, str) and k not in os.environ:
                os.environ[k] = v
except Exception:
    pass

from supabase_client import fetch_all, fetch_where, fetch_by_id
from nasa_images import fetch_spacecraft_photos
from gemini_chat import chat_with_spacecraft
from solar_system import render_enhanced_cinematic_solar_system

# ==============================================================================
# STREAMLIT CONFIGURATION
# ==============================================================================
st.set_page_config(
    page_title="Forgotten in Space: Every Mission Leaves a Story",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom Glassmorphic Sci-Fi CSS with Cyan Accents
st.markdown("""
<style>
    .stApp {
        background-color: #030611;
        color: #F8FAFC;
    }
    
    /* Top Header Branding */
    .site-title {
        font-size: 2.6rem;
        font-weight: 900;
        letter-spacing: -0.05em;
        background: linear-gradient(135deg, #00F0FF 0%, #38BDF8 50%, #818CF8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    .site-tagline {
        font-size: 1.05rem;
        color: #94A3B8;
        font-weight: 400;
        margin-top: -6px;
        margin-bottom: 20px;
    }

    /* Glassmorphic Cards */
    .glass-card {
        background: rgba(15, 23, 42, 0.75);
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 12px;
        padding: 20px;
        backdrop-filter: blur(12px);
        margin-bottom: 16px;
        transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
    }
    .glass-card:hover {
        border-color: rgba(0, 240, 255, 0.6);
        box-shadow: 0 8px 32px rgba(0, 240, 255, 0.15);
        transform: translateY(-2px);
    }

    /* Badges */
    .badge-silent {
        background-color: rgba(239, 68, 68, 0.18);
        color: #FCA5A5;
        border: 1px solid rgba(239, 68, 68, 0.4);
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.05em;
    }
    .badge-active {
        background-color: rgba(34, 197, 94, 0.18);
        color: #86EFAC;
        border: 1px solid rgba(34, 197, 94, 0.4);
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.05em;
    }

    /* Hardware to Science Bridge Visual Box */
    .bridge-box {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.8) 100%);
        border: 1px solid rgba(0, 240, 255, 0.3);
        border-radius: 10px;
        padding: 16px;
        margin: 10px 0;
    }
    .bridge-hw {
        color: #38BDF8;
        font-weight: 700;
        font-size: 0.95rem;
    }
    .bridge-sc {
        color: #F1F5F9;
        font-size: 0.9rem;
        margin-top: 4px;
    }

    /* Audio Hook Quote */
    .hook-quote {
        border-left: 4px solid #00F0FF;
        padding-left: 14px;
        font-style: italic;
        color: #CBD5E1;
        font-size: 1.1rem;
        margin: 16px 0;
        background: rgba(0, 240, 255, 0.05);
        padding-top: 8px;
        padding-bottom: 8px;
        border-radius: 0 8px 8px 0;
    }
</style>
""", unsafe_allow_html=True)

# Hardware to Science mappings
HARDWARE_SCIENCE_MAP = {
    "opportunity": [
        ("Mössbauer Spectrometer", "Identified jarosite minerals that exclusively form in acidic, standing liquid water lakes."),
        ("Microscopic Imager", "Captured extreme close-ups of hematite 'blueberries' formed in ancient aqueous sediments."),
        ("Rock Abrasion Tool (RAT)", "Drilled interior layers of rock untouched by dust, confirming historic surface oceans.")
    ],
    "perseverance": [
        ("SHERLOC UV Spectrometer", "Detected organic aromatic molecules preserved in river delta mudstones."),
        ("PIXL X-Ray Lithochemist", "Mapped elemental chemistry at grain scale, hunting ancient microscopic microbial fossils."),
        ("MOXIE Oxygen Generator", "Produced 122 grams of 98% pure breathable oxygen directly from Mars's carbon dioxide atmosphere.")
    ],
    "curiosity": [
        ("SAM Chemical Lab Suite", "Detected complex organic carbon chains and verified nitrates necessary for life."),
        ("ChemCam Laser Spectrometer", "Blasted Martian boulders with pulsed laser, proving ancient Gale Crater was a freshwater lake."),
        ("Alpha Particle X-Ray (APXS)", "Measured heavy elements across 30 kilometers of Martian mountain traverses.")
    ],
    "spirit": [
        ("Stuck Right Front Wheel", "Accidentally gouged trenches into the soil, uncovering 90% pure silica created by ancient hydrothermal vents."),
        ("Mini-TES Thermal Spectrometer", "Discovered carbonate-rich outcrops indicating wet, non-acidic ancient Martian environments.")
    ],
    "viking-1": [
        ("Biology Gas Exchange (GEX)", "First automated life-detection metabolism experiment conducted on another planet."),
        ("Gas Chromatograph Mass Spec (GCMS)", "Measured atmospheric composition and searched for organic molecules in Martian soil.")
    ],
    "insight": [
        ("SEIS Ultra-Sensitive Seismometer", "Detected over 1,300 marsquakes, mapping core-mantle boundaries and crustal thickness."),
        ("HP3 Heat Flow Probe ('The Mole')", "Attempted thermal conductivity measurements beneath the Elysium Planitia regolith.")
    ],
    "apollo-11": [
        ("Laser Ranging Retroreflector (LRRR)", "Still active today after 55+ years: reflects Earth lasers to measure Moon's orbit to millimeter accuracy."),
        ("Passive Seismic Experiment (PSEP)", "Detected moonquakes and meteorite strikes, proving the Moon possesses a differentiated crust and mantle."),
        ("Descent Propulsion Engine", "First throttleable rocket engine enabling soft human landing on extraterrestrial terrain.")
    ],
    "apollo-15": [
        ("Lunar Roving Vehicle (LRV)", "Allowed astronauts to travel 28 km away from the lander, exploring Hadley Rille canyon."),
        ("Lunar Surface Drill", "Extracted 3-meter deep core samples revealing billions of years of solar wind history."),
        ("Orbital Scientific Instrument Module", "High-resolution orbital photography of candidate landing sites across the lunar farside.")
    ],
    "surveyor-3": [
        ("Remote Soil Surface Sampler", "Dug trenches in lunar mare regolith, proving it could support the weight of future Apollo landers."),
        ("Scanning Television Camera", "Beamed 6,315 multi-filter photos back to Earth before Apollo 12 retrieved its camera.")
    ],
    "voyager-1": [
        ("Plasma Wave Instrument (PWS)", "Detected first sound oscillations of interstellar space outside the solar heliosphere in 2012."),
        ("Magnetometer (MAG)", "Measured interstellar magnetic field vectors untouched by solar wind."),
        ("Low-Energy Charged Particle (LECP)", "Monitored cosmic rays escaping our Solar System.")
    ]
}

# ==============================================================================
# SESSION STATE INITIALIZATION & ROUTING
# ==============================================================================
current_page = st.query_params.get("page", st.query_params.get("view", "home")).lower()

if "artifact" in st.query_params:
    st.session_state.selected_artifact_id = st.query_params["artifact"]

if "selected_artifact_id" not in st.session_state:
    st.session_state.selected_artifact_id = None

if "age_group" not in st.session_state:
    st.session_state.age_group = "junior"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = {}


# ==============================================================================
# VERIFIED NASA MARS SITES & FULL-SCREEN 3D WEBGL ENGINE (EXACT MATCH TO REFERENCE)
# ==============================================================================
NASA_MARS_LOCATIONS = [
    {
        "id": "opportunity",
        "short": "Opportunity",
        "name": "Opportunity Rover ('Oppy')",
        "site": "Meridiani Planum",
        "lat": -1.95, "lon": 354.47,
        "year": "2004–2018",
        "status": "Silent Monument",
        "color": "#38bdf8",
        "hardware": "Rock Abrasion Tool & Mössbauer Spectrometer",
        "science": "Discovered hematite 'blueberries' proving liquid water once soaked the Martian plains for millions of years."
    },
    {
        "id": "spirit",
        "short": "Spirit",
        "name": "Spirit Rover",
        "site": "Gusev Crater",
        "lat": -14.57, "lon": 175.47,
        "year": "2004–2010",
        "status": "Silent Monument",
        "color": "#fbbf24",
        "hardware": "Mössbauer Spectrometer & Locked Front Wheel",
        "science": "Its locked wheel scraped away red dust, accidentally discovering pure white silica formed by ancient boiling hot springs."
    },
    {
        "id": "insight",
        "short": "InSight",
        "name": "InSight Lander",
        "site": "Elysium Planitia",
        "lat": 4.50, "lon": 135.62,
        "year": "2018–2022",
        "status": "Silent Monument",
        "color": "#ec4899",
        "hardware": "SEIS Ultra-Sensitive Dome Seismometer",
        "science": "Listened to over 1,300 marsquakes, mapping Mars's crust thickness and proving it has a liquid molten core."
    },
    {
        "id": "viking-1",
        "short": "Viking 1",
        "name": "Viking 1 Lander",
        "site": "Chryse Planitia",
        "lat": 22.27, "lon": 312.05,
        "year": "1976–1982",
        "status": "Historic Monument",
        "color": "#a855f7",
        "hardware": "Biological Sampler Arm & GCMS",
        "science": "First spacecraft to successfully operate on the Martian surface, transmitting humanity's first clear ground photos."
    },
    {
        "id": "sojourner",
        "short": "Sojourner",
        "name": "Sojourner Rover",
        "site": "Ares Vallis",
        "lat": 19.13, "lon": 326.78,
        "year": "1997",
        "status": "Historic Monument",
        "color": "#22c55e",
        "hardware": "Alpha Proton X-Ray Spectrometer (Microwave-sized rover)",
        "science": "First wheeled rover on another planet, analyzing rounded pebbles carved by catastrophic ancient Martian floods."
    },
    {
        "id": "perseverance",
        "short": "Perseverance",
        "name": "Perseverance & Ingenuity",
        "site": "Jezero Crater",
        "lat": 18.44, "lon": 77.45,
        "year": "2021–Active",
        "status": "Active Explorer",
        "color": "#00f0ff",
        "hardware": "SuperCam Laser & MOXIE Oxygen Generator",
        "science": "Hunting ancient microscopic fossils in a dried river delta and manufacturing pure breathable oxygen from thin CO2."
    },
    {
        "id": "curiosity",
        "short": "Curiosity",
        "name": "Curiosity Rover",
        "site": "Gale Crater",
        "lat": -4.59, "lon": 137.44,
        "year": "2012–Active",
        "status": "Active Explorer",
        "color": "#38bdf8",
        "hardware": "ChemCam Laser & SAM Chemical Lab",
        "science": "Proved ancient Mars had freshwater lakes containing sulfur, nitrogen, oxygen, and carbon—the key building blocks of life."
    }
]


def render_full_screen_mars(locations=None):
    if not locations:
        try:
            from supabase_client import fetch_where
            locations = fetch_where(column="zone", value="mars")
        except Exception:
            locations = []

    NASA_MARS_COORDS = {
        "sojourner-rover": {"lat": 19.33, "lon": 326.45, "site": "Ares Vallis", "year": "1997", "color": "#22c55e", "short": "Sojourner"},
        "spirit-rover": {"lat": -14.5684, "lon": 175.4726, "site": "Gusev Crater", "year": "2004", "color": "#fbbf24", "short": "Spirit"},
        "opportunity-rover": {"lat": -1.9483, "lon": 354.4742, "site": "Meridiani Planum", "year": "2004", "color": "#38bdf8", "short": "Opportunity"},
        "viking-1-lander": {"lat": 22.697, "lon": 311.778, "site": "Chryse Planitia", "year": "1976", "color": "#a855f7", "short": "Viking 1"},
        "viking-2-lander": {"lat": 47.968, "lon": 134.262, "site": "Utopia Planitia", "year": "1976", "color": "#f97316", "short": "Viking 2"},
        "phoenix-lander": {"lat": 68.2188, "lon": 234.2508, "site": "Vastitas Borealis", "year": "2008", "color": "#06b6d4", "short": "Phoenix"},
        "insight-lander": {"lat": 4.502, "lon": 135.623, "site": "Elysium Planitia", "year": "2018", "color": "#ec4899", "short": "InSight"},
        "ingenuity-helicopter": {"lat": 18.4446, "lon": 77.4509, "site": "Jezero Crater / Valinor Hills", "year": "2021", "color": "#00f0ff", "short": "Ingenuity"}
    }

    default_mars_artifacts = [
        {"id": "opportunity-rover", "name": "Opportunity Rover", "landing_coordinates": "1.9483° S, 354.4742° E (Meridiani Planum)", "nasa_description": "MER-B marathon runner, explored Meridiani Planum for 14.8 years until 2018 dust storm.", "power_source": "Triple-junction solar cells"},
        {"id": "viking-1-lander", "name": "Viking 1 Lander", "landing_coordinates": "22.697° N, 48.222° W (Chryse Planitia)", "nasa_description": "First operational lander on Mars (1976). Operated for 6 years in Chryse Planitia.", "power_source": "Snap-19 Radioisotope Thermoelectric Generators (RTG)"},
        {"id": "ingenuity-helicopter", "name": "Ingenuity Helicopter", "landing_coordinates": "18.4446° N, 77.4509° E (Valinor Hills)", "nasa_description": "First powered flight on another planet (2021–2024). Completed 72 flights. Resting at Valinor Hills.", "power_source": "Solar panel charging secondary lithium-ion batteries"},
        {"id": "sojourner-rover", "name": "Sojourner Rover", "landing_coordinates": "19.33° N, 33.55° W (Ares Vallis)", "nasa_description": "First rover on Mars (1997), delivered by Pathfinder. Now permanently parked.", "power_source": "GaAs solar array + primary lithium D-cells"},
        {"id": "spirit-rover", "name": "Spirit Rover", "landing_coordinates": "14.5684° S, 175.4726° E (Gusev Crater)", "nasa_description": "MER-A explored Gusev Crater for over 6 years. Permanently parked at Troy.", "power_source": "Solar array generating ~140W"},
        {"id": "viking-2-lander", "name": "Viking 2 Lander", "landing_coordinates": "47.968° N, 225.738° W (Utopia Planitia)", "nasa_description": "Landed September 1976 in Utopia Planitia. Performed biology experiments.", "power_source": "Dual RTGs producing 57W"},
        {"id": "phoenix-lander", "name": "Phoenix Lander", "landing_coordinates": "68.2188° N, 234.2508° E (Vastitas Borealis)", "nasa_description": "First spacecraft to touch water ice on Mars (2008) in arctic plains.", "power_source": "Dual gallium arsenide solar arrays"},
        {"id": "insight-lander", "name": "InSight Lander", "landing_coordinates": "4.502° N, 135.623° E (Elysium Planitia)", "nasa_description": "Studied Mars interior structure using seismometers (2018–2022). Silent monument.", "power_source": "UltraFlex solar arrays"}
    ]

    source_list = locations if (locations and len(locations) > 0) else default_mars_artifacts
    enriched_locations = []
    seen_ids = set()
    for loc in source_list:
        cid = loc.get("id")
        if cid in seen_ids:
            continue
        seen_ids.add(cid)
        coords_info = NASA_MARS_COORDS.get(cid, {
            "lat": 0.0, "lon": 0.0, "site": "Martian Surface", "year": "Historic", "color": "#00d2ff", "short": loc.get("name", "Spacecraft")
        })
        item = dict(loc)
        item.update(coords_info)
        enriched_locations.append(item)

    for def_item in default_mars_artifacts:
        did = def_item["id"]
        if did not in seen_ids:
            item = dict(def_item)
            item.update(NASA_MARS_COORDS.get(did, {}))
            enriched_locations.append(item)
            seen_ids.add(did)

    # Always put the 3 verified NASA equipment with 3D models and audio stories at the very top
    priority_order = {"opportunity-rover": 0, "viking-1-lander": 1, "ingenuity-helicopter": 2}
    enriched_locations.sort(key=lambda x: priority_order.get(x.get("id"), 99))

    MARS_EXTRA_FACTS = {
        "opportunity-rover": {
            "hardware": "Rock Abrasion Tool & Mössbauer Spectrometer",
            "science": "Discovered hematite 'blueberries' proving liquid water once soaked the Martian plains for millions of years.",
            "first_person_script": "My battery is low and it's getting dark. I survived 14.8 years on a 90-day mission across 45 km of Mars.",
            "type": "Rover",
            "status": "Silent Monument",
            "year": "2004–2018"
        },
        "spirit-rover": {
            "hardware": "Stuck Right Front Wheel & Mini-TES Thermal Spectrometer",
            "science": "Accidentally gouged trenches into the soil, uncovering 90% pure silica created by ancient volcanic hot springs.",
            "first_person_script": "I dragged my frozen wheel across Gusev Crater, uncovering evidence of ancient hydrothermal springs before getting trapped at Troy.",
            "type": "Rover",
            "status": "Silent Monument",
            "year": "2004–2010"
        },
        "sojourner-rover": {
            "hardware": "Alpha Proton X-Ray Spectrometer (APXS) & Microrover Chassis",
            "science": "First microrover on Mars; analyzed andesite volcanic rocks in Ares Vallis and proved robotic mobility on the Martian surface.",
            "first_person_script": "I was humanity's first wheels on Mars in 1997. Microrover size, I proved rovers could roam the red planet.",
            "type": "Rover",
            "status": "Historic Monument",
            "year": "1997"
        },
        "viking-1-lander": {
            "hardware": "Biological Sampler Arm & GCMS (Gas Chromatograph Mass Spectrometer)",
            "science": "First spacecraft to successfully operate on the Martian surface, transmitting humanity's first clear ground photos.",
            "first_person_script": "I was humanity's first successful sentinel on Martian soil at Chryse Planitia, operating for over 6 years.",
            "type": "Lander",
            "status": "Historic Monument",
            "year": "1976–1982"
        },
        "viking-2-lander": {
            "hardware": "Surface Seismometer & Gas Exchange Biology Laboratory",
            "science": "Analyzed permafrost soil chemistry and atmospheric composition across Utopia Planitia for 1,281 Martian sols.",
            "first_person_script": "I touched down in Utopia Planitia, analyzing Martian soil and searching for organic traces.",
            "type": "Lander",
            "status": "Historic Monument",
            "year": "1976–1980"
        },
        "phoenix-lander": {
            "hardware": "Robotic Trench Arm & TEGA Thermal/Evolved Gas Analyzer",
            "science": "Dug into the Martian arctic permafrost and directly touched water ice, discovering perchlorate salts.",
            "first_person_script": "I scraped the arctic soil of Vastitas Borealis and confirmed water ice just beneath the dust before winter froze my solar panels.",
            "type": "Lander",
            "status": "Silent Monument",
            "year": "2008"
        },
        "insight-lander": {
            "hardware": "SEIS Ultra-Sensitive Seismometer & HP3 Heat Flow Probe",
            "science": "Detected over 1,300 marsquakes, revealing Mars's liquid iron-nickel core and crustal thickness.",
            "first_person_script": "I listened to the pulse of Mars with my seismometer dome, measuring over 1,300 quakes until dust blanketed my arrays in 2022.",
            "type": "Lander",
            "status": "Silent Monument",
            "year": "2018–2022"
        },
        "ingenuity-helicopter": {
            "hardware": "Dual Counter-Rotating Carbon Fiber Rotors (2400 RPM) & Solar Cell",
            "science": "First powered aerodynamic flight on another planet, proving aerial exploration in Mars's 1% atmosphere over 72 flights.",
            "first_person_script": "They said powered flight was impossible in Mars's razor-thin air. I flew 72 times across Jezero Crater.",
            "type": "Helicopter",
            "status": "Silent Monument",
            "year": "2021–2024"
        }
    }
    for loc in enriched_locations:
        lid = loc.get("id")
        if lid in MARS_EXTRA_FACTS:
            loc.update(MARS_EXTRA_FACTS[lid])

    locs_json = json.dumps(enriched_locations)

    template_path = os.path.join(os.path.dirname(__file__), "static", "mars_explorer.html")
    with open(template_path, "r", encoding="utf-8") as f:
        html = f.read()

    html = html.replace("/*LOCATIONS_PLACEHOLDER*/[]", locs_json)
    html = html.replace("/*GEMINI_KEY_PLACEHOLDER*/\"\"", json.dumps(os.getenv("GEMINI_API_KEY", "")))
    html = html.replace("/*NASA_KEY_PLACEHOLDER*/\"\"", json.dumps(os.getenv("NASA_API_KEY", "8P7pKqtdRdfbhHnww87fmNqPbh7fT6wLzCbQwC9F")))
    components.html(html, height=880, scrolling=False)


# ==============================================================================
# VERIFIED NASA APOLLO LUNAR ARTIFACTS ROSTER
# ==============================================================================
NASA_MOON_LOCATIONS = [
    {
        "id": "apollo-11-lm",
        "name": "Apollo 11 'Eagle' LM",
        "short": "Apollo 11",
        "site": "Sea of Tranquility (Mare Tranquillitatis)",
        "lat": 0.674, "lon": 23.473,
        "year": "1969",
        "status": "Historic Monument",
        "color": "#fbbf24",
        "type": "Lander",
        "hardware": "Lunar Module Descent Stage and EASEP Laser Reflector",
        "science": "First human touchdown on another world; returned 21.6 kg of lunar basalt and soil proving ancient magma ocean."
    },
    {
        "id": "apollo-15-lrv",
        "name": "Apollo 15 and Lunar Rover #1",
        "short": "Apollo 15",
        "site": "Hadley Rille / Apennine Mountains",
        "lat": 26.132, "lon": 3.634,
        "year": "1971",
        "status": "Historic Monument",
        "color": "#00f0ff",
        "type": "Rover",
        "hardware": "Boeing Lunar Roving Vehicle and Heat Flow Probes",
        "science": "Discovered the 'Genesis Rock' (anorthosite dated to 4.1 billion yrs), confirming early primordial lunar magma crust."
    },
    {
        "id": "surveyor-3-lander",
        "name": "Surveyor 3 Lander",
        "short": "Surveyor 3",
        "site": "Ocean of Storms",
        "lat": -3.015, "lon": -23.418,
        "year": "1967",
        "status": "Historic Monument",
        "color": "#22c55e",
        "type": "Lander",
        "hardware": "Robotic Surface Soil Sampler Arm and Scanning TV Camera",
        "science": "First robotic trench dug into lunar regolith, demonstrating the lunar surface could support the weight of Apollo landing modules."
    },
    {
        "id": "apollo-12-lm",
        "name": "Apollo 12 'Intrepid' LM",
        "short": "Apollo 12",
        "site": "Ocean of Storms (Oceanus Procellarum)",
        "lat": -3.012, "lon": -23.422,
        "year": "1969",
        "status": "Historic Monument",
        "color": "#38bdf8",
        "type": "Lander",
        "hardware": "Intrepid Descent Stage and ALSEP Nuclear Station",
        "science": "Precision landing within 160m of Surveyor 3; retrieved parts proving 2-year survival of mechanical parts in lunar vacuum."
    },
    {
        "id": "apollo-14-lm",
        "name": "Apollo 14 'Antares' LM",
        "short": "Apollo 14",
        "site": "Fra Mauro Highlands",
        "lat": -3.645, "lon": -17.471,
        "year": "1971",
        "status": "Historic Monument",
        "color": "#fbbf24",
        "type": "Lander",
        "hardware": "Modular Equipment Transporter ('Lunar Rickshaw') and ALSEP",
        "science": "Sampled Cone Crater impact breccias, dating the colossal Imbrium Basin impact event to 3.85 billion years ago."
    },
    {
        "id": "apollo-16-lrv",
        "name": "Apollo 16 and Lunar Rover #2",
        "short": "Apollo 16",
        "site": "Descartes Highlands",
        "lat": -8.973, "lon": 15.500,
        "year": "1972",
        "status": "Historic Monument",
        "color": "#a855f7",
        "type": "Rover",
        "hardware": "Lunar Roving Vehicle and Far UV Camera/Spectrograph",
        "science": "First astronomical observatory deployed on the Moon; proved highland plains are impact-generated, not volcanic."
    },
    {
        "id": "apollo-17-lrv",
        "name": "Apollo 17 and Lunar Rover #3",
        "short": "Apollo 17",
        "site": "Taurus-Littrow Valley",
        "lat": 20.191, "lon": 30.772,
        "year": "1972",
        "status": "Historic Monument",
        "color": "#ec4899",
        "type": "Rover",
        "hardware": "Lunar Roving Vehicle and Traverse Gravimeter",
        "science": "Discovered 3.6-billion-year-old orange volcanic glass beads, revealing explosive ancient pyroclastic fire fountains on the Moon."
    }
]

def render_full_screen_moon(locations=None):
    source_list = locations if (locations and len(locations) > 0) else NASA_MOON_LOCATIONS
    
    seen_ids = set()
    enriched = []
    for loc in source_list:
        cid = loc.get("id") or loc.get("name")
        if cid in seen_ids:
            continue
        seen_ids.add(cid)
        enriched.append(dict(loc))
        
    for def_loc in NASA_MOON_LOCATIONS:
        did = def_loc["id"]
        if did not in seen_ids:
            enriched.append(dict(def_loc))
            seen_ids.add(did)

    # Priority order: Apollo 11, Apollo 15 Lunar Rover, Surveyor 3 at top
    priority = {"apollo-11-lm": 0, "apollo-15-lrv": 1, "surveyor-3-lander": 2}
    enriched.sort(key=lambda x: priority.get(x.get("id"), 99))

    MOON_EXTRA_FACTS = {
        "apollo-11-lm": {
            "landing_coordinates": "0.674° N, 23.473° E (Mare Tranquillitatis)",
            "power_source": "Descent Stage Silver-Zinc Batteries (Apollo LM)",
            "nasa_description": "First human touchdown on another world; returned 21.6 kg of lunar basalt and soil proving ancient magma ocean.",
            "first_person_script": "Houston, Tranquility Base here. The Eagle has landed. July 20, 1969.",
            "type": "Lander",
            "status": "Historic Monument",
            "year": "1969"
        },
        "apollo-15-lrv": {
            "landing_coordinates": "26.132° N, 3.634° E (Hadley Rille / Apennines)",
            "power_source": "Two 36-volt Silver-Zinc Non-Rechargeable Batteries",
            "nasa_description": "Discovered the 'Genesis Rock' (anorthosite dated to 4.1 billion yrs), confirming early primordial lunar magma crust.",
            "first_person_script": "I was the very first Lunar Rover driven by human astronauts across the Moon.",
            "type": "Rover",
            "status": "Historic Monument",
            "year": "1971"
        },
        "surveyor-3-lander": {
            "landing_coordinates": "3.015° S, 23.418° W (Ocean of Storms)",
            "power_source": "Solar Panel & Rechargeable Silver-Zinc Battery",
            "nasa_description": "First robotic trench dug into lunar regolith, demonstrating the lunar surface could support the weight of Apollo landing modules.",
            "first_person_script": "I was the automated scout that tested the lunar soil before human boots touched it.",
            "type": "Lander",
            "status": "Historic Monument",
            "year": "1967"
        }
    }
    for loc in enriched:
        lid = loc.get("id")
        if lid in MOON_EXTRA_FACTS:
            loc.update(MOON_EXTRA_FACTS[lid])
    
    locs_json = json.dumps(enriched)
    
    template_path = os.path.join(os.path.dirname(__file__), "static", "moon_explorer.html")
    with open(template_path, "r", encoding="utf-8") as f:
        html = f.read()
        
    html = html.replace("/*LOCATIONS_PLACEHOLDER*/[]", locs_json)
    html = html.replace("/*GEMINI_KEY_PLACEHOLDER*/\"\"", json.dumps(os.getenv("GEMINI_API_KEY", "")))
    html = html.replace("/*NASA_KEY_PLACEHOLDER*/\"\"", json.dumps(os.getenv("NASA_API_KEY", "8P7pKqtdRdfbhHnww87fmNqPbh7fT6wLzCbQwC9F")))
    components.html(html, height=880, scrolling=False)


# ==============================================================================
# VERIFIED NASA DEEP SPACE ARTIFACTS ROSTER
# ==============================================================================
NASA_DEEP_LOCATIONS = [
    {
        "id": "voyager-1",
        "name": "Voyager 1",
        "short": "Voyager 1",
        "site": "Interstellar Space (Ophiuchus)",
        "lat": 0.0, "lon": 0.0,
        "year": "1977",
        "launch_date": "September 5, 1977",
        "status": "Active Interstellar",
        "color": "#38bdf8",
        "type": "Interstellar Probe",
        "power_source": "3 MHW-RTGs (~220W Today)",
        "mission_duration": "47+ Years (Active Since 1977)",
        "distance_traveled": "17 km/s (38,000 mph)",
        "landing_coordinates": "Interstellar Space (Ophiuchus constellation)",
        "mass_dimensions": "825 kg (1,819 lb)",
        "communications": "3.7m High-Gain Parabolic Dish (8.4 GHz X-band)",
        "hardware": "Plasma Wave Subsystem (PWS) & Magnetometer",
        "science": "Recorded first authentic sounds of interstellar plasma oscillations outside the Sun's magnetic bubble.",
        "first_person_script": "I have traveled farther from Earth than any creation of humanity in history. Even beyond our Sun's magnetic realm, I am still speaking across the dark.",
        "nasa_description": "Most distant human-made object in history. Launched in 1977, Voyager 1 crossed the heliopause into interstellar space on August 25, 2012."
    },
    {
        "id": "dawn-spacecraft",
        "name": "Dawn Spacecraft",
        "short": "Dawn",
        "site": "Orbit around Dwarf Planet Ceres",
        "lat": 0.0, "lon": 0.0,
        "year": "2007",
        "launch_date": "September 27, 2007",
        "status": "Silent Monument",
        "color": "#fbbf24",
        "type": "Orbiter",
        "power_source": "10 kW Solar Arrays & Xenon Ion Thrusters",
        "mission_duration": "11 Years (2007–2018)",
        "distance_traveled": "6.9 Billion km",
        "landing_coordinates": "Stable Uncontrolled Orbit around Ceres",
        "mass_dimensions": "1,240 kg (2,734 lb)",
        "communications": "1.52m High-Gain Dish (Deep Space Network)",
        "hardware": "Framing Camera & Visible/Infrared Spectrometer (VIR)",
        "science": "Discovered sodium carbonate deposits in Occator Crater and subsurface brine ocean on dwarf planet Ceres.",
        "first_person_script": "Propelled by glowing xenon ion thrusters, I unlocked the ancient secrets of the asteroid belt and Ceres before quietly running out of fuel.",
        "nasa_description": "First spacecraft to orbit two extraterrestrial destinations (Vesta and Ceres). It remains in a stable quarantine orbit around Ceres."
    },
    {
        "id": "kepler-space-telescope",
        "name": "Kepler Space Telescope",
        "short": "Kepler",
        "site": "Earth-trailing Heliocentric Orbit",
        "lat": 0.0, "lon": 0.0,
        "year": "2009",
        "launch_date": "March 7, 2009",
        "status": "Silent Monument",
        "color": "#00f0ff",
        "type": "Space Telescope",
        "power_source": "1.1 kW Solar Array & Reaction Wheels",
        "mission_duration": "9.6 Years (2009–2018)",
        "distance_traveled": "Earth-Trailing Orbit (~150 Million km from Earth)",
        "landing_coordinates": "Heliocentric Earth-Trailing Orbit",
        "mass_dimensions": "1,052 kg (2,319 lb)",
        "communications": "High-Gain X-band Antenna",
        "hardware": "0.95m Schmidt Telescope & 95-Megapixel Array (42 CCDs)",
        "science": "Discovered over 2,600 confirmed exoplanets, proving that planets outnumber stars across our Milky Way galaxy.",
        "first_person_script": "I stared unblinking at 150,000 stars in the Cygnus constellation, hunting tiny dips in starlight to prove that planets are everywhere in the universe.",
        "nasa_description": "NASA's premier planet-hunting space telescope. Revolutionized our understanding of exoplanets before retiring in October 2018."
    },
    {
        "id": "near-shoemaker",
        "name": "NEAR Shoemaker",
        "short": "NEAR Shoemaker",
        "site": "Surface of Asteroid 433 Eros",
        "lat": 0.0, "lon": 0.0,
        "year": "1996",
        "launch_date": "February 17, 1996",
        "status": "Silent Monument",
        "color": "#ec4899",
        "type": "Asteroid Lander",
        "power_source": "Gallium Arsenide Solar Arrays (~1.8 kW)",
        "mission_duration": "5 Years (1996–2001)",
        "distance_traveled": "3.2 Billion km",
        "landing_coordinates": "Sedis Regio, Asteroid 433 Eros",
        "mass_dimensions": "805 kg (1,775 lb)",
        "communications": "1.5m High-Gain Antenna",
        "hardware": "X-ray/Gamma-Ray Spectrometer (XGRS) & Laser Rangefinder",
        "science": "First spacecraft to orbit and touch down on an asteroid, transmitting surface chemistry data directly from Eros bedrock.",
        "first_person_script": "I was never designed to land, but on February 12, 2001, I made history by gently touching down onto asteroid 433 Eros and transmitting from its surface.",
        "nasa_description": "First mission to orbit and land on an asteroid (433 Eros). Safely rested on the surface and sent gamma-ray spectra."
    },
    {
        "id": "pioneer-10",
        "name": "Pioneer 10",
        "short": "Pioneer 10",
        "site": "Interstellar Trajectory (Taurus)",
        "lat": 0.0, "lon": 0.0,
        "year": "1972",
        "launch_date": "March 3, 1972",
        "status": "Silent Monument",
        "color": "#a855f7",
        "type": "Deep Space Probe",
        "power_source": "4 SNAP-19 RTGs (Plutonium-238)",
        "mission_duration": "30+ Years (Last Signal Jan 2003)",
        "distance_traveled": "12 km/s Interstellar Trajectory",
        "landing_coordinates": "Heading toward star Aldebaran (Taurus)",
        "mass_dimensions": "258 kg (569 lb)",
        "communications": "2.74m Parabolic Dish Antenna",
        "hardware": "Helium Vector Magnetometer & Pioneer Plaque",
        "science": "First craft to traverse Asteroid Belt and encounter Jupiter; carries gold-anodized pictorial plaque for extraterrestrial finders.",
        "first_person_script": "I was the very first spacecraft to sail through the asteroid belt and photograph the swirling violent clouds of Jupiter up close.",
        "nasa_description": "First mission to Jupiter and first craft to achieve escape velocity from the Solar System. Carries the famous Pioneer Plaque."
    },
    {
        "id": "pioneer-11",
        "name": "Pioneer 11",
        "short": "Pioneer 11",
        "site": "Interstellar Trajectory (Aquila)",
        "lat": 0.0, "lon": 0.0,
        "year": "1973",
        "launch_date": "April 5, 1973",
        "status": "Silent Monument",
        "color": "#f97316",
        "type": "Deep Space Probe",
        "power_source": "4 SNAP-19 RTGs (Plutonium-238)",
        "mission_duration": "22 Years (Last Signal Nov 1995)",
        "distance_traveled": "11.4 km/s Interstellar Trajectory",
        "landing_coordinates": "Heading toward constellation Aquila",
        "mass_dimensions": "259 kg (571 lb)",
        "communications": "2.74m Parabolic Dish Antenna",
        "hardware": "Fluxgate Magnetometer & Imaging Photopolarimeter",
        "science": "First probe to encounter Saturn and investigate its rings; discovered Saturn's F-ring and uncharted moon Epimetheus.",
        "first_person_script": "I skimmed just above Saturn's rings in 1979, proving ring gaps were clear enough for the Voyagers to safely navigate.",
        "nasa_description": "Pioneered the path through Saturn's rings and hazardous asteroid belts before embarking on its eternal interstellar outbound path."
    }
]

def render_full_screen_deep(locations=None):
    source_list = locations if (locations and len(locations) > 0) else NASA_DEEP_LOCATIONS
    seen_ids = set()
    enriched = []
    for loc in source_list:
        cid = loc.get("id") or loc.get("name")
        if cid in seen_ids:
            continue
        seen_ids.add(cid)
        enriched.append(dict(loc))
        
    for def_loc in NASA_DEEP_LOCATIONS:
        did = def_loc["id"]
        if did not in seen_ids:
            enriched.append(dict(def_loc))
            seen_ids.add(did)

    # Priority order: Voyager 1, Dawn, Kepler, NEAR, Pioneer 10, Pioneer 11
    priority = {"voyager-1": 0, "dawn-spacecraft": 1, "kepler-space-telescope": 2, "near-shoemaker": 3, "pioneer-10": 4, "pioneer-11": 5}
    enriched.sort(key=lambda x: priority.get(x.get("id"), 99))

    locs_json = json.dumps(enriched)
    
    template_path = os.path.join(os.path.dirname(__file__), "static", "deep_explorer.html")
    with open(template_path, "r", encoding="utf-8") as f:
        html = f.read()
        
    html = html.replace("/*LOCATIONS_PLACEHOLDER*/[]", locs_json)
    html = html.replace("/*GEMINI_KEY_PLACEHOLDER*/\"\"", json.dumps(os.getenv("GEMINI_API_KEY", "")))
    html = html.replace("/*NASA_KEY_PLACEHOLDER*/\"\"", json.dumps(os.getenv("NASA_API_KEY", "8P7pKqtdRdfbhHnww87fmNqPbh7fT6wLzCbQwC9F")))
    components.html(html, height=880, scrolling=False)


# ==============================================================================
# ROUTING & PAGES (QUERY PARAMETER PAGE ROUTER)
# ==============================================================================

# ==========================================
# PAGE 1: 3D SOLAR SYSTEM HOMEPAGE
# ==========================================
if current_page in ["home", "solar_system"]:
    st.markdown("""
    <style>
        .block-container {
            padding-top: 0rem !important;
            padding-bottom: 0rem !important;
            padding-left: 0rem !important;
            padding-right: 0rem !important;
            max-width: 100vw !important;
            margin: 0 !important;
        }
        header[data-testid="stHeader"] {
            display: none !important;
        }
        div[data-testid="stAppViewContainer"] {
            overflow: hidden !important;
        }
        div[data-testid="stVerticalBlock"] {
            gap: 0rem !important;
        }
        iframe {
            display: block !important;
            border: none !important;
            width: 100vw !important;
            height: 96vh !important;
            min-height: 900px !important;
        }
    </style>
    """, unsafe_allow_html=True)

    c_warp1, c_warp2, c_warp3, c_sp = st.columns([1.2, 1.2, 1.2, 4.0])
    with c_warp1:
        if st.button("🔴 Warp to 3D Mars", key="btn_quick_mars", use_container_width=True):
            st.query_params["page"] = "mars"
            st.rerun()
    with c_warp2:
        if st.button("🌕 Warp to 3D Moon", key="btn_quick_moon", use_container_width=True):
            st.query_params["page"] = "moon"
            st.rerun()
    with c_warp3:
        if st.button("🌌 Warp to Deep Space", key="btn_quick_deep", use_container_width=True):
            st.query_params["page"] = "deep"
            st.rerun()

    # Render Full-Screen Cinematic Solar System
    render_enhanced_cinematic_solar_system()


# ==========================================
# PAGE 2: 3D MARS MODEL SCREEN
# ==========================================
elif current_page in ["mars", "mars_explorer"]:
    st.markdown("""
    <style>
        .block-container, div[data-testid="stMainBlockContainer"], .main .block-container {
            padding: 0.5rem 1.5rem !important;
            max-width: 100% !important;
            width: 100% !important;
        }
        header, footer { visibility: hidden !important; }
        iframe {
            width: 100% !important;
            height: 86vh !important;
            display: block !important;
            margin: 0 auto !important;
            border: 1px solid rgba(56, 189, 248, 0.25) !important;
            border-radius: 14px !important;
            box-shadow: 0 0 50px rgba(0, 0, 0, 0.95), 0 0 25px rgba(255, 85, 51, 0.15) !important;
        }
    </style>
    """, unsafe_allow_html=True)

    c_ret, c_studio, c_title = st.columns([0.20, 0.35, 0.45])
    with c_ret:
        if st.button("⬅️ Return to Solar System", key="btn_ret_mars", use_container_width=True):
            st.query_params["page"] = "home"
            if "view" in st.query_params:
                del st.query_params["view"]
            st.rerun()
    with c_studio:
        if st.button("🤖 Gemini AI Chatbot & Database Studio", key="btn_quick_mars_studio", use_container_width=True):
            st.query_params["page"] = "spacecraft_studio"
            st.query_params["artifact"] = "opportunity-rover"
            st.rerun()
    with c_title:
        st.caption("Spin 3D Mars globe below or click beacons to launch 3D Equipment & Audio:")

    # Render Full-Screen Three.js WebGL Mars Model (Exact to reference image)
    mars_artifacts = fetch_where(column="zone", value="mars")
    render_full_screen_mars(mars_artifacts)

    with st.expander("🤖 Explore Martian Spacecraft Database & Stories", expanded=False):
        artifacts = fetch_where(column="zone", value="mars")
        for art in artifacts:
            st.markdown(f"""
            <div class="glass-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <h4 style="margin:0; color:#38BDF8;">{art['name']}</h4>
                    <span class="badge-silent">SILENT MONUMENT</span>
                </div>
                <p style="font-size:0.9rem; color:#E2E8F0; margin-top:0.4rem;">{art['nasa_description']}</p>
                <p style="font-size:0.8rem; color:#94A3B8;">⚡ <b>Power:</b> {art.get('power_source')} | 📍 <b>Site:</b> {art.get('landing_coordinates')}</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Open Story Studio: {art['name']} ➔", key=f"mars_open_{art['id']}", use_container_width=True):
                st.session_state.selected_artifact_id = art["id"]
                st.query_params["page"] = "spacecraft_studio"
                st.query_params["artifact"] = art["id"]
                st.rerun()


# ==========================================
# PAGE 3: 3D MOON MODEL SCREEN
# ==========================================
elif current_page in ["moon", "moon_explorer"]:
    st.markdown("""
    <style>
        .block-container, div[data-testid="stMainBlockContainer"], .main .block-container {
            padding: 0.5rem 1.5rem !important;
            max-width: 100% !important;
            width: 100% !important;
        }
        header, footer { visibility: hidden !important; }
        iframe {
            width: 100% !important;
            height: 86vh !important;
            display: block !important;
            margin: 0 auto !important;
            border: 1px solid rgba(56, 189, 248, 0.25) !important;
            border-radius: 14px !important;
            box-shadow: 0 0 50px rgba(0, 0, 0, 0.95), 0 0 25px rgba(251, 191, 36, 0.15) !important;
        }
    </style>
    """, unsafe_allow_html=True)

    c_ret, c_studio, c_title = st.columns([0.20, 0.35, 0.45])
    with c_ret:
        if st.button("⬅️ Return to Solar System", key="btn_ret_moon", use_container_width=True):
            st.query_params["page"] = "home"
            if "view" in st.query_params:
                del st.query_params["view"]
            st.rerun()
    with c_studio:
        if st.button("🤖 Gemini AI Chatbot & Database Studio", key="btn_quick_moon_studio", use_container_width=True):
            st.query_params["page"] = "spacecraft_studio"
            st.query_params["artifact"] = "apollo-11-lm"
            st.rerun()
    with c_title:
        st.caption("Spin 3D Moon globe below or click beacons to explore NASA Images, Telemetry & Voice Audio:")

    # Render Full-Screen Three.js WebGL Moon Model
    render_full_screen_moon(NASA_MOON_LOCATIONS)

    with st.expander("🚀 Explore Lunar Equipment Database & Stories", expanded=False):
        artifacts = fetch_where(column="zone", value="moon")
        for art in artifacts:
            st.markdown(f"""
            <div class="glass-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <h4 style="margin:0; color:#38BDF8;">{art['name']}</h4>
                    <span class="badge-silent">SILENT MONUMENT</span>
                </div>
                <p style="font-size:0.9rem; color:#E2E8F0; margin-top:0.4rem;">{art['nasa_description']}</p>
                <p style="font-size:0.8rem; color:#94A3B8;">⚡ <b>Power:</b> {art.get('power_source')} | 📍 <b>Site:</b> {art.get('landing_coordinates') or 'Apollo Landing Site'}</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Open Story Studio: {art['name']} ➔", key=f"moon_open_{art['id']}", use_container_width=True):
                st.session_state.selected_artifact_id = art["id"]
                st.query_params["page"] = "spacecraft_studio"
                st.query_params["artifact"] = art["id"]
                st.rerun()


# ==========================================
# PAGE 4: DEEP SPACE SCREEN
# ==========================================
elif current_page in ["deep", "deep_space"]:
    st.markdown("""
    <style>
        /* True 100% Full-Screen Edge-to-Edge Container */
        html, body, [data-testid="stAppViewContainer"], .main, .block-container, div[data-testid="stMainBlockContainer"] {
            padding: 0 !important;
            margin: 0 !important;
            max-width: 100vw !important;
            width: 100vw !important;
            height: 100vh !important;
            overflow: hidden !important;
            background: #020617 !important;
        }
        header, footer, [data-testid="stHeader"] { display: none !important; }
        div[data-testid="stVerticalBlock"] { gap: 0 !important; }
        iframe {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
            min-height: 100vh !important;
            border: none !important;
            border-radius: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
            box-shadow: none !important;
            z-index: 999999 !important;
        }
    </style>
    """, unsafe_allow_html=True)

    deep_artifacts = fetch_where(column="zone", value="deep_space")
    render_full_screen_deep(deep_artifacts)

    with st.expander("🤖 Explore Deep Space Spacecraft Database & Stories", expanded=False):
        artifacts = fetch_where(column="zone", value="deep_space")
        for art in artifacts:
            is_active = art.get("id") == "voyager-1"
            badge = '<span class="badge-active">ACTIVE INTERSTELLAR</span>' if is_active else '<span class="badge-silent">SILENT MONUMENT</span>'
            st.markdown(f"""
            <div class="glass-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <h4 style="margin:0; color:#38BDF8;">{art['name']}</h4>
                    {badge}
                </div>
                <p style="font-size:0.9rem; color:#E2E8F0; margin-top:0.4rem;">{art['nasa_description']}</p>
                <p style="font-size:0.8rem; color:#94A3B8;">⚡ <b>Power:</b> {art.get('power_source')} | 📍 <b>Destination:</b> Deep Space</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Open Story Studio: {art['name']} ➔", key=f"deep_open_{art['id']}", use_container_width=True):
                st.session_state.selected_artifact_id = art["id"]
                st.query_params["page"] = "spacecraft_studio"
                st.query_params["artifact"] = art["id"]
                st.rerun()


# ==========================================
# PAGE 5: SPACECRAFT STORY STUDIO
# ==========================================
elif current_page == "spacecraft_studio" and st.session_state.selected_artifact_id:
    craft = fetch_by_id(st.session_state.selected_artifact_id)

    if not craft:
        st.error("Spacecraft record not found.")
        if st.button("⬅ Return to Solar System"):
            st.query_params["page"] = "home"
            st.rerun()
    else:
        is_active = craft.get("id") == "voyager-1"
        badge = "🟢 ACTIVE INTERSTELLAR" if is_active else "🔴 SILENT MONUMENT"

        prev_page = "moon" if craft["zone"] == "moon" else "mars" if craft["zone"] == "mars" else "deep"
        if st.button(f"⬅ Back to {craft['zone'].capitalize()} Monuments"):
            st.query_params["page"] = prev_page
            if "artifact" in st.query_params:
                del st.query_params["artifact"]
            st.rerun()

        # Title Header
        c_hdr1, c_hdr2 = st.columns([3, 1])
        with c_hdr1:
            st.markdown(f"# {craft['name']}")
            st.markdown(f"**Status:** `{badge}` | **Location:** `{craft.get('landing_coordinates') or 'Deep Space Trajectory'}`")
            st.markdown(f"**Power System:** `{craft.get('power_source')}`")
        with c_hdr2:
            st.markdown(f"[🔗 Official NASA Catalog Record]({craft['nssdc_link']})")

        # 1st-Person Hook Quote
        st.markdown(f'<div class="hook-quote">"{craft.get("first_person_script")}"</div>', unsafe_allow_html=True)

        col_left, col_right = st.columns([1.1, 1.1])

        # Left Column: Hardware -> Science & Photos
        with col_left:
            st.markdown("### 🔬 The Hardware ➔ Science Bridge")
            st.caption("How physical engineering tools directly unlocked groundbreaking scientific discoveries:")

            bridges = HARDWARE_SCIENCE_MAP.get(craft["id"], [
                ("Specialized Spacecraft Bus", "Maintained instrument calibration and survived extreme thermal fluctuations in space."),
                ("Telemetry Communications Subsystem", "Beamed scientific sensor data across millions of miles back to NASA's Deep Space Network.")
            ])

            for hw, sc in bridges:
                st.markdown(f"""
                <div class="bridge-box">
                    <div class="bridge-hw">🛠️ Engineering Tool: {hw}</div>
                    <div class="bridge-sc">💡 Scientific Discovery: {sc}</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("#### 📜 Verbatim NASA Archive Record")
            st.info(craft["nasa_description"])

            st.markdown("#### 📷 Authentic NASA Mission Imagery")
            photos = fetch_spacecraft_photos(craft["name"], zone=craft["zone"], max_results=2)
            for p in photos:
                st.image(p["image_url"], caption=f"{p['title']} ({p.get('date', 'NASA Archive')})", use_container_width=True)

        # Right Column: Live 1st-Person AI Chat with Gemini
        with col_right:
            st.markdown(f"### 🤖 Live 1st-Person AI Chat with {craft['name']}")
            age_choice = st.radio(
                "Explorer Perspective:",
                options=["junior", "senior"],
                format_func=lambda x: "🌱 Junior Explorer (Ages 12–14)" if x == "junior" else "🔬 Senior Explorer (Ages 15–18)",
                horizontal=True,
                index=0 if st.session_state.age_group == "junior" else 1,
                key="studio_age_radio"
            )
            st.session_state.age_group = age_choice
            st.caption(f"Tone automatically customized for **{st.session_state.age_group.upper()}** explorers using Google Gemini & NASA archive facts.")

            @st.fragment
            def render_chat_fragment(craft_dict):
                cid = craft_dict["id"]
                if cid not in st.session_state.chat_history:
                    st.session_state.chat_history[cid] = [
                        {"role": "assistant", "content": f"Greetings explorer! {craft_dict.get('first_person_script', 'What would you like to know about my journey?')}"}
                    ]

                for msg in st.session_state.chat_history[cid]:
                    with st.chat_message(msg["role"]):
                        st.write(msg["content"])

                prompt = st.chat_input(f"Ask {craft_dict['name']} a question...")
                if prompt:
                    st.session_state.chat_history[cid].append({"role": "user", "content": prompt})
                    with st.chat_message("user"):
                        st.write(prompt)

                    with st.spinner(f"{craft_dict['name']} is transmitting response across space..."):
                        reply = chat_with_spacecraft(
                            spacecraft=craft_dict,
                            user_message=prompt,
                            chat_history=st.session_state.chat_history[cid],
                            age_group=st.session_state.age_group
                        )

                    st.session_state.chat_history[cid].append({"role": "assistant", "content": reply})
                    with st.chat_message("assistant"):
                        st.write(reply)

            render_chat_fragment(craft)
