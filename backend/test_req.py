import os
import django

import google.generativeai as genai

# Setup Django minimal
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agrotech.settings')
django.setup()

from django.conf import settings

print(f"Using KEY: {settings.GEMINI_API_KEY[:10]}...")
genai.configure(api_key=settings.GEMINI_API_KEY)

try:
    model = genai.GenerativeModel("gemini-2.5-flash")
    prompt = "testing"
    response = model.generate_content(prompt)
    print("gemini-2.5-flash RESPONSE:", response.text)
except Exception as e:
    import traceback
    print("ERROR with 2.5-flash:", traceback.format_exc())

try:
    model2 = genai.GenerativeModel("gemini-1.5-flash")
    response2 = model2.generate_content("testing")
    print("gemini-1.5-flash RESPONSE:", response2.text)
except Exception as e:
    print("ERROR with 1.5-flash:", str(e))
