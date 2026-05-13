from sqlite3 import IntegrityError

from fastapi import Depends, FastAPI, File, Form, Header, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.config import APP_NAME, FRONTEND_ASSETS_DIR, FRONTEND_DIST_DIR, UPLOAD_DIR
from app.database import (
    create_case,
    create_token,
    create_user,
    delete_token,
    get_case,
    get_user_by_email,
    get_user_by_token,
    init_db,
    list_cases,
    list_cases_for_user,
    update_case_review,
)
from app.schemas import AuthResponse, CaseResponse, ReviewRequest, UserCreate, UserLogin, UserResponse
from app.services.auth import create_auth_token, hash_password, verify_password
from app.services.prediction import predict_skin_disease
from app.services.recommendations import build_backend_result
from app.services.storage import save_upload_file


app = FastAPI(title=APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@app.on_event("startup")
def on_startup() -> None:
    init_db()
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

if FRONTEND_ASSETS_DIR.exists():
    app.mount("/app/assets", StaticFiles(directory=FRONTEND_ASSETS_DIR), name="frontend-assets")


def _extract_token(authorization: str | None) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Login required")
    return authorization.removeprefix("Bearer ").strip()


def get_current_user(authorization: str | None = Header(None)) -> dict:
    token = _extract_token(authorization)
    user = get_user_by_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired login")
    return user


def require_patient(user: dict = Depends(get_current_user)) -> dict:
    if user["role"] != "patient":
        raise HTTPException(status_code=403, detail="Patient account required")
    return user


def require_doctor(user: dict = Depends(get_current_user)) -> dict:
    if user["role"] != "doctor":
        raise HTTPException(status_code=403, detail="Doctor account required")
    return user


@app.get("/")
def health_check() -> dict:
    return {
        "message": "EIOT Skin Diagnosis API is running",
        "docs": "/docs",
    }


@app.get("/app")
@app.get("/app/")
def patient_app() -> FileResponse:
    index_file = FRONTEND_DIST_DIR / "index.html"
    if not index_file.exists():
        raise HTTPException(
            status_code=404,
            detail="Frontend build not found. Run npm.cmd run build inside the frontend folder.",
        )
    return FileResponse(index_file)


@app.post("/auth/register", response_model=AuthResponse)
def register_user(user_data: UserCreate) -> dict:
    role = user_data.role.lower()
    if role not in ["patient", "doctor"]:
        raise HTTPException(status_code=400, detail="Role must be patient or doctor")

    try:
        user = create_user(
            full_name=user_data.full_name.strip(),
            email=user_data.email.strip(),
            password_hash=hash_password(user_data.password),
            role=role,
        )
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Email is already registered")

    token = create_auth_token()
    create_token(token, user["id"])
    return {"token": token, "user": user}


@app.post("/auth/login", response_model=AuthResponse)
def login_user(credentials: UserLogin) -> dict:
    stored_user = get_user_by_email(credentials.email.strip())
    if not stored_user or not verify_password(credentials.password, stored_user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    user = {
        "id": stored_user["id"],
        "full_name": stored_user["full_name"],
        "email": stored_user["email"],
        "role": stored_user["role"],
        "created_at": stored_user["created_at"],
    }
    token = create_auth_token()
    create_token(token, user["id"])
    return {"token": token, "user": user}


@app.get("/auth/me", response_model=UserResponse)
def read_current_user(user: dict = Depends(get_current_user)) -> dict:
    return user


@app.post("/auth/logout")
def logout_user(authorization: str | None = Header(None)) -> dict:
    token = _extract_token(authorization)
    delete_token(token)
    return {"message": "Logged out"}


@app.post("/predict", response_model=CaseResponse)
async def predict_case(
    patient_name: str = Form(...),
    age: int = Form(...),
    gender: str = Form(...),
    body_location: str = Form(...),
    itch: str = Form(...),
    pain: str = Form(...),
    symptoms: str | None = Form(None),
    image: UploadFile = File(...),
    user: dict = Depends(require_patient),
) -> dict:
    image_path = await save_upload_file(image)
    prediction = predict_skin_disease(image_path)
    backend_result = build_backend_result(prediction)
    medicine = backend_result["medicine_guidance"]
    recommendation = (
        f"{medicine['category']}: {medicine['instruction']} "
        f"{backend_result['doctor_reason']}"
    )

    case = create_case(
        {
            "user_id": user["id"],
            "patient_name": patient_name,
            "age": age,
            "gender": gender,
            "body_location": body_location,
            "itch": itch,
            "pain": pain,
            "symptoms": symptoms,
            "image_path": f"/uploads/{image_path.name}",
            "predicted_disease": backend_result["disease"],
            "confidence": backend_result["confidence"],
            "risk_level": backend_result["risk_level"],
            "top_3_predictions": backend_result["top_3_predictions"],
            "needs_doctor_review": backend_result["needs_doctor_review"],
            "doctor_reason": backend_result["doctor_reason"],
            "medicine_guidance": backend_result["medicine_guidance"],
            "voice_text": backend_result["voice_text"],
            "model_status": backend_result["model_status"],
            "recommendation": recommendation,
            "doctor_status": "Pending",
            "doctor_notes": None,
        }
    )

    return case


@app.get("/cases", response_model=list[CaseResponse])
def get_cases(user: dict = Depends(require_doctor)) -> list[dict]:
    return list_cases()


@app.get("/my-cases", response_model=list[CaseResponse])
def get_my_cases(user: dict = Depends(require_patient)) -> list[dict]:
    return list_cases_for_user(user["id"])


@app.get("/cases/{case_id}", response_model=CaseResponse)
def get_case_by_id(case_id: int, user: dict = Depends(get_current_user)) -> dict:
    case = get_case(case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    if user["role"] == "patient" and case.get("user_id") != user["id"]:
        raise HTTPException(status_code=403, detail="You can only view your own cases")
    return case


@app.post("/cases/{case_id}/review", response_model=CaseResponse)
def review_case(case_id: int, review: ReviewRequest, user: dict = Depends(require_doctor)) -> dict:
    case = update_case_review(
        case_id=case_id,
        doctor_status=review.doctor_status,
        doctor_notes=review.doctor_notes,
    )
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case
