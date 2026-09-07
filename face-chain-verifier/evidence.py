import json
import hashlib
from datetime import datetime, timezone


def create_evidence(face_result, social_match):
    """
    Create a structured evidence record.
    """

    evidence = {
        "timestamp": datetime.now(timezone.utc).isoformat(),

        "face": {
            "model": "ArcFace",
            "embedding_dimensions": len(
                face_result["embedding"]
            )
        },

        "social_match": {
            "platform": social_match["platform"],
            "title": social_match["title"],
            "url": social_match["url"],
            "source": social_match["source"],
            "match_type": social_match["type"]
        }
    }

    return evidence


def canonicalize_evidence(evidence):
    """
    Convert evidence into deterministic JSON.
    """

    return json.dumps(
        evidence,
        sort_keys=True,
        separators=(",", ":")
    )


def calculate_hash(evidence):
    """
    Generate SHA-256 fingerprint of evidence.
    """

    canonical_json = canonicalize_evidence(
        evidence
    )

    hash_value = hashlib.sha256(
        canonical_json.encode("utf-8")
    ).hexdigest()

    return hash_value


def save_evidence(evidence, filename="evidence.json"):
    """
    Save evidence to a JSON file.
    """

    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            evidence,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(
        f"      ✓ Evidence saved: {filename}"
    )