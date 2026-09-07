from deepface import DeepFace
import cv2
import os


def detect_and_encode(image_path, output_path="face_crop.jpg"):
    """
    Detect the largest face, crop it, and generate an ArcFace embedding.
    """

    print("\n[1/3] Detecting face...")

    representations = DeepFace.represent(
        img_path=image_path,
        model_name="ArcFace",
        detector_backend="retinaface",
        enforce_detection=True
    )

    print("      ✓ Face detected")

    embedding = representations[0]["embedding"]

    print(f"      ✓ ArcFace embedding generated")
    print(f"      Embedding dimensions: {len(embedding)}")

    # Detect face coordinates
    faces = DeepFace.extract_faces(
        img_path=image_path,
        detector_backend="retinaface",
        enforce_detection=True,
        align=True
    )

    face = faces[0]["facial_area"]

    x = face["x"]
    y = face["y"]
    w = face["w"]
    h = face["h"]

    image = cv2.imread(image_path)

    # Protect against coordinates outside image
    x = max(0, x)
    y = max(0, y)

    face_crop = image[y:y+h, x:x+w]

    cv2.imwrite(output_path, face_crop)

    print(f"      ✓ Face crop saved: {output_path}")

    return {
        "embedding": embedding,
        "crop_path": output_path,
        "face_area": face
    }