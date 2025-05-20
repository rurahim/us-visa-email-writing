# 🛂 Visa Appointment AI Scorer

This project provides an AI-powered scoring system for prioritizing US visa appointments based on urgency, visa type, and message content. It uses:

- **FastAPI** for the backend API
- **OpenAI SDK** for text analysis (can be mocked for offline testing)
- **Streamlit** for the frontend UI
- **Modular Python services** for clean architecture

---

## 🚀 Features

- Score visa appointment requests based on urgency and keywords
- Analyze user message with OpenAI SDK
- Modular service-based design (extractor, scorer, XAI)
- Streamlit GUI for non-technical users
- Easily testable with Postman or CURL

---

## 📁 Project Structure

visa_appointment_ai/
├── app.py # FastAPI entry point
├── models/
│ ├── request_model.py # Pydantic model for API requests
│ └── visa_type.py # Visa weight configuration
├── services/
│ ├── extractor.py # Extracts date & keyword count from message
│ ├── scorer.py # Calculates total score
│ └── xai.py # Explains score via LLM (mockable)
├── api/
│ └── endpoints.py # FastAPI routes
├── streamlit_app/
│ └── gui.py # Streamlit-based frontend
├── requirements.txt
└── README.md # You are here



---

## ⚙️ Installation

### ✅ Clone the Repository

```bash
git clone https://github.com/yourname/visa_appointment_ai.git
cd visa_appointment_ai

python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

fastapi
uvicorn
pydantic
streamlit
requests
openai

OPENAI_API_KEY=your_openai_api_key_here

Run Backend (FastAPI)
uvicorn app:app --reload

Test API with Postman
POST http://127.0.0.1:8000/score

Body JSON
{
  "full_name": "John Doe",
  "email": "john@example.com",
  "visa_type": "F1",
  "message": "My university starts June 5th. Please help me get a visa appointment."
}

Expected Response
{
  "score": {
    "base": 80.0,
    "urgency": 10,
    "keywords": 5,
    "total": 95.0
  },
  "explanation": "Scored using F1 weight, event proximity, and urgency keywords."
}

Run Frontend
streamlit run streamlit_app/gui.py

 How Scoring Works
Base Score: Based on visa type

Urgency Boost: If an event date is found in the message

Keyword Boost: Based on urgency words like urgent, ASAP, soon, etc.

OpenAI SDK (Optional)
If you want XAI to use actual GPT-4 explanations, edit xai.py to use openai.ChatCompletion.create.

Otherwise, the current setup uses mock explanations for local testing.

Modular Testing
You can test modules individually by running:
python -m services.extractor
python -m services.scorer
python -m services.xai


Rauf ur Rahim
AI Engineer | Open Source Contributor
