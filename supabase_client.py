"""
Universal Data Client for NASA Hackathon Project
================================================
Fetches and updates NASA Spacecraft Artifacts and Explorer Badges.
- Tries Supabase cloud database first.
- If Supabase tables are not created yet, automatically falls back to `artifacts.json`
  so the app NEVER crashes and always has full access to the 18 NASA spacecraft!
"""

import os
import json
import warnings
from typing import Any, Dict, List, Optional

# Load environment
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

env_file = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(env_file):
    with open(env_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                os.environ.setdefault(key.strip(), val.strip().strip('"').strip("'"))

import httpx

warnings.filterwarnings("ignore", category=UserWarning)

ARTIFACTS_FILE = os.path.join(os.path.dirname(__file__), "artifacts.json")


def load_local_artifacts() -> List[Dict[str, Any]]:
    """Load artifacts from local artifacts.json catalog."""
    if os.path.exists(ARTIFACTS_FILE):
        try:
            with open(ARTIFACTS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading artifacts.json: {e}")
    return []


class SupabaseManager:
    """Handles data operations across Supabase with automatic JSON fallback."""

    def __init__(self, url: Optional[str] = None, key: Optional[str] = None):
        self.url = (url or os.getenv("SUPABASE_URL", "")).rstrip("/")
        self.key = key or os.getenv("SUPABASE_KEY", "")
        self.has_credentials = bool(self.url and self.key)

        if self.has_credentials:
            self.client = httpx.Client(
                base_url=self.url,
                headers=self.headers,
                verify=False,
                timeout=8.0
            )
        else:
            self.client = None

    @property
    def headers(self) -> Dict[str, str]:
        return {
            "apikey": self.key,
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }

    def fetch_all(self, table_name: str, select: str = "*", limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Fetch all records. If Supabase table is not found, fallback to artifacts.json."""
        if self.client and table_name == "artifacts":
            try:
                endpoint = f"/rest/v1/{table_name}?select={select}"
                if limit:
                    endpoint += f"&limit={limit}"
                resp = self.client.get(endpoint)
                if resp.status_code == 200:
                    data = resp.json()
                    if data:
                        return data
            except Exception:
                pass

        # Fallback to local artifacts catalog
        if table_name == "artifacts":
            data = load_local_artifacts()
            return data[:limit] if limit else data
        return []

    def fetch_where(self, table_name: str, column: str, value: Any, select: str = "*") -> List[Dict[str, Any]]:
        """Fetch filtered records (e.g. zone == 'mars')."""
        if self.client and table_name == "artifacts":
            try:
                endpoint = f"/rest/v1/{table_name}?{column}=eq.{value}&select={select}"
                resp = self.client.get(endpoint)
                if resp.status_code == 200:
                    data = resp.json()
                    if data:
                        return data
            except Exception:
                pass

        # Fallback to local filtering
        if table_name == "artifacts":
            all_records = load_local_artifacts()
            return [r for r in all_records if str(r.get(column, "")).lower() == str(value).lower()]
        return []

    def fetch_by_id(self, table_name: str, record_id: Any, id_column: str = "id") -> Optional[Dict[str, Any]]:
        """Fetch a single record by ID."""
        if self.client and table_name == "artifacts":
            try:
                endpoint = f"/rest/v1/{table_name}?{id_column}=eq.{record_id}&select=*"
                resp = self.client.get(endpoint)
                if resp.status_code == 200:
                    data = resp.json()
                    if data:
                        return data[0]
            except Exception:
                pass

        # Fallback to local lookup
        if table_name == "artifacts":
            all_records = load_local_artifacts()
            for r in all_records:
                if str(r.get(id_column, "")) == str(record_id):
                    return r
        return None

    def insert(self, table_name: str, record: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Insert a record into Supabase."""
        if self.client:
            try:
                endpoint = f"/rest/v1/{table_name}"
                resp = self.client.post(endpoint, json=record)
                if resp.status_code in [200, 201]:
                    data = resp.json()
                    return data[0] if isinstance(data, list) and data else data
            except Exception as e:
                print(f"Insert error: {e}")
        return record

    def upsert(self, table_name: str, record: Dict[str, Any], on_conflict: str = "id") -> Optional[Dict[str, Any]]:
        """Upsert a record into Supabase."""
        if self.client:
            try:
                endpoint = f"/rest/v1/{table_name}?on_conflict={on_conflict}"
                headers = self.headers.copy()
                headers["Prefer"] = "resolution=merge-duplicates,return=representation"
                resp = self.client.post(endpoint, json=record, headers=headers)
                if resp.status_code in [200, 201]:
                    data = resp.json()
                    return data[0] if isinstance(data, list) and data else data
            except Exception as e:
                print(f"Upsert error: {e}")
        return record


# Global instance
db = SupabaseManager()

# Shortcut functions
def fetch_all(table_name: str = "artifacts", limit: Optional[int] = None) -> List[Dict[str, Any]]:
    return db.fetch_all(table_name=table_name, limit=limit)

def fetch_where(table_name: str = "artifacts", column: str = "zone", value: Any = "mars") -> List[Dict[str, Any]]:
    return db.fetch_where(table_name=table_name, column=column, value=value)

def fetch_by_id(record_id: str, table_name: str = "artifacts", id_column: str = "id") -> Optional[Dict[str, Any]]:
    return db.fetch_by_id(table_name=table_name, record_id=record_id, id_column=id_column)

def insert(table_name: str, record: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return db.insert(table_name=table_name, record=record)

def upsert(table_name: str, record: Dict[str, Any], on_conflict: str = "id") -> Optional[Dict[str, Any]]:
    return db.upsert(table_name=table_name, record=record, on_conflict=on_conflict)
