# services/scorer.py

from datetime import datetime
from models.visa_type import VISA_WEIGHTS

def calculate_score(visa_type: str, urgency_hits: int, event_date=None):
    """
    Calculate priority score based on visa type, urgency keyword hits, and how close the event is.
    """
    base = VISA_WEIGHTS.get(visa_type.upper(), 0.5) * 100

    urgency_boost = 0
    if event_date:
        if isinstance(event_date, str):
            try:
                event_date = datetime.fromisoformat(event_date)
            except ValueError:
                return {
                    "error": f"Invalid date format: {event_date}. Expected ISO format like '2025-06-01T00:00:00'"
                }

        if isinstance(event_date, datetime):
            days_left = (event_date - datetime.now()).days
            urgency_boost = max(0, (30 - days_left)) * 2

    keyword_boost = urgency_hits * 5
    total = min(100, base + urgency_boost + keyword_boost)

    return {
        "base": base,
        "urgency": urgency_boost,
        "keywords": keyword_boost,
        "total": total
    }
