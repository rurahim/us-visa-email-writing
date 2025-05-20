# services/extractor.py

from datetime import datetime
import re
from typing import Dict, Optional

def extract_details(message: str, visa_type: str) -> Dict:
    # Extract date
    date_pattern = r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{1,2}"
    date_match = re.search(date_pattern, message, re.IGNORECASE)
    event_date = None

    if date_match:
        try:
            event_date = datetime.strptime(date_match.group(), "%B %d")
        except ValueError:
            try:
                event_date = datetime.strptime(date_match.group(), "%b %d")
            except ValueError:
                pass

    # Heuristic urgency score
    urgency_keywords = ["urgent", "immediately", "as soon as possible", "emergency", "soon", "delay"]
    urgency_score = sum(word in message.lower() for word in urgency_keywords)

    return {
        "event_date": event_date,
        "urgency_score": urgency_score,
        "original_message": message
    }
