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

    if not image_path:
        print("❌ No image provided.")
        return

    # ==========================================
    # STEP 1 — FACE
    # ==========================================

    print("\n[1/6] Processing face...")

    try:

        face_result = detect_and_encode(
            image_path,
            "face_crop.jpg"
        )

        print("      ✓ Face detected")
        print("      ✓ ArcFace embedding generated")
        print(
            f"      Embedding dimensions: "
            f"{len(face_result['embedding'])}"
        )

    except Exception as e:

        print("\n❌ Face processing failed:")
        print(e)

        return

    # ==========================================
    # STEP 2 + 3 — GOOGLE LENS
    # ==========================================

    try:

        data = search_google_lens(
            image_path
        )

        results = extract_results(data)

        print(
            f"      ✓ Results returned: "
            f"{len(results)}"
        )

    except Exception as e:

        print("\n❌ Google Lens search failed:")
        print(e)

        return

    # ==========================================
    # RESULTS
    # ==========================================

    print("""
══════════════════════════════════════════════
             GOOGLE LENS RESULTS
══════════════════════════════════════════════
""")

    if not results:

        print("❌ No visual matches found.")

    else:

        for i, result in enumerate(results[:15], 1):

            print(f"[{i}] {result['title']}")
            print(f"    Type   : {result['type']}")
            print(f"    Source : {result['source']}")
            print(f"    URL    : {result['url']}")
            print()

    print(
        "══════════════════════════════════════════════"
    )


if __name__ == "__main__":
    main()