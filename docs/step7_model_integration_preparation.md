# Step 7 Guide: Model Integration Preparation

This step prepares the backend for your teammate's trained AI model.

The real model is not required yet. The app still works with dummy prediction until the model file is added.

## What We Added

New folder:

```text
backend/models
```

New files:

```text
backend/models/README.md
backend/models/class_names.json
backend/models/labels.json after teammate download
```

Updated file:

```text
backend/app/services/prediction.py
```

## Current Behavior

Current local status:

```text
best_model.keras is present
labels.json is present
TensorFlow 2.20.0 is installed
The backend returns model_status: real in prediction tests
```

The backend now checks:

```text
Is backend/models/best_model.keras present?
```

If yes:

```text
load real TensorFlow/Keras model
preprocess uploaded image
run model prediction
return disease and confidence
```

If no:

```text
use dummy prediction
keep app working
```

## Expected Final Model File

Ask your teammate to give:

```text
best_model.keras
labels.json
```

Place it here:

```text
C:\Users\Hp\5 th Sem\EIOT\backend\models\best_model.keras
C:\Users\Hp\5 th Sem\EIOT\backend\models\labels.json
```

Accepted backup format:

```text
skindisnet_efficientnetv2b3.keras
skin_model.keras
skin_model.h5
```

## Class Names File

Current class file:

```text
backend/models/class_names.json
```

Current class order:

```text
Atopic Dermatitis
Contact Dermatitis
Eczema
Scabies
Seborrheic Dermatitis
Tinea Corporis
```

This must match the exact class order used during training.

## Backend Prediction Flow After Real Model

```text
Patient uploads image
        |
FastAPI saves image
        |
prediction.py checks for real model
        |
image converted to RGB
        |
image resized to 300x300
        |
EfficientNetV2B3 built-in preprocessing handles scaling
        |
model.predict() runs
        |
highest probability class selected
        |
backend returns disease, confidence, top-3 predictions, medicine guidance, and voice text
```

## New Python Packages

Added to:

```text
backend/requirements.txt
```

Packages:

```text
numpy
pillow
```

TensorFlow is not installed yet because it is large.

Install TensorFlow only when the real model is ready:

```powershell
pip install tensorflow==2.20.0
```

## What To Ask Your Teammate For Finally

Ask him for these:

```text
1. best_model.keras file
2. labels.json
3. exact class order
4. input image size
5. preprocessing method
6. whether images are RGB or BGR
7. validation accuracy
8. test accuracy
9. confusion matrix/classification report
10. training notebook/script
11. 3-5 sample test images with expected predictions
```

Most important three:

```text
best_model.keras
labels.json
preprocessing method
```

## How To Integrate Later

When teammate gives the model:

1. Put file here:

```text
backend/models/best_model.keras
backend/models/labels.json
```

2. Activate backend virtual environment:

```powershell
cd "C:\Users\Hp\5 th Sem\EIOT\backend"
.\.venv\Scripts\Activate.ps1
```

3. Install TensorFlow:

```powershell
pip install tensorflow==2.20.0
```

4. Start backend:

```powershell
uvicorn app.main:app --reload
```

5. Open:

```text
http://127.0.0.1:8000/app
```

6. Submit a test case.

## How To Know Real Model Is Being Used

The prediction function returns:

```text
model_status: real
```

when real model is loaded internally.

The frontend currently does not display this, but it helps backend debugging.

## Why This Step Helps

Now your teammate can work independently.

Your app has a fixed place where the model will go:

```text
backend/models/best_model.keras
```

And the backend already knows how to load it.
