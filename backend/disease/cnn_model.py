import numpy as np
import os
import threading

model_path = os.path.join(os.path.dirname(__file__), "model1.h5")

# Thread-safe lazy loading
_model = None
_model_lock = threading.Lock()

def _get_model():
    global _model
    if _model is None:
        with _model_lock:
            if _model is None:
                try:
                    from tensorflow.keras.models import load_model
                    print(f"[AI] Initializing CNN model from {model_path}...")
                    _model = load_model(model_path)
                    print("[AI] Model loaded successfully.")
                except Exception as e:
                    print(f"[AI] CRITICAL ERROR loading model: {e}")
                    return None
    return _model


# Standard PlantVillage labels (Mapped to 20 classes)
class_names = [
    "Apple Scab",
    "Apple Black Rot",
    "Apple Cedar Rust",
    "Apple Healthy",
    "Corn Cercospora Leaf Spot",
    "Corn Common Rust",
    "Corn Northern Leaf Blight",
    "Corn Healthy",
    "Grape Black Rot",
    "Grape Esca",
    "Grape Leaf Blight",
    "Grape Healthy",
    "Potato Early Blight",
    "Potato Late Blight",
    "Potato Healthy",
    "Tomato Bacterial Spot",
    "Tomato Early Blight",
    "Tomato Late Blight",
    "Tomato Leaf Mold",
    "Tomato Healthy"
]


def predict_disease(img_path):
    from tensorflow.keras.preprocessing import image

    model = _get_model()
    if model is None:
        raise RuntimeError("CNN Model could not be initialized. Please check server logs.")

    # Reverted to 227x227 as the model architecture expects this specific input volume
    img = image.load_img(img_path, target_size=(227, 227)) 
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # Verbose=0 to prevent stdout cluttering
    predictions = model.predict(img_array, verbose=0)

    predicted_index = int(np.argmax(predictions))
    confidence = float(np.max(predictions)) * 100

    print(f"[AI] Inference Result - Index: {predicted_index} | Confidence: {confidence:.1f}%")

    if predicted_index < len(class_names):
        predicted_class = class_names[predicted_index]
    else:
        predicted_class = f"Unknown Index ({predicted_index})"

    recommendation = get_recommendation(predicted_class)

    return predicted_class, recommendation, round(confidence, 2)


def get_recommendation(disease):
    recommendations = {
        "Scab": "Use fungicides containing captan or myclobutanil.",
        "Black Rot": "Prune out dead or diseased wood. Apply fungicide.",
        "Cedar Rust": "Apply protective fungicides. Remove nearby cedar trees.",
        "Cercospora": "Use resistant hybrids. Apply foliar fungicide if severe.",
        "Common Rust": "Apply fungicide early and use resistant corn varieties.",
        "Northern Leaf Blight": "Rotate crops, manage residue, and use resistant varieties.",
        "Esca": "Remove affected parts. Prune only in dry weather.",
        "Leaf Blight": "Improve air circulation. Remove infected foliage.",
        "Bacterial Spot": "Use copper-based bactericide. Avoid overhead watering.",
        "Early Blight": "Remove infected leaves and apply fungicide containing chlorothalonil or copper.",
        "Late Blight": "Apply protectant fungicides immediately. Destroy infected plants.",
        "Leaf Mold": "Reduce humidity and improve greenhouse ventilation.",
        "Healthy": "No treatment needed. Maintain regular monitoring."
    }

    # Case-insensitive substring matching
    for key, val in recommendations.items():
        if key.lower() in disease.lower():
            return val

    return "Refer to the AI advisory for detailed treatment steps."
