"""
NASA Archival Images API Service
=================================
Connects to NASA's public Images API (images-api.nasa.gov).
Features:
  - Smart keyword filtering to eliminate sterile factory cleanrooms,
    assembly jigs, schematics, and press conferences.
  - Returns authentic planetary surface, flight, and landscape photos.
  - In-memory caching to minimize latency and API calls.
"""

import warnings
from typing import Any, Dict, List, Optional
import httpx

warnings.filterwarnings("ignore", category=UserWarning)

# Negative keywords to filter out factory / sterile cleanroom photos
FORBIDDEN_KEYWORDS = [
    "cleanroom", "clean room", "clean-room", "assembly", "technician",
    "facility", "jig", "sterile", "blueprint", "diagram", "press conference",
    "auditorium", "poster", "logo", "patch", "hardware test", "standing next to",
    "hangar", "high bay", "shipping container", "vibration table"
]

# Simple in-memory cache to avoid repeated queries
_IMAGE_CACHE: Dict[str, List[Dict[str, str]]] = {}


def clean_text(text: Optional[str]) -> str:
    """Trim and clean text fields."""
    if not text:
        return ""
    return " ".join(text.split()).strip()


def is_authentic_space_image(item_data: Dict[str, Any]) -> bool:
    """Check if the image is an authentic space/surface shot rather than a factory floor."""
    title = (item_data.get("title") or "").lower()
    description = (item_data.get("description") or "").lower()
    combined = f"{title} {description}"

    for forbidden in FORBIDDEN_KEYWORDS:
        if forbidden in combined:
            return False
    return True


def fetch_spacecraft_photos(
    spacecraft_name: str,
    zone: str = "mars",
    max_results: int = 6
) -> List[Dict[str, str]]:
    """
    Search NASA Images API for authentic photos of the spacecraft or its landing site.
    
    Parameters:
      spacecraft_name: Name of the spacecraft (e.g. 'Sojourner Rover', 'Viking 1')
      zone: 'moon', 'mars', or 'deep_space'
      max_results: Max number of filtered images to return
    
    Returns:
      List of dicts: [{"title": ..., "description": ..., "image_url": ..., "date": ...}]
    """
    cache_key = f"{spacecraft_name}_{zone}_{max_results}"
    if cache_key in _IMAGE_CACHE:
        return _IMAGE_CACHE[cache_key]

    # Formulate clean search queries
    query_terms = spacecraft_name.replace("Rover", "").replace("Lander", "").strip()
    if zone == "moon":
        search_query = f"{query_terms} moon lunar surface Apollo"
    elif zone == "mars":
        search_query = f"{query_terms} Mars surface landscape rocks"
    else:
        search_query = f"{query_terms} space planet asteroid orbit"

    url = "https://images-api.nasa.gov/search"
    params = {
        "q": search_query,
        "media_type": "image",
        "page_size": 25  # fetch extra so we can filter out cleanrooms
    }

    results: List[Dict[str, str]] = []

    try:
        with httpx.Client(verify=False, timeout=10.0) as client:
            resp = client.get(url, params=params)
            if resp.status_code == 200:
                data = resp.json()
                items = data.get("collection", {}).get("items", [])

                for item in items:
                    data_list = item.get("data", [])
                    links = item.get("links", [])
                    if not data_list or not links:
                        continue

                    meta = data_list[0]
                    # Check cleanroom filter
                    if not is_authentic_space_image(meta):
                        continue

                    # Find preview image URL (typically href in links)
                    image_url = None
                    for link in links:
                        if link.get("rel") == "preview" or link.get("render") == "image":
                            image_url = link.get("href")
                            break
                    if not image_url and links:
                        image_url = links[0].get("href")

                    if image_url:
                        results.append({
                            "title": clean_text(meta.get("title", spacecraft_name)),
                            "description": clean_text(meta.get("description", ""))[:250] + "...",
                            "image_url": image_url,
                            "date": meta.get("date_created", "")[:10],
                            "nasa_id": meta.get("nasa_id", "")
                        })

                    if len(results) >= max_results:
                        break

    except Exception as e:
        print(f"⚠️ [NASA Images API Warning] Could not fetch photos for {spacecraft_name}: {e}")

    # Fallback to general zone query if zero results
    if not results:
        results = [
            {
                "title": f"NASA Archival View — {spacecraft_name}",
                "description": f"Archival imagery recorded during the {spacecraft_name} mission.",
                "image_url": "https://images-assets.nasa.gov/image/PIA00114/PIA00114~thumb.jpg" if zone == "mars" else "https://images-assets.nasa.gov/image/as11-40-5903/as11-40-5903~thumb.jpg",
                "date": "Historical",
                "nasa_id": "ARCHIVE_PREVIEW"
            }
        ]

    _IMAGE_CACHE[cache_key] = results
    return results


if __name__ == "__main__":
    print("Testing NASA Images API Service...")
    sample_rover = "Sojourner Rover"
    photos = fetch_spacecraft_photos(sample_rover, zone="mars", max_results=3)
    print(f"Found {len(photos)} authentic photo(s) for '{sample_rover}':")
    for i, p in enumerate(photos, 1):
        print(f"  [{i}] {p['title']}")
        print(f"      Image URL: {p['image_url']}")
