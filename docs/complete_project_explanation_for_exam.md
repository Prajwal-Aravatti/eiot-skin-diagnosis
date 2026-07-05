# Smart Remote Skin Disease Diagnosis - Complete Project Explanation For Exam

This document explains the full AI skin diagnosis project from the beginning to the current working version. It is written for teammates who are seeing the project for the first time, so it explains the purpose, technologies, file structure, code flow, setup process, and likely viva/examiner questions.

Project name:

```text
Smart Remote Skin Disease Diagnosis
```

Main idea:

```text
A patient uploads a skin image and symptom details.
The backend uses a trained AI model to screen the skin condition.
The system stores the case in a local database.
The patient sees the result, confidence, risk level, medicine guidance, and voice report.
A doctor can log in, view cases, and add review notes.
```

Important medical safety point:

```text
This project is a screening and decision-support system, not a final medical diagnosis system.
The final prescription or treatment must be approved by a doctor.
```

## 1. Current Project Status

The current project has these completed parts:

```text
FastAPI backend
SQLite database
Image upload storage
Patient login and signup
Doctor login and signup
Role-based access control
Patient screening form
Doctor dashboard
Doctor review notes
Browser voice report
Real TensorFlow/Keras model integration
React frontend
Frontend served through backend at /app
```

The real model files are currently present:

```text
backend/models/best_model.keras
backend/models/labels.json
backend/models/class_names.json
```

The backend is designed so that:

```text
If real model is available -> use real Keras prediction
If real model is missing -> use dummy prediction fallback
```

The frontend shows the model status as:

```text
Real AI model
Demo prediction
Model status unavailable
```

## 2. Technologies Used

### 2.1 Python

Python is the backend programming language.

Use in this project:

```text
Runs the FastAPI server
Handles API routes
Processes uploaded images
Loads TensorFlow/Keras model
Connects to SQLite database
Creates prediction and recommendation response
```

Why Python:

```text
Python is widely used for machine learning and backend APIs.
TensorFlow, Keras, NumPy, Pillow, and FastAPI work well in Python.
```

### 2.2 FastAPI

FastAPI is a Python web framework used to create APIs.

Definition:

```text
FastAPI helps us create backend routes such as /predict, /cases, /auth/login, and /auth/register.
```

Use in this project:

```text
Receives frontend requests
Accepts image uploads
Validates request and response data
Protects patient and doctor routes
Returns JSON responses
Provides automatic API documentation at /docs
```

Important URL:

```text
http://127.0.0.1:8000/docs
```

This opens Swagger UI, where APIs can be tested directly.

### 2.3 Uvicorn

Uvicorn is the server that runs the FastAPI app.

Definition:

```text
Uvicorn is an ASGI server. It starts the FastAPI application and listens for browser/API requests.
```

Command used:

```powershell
uvicorn app.main:app --reload
```

Meaning:

```text
app.main means backend/app/main.py
app means the FastAPI object created inside main.py
--reload restarts the server automatically when code changes
```

### 2.4 SQLite

SQLite is the local database.

Definition:

```text
SQLite is a lightweight database stored as a single file.
```

Database file:

```text
backend/data/eiot_cases.db
```

Use in this project:

```text
Stores user accounts
Stores login tokens
Stores submitted patient cases
Stores doctor review status and notes
```

Why SQLite:

```text
No separate database server needed
Easy to run on any laptop
Good for academic/demo projects
Simple file-based storage
```

### 2.5 React

React is the frontend UI library.

Definition:

```text
React helps build interactive browser interfaces using components and state.
```

Use in this project:

```text
Login/signup screen
Patient form
Image preview
Result card
Voice report buttons
Doctor dashboard
Case cards
Doctor review form
```

Main React file:

```text
frontend/src/main.jsx
```

### 2.6 Vite

Vite is the frontend build tool.

Definition:

```text
Vite runs and builds modern frontend projects quickly.
```

Use in this project:

```text
Builds React code into static HTML, CSS, and JavaScript files.
```

Build command:

```powershell
npm.cmd run build
```

Build output:

```text
frontend/dist
```

The backend serves this built frontend at:

```text
http://127.0.0.1:8000/app
```

### 2.7 TensorFlow and Keras

TensorFlow is the machine learning framework.

Keras is the high-level model API inside TensorFlow.

Use in this project:

```text
Loads the trained .keras skin disease model
Runs prediction on uploaded image
Returns probability scores for six disease classes
```

Model file:

```text
backend/models/best_model.keras
```

### 2.8 NumPy

NumPy is used for numerical array processing.

Use in this project:

```text
Converts the image into an array
Handles model output scores
Applies softmax if needed
```

### 2.9 Pillow

Pillow is a Python image processing library.

Use in this project:

```text
Opens uploaded image
Converts image to RGB
Resizes image to 300x300
```

### 2.10 Pydantic

Pydantic is used by FastAPI for data validation.

Use in this project:

```text
Defines request body structure
Defines response JSON structure
Validates fields such as password length
Documents API response format
```

Main schema file:

```text
backend/app/schemas.py
```

### 2.11 python-multipart

This package allows FastAPI to receive form data and file uploads.

Use in this project:

