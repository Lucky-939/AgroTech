import os
import google.generativeai as genai
from django.conf import settings
from django.shortcuts import render
from .cnn_model import predict_disease

# Configure Gemini with the API Key for agricultural advisory
genai.configure(api_key=settings.GEMINI_API_KEY)

def disease_home(request, id=None):
    context = {}

    if request.method == "POST" and request.FILES.get("photo"):
        img = request.FILES["photo"]

        # Ensure media directory exists for file handling
        os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
        file_path = os.path.join(settings.MEDIA_ROOT, img.name)

        # Persistence: Save the file locally before prediction
        with open(file_path, "wb+") as f:
            for chunk in img.chunks():
                f.write(chunk)

        try:
            # Step 1: Execute CNN Inference (local)
            disease, recommendation, confidence = predict_disease(file_path)

            context["result"] = {
                "disease": disease,
                "recommendation": recommendation,
                "confidence": confidence
            }

            # Step 2: Leverage Gemini for expert advisory (remote)
            prompt = f"""
            Act as a professional plant pathologist. 
            A user has uploaded a leaf image and our local model detected the disease '{disease}' with {confidence}% confidence. 
            The primary recommendation is '{recommendation}'.
            
            Provide a CONCISE expert advisory. 
            Include exactly 3 short bullet points, each under 15 words:
            - Treatment (chemical or organic)
            - Prevention for next cycle
            - Next step for the farmer
            """

            # Using gemma-3-1b-it to ensure available quota and fast expert agriculture advisory
            genai_model = genai.GenerativeModel(
                model_name="gemma-3-1b-it",
                safety_settings=[
                    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
                ]
            )
            
            try:
                response = genai_model.generate_content(prompt, generation_config={"max_output_tokens": 200})
                
                # Robust text extraction to avoid "No text candidate" errors
                if response.candidates and response.candidates[0].content.parts:
                    raw_text = response.candidates[0].content.parts[0].text
                    advisory_html = raw_text.strip().replace('\n', '<br>')
                else:
                    advisory_html = "Response was filtered. Please refer to primary recommendation."
                
                context["result"]["advisory"] = advisory_html
            except Exception as e:
                print(f"Gemini API failure: {e}")
                context["result"]["advisory"] = "Detailed AI advisory is currently unavailable. Please follow the primary recommendation below."
                
            # Rendered HTML string (backward compatibility with legacy template tags if any)
            context["solution"] = f"<div class='text-start'><h4>Disease: {disease}</h4><p>Confidence: {confidence}%</p><p>Primary: {recommendation}</p></div>"

        except Exception as e:
            import traceback
            print(f"Prediction Error: {traceback.format_exc()}")
            context["error"] = "We couldn't process this photo. Please try a clearer leaf image with better lighting."

    return render(request, "disease_predict.html", context)

