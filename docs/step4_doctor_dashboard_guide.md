# Step 4 Guide: Doctor Dashboard

This step adds the doctor-in-the-loop part of the EIOT architecture.

The doctor dashboard lets a doctor view patient submissions, inspect the uploaded image and AI screening result, then add review status and notes.

## What We Added

The same frontend app now has two views:

```text
Patient App
Doctor Dashboard
```

Open:

```text
http://127.0.0.1:8000/app
```

Use the top buttons to switch between views.

## Why Doctor Dashboard Is Needed

Your project should not behave like a fully automatic medical diagnosis system.

The AI model gives a screening result, but the doctor dashboard keeps a human expert in the loop.

This matches the project architecture:

```text
AI Model Layer
    -> Fusion & Output Layer
    -> Update Doctor Dashboard
    -> Doctor validation
```

## Backend APIs Used

The doctor dashboard uses existing backend APIs.

### Load all cases

```text
GET http://127.0.0.1:8000/cases
```

This returns all patient cases from SQLite database.

### Update doctor review

```text
POST http://127.0.0.1:8000/cases/{case_id}/review
```

This saves doctor status and doctor notes.

Example body:

```json
{
  "doctor_status": "Reviewed",
  "doctor_notes": "Patient should visit clinic if swelling continues."
}
```

## Frontend Files Changed

```text
frontend/src/main.jsx
```

Added:

```text
Patient App / Doctor Dashboard switcher
case loading from GET /cases
case cards
doctor status dropdown
doctor notes textarea
save review button
```

```text
frontend/src/styles.css
```

Added:

```text
dashboard layout
case card design
case image styling
risk badge styling
review form styling
mobile responsive layout
```

## How To Use Doctor Dashboard

1. Start backend:

```powershell
cd "C:\Users\Hp\5 th Sem\EIOT\backend"
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

2. Open:

```text
http://127.0.0.1:8000/app
```

3. Submit at least one patient case from the Patient App view.

4. Click:

```text
Doctor Dashboard
```

5. Click:

```text
Refresh Cases
```

6. Check the submitted case.

7. Choose review status:

```text
Pending
Reviewed
Needs Consultation
Urgent Follow-up
```

8. Add doctor notes.

9. Click:

```text
Save Doctor Review
```

## Current Workflow After Step 4

```text
Patient submits image and symptoms
        |
Frontend calls POST /predict
        |
Backend saves image
        |
Backend gets dummy AI prediction
        |
Backend calculates risk level
        |
Backend saves case in SQLite
        |
Patient sees result
        |
Doctor Dashboard calls GET /cases
        |
Doctor sees submitted case
        |
Doctor updates status and notes
        |
Frontend calls POST /cases/{case_id}/review
        |
Backend updates SQLite database
```

## Alignment With AI Training Work

This dashboard does not depend on the real model being ready.

Right now it shows dummy prediction results.

Later, after real model integration, it will automatically show real predictions because the dashboard reads saved cases from the database.

The dashboard does not need major changes when the model is added.

## Step 4 Success Criteria

This step is complete when:

```text
Doctor Dashboard button is visible
cases load from database
uploaded image is visible
patient details are visible
prediction and risk are visible
doctor can save status and notes
GET /cases shows updated doctor review
```