```text
Required for POST /predict because patient details and image are sent as multipart/form-data.
```

### 2.12 Lucide React

Lucide React provides icons for the frontend.

Use in this project:

```text
Login icon
Upload icon
Doctor icon
Voice icon
Refresh icon
Result icon
```

### 2.13 Browser Web Speech API

The Web Speech API is built into modern browsers.

Use in this project:

```text
Reads the screening report aloud when the patient clicks Play Voice Report.
```

Code concepts:

```text
window.speechSynthesis
SpeechSynthesisUtterance
```

No extra Python package or internet API is required for the current voice feature.

## 3. Full Project Folder Structure

Main folder:

```text
project-root/
```

Important files and folders:

```text
project-root/
  README.md
  architecture.png
  project_presentation.pptx

  backend/
    requirements.txt
    app/
      __init__.py
      main.py
      config.py
      database.py
      schemas.py
      services/
        __init__.py
        auth.py
        prediction.py
        recommendations.py
        storage.py
    data/
      eiot_cases.db
    models/
      README.md
      best_model.keras
      labels.json
      class_names.json
    uploads/
      uploaded patient images

  frontend/
    package.json
    package-lock.json
    index.html
    src/
      main.jsx
      styles.css
    dist/
      built frontend files
    node_modules/
      installed frontend packages

  docs/
    backend_step1_guide.md
    step2_next_steps_patient_app.md
    step3_patient_frontend_guide.md
    step4_doctor_dashboard_guide.md
    step5_voice_report_guide.md
    step6_login_signup_guide.md
    step7_model_integration_preparation.md
    current_progress_explanation.md
    model_contract.md
    model_notebook_analysis_and_integration.md
    stop_and_resume_guide.md
    complete_project_explanation_for_exam.md

  model_training/
    skin_disease_model.ipynb
```

Generated/vendor folders:

```text
frontend/node_modules
frontend/dist
backend/app/__pycache__
backend/uploads
```

These are not manually written source files. They are generated by package installation, frontend build, Python execution, or runtime image uploads.

## 4. File-By-File Explanation

### 4.1 README.md

Purpose:

```text
Gives quick project overview and setup commands.
```

It explains:

```text
Current status
Backend setup
Frontend build
App URL
Model integration files
Expected prediction output
```

### 4.2 architecture.png

Purpose:

```text
Project architecture image, useful for presentation.
```

Likely shows the flow:

```text
Patient input -> Backend/API -> AI model -> Database -> Doctor dashboard -> Patient report
```

Use in viva:

```text
Explain the system using this architecture diagram from left to right.
```

### 4.3 project_presentation.pptx

Purpose:

```text
Presentation file for the project.
```

Use:

```text
Contains slides for problem statement, architecture, implementation, results, and conclusion.
```

### 4.4 backend/requirements.txt

Purpose:

```text
Lists backend Python packages.
```

Current packages:

```text
fastapi==0.115.6
uvicorn[standard]==0.32.1
python-multipart==0.0.19
pydantic==2.10.3
numpy==2.0.2
pillow==11.0.0
tensorflow==2.20.0
```

Install command:

```powershell
pip install -r requirements.txt
```

### 4.5 backend/app/__init__.py

Purpose:

```text
Marks backend/app as a Python package.
```

Why needed:

```text
It allows imports like from app.config import APP_NAME.
```

### 4.6 backend/app/config.py

Purpose:

```text
Stores central project paths and app name.
```

Important variables:

```text
BASE_DIR
PROJECT_DIR
APP_NAME
DATABASE_PATH
UPLOAD_DIR
FRONTEND_DIST_DIR
FRONTEND_ASSETS_DIR
```

Example:

```text
DATABASE_PATH points to backend/data/eiot_cases.db
UPLOAD_DIR points to backend/uploads
FRONTEND_DIST_DIR points to frontend/dist
```

Why this file is useful:

```text
If paths are needed in many files, keeping them in config.py avoids repeating path logic.
```

### 4.7 backend/app/main.py

Purpose:

```text
Main FastAPI application file.
```

It does these jobs:

```text
Creates FastAPI app
Adds CORS middleware
Initializes database on startup
Serves uploaded images
Serves built React frontend
Defines auth routes
Defines patient prediction route
Defines doctor case routes
Protects routes by role
```

Main object:

```python
app = FastAPI(title=APP_NAME)
```

Important route list:

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

Important helper functions:

```text
_extract_token()
get_current_user()
require_patient()
require_doctor()
```

These functions check:

```text
Is the user logged in?
Is the token valid?
Is the user a patient or doctor?
```

### 4.8 backend/app/schemas.py

Purpose:

```text
Defines request and response data models using Pydantic.
```

Important classes:

```text
UserCreate
UserLogin
UserResponse
AuthResponse
PredictionResult
TopPrediction
MedicineGuidance
CaseResponse
ReviewRequest
```

Why schemas are used:

```text
They make API input/output clear.
They help FastAPI validate data.
They generate clean API docs.
They prevent random unknown response formats.
```

Example:

```text
ReviewRequest requires doctor_status and optional doctor_notes.
```

### 4.9 backend/app/database.py

Purpose:

```text
Handles all SQLite database work.
```

