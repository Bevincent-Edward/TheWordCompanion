import requests

def fetch_verse(reference: str) -> str:
    """
    Fetches a verse using bible-api.com (KJV by default).
    Example reference: 'John 3:16'
    """
    try:
        url = f"https://bible-api.com/{reference.replace(' ', '%20')}"
        r = requests.get(url, timeout=10)
        data = r.json()
        if "text" in data and data.get("reference"):
            return f"{data['reference']} — {data['text'].strip()}"
        return f"{reference} — (could not fetch verse text)"
    except Exception:
        return f"{reference} — (network error fetching verse)"
