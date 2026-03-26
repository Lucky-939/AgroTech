import os
import google.generativeai as genai
from django.conf import settings
from django.shortcuts import render
import joblib

genai.configure(api_key=settings.GEMINI_API_KEY)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model = joblib.load(os.path.join(BASE_DIR, 'crop_model.pkl'))

# Home Page
def home(request):
    return render(request, 'index.html')


def crop_form(request):
<<<<<<< HEAD
    return render(request, 'crop_predict.html')
=======
    return render(request, 'crop.html')
>>>>>>> 05f56bc7 (Initial commit for AgroTech)

def crop_result(request):
    if request.method == 'POST':
        data = [
            float(request.POST['N']),
            float(request.POST['P']),
            float(request.POST['K']),
            float(request.POST['temperature']),
            float(request.POST['humidity']),
            float(request.POST['ph']),
            float(request.POST['rainfall']),
        ]

        prediction = model.predict([data])[0]
        
        # Ask Gemini for a small advisory based on the crop
        prompt = f"""
        Act as a professional agronomist. 
        We have recommended '{prediction}' as the optimal crop for the user's soil.
        
        Provide a CONCISE cultivation advisory for {prediction}.
        Include exactly 3 short bullet points, each under 15 words:
        - Sowing time
        - Best practices
        - Expected yield
        """
        
<<<<<<< HEAD
        # Using gemma-3-1b-it for high-speed crop cultivation advisory
        gen_model = genai.GenerativeModel(
            model_name="gemma-3-1b-it",
            safety_settings=[
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
            ]
        )
        try:
            response = gen_model.generate_content(prompt, generation_config={"max_output_tokens": 200})
            if response.candidates and response.candidates[0].content.parts:
                advisory_text = response.candidates[0].content.parts[0].text.strip().replace('\n', '<br>')
            else:
                advisory_text = "Detailed AI advisory is currently unavailable due to filtering."
        except Exception as e:
            print(f"Crop Gemini Error: {e}")
            advisory_text = "Detailed AI advisory is currently unavailable."
        
        context = {
            'recomm': prediction, 
            'advisory': advisory_text,
            'temperature': request.POST.get('temperature', ''),
            'humidity': request.POST.get('humidity', ''),
            'location': 'Your Region'
        }
        return render(request, 'crop_predict.html', context)
=======
        gen_model = genai.GenerativeModel("gemini-2.5-flash")
        try:
            response = gen_model.generate_content(prompt)
            advisory_text = response.text
        except Exception as e:
            advisory_text = "Detailed AI advisory is currently unavailable."
        
        return render(request, 'result.html', {'crop': prediction, 'advisory': advisory_text})
>>>>>>> 05f56bc7 (Initial commit for AgroTech)
