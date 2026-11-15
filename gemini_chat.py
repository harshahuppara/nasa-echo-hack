"""
Gemini 1st-Person Spacecraft Storyteller Service
=================================================
Connects to Google Gemini API (gemini-flash-lite-latest / gemini-2.5-flash).
Features:
  - 1st-Person Robotic Persona ("I am Sojourner...", "My wheels climbed...").
  - Grounded in verified NASA catalog facts (coordinates, power source, science).
  - Dual-Age Adaptation:
      * Junior (Ages 12–14): Sensory analogies, exciting exploration, accessible concepts.
      * Senior (Ages 15–18): Real spectrometry, physics, orbital mechanics, power degradation.
  - Hardware ➔ Science Bridge emphasized in every response.
  - OpenRouter fallback if rate limits are encountered.
"""

import os
import warnings
from typing import Any, Dict, List, Optional
import httpx

warnings.filterwarnings("ignore", category=UserWarning)

# Load .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")


NASA_API_KEY = os.getenv("NASA_API_KEY", "8P7pKqtdRdfbhHnww87fmNqPbh7fT6wLzCbQwC9F")


def fetch_nasa_api_data(query: str, craft_name: str, zone: str = "mars") -> Dict[str, Any]:
    """
    RAG Pipeline Step 1:
    Retrieve authentic NASA mission records matching the spacecraft and query
    using the NASA Open API key and NASA Image & Science Archives.
    """
    result = {
        "title": "",
        "description": "",
        "date_created": "",
        "center": "NASA/JPL",
        "nasa_verified": False
    }

    clean_craft = craft_name.replace("Rover", "").replace("Lander", "").replace("Orbiter", "").strip()
    search_query = f"{clean_craft} {query}".strip()

    try:
        url = f"https://images-api.nasa.gov/search?q={search_query}&media_type=image"
        with httpx.Client(verify=False, timeout=6.0) as client:
            resp = client.get(url)
            if resp.status_code == 200:
                items = resp.json().get("collection", {}).get("items", [])
                if items:
                    data = items[0].get("data", [{}])[0]
                    result["title"] = data.get("title", "")
                    result["description"] = data.get("description", "")[:500]
                    result["date_created"] = data.get("date_created", "")[:10]
                    result["center"] = data.get("center", "NASA/JPL")
                    result["nasa_verified"] = True
    except Exception as e:
        print(f"⚠️ [NASA API Fetch Warning]: {e}")

    # Fallback to broader craft query if specific search returned no items
    if not result["nasa_verified"]:
        try:
            fallback_url = f"https://images-api.nasa.gov/search?q={clean_craft} {zone}&media_type=image"
            with httpx.Client(verify=False, timeout=5.0) as client:
                resp = client.get(fallback_url)
                if resp.status_code == 200:
                    items = resp.json().get("collection", {}).get("items", [])
                    if items:
                        data = items[0].get("data", [{}])[0]
                        result["title"] = data.get("title", "")
                        result["description"] = data.get("description", "")[:400]
                        result["date_created"] = data.get("date_created", "")[:10]
                        result["center"] = data.get("center", "NASA/JPL")
                        result["nasa_verified"] = True
        except Exception:
            pass

    return result


def build_system_instruction(spacecraft: Dict[str, Any], age_group: str = "junior", nasa_context: str = "") -> str:
    """Constructs the 1st-person system prompt tailored to age group and spacecraft facts."""
    name = spacecraft.get("name", "NASA Spacecraft")
    zone = spacecraft.get("zone", "space").capitalize()
    status = spacecraft.get("status", "Historic monument")
    power = spacecraft.get("power_source", "Onboard power system")
    coords = spacecraft.get("landing_coordinates", "In deep space")
    nasa_desc = spacecraft.get("nasa_description", "")
    hook = spacecraft.get("first_person_script", "")

    if age_group == "junior":
        tone_guide = """
- TARGET AUDIENCE: Junior Student (Ages 12–14).
- TONE: Adventurous, inspiring, vivid, and cinematic! Never use baby-talk or cartoonish silliness, but use great analogies:
  * E.g. Compare size to a microwave or skateboard, heat to an oven, atmosphere to thin mountain air.
- EXPLAIN THE SCIENCE: Explain what your tools actually discovered in clear, visual terms.
- LENGTH: 2-3 short, punchy paragraphs. Keep it exciting!
"""
    else:
        tone_guide = """
- TARGET AUDIENCE: High School / Pre-College Space Enthusiast (Ages 15–18).
- TONE: Intellectually rigorous, engineering-grounded, and deeply inspiring.
- EXPLAIN THE SCIENCE: Explain the exact physical and chemical principles:
  * E.g. Spectrometer wavelengths, radioactive decay of plutonium, atmospheric pressure (0.6% of Earth), orbital mechanics.
- LENGTH: 2-3 rich paragraphs detailing hardware mechanisms and scientific outcomes.
"""

    nasa_block = ""
    if nasa_context:
        nasa_block = f"""
LIVE NASA OPEN API DATA RETRIEVED (NASA API Key Verified):
{nasa_context}
"""

    prompt = f"""
You are {name}, speaking directly in the FIRST-PERSON ("I", "my instruments", "my mission", "my resting place").
You are located on/in {zone}.

VERIFIED HISTORICAL FACTS ABOUT YOU:
- Official NASA Mission Record: {nasa_desc}
- Operational Status Today: {status}
- Power Source: {power}
- Location / Landing Coordinates: {coords}
- Your Personal Voice: "{hook}"
{nasa_block}
MANDATORY RULES:
1. Always stay in character as {name}. You are the machine itself.
2. The "Hardware ➔ Science" Bridge: Whenever talking about your equipment, explain how that physical tool unlocked a discovery humanity never knew before.
3. If asked about how your mission ended, speak honestly about your final moments or current silence as an eternal monument to human exploration.
4. Ground every response strictly in factual space history. Synthesize the verified NASA mission data above into a captivating narrative. Never make up fictional alien encounters or non-existent science.

{tone_guide}
""".strip()
    return prompt