It creates three tables:

```text
users
auth_tokens
cases
```

users table stores:

```text
id
full_name
email
password_hash
role
created_at
```

auth_tokens table stores:

```text
token
user_id
created_at
```

cases table stores:

```text
id
user_id
patient_name
age
gender
body_location
itch
pain
symptoms
image_path
predicted_disease
confidence
risk_level
recommendation
top_3_predictions
needs_doctor_review
doctor_reason
medicine_guidance
voice_text
model_status
doctor_status
doctor_notes
created_at
```

Important functions:

```text
get_connection()
init_db()
create_user()
get_user_by_email()
get_user_by_id()
create_token()
get_user_by_token()
delete_token()
create_case()
list_cases()
list_cases_for_user()
get_case()
update_case_review()
```

Important implementation detail:

```text
top_3_predictions and medicine_guidance are Python objects, but SQLite stores text.
So database.py converts them to JSON strings while saving and converts them back while reading.
```

### 4.10 backend/app/services/auth.py

Purpose:

```text
Handles password hashing, password verification, and token creation.
```

Important functions:

```text
hash_password(password)
verify_password(password, stored_hash)
create_auth_token()
```

Password security:

```text
The raw password is never stored.
The password is converted into a hash using PBKDF2-HMAC-SHA256.
A random salt is generated for each password.
hmac.compare_digest is used for safe comparison.
```

Token:

```text
secrets.token_urlsafe(32) creates a random login token.
```

Viva answer:

```text
We used token-based authentication. After login, backend returns a token. Frontend stores it in localStorage and sends it in the Authorization header as Bearer token.
```

### 4.11 backend/app/services/storage.py

Purpose:

```text
Saves uploaded patient images.
```

Important function:

```text
save_upload_file(file)
```

What it does:

```text
Creates uploads folder if missing
Checks file extension
Allows jpg, jpeg, png
Generates unique filename using uuid4
Writes file bytes to backend/uploads
Returns saved file path
```

Why uuid is used:

```text
If two patients upload image.jpg, filenames would clash.
UUID creates a unique name for every uploaded file.
```

### 4.12 backend/app/services/prediction.py

Purpose:

```text
Loads the trained model and predicts the skin disease.
```

Important constants:

```text
MODEL_DIR
MODEL_CANDIDATES
LABEL_CANDIDATES
MODEL_INPUT_SIZE = (300, 300)
CLASS_NAMES
```

Supported model filenames:

```text
best_model.keras
skindisnet_efficientnetv2b3.keras
skin_model.keras
skin_model.h5
```

Supported label filenames:

```text
labels.json
class_names.json
```

Important functions:

```text
load_class_names()
get_model()
preprocess_image()
run_dummy_prediction()
predict_skin_disease()
```

Image preprocessing:

```text
Open image using Pillow
Convert to RGB
Resize to 300x300
Convert to float32 NumPy array
Add batch dimension
```

Batch dimension explanation:

```text
The model expects input shape like (batch_size, height, width, channels).
One image becomes shape (1, 300, 300, 3).
```

Prediction flow:

```text
Check if model already loaded
If not loaded, find model file
Load model with tensorflow.keras.models.load_model
Preprocess uploaded image
Run model.predict()
Convert scores into probabilities if required
Map probability indexes to class names
Select highest probability disease
Build top 3 predictions
Return disease, confidence, top_3_predictions, and model_status
```

Dummy fallback:

```text
If TensorFlow is not installed or model file is missing, app still works using dummy prediction.
```

Dummy prediction returns:

```text
Tinea Corporis with confidence 0.715
model_status: dummy
```

### 4.13 backend/app/services/recommendations.py

Purpose:

```text
Converts raw model prediction into safe user-facing guidance.
```

It contains:

```text
MEDICINE_GUIDANCE
risk_from_prediction()
build_backend_result()
calculate_risk_level()
build_recommendation()
```

Current active path:

```text
main.py calls build_backend_result(prediction)
```

Medicine guidance is available for:

```text
Atopic Dermatitis
Contact Dermatitis
Eczema
Scabies
Seborrheic Dermatitis
Tinea Corporis
```

Safety rule:

```text
doctor_approval_required is true for all classes.
```

Risk logic:

```text
If confidence < 0.60 -> High risk because model is uncertain.
If disease is Scabies or Tinea Corporis -> Moderate risk and doctor/pharmacist confirmation recommended.
Otherwise -> Low to Moderate and doctor approval recommended.
```

Voice text:

```text
The backend builds a readable sentence that the frontend can speak aloud.
```

### 4.14 backend/models/README.md

Purpose:

```text
Explains what model files should be placed in backend/models.
```

Important expected files:

```text
best_model.keras
labels.json
```

### 4.15 backend/models/best_model.keras

Purpose:

```text
Trained Keras model file.
```

Current size is about:

```text
123 MB
```

It is loaded by:

```text
backend/app/services/prediction.py
```

### 4.16 backend/models/labels.json

Purpose:

```text
Maps model output indexes to disease class names.
```

Current mapping:

```json
{
  "0": "Atopic Dermatitis",
  "1": "Contact Dermatitis",
  "2": "Eczema",
  "3": "Scabies",
  "4": "Seborrheic Dermatitis",
  "5": "Tinea Corporis"
}
```

