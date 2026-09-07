from face_encoder import detect_and_encode
from web_search import search_google_lens, extract_results


def main():

    print("""
╔══════════════════════════════════════════════╗
║       FACE → WEB → BLOCKCHAIN                ║
║          Evidence Verification               ║
╚══════════════════════════════════════════════╝
""")

    image_path = input("Enter image path: ").strip()

    # -------------------------------
    # FACE PROCESSING
    # -------------------------------

    try:
        result = detect_and_encode(image_path)

    except Exception as e:
        print(f"\n❌ Face processing failed: {e}")
        return

    # -------------------------------
    # WEB SEARCH
    # -------------------------------

    print("\n[2/3] Searching the web...")

    # TEMPORARY:
    # Google Lens requires a publicly accessible
    # image URL in our current implementation.
    image_url = input(
        "\nEnter public URL of this image for Lens search: "
    ).strip()

    try:
        data = search_google_lens(image_url)
        results = extract_results(data)

    except Exception as e:
        print(f"\n❌ Web search failed: {e}")
        return

    print(f"\n      ✓ Found {len(results)} results")

    # -------------------------------
    # DISPLAY RESULTS
    # -------------------------------

    print("\n══════════════════════════════════════")
    print("        WEB SEARCH RESULTS")
    print("══════════════════════════════════════")

    for i, result in enumerate(results[:10], 1):

        print(f"\n[{i}] {result['title']}")
        print(f"    Source: {result['source']}")
        print(f"    URL   : {result['url']}")

    print("\n══════════════════════════════════════")


if __name__ == "__main__":
    main()