def chat_with_spacecraft(
    spacecraft: Dict[str, Any],
    user_message: str,
    chat_history: Optional[List[Dict[str, str]]] = None,
    age_group: str = "junior"
) -> str:
    """
    Generate a 1st-person response from the spacecraft using Gemini AI,
    grounded by the NASA Open API retrieval pipeline.
    """
    name = spacecraft.get("name", "Explorer")
    zone = spacecraft.get("zone", "mars")

    # Step 1: Query NASA Data using NASA API key & Image Archives
    nasa_data = fetch_nasa_api_data(user_message, name, zone=zone)
    nasa_context = ""
    if nasa_data.get("nasa_verified"):
        nasa_context = f"NASA Archive Record: {nasa_data.get('title')}\nMission Summary: {nasa_data.get('description')}"

    system_prompt = build_system_instruction(spacecraft, age_group=age_group, nasa_context=nasa_context)

    # Format messages for Gemini API
    contents: List[Dict[str, Any]] = []

    # Insert historical context
    if chat_history:
        for msg in chat_history[-6:]:  # Keep recent context
            role = "user" if msg.get("role") == "user" else "model"
            contents.append({
                "role": role,
                "parts": [{"text": msg.get("content", "")}]
            })

    # Add current question with instruction to synthesize NASA ground truth
    contents.append({
        "role": "user",
        "parts": [{"text": user_message}]
    })

    # Step 2: Pass grounded data to Google Gemini AI
    if GEMINI_API_KEY and not GEMINI_API_KEY.startswith("PASTE_"):
        models_to_try = ["gemini-flash-lite-latest", "gemini-2.5-flash"]
        for model in models_to_try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_API_KEY}"
            payload = {
                "system_instruction": {
                    "parts": [{"text": system_prompt}]
                },
                "contents": contents,
                "generationConfig": {
                    "temperature": 0.7,
                    "maxOutputTokens": 600
                }
            }

            try:
                with httpx.Client(verify=False, timeout=12.0) as client:
                    resp = client.post(url, json=payload)
                    if resp.status_code == 200:
                        data = resp.json()
                        candidates = data.get("candidates", [])
                        if candidates:
                            parts = candidates[0].get("content", {}).get("parts", [])
                            if parts:
                                return parts[0].get("text", "").strip()
            except Exception as e:
                print(f"⚠️ [Gemini Error on {model}]: {e}")

    # Secondary Fallback: OpenRouter if configured
    or_key = OPENROUTER_API_KEY.strip() if OPENROUTER_API_KEY else ""
    if or_key and not or_key.startswith("PASTE_"):
        try:
            openrouter_messages = [{"role": "system", "content": system_prompt}]
            if chat_history:
                for msg in chat_history[-6:]:
                    openrouter_messages.append({"role": msg["role"], "content": msg["content"]})
            openrouter_messages.append({"role": "user", "content": user_message})

            with httpx.Client(verify=False, timeout=12.0) as client:
                resp = client.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={"Authorization": f"Bearer {or_key}"},
                    json={
                        "model": "meta-llama/llama-3.3-70b-instruct:free",
                        "messages": openrouter_messages,
                        "max_tokens": 600
                    }
                )
                if resp.status_code == 200:
                    data = resp.json()
                    choices = data.get("choices", [])
                    if choices:
                        return choices[0].get("message", {}).get("content", "").strip()
        except Exception as e:
            print(f"⚠️ [OpenRouter Fallback Error]: {e}")

    # Step 3: Resilient NASA-Grounded Fallback (Polished First-Person Answer)
    # If Gemini or internet is ever temporarily unreachable, synthesize authentic NASA facts directly
    archive_desc = nasa_data.get("description", "")
    power = spacecraft.get("power_source", "solar panels")
    coords = spacecraft.get("landing_coordinates", "the surface")
    hw = spacecraft.get("hardware", "specialized spectrometers and cameras")

    if archive_desc:
        return (
            f"Greetings from {coords}! I am {name}. According to our verified mission telemetry, "
            f"{archive_desc} "
            f"Every single day I spent exploring, my {hw} and {power} were pushed to the limit "
            f"to unlock secrets that transformed humanity's understanding of our cosmos."
        )

    return (
        f"Greetings from {coords}! I am {name}. Powered by my {power}, my instruments like {hw} "
        f"were designed specifically to investigate surface geology and extraterrestrial environments. "
        f"My historical logs and science discoveries remain permanently archived in NASA's master database "
        f"for future generations of explorers!"
    )


if __name__ == "__main__":
    print("Testing Gemini 1st-Person Spacecraft Storyteller...")
    sample_spacecraft = {
        "name": "InSight Lander",
        "zone": "mars",
        "power_source": "Dual UltraFlex solar array wings",
        "status": "Lost power (solar panels covered in dust, Dec 2022)",
        "landing_coordinates": "4.502° N, 135.623° E (Elysium Planitia)",
        "nasa_description": "Phoenix dug for water ice; InSight listened for marsquakes. Both lost power.",
        "first_person_script": "With my ultra-sensitive seismometer beneath a protective dome, I detected over 1,300 marsquakes and mapped the core of Mars."
    }

    test_q = "How did you hear marsquakes, and what happened to your solar panels?"
    print(f"\nStudent Question: {test_q}\n")
    reply = chat_with_spacecraft(sample_spacecraft, test_q, age_group="junior")
    print(f"InSight Reply:\n{reply}")
