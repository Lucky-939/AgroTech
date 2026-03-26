from django.shortcuts import render, HttpResponse, get_object_or_404
from .models import Predictor

import os
import numpy as np
import pickle
import boto3
import requests
import markdown2

from botocore.exceptions import NoCredentialsError
from django.conf import settings

from keras.models import load_model
from keras.preprocessing.image import img_to_array, load_img
from io import BytesIO

# ✅ CORRECT GEMINI SDK
import google.generativeai as genai

# ------------------------------------------------
# CONFIGURE GEMINI
# ------------------------------------------------
genai.configure(api_key=settings.GEMINI_API_KEY)
gemini_model = genai.GenerativeModel("gemini-2.5-flash")

# ------------------------------------------------
# SIMPLE TEST VIEW
# ------------------------------------------------
def populate_predictor_model(request):
    return HttpResponse("Predictor model populated successfully.")

# ------------------------------------------------
# IMAGE PREPROCESSING
# ------------------------------------------------
def preprocess_image(image_url):
    response = requests.get(image_url)
    img = load_img(BytesIO(response.content), target_size=(64, 64))
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0
    return img_array

# ------------------------------------------------
# 🌱 CROP RECOMMENDATION
# ------------------------------------------------
def crop_recommend(request):

    if request.method in ["POST", "GET"]:
        try:
            N = float(request.POST.get("N") or request.GET.get("N"))
            P = float(request.POST.get("P") or request.GET.get("P"))
            K = float(request.POST.get("K") or request.GET.get("K"))
            ph = float(request.POST.get("ph") or request.GET.get("ph"))
            rainfall = float(request.POST.get("rainfall") or request.GET.get("rainfall"))

            model_path = os.path.join(
                settings.BASE_DIR,
                "static",
                "models",
                "crop_model.pkl"
            )

            with open(model_path, "rb") as file:
                model = pickle.load(file)

            prediction = model.predict([[N, P, K, ph, rainfall]])
            crop = prediction[0]

            return render(request, "crop_recomm.html", {
                "result": crop
            })

        except:
            return render(request, "crop_recomm.html", {
                "error": "Please enter all values correctly"
            })

    return render(request, "crop_recomm.html")


# ------------------------------------------------
# 🌿 DISEASE PREDICTION + GEMINI AI
# ------------------------------------------------
def predict_disease(request, plant_id):

    s3 = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION_NAME
    )

    BUCKET_NAME = settings.AWS_S3_BUCKET_NAME

    if request.method == "POST":

        predictor = get_object_or_404(Predictor, id=plant_id)
        photo = request.FILES.get("photo")

        if not photo:
            return render(request, "disease_predict.html", {
                "error": "No image uploaded"
            })

        try:
            # Upload image to S3
            s3.upload_fileobj(photo, BUCKET_NAME, photo.name)
            photo_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{photo.name}"

            # Preprocess
            img = preprocess_image(photo_url)

            # Load ML model
            model_path = predictor.model_path.lstrip("../static/")
            labels_path = predictor.labels_path.lstrip("../static/")

            model_full_path = os.path.join(settings.BASE_DIR, model_path)
            labels_full_path = os.path.join(settings.BASE_DIR, labels_path)

            model = load_model(model_full_path)
            labels = np.load(labels_full_path, allow_pickle=True)

            prediction = model.predict(img)
            predicted_label = labels[np.argmax(prediction)]

            # Delete image from S3
            s3.delete_object(Bucket=BUCKET_NAME, Key=photo.name)

            # -----------------------------------
            # GEMINI AI RESPONSE
            # -----------------------------------
            crop = predictor.plant_name
            disease = str(predicted_label)

            prompt = f"""
You are an agricultural expert.

Provide:

1. Treatment steps
2. Organic solution
3. Chemical solution
4. Prevention tips

for {disease} disease in {crop}.
"""

            response = gemini_model.generate_content(prompt)

            html_content = markdown2.markdown(response.text)

            return render(request, "disease_predict.html", {
                "solution": html_content,
                "disease": disease
            })

        except NoCredentialsError:
            return render(request, "disease_predict.html", {
                "error": "AWS credentials not configured"
            })

        except Exception as e:
            print("ERROR:", e)
            return render(request, "disease_predict.html", {
                "error": str(e)
            })

    return render(request, "disease_predict.html")
