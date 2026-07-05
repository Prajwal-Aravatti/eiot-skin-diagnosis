# AI Skin Disease Screening Documentation

This project is a medical AI / computer-vision web application for preliminary skin-disease screening from image input.

## What The System Does

- Patients register or log in.
- Patients upload a skin image or capture one using a webcam.
- The backend preprocesses the image and runs a TensorFlow/Keras classifier when a trained model is available.
- The app shows predicted disease, confidence, top-3 predictions, risk level, medicine guidance, and voice-report text.
- Doctors log in separately, inspect submitted cases, and save review notes/status.

## Main Components

```text
frontend/
  React + Vite patient and doctor web interface

backend/
  FastAPI API, authentication, model inference, SQLite storage

backend/models/
  Trained model and label files
```

## Domain

The correct project domain is:

```text
Medical AI / Healthcare Software / Computer Vision / Machine Learning
```

The camera is only an image-input method. The cleaned project focuses on image capture, ML inference, web reporting, and doctor review.

## Model Integration

Preferred model file:

```text
backend/models/best_model.keras
```

Supported fallback names:

```text
backend/models/skindisnet_efficientnetv2b3.keras
backend/models/skin_model.keras
backend/models/skin_model.h5
```

If no trained model is present, the backend returns a demo prediction so the web workflow can still be tested.

## Run Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

## Run Frontend

```powershell
cd frontend
npm install
npm run dev
```

Open:

```text
http://localhost:5173
```

## Core API

```text
POST /auth/register
POST /auth/login
POST /predict
GET  /cases
GET  /my-cases
POST /cases/{case_id}/review
```

## Academic Safety Statement

This app supports preliminary screening and doctor review for project/demo use. It is not a replacement for professional dermatology diagnosis.


