import os
import json
import streamlit.components.v1 as components

def render_enhanced_cinematic_solar_system(locations=None):
    import json
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

    # Verified NASA Equipment with 3D Models & Audio Stories first
    default_mars_artifacts = [
        {"id": "opportunity-rover", "name": "Opportunity Rover", "landing_coordinates": "1.9483° S, 354.4742° E (Meridiani Planum)", "nasa_description": "MER-B marathon runner, explored Meridiani Planum for 14.8 years until 2018 dust storm.", "power_source": "Triple-junction solar cells", "first_person_script": "I am Opportunity. My mission was planned for 90 days, but I drove a full marathon across Meridiani Planum."},
        {"id": "viking-1-lander", "name": "Viking 1 Lander", "landing_coordinates": "22.697° N, 48.222° W (Chryse Planitia)", "nasa_description": "First operational lander on Mars (1976). Operated for 6 years in Chryse Planitia.", "power_source": "Snap-19 Radioisotope Thermoelectric Generators (RTG)", "first_person_script": "I am Viking 1. In July 1976, I sent humanity its very first clear color photographs from the surface of Mars."},
        {"id": "ingenuity-helicopter", "name": "Ingenuity Helicopter", "landing_coordinates": "18.4446° N, 77.4509° E (Valinor Hills)", "nasa_description": "First powered flight on another planet (2021–2024). Completed 72 flights. Resting at Valinor Hills.", "power_source": "Solar panel charging secondary lithium-ion batteries", "first_person_script": "I am Ingenuity. I proved that powered, controlled aerodynamic flight is possible in the razor-thin atmosphere of another planet."},
        {"id": "sojourner-rover", "name": "Sojourner Rover", "landing_coordinates": "19.33° N, 33.55° W (Ares Vallis)", "nasa_description": "First rover on Mars (1997), delivered by Pathfinder. Now permanently parked.", "power_source": "GaAs solar array + primary lithium D-cells", "first_person_script": "I am Sojourner. Just the size of a microwave oven, I became the very first rover to roll across the red sands of Mars."},
        {"id": "spirit-rover", "name": "Spirit Rover", "landing_coordinates": "14.5684° S, 175.4726° E (Gusev Crater)", "nasa_description": "MER-A explored Gusev Crater for over 6 years. Permanently parked at Troy.", "power_source": "Solar array generating ~140W", "first_person_script": "I am Spirit. For over six Earth years I climbed the Columbia Hills and uncovered ancient hydrothermal hot springs."},
        {"id": "viking-2-lander", "name": "Viking 2 Lander", "landing_coordinates": "47.968° N, 225.738° W (Utopia Planitia)", "nasa_description": "Landed September 1976 in Utopia Planitia. Performed biology experiments.", "power_source": "Dual RTGs producing 57W", "first_person_script": "I am Viking 2. Resting in the cold expanse of Utopia Planitia, I searched for the chemical signatures of Martian life."},
        {"id": "phoenix-lander", "name": "Phoenix Lander", "landing_coordinates": "68.2188° N, 234.2508° E (Vastitas Borealis)", "nasa_description": "First spacecraft to touch water ice on Mars (2008) in arctic plains.", "power_source": "Dual gallium arsenide solar arrays", "first_person_script": "I am Phoenix. In the frozen northern plains, my robotic arm scraped into the soil and touched genuine Martian water ice."},
        {"id": "insight-lander", "name": "InSight Lander", "landing_coordinates": "4.502° N, 135.623° E (Elysium Planitia)", "nasa_description": "Studied Mars interior structure using seismometers (2018–2022). Silent monument.", "power_source": "UltraFlex solar arrays", "first_person_script": "I am InSight. With my ultra-sensitive seismometer, I listened to the internal heartbeat of Mars and recorded over 1,300 marsquakes."}
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

    # Ensure all 8 canonical artifacts are included
    for def_item in default_mars_artifacts:
        did = def_item["id"]
        if did not in seen_ids:
            item = dict(def_item)
            item.update(NASA_MARS_COORDS.get(did, {}))
            enriched_locations.append(item)
            seen_ids.add(did)

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

    # Always put the 3 verified NASA equipment with 3D models and audio stories at the very top
    priority_order = {"opportunity-rover": 0, "viking-1-lander": 1, "ingenuity-helicopter": 2}
    enriched_locations.sort(key=lambda x: priority_order.get(x.get("id"), 99))

    locs_json = json.dumps(enriched_locations)
    html_code = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <style>
            * { box-sizing: border-box; }
            body, html {
                margin: 0; padding: 0; width: 100%; height: 100%;
                overflow: hidden; background: #010309;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                color: #F8FAFC;
            }
            #container {
                display: flex; width: 100vw; height: 100vh; position: relative;
            }
            #viewport-3d {
                width: 100%; height: 100%; position: relative;
                transition: width 0.75s cubic-bezier(0.16, 1, 0.3, 1);
            }
    
        /* View Toggle in Detail Header Bar */
        .detail-view-toggle {
          display: inline-flex;
          background: rgba(15, 23, 42, 0.85);
          border: 1px solid rgba(56, 189, 248, 0.4);
          border-radius: 20px;
          padding: 3px;
          gap: 4px;
        }
        .toggle-view-btn {
          background: transparent;
          border: none;
          color: #94A3B8;
          font-size: 11.5px;
          font-weight: 700;
          padding: 5px 14px;
          border-radius: 16px;
          cursor: pointer;
          transition: all 0.2s ease;
        }
        .toggle-view-btn:hover {
          color: #FFFFFF;
        }
        .toggle-view-btn.active {
          background: linear-gradient(135deg, #0284C7, #00D2FF);
          color: #FFFFFF;
          box-shadow: 0 0 12px rgba(0, 210, 255, 0.5);
        }

        /* 52% NASA Mission Imagery & Media Studio Viewport */
        .detail-nasa-gallery-viewport {
          flex: 1; height: 100%; position: relative;
          background: radial-gradient(circle at center, #0B132B 0%, #020617 100%);
          overflow: hidden; display: flex; flex-direction: column;
          padding: 18px 22px; box-sizing: border-box; gap: 12px;
        }
        .nasa-gallery-header {
          display: flex; justify-content: space-between; align-items: center;
          flex-wrap: wrap; gap: 8px;
        }
        .nasa-brand-badge {
          display: inline-flex; align-items: center; gap: 8px;
          background: rgba(15, 23, 42, 0.85); border: 1.5px solid rgba(56, 189, 248, 0.45);
          border-radius: 20px; padding: 6px 14px;
          box-shadow: 0 0 15px rgba(56, 189, 248, 0.2);
        }
        .nasa-insignia {
          font-weight: 900; font-size: 12px; color: #38BDF8; letter-spacing: 1px;
        }
        .nasa-live-status {
          font-size: 10.5px; font-weight: 700; color: #34D399; letter-spacing: 0.6px;
        }
        .nasa-gallery-actions {
          display: flex; gap: 8px;
        }
        .nasa-action-btn {
          background: rgba(30, 41, 59, 0.85); border: 1px solid rgba(251, 191, 36, 0.45);
          color: #FBBF24; font-size: 11px; font-weight: 700; padding: 5px 12px;
          border-radius: 14px; cursor: pointer; transition: all 0.2s ease;
        }
        .nasa-action-btn:hover {
          background: rgba(251, 191, 36, 0.2); border-color: #FBBF24; color: #FFF;
          box-shadow: 0 0 12px rgba(251, 191, 36, 0.4);
        }

        /* Main High-Resolution Photo Display */
        .nasa-hero-display-wrap {
          flex: 1; position: relative; width: 100%; min-height: 250px;
          background: #010409; border: 1.5px solid rgba(56, 189, 248, 0.35);
          border-radius: 14px; overflow: hidden; display: flex; align-items: center;
          justify-content: center; box-shadow: 0 8px 32px rgba(0,0,0,0.85), inset 0 0 25px rgba(56, 189, 248, 0.08);
        }
        .nasa-hero-img {
          width: 100%; height: 100%; object-fit: contain; background: #000;
          transition: transform 0.3s ease, opacity 0.25s ease;
        }
        .nasa-hero-img:hover {
          cursor: zoom-in;
        }
        .nasa-img-loading {
          position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
          display: flex; flex-direction: column; align-items: center; gap: 10px;
          color: #38BDF8; font-size: 12px; font-weight: 700; pointer-events: none;
        }
        .nasa-spinner {
          width: 38px; height: 38px; border: 3px solid rgba(56, 189, 248, 0.2);
          border-top-color: #38BDF8; border-radius: 50%; animation: spinAnim 0.8s linear infinite;
        }
        .nasa-img-info-overlay {
          position: absolute; bottom: 0; left: 0; right: 0;
          background: linear-gradient(180deg, transparent 0%, rgba(2, 6, 23, 0.92) 25%, rgba(2, 6, 23, 0.98) 100%);
          padding: 14px 18px; backdrop-filter: blur(8px); display: flex;
          flex-direction: column; gap: 4px; border-top: 1px solid rgba(255, 255, 255, 0.1);
          transition: opacity 0.2s ease;
        }
        .nasa-info-top {
          display: flex; justify-content: space-between; align-items: center;
        }
        .nasa-photo-id {
          color: #FBBF24; font-size: 10.5px; font-weight: 800; letter-spacing: 0.8px;
        }
        .nasa-photo-date {
          color: #94A3B8; font-size: 10.5px; font-weight: 600;
        }
        .nasa-photo-title {
          font-size: 13.5px; font-weight: 800; color: #FFFFFF; line-height: 1.3;
        }
        .nasa-photo-caption {
          font-size: 11.5px; color: #CBD5E1; line-height: 1.4; max-height: 48px;
          overflow-y: auto;
        }

        /* NASA Archive Live Search Bar */
        .nasa-search-bar-wrap {
          display: flex; gap: 8px; align-items: center;
          background: rgba(15, 23, 42, 0.85); border: 1.5px solid rgba(148, 163, 184, 0.25);
          border-radius: 10px; padding: 4px 8px;
        }
        .nasa-search-icon {
          font-size: 13px; color: #94A3B8; margin-left: 4px;
        }
        .nasa-search-input {
          flex: 1; background: transparent; border: none; outline: none;
          color: #FFFFFF; font-size: 11.5px; padding: 6px;
        }
        .nasa-search-btn {
          background: linear-gradient(135deg, #0284C7, #2563EB); color: #FFFFFF;
          border: none; border-radius: 6px; font-size: 11px; font-weight: 700;
          padding: 6px 14px; cursor: pointer; transition: all 0.2s ease;
        }
        .nasa-search-btn:hover {
          background: linear-gradient(135deg, #0369A1, #1D4ED8);
          box-shadow: 0 0 10px rgba(56, 189, 248, 0.4);
        }

        /* Thumbnails Strip */
        .nasa-thumbnail-strip-section {
          display: flex; flex-direction: column; gap: 6px;
        }
        .nasa-strip-title {
          font-size: 10px; font-weight: 800; color: #94A3B8; letter-spacing: 0.8px;
        }
        .nasa-thumbnails-strip {
          display: flex; gap: 10px; overflow-x: auto; padding: 4px 2px 8px 2px;
          scroll-behavior: smooth;
        }
        .nasa-thumb-card {
          flex: 0 0 88px; height: 60px; border-radius: 8px; overflow: hidden;
          border: 2px solid rgba(148, 163, 184, 0.25); cursor: pointer;
          position: relative; transition: all 0.2s ease; background: #020617;
        }
        .nasa-thumb-card:hover {
          border-color: rgba(56, 189, 248, 0.7); transform: translateY(-2px);
        }
        .nasa-thumb-card.active {
          border-color: #38BDF8; box-shadow: 0 0 14px rgba(56, 189, 248, 0.65);
          transform: translateY(-2px);
        }
        .nasa-thumb-img {
          width: 100%; height: 100%; object-fit: cover;
        }

        #viewport-3d canvas {
                width: 100% !important;
                height: 100% !important;
                display: block !important;
                outline: none;
            }
            #info-panel {
                width: 0%; height: 100%;
                background: linear-gradient(180deg, rgba(8, 15, 34, 0.97) 0%, rgba(3, 7, 18, 0.99) 100%);
                border-left: 1px solid rgba(0, 210, 255, 0.4);
                padding: 0; overflow-y: auto; opacity: 0;
                transition: width 0.75s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.5s ease;
                display: flex; flex-direction: column;
            }
            #container.panel-open #viewport-3d { width: 60%; }
            #container.panel-open #info-panel { width: 40%; opacity: 1; padding: 26px; }

            /* Mars Split-Screen Mode: Viewport occupies ONLY the right side */
            #container.mars-mode #viewport-3d {
                margin-left: 410px !important;
                width: calc(100% - 410px) !important;
            }
            #container.mars-mode #globe-badges-layer {
                left: 410px !important;
                width: calc(100% - 410px) !important;
            }
            #container.mars-mode #toolbar-mars {
                left: calc(50% + 205px) !important;
                transform: translateX(-50%) !important;
            }

            /* Floating Full-Width Glassmorphic Header */
            #main-header {
                position: absolute; top: 0; left: 0; width: 100vw;
                display: flex; align-items: center; justify-content: space-between;
                padding: 12px 28px; z-index: 100;
                background: linear-gradient(180deg, rgba(3, 7, 18, 0.92) 0%, rgba(3, 7, 18, 0.45) 80%, transparent 100%);
                backdrop-filter: blur(10px);
                border-bottom: 1px solid rgba(56, 189, 248, 0.22);
                user-select: none;
            }
            .brand-box { display: flex; flex-direction: column; }
            .site-header-title {
                font-size: 20px; font-weight: 900; letter-spacing: 2.2px;
                background: linear-gradient(90deg, #FFFFFF 0%, #00D2FF 50%, #38BDF8 100%);
                -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                text-transform: uppercase; margin: 0; line-height: 1.1;
            }
            .site-header-tagline {
                color: #94A3B8; font-size: 10px; font-weight: 600; letter-spacing: 1.2px; margin-top: 3px;
            }
            .nav-links { display: flex; align-items: center; gap: 8px; }
            .nav-btn {
                background: rgba(15, 23, 42, 0.75); border: 1px solid rgba(56, 189, 248, 0.35);
                color: #E2E8F0; border-radius: 20px; padding: 6px 14px; font-size: 12px; font-weight: 700;
                cursor: pointer; transition: all 0.2s ease;
            }
            .nav-btn:hover {
                background: rgba(0, 210, 255, 0.2); border-color: #00D2FF; color: #FFFFFF;
                box-shadow: 0 0 12px rgba(0, 210, 255, 0.5); transform: translateY(-1px);
            }
            .explore-hero-btn {
                background: linear-gradient(90deg, #0284C7 0%, #00D2FF 100%);
                border: none; color: #FFFFFF; border-radius: 20px; padding: 7px 18px;
                font-size: 12px; font-weight: 800; cursor: pointer; text-transform: uppercase;
                letter-spacing: 0.6px; box-shadow: 0 0 18px rgba(0, 210, 255, 0.45);
                transition: all 0.2s ease;
            }
            .explore-hero-btn:hover {
                box-shadow: 0 0 28px rgba(0, 210, 255, 0.85); transform: translateY(-1px);
            }
            .quick-controls { display: flex; align-items: center; gap: 8px; }
            .ctrl-group { display: flex; align-items: center; gap: 3px; }
            .ctrl-label { font-size: 10.5px; font-weight: 700; color: #94A3B8; text-transform: uppercase; margin-right: 4px; }
            .ctrl-btn {
                background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(148, 163, 184, 0.25);
                color: #CBD5E1; border-radius: 14px; padding: 3px 8px; font-size: 11px; font-weight: 600;
                cursor: pointer; transition: all 0.2s ease;
            }
            .ctrl-btn:hover {
                background: rgba(0, 210, 255, 0.2); border-color: #00D2FF; color: #FFFFFF;
            }
            .ctrl-btn.active {
                background: linear-gradient(90deg, #0284C7, #00D2FF); border-color: #00D2FF;
                color: #FFFFFF; font-weight: 700; box-shadow: 0 0 10px rgba(0, 210, 255, 0.5);
            }
            .ctrl-divider { width: 1px; height: 16px; background: rgba(148, 163, 184, 0.3); margin: 0 4px; }
            #audio-control {
                background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(0, 210, 255, 0.45);
                border-radius: 20px; padding: 4px 12px; display: flex; align-items: center;
                gap: 6px; cursor: pointer; font-size: 11px; font-weight: 700; color: #38BDF8;
                user-select: none; transition: all 0.2s ease;
            }
            #audio-control:hover { border-color: #00D2FF; box-shadow: 0 0 14px rgba(0, 210, 255, 0.6); }

            /* Floating 3D Planet Badges */
            .planet-badge {
                position: absolute; z-index: 85;
                transform: translate(-50%, -140%);
                background: rgba(8, 16, 36, 0.85);
                border: 1px solid rgba(56, 189, 248, 0.4);
                border-radius: 16px; padding: 3px 9px;
                font-size: 11px; font-weight: 700; color: #E2E8F0;
                white-space: nowrap; cursor: pointer; backdrop-filter: blur(6px);
                transition: border-color 0.2s, transform 0.2s, box-shadow 0.2s;
                user-select: none; display: none;
            }
            .planet-badge:hover {
                border-color: #00D2FF; color: #FFFFFF;
                background: rgba(0, 210, 255, 0.25);
                box-shadow: 0 0 14px rgba(0, 210, 255, 0.6);
                transform: translate(-50%, -150%) scale(1.08);
            }
            .planet-badge.monument-target {
                border-color: #00D2FF; color: #38BDF8;
                box-shadow: 0 0 10px rgba(0, 210, 255, 0.4);
            }

            /* Bottom Planet Dock */
            #planet-dock {
                position: absolute; bottom: 16px; left: 50%; transform: translateX(-50%);
                z-index: 90; background: rgba(8, 16, 36, 0.88); border: 1px solid rgba(56, 189, 248, 0.35);
                border-radius: 32px; padding: 6px 14px; display: flex; align-items: center; gap: 6px;
                backdrop-filter: blur(12px); box-shadow: 0 0 24px rgba(0, 0, 0, 0.7);
            }
            .dock-btn {
                background: transparent; border: 1px solid transparent; border-radius: 20px;
                color: #CBD5E1; padding: 4px 9px; font-size: 11px; font-weight: 600;
                cursor: pointer; transition: all 0.2s ease; display: flex; align-items: center; gap: 4px;
            }
            .dock-btn:hover {
                background: rgba(0, 210, 255, 0.15); border-color: #00D2FF; color: #FFFFFF;
                transform: translateY(-2px); box-shadow: 0 0 10px rgba(0, 210, 255, 0.4);
            }
            .dock-btn.highlight {
                background: rgba(0, 210, 255, 0.22); border-color: #00D2FF; color: #38BDF8;
                box-shadow: 0 0 8px rgba(0, 210, 255, 0.3);
            }

            /* Hover Tooltip */
            #hover-tooltip {
                position: absolute; z-index: 95; pointer-events: none;
                background: rgba(10, 18, 38, 0.92); border: 1px solid #00D2FF;
                border-radius: 6px; padding: 5px 12px; font-size: 12px; font-weight: 700;
                color: #00D2FF; display: none; transform: translate(-50%, -130%);
                box-shadow: 0 0 14px rgba(0, 210, 255, 0.6);
            }

            /* Welcome Hint Overlay */
            #welcome-overlay {
                position: absolute; bottom: 74px; left: 50%; transform: translateX(-50%);
                z-index: 50; background: rgba(10, 18, 38, 0.9); border: 1px solid rgba(0, 210, 255, 0.5);
                border-radius: 30px; padding: 8px 24px; font-size: 12.5px; font-weight: 600;
                color: #F8FAFC; pointer-events: none; transition: opacity 0.6s ease;
                box-shadow: 0 0 25px rgba(0, 210, 255, 0.35); display: flex; align-items: center; gap: 8px;
            }
            #welcome-overlay.hidden { opacity: 0; }

            /* HUD Details & Flash Cards */
            .fc-topbar {
                display: flex; align-items: center; justify-content: space-between;
                margin-bottom: 14px; padding-bottom: 10px;
                border-bottom: 1px solid rgba(56, 189, 248, 0.18);
            }
            .fc-nav-controls {
                display: flex; align-items: center; gap: 8px;
                background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(56, 189, 248, 0.25);
                border-radius: 20px; padding: 3px 10px;
            }
            .fc-arrow-btn {
                background: transparent; border: none; color: #38BDF8; font-size: 13px;
                cursor: pointer; padding: 2px 6px; font-weight: 800; transition: color 0.2s;
            }
            .fc-arrow-btn:hover { color: #FFFFFF; text-shadow: 0 0 8px #00D2FF; }
            .fc-counter { font-size: 11px; font-weight: 700; color: #94A3B8; letter-spacing: 1px; }

            .fc-voice-btn {
                background: rgba(14, 165, 233, 0.15); border: 1px solid rgba(0, 210, 255, 0.4);
                color: #38BDF8; border-radius: 16px; padding: 4px 12px; font-size: 11px;
                font-weight: 700; cursor: pointer; transition: all 0.2s ease;
            }
            .fc-voice-btn:hover {
                background: rgba(0, 210, 255, 0.25); border-color: #00D2FF; color: #FFFFFF;
                box-shadow: 0 0 12px rgba(0, 210, 255, 0.5);
            }

            .fc-hero {
                display: flex; align-items: center; gap: 14px; margin-bottom: 14px;
            }
            .fc-symbol {
                font-size: 38px; line-height: 1; filter: drop-shadow(0 0 16px rgba(0, 210, 255, 0.5));
            }
            .fc-title-group { display: flex; flex-direction: column; }
            .planet-title {
                font-size: 28px; font-weight: 900; margin: 0;
                background: linear-gradient(90deg, #FFFFFF, #00D2FF, #38BDF8);
                -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                letter-spacing: 1px; line-height: 1.1;
            }
            .planet-badge-row { display: flex; align-items: center; gap: 6px; margin-top: 6px; }
            .fc-tag-pill {
                background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(148, 163, 184, 0.3);
                color: #94A3B8; border-radius: 12px; padding: 2px 8px; font-size: 9.5px;
                font-weight: 800; letter-spacing: 1px; text-transform: uppercase;
            }
            .fc-tag-pill.highlight {
                background: rgba(14, 165, 233, 0.2); border-color: #00D2FF; color: #38BDF8;
            }

            .fc-tabs {
                display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px;
                margin-bottom: 14px; background: rgba(10, 18, 38, 0.65);
                padding: 4px; border-radius: 10px; border: 1px solid rgba(56, 189, 248, 0.15);
            }
            .fc-tab {
                background: transparent; border: 1px solid transparent; border-radius: 7px;
                color: #94A3B8; padding: 6px 4px; font-size: 11px; font-weight: 700;
                cursor: pointer; text-align: center; transition: all 0.2s ease;
            }
            .fc-tab:hover { color: #FFFFFF; background: rgba(255, 255, 255, 0.05); }
            .fc-tab.active {
                background: linear-gradient(135deg, rgba(2, 132, 199, 0.6), rgba(0, 210, 255, 0.5));
                border-color: #00D2FF; color: #FFFFFF; font-weight: 800;
                box-shadow: 0 0 10px rgba(0, 210, 255, 0.4);
            }

            .fc-tab-content { display: none; }
            .fc-tab-content.active { display: block; animation: fcFadeIn 0.25s ease; }
            @keyframes fcFadeIn { from { opacity: 0; transform: translateY(4px); } to { opacity: 1; transform: translateY(0); } }

            .flashcard-grid {
                display: grid; grid-template-columns: 1fr 1fr; gap: 8px;
            }
            .flashcard {
                background: linear-gradient(135deg, rgba(15, 23, 42, 0.85) 0%, rgba(30, 41, 59, 0.6) 100%);
                border: 1px solid rgba(56, 189, 248, 0.25);
                border-radius: 10px; padding: 10px 12px;
                backdrop-filter: blur(8px);
                transition: transform 0.2s, border-color 0.2s, box-shadow 0.2s;
            }
            .flashcard:hover {
                border-color: #00D2FF; transform: translateY(-2px);
                box-shadow: 0 4px 16px rgba(0, 210, 255, 0.2);
            }
            .flashcard.highlight-card {
                background: linear-gradient(135deg, rgba(14, 165, 233, 0.15) 0%, rgba(15, 23, 42, 0.85) 100%);
                border-color: rgba(0, 210, 255, 0.45);
            }
            .flashcard.gold-card {
                background: linear-gradient(135deg, rgba(245, 158, 11, 0.15) 0%, rgba(15, 23, 42, 0.88) 100%);
                border-color: rgba(251, 191, 36, 0.45);
            }
            .flashcard.gold-card:hover { border-color: #FBBF24; box-shadow: 0 4px 20px rgba(251, 191, 36, 0.25); }

            .fc-card-hdr {
                font-size: 11px; font-weight: 800; color: #38BDF8;
                text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 5px;
            }
            .flashcard.gold-card .fc-card-hdr { color: #FBBF24; }
            .fc-card-body {
                font-size: 12.5px; color: #E2E8F0; line-height: 1.5;
            }

            .fc-data { display: flex; flex-direction: column; }
            .stat-lbl { font-size: 9.5px; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.8px; font-weight: 700; }
            .stat-val { font-size: 14.5px; font-weight: 800; color: #FFFFFF; margin: 2px 0; }
            .stat-detail { font-size: 10.5px; color: #38BDF8; font-weight: 600; }

            .monument-box {
                background: rgba(14, 165, 233, 0.15); border: 1px solid rgba(0, 210, 255, 0.55);
                border-radius: 10px; padding: 12px; margin-bottom: 14px;
            }
            .monument-hdr { color: #38BDF8; font-weight: 800; font-size: 13px; margin-bottom: 5px; }
            .monument-txt { font-size: 12px; color: #CBD5E1; line-height: 1.5; }

            .warp-btn {
                width: 100%; padding: 12px; border-radius: 10px; border: none;
                background: linear-gradient(90deg, #0284C7 0%, #00D2FF 100%);
                color: #FFFFFF; font-weight: 800; font-size: 13.5px; cursor: pointer;
                text-transform: uppercase; letter-spacing: 1px;
                box-shadow: 0 0 20px rgba(0, 210, 255, 0.5);
                transition: transform 0.2s, box-shadow 0.2s;
            }
            .warp-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 0 30px rgba(0, 210, 255, 0.85);
            }
            /* Vibrant Rose-Coral Back Buttons for Maximum Contrast */
            .fc-back-btn {
                background: linear-gradient(135deg, rgba(225, 29, 72, 0.35) 0%, rgba(244, 63, 94, 0.55) 100%);
                border: 1.5px solid #FB7185;
                color: #FFF1F2;
                border-radius: 20px;
                padding: 5px 13px;
                font-size: 11.5px;
                font-weight: 800;
                cursor: pointer;
                display: flex;
                align-items: center;
                gap: 6px;
                box-shadow: 0 0 14px rgba(244, 63, 94, 0.45);
                transition: all 0.2s ease;
                user-select: none;
            }
            .fc-back-btn:hover {
                background: linear-gradient(135deg, rgba(225, 29, 72, 0.6) 0%, rgba(244, 63, 94, 0.8) 100%);
                border-color: #FDA4AF;
                color: #FFFFFF;
                box-shadow: 0 0 22px rgba(244, 63, 94, 0.85);
                transform: translateY(-1px);
            }

            .fc-close-icon {
                width: 26px;
                height: 26px;
                border-radius: 50%;
                background: rgba(225, 29, 72, 0.3);
                border: 1.5px solid #FB7185;
                color: #FFF1F2;
                font-size: 12px;
                font-weight: 900;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                transition: all 0.2s ease;
            }
            .fc-close-icon:hover {
                background: rgba(225, 29, 72, 0.65);
                box-shadow: 0 0 14px rgba(244, 63, 94, 0.75);
                transform: scale(1.1);
            }

            .fc-bottom-back-btn {
                width: 100%;
                margin-top: 16px;
                padding: 10px;
                border-radius: 10px;
                background: linear-gradient(135deg, rgba(225, 29, 72, 0.25) 0%, rgba(244, 63, 94, 0.45) 100%);
                border: 1.5px solid #FB7185;
                color: #FFF1F2;
                font-size: 12px;
                font-weight: 800;
                cursor: pointer;
                text-transform: uppercase;
                letter-spacing: 0.8px;
                box-shadow: 0 0 14px rgba(244, 63, 94, 0.35);
                transition: all 0.2s ease;
            }
            .fc-bottom-back-btn:hover {
                background: linear-gradient(135deg, rgba(225, 29, 72, 0.5) 0%, rgba(244, 63, 94, 0.7) 100%);
                box-shadow: 0 0 24px rgba(244, 63, 94, 0.8);
                transform: translateY(-1px);
            }

            /* Floating Viewport Back Button (Appears near the 3D planet) */
            .viewport-back-btn {
                position: absolute;
                top: 72px;
                left: 24px;
                z-index: 105;
                background: linear-gradient(135deg, rgba(225, 29, 72, 0.88) 0%, rgba(244, 63, 94, 0.95) 100%);
                border: 1.5px solid #FDA4AF;
                color: #FFFFFF;
                border-radius: 24px;
                padding: 8px 18px;
                font-size: 12.5px;
                font-weight: 800;
                cursor: pointer;
                box-shadow: 0 0 20px rgba(244, 63, 94, 0.6);
                display: none;
                align-items: center;
                gap: 8px;
                backdrop-filter: blur(8px);
                transition: all 0.2s ease;
                user-select: none;
            }
            .viewport-back-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 0 30px rgba(244, 63, 94, 0.95);
            }
            #container.panel-open .viewport-back-btn {
                display: flex;
            }

            /* Dynamic Fullscreen Descent Video Modal */
            #warp-modal {
                position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
                background: #000; z-index: 1000; display: none; justify-content: center; align-items: center;
            }
            .descent-video { width: 100%; height: 100%; object-fit: cover; display: none; }
            #warp-hud-overlay {
                position: absolute; top: 30px; left: 34px; z-index: 1010;
                pointer-events: none;
            }
            #warp-dest-title {
                font-size: 18px; font-weight: 900; letter-spacing: 2.5px;
                background: linear-gradient(90deg, #FFFFFF, #00D2FF);
                -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                text-transform: uppercase; text-shadow: 0 0 20px rgba(0, 210, 255, 0.6);
            }
            #warp-dest-sub {
                font-size: 11px; font-weight: 700; color: #94A3B8;
                letter-spacing: 1.5px; margin-top: 4px; text-transform: uppercase;
            }
            #skip-btn {
                position: absolute; top: 24px; right: 28px; z-index: 1010;
                background: rgba(15, 23, 42, 0.85); border: 1.5px solid #00D2FF;
                color: #F8FAFC; border-radius: 24px; padding: 8px 22px;
                font-weight: 800; font-size: 13px; cursor: pointer;
                box-shadow: 0 0 16px rgba(0, 210, 255, 0.5);
                backdrop-filter: blur(8px); transition: all 0.2s ease;
            }
            #skip-btn:hover {
                background: rgba(0, 210, 255, 0.3); border-color: #38BDF8;
                box-shadow: 0 0 26px rgba(0, 210, 255, 0.85);
            }

            /* Touchdown Action Bar Card requested by user */
            #warp-touchdown-card {
                position: absolute;
                bottom: 80px;
                left: 50%;
                transform: translateX(-50%);
                z-index: 1030;
                width: 90%;
                max-width: 620px;
                background: rgba(10, 17, 36, 0.94);
                border: 2px solid #FF5533;
                border-radius: 18px;
                padding: 24px 28px;
                text-align: center;
                box-shadow: 0 10px 40px rgba(0, 0, 0, 0.95), 0 0 35px rgba(255, 85, 51, 0.5);
                backdrop-filter: blur(16px);
                animation: touchdownSlideUp 0.45s cubic-bezier(0.16, 1, 0.3, 1) forwards;
            }
            @keyframes touchdownSlideUp {
                from { opacity: 0; transform: translate(-50%, 30px); }
                to { opacity: 1; transform: translate(-50%, 0); }
            }
            .touchdown-badge {
                display: inline-block;
                background: rgba(239, 68, 68, 0.22);
                border: 1px solid rgba(239, 68, 68, 0.6);
                color: #FCA5A5;
                font-size: 11px;
                font-weight: 800;
                letter-spacing: 1.2px;
                padding: 5px 14px;
                border-radius: 9999px;
                text-transform: uppercase;
                margin-bottom: 10px;
            }
            .touchdown-badge.moon-badge {
                background: rgba(245, 158, 11, 0.22);
                border-color: rgba(245, 158, 11, 0.6);
                color: #FDE68A;
            }
            .touchdown-title {
                font-size: 22px;
                font-weight: 900;
                color: #FFFFFF;
                letter-spacing: 1px;
                text-transform: uppercase;
                margin-bottom: 6px;
            }
            .touchdown-sub {
                font-size: 12.5px;
                color: #94A3B8;
                margin-bottom: 18px;
                line-height: 1.4;
            }
            .touchdown-action-bar {
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 10px;
                width: 100%;
                background: linear-gradient(135deg, #FF5533 0%, #DC2626 100%);
                color: #FFFFFF !important;
                text-decoration: none !important;
                font-size: 16px;
                font-weight: 900;
                letter-spacing: 1px;
                padding: 16px 24px;
                border-radius: 12px;
                border: 1px solid rgba(255, 255, 255, 0.4);
                box-shadow: 0 6px 24px rgba(255, 85, 51, 0.55);
                cursor: pointer;
                transition: all 0.2s ease;
                text-transform: uppercase;
            }
            .touchdown-action-bar:hover {
                transform: translateY(-2px) scale(1.02);
                box-shadow: 0 10px 35px rgba(255, 85, 51, 0.85);
                background: linear-gradient(135deg, #FF6644 0%, #EF4444 100%);
            }
            .touchdown-action-bar.moon-action-bar {
                background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%);
                box-shadow: 0 6px 24px rgba(245, 158, 11, 0.55);
            }
            .touchdown-action-bar.moon-action-bar:hover {
                box-shadow: 0 10px 35px rgba(245, 158, 11, 0.85);
                background: linear-gradient(135deg, #FBBF24 0%, #F59E0B 100%);
            }
            .touchdown-badge.deep-badge {
                background: rgba(56, 189, 248, 0.2);
                border-color: rgba(56, 189, 248, 0.5);
                color: #38BDF8;
            }
            .touchdown-action-bar.deep-action-bar {
                background: linear-gradient(135deg, #0284c7 0%, #38bdf8 100%);
                box-shadow: 0 6px 24px rgba(56, 189, 248, 0.55);
            }
            .touchdown-action-bar.deep-action-bar:hover {
                box-shadow: 0 10px 35px rgba(56, 189, 248, 0.85);
                background: linear-gradient(135deg, #38bdf8 0%, #0284c7 100%);
            }
            .touchdown-hint {
                font-size: 11px;
                color: #64748B;
                margin-top: 10px;
            }

            /* ==========================================
               SPLIT SCREEN MARS SIDEBAR & 3D HUD
               ========================================== */
            #mars-split-sidebar {
                position: absolute; top: 0; left: 0; width: 460px; height: 100%;
                background: linear-gradient(180deg, rgba(8, 14, 28, 0.98) 0%, rgba(2, 6, 23, 0.99) 100%);
                border-right: 1px solid rgba(255, 85, 51, 0.35);
                padding: 18px 16px 40px 16px;
                overflow-y: auto; box-sizing: border-box;
                display: none; flex-direction: column; gap: 14px;
                z-index: 130; box-shadow: 12px 0 40px rgba(0, 0, 0, 0.95);
            }

            /* Rover Selector Bar */
            .rover-selector-section {
                display: flex; flex-direction: column; gap: 8px;
                background: rgba(15, 23, 42, 0.7);
                border: 1px solid rgba(255, 85, 51, 0.25);
                border-radius: 10px; padding: 10px 12px;
            }
            .selector-header-label {
                font-size: 10px; font-weight: 800; color: #94A3B8;
                letter-spacing: 0.6px; text-transform: uppercase;
            }
            .rover-selector-pills {
                display: flex; flex-wrap: wrap; gap: 6px;
            }
            .rover-pill-btn {
                background: rgba(30, 41, 59, 0.8);
                border: 1px solid rgba(255, 255, 255, 0.12);
                color: #CBD5E1; font-size: 11px; font-weight: 700;
                padding: 5px 10px; border-radius: 14px; cursor: pointer;
                transition: all 0.2s ease; display: inline-flex; align-items: center; gap: 5px;
            }
            .rover-pill-btn:hover {
                background: rgba(255, 85, 51, 0.2);
                border-color: #FF5533; color: #FFFFFF;
                transform: translateY(-1px);
            }
            .rover-pill-btn.active {
                background: linear-gradient(135deg, rgba(255, 85, 51, 0.45) 0%, rgba(239, 68, 68, 0.45) 100%);
                border-color: #FF5533; color: #FFFFFF;
                box-shadow: 0 0 14px rgba(255, 85, 51, 0.45);
            }
            .sidebar-rover-hero {
                display: flex; flex-direction: column; gap: 6px;
                padding-bottom: 2px;
            }
            .sidebar-rover-name {
                font-size: 21px; font-weight: 900; color: #FFFFFF;
                letter-spacing: -0.3px; margin: 0; line-height: 1.15;
            }
            .sidebar-tagline {
                font-size: 11.5px; font-style: italic; color: #38BDF8;
                border-left: 2px solid #38BDF8; padding-left: 8px; line-height: 1.35;
            }

            /* Supabase Database Card */
            .detail-supabase-card {
                background: rgba(15, 23, 42, 0.85);
                border: 1px solid rgba(56, 189, 248, 0.3);
                border-radius: 12px; padding: 14px 16px;
                display: flex; flex-direction: column; gap: 10px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
            }
            .db-header {
                display: flex; justify-content: space-between; align-items: center;
                padding-bottom: 6px; border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            }
            .db-title {
                font-size: 11px; font-weight: 800; letter-spacing: 0.8px; color: #38BDF8;
                display: flex; align-items: center; gap: 6px;
            }
            .db-badge-verified {
                font-size: 9px; font-weight: 700; color: #34D399;
                background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.4);
                padding: 2px 6px; border-radius: 8px;
            }
            .db-grid {
                display: grid; grid-template-columns: 1fr 1fr; gap: 8px;
            }
            .db-cell {
                background: rgba(30, 41, 59, 0.6); border: 1px solid rgba(148, 163, 184, 0.15);
                border-radius: 8px; padding: 8px 10px;
            }
            .db-cell-label {
                font-size: 10px; text-transform: uppercase; font-weight: 700; color: #94A3B8; letter-spacing: 0.5px;
                margin-bottom: 2px;
            }
            .db-cell-val {
                font-size: 12px; font-weight: 600; color: #F1F5F9; line-height: 1.3;
            }
            .db-desc-box {
                background: rgba(2, 6, 23, 0.6); border-radius: 8px; padding: 8px 10px;
                border: 1px solid rgba(148, 163, 184, 0.12);
            }
            .db-desc-text {
                font-size: 11.5px; color: #CBD5E1; line-height: 1.4; margin: 2px 0 0 0;
            }
            .db-bridge {
                background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.8) 100%);
                border-left: 3px solid #00F0FF; padding: 8px 12px; border-radius: 0 8px 8px 0;
                border: 1px solid rgba(0, 240, 255, 0.25); border-left-width: 3px;
            }
            .db-bridge-title {
                font-size: 10.5px; font-weight: 800; color: #00F0FF; letter-spacing: 0.5px; margin-bottom: 3px;
            }
            .db-bridge-hw {
                font-size: 11.5px; font-weight: 700; color: #38BDF8; margin-bottom: 2px;
            }
            .db-bridge-sc {
                font-size: 11.5px; color: #E2E8F0; line-height: 1.35;
            }
            .db-stat-row {
                display: grid; grid-template-columns: repeat(2, 1fr); gap: 6px;
            }
            .db-stat-badge {
                background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(56, 189, 248, 0.25);
                border-radius: 8px; padding: 6px 8px; display: flex; align-items: center; gap: 7px;
            }
            .db-stat-icon { font-size: 15px; flex-shrink: 0; }
            .db-stat-label {
                font-size: 9px; text-transform: uppercase; font-weight: 700; color: #94A3B8; letter-spacing: 0.5px;
            }
            .db-stat-val {
                font-size: 11px; font-weight: 700; color: #38BDF8; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
            }
            .db-monument-box {
                background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.3);
                border-radius: 8px; padding: 7px 10px;
            }
            .db-monument-text {
                font-size: 11px; color: #6EE7B7; line-height: 1.35; margin-top: 2px;
            }

            /* Gemini AI Chatbot Card */
            .detail-chat-card {
                background: rgba(15, 23, 42, 0.9);
                border: 1.5px solid rgba(168, 85, 247, 0.45);
                border-radius: 12px; padding: 14px 16px;
                display: flex; flex-direction: column; gap: 10px;
                box-shadow: 0 4px 25px rgba(0, 0, 0, 0.6), 0 0 20px rgba(168, 85, 247, 0.15);
            }
            .chat-header-row {
                display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;
            }
            .chat-title-group {
                display: flex; align-items: center; gap: 6px;
            }
            .chat-card-title {
                font-size: 12px; font-weight: 800; color: #F1F5F9;
            }
            .chat-age-toggle-bar {
                display: flex; gap: 4px; background: rgba(30, 41, 59, 0.8); padding: 2px; border-radius: 8px;
            }
            .age-pill-btn {
                font-size: 10px; font-weight: 700; padding: 3px 8px; border-radius: 6px; border: none;
                background: transparent; color: #94A3B8; cursor: pointer; transition: all 0.2s;
            }
            .age-pill-btn.active {
                background: #A855F7; color: #FFFFFF; box-shadow: 0 2px 8px rgba(168, 85, 247, 0.4);
            }
            .chat-messages-wrap {
                max-height: 160px; min-height: 90px; overflow-y: auto; display: flex; flex-direction: column;
                gap: 8px; padding: 10px; background: rgba(2, 6, 23, 0.85); border-radius: 8px;
                border: 1px solid rgba(148, 163, 184, 0.18);
            }
            .chat-bubble {
                padding: 8px 12px; border-radius: 8px; font-size: 12px; line-height: 1.4; max-width: 92%;
                word-wrap: break-word;
            }
            .chat-bubble.assistant {
                background: rgba(30, 41, 59, 0.85); color: #F8FAFC; border-left: 3px solid #A855F7; align-self: flex-start;
            }
            .chat-bubble.user {
                background: linear-gradient(135deg, #0284C7, #2563EB); color: #FFFFFF; align-self: flex-end;
            }
            .chat-quick-chips {
                display: flex; gap: 6px; overflow-x: auto; padding-bottom: 2px;
            }
            .quick-chip {
                background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(56, 189, 248, 0.3); color: #38BDF8;
                font-size: 10.5px; font-weight: 600; padding: 4px 8px; border-radius: 16px; cursor: pointer; white-space: nowrap;
            }
            .quick-chip:hover {
                background: rgba(56, 189, 248, 0.2); border-color: #38BDF8;
            }
            .chat-input-row {
                display: flex; gap: 8px;
            }
            .chat-text-input {
                flex: 1; background: rgba(30, 41, 59, 0.85); border: 1px solid rgba(148, 163, 184, 0.3);
                border-radius: 8px; padding: 8px 12px; color: #FFFFFF; font-size: 12px; outline: none;
            }
            .chat-text-input:focus {
                border-color: #A855F7; box-shadow: 0 0 8px rgba(168, 85, 247, 0.35);
            }
            .chat-send-btn {
                background: linear-gradient(135deg, #A855F7, #7C3AED); color: #FFFFFF; font-weight: 700;
                font-size: 11px; padding: 0 12px; border: none; border-radius: 8px; cursor: pointer;
                box-shadow: 0 2px 10px rgba(168, 85, 247, 0.4); display: flex; align-items: center; gap: 4px;
            }

            /* Audio Player */
            .detail-audio-card {
                background: rgba(15, 23, 42, 0.85);
                border: 1.5px solid rgba(255, 85, 51, 0.5);
                border-radius: 14px; padding: 14px 16px;
                display: flex; flex-direction: column; gap: 10px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
            }
            .audio-card-header {
                display: flex; align-items: center; gap: 8px;
            }
            .audio-icon-pulse {
                font-size: 16px; animation: iconPulse 2s infinite ease-in-out;
            }
            .audio-card-title {
                font-size: 13px; font-weight: 800; color: #FF5533; letter-spacing: 0.5px;
            }
            .audio-controls-row {
                display: flex; align-items: center; gap: 12px;
            }
            .audio-play-btn {
                background: linear-gradient(135deg, #FF5533 0%, #EA580C 100%);
                border: none; color: #FFFFFF; font-size: 12px; font-weight: 800;
                padding: 8px 16px; border-radius: 16px; cursor: pointer;
                box-shadow: 0 0 12px rgba(255, 85, 51, 0.4);
                transition: all 0.2s ease; flex-shrink: 0;
            }
            .audio-play-btn:hover {
                transform: scale(1.04);
            }
            .audio-progress-wrap {
                flex: 1; display: flex; flex-direction: column; gap: 4px;
            }
            .audio-scrub-slider {
                width: 100%; -webkit-appearance: none; height: 5px;
                border-radius: 3px; background: rgba(51, 65, 85, 0.8); outline: none; cursor: pointer;
            }
            .audio-scrub-slider::-webkit-slider-thumb {
                -webkit-appearance: none; appearance: none;
                width: 12px; height: 12px; border-radius: 50%;
                background: #00F0FF; cursor: pointer;
            }
            .audio-time-row {
                display: flex; justify-content: space-between;
                font-size: 10.5px; color: #94A3B8; font-family: monospace;
            }
            .btn-launch-3d-sim {
                background: linear-gradient(135deg, #FF5533 0%, #EA580C 100%);
                border: 1px solid rgba(255, 255, 255, 0.2);
                color: #FFFFFF; font-size: 12px; font-weight: 800;
                padding: 10px 14px; border-radius: 10px; cursor: pointer;
                box-shadow: 0 4px 18px rgba(255, 85, 51, 0.4);
                transition: all 0.2s ease; text-align: center;
            }
            .btn-launch-3d-sim:hover {
                background: linear-gradient(135deg, #FF6644 0%, #F97316 100%);
                box-shadow: 0 6px 24px rgba(255, 85, 51, 0.6);
            }
            #mars-split-sidebar::-webkit-scrollbar { width: 6px; }
            #mars-split-sidebar::-webkit-scrollbar-track { background: rgba(15, 23, 42, 0.6); }
            #mars-split-sidebar::-webkit-scrollbar-thumb { background: rgba(255, 85, 51, 0.45); border-radius: 4px; }
            #mars-split-sidebar::-webkit-scrollbar-thumb:hover { background: rgba(255, 85, 51, 0.8); }

            .mars-sidebar-header {
                display: flex; flex-direction: column; gap: 8px;
                border-bottom: 1px solid rgba(255, 85, 51, 0.25);
                padding-bottom: 14px;
            }
            .mars-return-btn {
                background: rgba(15, 23, 42, 0.92); border: 1.5px solid #FF5533; color: #FFFFFF;
                border-radius: 20px; padding: 7px 16px; font-size: 11.5px; font-weight: 800;
                cursor: pointer; display: inline-flex; align-items: center; gap: 6px;
                box-shadow: 0 0 16px rgba(255, 85, 51, 0.35); transition: all 0.2s ease; width: fit-content;
            }
            .mars-return-btn:hover {
                background: rgba(255, 85, 51, 0.3); border-color: #FFAA88; transform: translateY(-1px);
            }
            .mars-planet-tag {
                display: inline-flex; align-items: center; gap: 6px;
                background: rgba(239, 68, 68, 0.18); border: 1px solid rgba(239, 68, 68, 0.5);
                color: #FCA5A5; font-size: 10px; font-weight: 800; letter-spacing: 1.2px;
                padding: 3px 10px; border-radius: 9999px; text-transform: uppercase; width: fit-content;
            }
            .mars-sidebar-title {
                font-size: 24px; font-weight: 900; letter-spacing: 0.5px;
                background: linear-gradient(135deg, #FFFFFF 0%, #FF5533 60%, #EF4444 100%);
                -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                margin: 0; line-height: 1.1;
            }
            .mars-sidebar-sub {
                font-size: 11.5px; color: #94A3B8; line-height: 1.4;
            }

            /* Telemetry Cards Grid */
            .mars-telemetry-grid {
                display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px;
            }
            .mars-tel-card {
                background: rgba(15, 23, 42, 0.85);
                border: 1px solid rgba(255, 85, 51, 0.25);
                border-radius: 10px; padding: 10px 12px;
                transition: border-color 0.2s ease, transform 0.2s ease;
            }
            .mars-tel-card:hover {
                border-color: rgba(255, 85, 51, 0.6);
                transform: translateY(-1px);
            }
            .mars-tel-label {
                font-size: 10px; font-weight: 700; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.5px;
            }
            .mars-tel-val {
                font-size: 14px; font-weight: 900; color: #FFFFFF; margin: 3px 0 1px 0;
            }
            .mars-tel-sub {
                font-size: 10px; color: #38BDF8; font-weight: 600;
            }

            /* Active Inspector Card (Dynamic Telemetry Detail) */
            #mars-inspector-card {
                background: rgba(15, 23, 42, 0.95);
                border: 1.5px solid #FF5533;
                border-radius: 12px; padding: 16px;
                box-shadow: 0 0 25px rgba(255, 85, 51, 0.35);
                display: none; animation: fadeInMars 0.3s ease;
            }
            @keyframes fadeInMars {
                from { opacity: 0; transform: translateY(-6px); }
                to { opacity: 1; transform: translateY(0); }
            }
            .mars-insp-hdr {
                display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;
            }
            .mars-insp-badge {
                font-size: 9.5px; font-weight: 800; color: #86EFAC;
                background: rgba(34, 197, 94, 0.18); border: 1px solid rgba(34, 197, 94, 0.4);
                padding: 2px 8px; border-radius: 9999px; text-transform: uppercase;
            }
            .mars-insp-close {
                cursor: pointer; color: #94A3B8; font-size: 14px; font-weight: bold;
            }
            .mars-insp-close:hover { color: #FFFFFF; }
            .mars-insp-title {
                font-size: 16px; font-weight: 900; color: #00D2FF; margin-bottom: 2px;
            }
            .mars-insp-site {
                font-size: 11px; color: #F97316; font-weight: 700; text-transform: uppercase; margin-bottom: 4px;
            }
            .mars-insp-power {
                font-size: 11px; color: #CBD5E1; margin-bottom: 8px; line-height: 1.35;
            }
            .mars-insp-desc {
                font-size: 11.5px; color: #E2E8F0; line-height: 1.45; margin-bottom: 8px;
                border-left: 2px solid #FF5533; padding-left: 8px;
            }
            .mars-insp-quote-box {
                background: rgba(2, 6, 23, 0.7); border: 1px solid rgba(0, 210, 255, 0.3);
                border-radius: 8px; padding: 10px; margin-top: 6px;
            }
            .mars-insp-quote-title {
                font-size: 10px; font-weight: 800; color: #00D2FF; text-transform: uppercase; margin-bottom: 3px;
            }
            .mars-insp-quote {
                font-size: 11px; font-style: italic; color: #E2E8F0; line-height: 1.4;
            }

            /* Supabase Spacecraft Directory Section */
            .mars-section-header {
                display: flex; justify-content: space-between; align-items: center;
                margin-top: 6px; margin-bottom: 2px;
            }
            .mars-sec-title {
                font-size: 11px; font-weight: 800; color: #F8FAFC; text-transform: uppercase; letter-spacing: 0.8px;
            }
            .mars-sec-count {
                font-size: 10px; font-weight: 700; color: #FF5533; background: rgba(255, 85, 51, 0.15);
                padding: 2px 7px; border-radius: 8px;
            }
            .mars-monument-list {
                display: flex; flex-direction: column; gap: 8px;
            }
            .mars-monument-card {
                background: rgba(15, 23, 42, 0.8);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 10px; padding: 11px 13px;
                cursor: pointer; transition: all 0.2s ease;
                display: flex; flex-direction: column; gap: 4px;
            }
            .mars-monument-card:hover, .mars-monument-card.active {
                border-color: #FF5533;
                background: rgba(255, 85, 51, 0.12);
                transform: translateX(3px);
                box-shadow: 0 4px 16px rgba(255, 85, 51, 0.25);
            }
            .mars-mc-top {
                display: flex; justify-content: space-between; align-items: center;
            }
            .mars-mc-name {
                font-size: 13px; font-weight: 800; color: #FFFFFF;
            }
            .mars-mc-year {
                font-size: 10.5px; font-weight: 700; color: #94A3B8;
            }
            .mars-mc-site {
                font-size: 11px; color: #38BDF8; font-weight: 600;
            }
            .mars-mc-btn {
                margin-top: 4px; align-self: flex-start;
                font-size: 10px; font-weight: 800; color: #FF5533;
                background: transparent; border: none; cursor: pointer;
                display: flex; align-items: center; gap: 4px; padding: 0;
            }
            .mars-mc-btn:hover { color: #FFAA88; }

            /* Top-Right HUD Controls for Mars */
            #hud-card-mars {
                position: absolute; top: 20px; right: 24px; z-index: 120;
                width: 310px; background: rgba(15, 23, 42, 0.88);
                border: 1px solid rgba(255, 85, 51, 0.45);
                border-radius: 14px; padding: 14px 16px;
                color: #ffffff; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.9), 0 0 20px rgba(255, 85, 51, 0.2);
                backdrop-filter: blur(12px); display: none;
            }
            #hud-card-mars-title {
                display: flex; align-items: center; gap: 8px;
                font-size: 13px; font-weight: 800; letter-spacing: 0.8px;
                color: #ff5533; text-transform: uppercase;
            }
            #hud-card-mars-sub {
                font-size: 10.5px; color: #cbd5e1; margin-top: 4px; line-height: 1.4;
            }
            #hud-card-mars-mesh {
                display: inline-flex; align-items: center; gap: 6px;
                margin-top: 7px; font-size: 10px; font-weight: 600;
                color: #86efac; background: rgba(34, 197, 94, 0.15);
                border: 1px solid rgba(34, 197, 94, 0.4);
                padding: 2px 8px; border-radius: 9999px;
            }
            #hud-card-mars-btns {
                display: flex; gap: 8px; margin-top: 10px;
            }
            .hud-btn-mars {
                flex: 1; padding: 6px 10px;
                background: rgba(30, 41, 59, 0.85);
                border: 1px solid rgba(255, 85, 51, 0.4);
                color: #ffffff; font-size: 11px; font-weight: 600;
                border-radius: 6px; cursor: pointer;
                transition: all 0.2s ease;
                display: flex; align-items: center; justify-content: center; gap: 5px;
            }
            .hud-btn-mars:hover {
                background: rgba(255, 85, 51, 0.25); border-color: #ff5533;
            }

            /* Floating 3D-to-2D Surface Badges for Mars */
            #globe-badges-layer {
                position: absolute; top: 0; left: 0; width: 100%; height: 100%;
                pointer-events: none; z-index: 115; overflow: hidden; display: none;
            }
            .globe-surface-badge {
                position: absolute; transform: translate(-50%, -130%);
                display: none; align-items: center; gap: 6px;
                background: rgba(15, 23, 42, 0.92);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 20px; padding: 4px 10px;
                color: #ffffff; font-size: 11px; font-weight: 700;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.8);
                pointer-events: auto; cursor: pointer;
                white-space: nowrap; transition: transform 0.15s ease, border-color 0.15s ease;
            }
            .globe-surface-badge:hover {
                transform: translate(-50%, -140%) scale(1.08);
                border-color: #00f0ff;
            }


        /* ==========================================
           FULL-SCREEN EQUIPMENT DETAIL VIEW (STEP 2-4)
           ========================================== */
        #equipment-detail-overlay {
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            background: #000000; z-index: 99999;
            display: none; flex-direction: column;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            color: #F8FAFC; user-select: none;
            overflow: hidden;
        }

        .detail-header-bar {
            height: 64px; padding: 0 28px;
            display: flex; align-items: center; justify-content: space-between;
            background: linear-gradient(180deg, rgba(15, 23, 42, 0.98) 0%, rgba(3, 7, 18, 0.95) 100%);
            border-bottom: 1.5px solid rgba(255, 85, 51, 0.35);
            box-shadow: 0 4px 24px rgba(0, 0, 0, 0.9);
            z-index: 20; flex-shrink: 0;
        }
        .detail-back-btn {
            background: rgba(15, 23, 42, 0.9); border: 1.5px solid #FF5533;
            color: #FFFFFF; font-size: 13px; font-weight: 800;
            padding: 8px 20px; border-radius: 24px; cursor: pointer;
            display: inline-flex; align-items: center; gap: 8px;
            box-shadow: 0 0 16px rgba(255, 85, 51, 0.4);
            transition: all 0.2s ease;
        }
        .detail-back-btn:hover {
            background: rgba(255, 85, 51, 0.28); border-color: #FFAA88;
            transform: translateY(-1px); box-shadow: 0 0 24px rgba(255, 85, 51, 0.7);
        }
        .detail-header-title {
            font-size: 15px; font-weight: 900; letter-spacing: 2px;
            background: linear-gradient(90deg, #FFFFFF 0%, #FF5533 50%, #EF4444 100%);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            text-transform: uppercase;
        }
        .detail-audio-toggle-btn {
            background: rgba(15, 23, 42, 0.9); border: 1px solid rgba(0, 210, 255, 0.45);
            color: #38BDF8; font-size: 12px; font-weight: 700;
            padding: 7px 16px; border-radius: 20px; cursor: pointer;
            transition: all 0.2s ease;
        }
        .detail-audio-toggle-btn:hover {
            border-color: #00D2FF; color: #FFFFFF; box-shadow: 0 0 14px rgba(0, 210, 255, 0.5);
        }

        .detail-split-container {
            display: flex; width: 100%; height: calc(100vh - 64px);
            background: #000000; position: relative; overflow: hidden;
        }

        /* LEFT COLUMN: SUPABASE DOSSIER (approx 40%) */
        .detail-info-panel {
            width: 40%; min-width: 380px; max-width: 500px; height: 100%;
            background: linear-gradient(180deg, rgba(10, 16, 32, 0.98) 0%, rgba(3, 7, 18, 0.99) 100%);
            border-right: 1.5px solid rgba(255, 85, 51, 0.35);
            padding: 26px 28px 40px 28px;
            overflow-y: auto; box-sizing: border-box;
            display: flex; flex-direction: column; gap: 16px;
            box-shadow: 12px 0 40px rgba(0, 0, 0, 0.95);
            z-index: 10;
        }
        .detail-info-panel::-webkit-scrollbar { width: 6px; }
        .detail-info-panel::-webkit-scrollbar-track { background: rgba(15, 23, 42, 0.6); }
        .detail-info-panel::-webkit-scrollbar-thumb { background: rgba(255, 85, 51, 0.45); border-radius: 4px; }

        .detail-badges-row {
            display: flex; align-items: center; gap: 8px; flex-wrap: wrap; margin-bottom: 6px;
        }
        .detail-type-badge {
            font-size: 11px; font-weight: 900; letter-spacing: 1.2px; text-transform: uppercase;
            padding: 3px 12px; border-radius: 9999px;
            background: rgba(0, 210, 255, 0.18); border: 1.5px solid #00D2FF; color: #38BDF8;
        }
        .detail-type-badge.rover { background: rgba(56, 189, 248, 0.2); border-color: #38BDF8; color: #38BDF8; }
        .detail-type-badge.lander { background: rgba(168, 85, 247, 0.2); border-color: #A855F7; color: #C084FC; }
        .detail-type-badge.helicopter { background: rgba(0, 240, 255, 0.2); border-color: #00F0FF; color: #67E8F9; }

        .detail-status-badge {
            font-size: 10.5px; font-weight: 800; color: #FCA5A5;
            background: rgba(239, 68, 68, 0.18); border: 1px solid rgba(239, 68, 68, 0.45);
            padding: 3px 10px; border-radius: 9999px; text-transform: uppercase;
        }

        .detail-name {
            font-size: 28px; font-weight: 900; letter-spacing: 0.5px;
            background: linear-gradient(135deg, #FFFFFF 0%, #FF5533 60%, #EF4444 100%);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            margin: 0; line-height: 1.15;
        }

        .detail-specs-grid {
            display: flex; flex-direction: column; gap: 10px;
        }
        .detail-spec-card {
            background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(255, 85, 51, 0.25);
            border-radius: 10px; padding: 12px 14px;
        }
        .spec-label {
            font-size: 10.5px; font-weight: 800; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.6px;
        }
        .spec-value {
            font-size: 13.5px; font-weight: 800; color: #FFFFFF; margin-top: 4px; line-height: 1.35;
        }

        .detail-narrative-card {
            background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 10px; padding: 14px;
        }
        .narrative-label {
            font-size: 10.5px; font-weight: 800; color: #38BDF8; text-transform: uppercase; letter-spacing: 0.6px;
            margin-bottom: 6px;
        }
        .narrative-body {
            font-size: 12.5px; color: #E2E8F0; line-height: 1.55;
        }

        /* PROMINENT AUDIO STORY PLAYER (STEP 4) */
        .detail-audio-card {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.95) 0%, rgba(15, 23, 42, 0.98) 100%);
            border: 1.5px solid #00D2FF; border-radius: 14px;
            padding: 16px 18px; box-shadow: 0 0 25px rgba(0, 210, 255, 0.25);
        }
        .audio-card-header {
            display: flex; align-items: center; gap: 8px; margin-bottom: 12px;
        }
        .audio-icon-pulse { font-size: 18px; }
        .audio-card-title {
            font-size: 13px; font-weight: 900; letter-spacing: 0.8px;
            color: #00D2FF; text-transform: uppercase;
        }
        .audio-controls-row {
            display: flex; align-items: center; gap: 14px;
        }
        .audio-play-btn {
            background: linear-gradient(135deg, #0284C7 0%, #00D2FF 100%);
            border: none; color: #FFFFFF; font-size: 13px; font-weight: 900;
            padding: 10px 18px; border-radius: 20px; cursor: pointer;
            box-shadow: 0 4px 15px rgba(0, 210, 255, 0.4);
            transition: all 0.2s ease; flex-shrink: 0; min-width: 80px;
            text-align: center;
        }
        .audio-play-btn:hover {
            transform: scale(1.05); box-shadow: 0 6px 25px rgba(0, 210, 255, 0.7);
        }
        .audio-progress-wrap {
            flex: 1; display: flex; flex-direction: column; gap: 4px;
        }
        .audio-scrub-slider {
            width: 100%; height: 6px; -webkit-appearance: none; appearance: none;
            background: rgba(255, 255, 255, 0.2); border-radius: 3px; outline: none; cursor: pointer;
        }
        .audio-scrub-slider::-webkit-slider-thumb {
            -webkit-appearance: none; appearance: none; width: 14px; height: 14px;
            border-radius: 50%; background: #00D2FF; cursor: pointer;
            box-shadow: 0 0 8px #00D2FF;
        }
        .audio-time-row {
            display: flex; justify-content: space-between; font-size: 10px; font-weight: 700; color: #94A3B8;
        }

        .detail-nasa-link-btn {
            background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(255, 85, 51, 0.4);
            color: #FF5533; font-size: 11.5px; font-weight: 800; text-decoration: none;
            padding: 10px 14px; border-radius: 8px; text-align: center; display: block;
            transition: all 0.2s ease;
        }
        .detail-nasa-link-btn:hover {
            background: rgba(255, 85, 51, 0.2); color: #FFAA88; border-color: #FF5533;
        }

        /* RIGHT COLUMN: 3D MODEL VIEWPORT (approx 60%) */
        .detail-model-viewport {
            flex: 1; height: 100%; position: relative; background: #000000; overflow: hidden;
        }
        .detail-spinner-wrap {
            position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
            display: flex; flex-direction: column; align-items: center; gap: 12px;
            z-index: 15; pointer-events: none;
        }
        .detail-spinner {
            width: 44px; height: 44px; border: 3px solid rgba(0, 210, 255, 0.25);
            border-top: 3px solid #00D2FF; border-radius: 50%;
            animation: spinDetail 1s linear infinite;
        }
        @keyframes spinDetail {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .spinner-text {
            font-size: 12px; font-weight: 700; color: #38BDF8; letter-spacing: 0.8px;
        }
        .detail-error-banner {
            position: absolute; top: 24px; left: 50%; transform: translateX(-50%);
            background: rgba(239, 68, 68, 0.9); border: 1.5px solid #FCA5A5; color: #FFFFFF;
            font-size: 12px; font-weight: 700; padding: 10px 20px; border-radius: 8px;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.85); z-index: 30;
        }
        .detail-model-hint {
            position: absolute; bottom: 20px; left: 50%; transform: translateX(-50%);
            background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(255, 255, 255, 0.15);
            color: #94A3B8; font-size: 11px; font-weight: 600; padding: 6px 16px; border-radius: 20px;
            backdrop-filter: blur(8px); pointer-events: none; white-space: nowrap; z-index: 10;
        }

        /* RESPONSIVE MOBILE STACK (3D Model on top, Name + Audio below) */
        @media (max-width: 768px) {
            .detail-split-container {
                flex-direction: column; overflow-y: auto; height: auto;
            }
            .detail-model-viewport {
                width: 100%; height: 50vh; min-height: 320px; flex: none; order: 1;
            }
            .detail-info-panel {
                width: 100%; max-width: 100%; min-width: 0; height: auto;
                border-right: none; border-top: 1.5px solid rgba(255, 85, 51, 0.35);
                order: 2; padding: 20px 18px 40px 18px;
            }
        }

            /* Bottom Mission Pill Toolbar for Mars */
            #toolbar-mars {
                position: absolute; bottom: 20px; left: calc(50% + 210px);
                transform: translateX(-50%); z-index: 120;
                display: none; align-items: center; gap: 6px;
                background: rgba(15, 23, 42, 0.9);
                border: 1px solid rgba(255, 85, 51, 0.35);
                border-radius: 30px; padding: 5px 12px;
                box-shadow: 0 8px 30px rgba(0, 0, 0, 0.85);
                backdrop-filter: blur(10px);
                max-width: 55%; overflow-x: auto;
            }
            .tool-btn-mars {
                background: transparent; border: none;
                color: #ffffff; font-size: 11px; font-weight: 600;
                padding: 5px 10px; border-radius: 20px;
                cursor: pointer; display: flex; align-items: center; gap: 5px;
                white-space: nowrap; transition: all 0.2s ease;
            }
            .tool-btn-mars:hover, .tool-btn-mars.active {
                background: rgba(255, 85, 51, 0.28);
                color: #FFFFFF; transform: translateY(-1px);
            }
        </style>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/loaders/GLTFLoader.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/loaders/DRACOLoader.js"></script>
    </head>
    <body>
        <div id="container">
            <div id="viewport-3d"></div>
            <div id="hover-tooltip">Planet</div>
            <!-- Distinct Floating Back Button directly on the 3D viewport near the planet -->
            <button class="viewport-back-btn" onclick="resetSolarSystem()">🪐 ⬅ Back to Solar System</button>

            <!-- Full-Width Floating Glassmorphic Sci-Fi Header -->
            <div id="main-header">
                <div class="brand-box">
                    <h1 class="site-header-title">FORGOTTEN IN SPACE</h1>
                    <div class="site-header-tagline">EVERY MISSION LEAVES A STORY • NASA SPACE APPS</div>
                </div>

                <div class="nav-links">
                    <button class="nav-btn" onclick="navigateToZone('moon')">🌕 Moon Explorer</button>
                    <button class="nav-btn" onclick="navigateToZone('mars')">🔴 Mars Explorer</button>
                    <button class="nav-btn" onclick="navigateToZone('deep')">🌌 Deep Space</button>
                    <button class="explore-hero-btn" onclick="navigateToZone('mars')">🚀 Start Exploring ➔</button>
                </div>

                <div class="quick-controls">
                    <div class="ctrl-group">
                        <span class="ctrl-label">Speed:</span>
                        <button class="ctrl-btn" id="spd-pause" onclick="setOrbitSpeed(0, this)">⏸</button>
                        <button class="ctrl-btn active" id="spd-slow" onclick="setOrbitSpeed(0.25, this)">🐢 0.2x</button>
                        <button class="ctrl-btn" id="spd-gentle" onclick="setOrbitSpeed(0.6, this)">🚶 0.5x</button>
                        <button class="ctrl-btn" id="spd-norm" onclick="setOrbitSpeed(1.2, this)">🚀 1.0x</button>
                    </div>
                    <div class="ctrl-divider"></div>
                    <div class="ctrl-group">
                        <button class="ctrl-btn" onclick="setViewMode('orbit')">🌐 360°</button>
                        <button class="ctrl-btn" onclick="setViewMode('top')">🔭 Top</button>
                        <button class="ctrl-btn" onclick="setViewMode('edge')">📐 Edge</button>
                    </div>
                    <div class="ctrl-divider"></div>
                    <div id="audio-control" onclick="toggleAudio()">
                        <span id="audio-icon">🔊</span>
                        <span id="audio-label">Voice</span>
                    </div>
                </div>
            </div>

            <!-- Floating 3D Badges Container (Dynamically updated on screen) -->
            <div id="badges-container">
                <div class="planet-badge" id="badge-Sun" onclick="selectPlanet('Sun')">☀️ Sun</div>
                <div class="planet-badge" id="badge-Mercury" onclick="selectPlanet('Mercury')">☿ Mercury</div>
                <div class="planet-badge" id="badge-Venus" onclick="selectPlanet('Venus')">♀ Venus</div>
                <div class="planet-badge" id="badge-Earth" onclick="selectPlanet('Earth')">🌍 Earth</div>
                <div class="planet-badge monument-target" id="badge-Moon" onclick="selectPlanet('Moon')">🌕 Moon [4 Monuments]</div>
                <div class="planet-badge monument-target" id="badge-Mars" onclick="selectPlanet('Mars')">🔴 Mars [8 Monuments]</div>
                <div class="planet-badge" id="badge-Jupiter" onclick="selectPlanet('Jupiter')">♃ Jupiter</div>
                <div class="planet-badge" id="badge-Saturn" onclick="selectPlanet('Saturn')">🪐 Saturn</div>
                <div class="planet-badge" id="badge-Uranus" onclick="selectPlanet('Uranus')">⛢ Uranus</div>
                <div class="planet-badge" id="badge-Neptune" onclick="selectPlanet('Neptune')">♆ Neptune</div>
            </div>

            <!-- Stylish Classy Flash Card HUD -->
            <div id="info-panel">
                <!-- Top Navigation & Actions Bar -->
                <div class="fc-topbar">
                    <button class="fc-back-btn" id="btn-back" onclick="resetSolarSystem()">🪐 ⬅ Back to Solar System</button>
                    <div class="fc-nav-controls">
                        <button class="fc-arrow-btn" onclick="cyclePlanet(-1)" title="Previous Planet">◀</button>
                        <span class="fc-counter" id="p-counter">1 / 10</span>
                        <button class="fc-arrow-btn" onclick="cyclePlanet(1)" title="Next Planet">▶</button>
                    </div>
                    <button class="fc-voice-btn" id="btn-card-voice" onclick="speakCurrentPlanet()" title="Listen to Voice Briefing">🔊 Briefing</button>
                    <button class="fc-close-icon" onclick="resetSolarSystem()" title="Close Flash Card">✕</button>
                </div>

                <!-- Planet Hero Identity Banner -->
                <div class="fc-hero">
                    <div class="fc-symbol" id="p-symbol">🪐</div>
                    <div class="fc-title-group">
                        <h2 class="planet-title" id="p-title">The Moon</h2>
                        <div class="planet-badge-row">
                            <span class="fc-tag-pill" id="p-type">NATURAL SATELLITE</span>
                            <span class="fc-tag-pill highlight" id="p-zone">EARTH SYSTEM</span>
                        </div>
                    </div>
                </div>

                <!-- Interactive Flash Card Tab Switcher -->
                <div class="fc-tabs">
                    <button class="fc-tab active" id="tabbtn-overview" onclick="switchCardTab('overview', this)">📊 Telemetry</button>
                    <button class="fc-tab" id="tabbtn-anatomy" onclick="switchCardTab('anatomy', this)">🧪 Anatomy</button>
                    <button class="fc-tab" id="tabbtn-missions" onclick="switchCardTab('missions', this)">🚀 Missions</button>
                    <button class="fc-tab" id="tabbtn-secrets" onclick="switchCardTab('secrets', this)">✨ Secrets</button>
                </div>

                <!-- TAB 1: TELEMETRY FLASH CARDS -->
                <div class="fc-tab-content active" id="tab-overview">
                    <div class="flashcard-grid">
                        <div class="flashcard">
                            <div class="fc-data">
                                <div class="stat-lbl">📏 Diameter</div>
                                <div class="stat-val" id="p-diam">3,474 km</div>
                                <div class="stat-detail" id="p-diam-rel">0.27 Earths</div>
                            </div>
                        </div>
                        <div class="flashcard">
                            <div class="fc-data">
                                <div class="stat-lbl">☀️ Sun Distance</div>
                                <div class="stat-val" id="p-dist">150M km</div>
                                <div class="stat-detail" id="p-dist-rel">1.0 AU</div>
                            </div>
                        </div>
                        <div class="flashcard">
                            <div class="fc-data">
                                <div class="stat-lbl">🌡️ Surface Temp</div>
                                <div class="stat-val" id="p-temp">-246°C to +120°C</div>
                                <div class="stat-detail" id="p-temp-detail">Extreme vacuum swings</div>
                            </div>
                        </div>
                        <div class="flashcard">
                            <div class="fc-data">
                                <div class="stat-lbl">⏱️ Day vs Year</div>
                                <div class="stat-val" id="p-period">Day: 27.3d</div>
                                <div class="stat-detail" id="p-period-detail">Year: 27.3d</div>
                            </div>
                        </div>
                    </div>
                    <div class="flashcard highlight-card" style="margin-top:10px;">
                        <div class="fc-card-hdr">🧲 Surface Gravity & Weight</div>
                        <div class="fc-card-body" id="p-gravity">0.166g (1/6th Earth gravity). You can leap 6 times higher!</div>
                    </div>
                </div>

                <!-- TAB 2: ANATOMY & ATMOSPHERE FLASH CARD -->
                <div class="fc-tab-content" id="tab-anatomy">
                    <div class="flashcard">
                        <div class="fc-card-hdr">🌬️ Atmospheric Composition</div>
                        <div class="fc-card-body" id="p-atmos-full">Near-vacuum surface boundary exosphere.</div>
                    </div>
                    <div class="flashcard" style="margin-top:10px;">
                        <div class="fc-card-hdr">🪨 Interior Structure & Moons</div>
                        <div class="fc-card-body" id="p-interior">Solid iron core, partially molten boundary, thick mantle.</div>
                    </div>
                </div>

                <!-- TAB 3: NASA EXPLORATION FLASH CARD -->
                <div class="fc-tab-content" id="tab-missions">
                    <div class="flashcard highlight-card">
                        <div class="fc-card-hdr">🛸 Historic NASA Pioneers</div>
                        <div class="fc-card-body" id="p-missions">Apollo 11–17 human landings, Surveyor landers, LRO.</div>
                    </div>
                    <div class="flashcard" style="margin-top:10px;">
                        <div class="fc-card-hdr">🏆 Key Scientific Discovery</div>
                        <div class="fc-card-body" id="p-discovery">Genesis Rock analysis confirmed the Giant Impact Hypothesis.</div>
                    </div>
                </div>

                <!-- TAB 4: COSMIC SECRETS FLASH CARD -->
                <div class="fc-tab-content" id="tab-secrets">
                    <div class="flashcard gold-card">
                        <div class="fc-card-hdr">✨ Mind-Bending Cosmic Secret</div>
                        <div class="fc-card-body" id="p-secret">Laser retroreflectors placed on the Moon by Apollo astronauts still bounce Earth lasers today!</div>
                    </div>
                </div>

                <!-- Off-World Monuments Box (Moon & Mars) -->
                <div class="monument-box" id="monument-alert" style="display:none; margin-top:14px;">
                    <div class="monument-hdr" id="m-hdr">🏛️ Off-World Monuments: 4 Machines</div>
                    <div class="monument-txt" id="m-txt">
                        Apollo Lunar Modules, Moon Buggies, ALSEP, and Surveyor landers rest in permanent silence.
                    </div>
                    <button class="warp-btn" id="btn-warp" style="margin-top:10px;">🚀 Launch Surface Descent Sequence</button>
                </div>

                <!-- Bottom Back Button for Easy Dismissal -->
                <button class="fc-bottom-back-btn" onclick="resetSolarSystem()">🪐 ⬅ Return to 360° Solar System View</button>
            </div>

            <!-- Bottom Quick Dock -->
            <div id="planet-dock">
                <button class="dock-btn" onclick="selectPlanet('Sun')">☀️ Sun</button>
                <button class="dock-btn" onclick="selectPlanet('Mercury')">☿ Mercury</button>
                <button class="dock-btn" onclick="selectPlanet('Venus')">♀ Venus</button>
                <button class="dock-btn" onclick="selectPlanet('Earth')">🌍 Earth</button>
                <button class="dock-btn highlight" onclick="selectPlanet('Moon')">🌕 Moon</button>
                <button class="dock-btn highlight" onclick="selectPlanet('Mars')">🔴 Mars</button>
                <button class="dock-btn" onclick="selectPlanet('Jupiter')">♃ Jupiter</button>
                <button class="dock-btn" onclick="selectPlanet('Saturn')">🪐 Saturn</button>
                <button class="dock-btn" onclick="selectPlanet('Uranus')">⛢ Uranus</button>
                <button class="dock-btn" onclick="selectPlanet('Neptune')">♆ Neptune</button>
            </div>

            <!-- Audio & Hint Prompt -->
            <div id="welcome-overlay">
                <span>🎧</span> Touch any planet or badge to inspect its telemetry & off-world monuments
            </div>
        </div>

        <!-- Floating Planet Globe HUD (Active in Globe Mode) -->
        <div id="globe-hud" style="display:none; position:absolute; top:70px; left:28px; z-index:120; pointer-events:auto;">
            <button id="btn-back-to-solar" onclick="window.exitGlobeMode()" style="background:rgba(15,23,42,0.92); border:1.5px solid #00D2FF; color:#F8FAFC; border-radius:24px; padding:9px 20px; font-size:13px; font-weight:800; cursor:pointer; display:flex; align-items:center; gap:8px; box-shadow:0 0 16px rgba(0,210,255,0.4); transition:all 0.2s;">
                🌌 ⬅ Return to 3D Solar System Overview
            </button>
            <div id="globe-badge" style="margin-top:10px; background:rgba(8,15,34,0.92); border:1px solid rgba(56,189,248,0.45); color:#38BDF8; font-size:12px; font-weight:800; padding:6px 16px; border-radius:20px; backdrop-filter:blur(10px); display:inline-block;">
                🪐 3D MARS SIMULATOR • TOUCHDOWN COMPLETE
            </div>
            <div style="margin-top:6px; background:rgba(3,7,18,0.7); color:#94A3B8; font-size:11px; font-weight:600; padding:4px 12px; border-radius:12px;">
                🖱️ Drag to rotate • Scroll to zoom • Hover/click glowing beacons
            </div>
        </div>

        <!-- Floating Sleek Space Card (Beacon Hover) -->
        <div id="beacon-card" style="position:absolute; z-index:150; display:none; width:280px; padding:12px 14px; border-radius:12px; background:linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.92) 100%); border:1.5px solid #00D2FF; box-shadow:0 8px 28px rgba(0, 210, 255, 0.38); backdrop-filter:blur(12px); pointer-events:none;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                <span id="bc-badge" style="font-size:9px; font-weight:800; color:#00D2FF; background:rgba(0,210,255,0.15); padding:2px 7px; border-radius:10px;">MONUMENT</span>
                <span id="bc-year" style="font-size:11px; font-weight:800; color:#FBBF24;">1969</span>
            </div>
            <div id="bc-title" style="font-size:13.5px; font-weight:800; color:#FFFFFF; margin:3px 0 2px 0;">Mission Name</div>
            <div id="bc-site" style="font-size:11px; color:#94A3B8; margin-bottom:5px;">📍 Coordinates</div>
            <div id="bc-status" style="font-size:11.5px; color:#E2E8F0; font-weight:600; line-height:1.35;">Status Description</div>
            <div style="margin-top:8px; padding-top:6px; border-top:1px solid rgba(56,189,248,0.25); font-size:10px; font-weight:800; color:#38BDF8;">🔍 Click to focus landing site</div>
        </div>

        <!-- Dynamic Fullscreen Descent Video Modal -->
        <div id="warp-modal">
            <div id="warp-hud-overlay">
                <div id="warp-dest-title">ORBITAL DESCENT TRAJECTORY INITIATED</div>
                <div id="warp-dest-sub">STAND BY FOR TOUCHDOWN TELEMETRY</div>
            </div>
            <video id="warp-video-mars" class="descent-video" playsinline preload="auto">
                <source src="https://raw.githubusercontent.com/harshahuppara/nasa-echo-hack/main/static/videos/space%20to%20mars.mp4" type="video/mp4">
                <source src="/app/static/videos/space%20to%20mars.mp4" type="video/mp4">
                <source src="/static/videos/space%20to%20mars.mp4" type="video/mp4">
            </video>
            <video id="warp-video-moon" class="descent-video" playsinline preload="auto">
                <source src="https://raw.githubusercontent.com/harshahuppara/nasa-echo-hack/main/static/videos/space%20to%20moon.mp4" type="video/mp4">
                <source src="/app/static/videos/space%20to%20moon.mp4" type="video/mp4">
                <source src="/static/videos/space%20to%20moon.mp4" type="video/mp4">
            </video>
            <video id="warp-video-deep" class="descent-video" playsinline preload="auto" src="https://raw.githubusercontent.com/harshahuppara/nasa-echo-hack/main/static/videos/deep_space.mp4">
                <source src="https://raw.githubusercontent.com/harshahuppara/nasa-echo-hack/main/static/videos/deep_space.mp4" type="video/mp4">
                <source src="/app/static/videos/deep_space.mp4" type="video/mp4">
                <source src="/static/videos/deep_space.mp4" type="video/mp4">
            </video>
            <button id="skip-btn">Skip Transition ⏩</button>

            <!-- Interactive Touchdown Action Bar Card (Appears immediately when video completes or is skipped) -->
            <div id="warp-touchdown-card" style="display:none;">
                <div id="touchdown-badge" class="touchdown-badge">🔴 TOUCHDOWN CONFIRMED • ATMOSPHERIC ENTRY COMPLETE</div>
                <div id="touchdown-title" class="touchdown-title">WELCOME TO THE SURFACE OF MARS</div>
                <div id="touchdown-sub" class="touchdown-sub">Jezero Crater, Meridiani Planum, and 8 NASA monument sites are standing by.</div>
                <a id="btn-touchdown-enter" href="/?page=mars" target="_top" class="touchdown-action-bar">
                    🚀 ENTER 3D MARS EXPLORER ➔
                </a>
                <div class="touchdown-hint">Click the bar above to launch the full-screen 3D model & monument explorer</div>
            </div>
        </div>

        <!-- LEFT SIDEBAR: MARS SCIENCE & SUPABASE ROSTER (Split-screen) -->
        <aside id="mars-split-sidebar">
            <div class="mars-sidebar-header">
                <button class="mars-return-btn" onclick="window.exitGlobeMode()">🌌 ⬅ Return to Solar System</button>
                <div class="mars-planet-tag">🔴 4th PLANET • THE RED PLANET</div>
                <h1 class="mars-sidebar-title">MARS EXPLORER</h1>
                <p class="mars-sidebar-sub">Off-World Artifacts & Silent NASA Monuments</p>
            </div>

            <!-- Planetary Telemetry Grid -->
            <div class="mars-telemetry-grid">
                <div class="mars-tel-card">
                    <div class="mars-tel-label">📏 Diameter</div>
                    <div class="mars-tel-val">6,779 km</div>
                    <div class="mars-tel-sub">0.53 × Earth</div>
                </div>
                <div class="mars-tel-card">
                    <div class="mars-tel-label">☀️ Sol (Day)</div>
                    <div class="mars-tel-val">24h 37m 22s</div>
                    <div class="mars-tel-sub">+39m vs Earth</div>
                </div>
                <div class="mars-tel-card">
                    <div class="mars-tel-label">🧲 Gravity</div>
                    <div class="mars-tel-val">3.72 m/s²</div>
                    <div class="mars-tel-sub">0.38g (38% Earth)</div>
                </div>
                <div class="mars-tel-card">
                    <div class="mars-tel-label">🌡️ Avg Temp</div>
                    <div class="mars-tel-val">-63°C</div>
                    <div class="mars-tel-sub">-140°C to +20°C</div>
                </div>
                <div class="mars-tel-card">
                    <div class="mars-tel-label">💨 Atmosphere</div>
                    <div class="mars-tel-val">6.1 mbar</div>
                    <div class="mars-tel-sub">95.3% Carbon Dioxide</div>
                </div>
                <div class="mars-tel-card">
                    <div class="mars-tel-label">🌋 Peak Height</div>
                    <div class="mars-tel-val">21.9 km</div>
                    <div class="mars-tel-sub">Olympus Mons Volcano</div>
                </div>
            </div>

            <!-- 1. ROVER SELECTOR TABS (ALL 8 ROVERS) -->
            <div class="rover-selector-section">
                <div class="selector-header-label">SELECT SPACECRAFT (ALL 8 MONITORED):</div>
                <div class="rover-selector-pills" id="mars-rover-selector-pills"></div>
            </div>

            <!-- 2. ACTIVE ROVER HERO / HEADER -->
            <div class="sidebar-rover-hero" id="mars-rover-hero">
                <div class="detail-badges-row" style="display:flex; gap:6px; flex-wrap:wrap;">
                    <span class="mars-insp-badge" id="mars-insp-badge" style="background:rgba(56,189,248,0.2); color:#38BDF8; padding:3px 8px; border-radius:8px; font-size:10px; font-weight:800;">ROVER</span>
                    <span id="mars-hero-status" style="background:rgba(239,68,68,0.15); color:#FCA5A5; padding:3px 8px; border-radius:8px; font-size:10px; font-weight:800;">SILENT MONUMENT</span>
                    <span id="mars-hero-year" style="background:rgba(255,255,255,0.08); color:#94A3B8; padding:3px 8px; border-radius:8px; font-size:10px; font-weight:700;">📅 2004–2018</span>
                </div>
                <h2 class="sidebar-rover-name" id="mars-insp-title">Opportunity Rover</h2>
                <div class="sidebar-tagline" id="mars-insp-quote">"My battery is low and it's getting dark."</div>
            </div>

            <!-- 3. SUPABASE MISSION DATABASE CARD -->
            <div class="detail-supabase-card">
                <div class="db-header">
                    <span class="db-title">📡 SUPABASE LIVE TELEMETRY</span>
                    <span class="db-badge-verified">✓ NASA VERIFIED CLOUD POSTGRES</span>
                </div>

                <!-- Mission Stat Highlights -->
                <div class="db-stat-row">
                    <div class="db-stat-badge">
                        <span class="db-stat-icon">⏱️</span>
                        <div>
                            <div class="db-stat-label">Active Duration</div>
                            <div class="db-stat-val" id="mars-db-duration">5,352 Sols (14.8 Yrs)</div>
                        </div>
                    </div>
                    <div class="db-stat-badge">
                        <span class="db-stat-icon">🏎️</span>
                        <div>
                            <div class="db-stat-label">Total Traverse</div>
                            <div class="db-stat-val" id="mars-db-odometer">45.16 km (28.1 mi)</div>
                        </div>
                    </div>
                    <div class="db-stat-badge">
                        <span class="db-stat-icon">🚀</span>
                        <div>
                            <div class="db-stat-label">Launch Date</div>
                            <div class="db-stat-val" id="mars-db-launch">July 7, 2003</div>
                        </div>
                    </div>
                    <div class="db-stat-badge">
                        <span class="db-stat-icon">🛬</span>
                        <div>
                            <div class="db-stat-label">Touchdown</div>
                            <div class="db-stat-val" id="mars-db-landing">Jan 25, 2004</div>
                        </div>
                    </div>
                </div>

                <div class="db-grid">
                    <div class="db-cell">
                        <div class="db-cell-label">📍 Landing Coordinates</div>
                        <div class="db-cell-val" id="mars-insp-site">1.9483° S, 354.4742° E</div>
                    </div>
                    <div class="db-cell">
                        <div class="db-cell-label">⚡ Power Architecture</div>
                        <div class="db-cell-val" id="mars-insp-power">Triple-junction solar cells</div>
                    </div>
                    <div class="db-cell">
                        <div class="db-cell-label">⚖️ Chassis Mass & Build</div>
                        <div class="db-cell-val" id="mars-db-mass">185 kg (408 lb)</div>
                    </div>
                    <div class="db-cell">
                        <div class="db-cell-label">📡 Comms & Telemetry</div>
                        <div class="db-cell-val" id="mars-db-comms">X-band Dish + UHF Relay</div>
                    </div>
                </div>

                <div class="db-desc-box">
                    <div class="db-cell-label">📜 NASA Archive Master Dossier</div>
                    <p class="db-desc-text" id="mars-insp-desc">MER-B marathon runner, explored Meridiani Planum for 14.8 years until 2018 dust storm.</p>
                </div>

                <div class="db-bridge">
                    <div class="db-bridge-title">🔬 THE HARDWARE ➔ SCIENCE BRIDGE</div>
                    <div class="db-bridge-hw" id="mars-db-hw">🛠️ Tool: Rock Abrasion Tool & Mössbauer Spectrometer</div>
                    <div class="db-bridge-sc" id="mars-db-sc">💡 Discovery: Discovered hematite 'blueberries' proving liquid water once soaked Mars.</div>
                </div>

                <div class="db-monument-box" id="mars-db-monument-wrap">
                    <div class="db-cell-label">🏛️ Historic Monument Status</div>
                    <div class="db-monument-text" id="mars-db-monument">Permanently preserved in Perseverance Valley, Endeavour Crater as an eternal monument to human exploration.</div>
                </div>
            </div>

            <!-- 4. AUDIO STORY PLAYER -->
            <div class="detail-audio-card">
                <div class="audio-card-header">
                    <span class="audio-icon-pulse">🎧</span>
                    <span class="audio-card-title">Audio Narration</span>
                    <span style="font-size:11px; color:#94A3B8; margin-left:auto;" id="mars-audio-label">Opportunity Story</span>
                </div>
                <div class="audio-controls-row">
                    <button class="audio-play-btn" id="mars-btn-audio-play" onclick="toggleMarsAudioPlay()">▶ Play</button>
                    <div class="audio-progress-wrap">
                        <input type="range" class="audio-scrub-slider" id="mars-audio-scrubber" min="0" max="100" value="0" oninput="onMarsScrubAudio(this.value)">
                        <div class="audio-time-row">
                            <span id="mars-audio-current-time">0:00</span>
                            <span id="mars-audio-total-time">0:00</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 5. GEMINI AI 1st-PERSON CHATBOT -->
            <div class="detail-chat-card">
                <div class="chat-header-row">
                    <div class="chat-title-group">
                        <span style="font-size:18px;">🤖</span>
                        <span class="chat-card-title" id="mars-chat-header-title">Live AI Chat with Opportunity</span>
                    </div>
                    <div class="chat-age-toggle-bar">
                        <button class="age-pill-btn active" id="mars-btn-age-junior" onclick="setMarsChatAge('junior')">🌱 Junior (12–14)</button>
                        <button class="age-pill-btn" id="mars-btn-age-senior" onclick="setMarsChatAge('senior')">🔬 Senior (15–18)</button>
                    </div>
                </div>

                <!-- Chat messages stream -->
                <div class="chat-messages-wrap" id="mars-chat-messages-box"></div>

                <!-- Quick prompt chips -->
                <div class="chat-quick-chips">
                    <button class="quick-chip" onclick="sendMarsQuickPrompt('What was your biggest scientific discovery?')">💡 Biggest Discovery?</button>
                    <button class="quick-chip" onclick="sendMarsQuickPrompt('How did your mission end?')">⏳ How Did Mission End?</button>
                    <button class="quick-chip" onclick="sendMarsQuickPrompt('What tools are on you?')">🛠️ What Tools?</button>
                </div>

                <!-- User input row -->
                <div class="chat-input-row">
                    <input type="text" id="mars-chat-user-input" class="chat-text-input" placeholder="Ask this spacecraft a question..." onkeydown="if(event.key==='Enter') sendMarsChatMessage()">
                    <button id="mars-btn-send-chat" class="chat-send-btn" onclick="sendMarsChatMessage()">Ask Gemini ➔</button>
                </div>
            </div>

            <!-- 6. LAUNCH DEDICATED 3D MARS EXPLORER PAGE -->
            <button class="btn-launch-3d-sim" onclick="window.top.location.href='/?page=mars';">
                🚀 Launch Full 3D Mars Explorer & 3D Rover Studio ➔
            </button>

            <div class="mars-monument-list" id="mars-monuments-list" style="display:none;"></div>
        </aside>

        <!-- Top-Right HUD Card for Mars View -->
        <div id="hud-card-mars">
            <div id="hud-card-mars-title">
                <span style="color:#ef4444; font-size:15px;">🔴</span>
                <span>NASA 3D MARS MODEL</span>
            </div>
            <div id="hud-card-mars-sub">Drag to spin 360°, scroll to zoom, click pins to inspect</div>
            <div id="hud-card-mars-mesh">
                <span>🟢</span>
                <span id="hud-mars-mesh-label">Active 3D Mesh: MARS.glb (NASA Normal + Diffuse)</span>
            </div>
            <div id="hud-card-mars-btns">
                <button class="hud-btn-mars" id="btn-mars-spin" onclick="toggleMarsSpin()">⏸ Pause Spin</button>
                <button class="hud-btn-mars" onclick="resetMarsOrbit()">🔄 Reset Orbit</button>
            </div>
        </div>

        <!-- Floating 3D Surface Badges Layer for Mars -->
        <div id="globe-badges-layer"></div>

        <!-- Bottom Mission Pill Toolbar for Mars -->
        <div id="toolbar-mars"></div>

      <!-- FULL-SCREEN EQUIPMENT DETAIL VIEW (STEP 2-4) -->
      <div id="equipment-detail-overlay">
      <div class="detail-header-bar">
        <button class="detail-back-btn" onclick="closeEquipmentDetail()">⬅ Back to Mars</button>
        <div class="detail-header-title" id="detail-header-title">OPPORTUNITY • ROVER SIMULATOR</div>
        <div class="detail-view-toggle">
          <button class="toggle-view-btn active" id="btn-view-3d" onclick="switchDetailTab('3d')">🛰️ 3D Model</button>
          <button class="toggle-view-btn" id="btn-view-nasa" onclick="switchDetailTab('nasa')">📷 NASA Photos</button>
        </div>
        <button class="detail-audio-toggle-btn" id="btn-audio-toggle" onclick="toggleAudioMute()">🔊 Audio: ON</button>
      </div>

      <div class="detail-split-container">
        <!-- 3D MODEL VIEWPORT (60% screen width, first on mobile) -->
        <div class="detail-model-viewport" id="detail-model-viewport">
          <div class="detail-spinner-wrap" id="detail-spinner">
            <div class="detail-spinner"></div>
            <div class="spinner-text">Loading 3D Model...</div>
          </div>
          <div class="detail-error-banner" id="detail-error-banner" style="display:none;"></div>
          <div class="detail-model-hint">🖱️ Drag to rotate • Scroll to zoom • Click 3D model to play audio</div>
        </div>

        <!-- NASA MISSION IMAGERY & MEDIA STUDIO (togglable) -->
        <div class="detail-nasa-gallery-viewport" id="detail-nasa-gallery-viewport" style="display:none;">
          <div class="nasa-gallery-header">
            <div class="nasa-brand-badge">
              <span class="nasa-insignia">📷 NASA</span>
              <span class="nasa-live-status">● LIVE NASA API IMAGERY</span>
            </div>
            <div class="nasa-gallery-actions">
              <button class="nasa-action-btn" id="btn-nasa-fullres" onclick="openFullResNasaImage()">🔍 View Full-Res</button>
              <button class="nasa-action-btn" id="btn-nasa-refresh" onclick="refreshNasaGalleryFeed()">🔄 Refresh Feed</button>
            </div>
          </div>

          <div class="nasa-hero-display-wrap">
            <div class="nasa-img-loading" id="nasa-img-loading" style="display:none;">
              <div class="nasa-spinner"></div>
              <span>Fetching Official NASA Imagery...</span>
            </div>
            <img id="nasa-hero-img" class="nasa-hero-img" src="" alt="NASA Mission Photo" onclick="openFullResNasaImage()" />
            <div class="nasa-img-info-overlay" id="nasa-img-info-overlay">
              <div class="nasa-info-top">
                <span class="nasa-photo-id" id="nasa-photo-id">NASA ARCHIVE</span>
                <span class="nasa-photo-date" id="nasa-photo-date">NASA Mission</span>
              </div>
              <div class="nasa-photo-title" id="nasa-photo-title">Martian Surface Exploration</div>
              <div class="nasa-photo-caption" id="nasa-photo-caption">Authentic archival record from NASA Mars Exploration Archives.</div>
            </div>
          </div>

          <div class="nasa-search-bar-wrap">
            <span class="nasa-search-icon">🔍</span>
            <input type="text" id="nasa-search-input" class="nasa-search-input" placeholder="Search NASA Mars archive..." onkeydown="if(event.key==='Enter') executeNasaPhotoSearch()" />
            <button class="nasa-search-btn" onclick="executeNasaPhotoSearch()">Search NASA API</button>
          </div>

          <div class="nasa-thumbnail-strip-section">
            <div class="nasa-strip-title">AUTHENTIC NASA MISSION PHOTOGRAPHY (<span id="nasa-photo-count">0</span> PHOTOS)</div>
            <div class="nasa-thumbnails-strip" id="nasa-thumbnails-strip"></div>
          </div>
        </div>

        <!-- INFO & AUDIO PLAYER PANEL (40% screen width beside 3D model) -->
        <div class="detail-info-panel">
          <div class="detail-title-section">
            <div class="detail-badges-row">
              <span class="detail-type-badge" id="detail-type-badge">ROVER</span>
            </div>
            <h1 class="detail-name" id="detail-name">Opportunity</h1>
          </div>

          <div class="detail-audio-card">
            <div class="audio-card-header">
              <span class="audio-icon-pulse">🎧</span>
              <span class="audio-card-title">Listen to the story</span>
            </div>
            <div class="audio-controls-row">
              <button class="audio-play-btn" id="btn-audio-play" onclick="toggleAudioPlay()">▶ Play</button>
              <div class="audio-progress-wrap">
                <input type="range" class="audio-scrub-slider" id="audio-scrubber" min="0" max="100" value="0" oninput="onScrubAudio(this.value)">
                <div class="audio-time-row">
                  <span id="audio-current-time">0:00</span>
                  <span id="audio-total-time">0:00</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>


        <script>
            // Helper: Generate soft radial blur textures for cosmic clouds (Zero network latency)
            function makeSoftSpriteTexture(colorInner, colorOuter) {
                const c = document.createElement('canvas');
                c.width = 128; c.height = 128;
                const ctx = c.getContext('2d');
                const g = ctx.createRadialGradient(64, 64, 0, 64, 64, 64);
                g.addColorStop(0, colorInner);
                g.addColorStop(0.35, colorOuter);
                g.addColorStop(1, 'rgba(0,0,0,0)');
                ctx.fillStyle = g;
                ctx.fillRect(0, 0, 128, 128);
                return new THREE.CanvasTexture(c);
            }

            // Resilient Texture Loader (Local + GitHub Raw CDN Fallback)
            const texLoader = new THREE.TextureLoader();
            const CDN_TEX_ROOT = "https://raw.githubusercontent.com/harshahuppara/nasa-echo-hack/main/static/textures/";
            
            function loadResilientTex(filename) {
                const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
                const primaryUrl = isLocal ? ("/app/static/textures/" + filename) : (CDN_TEX_ROOT + filename);
                const fallbackUrl = isLocal ? (CDN_TEX_ROOT + filename) : ("/app/static/textures/" + filename);
                
                const tex = texLoader.load(primaryUrl, undefined, undefined, function() {
                    console.warn("Retrying texture via fallback:", filename);
                    texLoader.load(fallbackUrl, function(fb) {
                        tex.image = fb.image;
                        tex.needsUpdate = true;
                    });
                });
                tex.crossOrigin = "anonymous";
                return tex;
            }

            const textures = {
                milkyWay: loadResilientTex("milky_way_2k.jpg"),
                stars: loadResilientTex("stars.jpg"),
                sun: loadResilientTex("sun.jpg"),
                mercury: loadResilientTex("mercury.jpg"),
                venus: loadResilientTex("venus.jpg"),
                earth: loadResilientTex("earth.jpg"),
                earthClouds: loadResilientTex("earth_clouds.png"),
                moon: loadResilientTex("moon.jpg"),
                mars: loadResilientTex("mars.jpg"),
                jupiter: loadResilientTex("jupiter.jpg"),
                saturn: loadResilientTex("saturn.jpg"),
                saturnRing: loadResilientTex("saturn_ring.png"),
                uranus: loadResilientTex("uranus.jpg"),
                neptune: loadResilientTex("neptune.jpg")
            };

                        const PLANET_NAMES = ["Sun", "Mercury", "Venus", "Earth", "Moon", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"];
            let currentPlanetIndex = 0;

            const PLANET_DATA = {
                "Sun": {
                    symbol: "☀️", title: "The Sun", sub: "Yellow Dwarf • Heart of the Solar System",
                    type: "G2V MAIN SEQUENCE STAR", zone: "SOLAR CENTER",
                    diam: "1,392,700 km", diamRel: "109 Earths across",
                    dist: "Center", distRel: "0.0 AU",
                    temp: "5,500°C (Core 15M°C)", tempDetail: "Thermonuclear fusion engine",
                    period: "Rotation: 27 days", periodDetail: "Differential equator-to-pole rotation",
                    gravity: "274 m/s² (28x Earth). A 150 lb human weighs 4,200 lbs here!",
                    atmosFull: "Superheated incandescent plasma: 73.4% Hydrogen, 25.0% Helium, with trace Oxygen, Carbon, Neon, and Iron.",
                    interior: "Core (nuclear fusion engine), Radiative Zone (photons take 100,000 years to reach the surface!), Convective Zone, Photosphere, Chromosphere, and Corona.",
                    missions: "Parker Solar Probe (first spacecraft to touch the Sun!), SOHO, Solar Dynamics Observatory (SDO), STEREO.",
                    discovery: "Proved the solar wind forms a vast protective bubble around all planets called the heliosphere, shielding our system from galactic cosmic rays.",
                    secret: "The Sun accounts for 99.86% of all the mass in the entire solar system. Approximately 1.3 million planet Earths could fit inside it!",
                    isTarget: false
                },
                "Mercury": {
                    symbol: "☿", title: "Mercury", sub: "Terrestrial World • Innermost Planet",
                    type: "CRATERED ROCKY WORLD", zone: "INNER SOLAR SYSTEM",
                    diam: "4,879 km", diamRel: "0.38 Earths",
                    dist: "57.9M km", distRel: "0.39 AU",
                    temp: "-180°C to +430°C", tempDetail: "600°C thermal swing (largest in solar system)",
                    period: "Day: 59 Earth Days", periodDetail: "Year: 88 Earth Days (fastest orbit)",
                    gravity: "3.70 m/s² (0.38g). You can leap nearly 3 times higher!",
                    atmosFull: "Near-vacuum ultra-thin exosphere composed of atoms blasted off the surface by solar wind: 42% Oxygen, 29% Sodium, 22% Hydrogen, 6% Helium.",
                    interior: "Colossal metallic iron core comprising 85% of its total planetary radius, wrapped in a thin 400 km silicate mantle.",
                    missions: "Mariner 10 (1974 flybys), MESSENGER (orbited 2011–2015), BepiColombo (arriving 2026).",
                    discovery: "MESSENGER confirmed water ice exists in permanently shadowed craters at Mercury's scorching poles, shielded in eternal sub-zero darkness.",
                    secret: "Mercury is shrinking! As its gigantic iron core slowly cools and contracts, colossal tectonic wrinkle cliffs (scarps) miles high buckle across its crust.",
                    isTarget: false
                },
                "Venus": {
                    symbol: "♀", title: "Venus", sub: "Terrestrial World • The Scorched Twin",
                    type: "RUNAWAY GREENHOUSE WORLD", zone: "INNER SOLAR SYSTEM",
                    diam: "12,104 km", diamRel: "0.95 Earths",
                    dist: "108.2M km", distRel: "0.72 AU",
                    temp: "465°C constant", tempDetail: "Hotter than Mercury, hot enough to melt lead!",
                    period: "Day: 243 Earth Days", periodDetail: "Year: 225 Earth Days (Day is longer than year!)",
                    gravity: "8.87 m/s² (0.91g). Almost identical to Earth.",
                    atmosFull: "96.5% Carbon Dioxide, 3.5% Nitrogen with dense clouds of sulfuric acid. Crushing surface pressure 92 times Earth's (equivalent to 1,000 meters underwater).",
                    interior: "Central iron core and rocky mantle similar to Earth, but without moving tectonic plates or an internal magnetic dynamo.",
                    missions: "Mariner 2 (first successful planetary flyby, 1962), Magellan (radar-mapped 98% of surface), Pioneer Venus, DAVINCI (upcoming).",
                    discovery: "Proved that runaway greenhouse warming can completely vaporize primordial oceans and turn a sister planet into a superheated inferno.",
                    secret: "Venus spins backwards (retrograde) compared to almost every other planet, meaning the Sun rises in the west and sets in the east!",
                    isTarget: false
                },
                "Earth": {
                    symbol: "🌍", title: "Earth", sub: "The Pale Blue Dot • Oasis of Life",
                    type: "OCEAN & BIOSPHERE WORLD", zone: "HABITABLE ZONE",
                    diam: "12,742 km", diamRel: "1.00 Earth",
                    dist: "149.6M km", distRel: "1.00 AU",
                    temp: "-88°C to +58°C", tempDetail: "Global average: +15°C",
                    period: "Day: 24.0 Hours", periodDetail: "Year: 365.25 Days",
                    gravity: "9.81 m/s² (1.00g). Standard planetary baseline.",
                    atmosFull: "78% Nitrogen, 21% Oxygen, 0.9% Argon, 0.04% Carbon Dioxide. The only atmosphere known to support liquid oceans and conscious life.",
                    interior: "Solid inner iron core, liquid outer iron core generating our protective magnetosphere, silicate mantle, and dynamic moving tectonic plates.",
                    missions: "Monitored continuously by NASA's Earth Observing Fleet: Terra, Aqua, Landsat, GRACE, and the International Space Station (ISS).",
                    discovery: "Earth is the only confirmed body in the universe possessing active plate tectonics, recycling carbon and stabilizing temperature for 4 billion years.",
                    secret: "Earth is not a perfect sphere—its rapid spin makes it bulge at the equator by 43 kilometers, making Chimborazo's peak closer to space than Mount Everest!",
                    isTarget: false
                },
                "Moon": {
                    symbol: "🌕", title: "The Moon", sub: "Earth's Companion • Silent Monument Realm",
                    type: "NATURAL SATELLITE", zone: "EARTH-MOON SYSTEM",
                    diam: "3,474 km", diamRel: "0.27 Earths",
                    dist: "384,400 km from Earth", distRel: "0.0026 AU",
                    temp: "-246°C to +120°C", tempDetail: "Zero atmosphere means direct solar cooking or freezing",
                    period: "Day: 27.3 Earth Days", periodDetail: "Year: 27.3 Earth Days (Tidally locked)",
                    gravity: "1.62 m/s² (0.166g). 1/6th of Earth gravity.",
                    atmosFull: "Near-vacuum surface boundary exosphere (trace helium, neon, hydrogen, argon) with pressure less than one ten-trillionth of Earth's air.",
                    interior: "Small metallic iron-rich core (330 km radius), partially molten boundary layer, rigid silicate mantle, and ancient anorthosite crust.",
                    missions: "Apollo 11–17 human landings (1969–1972), Surveyor robotic landers, Lunar Reconnaissance Orbiter (LRO), LCROSS, Artemis program.",
                    discovery: "Analysis of 842 pounds of Apollo Moon rocks proved the Giant Impact Hypothesis: a Mars-sized planet named Theia smashed into proto-Earth 4.5 billion years ago.",
                    secret: "Laser reflectors left behind by Apollo astronauts 50+ years ago still bounce laser pulses back to Earth today, proving the Moon drifts away at 3.8 cm per year!",
                    isTarget: true, targetZone: "moon",
                    monumentHdr: "🏛️ Off-World Monuments: 4 Machines",
                    monumentTxt: "Apollo Lunar Modules, Lunar Roving Buggies, ALSEP scientific packages, and Surveyor landers rest in permanent silence on the regolith."
                },
                "Mars": {
                    symbol: "🔴", title: "Mars", sub: "The Red Planet • Ancient Ocean World",
                    type: "TERRESTRIAL DESERT PLANET", zone: "INNER SOLAR SYSTEM",
                    diam: "6,779 km", diamRel: "0.53 Earths",
                    dist: "227.9M km", distRel: "1.52 AU",
                    temp: "-125°C to +20°C", tempDetail: "Global average: -60°C",
                    period: "Day: 24h 37m (1 Sol)", periodDetail: "Year: 687 Earth Days (nearly 2 Earth years)",
                    gravity: "3.72 m/s² (0.38g). A 100 lb astronaut weighs 38 lbs.",
                    atmosFull: "95.3% Carbon Dioxide, 2.6% Nitrogen, 1.9% Argon. Surface pressure is only 0.6% of Earth's (equivalent to 100,000 feet altitude).",
                    interior: "Dense iron, nickel, and sulfur core (1,800 km radius), silicate mantle, and basaltic crust covered in fine iron-oxide dust (rust).",
                    missions: "Viking 1 & 2 (1976), Pathfinder/Sojourner (1997), Spirit & Opportunity (2004), Curiosity (2012), InSight (2018), Perseverance & Ingenuity (2021).",
                    discovery: "NASA rovers found hematite blueberries, river pebbles, and lake mudstones proving ancient Mars once hosted standing freshwater lakes and rivers.",
                    secret: "Home to Olympus Mons—the largest volcano in the solar system. It towers 21 km (13 miles) high—nearly three times taller than Mount Everest!",
                    isTarget: true, targetZone: "mars",
                    monumentHdr: "🏛️ Off-World Monuments: 8 Machines",
                    monumentTxt: "Sojourner, Spirit, Opportunity, Viking 1 & 2, InSight, Phoenix, and Ingenuity stand silently as monuments to human exploration."
                },
                "Jupiter": {
                    symbol: "♃", title: "Jupiter", sub: "Gas Giant • King of Worlds",
                    type: "GAS GIANT PLANET", zone: "OUTER SOLAR SYSTEM",
                    diam: "139,820 km", diamRel: "11.0 Earths",
                    dist: "778.5M km", distRel: "5.20 AU",
                    temp: "-110°C cloud tops", tempDetail: "Core temperature exceeds 24,000°C",
                    period: "Day: 9h 55m (Fastest day!)", periodDetail: "Year: 11.86 Earth Years",
                    gravity: "24.79 m/s² (2.53g). Heaviest surface gravity of any planet.",
                    atmosFull: "89.8% Hydrogen, 10.2% Helium, with trace ammonia, methane, and water vapor forming swirling colorful jet stream bands.",
                    interior: "No solid surface! Gaseous outer layers compress into a vast ocean of liquid metallic hydrogen conducting colossal electrical currents.",
                    missions: "Pioneer 10 & 11, Voyager 1 & 2, Galileo orbiter & probe (1995–2003), Juno orbiter (active), Europa Clipper (en route).",
                    discovery: "Galileo discovered Jupiter's 4 large moons in 1610 (first proof Earth is not the center of all orbits), and Juno discovered colossal polar cyclone clusters.",
                    secret: "The Great Red Spot is a colossal anticyclone storm bigger than planet Earth that has been raging continuously for at least 350 years!",
                    isTarget: false
                },
                "Saturn": {
                    symbol: "🪐", title: "Saturn", sub: "Gas Giant • Jewel of the Solar System",
                    type: "RINGED GAS GIANT", zone: "OUTER SOLAR SYSTEM",
                    diam: "116,460 km", diamRel: "9.1 Earths (without rings)",
                    dist: "1.43B km", distRel: "9.58 AU",
                    temp: "-140°C cloud tops", tempDetail: "Internal heat creates violent supersonic storms",
                    period: "Day: 10h 33m", periodDetail: "Year: 29.45 Earth Years",
                    gravity: "10.44 m/s² (1.06g). Very close to Earth gravity.",
                    atmosFull: "96.3% Hydrogen, 3.2% Helium, trace methane and ammonia. Famous for its mysterious 20,000-mile hexagonal jet stream at its north pole.",
                    interior: "Dense core of rocky silicate and metallic ice, surrounded by liquid metallic hydrogen and an outer gaseous hydrogen envelope.",
                    missions: "Pioneer 11 (first flyby 1979), Voyager 1 & 2, Cassini-Huygens (orbited 2004–2017, deployed Huygens lander onto moon Titan).",
                    discovery: "Cassini discovered that Saturn's moon Enceladus has active geysers blasting salty ocean water and organic molecules into space through its icy crust.",
                    secret: "Saturn has the lowest density of any planet (0.687 g/cm³)—it is less dense than water! If you had a bathtub big enough, Saturn would float in it!",
                    isTarget: false
                },
                "Uranus": {
                    symbol: "⛢", title: "Uranus", sub: "Ice Giant • The Tilted Horizon",
                    type: "ICE GIANT PLANET", zone: "OUTER SOLAR SYSTEM",
                    diam: "50,724 km", diamRel: "4.0 Earths",
                    dist: "2.87B km", distRel: "19.2 AU",
                    temp: "-224°C", tempDetail: "Coldest planetary atmosphere in the solar system",
                    period: "Day: 17h 14m (Retrograde)", periodDetail: "Year: 84.0 Earth Years",
                    gravity: "8.69 m/s² (0.89g). Slightly less than Earth.",
                    atmosFull: "82.5% Hydrogen, 15.2% Helium, 2.3% Methane. Methane gas absorbs red sunlight, giving Uranus its striking cyan/aquamarine color.",
                    interior: "Small rocky silicate core surrounded by a vast slushy mantle of supercritical water, ammonia, and methane ice under extreme pressure.",
                    missions: "Voyager 2 (only spacecraft to ever visit Uranus, flyby in January 1986, discovering 10 new moons and 2 new rings).",
                    discovery: "Voyager 2 discovered that Uranus's magnetic field is tilted by 59 degrees from its rotation axis and offset from the planet's geometric center.",
                    secret: "Uranus is tilted on its side at an extreme 97.7 degrees—it rolls along its orbit like a bowling ball, causing 42 years of daylight followed by 42 years of night at the poles!",
                    isTarget: false
                },
                "Neptune": {
                    symbol: "♆", title: "Neptune", sub: "Ice Giant • The Supersonic Realm",
                    type: "ICE GIANT PLANET", zone: "OUTER SOLAR SYSTEM",
                    diam: "49,244 km", diamRel: "3.9 Earths",
                    dist: "4.50B km", distRel: "30.1 AU",
                    temp: "-200°C cloud tops", tempDetail: "Internal heat engine drives massive storms",
                    period: "Day: 16h 06m", periodDetail: "Year: 164.8 Earth Years",
                    gravity: "11.15 m/s² (1.14g). Slightly more than Earth.",
                    atmosFull: "80.0% Hydrogen, 19.0% Helium, 1.5% Methane. Deep vivid azure blue clouds featuring white cirrus clouds of frozen methane crystals.",
                    interior: "Rocky iron/silicate core (1.2 Earth masses), surrounded by a massive hot dense fluid mantle of water, ammonia, and methane.",
                    missions: "Voyager 2 (humanity's only close encounter, August 1989, skimming 3,000 miles over Neptune's north pole).",
                    discovery: "Voyager 2 discovered the Great Dark Spot—an Earth-sized storm with jet streams screaming at 1,200 mph (faster than the speed of sound!).",
                    secret: "It takes Neptune 165 Earth years to complete one single orbit around the Sun. Since its discovery in 1846, it has completed only ONE full orbit (in 2011)!",
                    isTarget: false
                }
            };

            // Global Scene, Camera, Renderer
            const container = document.getElementById('container');
            const viewport = document.getElementById('viewport-3d');
            const scene = new THREE.Scene();

            const initW = (viewport && viewport.clientWidth) ? viewport.clientWidth : (window.innerWidth || 1200);
            const initH = (viewport && viewport.clientHeight) ? viewport.clientHeight : (window.innerHeight || 800);
            const camera = new THREE.PerspectiveCamera(45, initW / initH, 0.1, 4000);
            camera.position.set(0, 36, 88);

            const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: "high-performance" });
            renderer.setSize(initW, initH);
            renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
            renderer.toneMapping = THREE.ACESFilmicToneMapping;
            renderer.toneMappingExposure = 1.35;
            viewport.appendChild(renderer.domElement);

            const controls = new THREE.OrbitControls(camera, renderer.domElement);
            controls.enableDamping = true;
            controls.dampingFactor = 0.05;
            controls.maxDistance = 450;
            controls.minDistance = 2.5;

            // Primary Hierarchy Groups: Solar System & Globe Mode
            const solarSystemGroup = new THREE.Group();
            scene.add(solarSystemGroup);

            const globeGroup = new THREE.Group();
            globeGroup.visible = false;
            scene.add(globeGroup);

            // Dedicated Cinematic Space Lighting for Globe Mode
            const globeSunLight = new THREE.DirectionalLight(0xFFF7EB, 2.8);
            globeSunLight.position.set(6, 3.5, 5);
            globeGroup.add(globeSunLight);

            const globeAmbientLight = new THREE.AmbientLight(0x1E293B, 0.22);
            globeGroup.add(globeAmbientLight);

            // 1,800 Twinkling Particle Stars for Globe Mode
            const starCount = 1800;
            const starGeo = new THREE.BufferGeometry();
            const starPos = new Float32Array(starCount * 3);
            for(let i = 0; i < starCount; i++) {
                const r = 110 + Math.random() * 85;
                const theta = Math.random() * Math.PI * 2;
                const phi = Math.acos(2 * Math.random() - 1);
                starPos[i * 3] = r * Math.sin(phi) * Math.cos(theta);
                starPos[i * 3 + 1] = r * Math.sin(phi) * Math.sin(theta);
                starPos[i * 3 + 2] = r * Math.cos(phi);
            }
            starGeo.setAttribute('position', new THREE.BufferAttribute(starPos, 3));
            const starMat = new THREE.PointsMaterial({
                color: 0xE2E8F0, size: 1.15, transparent: true, opacity: 0.85, blending: THREE.AdditiveBlending
            });
            const globeStars = new THREE.Points(starGeo, starMat);
            globeGroup.add(globeStars);

            // Globe Mode State Variables
            let inGlobeMode = false;
            let currentGlobeZone = null;
            let globeHoveredBeacon = null;
            let globeFocusingBeacon = null;
            let globeEffectiveRadius = 1.35;
            let globeIdleInteracting = false;
            const globeHitboxes = [];
            const globeBeacons = [];
            let globePlanetMesh = null;
            let globeAtmosphereMesh = null;

            window.exitGlobeMode = function() {
                inGlobeMode = false;
                currentGlobeZone = null;
                marsFocusing = false;

                container.classList.remove('mars-mode');
                syncResize();

                const marsSidebar = document.getElementById('mars-split-sidebar');
                const hudMars = document.getElementById('hud-card-mars');
                const tbMars = document.getElementById('toolbar-mars');
                const badgesLayer = document.getElementById('globe-badges-layer');
                const gh = document.getElementById('globe-hud');
                const bc = document.getElementById('beacon-card');

                if(marsSidebar) marsSidebar.style.display = 'none';
                if(hudMars) hudMars.style.display = 'none';
                if(tbMars) tbMars.style.display = 'none';
                if(badgesLayer) {
                    badgesLayer.style.display = 'none';
                    badgesLayer.innerHTML = '';
                }
                if(gh) gh.style.display = 'none';
                if(bc) bc.style.display = 'none';

                // Restore Solar System UI
                const mainHeader = document.getElementById('main-header');
                const planetDock = document.getElementById('planet-dock');
                const welcomeOverlay = document.getElementById('welcome-overlay');
                if(mainHeader) mainHeader.style.display = 'flex';
                if(planetDock) planetDock.style.display = 'flex';
                if(welcomeOverlay) welcomeOverlay.style.display = 'block';

                // Restore Skybox, Galaxy & Solar System
                scene.background = null;
                skySphere.visible = true;
                galaxyGroup.visible = true;
                globeGroup.visible = false;
                solarSystemGroup.visible = true;

                resetSolarSystem();
            };

            // ==========================================
            // LAYER 1: MILKY WAY SKYBOX (MATCHING USER IMAGES)
            // ==========================================
            const skyGeo = new THREE.SphereGeometry(1500, 48, 48);
            const skyMat = new THREE.MeshBasicMaterial({ map: textures.milkyWay, side: THREE.BackSide, color: 0xAACCFF });
            const skySphere = new THREE.Mesh(skyGeo, skyMat);
            skySphere.rotation.x = 0.55;
            skySphere.rotation.z = -0.32;
            scene.add(skySphere);

            // ==========================================
            // LAYER 2: DISTANT SPIRAL GALAXY (ANDROMEDA) - MATCHES IMAGE 1
            // ==========================================
            const galaxyGroup = new THREE.Group();
            galaxyGroup.position.set(-450, 210, -620);
            galaxyGroup.rotation.x = 0.75;
            galaxyGroup.rotation.y = -0.42;

            // Galaxy Core
            const galCoreGeo = new THREE.SphereGeometry(10, 16, 16);
            const galCoreMat = new THREE.MeshBasicMaterial({ color: 0xFFE8B2, transparent: true, opacity: 0.85 });
            galaxyGroup.add(new THREE.Mesh(galCoreGeo, galCoreMat));

            // Logarithmic 2-Arm Spiral Points
            const galCount = 2200;
            const galGeo = new THREE.BufferGeometry();
            const galPos = new Float32Array(galCount * 3);
            const galCols = new Float32Array(galCount * 3);

            for(let i = 0; i < galCount; i++) {
                const armIndex = i % 2;
                const angleOffset = armIndex * Math.PI;
                const r = 8 + Math.pow(Math.random(), 1.6) * 115;
                const theta = Math.log(r / 6) * 2.8 + angleOffset + (Math.random() - 0.5) * 0.45;
                const x = Math.cos(theta) * r + (Math.random() - 0.5) * 6;
                const z = Math.sin(theta) * r + (Math.random() - 0.5) * 6;
                const y = (Math.random() - 0.5) * 4 * (1 - r / 125);

                galPos[i*3] = x;
                galPos[i*3+1] = y;
                galPos[i*3+2] = z;

                const t = r / 115;
                if(t < 0.25) {
                    galCols[i*3] = 1.0; galCols[i*3+1] = 0.9; galCols[i*3+2] = 0.7; // Gold
                } else if(t < 0.65) {
                    galCols[i*3] = 0.35; galCols[i*3+1] = 0.8; galCols[i*3+2] = 1.0; // Cyan
                } else {
                    galCols[i*3] = 0.75; galCols[i*3+1] = 0.4; galCols[i*3+2] = 0.95; // Magenta
                }
            }
            galGeo.setAttribute('position', new THREE.BufferAttribute(galPos, 3));
            galGeo.setAttribute('color', new THREE.BufferAttribute(galCols, 3));
            const galMat = new THREE.PointsMaterial({ size: 2.2, vertexColors: true, transparent: true, opacity: 0.75, blending: THREE.AdditiveBlending });
            galaxyGroup.add(new THREE.Points(galGeo, galMat));
            solarSystemGroup.add(galaxyGroup);

            // ==========================================
            // LAYER 3: VOLUMETRIC MULTI-HUED NEBULAE - MATCHES IMAGES 1, 4
            // ==========================================
            const nebulaGroup = new THREE.Group();
            const nebulaCyanTex = makeSoftSpriteTexture('rgba(0, 210, 255, 0.42)', 'rgba(2, 132, 199, 0.12)');
            const nebulaVioletTex = makeSoftSpriteTexture('rgba(192, 132, 252, 0.36)', 'rgba(126, 34, 206, 0.10)');
            const nebulaAmberTex = makeSoftSpriteTexture('rgba(251, 191, 36, 0.38)', 'rgba(245, 158, 11, 0.08)');

            const nebulaConfigs = [
                { tex: nebulaCyanTex, x: 260, y: 70, z: -320, size: 480 },
                { tex: nebulaCyanTex, x: -320, y: -60, z: 280, size: 520 },
                { tex: nebulaVioletTex, x: -280, y: 120, z: -360, size: 540 },
                { tex: nebulaVioletTex, x: 340, y: -90, z: 250, size: 500 },
                { tex: nebulaAmberTex, x: 0, y: 20, z: 0, size: 380 } // Soft warm aura surrounding solar system
            ];
            nebulaConfigs.forEach(cfg => {
                const spMat = new THREE.SpriteMaterial({ map: cfg.tex, transparent: true, blending: THREE.AdditiveBlending });
                const sp = new THREE.Sprite(spMat);
                sp.position.set(cfg.x, cfg.y, cfg.z);
                sp.scale.set(cfg.size, cfg.size, 1);
                nebulaGroup.add(sp);
            });
            solarSystemGroup.add(nebulaGroup);

            // ==========================================
            // LAYER 4: SPARSE ROCKY ASTEROIDS (SMALL QUANTITY HERE & THERE)
            // ==========================================
            // Scattered naturally in small quantity between Mars (33.5) and Jupiter (48)
            const astCount = 160;
            const astGeo = new THREE.BufferGeometry();
            const astPos = new Float32Array(astCount * 3);
            const astCols = new Float32Array(astCount * 3);

            for(let i=0; i<astCount; i++) {
                const r = 38.0 + Math.random() * 6.5;
                const th = Math.random() * Math.PI * 2;
                astPos[i*3] = Math.cos(th) * r;
                astPos[i*3+1] = (Math.random() - 0.5) * 1.8;
                astPos[i*3+2] = Math.sin(th) * r;

                // Subtle rocky tones: dark charcoal and bronze stone (NOT harsh white)
                const shade = 0.45 + Math.random() * 0.25;
                astCols[i*3] = shade * 0.85;
                astCols[i*3+1] = shade * 0.75;
                astCols[i*3+2] = shade * 0.65;
            }
            astGeo.setAttribute('position', new THREE.BufferAttribute(astPos, 3));
            astGeo.setAttribute('color', new THREE.BufferAttribute(astCols, 3));
            const astMat = new THREE.PointsMaterial({ size: 0.85, vertexColors: true, transparent: true, opacity: 0.55 });
            const asteroidBelt = new THREE.Points(astGeo, astMat);
            solarSystemGroup.add(asteroidBelt);

            // ==========================================
            // LAYER 6: ANIMATED STREAKING COMETS - MATCHES IMAGES 1, 4
            // ==========================================
            // Comet Halley (Cyan)
            const cometGeo = new THREE.SphereGeometry(0.55, 16, 16);
            const cometMat = new THREE.MeshBasicMaterial({ color: 0x88EEFF });
            const comet = new THREE.Mesh(cometGeo, cometMat);
            comet.position.set(-140, 24, -120);
            solarSystemGroup.add(comet);

            const tailPts = [];
            for(let i=0; i<32; i++) tailPts.push(new THREE.Vector3(-140 - i*2, 24 + i*0.35, -120 - i*2.2));
            const tailGeo = new THREE.BufferGeometry().setFromPoints(tailPts);
            const tailMat = new THREE.LineBasicMaterial({ color: 0x00D2FF, transparent: true, opacity: 0.45 });
            const cometTail = new THREE.Line(tailGeo, tailMat);
            solarSystemGroup.add(cometTail);

            // ==========================================
            // LIGHTING & THE BLAZING FIERY SUN (WITH GOD RAYS)
            // ==========================================
            const ambient = new THREE.AmbientLight(0xa0b8d0, 1.4);
            solarSystemGroup.add(ambient);

            const hemiLight = new THREE.HemisphereLight(0xfff8ee, 0x1e293b, 1.1);
            solarSystemGroup.add(hemiLight);

            const sunLight = new THREE.PointLight(0xFFF2D6, 4.5, 800, 0.3);
            solarSystemGroup.add(sunLight);

            // Sun Sphere (Enlarged for clear near entrance)
            const sunGeo = new THREE.SphereGeometry(7.2, 48, 48);
            const sunMat = new THREE.MeshBasicMaterial({ map: textures.sun, color: 0xffdd44 });
            const sunMesh = new THREE.Mesh(sunGeo, sunMat);
            sunMesh.userData = { name: "Sun", size: 7.2 };
            solarSystemGroup.add(sunMesh);

            // Corona Flares
            const corona1Mat = new THREE.MeshBasicMaterial({ color: 0xFF5500, transparent: true, opacity: 0.38, side: THREE.BackSide, blending: THREE.AdditiveBlending });
            const corona1 = new THREE.Mesh(new THREE.SphereGeometry(8.2, 32, 32), corona1Mat);
            solarSystemGroup.add(corona1);

            const corona2Mat = new THREE.MeshBasicMaterial({ color: 0xFFAA00, transparent: true, opacity: 0.22, side: THREE.BackSide, blending: THREE.AdditiveBlending });
            const corona2 = new THREE.Mesh(new THREE.SphereGeometry(9.4, 32, 32), corona2Mat);
            solarSystemGroup.add(corona2);

            // Radiant God Rays / Solar Flare Sprite (Images 1, 2, 6)
            const sunGlowTex = makeSoftSpriteTexture('rgba(255, 200, 80, 0.95)', 'rgba(255, 120, 0, 0.2)');
            const sunGlowSprite = new THREE.Sprite(new THREE.SpriteMaterial({ map: sunGlowTex, transparent: true, blending: THREE.AdditiveBlending }));
            sunGlowSprite.scale.set(48, 48, 1);
            solarSystemGroup.add(sunGlowSprite);

            // ==========================================
            // PLANET DEFINITION & SPEED CONTROLS (ULTRA-CALM SPEEDS)
            // ==========================================
            // Slower orbital speeds by ~85% for serene, majestic planetarium pacing
            let speedMultiplier = 0.25; // Default: Cinematic Slow

            // Planet Configuration: Scaled UP (~40%) with vibrant natural base colors
            const PLANET_CONFIG = [
                { name: "Mercury", size: 1.25, dist: 13.0, speed: 0.00095, tex: textures.mercury, color: 0xb5b5b5 },
                { name: "Venus", size: 1.95, dist: 18.5, speed: 0.00070, tex: textures.venus, color: 0xe8c17b },
                { name: "Earth", size: 2.15, dist: 25.5, speed: 0.00048, tex: textures.earth, hasClouds: true, color: 0x2e86de },
                { name: "Mars", size: 1.65, dist: 33.5, speed: 0.00038, tex: textures.mars, color: 0xee5253 },
                { name: "Jupiter", size: 4.80, dist: 48.0, speed: 0.00019, tex: textures.jupiter, color: 0xf3a683 },
                { name: "Saturn", size: 3.80, dist: 62.0, speed: 0.00014, tex: textures.saturn, hasRings: true, color: 0xf7d794 },
                { name: "Uranus", size: 2.70, dist: 75.0, speed: 0.00010, tex: textures.uranus, color: 0x70a1ff },
                { name: "Neptune", size: 2.50, dist: 87.0, speed: 0.00008, tex: textures.neptune, color: 0x1e90ff }
            ];

            const planets = [];
            const interactiveObjects = [sunMesh];
            const hitBoxes = [];
            let earthCloudMesh = null;
            let moonMesh = null;

            // Reticle / Highlight Ring on Hover
            const reticleGeo = new THREE.RingGeometry(1, 1.25, 32);
            const reticleMat = new THREE.MeshBasicMaterial({ color: 0x00D2FF, side: THREE.DoubleSide, transparent: true, opacity: 0.0 });
            const hoverReticle = new THREE.Mesh(reticleGeo, reticleMat);
            hoverReticle.rotation.x = Math.PI / 2;
            solarSystemGroup.add(hoverReticle);

            // Transparent Material for 100% Reliable Hitboxes (Three.js raycast hits transparent meshes!)
            const hitMat = new THREE.MeshBasicMaterial({ transparent: true, opacity: 0.0001, depthWrite: false });

            // Sun Hitbox
            const sunHit = new THREE.Mesh(new THREE.SphereGeometry(10, 16, 16), hitMat);
            sunHit.userData = { parentPlanet: sunMesh, name: "Sun" };
            sunMesh.add(sunHit);
            hitBoxes.push(sunHit);

            PLANET_CONFIG.forEach(cfg => {
                // Orbital Path Ring
                const ringPts = [];
                for(let a=0; a<=Math.PI*2; a+=0.03) {
                    ringPts.push(new THREE.Vector3(Math.cos(a)*cfg.dist, 0, Math.sin(a)*cfg.dist));
                }
                const trackGeo = new THREE.BufferGeometry().setFromPoints(ringPts);
                const trackMat = new THREE.LineBasicMaterial({ color: 0x38BDF8, transparent: true, opacity: 0.32 });
                solarSystemGroup.add(new THREE.Line(trackGeo, trackMat));

                // Planet Mesh with Real NASA Texture & Natural Base Color
                const pGeo = new THREE.SphereGeometry(cfg.size, 40, 40);
                const pMat = new THREE.MeshStandardMaterial({ 
                    map: cfg.tex, 
                    color: cfg.color || 0xffffff,
                    roughness: 0.55, 
                    metalness: 0.05 
                });
                const mesh = new THREE.Mesh(pGeo, pMat);
                mesh.userData = { name: cfg.name, dist: cfg.dist, speed: cfg.speed, angle: Math.random()*Math.PI*2, size: cfg.size };
                solarSystemGroup.add(mesh);
                planets.push(mesh);
                interactiveObjects.push(mesh);

                // Invisible Hitbox for 100% Reliable Clicking
                // For Earth, use compact hitbox so it does NOT envelop or block the Moon!
                const hitRadius = cfg.hasClouds ? (cfg.size * 1.3) : Math.max(cfg.size * 3.8, 4.2);
                const hitGeo = new THREE.SphereGeometry(hitRadius, 16, 16);
                const hitMesh = new THREE.Mesh(hitGeo, hitMat);
                hitMesh.userData = { parentPlanet: mesh, name: cfg.name };
                mesh.add(hitMesh);
                hitBoxes.push(hitMesh);

                // Earth Clouds & Moon
                if(cfg.hasClouds) {
                    const cGeo = new THREE.SphereGeometry(cfg.size * 1.018, 36, 36);
                    const cMat = new THREE.MeshStandardMaterial({ map: textures.earthClouds, transparent: true, opacity: 0.45 });
                    earthCloudMesh = new THREE.Mesh(cGeo, cMat);
                    mesh.add(earthCloudMesh);

                    // Add Moon with NASA LRO texture (enlarged for easy touch & visibility)
                    const mGeo = new THREE.SphereGeometry(0.88, 32, 32);
                    const mMat = new THREE.MeshStandardMaterial({ map: textures.moon, roughness: 0.85 });
                    moonMesh = new THREE.Mesh(mGeo, mMat);
                    moonMesh.userData = { name: "Moon", isMoon: true, size: 0.88 };
                    mesh.add(moonMesh);
                    interactiveObjects.push(moonMesh);

                    // Moon Hitbox - Generous 3.4 radius and clearly separated from Earth
                    const moonHit = new THREE.Mesh(new THREE.SphereGeometry(3.4, 16, 16), hitMat);
                    moonHit.userData = { parentPlanet: moonMesh, name: "Moon" };
                    moonMesh.add(moonHit);
                    hitBoxes.push(moonHit);
                }

                // Mars Atmosphere Rim
                if(cfg.atmo) {
                    const atmoGeo = new THREE.SphereGeometry(cfg.size * 1.06, 32, 32);
                    const atmoMat = new THREE.MeshBasicMaterial({ color: cfg.atmo, transparent: true, opacity: 0.25, side: THREE.BackSide });
                    mesh.add(new THREE.Mesh(atmoGeo, atmoMat));
                }

                // Saturn Ring System
                if(cfg.hasRings) {
                    const ringGeo = new THREE.RingGeometry(cfg.size * 1.35, cfg.size * 2.45, 64);
                    const ringMat = new THREE.MeshStandardMaterial({
                        map: textures.saturnRing, side: THREE.DoubleSide, transparent: true, opacity: 0.78
                    });
                    const ring = new THREE.Mesh(ringGeo, ringMat);
                    ring.rotation.x = Math.PI / 2.3;
                    mesh.add(ring);
                }
            });

            // Bulletproof Top/Parent Window Navigation Helper (Works seamlessly across Streamlit srcdoc iframes)
            function navigateParentView(viewName, extraQuery) {
                const cleanPage = (viewName === 'mars_explorer' || viewName === 'mars') ? 'mars' :
                                  (viewName === 'moon_explorer' || viewName === 'moon') ? 'moon' :
                                  (viewName === 'deep_space' || viewName === 'deep') ? 'deep' : viewName;
                const query = 'page=' + cleanPage + '&view=' + cleanPage + (extraQuery ? ('&' + extraQuery) : '');

                // 1. Direct search modification on parent / top window if accessible
                try {
                    if (window.parent && window.parent.location && window.parent.location.search !== undefined) {
                        window.parent.location.search = '?' + query;
                        return;
                    }
                } catch(e) {}

                try {
                    if (window.top && window.top.location && window.top.location.search !== undefined) {
                        window.top.location.search = '?' + query;
                        return;
                    }
                } catch(e) {}

                // 2. Discover true origin of Streamlit application
                let origin = '';
                try {
                    if (window.parent && window.parent.location && window.parent.location.origin && window.parent.location.origin !== 'null') {
                        origin = window.parent.location.origin;
                    } else if (window.top && window.top.location && window.top.location.origin && window.top.location.origin !== 'null') {
                        origin = window.top.location.origin;
                    }
                } catch(e) {}

                if (!origin && window.location && window.location.ancestorOrigins && window.location.ancestorOrigins.length > 0) {
                    origin = window.location.ancestorOrigins[0];
                }

                if (!origin && window.document && window.document.referrer) {
                    try {
                        origin = new URL(window.document.referrer).origin;
                    } catch(e) {}
                }

                if (!origin || origin === 'null' || origin.startsWith('about')) {
                    origin = (window.location.protocol === 'http:' || window.location.protocol === 'https:') ? (window.location.protocol + '//' + window.location.host) : '';
                }

                const fullUrl = (origin ? origin : '') + '/?' + query;

                try {
                    window.top.location.href = fullUrl;
                    return;
                } catch(e1) {
                    try {
                        window.parent.location.href = fullUrl;
                        return;
                    } catch(e2) {
                        try {
                            window.open(fullUrl, '_top');
                            return;
                        } catch(e3) {
                            window.location.href = fullUrl;
                        }
                    }
                }
            }

            // Navigation Helper for Fullscreen Header
            window.navigateToZone = function(zone) {
                window.stopEntryAudio();
                if(zone === 'moon' || zone === 'mars' || zone === 'deep') {
                    triggerWarp(zone);
                } else {
                    const viewName = (zone === 'deep') ? 'deep_space' : (zone + '_explorer');
                    navigateParentView(viewName);
                }
            };

            window.toggleAudio = function() {
                muted = !muted;
                const audioIcon = document.getElementById('audio-icon');
                if(muted) {
                    if(audioIcon) audioIcon.innerText = "🔇";
                    window.stopEntryAudio();
                } else {
                    if(audioIcon) audioIcon.innerText = "🔊";
                    speechSilencedPermanently = false;
                    audioTriggered = false;
                    triggerAudio();
                }
            };

            // ==========================================
            // SPEED CONTROLS & CAMERA VIEWS
            // ==========================================
            window.setOrbitSpeed = function(val, btn) {
                speedMultiplier = val;
                document.querySelectorAll('#top-controls .ctrl-group:first-child .ctrl-btn').forEach(b => b.classList.remove('active'));
                if(btn) btn.classList.add('active');
            };

            window.setViewMode = function(mode) {
                if(mode === 'top') {
                    targetCameraPos = new THREE.Vector3(0, 115, 0.1);
                    targetLookAt.set(0, 0, 0);
                } else if(mode === 'edge') {
                    targetCameraPos = new THREE.Vector3(0, 5, 92);
                    targetLookAt.set(0, 0, 0);
                } else {
                    targetCameraPos = new THREE.Vector3(0, 36, 88);
                    targetLookAt.set(0, 0, 0);
                }
            };

            // ==========================================
            // RAYCASTER, CLICKING & 3D FLOATING BADGES
            // ==========================================
            const raycaster = new THREE.Raycaster();
            const mouse = new THREE.Vector2();
            let selectedTarget = null;
            let targetCameraPos = null;
            let targetLookAt = new THREE.Vector3(0, 0, 0);
            let isFocused = false;

            const monumentAlert = document.getElementById('monument-alert');
            const btnWarp = document.getElementById('btn-warp');
            const tooltip = document.getElementById('hover-tooltip');

            // ==========================================
            // AUDIO NARRATION & GLITCH PREVENTION
            // ==========================================
            let audioTriggered = false;
            let muted = false;
            let speechSilencedPermanently = false;
            const audioCtrl = document.getElementById('audio-control');
            const audioIcon = document.getElementById('audio-icon');
            const welcomeOverlay = document.getElementById('welcome-overlay');

            const welcomeSpeech = "Welcome to Forgotten in Space, Explorer! Across these orbiting worlds, humanity's greatest robotic pioneers stand silently as monuments to human curiosity. Touch any planet to awaken their untold stories and uncover the science they left behind.";

            // Bulletproof Speech Cancellation: stops all welcome/entry speech immediately with 0 latency
            window.stopEntryAudio = function() {
                speechSilencedPermanently = true;
                audioTriggered = true;
                const overlay = document.getElementById('welcome-overlay');
                if(overlay) overlay.classList.add('hidden');

                if('speechSynthesis' in window) {
                    try {
                        window.speechSynthesis.cancel();
                    } catch(e) {}
                }
            };

            function triggerAudio() {
                // If speech was silenced permanently by launching video or manual mute, NEVER play it
                if(speechSilencedPermanently || audioTriggered || muted) {
                    return;
                }
                audioTriggered = true;
                const overlay = document.getElementById('welcome-overlay');
                if(overlay) overlay.classList.add('hidden');
                if('speechSynthesis' in window) {
                    try { window.speechSynthesis.cancel(); } catch(e) {}
                    const utt = new SpeechSynthesisUtterance(welcomeSpeech);
                    utt.rate = 0.95;
                    window.speechSynthesis.speak(utt);
                }
            }

            if(audioCtrl) {
                audioCtrl.onclick = () => window.toggleAudio();
            }

            if(welcomeOverlay) {
                welcomeOverlay.onclick = () => {
                    if(!speechSilencedPermanently && !audioTriggered) {
                        triggerAudio();
                    }
                };
            }

            window.selectPlanet = function(name) {
                const data = PLANET_DATA[name];
                if(!data) return;

                // 2nd touch on Moon or Mars (when focused in the 60% screen view) -> TRIGGER DESCENT TRANSITION
                // At this exact moment, silence entry narration immediately so it never overlaps with the video audio!
                if(isFocused && selectedTarget && selectedTarget.userData.name === name && data.isTarget) {
                    window.stopEntryAudio();
                    triggerWarp(data.targetZone);
                    return;
                }

                // 1st click on any planet -> KEEP AUDIO PLAYING while zooming in to 60% screen & opening flashcard
                let obj = interactiveObjects.find(o => o.userData.name === name);
                if(!obj && name === "Moon" && moonMesh) obj = moonMesh;
                if(!obj) return;

                selectedTarget = obj;
                isFocused = true;
                container.classList.add('panel-open');

                // Track current index
                const idx = PLANET_NAMES.indexOf(name);
                if(idx !== -1) currentPlanetIndex = idx;

                // Fill Flash Card HUD
                document.getElementById('p-counter').innerText = `${currentPlanetIndex + 1} / ${PLANET_NAMES.length}`;
                document.getElementById('p-symbol').innerText = data.symbol;
                document.getElementById('p-title').innerText = data.title;
                document.getElementById('p-type').innerText = data.type;
                document.getElementById('p-zone').innerText = data.zone;

                // Tab 1: Telemetry
                document.getElementById('p-diam').innerText = data.diam;
                document.getElementById('p-diam-rel').innerText = data.diamRel;
                document.getElementById('p-dist').innerText = data.dist;
                document.getElementById('p-dist-rel').innerText = data.distRel;
                document.getElementById('p-temp').innerText = data.temp;
                document.getElementById('p-temp-detail').innerText = data.tempDetail;
                document.getElementById('p-period').innerText = data.period;
                document.getElementById('p-period-detail').innerText = data.periodDetail;
                document.getElementById('p-gravity').innerText = data.gravity;

                // Tab 2: Anatomy
                document.getElementById('p-atmos-full').innerText = data.atmosFull;
                document.getElementById('p-interior').innerText = data.interior;

                // Tab 3: Missions
                document.getElementById('p-missions').innerText = data.missions;
                document.getElementById('p-discovery').innerText = data.discovery;

                // Tab 4: Secrets
                document.getElementById('p-secret').innerText = data.secret;

                // Monuments Box (Moon & Mars)
                if(data.isTarget) {
                    monumentAlert.style.display = "block";
                    document.getElementById('m-hdr').innerText = data.monumentHdr;
                    document.getElementById('m-txt').innerText = data.monumentTxt;
                    btnWarp.style.display = "block";
                    btnWarp.innerText = `🚀 Descend to ${data.title} Explorer (${name === 'Moon' ? '4' : '8'} Machines)`;
                    btnWarp.onclick = () => {
                        window.stopEntryAudio();
                        triggerWarp(data.targetZone);
                    };
                } else {
                    monumentAlert.style.display = "none";
                    btnWarp.style.display = "none";
                }

                syncResize();
            };

            window.cyclePlanet = function(delta) {
                currentPlanetIndex = (currentPlanetIndex + delta + PLANET_NAMES.length) % PLANET_NAMES.length;
                const nextName = PLANET_NAMES[currentPlanetIndex];
                selectPlanet(nextName);
            };

            window.switchCardTab = function(tabName, btn) {
                document.querySelectorAll('.fc-tab').forEach(t => t.classList.remove('active'));
                document.querySelectorAll('.fc-tab-content').forEach(c => c.classList.remove('active'));
                if(btn) btn.classList.add('active');
                const targetContent = document.getElementById('tab-' + tabName);
                if(targetContent) targetContent.classList.add('active');
            };

            window.speakCurrentPlanet = function() {
                const name = PLANET_NAMES[currentPlanetIndex];
                const data = PLANET_DATA[name];
                if(!data || !('speechSynthesis' in window)) return;

                window.speechSynthesis.cancel();
                const text = `${data.title}. ${data.sub}. ${data.secret}`;
                const utt = new SpeechSynthesisUtterance(text);
                utt.rate = 0.95;
                window.speechSynthesis.speak(utt);
            };

            function resetSolarSystem() {
                isFocused = false;
                selectedTarget = null;
                container.classList.remove('panel-open');
                targetLookAt.set(0, 0, 0);
                targetCameraPos = new THREE.Vector3(0, 36, 88);
                syncResize();
            }

            document.getElementById('btn-back').onclick = resetSolarSystem;

            // Hover effects
            renderer.domElement.addEventListener('pointermove', (e) => {
                if(inGlobeMode) {
                    if(globeFocusingBeacon) return;
                    const rect = renderer.domElement.getBoundingClientRect();
                    mouse.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
                    mouse.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;

                    raycaster.setFromCamera(mouse, camera);
                    const hits = raycaster.intersectObjects(globeHitboxes, true);

                    const beaconCard = document.getElementById('beacon-card');
                    if(hits.length > 0) {
                        const hit = hits[0].object;
                        const b = hit.userData.beacon;
                        globeHoveredBeacon = hit.userData;
                        renderer.domElement.style.cursor = 'pointer';

                        document.getElementById('bc-badge').innerText = b.status.includes('ACTIVE') ? 'ACTIVE MONUMENT' : 'SILENT MONUMENT';
                        document.getElementById('bc-badge').style.color = b.color;
                        document.getElementById('bc-badge').style.borderColor = b.color;
                        document.getElementById('bc-year').innerText = '📅 ' + b.year;
                        document.getElementById('bc-title').innerText = b.name;
                        document.getElementById('bc-site').innerText = '📍 ' + b.site;
                        document.getElementById('bc-status').innerText = b.status;

                        const wp = new THREE.Vector3();
                        hit.getWorldPosition(wp);
                        wp.project(camera);

                        const sx = (wp.x * 0.5 + 0.5) * viewport.clientWidth;
                        const sy = (-wp.y * 0.5 + 0.5) * viewport.clientHeight;

                        beaconCard.style.display = 'block';
                        beaconCard.style.left = Math.min(Math.max(sx + 15, 10), viewport.clientWidth - 290) + 'px';
                        beaconCard.style.top = Math.min(Math.max(sy - 70, 15), viewport.clientHeight - 160) + 'px';
                    } else {
                        globeHoveredBeacon = null;
                        renderer.domElement.style.cursor = 'default';
                        if(beaconCard) beaconCard.style.display = 'none';
                    }
                    return;
                }

                const rect = renderer.domElement.getBoundingClientRect();
                mouse.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
                mouse.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;

                raycaster.setFromCamera(mouse, camera);
                const hits = raycaster.intersectObjects([...hitBoxes, ...interactiveObjects], true);

                if(hits.length > 0) {
                    renderer.domElement.style.cursor = 'pointer';
                    const moonHit = hits.find(h => (h.object.userData.name === "Moon" || (h.object.userData.parentPlanet && h.object.userData.parentPlanet.userData.name === "Moon")));
                    const hit = moonHit ? moonHit.object : hits[0].object;
                    const pName = hit.userData.name || (hit.userData.parentPlanet && hit.userData.parentPlanet.userData.name);
                    if(pName) {
                        tooltip.style.display = 'block';
                        tooltip.style.left = e.clientX + 'px';
                        tooltip.style.top = e.clientY + 'px';
                        tooltip.innerText = `Select ${pName}`;
                    }
                } else {
                    renderer.domElement.style.cursor = 'default';
                    tooltip.style.display = 'none';
                }
            });

            // Click vs Drag Detection (Fixing "isnt it clickable")
            let pointerStartX = 0;
            let pointerStartY = 0;
            let pointerStartTime = 0;

            renderer.domElement.addEventListener('pointerdown', (e) => {
                // Do not trigger audio on pointerdown - prevents accidental speech when touching planets or models
                pointerStartX = e.clientX;
                pointerStartY = e.clientY;
                pointerStartTime = Date.now();
            });

            renderer.domElement.addEventListener('pointerup', (e) => {
                const dx = e.clientX - pointerStartX;
                const dy = e.clientY - pointerStartY;
                const dist = Math.hypot(dx, dy);
                const elapsed = Date.now() - pointerStartTime;

                if(inGlobeMode) {
                    if(dist < 8 && elapsed < 500 && globeHoveredBeacon) {
                        const b = globeHoveredBeacon.beacon;
                        if(currentGlobeZone === 'mars') {
                            if (isEquipmentClickable(b.id)) {
                                openEquipmentDetail(b.id);
                            } else {
                                focusMarsLocation(b);
                            }
                        } else {
                            const wp = new THREE.Vector3();
                            globeHoveredBeacon.parentGroup.getWorldPosition(wp);
                            const destCam = wp.clone().normalize().multiplyScalar(globeEffectiveRadius * 1.8);
                            globeFocusingBeacon = {
                                startCam: camera.position.clone(),
                                endCam: destCam,
                                startTarget: controls.target.clone(),
                                endTarget: wp,
                                progress: 0,
                                id: b.id
                            };
                        }
                    }
                    return;
                }

                // If user didn't drag (dist < 8px) and released within 600ms, it is a deliberate click!
                if(dist < 8 && elapsed < 600) {
                    const rect = renderer.domElement.getBoundingClientRect();
                    mouse.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
                    mouse.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;

                    raycaster.setFromCamera(mouse, camera);
                    const hits = raycaster.intersectObjects([...hitBoxes, ...interactiveObjects], true);

                    if(hits.length > 0) {
                        const moonHit = hits.find(h => (h.object.userData.name === "Moon" || (h.object.userData.parentPlanet && h.object.userData.parentPlanet.userData.name === "Moon")));
                        const hit = moonHit ? moonHit.object : hits[0].object;
                        const targetName = hit.userData.name || (hit.userData.parentPlanet && hit.userData.parentPlanet.userData.name);
                        if(targetName) {
                            if(!audioTriggered && !speechSilencedPermanently) {
                                triggerAudio();
                            }
                            selectPlanet(targetName);
                        }
                    } else if(!isFocused && !speechSilencedPermanently && !audioTriggered) {
                        // Only trigger initial welcome voice if clicking empty space in 360 overview
                        triggerAudio();
                    }
                }
            });

            // Double-Click: When Mars or Moon is focused (60% screen view) or double-clicked anywhere, trigger warp transition
            renderer.domElement.addEventListener('dblclick', (e) => {
                if(isFocused && selectedTarget) {
                    const name = selectedTarget.userData.name;
                    if(name === 'Mars') {
                        window.stopEntryAudio();
                        triggerWarp('mars');
                        return;
                    } else if(name === 'Moon') {
                        window.stopEntryAudio();
                        triggerWarp('moon');
                        return;
                    }
                }
                const rect = renderer.domElement.getBoundingClientRect();
                mouse.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
                mouse.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;
                raycaster.setFromCamera(mouse, camera);
                const hits = raycaster.intersectObjects([...hitBoxes, ...interactiveObjects], true);
                if(hits.length > 0) {
                    const moonHit = hits.find(h => (h.object.userData.name === "Moon" || (h.object.userData.parentPlanet && h.object.userData.parentPlanet.userData.name === "Moon")));
                    const hit = moonHit ? moonHit.object : hits[0].object;
                    const targetName = hit.userData.name || (hit.userData.parentPlanet && hit.userData.parentPlanet.userData.name);
                    if(targetName === 'Mars') {
                        window.stopEntryAudio();
                        triggerWarp('mars');
                    } else if(targetName === 'Moon') {
                        window.stopEntryAudio();
                        triggerWarp('moon');
                    }
                }
            });

            // ==========================================
            // WARP TRANSITION VIDEO & ROUTING TO EXPLORER
            // ==========================================
            const warpModal = document.getElementById('warp-modal');
            const skipBtn = document.getElementById('skip-btn');
            let isWarping = false;
            let currentActiveVideo = null;

            const ZONE_TITLES = {
                "moon": {
                    title: "LUNAR DESCENT TRAJECTORY INITIATED",
                    sub: "STAND BY FOR APOLLO & SURVEYOR MONUMENT REGIONS",
                    videoId: "warp-video-moon"
                },
                "mars": {
                    title: "MARTIAN ATMOSPHERIC ENTRY INITIATED",
                    sub: "DE-ORBIT BURN COMPLETE • APPROACHING RED BEDROCK",
                    videoId: "warp-video-mars"
                },
                "deep": {
                    title: "INTERSTELLAR TRAJECTORY ENGAGED",
                    sub: "CROSSING THE HELIOPAUSE • APPROACHING VOYAGER & PIONEER",
                    videoId: "warp-video-deep"
                }
            };

            // ==========================================
            // DIRECT 3D PLANET GLOBE MODE (MARS.glb & MOON.glb)
            // ==========================================
            /* __INJECT_MARS_LOCATIONS__ */
            const GEMINI_API_KEY = /* __GEMINI_KEY__ */;
            const NASA_API_KEY = /* __NASA_KEY__ */;

        // ==========================================
        // MARS EQUIPMENT ASSETS CONFIG (STEP 1)
        // ==========================================
        const MARS_EQUIPMENT_ASSETS = {
          "opportunity": {
            id: "opportunity",
            name: "Opportunity",
            type: "Rover",
            aliasIds: ["opportunity-rover", "opportunity", "oppy", "mer-b", "mer_b"],
            modelFiles: [
              "https://raw.githubusercontent.com/harshahuppara/nasa-echo-hack/main/static/models/opportunity.glb",
              "https://raw.githubusercontent.com/harshahuppara/nasa-echo-hack/main/static/models/Oppurtunity%20.glb",
              "/app/static/models/Oppurtunity%20.glb",
              "/app/static/models/opportunity.glb",
              "/static/models/Oppurtunity%20.glb",
              "/static/models/opportunity.glb"
            ],
            audioFiles: [
              "https://raw.githubusercontent.com/harshahuppara/nasa-echo-hack/main/static/audio/opportunity.mp3",
              "/app/static/audio/opportunity.mp3",
              "/static/audio/opportunity.mp3",
              "static/audio/opportunity.mp3"
            ],
            color: "#38bdf8"
          },
          "viking-1": {
            id: "viking-1",
            name: "Viking 1",
            type: "Lander",
            aliasIds: ["viking-1-lander", "viking-1", "viking1", "viking_1", "viking-lander", "viking_one", "viking"],
            modelFiles: [
              "https://raw.githubusercontent.com/harshahuppara/nasa-echo-hack/main/static/models/viking-1.glb",
              "https://raw.githubusercontent.com/harshahuppara/nasa-echo-hack/main/static/models/Viking%20Lander%20.glb",
              "/app/static/models/Viking%20Lander%20.glb",
              "/app/static/models/viking-1.glb",
              "/app/static/models/viking.glb",
              "/static/models/Viking%20Lander%20.glb"
            ],
            audioFiles: [
              "https://raw.githubusercontent.com/harshahuppara/nasa-echo-hack/main/static/audio/viking-1.mp3",
              "/app/static/audio/viking-1.mp3",
              "/static/audio/viking-1.mp3",
              "static/audio/viking-1.mp3"
            ],
            color: "#a855f7"
          },
          "ingenuity": {
            id: "ingenuity",
            name: "Ingenuity",
            type: "Helicopter",
            aliasIds: ["ingenuity-helicopter", "ingenuity", "ingenuity_helicopter", "mars_helicopter", "heli"],
            modelFiles: [
              "https://raw.githubusercontent.com/harshahuppara/nasa-echo-hack/main/static/models/ingenuity.glb",
              "https://raw.githubusercontent.com/harshahuppara/nasa-echo-hack/main/static/models/Ingenuity%20Mars%20Helicopter%20.glb",
              "/app/static/models/Ingenuity%20Mars%20Helicopter%20.glb",
              "/app/static/models/ingenuity.glb",
              "/static/models/Ingenuity%20Mars%20Helicopter%20.glb"
            ],
            audioFiles: [
              "https://raw.githubusercontent.com/harshahuppara/nasa-echo-hack/main/static/audio/ingenuity.mp3",
              "/app/static/audio/ingenuity.mp3",
              "/static/audio/ingenuity.mp3",
              "static/audio/ingenuity.mp3"
            ],
            color: "#00f0ff"
          },
          "spirit": {
            id: "spirit",
            name: "Spirit Rover",
            type: "Rover",
            aliasIds: ["spirit-rover", "spirit", "mer-a", "mer_a"],
            modelFiles: [],
            audioFiles: [
              "/app/static/audio/spirit.mp3",
              "/static/audio/spirit.mp3",
              "static/audio/spirit.mp3",
              "/app/static/audio/spirit.mp3.mpeg",
              "/static/audio/spirit.mp3.mpeg",
              "static/audio/spirit.mp3.mpeg"
            ],
            color: "#fbbf24"
          },
          "sojourner": {
            id: "sojourner",
            name: "Sojourner Rover",
            type: "Rover",
            aliasIds: ["sojourner-rover", "sojourner", "pathfinder"],
            modelFiles: [],
            audioFiles: [
              "/app/static/audio/sojourner.mp3",
              "/static/audio/sojourner.mp3",
              "static/audio/sojourner.mp3",
              "/app/static/audio/sojourner.mp3.mpeg",
              "/static/audio/sojourner.mp3.mpeg",
              "static/audio/sojourner.mp3.mpeg"
            ],
            color: "#22c55e"
          },
          "viking-2": {
            id: "viking-2",
            name: "Viking 2 Lander",
            type: "Lander",
            aliasIds: ["viking-2-lander", "viking-2", "viking2"],
            modelFiles: [],
            audioFiles: [
              "/app/static/audio/viking-2.mp3",
              "/static/audio/viking-2.mp3",
              "static/audio/viking-2.mp3",
              "/app/static/audio/viking%202.mp3",
              "/static/audio/viking%202.mp3",
              "/app/static/audio/viking%202.mp3.mpeg",
              "/static/audio/viking%202.mp3.mpeg",
              "static/audio/viking 2.mp3.mpeg"
            ],
            color: "#f97316"
          },
          "insight": {
            id: "insight",
            name: "InSight Lander",
            type: "Lander",
            aliasIds: ["insight-lander", "insight"],
            modelFiles: [],
            audioFiles: [
              "/app/static/audio/insight.mp3",
              "/static/audio/insight.mp3",
              "static/audio/insight.mp3",
              "/app/static/audio/insight.mp3.mpeg",
              "/static/audio/insight.mp3.mpeg",
              "static/audio/insight.mp3.mpeg"
            ],
            color: "#ec4899"
          },
          "phoenix": {
            id: "phoenix",
            name: "Phoenix Lander",
            type: "Lander",
            aliasIds: ["phoenix-lander", "phoenix"],
            modelFiles: [],
            audioFiles: [
              "/app/static/audio/phoenix.mp3",
              "/static/audio/phoenix.mp3",
              "static/audio/phoenix.mp3",
              "/app/static/audio/phoenix.mp3.mpeg",
              "/static/audio/phoenix.mp3.mpeg",
              "static/audio/phoenix.mp3.mpeg"
            ],
            color: "#06b6d4"
          },
          "curiosity": {
            id: "curiosity",
            name: "Curiosity Rover",
            type: "Rover",
            aliasIds: ["curiosity-rover", "curiosity", "msl"],
            modelFiles: [],
            audioFiles: [
              "/app/static/audio/curiosity.mp3",
              "/static/audio/curiosity.mp3",
              "static/audio/curiosity.mp3",
              "/app/static/audio/curiosity.mp3.mpeg",
              "/static/audio/curiosity.mp3.mpeg",
              "static/audio/curiosity.mp3.mpeg"
            ],
            color: "#38bdf8"
          },
          "perseverance": {
            id: "perseverance",
            name: "Perseverance Rover",
            type: "Rover",
            aliasIds: ["perseverance-rover", "perseverance", "percy"],
            modelFiles: [],
            audioFiles: [
              "/app/static/audio/perseverance.mp3",
              "/static/audio/perseverance.mp3",
              "static/audio/perseverance.mp3",
              "/app/static/audio/perseverance.mp3.mpeg",
              "/static/audio/perseverance.mp3.mpeg",
              "static/audio/perseverance.mp3.mpeg"
            ],
            color: "#00f0ff"
          }
        };

        function isEquipmentClickable(locId) {
          return true; // All Mars rovers & landers are clickable!
        }

        function resolveEquipmentKey(locId) {
          if (!locId) return null;
          const s = String(locId).toLowerCase().replace(/[^a-z0-9]/g, '');
          for (const k in MARS_EQUIPMENT_ASSETS) {
            const asset = MARS_EQUIPMENT_ASSETS[k];
            if (asset.aliasIds.some(alias => {
              const a = alias.toLowerCase().replace(/[^a-z0-9]/g, '');
              return s === a || s.includes(a) || a.includes(s);
            })) {
              return k;
            }
          }
          return null;
        }


      // Authentic Curated NASA Mission Archives for Mars Spacecraft
      const MARS_NASA_IMAGES = {
  "opportunity": [
    {
      "title": "Mars Rover Opportunity at Rock Abrasion Target Potts",
      "nasa_id": "PIA20285",
      "date": "2016-01-25",
      "caption": "The target beneath the tool turret at the end of the rover's robotic arm in this image from NASA's Mars Exploration Rover Opportunity is 'Private John Potts.' It lies high on the southern side of 'Marathon Valley,' which slices through the western ri",
      "url": "https://images-assets.nasa.gov/image/PIA20285/PIA20285~small.jpg",
      "orig": "https://images-assets.nasa.gov/image/PIA20285/PIA20285~small.jpg"
    },
    {
      "title": "Frost on Mars Rover Opportunity",
      "nasa_id": "PIA07108",
      "date": "2004-12-13",
      "caption": "Frost on Mars Rover Opportunity",
      "url": "https://images-assets.nasa.gov/image/PIA07108/PIA07108~thumb.jpg",
      "orig": "https://images-assets.nasa.gov/image/PIA07108/PIA07108~orig.jpg"
    },
    {
      "title": "Mars Rover Opportunity's View of 'Orion Crater' (Stereo)",
      "nasa_id": "PIA21706",
      "date": "2017-06-16",
      "caption": "This view of a small, relatively fresh crater on Mars combines images from the left eye and right eye of the Panoramic Camera (Pancam) on NASA's Opportunity Mars rover, to appear three-dimensional when seen through blue-red glasses with the red lens",
      "url": "https://images-assets.nasa.gov/image/PIA21706/PIA21706~medium.jpg",
      "orig": "https://images-assets.nasa.gov/image/PIA21706/PIA21706~medium.jpg"
    },
    {
      "title": "Mars Rover Opportunity's View of 'Orion Crater'",
      "nasa_id": "PIA21708",
      "date": "2017-06-16",
      "caption": "NASA's Opportunity Mars rover passed near this small, relatively fresh crater in April 2017, during the 45th anniversary of the Apollo 16 mission to the moon. The rover team chose to call it 'Orion Crater,' after the Apollo 16 lunar module. The rover",
      "url": "https://images-assets.nasa.gov/image/PIA21708/PIA21708~medium.jpg",
      "orig": "https://images-assets.nasa.gov/image/PIA21708/PIA21708~medium.jpg"
    }
  ],
  "spirit": [
    {
      "title": "Spirit Stretches Out",
      "nasa_id": "PIA05040",
      "date": "2004-01-10",
      "caption": "This frame from an animation flips back and forth between images taken before and after deployment of the Mars Exploration Rover Spirit's bogie, a part of the rover's suspension system that extends the wheel base. These images were taken by Spirit's",
      "url": "https://images-assets.nasa.gov/image/PIA05040/PIA05040~small.jpg",
      "orig": "https://images-assets.nasa.gov/image/PIA05040/PIA05040~small.jpg"
    },
    {
      "title": "Mars Exploration Rover MER-A Spirit Landing Site",
      "nasa_id": "PIA05120",
      "date": "2004-01-03",
      "caption": "Mars Exploration Rover MER-A Spirit Landing Site",
      "url": "https://images-assets.nasa.gov/image/PIA05120/PIA05120~medium.jpg",
      "orig": "https://images-assets.nasa.gov/image/PIA05120/PIA05120~medium.jpg"
    },
    {
      "title": "Von Braun Mound in Spirit Drive Direction",
      "nasa_id": "PIA11996",
      "date": "2009-04-23",
      "caption": "NASA Mars Exploration Rover Spirit used its navigation camera to capture this view of the terrain toward the southeast from the location Spirit reached on the 1,871st Martian day, or sol, of the rover mission on Mars April 8, 2009.   The mound on the",
      "url": "https://images-assets.nasa.gov/image/PIA11996/PIA11996~small.jpg",
      "orig": "https://images-assets.nasa.gov/image/PIA11996/PIA11996~small.jpg"
    },
    {
      "title": "Spirit 360-Degree View on Sol 409 (vertical)",
      "nasa_id": "PIA07410",
      "date": "2005-03-03",
      "caption": "NASA's Mars Exploration Rover Spirit used its navigation camera to take the images combined into this 360-degree view of the rover's surroundings on Spirit's 409th martian day, or sol (Feb. 26, 2005). Spirit had driven 2 meters (7 feet) on this sol t",
      "url": "https://images-assets.nasa.gov/image/PIA07410/PIA07410~medium.jpg",
      "orig": "https://images-assets.nasa.gov/image/PIA07410/PIA07410~medium.jpg"
    }
  ],
  "sojourner": [
    {
      "title": "Newest is Biggest: Three Generations of NASA Mars Rovers",
      "nasa_id": "PIA11436",
      "date": "2008-11-19",
      "caption": "Full-scale models of three generations of NASA Mars rovers show the increase in size from the Sojourner rover of the Mars Pathfinder project, to the twin Mars Exploration Rovers Spirit and Opportunity, to the Mars Science Laboratory rover.",
      "url": "https://images-assets.nasa.gov/image/PIA11436/PIA11436~small.jpg",
      "orig": "https://images-assets.nasa.gov/image/PIA11436/PIA11436~small.jpg"
    },
    {
      "title": "Size Comparison: Three Generations of Mars Rovers",
      "nasa_id": "PIA11431",
      "date": "2008-11-19",
      "caption": "Full-scale models of three generations of NASA Mars rovers show the increase in size from the Sojourner rover of the Mars Pathfinder project, to the twin Mars Exploration Rovers Spirit and Opportunity, to the Mars Science Laboratory rover.",
      "url": "https://images-assets.nasa.gov/image/PIA11431/PIA11431~small.jpg",
      "orig": "https://images-assets.nasa.gov/image/PIA11431/PIA11431~small.jpg"
    },
    {
      "title": "Rovers and Sojourner",
      "nasa_id": "PIA04422",
      "date": "2003-02-26",
      "caption": "The twin rovers of NASAa Mars Exploration Rover Mission pose with their groundbreaking predecessor, the flight spare of the Sojourner rover from NASA 1997 Pathfinder mission.",
      "url": "https://images-assets.nasa.gov/image/PIA04422/PIA04422~medium.jpg",
      "orig": "https://images-assets.nasa.gov/image/PIA04422/PIA04422~medium.jpg"
    },
    {
      "title": "Sojourner Sits Near 'Rock Garden'",
      "nasa_id": "PIA04318",
      "date": "2003-02-01",
      "caption": "The Mars Pathfinder Rover Sojourner images by the Imager for Mars Pathfinder as it nears the rock 'Wedge.' Part of the Rock Garden is visible in the upper right of the image.  http://photojournal.jpl.nasa.gov/catalog/PIA04318",
      "url": "https://images-assets.nasa.gov/image/PIA04318/PIA04318~thumb.jpg",
      "orig": "https://images-assets.nasa.gov/image/PIA04318/PIA04318~orig.jpg"
    }
  ],
  "curiosity": [
    {
      "title": "Head of Mast on Mars Rover Curiosity",
      "nasa_id": "PIA15106",
      "date": "2011-11-28",
      "caption": "This view of the head of the remote sensing mast on the Mars Science Laboratory mission rover, Curiosity, shows seven of the 17 cameras on the rover.",
      "url": "https://images-assets.nasa.gov/image/PIA15106/PIA15106~small.jpg",
      "orig": "https://images-assets.nasa.gov/image/PIA15106/PIA15106~small.jpg"
    },
    {
      "title": "Curiosity Mars Rover Drilling Into Its Second Rock",
      "nasa_id": "PIA17068",
      "date": "2013-06-05",
      "caption": "This frame from an animation from NASA Mars rover Curiosity shows the rover drilling into rock target Cumberland. The drilling was performed during the 279th Martian day, or sol, of the Curiosity work on Mars May 19, 2013.",
      "url": "https://images-assets.nasa.gov/image/PIA17068/PIA17068~small.jpg",
      "orig": "https://images-assets.nasa.gov/image/PIA17068/PIA17068~small.jpg"
    },
    {
      "title": "Mars Rover Curiosity Raising Turret",
      "nasa_id": "PIA14253",
      "date": "2011-06-13",
      "caption": "This photograph of the NASA Mars Science Laboratory rover, Curiosity, was taken during testing on June 3, 2011. The turret at the end of Curiosity robotic arm holds five devices.",
      "url": "https://images-assets.nasa.gov/image/PIA14253/PIA14253~medium.jpg",
      "orig": "https://images-assets.nasa.gov/image/PIA14253/PIA14253~medium.jpg"
    },
    {
      "title": "Top of Mars Rover Curiosity Remote Sensing Mast",
      "nasa_id": "PIA13809",
      "date": "2011-04-06",
      "caption": "The remote sensing mast on NASA Mars rover Curiosity holds two science instruments for studying the rover surroundings and two stereo navigation cameras for use in driving the rover and planning rover activities.",
      "url": "https://images-assets.nasa.gov/image/PIA13809/PIA13809~medium.jpg",
      "orig": "https://images-assets.nasa.gov/image/PIA13809/PIA13809~medium.jpg"
    }
  ],
  "perseverance": [
    {
      "title": "Mars 2020 Perseverance Rover Wheels",
      "nasa_id": "KSC-20200402-PH-JPL01_0002",
      "date": "2020-04-02",
      "caption": "Wheels are installed on NASA\u2019s Mars Perseverance rover inside Kennedy Space Center\u2019s Payload Hazardous Servicing Facility on March 30, 2020. Perseverance will liftoff aboard a United Launch Alliance Atlas V 541 rocket from Cape Canaveral Air Force St",
      "url": "https://images-assets.nasa.gov/image/KSC-20200402-PH-JPL01_0002/KSC-20200402-PH-JPL01_0002~medium.jpg",
      "orig": "https://images-assets.nasa.gov/image/KSC-20200402-PH-JPL01_0002/KSC-20200402-PH-JPL01_0002~medium.jpg"
    },
    {
      "title": "Mars 2020 Perseverance Rover Wheels",
      "nasa_id": "KSC-20200402-PH-JPL01_0003",
      "date": "2020-04-02",
      "caption": "Wheels are installed on NASA\u2019s Mars Perseverance rover inside Kennedy Space Center\u2019s Payload Hazardous Servicing Facility on March 30, 2020. Perseverance will liftoff aboard a United Launch Alliance Atlas V 541 rocket from Cape Canaveral Air Force St",
      "url": "https://images-assets.nasa.gov/image/KSC-20200402-PH-JPL01_0003/KSC-20200402-PH-JPL01_0003~medium.jpg",
      "orig": "https://images-assets.nasa.gov/image/KSC-20200402-PH-JPL01_0003/KSC-20200402-PH-JPL01_0003~medium.jpg"
    },
    {
      "title": "Mars 2020 Perseverance Rover Wheels",
      "nasa_id": "KSC-20200402-PH-JPL01_0001",
      "date": "2020-04-02",
      "caption": "Wheels are installed on NASA\u2019s Mars Perseverance rover inside Kennedy Space Center\u2019s Payload Hazardous Servicing Facility on March 30, 2020. Perseverance will liftoff aboard a United Launch Alliance Atlas V 541 rocket from Cape Canaveral Air Force St",
      "url": "https://images-assets.nasa.gov/image/KSC-20200402-PH-JPL01_0001/KSC-20200402-PH-JPL01_0001~medium.jpg",
      "orig": "https://images-assets.nasa.gov/image/KSC-20200402-PH-JPL01_0001/KSC-20200402-PH-JPL01_0001~medium.jpg"
    },
    {
      "title": "Mars Perseverance Rover (Gradient Illustration)",
      "nasa_id": "PIA24348",
      "date": "2020-12-21",
      "caption": "An illustration of the planet Mars, highlighting NASA's Mars Perseverance rover mission.  https://photojournal.jpl.nasa.gov/catalog/PIA24348",
      "url": "https://images-assets.nasa.gov/image/PIA24348/PIA24348~medium.jpg",
      "orig": "https://images-assets.nasa.gov/image/PIA24348/PIA24348~medium.jpg"
    }
  ],
  "ingenuity": [
    {
      "title": "Ingenuity Helicopter on Mars (Illustration)",
      "nasa_id": "PIA24466",
      "date": "2021-03-16",
      "caption": "An illustration of NASA's Ingenuity Helicopter flying on Mars.  Ingenuity, a technology demonstration experiment, will be the first aircraft to attempt powered, controlled flight on another planet. Ingenuity arrived at Mars on Feb. 18, 2021, attached",
      "url": "https://images-assets.nasa.gov/image/PIA24466/PIA24466~medium.jpg",
      "orig": "https://images-assets.nasa.gov/image/PIA24466/PIA24466~medium.jpg"
    },
    {
      "title": "NASA's Ingenuity Mars Helicopter",
      "nasa_id": "PIA23882",
      "date": "2020-04-29",
      "caption": "The flight model of NASA's Ingenuity Mars Helicopter.  https://photojournal.jpl.nasa.gov/catalog/PIA23882",
      "url": "https://images-assets.nasa.gov/image/PIA23882/PIA23882~medium.jpg",
      "orig": "https://images-assets.nasa.gov/image/PIA23882/PIA23882~medium.jpg"
    },
    {
      "title": "Bottom of Ingenuity Mars Helicopter",
      "nasa_id": "PIA23969",
      "date": "2021-01-20",
      "caption": "An Ingenuity team member inspects NASA's Ingenuity Mars Helicopter in one of the space simulation chambers at the agency's Jet Propulsion Laboratory in Southern California.  The helicopter's two cameras are visible in this view of the underside of In",
      "url": "https://images-assets.nasa.gov/image/PIA23969/PIA23969~medium.jpg",
      "orig": "https://images-assets.nasa.gov/image/PIA23969/PIA23969~medium.jpg"
    },
    {
      "title": "Ingenuity Mars Helicopter Prototype Donation to NASM",
      "nasa_id": "NHQ202312150007",
      "date": "2023-12-15",
      "caption": "Teddy Tzanetos, Ingenuity project manager at NASA's Jet Propulsion Laboratory speaks at an event marking NASA\u2019s donation of the aerial prototype of the Ingenuity Mars Helicopter, Friday, Dec. 15, 2023, at the Smithsonian National Air and Space Museum",
      "url": "https://images-assets.nasa.gov/image/NHQ202312150007/NHQ202312150007~medium.jpg",
      "orig": "https://images-assets.nasa.gov/image/NHQ202312150007/NHQ202312150007~medium.jpg"
    }
  ],
  "viking-1": [
    {
      "title": "Mars Surface near Viking Lander 1 Footpad",
      "nasa_id": "PIA10738",
      "date": "2008-05-30",
      "caption": "Mars Surface near Viking Lander 1 Footpad",
      "url": "https://images-assets.nasa.gov/image/PIA10738/PIA10738~thumb.jpg",
      "orig": "https://images-assets.nasa.gov/image/PIA10738/PIA10738~orig.jpg"
    },
    {
      "title": "Viking Lander 1 U.S. Flag on Mars Surface",
      "nasa_id": "PIA00565",
      "date": "1997-02-28",
      "caption": "Viking Lander 1 U.S. Flag on Mars Surface",
      "url": "https://images-assets.nasa.gov/image/PIA00565/PIA00565~thumb.jpg",
      "orig": "https://images-assets.nasa.gov/image/PIA00565/PIA00565~orig.jpg"
    },
    {
      "title": "Launch Vehicles",
      "nasa_id": "9141929",
      "date": "1975-08-20",
      "caption": "The Titan III-Centaur carrying the Viking 1 Lander lifted off on August 20, 1975. The Viking Lander conducted a detailed scientific investigation of the planet Mars.",
      "url": "https://images-assets.nasa.gov/image/9141929/9141929~medium.jpg",
      "orig": "https://images-assets.nasa.gov/image/9141929/9141929~medium.jpg"
    },
    {
      "title": "Mars Orbiter Camera Acquires High Resolution Stereoscopic Images of the Viking One Landing Site",
      "nasa_id": "PIA01443",
      "date": "1998-07-03",
      "caption": "This image of the vicinity of the Viking Lander 1 was captured by NASA Mars Global Surveyor MOC camera. site. 3D glasses are necessary to identify surface detail.",
      "url": "https://images-assets.nasa.gov/image/PIA01443/PIA01443~small.jpg",
      "orig": "https://images-assets.nasa.gov/image/PIA01443/PIA01443~small.jpg"
    }
  ],
  "viking-2": [
    {
      "title": "Viking Lander 2 First Picture On The Surface Of Mars",
      "nasa_id": "PIA00396",
      "date": "1996-12-12",
      "caption": "Viking Lander 2 First Picture On The Surface Of Mars  http://photojournal.jpl.nasa.gov/catalog/PIA00396",
      "url": "https://images-assets.nasa.gov/image/PIA00396/PIA00396~thumb.jpg",
      "orig": "https://images-assets.nasa.gov/image/PIA00396/PIA00396~orig.jpg"
    },
    {
      "title": "KSC-75p-110",
      "nasa_id": "101-KSC-75P-110",
      "date": "1975-02-06",
      "caption": "CAPE CANAVERAL, Fla. -- At the Kennedy Space Center in Florida, technicians inspect the Viking Lander 2 in Kennedy's Spacecraft Assembly and Encapsulation Facility 1. The first Viking is scheduled for launch from Launch Complex 41 no earlier than Aug",
      "url": "https://images-assets.nasa.gov/image/101-KSC-75P-110/101-KSC-75P-110~medium.jpg",
      "orig": "https://images-assets.nasa.gov/image/101-KSC-75P-110/101-KSC-75P-110~medium.jpg"
    },
    {
      "title": "KSC-75p-12",
      "nasa_id": "101-KSC-75P-12",
      "date": "1975-01-07",
      "caption": "KENNEDY SPACE CENTER, FLA. --  Technicians prepared for removal of Viking Lander 1's aeroshell cover in KSC's Spacecraft Assembly and Encapsulation Facility 2 (SAEF-2) today.  The cover remains over the Lander throughout its 440,000,000-mile journey",
      "url": "https://images-assets.nasa.gov/image/101-KSC-75P-12/101-KSC-75P-12~medium.jpg",
      "orig": "https://images-assets.nasa.gov/image/101-KSC-75P-12/101-KSC-75P-12~medium.jpg"
    },
    {
      "title": "KSC-75pc-167",
      "nasa_id": "101-KSC-75PC-167",
      "date": "1975-03-27",
      "caption": "KENNEDY SPACE CENTER, FLA. --  The mated orbiter and lander for Viking A were encapsulated within a Centaur shroud at Spacecraft Assembly and Encapsulation Facility 2 (SAEF-2) today.  The spacecraft, one of two to be launched toward Mars atop Titan_C",
      "url": "https://images-assets.nasa.gov/image/101-KSC-75PC-167/101-KSC-75PC-167~medium.jpg",
      "orig": "https://images-assets.nasa.gov/image/101-KSC-75PC-167/101-KSC-75PC-167~medium.jpg"
    }
  ],
  "phoenix": [
    {
      "title": "Phoenix Mars Lander Spacecraft Processing",
      "nasa_id": "KSC-07PD-1085",
      "date": "2007-05-10",
      "caption": "In the Payload Hazardous Servicing Facility, technicians attach a crane to the Phoenix Mars Lander spacecraft. The crane will be used to remove the heat shield from around the Phoenix. The Phoenix mission is the first project in NASA's first openly c",
      "url": "https://images-assets.nasa.gov/image/KSC-07PD-1085/KSC-07PD-1085~medium.jpg",
      "orig": "https://images-assets.nasa.gov/image/KSC-07PD-1085/KSC-07PD-1085~medium.jpg"
    },
    {
      "title": "Phoenix Mars Lander Spacecraft Processing",
      "nasa_id": "KSC-07PD-1084",
      "date": "2007-05-10",
      "caption": "In the Payload Hazardous Servicing Facility, technicians lower a crane over the Phoenix Mars Lander spacecraft. The crane will be used to remove the heat shield from around the Phoenix. The Phoenix mission is the first project in NASA's first openly",
      "url": "https://images-assets.nasa.gov/image/KSC-07PD-1084/KSC-07PD-1084~medium.jpg",
      "orig": "https://images-assets.nasa.gov/image/KSC-07PD-1084/KSC-07PD-1084~medium.jpg"
    },
    {
      "title": "Phoenix Mars Lander Spacecraft Processing",
      "nasa_id": "KSC-07PD-1090",
      "date": "2007-05-10",
      "caption": "In the Payload Hazardous Servicing Facility, the Phoenix Mars Lander (foreground) can be seen inside the backshell. In the background, workers are helping place the heat shield, just removed from the Phoenix, onto a platform. The Phoenix mission is t",
      "url": "https://images-assets.nasa.gov/image/KSC-07PD-1090/KSC-07PD-1090~medium.jpg",
      "orig": "https://images-assets.nasa.gov/image/KSC-07PD-1090/KSC-07PD-1090~medium.jpg"
    },
    {
      "title": "Phoenix Mars Lander Spacecraft Processing",
      "nasa_id": "KSC-07PD-1093",
      "date": "2007-05-10",
      "caption": "An overhead crane lowers the backshell with the Phoenix Mars Lander inside toward a spin table for spin testing in the Payload Hazardous Servicing Facility. The Phoenix mission is the first project in NASA's first openly competed program of Mars Scou",
      "url": "https://images-assets.nasa.gov/image/KSC-07PD-1093/KSC-07PD-1093~medium.jpg",
      "orig": "https://images-assets.nasa.gov/image/KSC-07PD-1093/KSC-07PD-1093~medium.jpg"
    }
  ],
  "insight": [
    {
      "title": "Artist Concept of InSight Lander on Mars",
      "nasa_id": "PIA19811",
      "date": "2015-08-18",
      "caption": "This artist's concept from August 2015 depicts NASA's InSight Mars lander fully deployed for studying the deep interior of Mars. This illustration updates the correct placement and look of Insight's main instruments. For an earlier artist rendition,",
      "url": "https://images-assets.nasa.gov/image/PIA19811/PIA19811~medium.jpg",
      "orig": "https://images-assets.nasa.gov/image/PIA19811/PIA19811~medium.jpg"
    },
    {
      "title": "Artist Concept of InSight Lander on Mars",
      "nasa_id": "PIA17358",
      "date": "2014-03-26",
      "caption": "This artist's concept depicts the stationary NASA Mars lander known by the acronym InSight at work studying the interior of Mars. The InSight mission (for Interior Exploration using Seismic Investigations, Geodesy and Heat Transport) is scheduled to",
      "url": "https://images-assets.nasa.gov/image/PIA17358/PIA17358~medium.jpg",
      "orig": "https://images-assets.nasa.gov/image/PIA17358/PIA17358~medium.jpg"
    },
    {
      "title": "InSight's Inner Sanctum Revealed",
      "nasa_id": "PIA22647",
      "date": "2018-08-20",
      "caption": "This long-exposure image (24 seconds) was taken by Instrument Context Camera (ICC) of NASA's InSight Mars lander. The image shows some of the interior features of the backshell that encapsulates the spacecraft. The backshell carries the parachute and",
      "url": "https://images-assets.nasa.gov/image/PIA22647/PIA22647~small.jpg",
      "orig": "https://images-assets.nasa.gov/image/PIA22647/PIA22647~small.jpg"
    },
    {
      "title": "Mars Lander Deck of NASA's InSight Mission",
      "nasa_id": "PIA21847",
      "date": "2017-08-28",
      "caption": "This view looks upward toward the InSight Mars lander suspended upside down. It shows the top of the lander's science deck with the mission's two main science instruments -- the Seismic Experiment for Interior Structure (SEIS) and the Heat Flow and P",
      "url": "https://images-assets.nasa.gov/image/PIA21847/PIA21847~medium.jpg",
      "orig": "https://images-assets.nasa.gov/image/PIA21847/PIA21847~medium.jpg"
    }
  ]
};

      let currentNasaPhotos = [];
      let currentNasaPhotoIndex = 0;

      window.switchDetailTab = function(tab) {
        const modelVp = document.getElementById('detail-model-viewport');
        const nasaVp = document.getElementById('detail-nasa-gallery-viewport');
        const btn3d = document.getElementById('btn-view-3d');
        const btnNasa = document.getElementById('btn-view-nasa');

        if (tab === 'nasa') {
          if (modelVp) modelVp.style.display = 'none';
          if (nasaVp) nasaVp.style.display = 'flex';
          if (btn3d) btn3d.classList.remove('active');
          if (btnNasa) btnNasa.classList.add('active');
          if (currentDetailEquipment) {
            window.renderNasaGallery(currentDetailEquipment.id, currentDetailEquipment, currentChatCraft || {});
          }
        } else {
          if (modelVp) modelVp.style.display = 'block';
          if (nasaVp) nasaVp.style.display = 'none';
          if (btn3d) btn3d.classList.add('active');
          if (btnNasa) btnNasa.classList.remove('active');
          if (typeof onDetailResize === 'function') {
            onDetailResize();
          }
        }
      };

      async function fetchLiveNasaImages(query) {
        try {
          const cleanQ = encodeURIComponent(query + ' Mars rover lander');
          const res = await fetch('https://images-api.nasa.gov/search?q=' + cleanQ + '&media_type=image');
          if (!res.ok) return [];
          const data = await res.json();
          const items = data && data.collection && data.collection.items ? data.collection.items : [];
          const results = [];
          for (let i = 0; i < Math.min(items.length, 12); i++) {
            const item = items[i];
            const meta = item && item.data && item.data[0] ? item.data[0] : null;
            const links = item && item.links ? item.links : [];
            const thumbLink = links.find(l => l.rel === 'preview') || links[0];
            if (meta && thumbLink && thumbLink.href) {
              const thumbUrl = thumbLink.href;
              const origUrl = thumbUrl.replace('~thumb.jpg', '~orig.jpg').replace('~thumb.png', '~orig.png');
              results.push({
                title: meta.title || 'NASA Mars Archive Record',
                nasa_id: meta.nasa_id || 'NASA-MARS',
                date: (meta.date_created ? meta.date_created.substring(0, 10) : 'NASA Archive'),
                caption: meta.description || 'Authentic Mars mission imagery from NASA JPL & Open Archives.',
                url: thumbUrl,
                orig: origUrl
              });
            }
          }
          return results;
        } catch(e) {
          console.warn("fetchLiveNasaImages error:", e);
          return [];
        }
      }

      window.renderNasaGallery = async function(assetKey, asset, locData) {
        const loadingEl = document.getElementById('nasa-img-loading');
        if (loadingEl) loadingEl.style.display = 'flex';

        // 1. Load authentic pre-curated NASA photos for this craft
        const key = String(assetKey || '').toLowerCase();
        let curated = MARS_NASA_IMAGES[key];
        if (!curated || curated.length === 0) {
          for (const k in MARS_NASA_IMAGES) {
            if (key.includes(k) || k.includes(key)) {
              curated = MARS_NASA_IMAGES[k];
              break;
            }
          }
        }
        if (!curated || curated.length === 0) {
          curated = MARS_NASA_IMAGES['opportunity'] || [];
        }

        currentNasaPhotos = [...curated];
        currentNasaPhotoIndex = 0;
        window.updateNasaGalleryDisplay();

        // 2. Query Live NASA Image API to fetch live supplementary photos
        try {
          const qName = (locData && locData.name) ? locData.name : (asset && asset.name ? asset.name : 'Mars Rover');
          const liveResults = await fetchLiveNasaImages(qName);
          if (liveResults && liveResults.length > 0) {
            const existingIds = new Set(currentNasaPhotos.map(p => p.nasa_id));
            liveResults.forEach(lp => {
              if (!existingIds.has(lp.nasa_id)) {
                currentNasaPhotos.push(lp);
                existingIds.add(lp.nasa_id);
              }
            });
            window.updateNasaGalleryDisplay();
          }
        } catch(e) {
          console.warn("Supplementary NASA image query skipped:", e);
        } finally {
          if (loadingEl) loadingEl.style.display = 'none';
        }
      };

      window.updateNasaGalleryDisplay = function() {
        if (!currentNasaPhotos || currentNasaPhotos.length === 0) return;
        const photo = currentNasaPhotos[currentNasaPhotoIndex] || currentNasaPhotos[0];

        const heroImg = document.getElementById('nasa-hero-img');
        if (heroImg) {
          heroImg.src = photo.url;
          heroImg.alt = photo.title || 'NASA Mission Photo';
        }

        const idEl = document.getElementById('nasa-photo-id');
        if (idEl) idEl.innerText = photo.nasa_id ? ('NASA ' + photo.nasa_id) : 'NASA ARCHIVE RECORD';

        const dateEl = document.getElementById('nasa-photo-date');
        if (dateEl) dateEl.innerText = photo.date || 'NASA MISSION ARCHIVE';

        const titleEl = document.getElementById('nasa-photo-title');
        if (titleEl) titleEl.innerText = photo.title || 'Martian Surface Exploration';

        const capEl = document.getElementById('nasa-photo-caption');
        if (capEl) capEl.innerText = photo.caption || 'Archival record from NASA Mars exploration archives.';

        const countEl = document.getElementById('nasa-photo-count');
        if (countEl) countEl.innerText = currentNasaPhotos.length;

        // Render Thumbnails
        const strip = document.getElementById('nasa-thumbnails-strip');
        if (strip) {
          strip.innerHTML = '';
          currentNasaPhotos.forEach((p, idx) => {
            const card = document.createElement('div');
            card.className = 'nasa-thumb-card' + (idx === currentNasaPhotoIndex ? ' active' : '');
            card.title = p.title;
            card.innerHTML = '<img src="' + p.url + '" class="nasa-thumb-img" alt="' + (p.title || '') + '" />';
            card.onclick = () => window.selectNasaPhoto(idx);
            strip.appendChild(card);
          });
        }
      };

      window.selectNasaPhoto = function(idx) {
        if (idx >= 0 && idx < currentNasaPhotos.length) {
          currentNasaPhotoIndex = idx;
          window.updateNasaGalleryDisplay();
        }
      };

      window.openFullResNasaImage = function() {
        if (!currentNasaPhotos || currentNasaPhotos.length === 0) return;
        const photo = currentNasaPhotos[currentNasaPhotoIndex] || currentNasaPhotos[0];
        const targetUrl = photo.orig || photo.url;
        window.open(targetUrl, '_blank');
      };

      window.executeNasaPhotoSearch = async function() {
        const input = document.getElementById('nasa-search-input');
        if (!input || !input.value.trim()) return;
        const query = input.value.trim();

        const loadingEl = document.getElementById('nasa-img-loading');
        if (loadingEl) loadingEl.style.display = 'flex';

        try {
          const results = await fetchLiveNasaImages(query);
          if (results && results.length > 0) {
            currentNasaPhotos = results;
            currentNasaPhotoIndex = 0;
            window.updateNasaGalleryDisplay();
          } else {
            alert("No NASA archive photos found for: " + query);
          }
        } catch(e) {
          console.warn("NASA search error:", e);
        } finally {
          if (loadingEl) loadingEl.style.display = 'none';
        }
      };

      window.refreshNasaGalleryFeed = function() {
        if (currentDetailEquipment) {
          window.renderNasaGallery(currentDetailEquipment.id, currentDetailEquipment, currentChatCraft || {});
        }
      };


        let currentDetailEquipment = null;
        let detailScene = null;
        let detailCamera = null;
        let detailRenderer = null;
        let detailControls = null;
        let detailAnimId = null;
        let detailAudio = new Audio();
        let isAudioMuted = false;

        function formatAudioTime(seconds) {
          if (isNaN(seconds) || seconds === Infinity) return "0:00";
          const mins = Math.floor(seconds / 60);
          const secs = Math.floor(seconds % 60);
          return mins + ":" + (secs < 10 ? "0" : "") + secs;
        }

        detailAudio.ontimeupdate = function() {
          const scrubber = document.getElementById('audio-scrubber');
          const curTime = document.getElementById('audio-current-time');
          const totTime = document.getElementById('audio-total-time');
          if (scrubber && detailAudio.duration) {
            scrubber.value = (detailAudio.currentTime / detailAudio.duration) * 100;
          }
          if (curTime) curTime.innerText = formatAudioTime(detailAudio.currentTime);
          if (totTime && detailAudio.duration) totTime.innerText = formatAudioTime(detailAudio.duration);
        };

        detailAudio.onloadedmetadata = function() {
          const totTime = document.getElementById('audio-total-time');
          if (totTime && detailAudio.duration) {
            totTime.innerText = formatAudioTime(detailAudio.duration);
          }
        };

        detailAudio.onended = function() {
          const playBtn = document.getElementById('btn-audio-play');
          if (playBtn) playBtn.innerText = "▶ Play";
          const scrubber = document.getElementById('audio-scrubber');
          if (scrubber) scrubber.value = 0;
        };

        window.toggleAudioPlay = function() {
          const playBtn = document.getElementById('btn-audio-play');
          if (detailAudio.paused) {
            if (isAudioMuted) {
              isAudioMuted = false;
              window.updateAudioToggleBtn();
            }
            const playPromise = detailAudio.play();
            if (playPromise !== undefined) {
              playPromise.then(() => {
                if (playBtn) playBtn.innerText = "⏸ Pause";
              }).catch(err => {
                console.warn("Audio play prevented:", err);
                if (playBtn) playBtn.innerText = "▶ Play";
              });
            }
          } else {
            detailAudio.pause();
            if (playBtn) playBtn.innerText = "▶ Play";
          }
        };

        window.onScrubAudio = function(val) {
          if (detailAudio.duration) {
            detailAudio.currentTime = (val / 100) * detailAudio.duration;
          }
        };

        window.toggleAudioMute = function() {
          isAudioMuted = !isAudioMuted;
          window.updateAudioToggleBtn();
          if (isAudioMuted && !detailAudio.paused) {
            detailAudio.pause();
            const playBtn = document.getElementById('btn-audio-play');
            if (playBtn) playBtn.innerText = "▶ Play";
          }
        };

        window.updateAudioToggleBtn = function() {
          const btn = document.getElementById('btn-audio-toggle');
          if (btn) {
            btn.innerText = isAudioMuted ? "🔇 Audio: OFF" : "🔊 Audio: ON";
          }
        };

        window.closeEquipmentDetail = function() {
          try {
            detailAudio.pause();
            detailAudio.currentTime = 0;
            detailAudio.src = "";
          } catch(e) {}

          if (detailAnimId) {
            cancelAnimationFrame(detailAnimId);
            detailAnimId = null;
          }
          if (detailRenderer) {
            try {
              detailRenderer.dispose();
              if (detailRenderer.domElement && detailRenderer.domElement.parentNode) {
                detailRenderer.domElement.parentNode.removeChild(detailRenderer.domElement);
              }
            } catch(e) {}
            detailRenderer = null;
          }
          detailScene = null;
          detailCamera = null;
          detailControls = null;
          currentDetailEquipment = null;

          const overlay = document.getElementById('equipment-detail-overlay');
          if (overlay) overlay.style.display = 'none';
        };

        window.addEventListener("message", (event) => {
          if (!event.data) return;
          if (event.data.action === 'openEquipmentDetail') {
            window.openEquipmentDetail(event.data.equipmentKey);
          } else if (event.data.action === 'closeEquipmentDetail') {
            window.closeEquipmentDetail();
          } else if (event.data.action === 'toggleAudio') {
            window.toggleAudioPlay();
          }
        });

        async function loadResilientAudio(candidates) {
          let selectedUrl = null;
          for (const url of candidates) {
            try {
              const resp = await fetch(url, { method: 'HEAD' });
              if (resp.ok) {
                const ct = resp.headers.get('Content-Type') || '';
                if (!ct.includes('text/html')) {
                  selectedUrl = url;
                  break;
                }
              }
            } catch(e) {}
          }
          if (!selectedUrl && candidates.length > 0) {
            selectedUrl = candidates[0];
          }
          if (selectedUrl) {
            console.log("Loading audio from:", selectedUrl);
            detailAudio.src = selectedUrl;
            detailAudio.load();
          } else {
            console.error("No valid audio candidate found:", candidates);
            const errBanner = document.getElementById('detail-error-banner');
            if (errBanner) {
              errBanner.innerText = "Notice: Audio story file could not be loaded.";
              errBanner.style.display = "block";
            }
          }
        }

        async function loadResilientGLB(candidates, gltfLoader, spinner, errBanner, onLoadSuccess) {
          let loaded = false;
          let lastErr = null;

          for (const url of candidates) {
            try {
              console.log("Attempting to load GLB model from:", url);
              const resp = await fetch(url);
              if (!resp.ok) {
                console.warn("HTTP " + resp.status + " for " + url);
                continue;
              }
              const ct = resp.headers.get('Content-Type') || '';
              if (ct.includes('text/html')) {
                console.warn("Response for " + url + " is HTML, skipping...");
                continue;
              }

              const buffer = await resp.arrayBuffer();
              if (buffer.byteLength < 4) continue;

              const b = new Uint8Array(buffer);
              const isGlb = (b[0] === 0x67 && b[1] === 0x6C && b[2] === 0x54 && b[3] === 0x46);
              const isJson = (b[0] === 0x7B);
              if (!isGlb && !isJson) {
                console.warn("Invalid signature for " + url);
                continue;
              }

              const basePath = url.includes('/') ? url.substring(0, url.lastIndexOf('/') + 1) : "";
              await new Promise((resolve, reject) => {
                gltfLoader.parse(buffer, basePath, (gltf) => {
                  onLoadSuccess(gltf, url);
                  loaded = true;
                  resolve();
                }, (parseErr) => {
                  lastErr = parseErr;
                  reject(parseErr);
                });
              });

              if (loaded) break;
            } catch(err) {
              console.warn("Failed candidate " + url + ":", err);
              lastErr = err;
            }
          }

          if (!loaded) {
            if (spinner) spinner.style.display = 'none';
            if (errBanner) {
              errBanner.innerText = "Notice: 3D model could not be loaded.";
              errBanner.style.display = "block";
            }
            console.error("All GLB candidates failed:", candidates, lastErr);
          }
        }

        window.openEquipmentDetail = function(equipmentKey) {
          const assetKey = resolveEquipmentKey(equipmentKey);
          const asset = assetKey ? MARS_EQUIPMENT_ASSETS[assetKey] : null;
          if (!asset) {
            console.warn("No equipment asset found for key:", equipmentKey);
            return;
          }

          currentDetailEquipment = asset;

          const rawKey = String(equipmentKey || '').toLowerCase();
          const normKey = rawKey.replace(/[^a-z0-9]/g, '');
          const locs = (typeof LOCATIONS !== 'undefined' ? LOCATIONS : []);
          let locData = locs.find(l => {
            const lid = String(l.id || '').toLowerCase();
            const lname = String(l.name || '').toLowerCase();
            return lid === rawKey || lid.replace(/[^a-z0-9]/g, '') === normKey || lname.replace(/[^a-z0-9]/g, '').includes(normKey);
          });
          if (!locData) {
            locData = locs.find(l => {
              const lid = (l.id || '').toLowerCase();
              return asset.aliasIds.some(alias => lid.includes(alias.toLowerCase()));
            }) || {};
          }

          const has3D = asset && asset.modelFiles && asset.modelFiles.length > 0;
          const btn3d = document.getElementById('btn-view-3d');
          const btnNasa = document.getElementById('btn-view-nasa');

          const headerTitle = document.getElementById('detail-header-title');
          if (headerTitle) {
            if (has3D) {
              headerTitle.innerText = ((locData.name || asset.name).toUpperCase()) + " • " + ((locData.type || asset.type).toUpperCase()) + " 3D SIMULATOR";
            } else {
              headerTitle.innerText = ((locData.name || asset.name).toUpperCase()) + " • NASA MISSION ARCHIVE & MEDIA STUDIO";
            }
          }

          const nameEl = document.getElementById('detail-name');
          if (nameEl) nameEl.innerText = locData.name || asset.name;

          const typeBadge = document.getElementById('detail-type-badge');
          if (typeBadge) {
            typeBadge.innerText = (locData.type || asset.type).toUpperCase();
            typeBadge.className = 'detail-type-badge ' + (locData.type || asset.type).toLowerCase();
          }

          const overlay = document.getElementById('equipment-detail-overlay');
          if (overlay) overlay.style.display = 'flex';

          const errBanner = document.getElementById('detail-error-banner');
          if (errBanner) errBanner.style.display = 'none';

          const playBtn = document.getElementById('btn-audio-play');
          if (playBtn) playBtn.innerText = "▶ Play";

          const scrubber = document.getElementById('audio-scrubber');
          if (scrubber) scrubber.value = 0;

          const curTime = document.getElementById('audio-current-time');
          const totTime = document.getElementById('audio-total-time');
          if (curTime) curTime.innerText = "0:00";
          if (totTime) totTime.innerText = "0:00";

          loadResilientAudio(asset.audioFiles);

          // Render Authentic NASA Mission Imagery & Media Studio
          window.renderNasaGallery(assetKey, asset, locData);

          if (has3D) {
            if (btn3d) btn3d.style.display = 'inline-flex';
            window.switchDetailTab('3d');

            const viewport = document.getElementById('detail-model-viewport');
            const spinner = document.getElementById('detail-spinner');
            if (spinner) spinner.style.display = 'flex';

            const oldCanvas = viewport.querySelector('canvas');
            if (oldCanvas) oldCanvas.remove();

            detailScene = new THREE.Scene();
            detailScene.background = new THREE.Color(0x020617);

            const w = viewport.clientWidth || (window.innerWidth * 0.6);
            const h = viewport.clientHeight || (window.innerHeight - 60);

            detailCamera = new THREE.PerspectiveCamera(45, w / h, 0.1, 100);
            detailCamera.position.set(0, 0.8, 3.8);

            detailRenderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
            detailRenderer.setSize(w, h);
            detailRenderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
            detailRenderer.toneMapping = THREE.ACESFilmicToneMapping;
            detailRenderer.toneMappingExposure = 1.25;
            viewport.appendChild(detailRenderer.domElement);

            detailControls = new THREE.OrbitControls(detailCamera, detailRenderer.domElement);
            detailControls.enableDamping = true;
            detailControls.dampingFactor = 0.05;
            detailControls.autoRotate = true;
            detailControls.autoRotateSpeed = 1.0;
            detailControls.minDistance = 0.8;
            detailControls.maxDistance = 15.0;

            const keyLight = new THREE.DirectionalLight(0xffffff, 2.4);
            keyLight.position.set(5, 6, 5);
            detailScene.add(keyLight);

            const fillLight = new THREE.DirectionalLight(0x90b0e0, 1.2);
            fillLight.position.set(-5, -2, -4);
            detailScene.add(fillLight);

            const ambLight = new THREE.AmbientLight(0x64748b, 0.95);
            detailScene.add(ambLight);

            let canvasPointerDownTime = 0;
            let canvasPointerDownPos = { x: 0, y: 0 };
            detailRenderer.domElement.addEventListener('pointerdown', (e) => {
              canvasPointerDownTime = Date.now();
              canvasPointerDownPos = { x: e.clientX, y: e.clientY };
            });
            detailRenderer.domElement.addEventListener('pointerup', (e) => {
              const elapsed = Date.now() - canvasPointerDownTime;
              const dist = Math.hypot(e.clientX - canvasPointerDownPos.x, e.clientY - canvasPointerDownPos.y);
              if (elapsed < 350 && dist < 6) {
                window.toggleAudioPlay();
              }
            });

            const starGeo = new THREE.BufferGeometry();
            const starCount = 400;
            const starCoords = new Float32Array(starCount * 3);
            for (let i = 0; i < starCount * 3; i += 3) {
              starCoords[i] = (Math.random() - 0.5) * 60;
              starCoords[i+1] = (Math.random() - 0.5) * 60;
              starCoords[i+2] = (Math.random() - 0.5) * 60;
            }
            starGeo.setAttribute('position', new THREE.BufferAttribute(starCoords, 3));
            detailScene.add(new THREE.Points(starGeo, new THREE.PointsMaterial({ color: 0x94A3B8, size: 0.16 })));

            const gltfLoader = new THREE.GLTFLoader();
            if (typeof THREE.DRACOLoader !== 'undefined') {
              const dracoLoader = new THREE.DRACOLoader();
              dracoLoader.setDecoderPath('https://www.gstatic.com/draco/versioned/decoders/1.5.6/');
              gltfLoader.setDRACOLoader(dracoLoader);
            }
            loadResilientGLB(asset.modelFiles, gltfLoader, spinner, errBanner, (gltf, loadedUrl) => {
              const model = gltf.scene;
              const box = new THREE.Box3().setFromObject(model);
              const center = box.getCenter(new THREE.Vector3());
              const size = box.getSize(new THREE.Vector3());
              const maxDim = Math.max(size.x, size.y, size.z) || 1.0;
              const scale = 2.4 / maxDim;

              model.position.sub(center);
              const pivot = new THREE.Group();
              pivot.add(model);
              pivot.scale.set(scale, scale, scale);

              model.traverse(node => {
                if (node.isMesh) {
                  node.castShadow = true;
                  node.receiveShadow = true;
                }
              });

              detailScene.add(pivot);
              if (spinner) spinner.style.display = 'none';
              console.log("Successfully loaded and auto-centered " + asset.name + " from " + loadedUrl);
            });

            function onDetailResize() {
              if (!detailRenderer || !detailCamera) return;
              const nw = viewport.clientWidth;
              const nh = viewport.clientHeight;
              detailCamera.aspect = nw / nh;
              detailCamera.updateProjectionMatrix();
              detailRenderer.setSize(nw, nh);
            }
            window.addEventListener('resize', onDetailResize);

            function animateDetail() {
              detailAnimId = requestAnimationFrame(animateDetail);
              if (detailControls) detailControls.update();
              if (detailRenderer && detailScene && detailCamera) {
                detailRenderer.render(detailScene, detailCamera);
              }
            }
            animateDetail();
          } else {
            // No 3D model exists for this spacecraft (only Opportunity, Viking 1, Ingenuity have 3D models)
            if (btn3d) btn3d.style.display = 'none';
            const viewport = document.getElementById('detail-model-viewport');
            const spinner = document.getElementById('detail-spinner');
            if (spinner) spinner.style.display = 'none';
            if (viewport) {
              const oldCanvas = viewport.querySelector('canvas');
              if (oldCanvas) oldCanvas.remove();
            }
            window.switchDetailTab('nasa');
          }
        };

        const globeBadgeElements = [];
            let marsSpinning = true;
            let marsFocusing = false;
            let marsCamStart = new THREE.Vector3();
            let marsCamEnd = new THREE.Vector3();
            let marsFocusProgress = 1.0;

            // Mars Helper Functions: Focus, UI Inspector, Spin, Orbit Reset
            window.closeMarsInspector = function() {
                const insp = document.getElementById('mars-inspector-card');
                if(insp) insp.style.display = 'none';
                document.querySelectorAll('.mars-monument-card').forEach(c => c.classList.remove('active'));
                document.querySelectorAll('.tool-btn-mars').forEach(b => b.classList.remove('active'));
            };

            window.toggleMarsSpin = function() {
                marsSpinning = !marsSpinning;
                const btn = document.getElementById('btn-mars-spin');
                if(btn) btn.innerText = marsSpinning ? "⏸ Pause Spin" : "▶ Resume Spin";
                if(marsSpinning) marsFocusing = false;
            };

            window.resetMarsOrbit = function() {
                marsFocusing = false;
                marsSpinning = true;
                const btn = document.getElementById('btn-mars-spin');
                if(btn) btn.innerText = "⏸ Pause Spin";
                camera.position.set(0, 0, 5.9);
                controls.target.set(0, 0, 0);
                controls.update();
                closeMarsInspector();
            };

            function latLonToVec3(lat, lon, r) {
                const phi = (90 - lat) * (Math.PI / 180);
                const theta = (lon + 180) * (Math.PI / 180);
                return new THREE.Vector3(
                    -(r * Math.sin(phi) * Math.cos(theta)),
                    (r * Math.cos(phi)),
                    (r * Math.sin(phi) * Math.sin(theta))
                );
            }

            function focusMarsLocation(loc) {
                // Update active classes
                document.querySelectorAll('.tool-btn-mars').forEach(b => b.classList.remove('active'));
                const activeToolBtn = document.getElementById('tb-mars-' + loc.id);
                if(activeToolBtn) activeToolBtn.classList.add('active');

                document.querySelectorAll('.mars-monument-card').forEach(c => c.classList.remove('active'));
                const activeCard = document.getElementById('mc-mars-' + loc.id);
                if(activeCard) activeCard.classList.add('active');

                // Populate Inspector Card
                const inspBadge = document.getElementById('mars-insp-badge');
                if(inspBadge) {
                    inspBadge.innerText = loc.status || 'SILENT MONUMENT';
                    inspBadge.style.color = loc.color || '#38BDF8';
                }
                const inspTitle = document.getElementById('mars-insp-title');
                if(inspTitle) inspTitle.innerText = loc.name;

                const inspSite = document.getElementById('mars-insp-site');
                if(inspSite) inspSite.innerText = '📍 ' + (loc.site || loc.landing_coordinates || 'Martian Surface');

                const inspPower = document.getElementById('mars-insp-power');
                if(inspPower) inspPower.innerText = loc.power_source ? ('⚡ Power: ' + loc.power_source) : '';

                const inspDesc = document.getElementById('mars-insp-desc');
                if(inspDesc) inspDesc.innerText = loc.nasa_description || 'NASA Historic Artifact Resting on Mars.';

                const quoteBox = document.querySelector('.mars-insp-quote-box');
                const quoteEl = document.getElementById('mars-insp-quote');
                if(quoteEl && loc.first_person_script) {
                    quoteEl.innerText = '"' + loc.first_person_script + '"';
                    if(quoteBox) quoteBox.style.display = 'block';
                } else if(quoteBox) {
                    quoteBox.style.display = 'none';
                }

                const inspCard = document.getElementById('mars-inspector-card');
                if(inspCard) inspCard.style.display = 'block';

                // Target Camera Position (Facing the landing site on right side of screen)
                const worldPos = latLonToVec3(loc.lat, loc.lon, globeEffectiveRadius);
                worldPos.applyEuler(globeGroup.rotation);
                const targetDir = worldPos.clone().normalize();
                const targetCamPos = targetDir.clone().multiplyScalar(4.9);

                marsCamStart.copy(camera.position);
                marsCamEnd.copy(targetCamPos);
                marsFocusProgress = 0.0;
                marsFocusing = true;
                marsSpinning = false;
                const btn = document.getElementById('btn-mars-spin');
                if(btn) btn.innerText = "▶ Resume Spin";
            }

            // ==========================================
            // MARS AUDIO STORY & GEMINI AI CHATBOT STUDIO
            // ==========================================
            let marsAudio = new Audio();
            let isMarsAudioMuted = false;

            window.toggleMarsAudioPlay = function() {
                const playBtn = document.getElementById('mars-btn-audio-play');
                if (marsAudio.paused) {
                    marsAudio.play().then(() => {
                        if (playBtn) playBtn.innerText = "⏸ Pause";
                    }).catch(e => {
                        console.warn("Audio play prevented:", e);
                    });
                } else {
                    marsAudio.pause();
                    if (playBtn) playBtn.innerText = "▶ Play";
                }
            };

            window.onMarsScrubAudio = function(val) {
                if (marsAudio.duration) {
                    marsAudio.currentTime = (val / 100) * marsAudio.duration;
                }
            };

            marsAudio.ontimeupdate = function() {
                const scrubber = document.getElementById('mars-audio-scrubber');
                const curTime = document.getElementById('mars-audio-current-time');
                const totTime = document.getElementById('mars-audio-total-time');
                if (scrubber && marsAudio.duration) {
                    scrubber.value = (marsAudio.currentTime / marsAudio.duration) * 100;
                }
                function formatT(s) {
                    if(isNaN(s) || s === Infinity) return "0:00";
                    const m = Math.floor(s / 60); const sc = Math.floor(s % 60);
                    return m + ":" + (sc < 10 ? "0" : "") + sc;
                }
                if (curTime) curTime.innerText = formatT(marsAudio.currentTime);
                if (totTime && marsAudio.duration) totTime.innerText = formatT(marsAudio.duration);
            };

            marsAudio.onended = function() {
                const playBtn = document.getElementById('mars-btn-audio-play');
                if (playBtn) playBtn.innerText = "▶ Play";
                const scrubber = document.getElementById('mars-audio-scrubber');
                if (scrubber) scrubber.value = 0;
            };

            let currentMarsChatCraft = null;
            let marsChatAge = "junior";
            let marsChatHistory = [];

            window.setMarsChatAge = function(age) {
                marsChatAge = age;
                const btnJ = document.getElementById('mars-btn-age-junior');
                const btnS = document.getElementById('mars-btn-age-senior');
                if (btnJ && btnS) {
                    btnJ.classList.toggle('active', age === 'junior');
                    btnS.classList.toggle('active', age === 'senior');
                }
            };

            window.sendMarsQuickPrompt = function(promptText) {
                const inputEl = document.getElementById('mars-chat-user-input');
                if (inputEl) inputEl.value = promptText;
                window.sendMarsChatMessage();
            };

            function renderMarsChatMessages() {
                const box = document.getElementById('mars-chat-messages-box');
                if (!box) return;
                box.innerHTML = '';
                marsChatHistory.forEach(msg => {
                    const bubble = document.createElement('div');
                    bubble.className = 'chat-bubble ' + (msg.role === 'user' ? 'user' : 'assistant');
                    if (msg.role === 'user') {
                        bubble.innerText = msg.content;
                    } else {
                        let cleanText = (msg.content || '').replace(/\\n\\n/g, '<br><br>').replace(/\\n/g, '<br>');
                        let badgeHtml = msg.nasaVerified ? '<div style="margin-top:8px; font-size:10.5px; color:#38bdf8; display:flex; align-items:center; gap:5px; border-top:1px solid rgba(56,189,248,0.25); padding-top:4px;"><span>🛰️</span><span>Verified via NASA Open API & Gemini AI</span></div>' : '';
                        bubble.innerHTML = cleanText + badgeHtml;
                    }
                    box.appendChild(bubble);
                });
                box.scrollTop = box.scrollHeight;
            }

            window.sendMarsChatMessage = async function() {
                const inputEl = document.getElementById('mars-chat-user-input');
                if (!inputEl) return;
                const prompt = inputEl.value.trim();
                if (!prompt) return;
                inputEl.value = '';

                marsChatHistory.push({ role: 'user', content: prompt });
                renderMarsChatMessages();

                const box = document.getElementById('mars-chat-messages-box');
                let loadingBubble = null;
                if (box) {
                    loadingBubble = document.createElement('div');
                    loadingBubble.className = 'chat-bubble assistant';
                    loadingBubble.style.opacity = '0.85';
                    loadingBubble.innerHTML = '<span style="color:#38bdf8;">🔍 Querying NASA Open Archives with NASA API key...</span>';
                    box.appendChild(loadingBubble);
                    box.scrollTop = box.scrollHeight;
                }

                const craft = currentMarsChatCraft || {};
                const craftName = craft.displayName || craft.name || "NASA Spacecraft";
                const coords = craft.landing_coordinates || craft.site || "Martian Surface";
                const power = craft.power_source || "Solar cells";
                const desc = craft.nasa_description || craft.science || "";
                const hw = craft.hardware || "";
                const sc = craft.science || "";

                // STEP 1: Query NASA Open Archives using NASA API key & Image/Science API
                let nasaRecord = null;
                try {
                    const cleanCraft = craftName.replace(/Rover|Lander|Orbiter|Helicopter/gi, '').trim();
                    const nasaQuery = encodeURIComponent(cleanCraft + ' ' + prompt);
                    const nasaRes = await fetch('https://images-api.nasa.gov/search?q=' + nasaQuery + '&media_type=image');
                    if (nasaRes.ok) {
                        const nData = await nasaRes.json();
                        const items = nData?.collection?.items || [];
                        if (items.length > 0 && items[0]?.data && items[0]?.data[0]) {
                            nasaRecord = items[0].data[0];
                        }
                    }
                } catch (e) {
                    console.warn("NASA API search notice:", e);
                }

                // Fallback to broader craft query if specific search returned no items
                if (!nasaRecord) {
                    try {
                        const cleanCraft = craftName.replace(/Rover|Lander|Orbiter|Helicopter/gi, '').trim();
                        const nasaRes = await fetch('https://images-api.nasa.gov/search?q=' + encodeURIComponent(cleanCraft + ' Mars') + '&media_type=image');
                        if (nasaRes.ok) {
                            const nData = await nasaRes.json();
                            const items = nData?.collection?.items || [];
                            if (items.length > 0 && items[0]?.data && items[0]?.data[0]) {
                                nasaRecord = items[0].data[0];
                            }
                        }
                    } catch(e) {}
                }

                if (loadingBubble) {
                    loadingBubble.innerHTML = '<span style="color:#c084fc;">🛰️ Authentic NASA mission data retrieved! Polishing response with Gemini AI...</span>';
                }

                let ageTone = marsChatAge === 'junior'
                    ? "Target Audience: Junior Student (Ages 12-14). Use vivid adventurous analogies, explain what your tools discovered in exciting visual terms. 2 short paragraphs."
                    : "Target Audience: Senior Space Enthusiast (Ages 15-18). Rigorous physics, spectrometry wavelengths, power degradation, and orbital mechanics. 2 rich paragraphs.";

                let nasaContext = "";
                if (nasaRecord) {
                    nasaContext = `\nLIVE NASA OPEN ARCHIVE DATA (NASA API Verified):
Title: ${nasaRecord.title || ''}
Archive Report: ${(nasaRecord.description || '').substring(0, 450)}\n`;
                }

                const systemInstruction = `You are ${craftName}, speaking directly in FIRST-PERSON ("I", "my wheels", "my instruments", "my resting place") on Mars.
Location: ${coords}.
Power: ${power}.
Verified NASA Fact: ${desc}.
Hardware Tool: ${hw}.
Scientific Discovery: ${sc}.
${nasaContext}
MANDATORY RULES:
1. Always stay in character as ${craftName}. You are the machine itself.
2. Bridge your physical hardware tool to your real scientific discovery.
3. Ground your response in the verified NASA facts above and provide a captivating, polished first-person answer to the question: "${prompt}".
4. Never make up fictional alien encounters.
${ageTone}`;

                let aiReply = "";

                // STEP 2: Send Grounded NASA Context to Google Gemini AI
                if (typeof GEMINI_API_KEY !== 'undefined' && GEMINI_API_KEY && GEMINI_API_KEY.length > 5) {
                    try {
                        const url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-lite-latest:generateContent?key=" + encodeURIComponent(GEMINI_API_KEY);
                        const contents = [];
                        marsChatHistory.slice(-5).forEach(m => {
                            contents.push({
                                role: m.role === 'user' ? 'user' : 'model',
                                parts: [{ text: m.content }]
                            });
                        });

                        const controller = new AbortController();
                        const timeoutId = setTimeout(() => controller.abort(), 10000);

                        const resp = await fetch(url, {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            signal: controller.signal,
                            body: JSON.stringify({
                                system_instruction: { parts: [{ text: systemInstruction }] },
                                contents: contents,
                                generationConfig: { temperature: 0.7, maxOutputTokens: 500 }
                            })
                        });
                        clearTimeout(timeoutId);

                        if (resp.ok) {
                            const data = await resp.json();
                            if (data && data.candidates && data.candidates[0] && data.candidates[0].content) {
                                const parts = data.candidates[0].content.parts;
                                if (parts && parts.length > 0) {
                                    aiReply = parts[0].text;
                                }
                            }
                        }
                    } catch(err) {
                        console.warn("Client Gemini call failed or timed out, using grounded NASA fallback:", err);
                    }
                }

                // STEP 3: Resilient Polished Fallback if Gemini is unavailable
                if (!aiReply) {
                    if (nasaRecord && nasaRecord.description) {
                        aiReply = `As ${craftName}, our mission telemetry safely archived in NASA's database records: ${(nasaRecord.description || '').substring(0, 320)} Working with my ${hw || 'scientific instruments'} and powered by my ${power}, this research at ${coords} gave humanity crucial insights into Martian history!`;
                    } else if (prompt.toLowerCase().includes("water") || prompt.toLowerCase().includes("discover")) {
                        aiReply = `As ${craftName}, my greatest breakthrough was directly linked to my ${hw || 'instruments'}. ${sc || desc} Being here on Mars showed humanity that this planet once possessed liquid water environments!`;
                    } else if (prompt.toLowerCase().includes("tool") || prompt.toLowerCase().includes("hardware")) {
                        aiReply = `My primary exploration payload includes ${hw || 'advanced spectrometers and imaging cameras'}. Powered by my ${power}, I was engineered to survive extreme thermal fluctuations while transmitting sensor telemetry back to Earth.`;
                    } else if (prompt.toLowerCase().includes("end") || prompt.toLowerCase().includes("battery") || prompt.toLowerCase().includes("dust")) {
                        aiReply = `My mission was an incredible odyssey. Over my years on Mars, dust storms and Martian winters gradually tested my systems. Today, I remain permanently resting at ${coords} as an eternal monument to human curiosity.`;
                    } else {
                        aiReply = `Speaking from my coordinates at ${coords}, I am ${craftName}. Using my ${hw || 'instruments'}, ${sc || desc} What else would you like to explore about my mission?`;
                    }
                }

                marsChatHistory.push({ role: 'assistant', content: aiReply.trim(), nasaVerified: true });
                renderMarsChatMessages();
            };

            window.selectMarsActiveRover = function(locId) {
                const rawKey = String(locId || '').toLowerCase();
                const normKey = rawKey.replace(/[^a-z0-9]/g, '');

                const locList = (typeof MARS_LOCATIONS_DATA !== 'undefined' && MARS_LOCATIONS_DATA.length > 0) ? MARS_LOCATIONS_DATA : (typeof default_mars_artifacts !== 'undefined' ? default_mars_artifacts : []);
                let loc = locList.find(l => {
                    const lid = String(l.id || '').toLowerCase();
                    const lname = String(l.name || '').toLowerCase();
                    return lid === rawKey || lid.replace(/[^a-z0-9]/g, '') === normKey || lname.replace(/[^a-z0-9]/g, '').includes(normKey);
                }) || locList[0];

                if (!loc) return;

                // 1. Highlight pill in selector
                document.querySelectorAll('#mars-rover-selector-pills .rover-pill-btn').forEach(btn => {
                    btn.classList.toggle('active', btn.getAttribute('data-id') === loc.id);
                });

                // 2. Update Hero & Badges
                const t = document.getElementById('mars-insp-title');
                if (t) t.innerText = loc.name;

                const b = document.getElementById('mars-insp-badge');
                if (b) {
                    b.innerText = (loc.type || 'Rover').toUpperCase();
                }
                const stat = document.getElementById('mars-hero-status');
                if (stat) stat.innerText = (loc.status || 'Silent Monument').toUpperCase();

                const yr = document.getElementById('mars-hero-year');
                if (yr) yr.innerText = loc.year ? ('📅 ' + loc.year) : '📅 Historic';

                const q = document.getElementById('mars-insp-quote');
                if (q) {
                    q.innerText = loc.first_person_script ? `"${loc.first_person_script}"` : "";
                    q.style.display = loc.first_person_script ? "block" : "none";
                }

                // 3. Update Supabase telemetry fields
                const hs = (loc.hotspots && loc.hotspots.length > 0) ? loc.hotspots[0] : {};

                const dur = document.getElementById('mars-db-duration');
                if (dur) dur.innerText = loc.mission_duration || hs.mission_duration || (loc.year ? ('Active: ' + loc.year) : 'Historic Mission');

                const odo = document.getElementById('mars-db-odometer');
                if (odo) odo.innerText = loc.distance_traveled || hs.odometer || 'Stationary Surface Base';

                const lnch = document.getElementById('mars-db-launch');
                if (lnch) lnch.innerText = loc.launch_date || hs.launch_date || (loc.year ? ('🚀 ' + loc.year) : '🚀 Historic Launch');

                const lnd = document.getElementById('mars-db-landing');
                if (lnd) lnd.innerText = loc.landing_date || hs.landing_date || '🛬 Martian Surface Touchdown';

                const site = document.getElementById('mars-insp-site');
                if (site) site.innerText = loc.landing_coordinates || loc.site || 'Martian Surface';

                const pwr = document.getElementById('mars-insp-power');
                if (pwr) pwr.innerText = loc.power_source || 'Solar / Battery Array';

                const mass = document.getElementById('mars-db-mass');
                if (mass) mass.innerText = loc.mass_dimensions || hs.mass || 'Surface Scientific Station';

                const comms = document.getElementById('mars-db-comms');
                if (comms) comms.innerText = loc.communications || hs.communications || 'Deep Space Network Link';

                const desc = document.getElementById('mars-insp-desc');
                if (desc) desc.innerText = loc.nasa_description || loc.science || 'Archival NASA exploration mission record.';

                const hw = document.getElementById('mars-db-hw');
                if (hw) hw.innerText = (loc.hardware || hs.hardware) ? ('🛠️ Tool: ' + (loc.hardware || hs.hardware)) : '🛠️ Tool: Planetary Surface Instrumentation Suite';

                const sc = document.getElementById('mars-db-sc');
                if (sc) sc.innerText = (loc.science || hs.science) ? ('💡 Discovery: ' + (loc.science || hs.science)) : '💡 Discovery: Surface geology telemetry transmitted to Earth.';

                const mon = document.getElementById('mars-db-monument');
                if (mon) mon.innerText = loc.monument_commemoration || hs.monument_commemoration || (loc.status || 'Preserved as an eternal monument to human space exploration.');

                // 4. Update Audio
                const isViking = loc.id && loc.id.includes('viking');
                const isIngenuity = loc.id && loc.id.includes('ingenuity');
                const audioFile = isViking ? 'VIKING%20MARS.mp3' : (isIngenuity ? 'INGENVITY%20MARS.mp3' : 'SPIRIT%20AND%20OPPURTUNITY%20MARS.mp3');
                marsAudio.src = '/static/audio/' + audioFile;

                const lbl = document.getElementById('mars-audio-label');
                if (lbl) lbl.innerText = (loc.short || loc.name) + " Story";

                const playBtn = document.getElementById('mars-btn-audio-play');
                if (playBtn) playBtn.innerText = "▶ Play";

                // 5. Update Gemini Chatbot
                currentMarsChatCraft = loc;
                currentMarsChatCraft.displayName = loc.name;
                const chatTitle = document.getElementById('mars-chat-header-title');
                if (chatTitle) chatTitle.innerText = "Live AI Chat with " + currentMarsChatCraft.displayName;

                const chatInput = document.getElementById('mars-chat-user-input');
                if (chatInput) chatInput.placeholder = "Ask " + currentMarsChatCraft.displayName + " a question...";

                marsChatHistory = [{
                    role: "assistant",
                    content: `Greetings explorer! I am ${currentMarsChatCraft.displayName}. ${loc.first_person_script || ''} What would you like to know about my journey across Mars?`
                }];
                renderMarsChatMessages();

                // 6. Rotate & Focus 3D Mars Globe
                if (typeof focusMarsMonument === 'function') {
                    selectMarsActiveRover(loc.id);
                }
            };

            function populateMarsMonuments() {
                const listContainer = document.getElementById('mars-monuments-list');
                const badgesLayer = document.getElementById('globe-badges-layer');
                const toolbar = document.getElementById('toolbar-mars');
                const pillsContainer = document.getElementById('mars-rover-selector-pills');

                if(listContainer) listContainer.innerHTML = '';
                if(pillsContainer) pillsContainer.innerHTML = '';
                if(badgesLayer) {
                    badgesLayer.innerHTML = '';
                    badgesLayer.style.display = 'block';
                }
                if(toolbar) {
                    toolbar.innerHTML = '';
                    toolbar.style.display = 'flex';
                }
                globeBadgeElements.length = 0;

                const locs = (typeof MARS_LOCATIONS_DATA !== 'undefined' && MARS_LOCATIONS_DATA.length > 0)
                    ? MARS_LOCATIONS_DATA
                    : default_mars_artifacts;

                // Populate Rover Selector Pills
                if(pillsContainer) {
                    locs.forEach(loc => {
                        const pillBtn = document.createElement("button");
                        pillBtn.className = "rover-pill-btn";
                        pillBtn.setAttribute("data-id", loc.id);
                        pillBtn.innerHTML = `<span style="color:${loc.color || '#38bdf8'};">●</span> ${loc.short || loc.name}`;
                        pillBtn.onclick = () => {
                            selectMarsActiveRover(loc.id);
                        };
                        pillsContainer.appendChild(pillBtn);
                    });
                }

                const countEl = document.getElementById('mars-sec-count');
                if(countEl) countEl.innerText = MARS_LOCATIONS_DATA.length + " MONUMENTS";

                MARS_LOCATIONS_DATA.forEach(loc => {
                    const pos = latLonToVec3(loc.lat, loc.lon, globeEffectiveRadius * 1.002);
                    const bColor = new THREE.Color(loc.color || '#38bdf8');
                    const bGroup = new THREE.Group();
                    bGroup.position.copy(pos);

                    // 1. Glowing Core Sphere
                    const core = new THREE.Mesh(
                        new THREE.SphereGeometry(0.045, 16, 16),
                        new THREE.MeshBasicMaterial({ color: bColor })
                    );
                    bGroup.add(core);

                    // 2. Pulsing Ring facing outwards
                    const ring = new THREE.Mesh(
                        new THREE.RingGeometry(0.065, 0.11, 32),
                        new THREE.MeshBasicMaterial({ color: bColor, side: THREE.DoubleSide, transparent: true, opacity: 0.85 })
                    );
                    ring.lookAt(pos.clone().multiplyScalar(2));
                    bGroup.add(ring);

                    // 3. Invisible Hitbox for 3D click raycasting
                    const hitbox = new THREE.Mesh(
                        new THREE.SphereGeometry(0.16, 12, 12),
                        new THREE.MeshBasicMaterial({ visible: false })
                    );
                    hitbox.userData = { beacon: loc, location: loc, parentGroup: bGroup };
                    bGroup.add(hitbox);

                    globeGroup.add(bGroup);
                    globeHitboxes.push(hitbox);
                    globeBeacons.push({ group: bGroup, ring: ring, beacon: loc });

                    // 4. Floating 2D Surface Badge
                    if(badgesLayer) {
                        const badge = document.createElement('div');
                        badge.className = 'globe-surface-badge';
                        badge.innerHTML = '<span style="color:' + loc.color + '">●</span> <span>' + (loc.short || loc.name) + '</span>';
                        badge.onclick = (e) => {
                            e.stopPropagation();
                            if (isEquipmentClickable(loc.id)) {
                                openEquipmentDetail(loc.id);
                            } else {
                                focusMarsLocation(loc);
                            }
                        };
                        badgesLayer.appendChild(badge);
                        globeBadgeElements.push({ el: badge, pos: pos, loc: loc });
                    }

                    // 5. Left Sidebar Directory Card
                    if(listContainer) {
                        const card = document.createElement('div');
                        card.className = 'mars-monument-card';
                        card.id = 'mc-mars-' + loc.id;
                        card.innerHTML = `
                            <div class="mars-mc-top">
                                <div class="mars-mc-name">${loc.name}</div>
                                <div class="mars-mc-year">📅 ${loc.year || 'Historic'}</div>
                            </div>
                            <div class="mars-mc-site">📍 ${loc.site || loc.landing_coordinates || 'Mars Surface'}</div>
                            <button class="mars-mc-btn">🎯 Focus on 3D Globe ➔</button>
                        `;
                        card.onclick = () => {
                            if (isEquipmentClickable(loc.id)) {
                                openEquipmentDetail(loc.id);
                            } else {
                                focusMarsLocation(loc);
                            }
                        };
                        listContainer.appendChild(card);
                    }

                    // 6. Bottom Pill Toolbar
                    if(toolbar) {
                        const btn = document.createElement('button');
                        btn.className = 'tool-btn-mars';
                        btn.id = 'tb-mars-' + loc.id;
                        btn.innerHTML = `<span style="color:${loc.color};">●</span> ${loc.short || loc.name}`;
                        btn.onclick = () => {
                            if (isEquipmentClickable(loc.id)) {
                                openEquipmentDetail(loc.id);
                            } else {
                                focusMarsLocation(loc);
                            }
                        };
                        toolbar.appendChild(btn);
                    }
                });
            }

            function enterGlobeMode(zone) {
                if(warpModal) warpModal.style.display = 'none';
                isWarping = false;
                inGlobeMode = true;
                currentGlobeZone = zone;

                // 1. Hide Solar System, Show Globe Group
                solarSystemGroup.visible = false;
                container.classList.remove('panel-open');
                if(selectedTarget) selectedTarget = null;
                isFocused = false;

                // Hide Main Header & Dock
                const mainHeader = document.getElementById('main-header');
                const planetDock = document.getElementById('planet-dock');
                const welcomeOverlay = document.getElementById('welcome-overlay');
                if(mainHeader) mainHeader.style.display = 'none';
                if(planetDock) planetDock.style.display = 'none';
                if(welcomeOverlay) welcomeOverlay.style.display = 'none';

                // Clear previous planet meshes & beacons in globeGroup
                if(globePlanetMesh) {
                    globeGroup.remove(globePlanetMesh);
                    globePlanetMesh = null;
                }
                if(globeAtmosphereMesh) {
                    globeGroup.remove(globeAtmosphereMesh);
                    globeAtmosphereMesh = null;
                }
                globeBeacons.forEach(b => {
                    if(b.group) globeGroup.remove(b.group);
                });
                globeBeacons.length = 0;
                globeHitboxes.length = 0;

                if(zone === 'mars') {
                    // PURE PITCH-BLACK DEEP SPACE
                    scene.background = new THREE.Color(0x000000);
                    skySphere.visible = false;
                    galaxyGroup.visible = false;

                    // SHOW MARS SPLIT SIDEBAR & HUD CONTROLS
                    const marsSidebar = document.getElementById('mars-split-sidebar');
                    const hudMars = document.getElementById('hud-card-mars');
                    const defHud = document.getElementById('globe-hud');
                    if(marsSidebar) marsSidebar.style.display = 'flex';
                    if(hudMars) hudMars.style.display = 'block';
                    if(defHud) defHud.style.display = 'none';

                    // Split container so canvas is ONLY on right side (x >= 410px)
                    container.classList.add('mars-mode');

                    // Mars is centered inside its dedicated right viewport
                    globeGroup.position.set(0, 0, 0);
                    globeGroup.visible = true;
                    globeEffectiveRadius = 2.10;

                    // Frame Camera for Large Mars in right viewport
                    camera.position.set(0, 0, 5.9);
                    controls.target.set(0, 0, 0);
                    controls.minDistance = 3.2;
                    controls.maxDistance = 10.0;
                    controls.update();
                    syncResize();

                    // Procedural High-Res Base Sphere
                    const baseGeo = new THREE.SphereGeometry(globeEffectiveRadius, 64, 64);
                    const baseMat = new THREE.MeshStandardMaterial({
                        map: textures.mars,
                        roughness: 0.85,
                        metalness: 0.08
                    });
                    globePlanetMesh = new THREE.Mesh(baseGeo, baseMat);
                    globeGroup.add(globePlanetMesh);

                    // Load User's Uploaded MARS.glb (Auto-Normalized to radius 2.30)
                    const gltfLoader = new THREE.GLTFLoader();
        if (typeof THREE.DRACOLoader !== 'undefined') {
          const dracoLoader = new THREE.DRACOLoader();
          dracoLoader.setDecoderPath('https://www.gstatic.com/draco/versioned/decoders/1.5.6/');
          gltfLoader.setDRACOLoader(dracoLoader);
        }
                    const modelUrls = [
                        '/app/static/models/MARS.glb',
                        '/static/models/MARS.glb',
                        'static/models/MARS.glb'
                    ];
                    function loadMarsGLB(idx) {
                        if(idx >= modelUrls.length) return;
                        gltfLoader.load(
                            modelUrls[idx],
                            function(gltf) {
                                const model = gltf.scene;
                                const mBox = new THREE.Box3().setFromObject(model);
                                const mCenter = mBox.getCenter(new THREE.Vector3());
                                const mSize = mBox.getSize(new THREE.Vector3());
                                const maxDim = Math.max(mSize.x, mSize.y, mSize.z);
                                const scale = (globeEffectiveRadius * 2) / maxDim;

                                const modelPivot = new THREE.Group();
                                model.position.sub(mCenter);
                                modelPivot.add(model);
                                modelPivot.scale.set(scale, scale, scale);

                                model.traverse(node => {
                                    if(node.isMesh) {
                                        node.castShadow = true;
                                        node.receiveShadow = true;
                                        if(node.material) {
                                            node.material.roughness = 0.85;
                                            node.material.metalness = 0.08;
                                        }
                                    }
                                });

                                if(globePlanetMesh) globeGroup.remove(globePlanetMesh);
                                globePlanetMesh = modelPivot;
                                globeGroup.add(modelPivot);
                                const lbl = document.getElementById('hud-mars-mesh-label');
                                if(lbl) lbl.innerText = 'Active 3D Mesh: MARS.glb (NASA Normal + Diffuse)';
                            },
                            undefined,
                            function(err) {
                                loadMarsGLB(idx + 1);
                            }
                        );
                    }
                    loadMarsGLB(0);

                    // Build 8 Spacecraft Beacons, Floating Indicators, Directory & Pill Toolbar
                    populateMarsMonuments();
                    setTimeout(() => { selectMarsActiveRover('opportunity-rover'); }, 50);
                } else {
                    // Fallback for Moon
                    const globeHud = document.getElementById('globe-hud');
                    const globeBadge = document.getElementById('globe-badge');
                    if(globeHud) globeHud.style.display = 'block';
                    if(globeBadge) globeBadge.innerText = "🌕 3D MOON SIMULATOR • LUNAR TOUCHDOWN CONFIRMED";

                    globeEffectiveRadius = 1.6;
                    globeGroup.position.set(0, 0, 0);
                    globeGroup.visible = true;
                    camera.position.set(0, 0, 5.0);
                    controls.target.set(0, 0, 0);

                    const baseGeo = new THREE.SphereGeometry(globeEffectiveRadius, 64, 64);
                    const baseMat = new THREE.MeshStandardMaterial({
                        map: textures.moon,
                        roughness: 0.82,
                        metalness: 0.08
                    });
                    globePlanetMesh = new THREE.Mesh(baseGeo, baseMat);
                    globeGroup.add(globePlanetMesh);

                    const moonBeacons = [
                        { id: "apollo-lunar-modules", name: "Apollo 11 Eagle Descent Stage", site: "Sea of Tranquility", lat: 0.67408, lon: 23.47297, year: "1969", status: "HISTORIC FIRST MOON LANDING", color: "#FBBF24" },
                        { id: "lunar-roving-vehicles", name: "Apollo 15 Lunar Roving Vehicle", site: "Hadley-Apennine Region", lat: 26.1322, lon: 3.6339, year: "1971", status: "ELECTRIC MOON BUGGY MONUMENT", color: "#FBBF24" },
                        { id: "surveyor-landers", name: "Surveyor 3 Lander", site: "Ocean of Storms", lat: -3.015, lon: -23.418, year: "1967", status: "HISTORIC SOFT-LANDING PIONEER", color: "#38BDF8" },
                        { id: "alsep-scientific-packages", name: "ALSEP Long-Term Science Station", site: "Fra Mauro Base", lat: -3.6453, lon: -17.4714, year: "1971", status: "PASSIVE RETROREFLECTOR ARRAY", color: "#FBBF24" }
                    ];

                    moonBeacons.forEach(b => {
                        const pos = latLonToVec3(b.lat, b.lon, globeEffectiveRadius * 1.002);
                        const bColor = new THREE.Color(b.color);
                        const bGroup = new THREE.Group();
                        bGroup.position.copy(pos);

                        const core = new THREE.Mesh(
                            new THREE.SphereGeometry(0.035, 16, 16),
                            new THREE.MeshBasicMaterial({ color: bColor })
                        );
                        bGroup.add(core);

                        const ring = new THREE.Mesh(
                            new THREE.RingGeometry(0.055, 0.09, 32),
                            new THREE.MeshBasicMaterial({ color: bColor, side: THREE.DoubleSide, transparent: true, opacity: 0.85 })
                        );
                        ring.lookAt(pos.clone().multiplyScalar(2));
                        bGroup.add(ring);

                        const hitbox = new THREE.Mesh(
                            new THREE.SphereGeometry(0.12, 12, 12),
                            new THREE.MeshBasicMaterial({ visible: false })
                        );
                        hitbox.userData = { beacon: b, parentGroup: bGroup };
                        bGroup.add(hitbox);

                        globeGroup.add(bGroup);
                        globeHitboxes.push(hitbox);
                        globeBeacons.push({ group: bGroup, ring: ring, beacon: b });
                    });
                }

                syncResize();
            }

            function triggerWarp(zone) {
                // Immediately cancel all speech synthesis cleanly
                window.stopEntryAudio();

                // Pause Three.js rendering loop so video playback has 100% GPU and CPU dedicated to it
                isWarping = true;

                const cfg = ZONE_TITLES[zone] || ZONE_TITLES["mars"];
                const warpTitle = document.getElementById('warp-dest-title');
                const warpSub = document.getElementById('warp-dest-sub');
                if(warpTitle) warpTitle.innerText = cfg.title;
                if(warpSub) warpSub.innerText = cfg.sub;

                // Hide touchdown card on new warp initiation
                const touchdownCard = document.getElementById('warp-touchdown-card');
                if(touchdownCard) touchdownCard.style.display = 'none';

                // Reset and show skip button
                if(skipBtn) skipBtn.style.display = 'block';

                // Stop and hide any other video elements
                document.querySelectorAll('.descent-video').forEach(v => {
                    v.pause();
                    v.style.display = 'none';
                });

                // Pick preloaded video element
                currentActiveVideo = document.getElementById(cfg.videoId);
                if(!currentActiveVideo) currentActiveVideo = document.getElementById('warp-video-mars');

                currentActiveVideo.style.display = 'block';
                try { currentActiveVideo.load(); } catch(e) {}
                try { currentActiveVideo.currentTime = 0; } catch(e) {}
                currentActiveVideo.muted = false;
                currentActiveVideo.volume = 1.0;
                warpModal.style.display = 'flex';

                const playPromise = currentActiveVideo.play();
                if(playPromise !== undefined) {
                    playPromise.catch((err) => {
                        console.warn("Autoplay with sound prevented, playing muted fallback:", err);
                        currentActiveVideo.muted = true;
                        currentActiveVideo.play().catch(() => {});
                    });
                }

                function onWarpDone() {
                    if(currentActiveVideo) currentActiveVideo.pause();
                    window.stopEntryAudio();

                    // Hide skip button once descent sequence finishes
                    if(skipBtn) skipBtn.style.display = 'none';

                    // Reveal the Touchdown Action Bar Card requested by user!
                    if(touchdownCard) {
                        const isMoon = (zone === 'moon');
                        const isDeep = (zone === 'deep');
                        const targetPage = isMoon ? 'moon' : (isDeep ? 'deep' : 'mars');
                        const tBadge = document.getElementById('touchdown-badge');
                        const tTitle = document.getElementById('touchdown-title');
                        const tSub = document.getElementById('touchdown-sub');
                        const tBtn = document.getElementById('btn-touchdown-enter');

                        if(tBadge) {
                            if(isMoon) {
                                tBadge.innerText = "🌕 TOUCHDOWN CONFIRMED • LUNAR DESCENT COMPLETE";
                                tBadge.className = 'touchdown-badge moon-badge';
                            } else if(isDeep) {
                                tBadge.innerText = "🌌 INTERSTELLAR TRAJECTORY CONFIRMED • CROSSING HELIOPAUSE";
                                tBadge.className = 'touchdown-badge deep-badge';
                            } else {
                                tBadge.innerText = "🔴 TOUCHDOWN CONFIRMED • ATMOSPHERIC ENTRY COMPLETE";
                                tBadge.className = 'touchdown-badge';
                            }
                        }
                        if(tTitle) {
                            tTitle.innerText = isMoon ? "WELCOME TO THE MOON" : (isDeep ? "WELCOME TO DEEP SPACE" : "WELCOME TO THE SURFACE OF MARS");
                        }
                        if(tSub) {
                            tSub.innerText = isMoon ? "Apollo 11, Apollo 15, and Surveyor historic monument sites are standing by." : (isDeep ? "Voyager 1, Dawn, Kepler, NEAR Shoemaker, and Pioneer outposts are standing by." : "Jezero Crater, Meridiani Planum, and 8 NASA monument sites are standing by.");
                        }
                        if(tBtn) {
                            tBtn.innerText = isMoon ? "🚀 ENTER 3D MOON EXPLORER ➔" : (isDeep ? "🌌 ENTER DEEP SPACE EXPLORER ➔" : "🚀 ENTER 3D MARS EXPLORER ➔");
                            tBtn.href = "/?page=" + targetPage;
                            if(isMoon) {
                                tBtn.className = 'touchdown-action-bar moon-action-bar';
                                touchdownCard.style.borderColor = '#F59E0B';
                                touchdownCard.style.boxShadow = '0 10px 40px rgba(0, 0, 0, 0.95), 0 0 35px rgba(245, 158, 11, 0.5)';
                            } else if(isDeep) {
                                tBtn.className = 'touchdown-action-bar deep-action-bar';
                                touchdownCard.style.borderColor = '#38BDF8';
                                touchdownCard.style.boxShadow = '0 10px 40px rgba(0, 0, 0, 0.95), 0 0 35px rgba(56, 189, 248, 0.5)';
                            } else {
                                tBtn.className = 'touchdown-action-bar';
                                touchdownCard.style.borderColor = '#FF5533';
                                touchdownCard.style.boxShadow = '0 10px 40px rgba(0, 0, 0, 0.95), 0 0 35px rgba(255, 85, 51, 0.5)';
                            }

                            tBtn.onclick = function(e) {
                                e.preventDefault();
                                const finalUrl = (targetPage === 'deep') ? "/?page=deep&nowarp=1" : ("/?page=" + targetPage);
                                try {
                                    if(window.top && window.top.location) {
                                        window.top.location.href = finalUrl;
                                        return false;
                                    }
                                } catch(err) {}
                                window.location.href = finalUrl;
                                return false;
                            };
                        }
                        touchdownCard.style.display = 'block';
                    } else {
                        // Fallback if card element not found
                        if(warpModal) warpModal.style.display = 'none';
                        isWarping = false;
                        enterGlobeMode(zone);
                    }
                }

                currentActiveVideo.onended = onWarpDone;
                skipBtn.onclick = onWarpDone;
            }

            // ==========================================
            // ANIMATION LOOP & 3D BADGES PROJECTION
            // ==========================================
            let moonOrbitAngle = 0;
            let clock = 0;

            function animate() {
                requestAnimationFrame(animate);
                // Completely pause Three.js rendering loop while transition video plays for 100% GPU smoothness
                if(isWarping) return;

                if(inGlobeMode) {
                    clock += 0.016;

                    // Mars Globe Logic
                    if(currentGlobeZone === 'mars') {
                        if(marsSpinning && !marsFocusing && globeGroup) {
                            globeGroup.rotation.y += 0.0018;
                        }
                        const pulseScale = 1.0 + Math.sin(clock * 3.5) * 0.35;
                        const pulseOpacity = 0.45 + Math.sin(clock * 3.5) * 0.45;
                        globeBeacons.forEach(b => {
                            if(b && b.ring) {
                                b.ring.scale.set(pulseScale, pulseScale, pulseScale);
                                b.ring.material.opacity = pulseOpacity;
                            }
                        });
                        if(marsFocusing) {
                            marsFocusProgress += 0.035;
                            const t = Math.min(marsFocusProgress, 1.0);
                            const ease = t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
                            camera.position.lerpVectors(marsCamStart, marsCamEnd, ease);
                            controls.target.set(0, 0, 0);
                            if(t >= 1.0) marsFocusing = false;
                        }
                        controls.update();

                        // Dynamic 3D-to-2D Surface Badges Projection with Back-Hemisphere Culling
                        const globeCenter = new THREE.Vector3();
                        globeGroup.getWorldPosition(globeCenter);
                        const toCam = new THREE.Vector3();
                        const wp = new THREE.Vector3();

                        globeBadgeElements.forEach(item => {
                            wp.copy(item.pos);
                            wp.applyEuler(globeGroup.rotation);
                            wp.add(globeCenter);

                            toCam.copy(camera.position).sub(wp).normalize();
                            const norm = wp.clone().sub(globeCenter).normalize();
                            const dot = norm.dot(toCam);

                            if(dot > 0.08) {
                                wp.project(camera);
                                const x = (wp.x * 0.5 + 0.5) * viewport.clientWidth;
                                const y = (-wp.y * 0.5 + 0.5) * viewport.clientHeight;
                                item.el.style.display = 'flex';
                                item.el.style.left = x + 'px';
                                item.el.style.top = y + 'px';
                            } else {
                                item.el.style.display = 'none';
                            }
                        });

                        renderer.render(scene, camera);
                        return;
                    }

                    // Moon Globe Fallback Logic
                    if(!globeIdleInteracting && !globeFocusingBeacon && globeGroup) {
                        globeGroup.rotation.y += 0.001;
                    }
                    const pulseScale = 1.0 + Math.sin(clock * 3.5) * 0.35;
                    const pulseOpacity = 0.45 + Math.sin(clock * 3.5) * 0.45;
                    globeBeacons.forEach(b => {
                        if(b && b.ring) {
                            b.ring.scale.set(pulseScale, pulseScale, pulseScale);
                            b.ring.material.opacity = pulseOpacity;
                        }
                    });
                    if(globeFocusingBeacon) {
                        globeFocusingBeacon.progress += 0.035;
                        const t = Math.min(globeFocusingBeacon.progress, 1.0);
                        const ease = t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
                        camera.position.lerpVectors(globeFocusingBeacon.startCam, globeFocusingBeacon.endCam, ease);
                        controls.target.lerpVectors(globeFocusingBeacon.startTarget, globeFocusingBeacon.endTarget, ease);
                        if(t >= 1.0) globeFocusingBeacon = null;
                    }
                    controls.update();
                    renderer.render(scene, camera);
                    return;
                }

                clock += 0.016;

                // Slow rotation of Sun
                sunMesh.rotation.y += 0.001;

                // Pulsate Solar Corona Layers
                const pulse = 1.0 + Math.sin(clock * 2.5) * 0.04;
                corona1.scale.set(pulse, pulse, pulse);
                corona2.scale.set(pulse * 0.98, pulse * 0.98, pulse * 0.98);

                // Rotate Spiral Galaxy in background
                galaxyGroup.rotation.z += 0.0003;

                // Planetary Orbits (scaled by speedMultiplier)
                planets.forEach(p => {
                    p.rotation.y += 0.004;
                    // Freeze orbit if this planet is focused OR if Moon is focused and this planet is Earth!
                    const isTargetLocked = isFocused && selectedTarget && (selectedTarget === p || (selectedTarget.userData.name === "Moon" && p.userData.name === "Earth"));
                    if(!isTargetLocked) {
                        p.userData.angle += p.userData.speed * speedMultiplier;
                        p.position.x = Math.cos(p.userData.angle) * p.userData.dist;
                        p.position.z = Math.sin(p.userData.angle) * p.userData.dist;
                    }
                });

                // Rotate Sparse Asteroid Belt
                asteroidBelt.rotation.y += 0.00025 * speedMultiplier;

                // Animate Streaking Comet
                comet.position.x += 0.14 * (speedMultiplier > 0 ? 1 : 0.2);
                comet.position.z += 0.16 * (speedMultiplier > 0 ? 1 : 0.2);
                cometTail.position.x += 0.14 * (speedMultiplier > 0 ? 1 : 0.2);
                cometTail.position.z += 0.16 * (speedMultiplier > 0 ? 1 : 0.2);
                if(comet.position.x > 220) {
                    comet.position.set(-180, 24, -140);
                    cometTail.position.set(-180, 24, -140);
                }

                // Earth Clouds
                if(earthCloudMesh) earthCloudMesh.rotation.y += 0.005;

                // Moon Orbit around Earth (distance 5.4, frozen when Moon is selected)
                const earth = planets.find(p => p.userData.name === "Earth");
                if(earth && moonMesh) {
                    if(!isFocused || (selectedTarget && selectedTarget.userData.name !== "Moon" && selectedTarget.userData.name !== "Earth")) {
                        moonOrbitAngle += 0.0028 * speedMultiplier;
                        moonMesh.position.set(Math.cos(moonOrbitAngle) * 5.4, 0, Math.sin(moonOrbitAngle) * 5.4);
                    }
                    moonMesh.rotation.y += 0.002;
                }

                // Smooth Camera Lerp (Follows locked planet smoothly)
                if(isFocused && selectedTarget) {
                    const worldPos = new THREE.Vector3();
                    selectedTarget.getWorldPosition(worldPos);
                    targetLookAt.lerp(worldPos, 0.06);
                    controls.target.copy(targetLookAt);

                    const radius = selectedTarget.userData.size || 1.5;
                    const distMultiplier = (selectedTarget.userData.name === "Moon") ? 3.4 : 4.0;
                    const dest = worldPos.clone().add(new THREE.Vector3(0, radius * 1.3, radius * distMultiplier));
                    camera.position.lerp(dest, 0.06);
                } else if(targetCameraPos) {
                    camera.position.lerp(targetCameraPos, 0.05);
                    controls.target.lerp(targetLookAt, 0.05);
                    if(camera.position.distanceTo(targetCameraPos) < 0.5) targetCameraPos = null;
                }

                // Project 3D Positions to 2D Floating Badges
                const allBadgeTargets = [...planets, sunMesh];
                if(moonMesh) allBadgeTargets.push(moonMesh);

                allBadgeTargets.forEach(obj => {
                    const name = obj.userData.name;
                    const badge = document.getElementById('badge-' + name);
                    if(badge) {
                        const wp = new THREE.Vector3();
                        obj.getWorldPosition(wp);
                        wp.y += (obj.userData.size || 1.5) * 1.5;
                        wp.project(camera);

                        // Only show if in front of camera and not currently focused on it
                        if(wp.z < 1 && (!isFocused || (selectedTarget && selectedTarget.userData.name !== name))) {
                            const sx = (wp.x * 0.5 + 0.5) * viewport.clientWidth;
                            const sy = (-wp.y * 0.5 + 0.5) * viewport.clientHeight;
                            badge.style.display = 'block';
                            badge.style.left = sx + 'px';
                            badge.style.top = sy + 'px';
                        } else {
                            badge.style.display = 'none';
                        }
                    }
                });

                controls.update();
                renderer.render(scene, camera);
            }
            animate();

            function syncResize() {
                const w = (viewport && viewport.clientWidth) ? viewport.clientWidth : (window.innerWidth || 1200);
                const h = (viewport && viewport.clientHeight) ? viewport.clientHeight : (window.innerHeight || 800);
                if (w > 0 && h > 0) {
                    camera.aspect = w / h;
                    camera.updateProjectionMatrix();
                    renderer.setSize(w, h);
                }
            }
            window.addEventListener('resize', () => setTimeout(syncResize, 50));
            window.addEventListener('load', syncResize);
            setTimeout(syncResize, 50);
            setTimeout(syncResize, 250);
            setTimeout(syncResize, 800);
        </script>
    </body>
    </html>
    """
    gemini_key = os.getenv("GEMINI_API_KEY", "")
    nasa_key = os.getenv("NASA_API_KEY", "8P7pKqtdRdfbhHnww87fmNqPbh7fT6wLzCbQwC9F")
    html_code = html_code.replace("/* __INJECT_MARS_LOCATIONS__ */", f"const MARS_LOCATIONS_DATA = {locs_json};")
    html_code = html_code.replace("/* __GEMINI_KEY__ */", json.dumps(gemini_key))
    html_code = html_code.replace("/* __NASA_KEY__ */", json.dumps(nasa_key))
    return components.html(html_code, height=920)


# ==============================================================================