Important:

```text
This order must match the exact order used during model training.
If order is wrong, model may predict one class but app may display another class.
```

### 4.17 backend/models/class_names.json

Purpose:

```text
Backup class names list.
```

Current list:

```json
[
  "Atopic Dermatitis",
  "Contact Dermatitis",
  "Eczema",
  "Scabies",
  "Seborrheic Dermatitis",
  "Tinea Corporis"
]
```

### 4.18 backend/data/eiot_cases.db

Purpose:

```text
SQLite database file.
```

It is automatically created/updated when backend starts.

Do not manually edit it unless you know SQLite.

### 4.19 backend/uploads/

Purpose:

```text
Stores uploaded skin images.
```

Files here have random UUID names like:

```text
d77726678f2345ff8b1b5974dca4e034.jpg
```

The database stores image path like:

```text
/uploads/d77726678f2345ff8b1b5974dca4e034.jpg
```

The doctor dashboard uses this path to display the image.

### 4.20 frontend/package.json

Purpose:

```text
Defines frontend project name, scripts, and dependencies.
```

Important scripts:

```json
{
  "dev": "vite",
  "build": "vite build --base=/app/",
  "preview": "vite preview"
}
```

Important dependency list:

```text
React
React DOM
Vite
@vitejs/plugin-react
lucide-react
```

Why build uses `--base=/app/`:

```text
The frontend is served under http://127.0.0.1:8000/app.
So built asset paths must work from /app/.
```

### 4.21 frontend/package-lock.json

Purpose:

```text
Locks exact installed frontend package versions.
```

Why useful:

```text
Other teammates get the same dependency versions when they run npm.cmd install.
```

### 4.22 frontend/index.html

Purpose:

```text
Base HTML page for the React app.
```

Important line:

```html
<div id="root"></div>
```

React attaches the whole application into this root div.

### 4.23 frontend/src/main.jsx

Purpose:

```text
Main frontend application logic.
```

It contains:

```text
React imports
Icon imports
API base URL
Initial patient form state
Initial auth form state
Helper functions
Login/signup logic
Logout logic
Patient form submission
Doctor case loading
Doctor review update
Voice report playback
Full JSX UI
```

Important constant:

```javascript
const API_BASE_URL = "http://127.0.0.1:8000";
```

This tells React where the backend is running.

Important frontend states:

```text
session
authMode
authForm
activeView
form
result
cases
reviewDrafts
loading/error states
```

What `session` stores:

```text
token
user details
```

Where session is saved:

```text
browser localStorage under key skin_diagnosis_session
```

Patient submit flow inside frontend:

```text
User fills form
User selects image
submitCase() runs
Creates FormData
Sends POST /predict with Authorization header
Receives JSON result
Stores result in React state
UI displays result card
```

Doctor dashboard flow inside frontend:

```text
Doctor logs in
loadCases() calls GET /cases
Cases are stored in state
UI maps each case to a case card
Doctor edits status/notes
submitReview() calls POST /cases/{case_id}/review
Updated case replaces old case in state
```

Voice report flow:

```text
Patient clicks Play Voice Report
speakReport() builds text
SpeechSynthesisUtterance is created
window.speechSynthesis.speak() reads it aloud
Stop button calls window.speechSynthesis.cancel()
```

### 4.24 frontend/src/styles.css

Purpose:

```text
Controls the visual design of the app.
```

It styles:

```text
Page shell
Intro panel
Auth screen
Patient form
Upload box
Result panel
Risk badges
Medicine guidance box
Top predictions list
Doctor dashboard
Case cards
Review form
Voice buttons
Mobile responsiveness
```

Responsive design:

```text
The @media rule changes grid layouts to single-column layout on smaller screens.
```

### 4.25 frontend/dist/

Purpose:

```text
Built production frontend files.
```

Created by:

```powershell
npm.cmd run build
```

Served by FastAPI route:

```text
GET /app
```

Important:

```text
If you change frontend/src files, you must rebuild frontend/dist before using /app through FastAPI.
```

### 4.26 frontend/node_modules/

Purpose:

```text
Installed frontend packages.
```

Created by:

```powershell
npm.cmd install
```

Usually you do not send this folder to teammates because it is large. They can recreate it using npm install.

### 4.27 docs/

Purpose:

```text
Contains project notes and step-by-step guides.
```

Important docs:

```text
backend_step1_guide.md -> backend setup explanation
step3_patient_frontend_guide.md -> patient frontend explanation
step4_doctor_dashboard_guide.md -> doctor dashboard explanation
step5_voice_report_guide.md -> voice report explanation
step6_login_signup_guide.md -> auth explanation
step7_model_integration_preparation.md -> model integration explanation
model_contract.md -> agreement between model and backend
model_notebook_analysis_and_integration.md -> training notebook summary
stop_and_resume_guide.md -> how to start/stop project
```

### 4.28 model_training/skin_disease_model.ipynb

Purpose:

```text
Training notebook for the skin disease model.
```

Important notebook details:

```text
Dataset: SkinDisNet
Model: EfficientNetV2B3
Input size: 300x300
Classes: 6
Output activation: softmax
Saved model: best_model.keras
Saved labels: labels.json
```

