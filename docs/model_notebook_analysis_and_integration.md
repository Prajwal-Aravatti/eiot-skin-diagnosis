# Model Notebook Analysis And Integration Notes

Notebook analyzed:

```text
C:\Users\Hp\Downloads\EIOT(MODEL).ipynb
```

The notebook was readable and contains 22 cells.

## Important Finding

The final model notebook does not use the earlier placeholder MobileNetV2 setup.

It uses:

```text
EfficientNetV2B3
Input size: 300x300
TensorFlow version in Colab: 2.20.0
Class count: 6
Output activation: softmax
Confidence format: decimal value between 0 and 1
```

Example confidence:

```text
0.9936 means 99.36%
```

## Dataset Used

Dataset:

```text
SkinDisNet
```

Detected folders:

```text
Preprocessed
Augmented
```

Classes:

```text
Atopic Dermatitis
Contact Dermatitis
Eczema
Scabies
Seborrheic Dermatitis
Tinea Corporis
```

Original/preprocessed image count:

```text
1710
```

Augmented image count:

```text
11970
```

Total indexed images:

```text
13680
```

## Dataset Split

Original/preprocessed images were split into train, validation, and test.

Then augmented images were added only to training.

Final split:

```text
Training: 13167 images
Validation: 256 images
Test: 257 images
```

## Class Order

The notebook uses this exact order:

```text
0: Atopic Dermatitis
1: Contact Dermatitis
2: Eczema
3: Scabies
4: Seborrheic Dermatitis
5: Tinea Corporis
```

This must match the backend `labels.json`.

## Model Architecture

The notebook builds:

```text
EfficientNetV2B3
include_top=False
weights=imagenet
input_shape=(300, 300, 3)
include_preprocessing=True
```

Custom head:

```text
GlobalAveragePooling2D
BatchNormalization
Dropout(0.35)
Dense(256, relu, L2 regularization)
Dropout(0.30)
Dense(6, softmax)
```

Training also used data augmentation:

```text
RandomFlip
RandomRotation
RandomZoom
RandomTranslation
RandomContrast
```

## Evaluation Result

Test result:

```text
Accuracy: 0.9533
Loss: 0.5589
```

Classification report:

```text
Atopic Dermatitis      F1: 0.9091
Contact Dermatitis     F1: 0.9718
Eczema                 F1: 0.9559
Scabies                F1: 0.9623
Seborrheic Dermatitis  F1: 0.9231
Tinea Corporis         F1: 0.9268
```

Weighted average F1:

```text
0.9537
```

## Files Created By Notebook

From the screenshot and notebook, these files exist:

```text
best_model.keras
labels.json
skindisnet_efficientnetv2b3.keras
skindisnet_efficientnetv2b3.tflite
skindisnet_augmented_image_index.csv
skindisnet_image_index.csv
skindisnet_original_image_index.csv
train_split.csv
val_split.csv
test_split.csv
```

## Which Files Are Needed For Our App

Required for backend prediction:

```text
best_model.keras
labels.json
```

Place them here:

```text
C:\Users\Hp\5 th Sem\EIOT\backend\models\best_model.keras
C:\Users\Hp\5 th Sem\EIOT\backend\models\labels.json
```

Optional:

```text
skindisnet_efficientnetv2b3.keras
```

This appears to be another saved copy of the best Keras model. The backend supports it as a fallback, but use `best_model.keras` first because the notebook prediction function loads `best_model.keras`.

Not needed for current web backend:

```text
skindisnet_efficientnetv2b3.tflite
```

This is useful later only if you want mobile/edge deployment.

Not needed for app runtime, but useful for report/proof:

```text
train_split.csv
val_split.csv
test_split.csv
image index CSV files
```

## Notebook Prediction Format

The notebook prediction function returns:

```json
{
  "predicted_disease": "Contact Dermatitis",
  "confidence": 0.9936029314994812,
  "top_3_predictions": [
    {
      "disease": "Contact Dermatitis",
      "confidence": 0.9936029314994812
    }
  ]
}
```

Our backend now follows this same structure internally.

## Backend Result Format

The notebook then builds:

```json
{
  "disease": "Contact Dermatitis",
  "confidence": 0.9936029314994812,
  "top_3_predictions": [],
  "risk_level": "Low to Moderate",
  "needs_doctor_review": true,
  "doctor_reason": "Doctor approval recommended before final prescription.",
  "medicine_guidance": {},
  "voice_text": "The detected condition may be Contact Dermatitis..."
}
```

Our backend now returns the same style.

## Medicine Guidance Added

The backend now includes medicine guidance for:

```text
Atopic Dermatitis
Contact Dermatitis
Eczema
Scabies
Seborrheic Dermatitis
Tinea Corporis
```

Important safety rule:

```text
Final medicine or prescription should be verified by a doctor.
```

## Backend Changes Made

Updated:

```text
backend/app/services/prediction.py
backend/app/services/recommendations.py
backend/app/database.py
backend/app/schemas.py
backend/app/main.py
frontend/src/main.jsx
frontend/src/styles.css
```

The backend now returns:

```text
disease
confidence
top_3_predictions
risk_level
needs_doctor_review
doctor_reason
medicine_guidance
voice_text
model_status
```

## Current Status

The app now uses the real Keras model locally.

Completed integration checks:

```text
best_model.keras placed in backend/models
labels.json placed in backend/models
TensorFlow 2.20.0 installed in backend/.venv
Direct prediction smoke test returned model_status: real
End-to-end /predict API test returned model_status: real
```

Previous dummy response format for reference:

Current dummy response confirms the new format:

```text
model_status: dummy
confidence: 0.715
medicine_guidance included
top_3_predictions included
voice_text included
```

When `best_model.keras` is added and TensorFlow is installed, the backend should switch to:

```text
model_status: real
```

## Final Instructions For Teammate

Ask him to provide:

```text
1. best_model.keras
2. labels.json
3. EIOT(MODEL).ipynb final notebook
4. test accuracy and classification report screenshot
5. confusion matrix screenshot
6. sample predictions screenshot
```

For app integration, only these two are mandatory:

```text
best_model.keras
labels.json
```
