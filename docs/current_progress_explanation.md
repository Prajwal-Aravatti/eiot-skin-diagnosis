# Current Progress Explanation

This document explains what has been built so far, what technologies are used, how the files are arranged, and how the current workflow works.

## Is The Current Output Correct?

Yes.

Current update after model integration:

```text
TensorFlow 2.20.0 is installed in backend/.venv
backend/models/best_model.keras is present
backend/models/labels.json is present
/predict has been tested and now returns model_status: real
```

Older notes below describe the previous dummy-prediction phase before TensorFlow and the trained model were connected.

The browser page at:

```text
http://127.0.0.1:8000/app
```

is the patient frontend.

When a patient fills the form, uploads an image, and clicks submit, the frontend sends the data to the backend. The backend returns a dummy prediction for now.

The result shown in the screenshot is expected:

```text
Predicted disease: Tinea Corporis
Confidence: 71.5%
Risk level: High
Doctor status: Pending
```

It is not a real AI prediction yet. It is coming from the temporary dummy prediction function.

## Technologies Used

### 1. Python

Python is used for the backend server.

Backend means the main system that receives patient details, stores images, stores case data, and later calls the AI model.

### 2. FastAPI

FastAPI is the backend framework.

It helps us create API routes like:

```text
POST /predict
GET /cases
GET /cases/{case_id}
POST /cases/{case_id}/review
```

It also automatically creates the testing page:

```text
http://127.0.0.1:8000/docs
```

### 3. Uvicorn

Uvicorn runs the FastAPI server.

Command:

```powershell
uvicorn app.main:app --reload
```

### 4. SQLite

SQLite is the database used right now.

It is a lightweight local database stored as a file.

Current database file:

```text
C:\Users\Hp\5 th Sem\EIOT\backend\data\eiot_cases.db
```

We chose SQLite because:

```text
easy for student project
no separate database server needed
works locally
good for demo
simple to replace later if needed
```

### 5. React

React is used for the frontend patient app.

Frontend means what the patient sees in the browser.

It contains:

```text
input form
image upload
submit button
result display
```

### 6. Vite

Vite is used to build the React frontend.

Build command:

```powershell
npm.cmd run build
```

The built frontend is stored in:

```text
C:\Users\Hp\5 th Sem\EIOT\frontend\dist
```

### 7. Lucide React

Lucide React provides icons used in the frontend UI.

## Main Project File Structure

```text
EIOT/
  architecture.png
  EIOT_ppt_project.pptx
  README.md

  backend/
    requirements.txt
    .env.example
    app/
      __init__.py
      main.py
      config.py
      database.py
      schemas.py
      services/
        __init__.py
        prediction.py
        recommendations.py
        storage.py
    data/
      eiot_cases.db
    uploads/
      uploaded images

  frontend/
    package.json
    index.html
    src/
      main.jsx
      styles.css
    dist/
      index.html
      assets/

  docs/
    model_contract.md
    backend_step1_guide.md
    step2_next_steps_patient_app.md
    step3_patient_frontend_guide.md
    stop_and_resume_guide.md
    current_progress_explanation.md
```

## Backend Files Explained

### `backend/requirements.txt`

Lists Python packages required for backend.

Current packages include:

```text
fastapi
uvicorn
python-multipart
pydantic
```

### `backend/app/main.py`

This is the main backend file.

It defines API routes:

```text
/                  health check
/app               patient frontend page
/predict           submit patient case
/cases             get all cases
/cases/{case_id}   get one case
/cases/{case_id}/review  doctor review update
```

### `backend/app/config.py`

Stores important paths:

```text
database path
uploads folder path
frontend build folder path
```

### `backend/app/database.py`

Handles SQLite database work.

It:

```text
creates cases table
saves a new patient case
lists all cases
gets one case
updates doctor review
```

### `backend/app/schemas.py`

Defines response/request shapes.

This helps FastAPI know what data format to accept and return.

### `backend/app/services/storage.py`

Saves uploaded images into:

```text
backend/uploads
```

### `backend/app/services/prediction.py`

This is the current dummy AI prediction file.

Right now it always returns fixed sample probabilities and selects:

```text
Tinea Corporis
```

Later, when the real model is ready, this file will be changed to:

```text
load model
preprocess image
run model.predict()
return real disease and confidence
```

### `backend/app/services/recommendations.py`

Calculates:

```text
risk level
recommendation text
```

Example:

If symptoms contain words like:

```text
swelling
fever
bleeding
spreading
severe
```

or pain is yes, the risk becomes high.

## Frontend Files Explained

### `frontend/package.json`

Stores frontend project details, dependencies, and scripts.

Important command:

```powershell
npm.cmd run build
```

### `frontend/src/main.jsx`

Main React file.

It contains:

```text
patient form
image preview
submit function
fetch request to backend
result display
```

### `frontend/src/styles.css`

Controls frontend design:

```text
layout
colors
form styling
result card
risk badge
mobile responsiveness
```

### `frontend/dist`

This is the built frontend output.

FastAPI serves this page through:

```text
http://127.0.0.1:8000/app
```

## Current Workflow

Current working flow:

```text
Patient opens http://127.0.0.1:8000/app
        |
Patient fills form and uploads image
        |
React frontend creates FormData
        |
Frontend sends POST request to http://127.0.0.1:8000/predict
        |
FastAPI receives patient details and image
        |
Backend saves uploaded image in backend/uploads
        |
Backend calls dummy prediction.py
        |
Dummy prediction returns Tinea Corporis with 71.5 confidence
        |
Backend checks symptoms and calculates risk level
        |
Backend saves full case in SQLite database
        |
Backend returns result to frontend
        |
Frontend displays disease, confidence, risk, recommendation, and doctor status
```

## Why Risk Became High In The Screenshot

In the screenshot, symptoms include:

```text
swelling
```

Our current rule treats swelling as a severe symptom.

So even though dummy confidence is 71.5%, the backend marks the case:

```text
High
```

This is expected.

## How This Aligns With The AI Training Part

Your teammate is working on:

```text
dataset
preprocessing
training
model export
```

You are working on:

```text
patient app
backend API
database
doctor dashboard
voice report
model integration point
```

The connection point is:

```text
backend/app/services/prediction.py
```

When the real trained model is ready, we replace the dummy prediction code in this file.

The frontend and database do not need major changes.

## Current Limitations

The system is working structurally, but:

```text
prediction is dummy
doctor dashboard UI is not built yet
voice report is not added yet
real model is not connected yet
medicine recommendation is kept as safe guidance
```

## Next Step

The next development step is:

```text
Doctor dashboard
```

It will use:

```text
GET /cases
POST /cases/{case_id}/review
```

It will show submitted patient cases and allow doctor review.
