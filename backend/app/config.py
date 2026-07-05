from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
PROJECT_DIR = BASE_DIR.parent
APP_NAME = "AI Skin Diagnosis API"
DATABASE_PATH = BASE_DIR / "data" / "skin_diagnosis_cases.db"
UPLOAD_DIR = BASE_DIR / "uploads"
FRONTEND_DIST_DIR = PROJECT_DIR / "frontend" / "dist"
FRONTEND_ASSETS_DIR = FRONTEND_DIST_DIR / "assets"
