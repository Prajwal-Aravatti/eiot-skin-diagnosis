MEDICINE_GUIDANCE = {
    "Atopic Dermatitis": {
        "category": "Moisturizer/emollient and doctor-approved anti-inflammatory cream",
        "examples": [
            "fragrance-free moisturizer",
            "emollient",
            "mild topical corticosteroid if doctor-approved",
        ],
        "instruction": "Use moisturizer regularly and avoid irritants. Steroid or prescription creams should be used only after doctor approval.",
        "doctor_approval_required": True,
    },
    "Contact Dermatitis": {
        "category": "Trigger avoidance and anti-itch support",
        "examples": [
            "calamine lotion",
            "fragrance-free moisturizer",
            "hydrocortisone only if doctor-approved",
        ],
        "instruction": "Avoid the suspected trigger. Seek doctor review if swelling, severe itching, or spreading occurs.",
        "doctor_approval_required": True,
    },
    "Eczema": {
        "category": "Moisturizer/emollient and doctor-approved medicated cream",
        "examples": [
            "emollient",
            "gentle cleanser",
            "topical corticosteroid if doctor-approved",
        ],
        "instruction": "Keep the area moisturized and avoid harsh soaps. Medicated creams should be doctor-approved.",
        "doctor_approval_required": True,
    },
    "Scabies": {
        "category": "Doctor-approved scabicide treatment",
        "examples": [
            "permethrin 5% cream if prescribed",
            "ivermectin if prescribed",
        ],
        "instruction": "Do not self-medicate. Scabies usually needs doctor-confirmed treatment and household contact management.",
        "doctor_approval_required": True,
    },
    "Seborrheic Dermatitis": {
        "category": "Antifungal shampoo or cream",
        "examples": [
            "ketoconazole shampoo",
            "ketoconazole cream",
            "anti-dandruff shampoo",
        ],
        "instruction": "Use only as directed by a doctor, pharmacist, or product label. Consult doctor if recurrent or severe.",
        "doctor_approval_required": True,
    },
    "Tinea Corporis": {
        "category": "Topical antifungal",
        "examples": [
            "clotrimazole",
            "terbinafine",
            "miconazole",
            "ketoconazole",
        ],
        "instruction": "Avoid steroid creams unless prescribed because they can worsen fungal infection. Consult doctor if widespread or not improving.",
        "doctor_approval_required": True,
    },
}


def risk_from_prediction(disease: str, confidence: float) -> tuple[str, bool, str]:
    if confidence < 0.60:
        return "High", True, "Low confidence. Doctor review required."

    if disease in ["Scabies", "Tinea Corporis"]:
        return "Moderate", True, "Doctor or pharmacist confirmation recommended before treatment."

    return "Low to Moderate", True, "Doctor approval recommended before final prescription."


def build_backend_result(prediction: dict) -> dict:
    disease = prediction["predicted_disease"]
    confidence = prediction["confidence"]
    risk_level, needs_doctor_review, doctor_reason = risk_from_prediction(disease, confidence)
    medicine = MEDICINE_GUIDANCE[disease]

    voice_text = (
        f"The detected condition may be {disease}. "
        f"The confidence score is {confidence:.2f}. "
        f"Risk level is {risk_level}. "
        f"Suggested guidance: {medicine['category']}. "
        f"Final medicine or prescription should be approved by a doctor."
    )

    return {
        "disease": disease,
        "confidence": confidence,
        "top_3_predictions": prediction["top_3_predictions"],
        "risk_level": risk_level,
        "needs_doctor_review": needs_doctor_review,
        "doctor_reason": doctor_reason,
        "medicine_guidance": medicine,
        "voice_text": voice_text,
        "model_status": prediction.get("model_status", "unknown"),
    }


def calculate_risk_level(confidence: float, itch: str, pain: str, symptoms: str | None) -> str:
    symptom_text = (symptoms or "").lower()
    has_severe_symptom = any(
        keyword in symptom_text
        for keyword in ["bleeding", "pus", "fever", "spreading", "swelling", "severe"]
    )

    if has_severe_symptom or pain.lower() == "yes":
        return "High"

    if confidence < 60:
        return "Needs Doctor Review"

    if itch.lower() == "yes" or confidence < 85:
        return "Medium"

    return "Low"


def build_recommendation(disease: str, risk_level: str) -> str:
    general_note = "This is a screening result, not a final diagnosis. Please consult a doctor for confirmation."

    disease_guidance = {
        "Atopic Dermatitis": "Avoid scratching, keep the skin moisturized, and avoid known irritants.",
        "Contact Dermatitis": "Wash the affected area gently and avoid suspected allergens or chemicals.",
        "Eczema": "Keep the area moisturized and avoid harsh soaps or irritants.",
        "Scabies": "Avoid close skin contact and consult a doctor because treatment is usually required.",
        "Seborrheic Dermatitis": "Keep the affected area clean and consult a doctor if scaling or redness continues.",
        "Tinea Corporis": "Keep the area clean and dry, and avoid sharing towels or clothing.",
    }

    risk_note = {
        "Low": "The case can be monitored, but doctor validation is still recommended.",
        "Medium": "Doctor review is recommended, especially if symptoms continue.",
        "High": "This case should be reviewed by a doctor as soon as possible.",
        "Needs Doctor Review": "The model confidence is low, so doctor review is required.",
    }

    return f"{disease_guidance.get(disease, 'Please monitor symptoms carefully.')} {risk_note[risk_level]} {general_note}"
