import os
import requests
from dotenv import load_dotenv

load_dotenv()

SERPAPI_KEY = os.getenv("SERPAPI_KEY")


def search_google_lens(image_url):
    params = {
        "engine": "google_lens",
        "url": image_url,
        "api_key": SERPAPI_KEY
    }

    response = requests.get(
        "https://serpapi.com/search.json",
        params=params,
        timeout=60
    )

    response.raise_for_status()

    return response.json()


def extract_results(data):
    results = []

    # Exact matches
    for result in data.get("exact_matches", []):
        results.append({
            "type": "exact",
            "title": result.get("title"),
            "url": result.get("link"),
            "source": result.get("source")
        })

    # Visual matches
    for result in data.get("visual_matches", []):
        results.append({
            "type": "visual",
            "title": result.get("title"),
            "url": result.get("link"),
            "source": result.get("source")
        })

    return results


if __name__ == "__main__":
    image_url = input("Enter publicly accessible image URL: ")

    print("\nSearching Google Lens...\n")

    data = search_google_lens(image_url)
    results = extract_results(data)

    print(f"Found {len(results)} results\n")

    for i, result in enumerate(results[:10], 1):
        print(f"[{i}] {result['title']}")
        print(f"    Source: {result['source']}")
        print(f"    URL: {result['url']}")
        print()