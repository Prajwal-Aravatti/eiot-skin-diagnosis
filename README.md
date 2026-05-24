# Smart Remote Skin Disease Diagnosis

EIOT project for remote skin disease screening with patient image upload, AI-based prediction, doctor review, and voice report support.

This repository contains the application source code. The trained Keras model file is large, so it is shared separately through Google Drive and must be placed inside the backend model folder before running real predictions.

## Project Overview

This project allows:

- Patients to create an account and log in.
- Patients to upload a skin image with symptom details.
- The backend to preprocess the image and run a TensorFlow/Keras model.
- The app to show predicted disease, confidence, risk level, medicine guidance, and top-3 predictions.
- The browser to read the report aloud using the Web Speech API.
- Doctors to log in, view submitted patient cases, and add review notes.

Important medical note:

```text
This is a screening and decision-support project, not a final medical diagnosis system.
Final diagnosis and medicine/prescription must be approved by a doctor.
```

## Current Features

- FastAPI backend
- React + Vite frontend
- SQLite local database
- Patient login/signup
- Doctor login/signup
- Token-based authentication
- Role-based route protection
- Image upload storage
- Laptop camera capture for patient images
- TensorFlow/Keras model integration
- Dummy prediction fallback if model is missing
- Doctor dashboard
- Doctor case review status and notes
- Browser voice report
- API documentation through Swagger UI

## Tech Stack

### Backend

- Python
- FastAPI
- Uvicorn
- SQLite
- Pydantic
- TensorFlow/Keras
- NumPy
- Pillow
- python-multipart

### Frontend

- React
- Vite
- Lucide React icons
- Browser Web Speech API

## Repository Structure

```text
EIOT/
  README.md
  architecture.png
  EIOT_ppt_project.pptx

  backend/
    requirements.txt
    app/
      main.py
      config.py
      database.py
      schemas.py
      services/
        auth.py
        prediction.py
        recommendations.py
        storage.py
    models/
      README.md
      labels.json
      class_names.json

  frontend/
    package.json
    package-lock.json
    index.html
    src/
      main.jsx
      styles.css

  docs/
    complete_project_explanation_for_exam.md
    model_contract.md
    model_notebook_analysis_and_integration.md
    stop_and_resume_guide.md
    other step-by-step guides
```

The following are intentionally not stored in GitHub:

```text
backend/.venv/
backend/data/*.db
backend/uploads/
backend/models/*.keras
frontend/node_modules/
frontend/dist/
*.log
*.zip
```

## Model File Setup

The trained model file is not included in this GitHub repository because it is large.

Download `best_model.keras` from Google Drive:

```text
PASTE_GOOGLE_DRIVE_MODEL_LINK_HERE
```

After downloading, place it here:

```text
backend/models/best_model.keras
```

Required model-related files:

```text
backend/models/best_model.keras
backend/models/labels.json
backend/models/class_names.json
```

The backend automatically checks for the model file. If it is present and TensorFlow is installed, the app uses the real model and returns:

```text
model_status: real
```

If the model file is missing, the backend uses demo prediction fallback and returns:

```text
model_status: dummy
```

## AI Model Details

Dataset:

```text
SkinDisNet
```

Model:

```text
EfficientNetV2B3
```

Input:

```text
300x300 RGB image
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

The class order in `labels.json` must match the model training order.

## Setup On A New Laptop

Install these first:

- Python 3.11 or 3.12
- Node.js LTS
- Git
- Chrome/Edge or another modern browser

Check installation:

```powershell
python --version
node --version
npm --version
git --version
```

## Clone The Repository

```powershell
git clone https://github.com/Prajwal-Aravatti/eiot-skin-diagnosis.git
cd eiot-skin-diagnosis
```

## Backend Setup

Go to the backend folder:

```powershell
cd backend
```

Create a virtual environment:

```powershell
py -m venv .venv
```

If `py` does not work, use:

```powershell
python -m venv .venv
```

Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Then activate again:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install backend packages:

```powershell
pip install -r requirements.txt
```

Start the backend:

```powershell
uvicorn app.main:app --reload
```

Keep this PowerShell window open while using the app.

Backend health check:

```text
http://127.0.0.1:8000/
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

## Frontend Setup

Open another PowerShell window from the project root:

```powershell
cd frontend
```

Install frontend packages:

```powershell
npm.cmd install
```

Build the frontend:

```powershell
npm.cmd run build
```

The build creates:

```text
frontend/dist/
```

FastAPI serves this built frontend at:

```text
http://127.0.0.1:8000/app
```

## How To Run The App

Start backend first:

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

Then open:

```text
http://127.0.0.1:8000/app
```

Only the backend server is required for normal use because the React frontend is served from `frontend/dist`.

## Patient Flow

1. Open the app.
2. Create or log in to a patient account.
3. Fill patient details.
4. Upload a JPG/PNG skin image or capture one using the laptop camera.
5. Submit the case.
6. View disease prediction, confidence, risk level, medicine guidance, and top-3 predictions.
7. Click `Play Voice Report` to hear the result.

## Doctor Flow

1. Create or log in to a doctor account.
2. Open the Doctor Dashboard.
3. Refresh submitted cases.
4. View patient details, uploaded image, prediction, confidence, and guidance.
5. Add doctor status and notes.
6. Save the review.

## Main API Endpoints

```text
GET  /
GET  /app
POST /auth/register
POST /auth/login
GET  /auth/me
POST /auth/logout
POST /predict
GET  /cases
GET  /my-cases
GET  /cases/{case_id}
POST /cases/{case_id}/review
```

Role protection:

```text
POST /predict              patient only
GET /my-cases              patient only
GET /cases                 doctor only
POST /cases/{id}/review    doctor only
```

## Troubleshooting

### Frontend build not found

Run:

```powershell
cd frontend
npm.cmd install
npm.cmd run build
```

Then refresh:

```text
http://127.0.0.1:8000/app
```

### Prediction shows Demo prediction

Check:

```text
backend/models/best_model.keras exists
backend/models/labels.json exists
TensorFlow installed successfully
Backend restarted after adding model
```

Then submit a new case. Old saved cases may still show old model status.

### Port 8000 already in use

Stop the old backend PowerShell window with:

```text
Ctrl + C
```

Then restart:

```powershell
uvicorn app.main:app --reload
```

### npm command blocked on Windows

Use:

```powershell
npm.cmd install
npm.cmd run build
```

instead of:

```powershell
npm install
npm run build
```

## Documentation

For complete exam/viva explanation, read:

```text
docs/complete_project_explanation_for_exam.md
```

For model integration details, read:

```text
docs/model_contract.md
docs/model_notebook_analysis_and_integration.md
```

For restart instructions, read:

```text
docs/stop_and_resume_guide.md
```

For laptop camera capture details, read:

```text
docs/step8_laptop_camera_capture_guide.md
```

## One-Minute Explanation

This is a remote skin disease screening web application. The frontend is built with React and Vite. The backend is built with FastAPI in Python. Patients can register, log in, upload a skin image, and enter symptoms. The backend saves the image, preprocesses it to 300x300 RGB, and sends it to a TensorFlow/Keras EfficientNetV2B3 model trained on six SkinDisNet classes. The result includes predicted disease, confidence, top-3 predictions, risk level, medicine guidance, and voice report text. The case is stored in SQLite. Doctors can log in separately, view submitted cases, inspect images and AI results, and save review notes. The system is designed as a doctor-supported screening tool, not a replacement for medical diagnosis.
