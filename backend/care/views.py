import google.generativeai as genai
from django.conf import settings
from django.shortcuts import render

# Configure Gemini with your API Key
genai.configure(api_key=settings.GEMINI_API_KEY)

def care_advisory(request):
    advisory_text = ""

    if request.method == "POST":
        crop = request.POST.get("crop")
        soil = request.POST.get("soil")
        disease = request.POST.get("disease")

        # The prompt is now strictly formatted for your "Short Info" request
        prompt = f"""
        Act as a professional agronomist. Provide a CONCISE care advisory for:
        Crop: {crop} | Soil: {soil} | Condition: {disease}

        Provide exactly 4 bullet points, each under 15 words:
        - Fertilizer: [Best nutrient mix]
        - Irrigation: [Watering schedule]
        - Treatment: [Immediate cure for {disease}]
        - Prevention: [Long-term protection]
        """

        # Ensure you use 'gemini-1.5-flash' for stable performance
<<<<<<< HEAD
        model = genai.GenerativeModel("gemma-3-1b-it")
=======
        model = genai.GenerativeModel("gemini-2.5-flash")
>>>>>>> 05f56bc7 (Initial commit for AgroTech)

        try:
            response = model.generate_content(prompt)
            advisory_text = response.text
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print("GEMINI ERROR:", error_details)
            advisory_text = "Analysis service temporarily unavailable. Error: " + str(e)


<<<<<<< HEAD
    context = {}
    if advisory_text:
        context["solution"] = advisory_text
    return render(request, "care_advisor.html", context)
=======
    return render(request, "care/advisory.html", {"advisory": advisory_text})
>>>>>>> 05f56bc7 (Initial commit for AgroTech)
