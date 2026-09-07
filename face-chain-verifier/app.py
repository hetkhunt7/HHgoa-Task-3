from face_encoder import detect_and_encode

from web_search import (
    search_google_lens,
    extract_results,
    find_social_match
)
from evidence import (
    create_evidence,
    calculate_hash,
    save_evidence
)

def main():

    print("""
╔══════════════════════════════════════════════╗
║       FACE → WEB → BLOCKCHAIN                ║
║          Evidence Verification               ║
╚══════════════════════════════════════════════╝
""")

    # ------------------------------------------------
    # STEP 1: INPUT IMAGE
    # ------------------------------------------------

    image_path = input(
        "Enter image path: "
    ).strip()

    if not image_path:

        print("❌ No image provided.")

        return

    # ------------------------------------------------
    # STEP 2: FACE DETECTION + ARCface
    # ------------------------------------------------

    print("\n[1/6] Processing face...")

    try:

        face_result = detect_and_encode(
            image_path,
            "face_crop.jpg"
        )

        print("      ✓ Face detected")

        print(
            "      ✓ ArcFace embedding generated"
        )

        print(
            f"      Embedding dimensions: "
            f"{len(face_result['embedding'])}"
        )

    except Exception as e:

        print("\n❌ Face processing failed:")

        print(e)

        return

    # ------------------------------------------------
    # STEP 3: GOOGLE LENS SEARCH
    # ------------------------------------------------

    try:

        data = search_google_lens(
            image_path
        )

        results = extract_results(
            data
        )

        print(
            f"      ✓ Results returned: "
            f"{len(results)}"
        )

    except Exception as e:

        print("\n❌ Google Lens search failed:")

        print(e)

        return

    # ------------------------------------------------
    # DISPLAY GOOGLE LENS RESULTS
    # ------------------------------------------------

    print("""
══════════════════════════════════════════════
             GOOGLE LENS RESULTS
══════════════════════════════════════════════
""")

    if not results:

        print("❌ No visual matches found.")

    else:

        for i, result in enumerate(
            results[:15],
            1
        ):

            print(
                f"[{i}] "
                f"{result['title']}"
            )

            print(
                f"    Type   : "
                f"{result['type']}"
            )

            print(
                f"    Source : "
                f"{result['source']}"
            )

            print(
                f"    URL    : "
                f"{result['url']}"
            )

            print()

    # ------------------------------------------------
    # STEP 4: FIND SOCIAL MEDIA MATCH
    # ------------------------------------------------

    social_match = find_social_match(
        results
    )

    if not social_match:

        print("""
❌ No social-media match was found.

The Google Lens search worked, but none of
the returned results were from the supported
social-media platforms.
""")

        return

    # ------------------------------------------------
    # FINAL RESULT
    # ------------------------------------------------

    print("""
══════════════════════════════════════════════
              MATCH FOUND
══════════════════════════════════════════════
""")

    print(
        f"Platform : "
        f"{social_match['platform']}"
    )

    print(
        f"Title    : "
        f"{social_match['title']}"
    )

    print(
        f"URL      : "
        f"{social_match['url']}"
    )

    print(
        f"Type     : "
        f"{social_match['type']}"
    )

    # ------------------------------------------------
    # STEP 5: CREATE EVIDENCE + SHA-256 
    # ------------------------------------------------

    print("\n[5/6] Creating evidence fingerprint...")

    try:

        evidence = create_evidence(
            face_result,
            social_match
        )

        save_evidence(
            evidence,
            "evidence.json"
        )

        evidence_hash = calculate_hash(
            evidence
        )

        print("      ✓ Evidence canonicalized")
        print("      ✓ SHA-256 fingerprint generated")

        print(
            f"\n      SHA-256:\n"
            f"      {evidence_hash}"
        )

    except Exception as e:

        print(
            "\n❌ Evidence creation failed:"
        )

        print(e)

        return

    print("""
══════════════════════════════════════════════
          STEP 5 COMPLETED ✓
══════════════════════════════════════════════

Evidence file : evidence.json
SHA-256       : generated

Next:
SHA-256 → Polygon Amoy Blockchain
""")


if __name__ == "__main__":
    main()