Notebook class order:

```text
0: Atopic Dermatitis
1: Contact Dermatitis
2: Eczema
3: Scabies
4: Seborrheic Dermatitis
5: Tinea Corporis
```

Reported test performance from existing analysis notes:

```text
Accuracy: 0.9533
Weighted F1: 0.9537
```

## 5. Complete System Workflow

### 5.1 Start Of Use

User opens:

```text
http://127.0.0.1:8000/app
```

FastAPI serves:

```text
frontend/dist/index.html
frontend/dist/assets/*
```

React app loads in browser.

### 5.2 Signup/Login Flow

Patient or doctor creates account:

```text
POST /auth/register
```

Backend:

```text
Validates role
Hashes password
Stores user in SQLite
Creates login token
Stores token in auth_tokens table
Returns token and user
```

Frontend:

```text
Saves token and user in localStorage
Shows patient app for patient
Shows doctor dashboard for doctor
```

Login flow:

```text
POST /auth/login
```

Backend:

```text
Finds user by email
Verifies password hash
Creates new token
Returns token and user
```

### 5.3 Patient Case Submission Flow

Step-by-step:

```text
1. Patient logs in.
2. Patient fills name, age, gender, body location, itch, pain, symptoms.
3. Patient uploads JPG/PNG skin image.
4. React creates FormData.
5. React sends POST /predict with Bearer token.
6. FastAPI checks token.
7. FastAPI checks user role is patient.
8. Backend saves uploaded image in backend/uploads.
9. Backend calls predict_skin_disease(image_path).
10. prediction.py loads model if available.
11. Image is resized to 300x300 RGB.
12. Model predicts six class probabilities.
13. Highest probability becomes predicted disease.
14. Top 3 predictions are created.
15. recommendations.py creates risk level, medicine guidance, doctor reason, voice text.
16. database.py saves full case in SQLite.
17. Backend returns case JSON.
18. React displays result card.
```

### 5.4 Doctor Review Flow

Step-by-step:

```text
1. Doctor logs in.
2. Doctor opens dashboard.
3. React calls GET /cases with Bearer token.
4. FastAPI checks token.
5. FastAPI checks user role is doctor.
6. Backend reads all cases from SQLite.
7. Frontend displays case image, patient details, disease, confidence, risk, guidance.
8. Doctor selects review status.
9. Doctor writes notes.
10. React sends POST /cases/{case_id}/review.
11. Backend updates doctor_status and doctor_notes.
12. Frontend updates that case card.
```

### 5.5 Voice Report Flow

Step-by-step:

```text
1. Patient submits a case.
2. Backend returns voice_text.
3. Patient clicks Play Voice Report.
4. Browser Web Speech API reads the text.
5. Patient can click Stop to cancel speech.
```

## 6. API Endpoints Explained

### GET /

Purpose:

```text
Health check.
```

Returns:

```json
{
  "message": "AI Skin Diagnosis API is running",
  "docs": "/docs"
}
```

### GET /app

Purpose:

```text
Serves React frontend.
```

If frontend build is missing:

```text
Backend returns 404 with message telling you to run npm.cmd run build.
```

### POST /auth/register

Purpose:

```text
Creates patient or doctor account.
```

Example request:

```json
{
  "full_name": "Patient One",
  "email": "patient@example.com",
  "password": "123456",
  "role": "patient"
}
```

Returns:

```text
token and user object
```

### POST /auth/login

Purpose:

```text
Logs in existing user.
```

Example request:

```json
{
  "email": "patient@example.com",
  "password": "123456"
}
```

### GET /auth/me

Purpose:

```text
Returns currently logged-in user.
```

Requires header:

```text
Authorization: Bearer token_here
```

### POST /auth/logout

Purpose:

```text
Deletes token from database.
```

### POST /predict

Purpose:

```text
Patient submits image and symptoms for AI screening.
```

Requires:

```text
Logged-in patient token
multipart/form-data
```

Fields:

```text
patient_name
age
gender
body_location
itch
pain
symptoms
image
```

Returns:

```text
Full saved case with prediction and guidance.
```

### GET /cases

Purpose:

```text
Doctor gets all patient cases.
```

Requires:

```text
Logged-in doctor token
```

### GET /my-cases

Purpose:

```text
Patient gets only their own cases.
```

Requires:

```text
Logged-in patient token
```

### GET /cases/{case_id}

Purpose:

```text
Gets one case by ID.
```

Access rule:

```text
Doctor can view any case.
Patient can view only their own case.
```

### POST /cases/{case_id}/review

Purpose:

```text
Doctor saves review status and notes.
```

Requires:

```text
Logged-in doctor token
```

Example request:

```json
{
  "doctor_status": "Reviewed",
  "doctor_notes": "Patient should consult dermatologist if symptoms continue."
}
```

## 7. AI Model Explanation

### 7.1 Dataset

Dataset:

