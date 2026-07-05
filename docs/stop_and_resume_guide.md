# Stop And Resume Guide

Use this when stopping for the night and starting the AI skin diagnosis project again later.

## Current Project Status

Completed locally:

```text
FastAPI backend
SQLite database
Image upload storage
Patient login/signup
Doctor login/signup
Patient screening form
Doctor dashboard
Voice report
Real Keras model integration
TensorFlow 2.20.0 installed in backend/.venv
Frontend rebuilt into frontend/dist
```

The real model files are here:

```text
<project-root>\backend\models\best_model.keras
<project-root>\backend\models\labels.json
```

The latest prediction test returned:

```text
model_status: real
```

## What Is Running Right Now

Only the backend server needs to run while using the app.

The app URL is:

```text
http://127.0.0.1:8000/app
```

The API docs URL is:

```text
http://127.0.0.1:8000/docs
```

There is no separate frontend server required because FastAPI serves the built React app from:

```text
<project-root>\frontend\dist
```

## How To Stop Tonight

### Option 1: If Uvicorn Is Visible In PowerShell

If you see a PowerShell window showing something like:

```text
Uvicorn running on http://127.0.0.1:8000
```

click that PowerShell window and press:

```text
Ctrl + C
```

If PowerShell asks:

```text
Terminate batch job (Y/N)?
```

type:

```text
Y
```

and press Enter.

### Option 2: If Uvicorn Is Running In The Background

Open PowerShell and run:

```powershell
Get-Process uvicorn, python -ErrorAction SilentlyContinue
```

If you want to stop only the AI skin diagnosis backend processes, run:

```powershell
Get-CimInstance Win32_Process |
  Where-Object {
    $_.CommandLine -like '*backend*uvicorn*' -or
    $_.CommandLine -like '*backend*app.main*'
  } |
  ForEach-Object {
    Stop-Process -Id $_.ProcessId -Force
  }
```

After that, close browser tabs for:

```text
http://127.0.0.1:8000/app
http://127.0.0.1:8000/docs
```

Nothing else needs to be stopped.

## How To Start Again Tomorrow

Open PowerShell.

Go to the backend folder:

```powershell
cd "<project-root>\backend"
```

Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Start FastAPI:

```powershell
uvicorn app.main:app --reload
```

Keep this PowerShell window open while using the app.

Then open:

```text
http://127.0.0.1:8000/app
```

For API testing, open:

```text
http://127.0.0.1:8000/docs
```

## How To Confirm Everything Is Working

### 1. Check Backend

Open:

```text
http://127.0.0.1:8000/
```

Expected response:

```json
{
  "message": "AI Skin Diagnosis API is running",
  "docs": "/docs"
}
```

### 2. Check Patient Flow

Open:

```text
http://127.0.0.1:8000/app
```

Then:

```text
Login or create a patient account
Fill patient details
Upload JPG or PNG skin image
Submit for screening
Check result card
```

New predictions should show:

```text
Real AI model
```

Older cases may still show dummy because they were created before TensorFlow was installed.

### 3. Check Doctor Flow

Login or create a doctor account.

Then:

```text
Open Doctor Dashboard
Refresh Cases
Review submitted patient cases
Save doctor notes
```

## If It Still Shows Dummy

First confirm TensorFlow is installed:

```powershell
cd "<project-root>\backend"
.\.venv\Scripts\Activate.ps1
python -m pip show tensorflow
```

Expected:

```text
Name: tensorflow
Version: 2.20.0
```

Then confirm model files exist:

```powershell
dir models
```

Expected important files:

```text
best_model.keras
labels.json
class_names.json
```

Restart backend:

```powershell
Ctrl + C
uvicorn app.main:app --reload
```

Submit a new patient case. Do not judge by old saved cases.

## If Port 8000 Is Already In Use

It means the old backend is still running.

Run:

```powershell
Get-CimInstance Win32_Process |
  Where-Object {
    $_.CommandLine -like '*backend*uvicorn*' -or
    $_.CommandLine -like '*backend*app.main*'
  } |
  Select-Object ProcessId, Name, CommandLine
```

Then stop those process IDs:

```powershell
Stop-Process -Id PROCESS_ID_HERE -Force
```

Start again:

```powershell
cd "<project-root>\backend"
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

## If Frontend Changes Are Made Later

After editing files in:

```text
frontend/src
```

rebuild:

```powershell
cd "<project-root>\frontend"
npm.cmd run build
```

Then refresh:

```text
http://127.0.0.1:8000/app
```

## Quick Resume Commands

Most days, this is all you need:

```powershell
cd "<project-root>\backend"
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

Then open:

```text
http://127.0.0.1:8000/app
```



