from django.conf import settings
import django
import os
import google.generativeai as genai

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "agrotech.settings")
django.setup()

API_KEY = settings.GEMINI_API_KEY
print(f"Testing Gemini with key: {API_KEY[:8] if API_KEY else 'None'}...")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

try:
    response = model.generate_content("Say hello!")
    print("Success:", response.text)
except Exception as e:
    print("Error:", str(e))
