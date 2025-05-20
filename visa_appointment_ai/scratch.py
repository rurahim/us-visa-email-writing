from services.rewriter import rewrite_email

email = "I am a student. My university starts soon. Please help."
feedback = "Low urgency words used."
print(rewrite_email(email, feedback))
