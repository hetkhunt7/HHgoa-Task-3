import os
import requests
from dotenv import load_dotenv

load_dotenv()

SERPAPI_KEY = os.getenv("SERPAPI_KEY")

IMAGE_UPLOAD_URL = "https://serpapi.com/image"
SEARCH_URL = "https://serpapi.com/search"


# Social-media domains we want to detect
SOCIAL_DOMAINS = [
    "instagram.com",
    "x.com",
    "twitter.com",
    "facebook.com",
    "tiktok.com",
    "youtube.com",
    "reddit.com"
]


def upload_image(image_path):
    """
    Upload a local image to SerpApi Image API.
    Returns an image_id.
    """

    if not SERPAPI_KEY:
        raise ValueError(
            "SERPAPI_KEY is missing from .env"
        )

    if not os.path.exists(image_path):
        raise FileNotFoundError(
            f"Image not found: {image_path}"
        )

    file_size = os.path.getsize(image_path)

    print("\n[2/6] Uploading image to SerpApi...")
    print(f"      File: {os.path.basename(image_path)}")
    print(f"      Size: {file_size / 1024:.1f} KB")

    # SerpApi Image API limit
    if file_size > 500 * 1024:
        raise ValueError(
            "Image is larger than 500 KB. "
            "Please use a smaller image."
        )

    with open(image_path, "rb") as image_file:

        files = {
            "image": (
                os.path.basename(image_path),
                image_file
            )
        }

        data = {
            "api_key": SERPAPI_KEY
        }

        response = requests.post(
            IMAGE_UPLOAD_URL,
            files=files,
            data=data,
            timeout=60
        )

    response.raise_for_status()

    result = response.json()

    if "error" in result:
        raise RuntimeError(result["error"])

    image_id = result.get("image_id")

    if not image_id:
        raise RuntimeError(
            f"No image_id returned: {result}"
        )

    print("      ✓ Image uploaded")
    print(f"      Image ID: {image_id}")

    return image_id


def search_google_lens(image_path):
    """
    Upload local image and search it using Google Lens.
    """

    image_id = upload_image(image_path)

    print("\n[3/6] Searching Google Lens...")

    params = {
        "engine": "google_lens",
        "image_id": image_id,
        "api_key": SERPAPI_KEY,
        "hl": "en",
        "type": "all"
    }

    response = requests.get(
        SEARCH_URL,
        params=params,
        timeout=90
    )

    response.raise_for_status()

    result = response.json()

    if "error" in result:
        raise RuntimeError(result["error"])

    print("      ✓ Google Lens search completed")

    return result


def extract_results(data):
    """
    Extract useful results from Google Lens response.
    """

    results = []

    # Exact matches
    for result in data.get("exact_matches", []):

        results.append({
            "type": "exact",
            "title": result.get("title", ""),
            "url": result.get("link", ""),
            "source": result.get("source", ""),
            "thumbnail": result.get("thumbnail", "")
        })

    # Visual matches
    for result in data.get("visual_matches", []):

        results.append({
            "type": "visual",
            "title": result.get("title", ""),
            "url": result.get("link", ""),
            "source": result.get("source", ""),
            "thumbnail": result.get("thumbnail", "")
        })

    return results


def find_social_match(results):
    """
    Find the first social-media result
    from the Google Lens results.
    """

    print("\n[4/6] Finding social-media match...")

    for result in results:

        url = result.get("url", "").lower()

        if not url:
            continue

        for domain in SOCIAL_DOMAINS:

            if domain in url:

                print("      ✓ Social-media candidate found")
                print(f"      Platform : {domain}")
                print(
                    f"      Title    : "
                    f"{result.get('title', '')}"
                )
                print(
                    f"      URL      : "
                    f"{result.get('url', '')}"
                )

                return {
                    "platform": domain,
                    "title": result.get("title", ""),
                    "url": result.get("url", ""),
                    "source": result.get("source", ""),
                    "type": result.get("type", ""),
                    "thumbnail": result.get("thumbnail", "")
                }

    print("      ❌ No social-media result found")

    return None