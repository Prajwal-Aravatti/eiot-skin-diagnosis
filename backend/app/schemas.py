from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    full_name: str
    email: str
    password: str = Field(min_length=6)
    role: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str
    role: str
    created_at: str


class AuthResponse(BaseModel):
    token: str
    user: UserResponse


class Probabilities(BaseModel):
    atopic_dermatitis: float = Field(alias="Atopic Dermatitis")
    contact_dermatitis: float = Field(alias="Contact Dermatitis")
    eczema: float = Field(alias="Eczema")
    scabies: float = Field(alias="Scabies")
    seborrheic_dermatitis: float = Field(alias="Seborrheic Dermatitis")
    tinea_corporis: float = Field(alias="Tinea Corporis")


class PredictionResult(BaseModel):
    disease: str
    confidence: float
    probabilities: dict[str, float]


class TopPrediction(BaseModel):
    disease: str
    confidence: float


class MedicineGuidance(BaseModel):
    category: str
    examples: list[str]
    instruction: str
    doctor_approval_required: bool


class CaseResponse(BaseModel):
    id: int
    user_id: int | None = None
    disease: str | None = None
    patient_name: str
    age: int
    gender: str
    body_location: str
    itch: str
    pain: str
    symptoms: str | None
    image_path: str
    predicted_disease: str
    confidence: float
    top_3_predictions: list[TopPrediction] = []
    risk_level: str
    needs_doctor_review: bool = True
    doctor_reason: str | None = None
    medicine_guidance: MedicineGuidance | None = None
    voice_text: str | None = None
    model_status: str | None = None
    recommendation: str
    doctor_status: str
    doctor_notes: str | None
    created_at: str


class ReviewRequest(BaseModel):
    doctor_status: str
    doctor_notes: str | None = None


class TelegramCaseLinkRequest(BaseModel):
    chat_id: str
