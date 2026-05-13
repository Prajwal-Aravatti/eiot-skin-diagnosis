# Step 5 Guide: Voice Report

This step adds the voice-assisted patient report from the Fusion & Output Layer.

## What We Added

After a patient submits a case and receives a screening result, the result card now shows:

```text
Play Voice Report
Stop
```

The voice report reads:

```text
patient name
predicted disease
confidence
risk level
recommendation
doctor review status
```

## Technology Used

We used the browser's built-in Web Speech API:

```text
window.speechSynthesis
SpeechSynthesisUtterance
```

No extra backend package is needed.

No internet is needed for the basic browser voice.

## Why We Used Browser Text-To-Speech

It is the easiest and safest option for this project stage.

Advantages:

```text
works directly in browser
no audio file generation needed
no Python TTS setup needed
no extra API key needed
fits patient accessibility requirement
```

## Files Changed

```text
frontend/src/main.jsx
```

Added:

```text
speakReport()
stopVoiceReport()
Play Voice Report button
Stop button
```

```text
frontend/src/styles.css
```

Added:

```text
voice button layout
voice button styling
mobile responsive styling
```

## How It Works

Current flow:

```text
Patient submits case
        |
Backend returns result
        |
Frontend displays result
        |
Patient clicks Play Voice Report
        |
Browser reads report aloud
```

## How To Test

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

3. Submit a patient case.

4. In the result card, click:

```text
Play Voice Report
```

5. The browser should read the report aloud.

6. Click:

```text
Stop
```

to stop the speech.

## Alignment With Project Architecture

This implements the part of the architecture that says:

```text
Generate TTS Voice Audio
Display Patient Dashboard
Show Disease, Severity, and Play Voice Report
```

## Limitations

The voice depends on the browser and operating system.

If sound does not play:

```text
check system volume
check Chrome tab is not muted
try clicking Play Voice Report again
```

Some browsers block automatic speech, but user-clicked speech should work.

## Step 5 Success Criteria

This step is complete when:

```text
result card shows Play Voice Report
voice reads the report aloud
Stop button cancels speech
```

