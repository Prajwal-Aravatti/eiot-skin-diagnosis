# AI Skin Disease Screening

An AI/ML computer-vision web application for preliminary skin-disease screening from a skin image. Patients can upload an image or capture one with a webcam, add basic symptoms, and submit the case to a FastAPI backend. The backend runs a trained TensorFlow/Keras image-classification model when available, stores the case in SQLite, and lets doctors review the prediction with notes.

Its domain is medical AI / healthcare software, focused on image-based machine learning and a web interface for patient and doctor workflows.

## Core Features

- React + Vite patient web interface
- Skin-image upload and browser camera capture
- FastAPI backend with authentication
- TensorFlow/Keras model integration with fallback demo prediction
- Six supported classes: Atopic Dermatitis, Contact Dermatitis, Eczema, Scabies, Seborrheic Dermatitis, and Tinea Corporis
- Top-3 prediction probabilities, confidence score, risk level, and medicine guidance
- Doctor dashboard for case review and notes
- SQLite storage for users, cases, predictions, uploaded images, and doctor review status
- Optional browser voice report for the generated screening summary
- Optional Telegram bot for submitting phone-captured skin images to the same backend

## Project Structure

```text
backend/
  app/
    main.py                 FastAPI routes and application startup
    database.py             SQLite schema and case/user helpers
    schemas.py              Pydantic response/request models
    services/
      prediction.py         Keras model loading, preprocessing, prediction
      recommendations.py    Risk level and guidance generation
      auth.py               Password hashing and token generation
      storage.py            Uploaded image storage
  models/
    README.md               Model placement instructions
    labels.json             Optional label mapping
    class_names.json        Class names used by the model
  requirements.txt

frontend/
  src/
    main.jsx                React application
    styles.css              UI styling
  package.json
```

## Model

Place the trained model in:

```text
backend/models/best_model.keras
```

The backend also checks these fallback names:

```text
backend/models/skindisnet_efficientnetv2b3.keras
backend/models/skin_model.keras
backend/models/skin_model.h5
```

If no model file is found, the backend returns a demo prediction so the web application can still be tested end to end.

## Backend Setup

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend API:

```text
http://127.0.0.1:8000
```

API docs:

```text
http://127.0.0.1:8000/docs
```

## Frontend Setup

Open a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Frontend app:

```text
http://localhost:5173
```

## Build Frontend For FastAPI Serving

```powershell
cd frontend
npm run build
```

Then start the backend and open:

```text
http://127.0.0.1:8000/app
```

## Typical Workflow

1. Create a patient account.
2. Upload a JPG/PNG skin image or capture one using the camera panel.
3. Enter age, gender, affected body location, itching/pain, and symptoms.
4. Submit the case for AI screening.
5. View predicted disease, confidence, top-3 predictions, risk level, guidance, and voice report.
6. Create or log in as a doctor.
7. Review submitted cases and save doctor notes/status.

## Main API Endpoints

```text
POST /auth/register
POST /auth/login
POST /auth/logout
GET  /auth/me
POST /predict
GET  /cases
GET  /my-cases
GET  /cases/{case_id}
POST /telegram/cases/{case_id}/link
POST /cases/{case_id}/review
```

## Optional Telegram Mobile Image Submission

The Telegram bot is a software helper for sending phone-captured skin images to the FastAPI backend. It uses the same patient login and `/predict` route as the website.

Set environment variables:

```powershell
$env:TELEGRAM_BOT_TOKEN="PASTE_BOTFATHER_TOKEN_HERE"
$env:SKIN_DIAGNOSIS_API_URL="http://127.0.0.1:8000"
```

Start the bot:

```powershell
cd backend
python telegram_camera_bot.py
```

Guide:

```text
docs/step9_telegram_mobile_camera_bot_guide.md
```

## Important Note

This application is a doctor-supported screening tool for academic/project use. It should not be treated as a replacement for a dermatologist or professional medical diagnosis.
