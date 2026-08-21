# 💪 AI Real-Time GYM Assistant

> **Next-Gen Computer Vision & Proactive Voice AI Coach for Real-Time Form Correction and Workout Tracking.**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.54.0-FF4B4B?style=for-the-badge&logo=streamlit)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.14-00F2FE?style=for-the-badge&logo=google)
![Groq](https://img.shields.io/badge/Groq-AI%20LLM-8B5CF6?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

---

## 🌟 Overview

The **AI Real-Time GYM Assistant** is an end-to-end fitness application that monitors user posture during exercise via a live camera feed. Powered by MediaPipe 33-point pose landmarking and Groq LLM intelligence, the system counts reps, checks form errors, and speaks proactive audio cues in real time to prevent injury and optimize training performance.

---

## ✨ Features

- 📹 **30 FPS Real-Time Pose Landmarking**: Uses MediaPipe PoseLandmarker to analyze joint angles (knee, hip, elbow, back arch, torso inclination) in real time via WebRTC.
- 🎙️ **Proactive AI Voice Coaching**: Integrated Groq LLM + gTTS (Google Text-to-Speech) + Web Audio API to deliver natural, high-energy coaching cues directly through your device speakers.
- 🏋️‍♂️ **5 Target Exercises Supported**:
  - **Squats**: Detects knee angle, back lean angle, and depth status (`TOO HIGH`, `GOOD DEPTH`).
  - **Push-ups**: Monitors elbow angle, body alignment, and hip posture (`SAGGING`, `PIKED UP`).
  - **Biceps Curls**: Tracks elbow flexion, shoulder drift, and torso swinging.
  - **Shoulder Press**: Checks arm extension and lower back arching.
  - **Lunges**: Evaluates front knee flex angle, torso inclination, and lateral balance.
- 📊 **Automated Workout Logging**: SQLite database integration storing total reps, completed sets, active duration, and session dates per profile.
- 🎨 **Futuristic Glassmorphic Dark UI**: High-converting landing page, deep obsidian theme (`#0B0E14`), neon accents, live 1-second updating sidebar metrics, and glowing speech cards.

---

## 🏗️ Architecture & Project Structure

```text
AI_trainer/
├── main.py                          # Main Streamlit dashboard & WebRTC video streamer
├── requirements.txt                 # Project dependencies
├── .env                             # Environment variables (GROQ_API_KEY)
├── data.db                          # SQLite database for exercise history
├── ml_models/
│   └── pose_landmarker_full.task    # MediaPipe pose landmarking model
├── detectors/                       # Exercise geometry detection algorithms
│   ├── squat.py
│   ├── pushups.py
│   ├── biceps_curl.py
│   ├── shoulder_press.py
│   └── lunges.py
├── services/
│   ├── auth/
│   │   └── login.py                 # Landing page & user authentication
│   ├── coaching/
│   │   ├── llm.py                   # Groq LLM prompt & completion handler
│   │   ├── tts.py                   # gTTS text-to-speech generator
│   │   └── voice_pipeLine.py        # Voice pipeline & Web Audio API player
│   ├── config/
│   │   └── workout_config.py        # Exercise parameters & system prompts
│   ├── persistence/
│   │   └── exercise_repo.py         # SQLite database CRUD operations
│   ├── state/
│   │   └── default_session.py       # Streamlit session state initialization
│   ├── tracking/
│   │   └── metrics.py               # Live pose metrics sync & event trigger
│   ├── ui/
│   │   └── style_loader.py          # CSS, Google Fonts & Web Audio API injection
│   └── vision/
│       └── exercise_video_processor.py # WebRTC frame handler & skeleton overlay
└── static/
    └── stle.css                     # Dark glassmorphism stylesheet
```

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.10 or higher
- Webcam connected to your computer
- Free [Groq API Key](https://console.groq.com/)

### 2. Installation & Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/AI_trainer.git
   cd AI_trainer
   ```

2. **Create & Activate Virtual Environment**:
   ```bash
   # Windows (PowerShell)
   python -m venv .venv
   .venv\Scripts\Activate.ps1

   # macOS / Linux
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**:
   Create a `.env` file in the project root:
   ```env
   GROQ_API_KEY=gsk_your_groq_api_key_here
   ```

5. **Run the Application**:
   ```bash
   streamlit run main.py
   ```

6. Open your web browser at `http://localhost:8501`.

---

## 🌐 Deployment Guide

### Option 1: Streamlit Community Cloud (Free & Recommended)
1. Push your project to a GitHub repository.
2. Sign in to [share.streamlit.io](https://share.streamlit.io/).
3. Click **New app** and select your repository & `main.py`.
4. In App Settings > **Secrets**, add:
   ```toml
   GROQ_API_KEY = "gsk_your_groq_api_key_here"
   ```
5. Click **Deploy**!

### Option 2: Render.com (Web Service)
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `streamlit run main.py --server.port $PORT --server.address 0.0.0.0`
- **Environment Variables**: Add `GROQ_API_KEY`.

---

## 🛠️ Technology Stack

| Component | Technology |
|---|---|
| **Frontend UI** | Streamlit, HTML5, CSS3 Glassmorphic Design |
| **Video Processing** | Streamlit WebRTC, OpenCV |
| **Pose Detection** | MediaPipe Tasks Vision (33-Point Landmarker) |
| **AI LLM Engine** | Groq API (`openai/gpt-oss-20b` / `llama-3.3-70b-versatile`) |
| **Voice Synthesis** | gTTS (Google Text-to-Speech), Web Audio API |
| **Database** | SQLite3 |

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
