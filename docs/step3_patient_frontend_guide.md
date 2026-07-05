# Step 3 Guide: Patient Frontend

This step creates the patient-facing web app.

The patient app collects patient details, accepts a skin image upload, sends the data to the FastAPI backend, and displays the screening result.

## What We Created

New folder:

```text
<project-root>\frontend
```

Important files:

```text
frontend/package.json
frontend/index.html
frontend/src/main.jsx
frontend/src/styles.css
frontend/dist/index.html
```

## What Each File Does

```text
frontend/package.json
```

Stores frontend package details and commands like build.

```text
frontend/src/main.jsx
```

Main React code. It contains the patient form, image upload, backend request, and result display.

```text
frontend/src/styles.css
```

Controls the visual design of the patient app.

```text
frontend/dist/index.html
```

Final built page that can be opened in the browser.

## Installed Frontend Packages

```text
React
React DOM
Vite
Lucide React
```

React is used to build the user interface.

Vite is used to build the frontend.

Lucide React provides clean icons.

## Important Windows Note

PowerShell may block normal `npm` because of script execution policy.

So use:

```powershell
npm.cmd install
npm.cmd run build
```

instead of:

```powershell
npm install
npm run build
```

## How To Rebuild The Frontend

If you edit frontend code, run:

```powershell
cd "<project-root>\frontend"
npm.cmd run build
```

This updates:

```text
frontend/dist/index.html
```

## How To Open Patient App

Make sure backend is running first:

```powershell
cd "<project-root>\backend"
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

Then open this URL in browser:

```text
http://127.0.0.1:8000/app
```

The frontend sends requests to:

```text
http://127.0.0.1:8000/predict
```

## How To Test

1. Open the patient app.
2. Fill patient name, age, gender, body location, itch, pain, and symptoms.
3. Upload a JPG or PNG image.
4. Click `Submit For Screening`.
5. Check whether the result appears on the right side.

Expected result fields:

```text
Predicted disease
Confidence
Risk level
Recommendation
Case ID
Doctor status
```

## How To Confirm Database Save

Open FastAPI docs:

```text
http://127.0.0.1:8000/docs
```

Run:

```text
GET /cases
```

The case submitted from the patient app should appear there.

## How This Connects To Training Work

Right now the frontend is connected to the backend, and the backend uses dummy prediction.

Current flow:

```text
Patient frontend
    -> FastAPI /predict
    -> dummy prediction.py
    -> SQLite database
    -> result shown in frontend
```

Later flow:

```text
Patient frontend
    -> FastAPI /predict
    -> real trained model in prediction.py
    -> SQLite database
    -> result shown in frontend
```

So when your teammate gives the real model, this patient frontend does not need major changes.

## Step 3 Success Criteria

This step is complete when:

```text
Patient app opens
Form accepts details
Image upload works
Submit calls backend
Result appears in frontend
Case appears in GET /cases
```


