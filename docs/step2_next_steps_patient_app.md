# Step 2 Next Steps: Patient App And Backend Testing

You have completed Step 1 successfully because the FastAPI docs page opens and `/predict` is working.

Now the project has a backend server. The next goal is to create the patient-facing application that sends data to this backend.

## Current Position

Completed:

```text
Backend server
API documentation page
Dummy prediction API
SQLite database
Image upload saving
Case listing API
Doctor review API
```

Pending:

```text
Patient app UI
Doctor dashboard UI
Real AI model integration
Voice report
Final testing and presentation polish
```

## Overall Next Workflow

The next work should happen in this order:

1. Build patient input page
2. Connect patient page to `/predict`
3. Display prediction result
4. Build doctor dashboard page
5. Connect doctor dashboard to `/cases`
6. Add doctor review update
7. Add voice report
8. Replace dummy model with real trained model

## Why Patient App Comes Next

The backend is already ready to receive:

```text
patient name
age
gender
body location
itch
pain
symptoms
image
```

So now we need a simple screen where the patient can enter these details and upload/capture an image.

This will prove that the frontend and backend are connected correctly before the real AI model arrives.

## Recommended Frontend Choice

Use React with Vite.

Reasons:

```text
Fast to create
Easy to connect to FastAPI
Works in browser on laptop
Can be shown as patient app during demo
Can later be opened from mobile browser also
```

We are not starting with Flutter/Android because that takes more setup time. For this project demo, a React web app is faster and safer.

## Tool Needed For Step 2

Install Node.js LTS.

Download from:

```text
https://nodejs.org/
```

After installation, check in PowerShell:

```powershell
node --version
npm --version
```

Both commands should show version numbers.

## Folder Plan

The project will look like this:

```text
EIOT/
  backend/
    app/
    requirements.txt
  frontend/
    src/
    package.json
  docs/
    model_contract.md
    backend_step1_guide.md
    step2_next_steps_patient_app.md
```

The new `frontend` folder will contain the patient app first.

Later, the same frontend can also include the doctor dashboard.

## Patient App Features

The first patient page should have:

```text
Project title
Patient name input
Age input
Gender select
Body location input/select
Itch yes/no
Pain yes/no
Symptoms textarea
Image upload
Submit button
Result display
```

After submit, it should show:

```text
Predicted disease
Confidence
Risk level
Recommendation
Doctor review status
```

## Backend Connection

The frontend will send data to:

```text
POST http://127.0.0.1:8000/predict
```

Because the request includes an image, it must use `FormData`, not normal JSON.

Frontend sends:

```text
FormData:
  patient_name
  age
  gender
  body_location
  itch
  pain
  symptoms
  image
```

Backend returns:

```json
{
  "id": 1,
  "patient_name": "Test Patient",
  "predicted_disease": "Tinea Corporis",
  "confidence": 71.5,
  "risk_level": "Medium",
  "recommendation": "Keep the area clean and dry...",
  "doctor_status": "Pending"
}
```

## Alignment With Teammate Training Work

While your teammate trains the model, you can finish this frontend using dummy backend prediction.

Later, when real model is ready:

```text
frontend does not change much
database does not change much
doctor dashboard does not change much
only backend prediction.py changes
```

That is why we built a dummy prediction API first.

## What To Do After Patient App Works

After the patient page works, build doctor dashboard.

Doctor dashboard will call:

```text
GET http://127.0.0.1:8000/cases
POST http://127.0.0.1:8000/cases/{case_id}/review
```

This will complete the doctor-in-the-loop part from the architecture.

## Success Criteria For Step 2

Step 2 is complete when:

```text
Patient opens frontend
Patient fills form
Patient uploads image
Frontend sends request to backend
Backend saves case
Frontend displays prediction result
GET /cases shows the same case
```

