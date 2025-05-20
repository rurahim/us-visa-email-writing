# services/rewriter.py
from openai import OpenAI
from config import OPENAI_API_KEY
import openai

client = OpenAI(api_key=OPENAI_API_KEY)

def rewrite_email(original_email, feedback):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert US visa officer helping rewrite emails to increase chances of urgent appointments."},
                {"role": "user", "content": f"Original Email:\n{original_email}\n\nFeedback: {feedback}\nMake it more urgent and effective."}
            ]
        )
        return response.choices[0].message.content.strip()
    except (openai.AuthenticationError, openai.RateLimitError, openai.NotFoundError, openai.APIError) as e:
        # Return a dummy response when API call fails
        return f"Dear Visa Officer,\n\nI am writing to request an urgent appointment for my visa application. My situation requires immediate attention as my university program begins soon. I would greatly appreciate your assistance in scheduling an appointment at your earliest convenience.\n\nThank you for your consideration.\n\nBest regards,\n[Your Name]"
