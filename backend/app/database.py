import json
import sqlite3
from pathlib import Path
from typing import Any

from app.config import DATABASE_PATH


def get_connection() -> sqlite3.Connection:
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('patient', 'doctor')),
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS auth_tokens (
                token TEXT PRIMARY KEY,
                user_id INTEGER NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS cases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                patient_name TEXT NOT NULL,
                age INTEGER NOT NULL,
                gender TEXT NOT NULL,
                body_location TEXT NOT NULL,
                itch TEXT NOT NULL,
                pain TEXT NOT NULL,
                symptoms TEXT,
                image_path TEXT NOT NULL,
                predicted_disease TEXT NOT NULL,
                confidence REAL NOT NULL,
                risk_level TEXT NOT NULL,
                recommendation TEXT NOT NULL,
                top_3_predictions TEXT,
                needs_doctor_review INTEGER NOT NULL DEFAULT 1,
                doctor_reason TEXT,
                medicine_guidance TEXT,
                voice_text TEXT,
                model_status TEXT,
                doctor_status TEXT NOT NULL DEFAULT 'Pending',
                doctor_notes TEXT,
                telegram_chat_id TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
            """
        )
        _ensure_column(connection, "cases", "user_id", "INTEGER")
        _ensure_column(connection, "cases", "top_3_predictions", "TEXT")
        _ensure_column(connection, "cases", "needs_doctor_review", "INTEGER NOT NULL DEFAULT 1")
        _ensure_column(connection, "cases", "doctor_reason", "TEXT")
        _ensure_column(connection, "cases", "medicine_guidance", "TEXT")
        _ensure_column(connection, "cases", "voice_text", "TEXT")
        _ensure_column(connection, "cases", "model_status", "TEXT")
        _ensure_column(connection, "cases", "telegram_chat_id", "TEXT")


def _ensure_column(connection: sqlite3.Connection, table_name: str, column_name: str, column_type: str) -> None:
    columns = connection.execute(f"PRAGMA table_info({table_name})").fetchall()
    if column_name not in [column["name"] for column in columns]:
        connection.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}")


def create_user(full_name: str, email: str, password_hash: str, role: str) -> dict[str, Any]:
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO users (full_name, email, password_hash, role)
            VALUES (?, ?, ?, ?)
            """,
            (full_name, email.lower(), password_hash, role),
        )
        user_id = cursor.lastrowid
    return get_user_by_id(user_id)


def get_user_by_email(email: str) -> dict[str, Any] | None:
    with get_connection() as connection:
        row = connection.execute(
            "SELECT * FROM users WHERE email = ?",
            (email.lower(),),
        ).fetchone()
    return dict(row) if row else None


def get_user_by_id(user_id: int) -> dict[str, Any] | None:
    with get_connection() as connection:
        row = connection.execute(
            "SELECT id, full_name, email, role, created_at FROM users WHERE id = ?",
            (user_id,),
        ).fetchone()
    return dict(row) if row else None


def create_token(token: str, user_id: int) -> None:
    with get_connection() as connection:
        connection.execute(
            "INSERT INTO auth_tokens (token, user_id) VALUES (?, ?)",
            (token, user_id),
        )


def get_user_by_token(token: str) -> dict[str, Any] | None:
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT users.id, users.full_name, users.email, users.role, users.created_at
            FROM auth_tokens
            JOIN users ON users.id = auth_tokens.user_id
            WHERE auth_tokens.token = ?
            """,
            (token,),
        ).fetchone()
    return dict(row) if row else None


def delete_token(token: str) -> None:
    with get_connection() as connection:
        connection.execute("DELETE FROM auth_tokens WHERE token = ?", (token,))


def create_case(case_data: dict[str, Any]) -> dict[str, Any]:
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO cases (
                user_id, patient_name, age, gender, body_location, itch, pain, symptoms,
                image_path, predicted_disease, confidence, risk_level,
                recommendation, top_3_predictions, needs_doctor_review,
                doctor_reason, medicine_guidance, voice_text, model_status,
                doctor_status, doctor_notes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                case_data.get("user_id"),
                case_data["patient_name"],
                case_data["age"],
                case_data["gender"],
                case_data["body_location"],
                case_data["itch"],
                case_data["pain"],
                case_data.get("symptoms"),
                case_data["image_path"],
                case_data["predicted_disease"],
                case_data["confidence"],
                case_data["risk_level"],
                case_data["recommendation"],
                json.dumps(case_data.get("top_3_predictions", [])),
                1 if case_data.get("needs_doctor_review", True) else 0,
                case_data.get("doctor_reason"),
                json.dumps(case_data.get("medicine_guidance")),
                case_data.get("voice_text"),
                case_data.get("model_status"),
                case_data.get("doctor_status", "Pending"),
                case_data.get("doctor_notes"),
            ),
        )
        case_id = cursor.lastrowid

    return get_case(case_id)


def _decode_json(value: str | None, fallback: Any) -> Any:
    if not value:
        return fallback
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return fallback


def _case_from_row(row: sqlite3.Row) -> dict[str, Any]:
    case = dict(row)
    if case.get("confidence") and case["confidence"] > 1:
        case["confidence"] = case["confidence"] / 100

    case["disease"] = case.get("predicted_disease")
    case["top_3_predictions"] = _decode_json(case.get("top_3_predictions"), [])
    case["medicine_guidance"] = _decode_json(case.get("medicine_guidance"), None)
    case["needs_doctor_review"] = bool(case.get("needs_doctor_review", True))

    if not case.get("voice_text"):
        case["voice_text"] = (
            f"The detected condition may be {case.get('predicted_disease')}. "
            f"Confidence score is {case.get('confidence', 0):.2f}. "
            f"Risk level is {case.get('risk_level')}."
        )

    return case


def list_cases() -> list[dict[str, Any]]:
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT * FROM cases ORDER BY created_at DESC"
        ).fetchall()
    return [_case_from_row(row) for row in rows]


def list_cases_for_user(user_id: int) -> list[dict[str, Any]]:
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT * FROM cases WHERE user_id = ? ORDER BY created_at DESC",
            (user_id,),
        ).fetchall()
    return [_case_from_row(row) for row in rows]


def get_case(case_id: int) -> dict[str, Any] | None:
    with get_connection() as connection:
        row = connection.execute(
            "SELECT * FROM cases WHERE id = ?",
            (case_id,),
        ).fetchone()
    return _case_from_row(row) if row else None


def update_case_review(case_id: int, doctor_status: str, doctor_notes: str | None) -> dict[str, Any] | None:
    with get_connection() as connection:
        connection.execute(
            """
            UPDATE cases
            SET doctor_status = ?, doctor_notes = ?
            WHERE id = ?
            """,
            (doctor_status, doctor_notes, case_id),
        )
    return get_case(case_id)


def link_case_to_telegram_chat(case_id: int, user_id: int, telegram_chat_id: str) -> dict[str, Any] | None:
    with get_connection() as connection:
        cursor = connection.execute(
            """
            UPDATE cases
            SET telegram_chat_id = ?
            WHERE id = ? AND user_id = ?
            """,
            (telegram_chat_id, case_id, user_id),
        )
        if cursor.rowcount == 0:
            return None
    return get_case(case_id)


def ensure_parent_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
