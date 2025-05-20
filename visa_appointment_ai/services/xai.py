def explain_score(score: float, visa_type: str, urgency_score: float) -> str:
    explanation = []

    if visa_type.lower() == "medical":
        explanation.append("Medical visas are treated as top priority.")
    elif visa_type.lower().startswith("f"):
        explanation.append("Student visas (e.g., F1) are prioritized if the session start date is near.")
    elif visa_type.lower().startswith("b"):
        explanation.append("Business/tourist visas have lower priority unless a specific urgent event is near.")
    else:
        explanation.append(f"Visa type '{visa_type}' has moderate priority.")

    if urgency_score >= 0.9:
        explanation.append("The email uses highly urgent language.")
    elif urgency_score >= 0.6:
        explanation.append("The email reflects moderate urgency.")
    else:
        explanation.append("The email lacks urgency, which affects priority.")

    if score >= 0.85:
        explanation.append("Overall, this request is likely to get an early appointment.")
    elif score >= 0.65:
        explanation.append("This request has a fair chance, but could be improved.")
    else:
        explanation.append("Low likelihood for early appointment due to missing urgency or timing.")

    return " ".join(explanation)
