# Step 6 Guide: Login, Signup, And Role Separation

This step adds account-based access for patients and doctors.

## Why We Added Login

Login is useful because the project handles patient images and health-related details.

Without login:

```text
anyone can submit cases
anyone can open doctor dashboard
anyone can view all cases
```

With login:

```text
patients submit their own cases
doctors view and review submitted cases
backend checks the user's role before allowing access
```

This improves privacy and makes the project look more complete.

## What We Implemented

New features:

```text
patient signup
doctor signup
login
logout
password hashing
token-based login
patient-only case submission
doctor-only case dashboard
doctor-only case review
```

## Technologies Used

### Backend

```text
FastAPI
SQLite
Python hashlib
Python secrets
Bearer token authentication
```

### Frontend

```text
React
localStorage
fetch Authorization headers
```

## New Backend API Routes

### Register

```text
POST /auth/register
```

Body:

```json
{
  "full_name": "Prajwal",
  "email": "prajwal@example.com",
  "password": "123456",
  "role": "patient"
}
```

Role can be:

```text
patient
doctor
```

### Login

```text
POST /auth/login
```

Body:

```json
{
  "email": "prajwal@example.com",
  "password": "123456"
}
```

Returns:

```json
{
  "token": "login-token",
  "user": {
    "id": 1,
    "full_name": "Prajwal",
    "email": "prajwal@example.com",
    "role": "patient",
    "created_at": "..."
  }
}
```

### Current User

```text
GET /auth/me
```

Requires:

```text
Authorization: Bearer token
```

### Logout

```text
POST /auth/logout
```

Deletes the saved token from the backend database.

## Protected Routes

### Patient Only

```text
POST /predict
GET /my-cases
```

Only logged-in patients can submit screening cases.

### Doctor Only

```text
GET /cases
POST /cases/{case_id}/review
```

Only logged-in doctors can view all cases and save review notes.

### Shared With Rules

```text
GET /cases/{case_id}
```

Doctors can view any case.

Patients can only view their own case.

## Database Changes

SQLite now has these main tables:

```text
users
auth_tokens
cases
```

### users table

Stores:

```text
id
full_name
email
password_hash
role
created_at
```

The raw password is not stored.

### auth_tokens table

Stores login tokens:

```text
token
user_id
created_at
```

### cases table

Now also stores:

```text
user_id
```

This connects a patient case to the patient account.

## Files Changed

```text
backend/app/main.py
```

Added auth routes and role protection.

```text
backend/app/database.py
```

Added users table, auth token table, and user-linked cases.

```text
backend/app/schemas.py
```

Added login, register, user, and auth response schemas.

```text
backend/app/services/auth.py
```

Added password hashing, password verification, and token creation.

```text
frontend/src/main.jsx
```

Added login/signup UI, logout, role-based view switching, and authorization headers.

```text
frontend/src/styles.css
```

Added styling for auth pages and account bar.

## How To Test

Restart backend:

```powershell
cd "C:\Users\Hp\5 th Sem\EIOT\backend"
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/app
```

Test patient:

```text
Create patient account
Submit skin screening case
Check result and voice report
Logout
```

Test doctor:

```text
Create doctor account
Open doctor dashboard
Refresh cases
Review a patient case
Save doctor notes
Logout
```

## Important Demo Note

For demo, create two accounts:

```text
Patient account
Doctor account
```

Use patient account to submit a case.

Use doctor account to review that case.

This clearly shows privacy and doctor-in-the-loop validation.

## Current Limitation

This is good for local project demonstration.

For real hospital production use, more security would be needed:

```text
HTTPS
token expiry
password reset
admin doctor approval
audit logs
stronger deployment security
```

But for your EIOT academic project, this is a strong and realistic implementation.

