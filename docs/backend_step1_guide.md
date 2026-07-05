# Step 1 Guide: Backend Skeleton

This step creates the central server for the AI skin diagnosis project.

The backend will receive patient data, save the uploaded skin image, call the AI prediction function, calculate risk level, save the case, and return the result to the patient app.

For now, the AI model is dummy. Later, only `backend/app/services/prediction.py` needs to be changed when the trained model is ready.

## What To Install

Install these on your laptop:

1. Python 3.11 or Python 3.12
2. VS Code
3. Postman, optional but useful

When installing Python on Windows, enable:

```text
Add python.exe to PATH
```

After installing, check PowerShell:

```powershell
py --version
python --version
```

At least one of them should show a Python version.

## Project Folder

Your project is here:

```text
<project-root>
```

The backend is here:

```text
<project-root>\backend
```

## Backend Setup Commands

Run these in PowerShell:

```powershell
cd "<project-root>\backend"
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

If `py` does not work after Python installation, use:

```powershell
python -m venv .venv
```

## Why We Use Virtual Environment

The `.venv` folder keeps this project's Python packages separate from other projects.

That means FastAPI, Uvicorn, TensorFlow, and other packages can be installed for this project without disturbing your system Python.

## What Each Backend File Does

```text
backend/requirements.txt
```

Lists Python packages needed for the backend.

```text
backend/app/main.py
```

Main FastAPI app. It contains API routes like `/predict`, `/cases`, and doctor review.

```text
backend/app/database.py
```

Creates and manages the SQLite database where patient cases are stored.

```text
backend/app/services/storage.py
```

Saves uploaded skin images into the `uploads` folder.

```text
backend/app/services/prediction.py
```

Currently gives dummy AI prediction. Later this is where the real trained model will be connected.

```text
backend/app/services/recommendations.py
```

Calculates risk level and creates patient-safe recommendation text.

```text
docs/model_contract.md
```

Agreement between your backend work and your teammate's training work.

## Current API Endpoints

```text
GET /
```

Checks whether backend is running.

```text
POST /predict
```

Accepts patient details and skin image, then returns prediction result.

```text
GET /cases
```

Returns all submitted cases for doctor dashboard.

```text
GET /cases/{case_id}
```

Returns one case.

```text
POST /cases/{case_id}/review
```

Allows doctor to update review status and notes.

## How This Helps Later

Your frontend will call:

```text
POST /predict
```

Your doctor dashboard will call:

```text
GET /cases
POST /cases/{case_id}/review
```

When the model is ready, the app structure does not change. You only replace the dummy prediction function with real model prediction.

## Alignment With Training Part

Your teammate should provide:

```text
skin_model.keras
class order
preprocessing details
sample prediction result
```

The backend expects this class order:

```text
Atopic Dermatitis
Contact Dermatitis
Eczema
Scabies
Seborrheic Dermatitis
Tinea Corporis
```

The model should output probabilities for these classes.



