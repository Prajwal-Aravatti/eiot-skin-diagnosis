# Smart Remote Skin Disease Diagnosis

EIOT project backend and application workspace.

## Current Status

The backend skeleton is ready with:

- Patient case submission API
- Image upload storage
- Dummy AI prediction
- Risk level calculation
- Recommendation text
- SQLite case database
- Doctor review API
- React patient frontend
- Doctor dashboard frontend
- Browser voice report
- Patient and doctor login/signup
- Role-based API protection
- Real Keras model integration using TensorFlow

## Backend Setup

Install Python 3.11 or 3.12 first, then run:

```powershell
cd "C:\Users\Hp\5 th Sem\EIOT\backend"
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open the API docs:

```text
http://127.0.0.1:8000/docs
```

## Patient Frontend

Install frontend packages:

```powershell
cd "C:\Users\Hp\5 th Sem\EIOT\frontend"
npm.cmd install
```

Build the frontend:

```powershell
npm.cmd run build
```

Open:

```text
http://127.0.0.1:8000/app
```

Keep the backend running while using the frontend.

The same app has:

```text
Patient App
Doctor Dashboard
```

## Real Model Integration

The trained model is now connected locally. The backend has been tested with:

```text
model_status: real
```

When the trained model is ready, update:

```text
backend/models/best_model.keras
backend/models/labels.json
```

The backend will automatically try to load the real model from:

```text
C:\Users\Hp\5 th Sem\EIOT\backend\models\best_model.keras
C:\Users\Hp\5 th Sem\EIOT\backend\models\labels.json
```

Keep the prediction output format same as:

```json
{
  "disease": "Tinea Corporis",
  "confidence": 0.715,
  "top_3_predictions": [],
  "medicine_guidance": {},
  "voice_text": ""
}
```