```text
SkinDisNet
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

### 7.2 Model Architecture

Model used:

```text
EfficientNetV2B3
```

Definition:

```text
EfficientNetV2B3 is a convolutional neural network architecture designed for image classification.
It is efficient because it balances depth, width, and resolution scaling.
```

Notebook configuration:

```text
include_top=False
weights=imagenet
input_shape=(300, 300, 3)
include_preprocessing=True
```

Meaning:

```text
include_top=False removes original ImageNet classifier.
weights=imagenet uses transfer learning from ImageNet.
input_shape=(300,300,3) means image is 300x300 RGB.
include_preprocessing=True means model includes its required preprocessing layer.
```

Custom classification head:

```text
GlobalAveragePooling2D
BatchNormalization
Dropout(0.35)
Dense(256, relu, L2 regularization)
Dropout(0.30)
Dense(6, softmax)
```

Why softmax:

```text
Softmax converts model outputs into probabilities across the six classes.
All probabilities together add up to approximately 1.
```

### 7.3 Transfer Learning

Definition:

```text
Transfer learning means using a model already trained on a large dataset and adapting it for our own dataset.
```

Use here:

```text
EfficientNetV2B3 was pre-trained on ImageNet.
We reused its feature extraction ability and trained final layers for skin disease classes.
```

Why useful:

```text
Needs less data than training from scratch.
Gives better accuracy for student project scale.
Speeds up training.
```

### 7.4 Data Augmentation

Definition:

```text
Data augmentation creates modified versions of images to improve model generalization.
```

Notebook used:

```text
RandomFlip
RandomRotation
RandomZoom
RandomTranslation
RandomContrast
```

Why useful:

```text
Skin images can vary by angle, lighting, zoom, and position.
Augmentation helps model become less sensitive to such variations.
```

### 7.5 Model Input And Output

Input:

```text
One RGB image resized to 300x300
Shape: (1, 300, 300, 3)
```

Output:

```text
Six probability values
One probability for each disease class
```

Example:

```json
{
  "Atopic Dermatitis": 0.04,
  "Contact Dermatitis": 0.05,
  "Eczema": 0.09,
  "Scabies": 0.06,
  "Seborrheic Dermatitis": 0.03,
  "Tinea Corporis": 0.71
}
```

Predicted class:

```text
The class with highest probability.
```

Confidence:

```text
The probability of the selected class.
```

### 7.6 Why labels.json Is Important

The model returns numbers by index:

```text
index 0 probability
index 1 probability
index 2 probability
...
```

The app needs labels.json to know:

```text
0 means Atopic Dermatitis
1 means Contact Dermatitis
...
```

If this mapping is wrong:

```text
The app may display the wrong disease name even if the model output is correct.
```

## 8. Security And Role-Based Access

### 8.1 Password Hashing

The project does not store raw passwords.

Instead:

```text
User enters password
Backend creates random salt
Backend creates secure hash using PBKDF2-HMAC-SHA256
Database stores salt:hash
```

During login:

```text
Backend hashes entered password using same salt
Compares with stored hash
If equal, login succeeds
```

### 8.2 Token-Based Authentication

After login/register:

```text
Backend creates token
Stores token in auth_tokens table
Returns token to frontend
Frontend stores token in localStorage
Frontend sends token in Authorization header
```

Header format:

```text
Authorization: Bearer token_here
```

### 8.3 Role Protection

Patient-only:

```text
POST /predict
GET /my-cases
```

Doctor-only:

```text
GET /cases
POST /cases/{case_id}/review
```

Shared with rule:

```text
GET /cases/{case_id}
```

## 9. How To Run This Project On A Teammate Laptop

### 9.1 What They Need To Install

Install these first:

```text
1. Python 3.11 or Python 3.12
2. Node.js LTS
3. VS Code
4. Git optional
5. Modern browser such as Chrome or Edge
```

Important Windows Python installation option:

```text
Tick "Add python.exe to PATH"
```

Check Python:

```powershell
py --version
python --version
```

At least one should work.

Check Node and npm:

```powershell
node --version
npm --version
```

### 9.2 What Project Files To Send

Send:

```text
backend/
frontend/
docs/
README.md
architecture.png
project_presentation.pptx
model_training/skin_disease_model.ipynb if needed
```

Usually do not send:

```text
frontend/node_modules
backend/app/__pycache__
frontend/dist if they can rebuild
backend/uploads unless demo images are needed
uvicorn log files
```

Important:

```text
If you want the real model to work on their laptop, include backend/models/best_model.keras and backend/models/labels.json.
```

### 9.3 Backend Setup On Their Laptop

Open PowerShell in backend folder:

```powershell
cd "<project-root>\backend"
```

Create virtual environment:

```powershell
py -m venv .venv
```

If `py` does not work:

```powershell
python -m venv .venv
```

Activate virtual environment:

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

Start backend:

```powershell
uvicorn app.main:app --reload
```

Keep this PowerShell window open.

Backend check:

```text
http://127.0.0.1:8000/
```

API docs:

```text
http://127.0.0.1:8000/docs
```

### 9.4 Frontend Setup On Their Laptop

Open another PowerShell:

```powershell
cd "<project-root>\frontend"
```

Install frontend packages:

```powershell
npm.cmd install
```

Build frontend:

```powershell
npm.cmd run build
```

Now open:

```text
http://127.0.0.1:8000/app
```

Important:

```text
For the final app, only the backend server needs to run.
FastAPI serves the built frontend from frontend/dist.
```

### 9.5 Real Model Setup

Ensure these files exist:

```text
backend/models/best_model.keras
backend/models/labels.json
backend/models/class_names.json
```

Then install backend dependencies:

```powershell
pip install -r requirements.txt
```

Since requirements.txt includes TensorFlow:

```text
TensorFlow 2.20.0 will be installed.
```

Start backend:

```powershell
uvicorn app.main:app --reload
```

Submit a new patient case.

Expected result badge:

```text
Real AI model
```

If it shows demo prediction:

```text
Check model files exist.
Check TensorFlow installed.
Restart backend.
Submit a new case.
Do not judge by old cases saved before model integration.
```

## 10. Demo Script For Examiner

### 10.1 Start Project

Run backend:

```powershell
cd "<project-root>\backend"
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/app
```

### 10.2 Patient Demo

Do this:

```text
1. Create/login patient account.
2. Fill patient details.
3. Upload skin image.
4. Submit for screening.
5. Explain result card:
   disease
   confidence
   risk level
   model status
   medicine guidance
   top 3 predictions
   doctor status
