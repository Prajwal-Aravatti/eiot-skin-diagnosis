# Model Contract

This file is the agreement between the AI training part and the application/backend part.

## Dataset Classes

Use these six SkinDisNet classes in this exact order:

1. Atopic Dermatitis
2. Contact Dermatitis
3. Eczema
4. Scabies
5. Seborrheic Dermatitis
6. Tinea Corporis

## Model Input

- Input image size: `300x300`
- Channels: `3`
- Color format: `RGB`
- Model used in notebook: `EfficientNetV2B3`
- Preprocessing: built into the model using `include_preprocessing=True`
- Backend input: RGB float32 image resized to `300x300`, values kept in `0-255` range

## Model File

The training teammate should provide:

- `best_model.keras` preferred because the notebook's `predict_image()` loads this file
- `labels.json`

Also acceptable:

- `skindisnet_efficientnetv2b3.keras`
- `skindisnet_efficientnetv2b3.tflite` for future mobile/edge deployment

Place it here:

```text
backend/models/best_model.keras
backend/models/labels.json
```

The backend already contains:

```text
backend/models/class_names.json
```

If the real model file is missing, the backend will continue using dummy prediction.

## Backend Prediction Output

The backend prediction function should return this format:

```json
{
  "disease": "Tinea Corporis",
  "confidence": 0.715,
  "top_3_predictions": [
    {"disease": "Tinea Corporis", "confidence": 0.715},
    {"disease": "Eczema", "confidence": 0.092},
    {"disease": "Scabies", "confidence": 0.064}
  ],
  "risk_level": "Moderate",
  "needs_doctor_review": true,
  "doctor_reason": "Doctor or pharmacist confirmation recommended before treatment.",
  "medicine_guidance": {},
  "voice_text": "The detected condition may be Tinea Corporis..."
}
```

## Integration Rule

The backend is already prepared for integration.

When the real trained model is ready:

1. Place `best_model.keras` and `labels.json` inside `backend/models`.
2. Install TensorFlow in the backend virtual environment.
3. Restart FastAPI.
4. Test prediction from the patient app.

The expected integration file is:

```text
backend/app/services/prediction.py
```

## Final Checklist For Training Teammate

Ask the training teammate for:

```text
1. Final trained model file: best_model.keras
2. labels.json
3. Exact class order used during training
4. Input image size used during training
5. Color format: RGB or BGR
6. Preprocessing function used
7. Validation accuracy and loss
8. Confusion matrix or classification report if available
9. Sample test predictions on 3-5 images
10. Dataset split details: train/validation/test percentage
11. Training notebook or Python script
```

Most important:

```text
best_model.keras
labels.json
preprocessing
```

If these three are wrong, the app may run but predictions may be incorrect.
