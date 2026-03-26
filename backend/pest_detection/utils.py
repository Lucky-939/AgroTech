import cv2
import numpy as np
import os
import joblib
from skimage.feature import graycomatrix, graycoprops
from django.conf import settings

# Path to the trained SVM model
MODEL_PATH = os.path.join(settings.BASE_DIR, 'pest_detection', 'paddy_pest_svm.pkl')

def extract_glcm_features(image_path):
    """
    Extracts GLCM features (Contrast, Energy, Homogeneity, Correlation) from an image.
    """
    # Step 1: Preprocessing - RGB -> Grayscale and Resize to 128x128
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Could not read image")
    
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_resized = cv2.resize(img_gray, (128, 128))
    
    # Step 2: GLCM Feature Extraction
    # Distance: 1, Angle: 0 (horizontal)
    glcm = graycomatrix(img_resized, [1], [0], 256, symmetric=True, normed=True)
    
    contrast = graycoprops(glcm, 'contrast')[0, 0]
    energy = graycoprops(glcm, 'energy')[0, 0]
    homogeneity = graycoprops(glcm, 'homogeneity')[0, 0]
    correlation = graycoprops(glcm, 'correlation')[0, 0]
    
    return [contrast, energy, homogeneity, correlation]

def predict_pest(image_path):
    """
    Predicts if the paddy leaf is Healthy or Pest Infected using the SVM model.
    """
    # Ensure model exists
    if not os.path.exists(MODEL_PATH):
        return "Model not found", 0.0
        
    # Load model
    model_data = joblib.load(MODEL_PATH)
    svm_model = model_data['model']
    
    # Extract features
    features = extract_glcm_features(image_path)
    features_reshaped = np.array(features).reshape(1, -1)
    
    # Prediction
    prediction_idx = svm_model.predict(features_reshaped)[0]
    
    # Get probability if available
    try:
        probabilities = svm_model.predict_proba(features_reshaped)[0]
        confidence = float(np.max(probabilities)) * 100
    except:
        confidence = 100.0 # Fallback if probability is not enabled
        
    label = "Pest Infected" if prediction_idx == 1 else "Healthy"
    
    return label, round(confidence, 2)
