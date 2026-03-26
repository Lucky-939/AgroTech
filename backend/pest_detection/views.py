import os
import google.generativeai as genai
from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import predict_pest
from .models import PestPrediction
import joblib

# Configure Gemini with the API Key for agricultural advisory
genai.configure(api_key=settings.GEMINI_API_KEY)

def pest_detect_home(request):
    """
    Renders the Pest Detection page.
    Handles form submission and returns the combined result.
    """
    context = {}
    
    if request.method == "POST" and request.FILES.get("photo"):
        img = request.FILES["photo"]
        selected_lang = request.POST.get("language", "English")
        
        # Ensure media directory exists
        os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
        file_path = os.path.join(settings.MEDIA_ROOT, img.name)
        
        # Save file local context
        with open(file_path, "wb+") as f:
            for chunk in img.chunks():
                f.write(chunk)
                
        try:
            # Step 1: Predict using ML model
            prediction, confidence = predict_pest(file_path)
            
            # Step 2: Comprehensive Fallback Advisory (used when AI fails)
            # Standard English for fallback, could be localized later
            fallback_advisory = {
                "Healthy": [
                    "<b>Nutrient Balance:</b> Continue with current nitrogen application.",
                    "<b>Water Management:</b> Maintain shallow water (2-3 cm).",
                    "<b>Preventive:</b> Regular scouting for early signs."
                ],
                "Pest Infected": [
                    "<b>Immediate Action:</b> Isolate infected plants.",
                    "<b>Chemical Control:</b> Apply Imidacloprid (0.1%).",
                    "<b>Strengthening:</b> Apply Potash-rich fertilizer."
                ]
            }
            
            # Step 3: Generate Gemini AI advisory [Localized Version]
            prompt = f"""
            Act as an agricultural expert. We detected '{prediction}' in a paddy crop.
            
            PROVIDE THE RESPONSE ENTIRELY IN {selected_lang}.
            
            Structure the response as 2 concise bullet points on:
            1. Treatment or maintenance.
            2. Advice to improve leaf quality.
            
            Keep the tone professional and helpful for a farmer.
            """
            
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
                    raise Exception("Filtered")
            except:
                # Better fallback display
                tips = fallback_advisory.get(prediction, ["Consult local agronomist."])
                advisory_text = "<br>".join([f"• {t}" for t in tips])
            
            # Step 4: Save result to database
            PestPrediction.objects.create(
                image_name=img.name,
                prediction=prediction,
                confidence=confidence,
                advisory=advisory_text
            )

            context["result"] = {
                "prediction": prediction,
                "confidence": confidence,
                "image_url": f"{settings.MEDIA_URL}{img.name}",
                "advisory": advisory_text
            }
                
        except Exception as e:
            import traceback
            print(f"Prediction Error: {traceback.format_exc()}")
            context["error"] = "Error processing image. Please ensure it's a clear paddy leaf image."
            
    return render(request, "pest_detection.html", context)

@csrf_exempt
def api_pest_detect(request):
    """
    REST API endpoint for prediction.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Only POST requests allowed"}, status=405)
        
    if not request.FILES.get("photo"):
        return JsonResponse({"error": "No image provided"}, status=400)
        
    img = request.FILES["photo"]
    file_path = os.path.join(settings.MEDIA_ROOT, img.name)
    
    with open(file_path, "wb+") as f:
        for chunk in img.chunks():
            f.write(chunk)
            
    try:
        prediction, confidence = predict_pest(file_path)
        
        # Advisory for API users
        prompt = f"Detected {prediction} in paddy crop. Suggest treatment."
        gen_model = genai.GenerativeModel("gemma-3-1b-it")
        
        try:
            res = gen_model.generate_content(prompt)
            advisory = res.text if res.text else ""
        except:
            advisory = "Advisory unavailable."
            
        # Log to DB
        PestPrediction.objects.create(
            image_name=img.name,
            prediction=prediction,
            confidence=confidence,
            advisory=advisory
        )
            
        return JsonResponse({
            "status": "success",
            "prediction": prediction,
            "confidence": confidence,
            "advisory": advisory
        })
        
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
