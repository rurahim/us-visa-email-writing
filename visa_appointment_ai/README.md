# US Visa Appointment Assistant

A web application that helps optimize visa appointment requests by analyzing messages and providing priority scores based on various factors.

## Application Flow

### 1. Frontend (Streamlit)
- Located in `gui/main_gui.py`
- Provides a user interface with:
  - Full Name input
  - Email input
  - Visa Type selection (B1/B2, F1, H1B, J1, L1, Other)
  - Message text area for appointment request
  - Process Request button

### 2. Request Flow
1. User fills out the form and clicks "Process Request"
2. Frontend validates all fields are filled
3. Frontend sends POST request to backend at `http://localhost:8000/api/process/` with:
   ```json
   {
     "full_name": "user's name",
     "email": "user's email",
     "visa_type": "selected visa type",
     "message": "appointment request message"
   }
   ```

### 3. Backend Processing (FastAPI)
- Located in `api/endpoints.py`
- Receives request and processes it through multiple services:

#### a. Details Extraction (`services/extractor.py`)
- Extracts key information from the message:
  - Event dates using regex pattern matching
  - Urgency score based on keyword matching
  - Returns:
    ```python
    {
        "event_date": datetime or None,
        "urgency_score": int,
        "original_message": str
    }
    ```

#### b. Score Calculation (`services/scorer.py`)
- Calculates priority score based on:
  - Visa type
  - Urgency score
  - Event date proximity
- Returns normalized score (0-1)

#### c. Message Rewriting (`services/rewriter.py`)
- Attempts to improve the message for better impact
- Uses template-based approach to generate optimized version
- Returns improved message text

#### d. Score Explanation (`services/xai.py`)
- Generates human-readable explanation of the score
- Explains why the request received its priority score

### 4. Response Flow
Backend sends response to frontend:
```json
{
    "initial_score": float,
    "final_score": float,
    "original_email": str,
    "best_email": str,
    "xai_explanation": str,
    "event_date": datetime or null
}
```

### 5. Frontend Display
- Shows results in expandable sections:
  - Priority Score with visual progress bar
  - Analysis Details
  - Optimized Message
  - Timestamp of processing

## Running the Application

### Prerequisites
- Docker
- Docker Compose

### Steps to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/us-visa-appointment-assistant.git
   cd us-visa-appointment-assistant
   ```

2. Build and run using Docker Compose:
   ```bash
   docker-compose up --build
   ```

3. Access the application:
   - Frontend: http://localhost:8501
   - Backend API: http://localhost:8000

### Testing the API
You can test the backend API directly using curl:
```bash
curl http://localhost:8000/api/process/ \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Test User",
    "email": "test@example.com",
    "visa_type": "F1",
    "message": "Need urgent appointment for university program starting next month"
  }'
```

## Architecture

The application uses a microservices architecture with:

1. **Frontend Service**
   - Streamlit web application
   - Handles user interface and input
   - Makes API calls to backend

2. **Backend Service**
   - FastAPI application
   - Processes requests through multiple services
   - Returns analyzed and optimized results

3. **Docker Configuration**
   - `Dockerfile.streamlit` for frontend
   - `Dockerfile` for backend
   - `docker-compose.yml` for orchestration

## Error Handling

The application includes error handling for:
- Missing form fields
- Backend connection issues
- API request failures
- Invalid input data

Each error is displayed to the user with appropriate messages and suggestions for resolution. 