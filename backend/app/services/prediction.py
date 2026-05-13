import json
from pathlib import Path

from app.config import PROJECT_DIR


MODEL_DIR = PROJECT_DIR / "backend" / "models"
MODEL_CANDIDATES = [
    MODEL_DIR / "best_model.keras",
    MODEL_DIR / "skindisnet_efficientnetv2b3.keras",
    MODEL_DIR / "skin_model.keras",
    MODEL_DIR / "skin_model.h5",
]
LABEL_CANDIDATES = [
    MODEL_DIR / "labels.json",
    MODEL_DIR / "class_names.json",
]
CLASS_NAMES_PATH = MODEL_DIR / "class_names.json"
MODEL_INPUT_SIZE = (300, 300)
_MODEL = None


def load_class_names() -> list[str]:
    for label_path in LABEL_CANDIDATES:
        if label_path.exists():
            labels = json.loads(label_path.read_text(encoding="utf-8"))
            if isinstance(labels, dict):
                return [labels[str(index)] for index in range(len(labels))]
            return labels

    return [
        "Atopic Dermatitis",
        "Contact Dermatitis",
        "Eczema",
        "Scabies",
        "Seborrheic Dermatitis",
        "Tinea Corporis",
    ]


CLASS_NAMES = load_class_names()


def get_model():
    global _MODEL

    if _MODEL is not None:
        return _MODEL

    model_file = next((path for path in MODEL_CANDIDATES if path.exists()), None)
    if model_file is None:
        return None

    try:
        from tensorflow.keras.models import load_model
    except ImportError:
        return None

    _MODEL = load_model(model_file)
    return _MODEL


def preprocess_image(image_path: Path):
    import numpy as np
    from PIL import Image

    image = Image.open(image_path).convert("RGB")
    image = image.resize(MODEL_INPUT_SIZE)
    image_array = np.asarray(image, dtype=np.float32)
    return np.expand_dims(image_array, axis=0)


def run_dummy_prediction() -> dict:
    probabilities = {
        "Atopic Dermatitis": 0.041,
        "Contact Dermatitis": 0.058,
        "Eczema": 0.092,
        "Scabies": 0.064,
        "Seborrheic Dermatitis": 0.030,
        "Tinea Corporis": 0.715,
    }

    disease = max(probabilities, key=probabilities.get)
    confidence = probabilities[disease]
    top_3_predictions = [
        {"disease": disease_name, "confidence": confidence_score}
        for disease_name, confidence_score in sorted(
            probabilities.items(),
            key=lambda item: item[1],
            reverse=True,
        )[:3]
    ]

    return {
        "predicted_disease": disease,
        "confidence": confidence,
        "top_3_predictions": top_3_predictions,
        "model_status": "dummy",
    }


def predict_skin_disease(image_path: Path) -> dict:
    """
    Uses the real Keras model if available.
    Falls back to dummy output until the trained model is added.
    """
    model = get_model()
    if model is None:
        return run_dummy_prediction()

    image_batch = preprocess_image(image_path)
    raw_predictions = model.predict(image_batch, verbose=0)[0]
    import numpy as np

    scores = np.asarray(raw_predictions, dtype=np.float32)
    if scores.max() > 1 or scores.sum() > 1.5:
        exp_scores = np.exp(scores - np.max(scores))
        scores = exp_scores / exp_scores.sum()

    probabilities = {
        class_name: float(scores[index])
        for index, class_name in enumerate(CLASS_NAMES)
    }

    disease = max(probabilities, key=probabilities.get)
    confidence = probabilities[disease]
    top_3_predictions = [
        {"disease": disease_name, "confidence": confidence_score}
        for disease_name, confidence_score in sorted(
            probabilities.items(),
            key=lambda item: item[1],
            reverse=True,
        )[:3]
    ]

    return {
        "predicted_disease": disease,
        "confidence": confidence,
        "top_3_predictions": top_3_predictions,
        "model_status": "real",
    }
