# Model Notebook And Backend Integration

The training notebook belongs to the ML part of this project. Its purpose is to train or export a skin-disease image classifier that the FastAPI backend can load for inference.

## Expected Model Output

Save the final trained model as:

```text
backend/models/best_model.keras
```

Save labels as either:

```text
backend/models/labels.json
backend/models/class_names.json
```

The backend expects the model labels to match these six classes:

```text
Atopic Dermatitis
Contact Dermatitis
Eczema
Scabies
Seborrheic Dermatitis
Tinea Corporis
```

## Backend Prediction Flow

1. `/predict` receives the patient form and skin image.
2. `backend/app/services/storage.py` saves the uploaded image.
3. `backend/app/services/prediction.py` loads the trained model if present.
4. The image is converted to RGB and resized to `300x300`.
5. The model output is converted into probabilities.
6. The backend returns predicted disease, confidence, top-3 predictions, model status, risk level, recommendation, and doctor-review fields.

## Fallback Behavior

If a real model is not available, the backend returns a demo prediction. This lets the web interface, database, login flow, and doctor dashboard be tested before the trained model file is copied into `backend/models/`.


