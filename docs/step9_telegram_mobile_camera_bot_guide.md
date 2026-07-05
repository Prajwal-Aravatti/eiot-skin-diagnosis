# Telegram Mobile Camera Bot Guide

This optional software feature lets a patient send a phone-captured skin image through Telegram when using the web camera is inconvenient. It is a software-only helper, not a hardware integration module.

## Flow

```text
Telegram mobile app
  -> telegram_camera_bot.py
  -> FastAPI /predict
  -> patient case history
  -> doctor dashboard
```

## Environment

Set these values in the backend terminal:

```powershell
$env:TELEGRAM_BOT_TOKEN="PASTE_BOTFATHER_TOKEN_HERE"
$env:SKIN_DIAGNOSIS_API_URL="http://127.0.0.1:8000"
```

## Start Backend

```powershell
cd backend
uvicorn app.main:app --reload
```

## Start Bot

Open another terminal:

```powershell
cd backend
python telegram_camera_bot.py
```

## Patient Usage

1. Open the Telegram bot.
2. Send `hi`.
3. Enter patient email and password.
4. Send a skin image with this caption:

```text
name: Patient Name
age: 21
gender: Male
location: Arm
itch: yes
pain: no
symptoms: red circular patch
```

The bot submits the image to the same `/predict` endpoint used by the website and links the Telegram chat to that case.

## Doctor Review Notification

When the doctor saves review notes from the website, the backend can send a Telegram message back to the same chat if `TELEGRAM_BOT_TOKEN` is set.


