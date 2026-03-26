<<<<<<< HEAD
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse("Welcome to AgriDoctor!")

def index_view(request):
    return render(request, 'index.html')
=======
from django.shortcuts import render, redirect
from django.http import JsonResponse
import requests, joblib, numpy as np, os
from django.conf import settings
# 
# from google import genai
import google.generativeai as genai

from django.conf import settings

from google.api_core.exceptions import ResourceExhausted
import markdown2


# 🌱 Home Page
def home(request):
    if request.method == 'POST':
        return redirect(
            f"/crop-recomm/?N={request.POST.get('nitrogen')}"
            f"&P={request.POST.get('phosphorus')}"
            f"&K={request.POST.get('potassium')}"
            f"&ph={request.POST.get('ph')}"
            f"&rainfall={request.POST.get('rainfall')}"
        )
    return render(request, 'index.html')


# 🌱 Crop Recommendation
def predict_crop(request):
    try:
        N = int(request.GET.get('N', 0))
        P = int(request.GET.get('P', 0))
        K = int(request.GET.get('K', 0))
        ph = float(request.GET.get('ph', 6.5))
        rainfall = float(request.GET.get('rainfall', 200))

        location = "Pune"
        weather_url = (
            f"http://api.openweathermap.org/data/2.5/weather"
            f"?q={location}&appid={settings.OPENWEATHER_API_KEY}&units=metric"
        )

        weather = requests.get(weather_url).json()
        temperature = weather.get('main', {}).get('temp', 25)
        humidity = weather.get('main', {}).get('humidity', 70)

        model_path = os.path.join(settings.BASE_DIR, 'static', 'RandomForest.pkl')
        model = joblib.load(model_path)

        data = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
        prediction = model.predict(data)[0]

        return render(request, 'crop_predict.html', {
            'recomm': prediction,
            'temperature': temperature,
            'humidity': humidity,
            'location': location
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# 🌱 Crop Care Advisor — Gemini 2.5 Flash (CORRECT)
def care_advisor(request):
    if request.method == 'POST':
        crop = request.POST.get('planted_crop')

        try:
            # ✅ NEW WAY (Client-based)
            client = genai.Client(api_key=settings.GEMINI_API_KEY)

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=f"""
                You are an agricultural expert.
                Give simple and practical crop care guidance for {crop}.

                Include:
                - Soil and pH
                - Watering
                - Fertilizer
                - Pests and diseases
                - Harvesting tips

                Use simple language for farmers.
                """
            )

            html = markdown2.markdown(response.text)

        except ResourceExhausted:
            html = """
            <h3>⚠ AI Quota Exceeded</h3>
            <p>Please try again later.</p>
            """

        except Exception as e:
            html = f"<p>Error: {str(e)}</p>"

        return render(request, 'care_advisor.html', {'solution': html})

    return render(request, 'care_advisor.html')
>>>>>>> 05f56bc7 (Initial commit for AgroTech)