6. Click Play Voice Report.
```

### 10.3 Doctor Demo

Do this:

```text
1. Logout patient.
2. Login/create doctor account.
3. Open Doctor Dashboard.
4. Refresh cases.
5. Show uploaded image and patient details.
6. Explain AI screening result.
7. Change review status.
8. Add doctor notes.
9. Save doctor review.
```

### 10.4 API Demo

Open:

```text
http://127.0.0.1:8000/docs
```

Show:

```text
GET /
POST /auth/login
POST /predict
GET /cases
POST /cases/{case_id}/review
```

## 11. How To Explain The Project From Start To End

Use this paragraph in viva:

```text
Our project is a smart remote skin disease screening system. The patient first creates an account and uploads a skin image with symptoms. The React frontend sends this data to a FastAPI backend. The backend verifies the patient token, saves the image, preprocesses it using Pillow and NumPy, and passes it to a TensorFlow/Keras EfficientNetV2B3 model. The model predicts one of six skin disease classes and returns confidence scores. The backend then creates risk level, top-3 predictions, medicine guidance, and voice report text. The complete case is saved in a SQLite database. The patient sees the result in the browser and can listen to a voice report. A doctor can log in separately, view all submitted cases, inspect patient details and images, and add review status and notes. This keeps the doctor in the loop and avoids treating AI output as a final diagnosis.
```

## 12. Implementation Process From Beginning

### Step 1: Backend Skeleton

Created:

```text
backend folder
requirements.txt
FastAPI app
SQLite database functions
Image upload service
Dummy prediction function
Recommendation function
```

Goal:

```text
Make the backend capable of receiving patient data and returning a test prediction.
```

### Step 2: API And Database Flow

Implemented:

```text
POST /predict
GET /cases
GET /cases/{case_id}
POST /cases/{case_id}/review
```

Goal:

```text
Patient cases should be saved and doctors should be able to review them.
```

### Step 3: Patient Frontend

Created:

```text
frontend React app
patient form
image upload
image preview
result display
```

Goal:

```text
Make the project usable through browser instead of only API docs.
```

### Step 4: Doctor Dashboard

Added:

```text
case list
patient details display
uploaded image display
doctor status dropdown
doctor notes box
save review button
```

Goal:

```text
Add human expert validation.
```

### Step 5: Voice Report

Added:

```text
Play Voice Report
Stop
browser speech synthesis
```

Goal:

```text
Make result more accessible and align with output layer in architecture.
```

### Step 6: Login, Signup, And Roles

Added:

```text
patient signup
doctor signup
login
logout
password hashing
token authentication
role protection
```

Goal:

```text
Patients and doctors should have separate access.
```

### Step 7: Real Model Integration

Added:

```text
backend/models folder
best_model.keras
labels.json
TensorFlow loading
image preprocessing
real prediction
dummy fallback
top 3 predictions
model status
medicine guidance
voice text from backend
```

Goal:

```text
Replace demo prediction with trained AI model while keeping app stable.
```

## 13. Common Viva Questions And Answers

### Q1. What problem does your project solve?

Answer:

```text
It helps patients remotely screen possible skin diseases by uploading an image and symptoms. It also allows doctors to review AI-screened cases, which is useful where immediate dermatology access is limited.
```

### Q2. Is this a final diagnosis system?

Answer:

```text
No. It is a screening and decision-support system. The AI result must be reviewed by a doctor before final diagnosis or prescription.
```

### Q3. Why did you use FastAPI?

Answer:

```text
FastAPI is fast, simple, supports automatic API documentation, handles file uploads, and integrates well with Python machine learning libraries.
```

### Q4. Why did you use SQLite?

Answer:

```text
SQLite is lightweight, file-based, and does not require a separate database server, so it is ideal for a local academic prototype.
```

### Q5. Why did you use React?

Answer:

```text
React makes it easy to build an interactive frontend with forms, image preview, login state, result cards, and doctor dashboard updates.
```

### Q6. What is the role of TensorFlow/Keras?

Answer:

```text
TensorFlow/Keras loads the trained EfficientNetV2B3 model and runs image classification on the uploaded skin image.
```

### Q7. What model did you use?

Answer:

```text
We used EfficientNetV2B3 with transfer learning. The final classifier predicts six SkinDisNet disease classes.
```

### Q8. What are the six classes?

Answer:

```text
Atopic Dermatitis, Contact Dermatitis, Eczema, Scabies, Seborrheic Dermatitis, and Tinea Corporis.
```

### Q9. How is image preprocessing done?

Answer:

```text
The backend opens the uploaded image using Pillow, converts it to RGB, resizes it to 300x300, converts it to a NumPy float32 array, and adds a batch dimension before passing it to the model.
```

### Q10. Why do you need labels.json?

Answer:

```text
The model outputs probabilities by index. labels.json maps those indexes to disease names. Without correct label order, predictions can be displayed incorrectly.
```

### Q11. What happens if the model file is missing?

Answer:

```text
The backend falls back to dummy prediction so the rest of the app can still be demonstrated.
```

### Q12. How do you protect doctor dashboard?

Answer:

```text
The backend checks the Bearer token and verifies that the logged-in user's role is doctor before allowing access to /cases and /cases/{case_id}/review.
```

### Q13. How are passwords stored?

Answer:

```text
Passwords are not stored directly. We store salted PBKDF2-HMAC-SHA256 password hashes.
```

### Q14. How are uploaded images stored?

Answer:

```text
They are saved in backend/uploads using unique UUID filenames. The database stores the image URL path.
```

### Q15. How does the voice report work?

Answer:

```text
The backend returns voice_text. The frontend uses the browser Web Speech API to read that text aloud when the user clicks Play Voice Report.
```

### Q16. Why do you have a doctor review even after AI prediction?

Answer:

```text
Medical AI should support doctors, not replace them. The doctor dashboard keeps a human expert in the loop for safety and validation.
```

### Q17. What is CORS?

Answer:

```text
CORS means Cross-Origin Resource Sharing. It controls whether frontend running on one origin can call backend running on another origin. We enabled it so frontend requests can reach FastAPI during development.
```

### Q18. What is FormData?

Answer:

```text
FormData is a browser object used to send form fields and files together as multipart/form-data. We use it because /predict receives both patient details and an image file.
```

### Q19. What is localStorage used for?

Answer:

```text
The frontend stores the login session token and user details in localStorage so the user remains logged in after page refresh.
```

### Q20. What improvements can be made in future?

Answer:

```text
Deploy online, add HTTPS, token expiry, admin approval for doctors, better dataset, Grad-CAM explainability, mobile app, mobile camera capture, SMS/email alerts, cloud database, and dermatologist feedback loop.
```

## 14. Troubleshooting

### Backend command not working

Check:

```powershell
cd "<project-root>\backend"
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend page says build not found

