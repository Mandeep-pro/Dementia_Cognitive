# SmritiRoots (स्मृतिRoots) - Cognitive Wellness & Memory Care

> **Play · Remember · Live Better**  
> An elder-friendly, mobile-first cognitive engagement and dementia care application designed for patients (like Maya Ji) and caregivers.

---

## 📱 Mobile-First Frontend

The frontend is built with React and Vite, strictly matching the provided reference designs:

1. **Home Screen (`media_1790144603540.png`)**:
   - **Header**: Sprout leaf logo, tagline, and Maya Ji's avatar.
   - **Greeting**: *"Good Morning, Maya Ji ☀️ - A brighter day for a healthier you."*
   - **Card 1 (Keep Your Mind Active)**: Lilac/lavender gradient, 3D brain mascot, *"Play a Game Today"*, and *"Start Playing →"* pill button.
   - **Card 2 (Next Reminder)**: Warm peach/vanilla cream card, bell icon, capsule badge, *"Take Medicine - Today, 9:00 AM"*, and full-width brown pill button *"Mark as Done"*.
   - **Card 3 (Your Memories)**: Mint green gradient, polaroid preview, *"View Your Memories"*.
   - **Bottom Navigation**: 4 docked tabs with active pill styling: **Home**, **Games**, **Reminders**, and **Profile**.

2. **Quiz / Brain Boost Screen (`media_1790144618624.png`)**:
   - **Header**: Circular back button (`<`), logo, and **Read Aloud** button (uses Web Speech Synthesis to read question and choices aloud for elder accessibility).
   - **Sub-header**: *"Question X of Y"*, smooth green progress bar, and *"Brain Boost 🧠"* badge.
   - **Question Card**: Mint container, high-contrast dark green typography, *"Choose the correct answer."* subtext. **Strictly text-only questions and options (no images in questions as requested)**.
   - **Options**: Large touch targets (>62px), rounded rectangular cards with circular radio indicator.
   - **Navigation**: *"← Previous"* and *"Next →"* / *"Finish"* pill buttons.
   - **Results Card**: Celebratory score breakdown, accuracy %, time taken, and *"Play Again"* / *"Back to Home"* actions.

---

## 🛠️ Backend API Endpoints & Architecture

### Key Endpoints

| Endpoint | Method | Auth | Description |
| :--- | :---: | :---: | :--- |
| `/api/health` | GET | None | Health check |
| `/api/auth/register` | POST | None | Register new patient or caregiver |
| `/api/auth/login` | POST | None | Login with email and password |
| `/api/patients/me` | GET | Token | **(New)** Current patient self profile |
| `/api/patients/<id>` | GET | Token | Patient profile (accessible by caregiver & patient) |
| `/api/patients/` | GET | Token | Caregiver's patient list |
| `/api/patients/` | POST | Token | Caregiver creates new patient profile |
| `/api/reminders/<patient_id>` | GET | Token | Patient reminders (accessible by caregiver & patient) |
| `/api/reminders/<id>/complete` | PUT | Token | Mark reminder completed (patient "Mark as Done") |
| `/api/memories/<patient_id>` | GET | Token | Patient memories (accessible by caregiver & patient) |
| `/api/games/` | GET | None | Cognitive games directory |
| `/api/questions/general` | GET | None | General text questions (filtered by category/difficulty) |
| `/api/quiz/check-answer` | POST | None | Check answer validity |
| `/api/game-session/personalized` | POST | Token | Generate personalized cognitive session |
| `/api/game-session/submit` | POST | Token | Submit game session answers & compute adaptive score |
| `/api/game-results/<patient_id>` | GET | Token | Game history and statistics |
| `/api/caregiver/dashboard/<patient_id>` | GET | Token | Caregiver dashboard metrics |

---

## 🚀 Running the Project

### 1. Run the Flask Backend
```bash
cd backend
python run.py
```
*Backend runs on `http://127.0.0.1:5000`.*

### 2. Run the Frontend
```bash
cd frontend
npm run dev
```
*Frontend runs on `http://localhost:3000` with automatic API proxy to port 5000.*

To build for production:
```bash
cd frontend
npm run build
```
