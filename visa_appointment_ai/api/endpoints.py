from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.extractor import extract_details
from services.rewriter import rewrite_email
from services.scorer import calculate_score
from services.xai import explain_score

router = APIRouter()

class EmailRequest(BaseModel):
    full_name: str
    email: str
    visa_type: str
    message: str

@router.post("/process/")
def process_email(req: EmailRequest):
    try:
        extracted = extract_details(req.message, req.visa_type)
        score = calculate_score(
            visa_type=req.visa_type,
            urgency_hits=extracted["urgency_score"],
            event_date=extracted["event_date"]
        )
        
        rewritten_email = req.message
        best_score = score["total"] / 100  # Convert to 0-1 scale
        best_email = rewritten_email

        attempts = 0
        while best_score < 0.75 and attempts < 3:
            rewritten_email = rewrite_email(req.message, "Low urgency words used")
            temp = extract_details(rewritten_email, req.visa_type)
            temp_score = calculate_score(
                visa_type=req.visa_type,
                urgency_hits=temp["urgency_score"],
                event_date=temp["event_date"]
            )
            temp_score_normalized = temp_score["total"] / 100  # Convert to 0-1 scale
            if temp_score_normalized > best_score:
                best_score = temp_score_normalized
                best_email = rewritten_email
            attempts += 1

        explanation = explain_score(best_score, req.visa_type, extracted["urgency_score"])

        return {
            "initial_score": score["total"] / 100,  # Convert to 0-1 scale
            "final_score": best_score,
            "original_email": req.message,
            "best_email": best_email,
            "xai_explanation": explanation,
            "event_date": extracted["event_date"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