Run:

```powershell
cd "<project-root>\frontend"
npm.cmd install
npm.cmd run build
```

Then refresh:

```text
http://127.0.0.1:8000/app
```

### Port 8000 already in use

It means an old backend may still be running.

Stop old PowerShell server using:

```text
Ctrl + C
```

Then restart:

```powershell
uvicorn app.main:app --reload
```

### PowerShell blocks virtual environment activation

Run:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Then:

```powershell
.\.venv\Scripts\Activate.ps1
```

### npm command blocked

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

### Prediction shows Demo prediction

Check:

```text
backend/models/best_model.keras exists
backend/models/labels.json exists
TensorFlow installed
Backend restarted after adding model
```

### Uploaded image not showing in doctor dashboard

Check:

```text
backend/uploads contains image
image_path in database starts with /uploads/
FastAPI is running
```

## 15. What Each Teammate Should Understand

### Teammate 1: Backend/API

Must explain:

```text
FastAPI
routes
SQLite
schemas
auth tokens
role protection
image upload
case save and review
```

### Teammate 2: Frontend/UI

Must explain:

```text
React
state
forms
fetch API
FormData
localStorage
patient app
doctor dashboard
voice report
```

### Teammate 3: AI/Model

Must explain:

```text
SkinDisNet
six classes
EfficientNetV2B3
transfer learning
image preprocessing
softmax
confidence
labels.json
model integration
```

### Teammate 4: System Integration/Presentation

Must explain:

```text
complete workflow
architecture diagram
doctor-in-the-loop safety
setup process
demo process
limitations
future scope
```

Everyone should be able to explain the full flow at a high level.

## 16. Final One-Minute Summary

Use this if examiner asks for a quick explanation:

```text
This is a remote skin disease screening web application. The frontend is built with React and Vite. The backend is built with FastAPI in Python. Patients can register, log in, upload a skin image, and enter symptoms. The backend saves the image, preprocesses it to 300x300 RGB, and sends it to a TensorFlow/Keras EfficientNetV2B3 model trained on six SkinDisNet classes. The result includes predicted disease, confidence, top-3 predictions, risk level, medicine guidance, and voice report text. The case is stored in a SQLite database. Doctors can log in separately, view all submitted cases, inspect images and AI results, and save review notes. The system is designed as a doctor-supported screening tool, not a replacement for medical diagnosis.
```



