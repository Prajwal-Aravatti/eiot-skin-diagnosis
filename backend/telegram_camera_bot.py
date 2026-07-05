import os
from pathlib import Path

import requests


API_BASE_URL = os.getenv("SKIN_DIAGNOSIS_API_URL", "http://127.0.0.1:8000").rstrip("/")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
DOWNLOAD_DIR = Path(__file__).resolve().parent / "telegram_downloads"


def telegram_url(method: str) -> str:
    return f"https://api.telegram.org/bot{BOT_TOKEN}/{method}"


def send_message(chat_id: int, text: str) -> None:
    requests.post(
        telegram_url("sendMessage"),
        json={"chat_id": chat_id, "text": text},
        timeout=20,
    )


def caption_help() -> str:
    return (
        "Send a skin image with this caption:\n\n"
        "name: Patient Name\n"
        "age: 21\n"
        "gender: Male\n"
        "location: Arm\n"
        "itch: yes\n"
        "pain: no\n"
        "symptoms: red circular patch"
    )


def parse_caption(caption: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in caption.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        values[key.strip().lower()] = value.strip()

    required = ["name", "age", "gender", "location", "itch", "pain"]
    missing = [key for key in required if not values.get(key)]
    if missing:
        raise ValueError(f"Missing caption field(s): {', '.join(missing)}")

    return values


def login_patient(email: str, password: str) -> tuple[str, dict]:
    response = requests.post(
        f"{API_BASE_URL}/auth/login",
        json={"email": email, "password": password},
        timeout=20,
    )
    response.raise_for_status()
    data = response.json()
    if data["user"]["role"] != "patient":
        raise ValueError("Only patient accounts can submit cases from Telegram.")
    return data["token"], data["user"]


def download_photo(file_id: str) -> Path:
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
    file_response = requests.get(
        telegram_url("getFile"),
        params={"file_id": file_id},
        timeout=20,
    )
    file_response.raise_for_status()
    file_path = file_response.json()["result"]["file_path"]

    download_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
    image_response = requests.get(download_url, timeout=30)
    image_response.raise_for_status()

    local_path = DOWNLOAD_DIR / Path(file_path).name
    local_path.write_bytes(image_response.content)
    return local_path


def submit_case(token: str, chat_id: int, photo_path: Path, caption_data: dict[str, str]) -> dict:
    with photo_path.open("rb") as image_file:
        response = requests.post(
            f"{API_BASE_URL}/predict",
            headers={"Authorization": f"Bearer {token}"},
            data={
                "patient_name": caption_data["name"],
                "age": caption_data["age"],
                "gender": caption_data["gender"],
                "body_location": caption_data["location"],
                "itch": caption_data["itch"],
                "pain": caption_data["pain"],
                "symptoms": caption_data.get("symptoms", ""),
            },
            files={"image": (photo_path.name, image_file, "image/jpeg")},
            timeout=60,
        )
    response.raise_for_status()
    case = response.json()

    requests.post(
        f"{API_BASE_URL}/telegram/cases/{case['id']}/link",
        headers={"Authorization": f"Bearer {token}"},
        json={"chat_id": str(chat_id)},
        timeout=20,
    ).raise_for_status()
    return case


def main() -> None:
    if not BOT_TOKEN:
        raise RuntimeError("Set TELEGRAM_BOT_TOKEN before starting telegram_camera_bot.py")

    sessions: dict[int, dict] = {}
    offset = None
    print("Telegram camera bot started. Press Ctrl+C to stop.")

    while True:
        response = requests.get(
            telegram_url("getUpdates"),
            params={"offset": offset, "timeout": 30},
            timeout=40,
        )
        response.raise_for_status()

        for update in response.json().get("result", []):
            offset = update["update_id"] + 1
            message = update.get("message") or {}
            chat_id = message.get("chat", {}).get("id")
            if not chat_id:
                continue

            text = (message.get("text") or "").strip()
            session = sessions.setdefault(chat_id, {"step": "email"})

            try:
                if text.lower() in {"/start", "hi", "hello"}:
                    sessions[chat_id] = {"step": "email"}
                    send_message(chat_id, "Enter patient email.")
                    continue

                if text.lower() == "/logout":
                    sessions.pop(chat_id, None)
                    send_message(chat_id, "You are logged out from the Telegram bot session.")
                    continue

                if session["step"] == "email":
                    session["email"] = text
                    session["step"] = "password"
                    send_message(chat_id, "Enter patient password.")
                    continue

                if session["step"] == "password":
                    token, user = login_patient(session["email"], text)
                    sessions[chat_id] = {"step": "ready", "token": token, "user": user}
                    send_message(chat_id, "Login successful.\n\n" + caption_help())
                    continue

                if "photo" not in message:
                    send_message(chat_id, caption_help())
                    continue

                caption_data = parse_caption(message.get("caption") or "")
                largest_photo = message["photo"][-1]
                photo_path = download_photo(largest_photo["file_id"])
                case = submit_case(session["token"], chat_id, photo_path, caption_data)
                send_message(
                    chat_id,
                    "Case submitted.\n\n"
                    f"Case ID: {case['id']}\n"
                    f"Prediction: {case['predicted_disease']}\n"
                    f"Confidence: {case['confidence'] * 100:.1f}%\n"
                    f"Risk: {case['risk_level']}",
                )
            except Exception as error:
                send_message(chat_id, f"Submission failed.\n\n{error}")


if __name__ == "__main__":
    main()
