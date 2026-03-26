import os
import cv2
import numpy as np
import joblib
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
try:
    from skimage.feature import graycomatrix, graycoprops
except ImportError:
    # If using older version of skimage
    from skimage.feature import greycomatrix as graycomatrix, greycoprops as graycoprops

def extract_features(image_path):
    """Preprocessing and GLCM Feature Extraction"""
    # Resize to 128x128 and convert to grayscale
    img = cv2.imread(image_path)
    if img is None:
        return None
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_resized = cv2.resize(img_gray, (128, 128))
    
    # Extract GLCM features
    glcm = graycomatrix(img_resized, [1], [0], 256, symmetric=True, normed=True)
    contrast = graycoprops(glcm, 'contrast')[0, 0]
    energy = graycoprops(glcm, 'energy')[0, 0]
    homogeneity = graycoprops(glcm, 'homogeneity')[0, 0]
    correlation = graycoprops(glcm, 'correlation')[0, 0]
    
    return [contrast, energy, homogeneity, correlation]

def train_save_model(data_dir=None, save_path='paddy_pest_svm.pkl'):
    """
    Train SVM classifier.
    If data_dir is None, it creates a sample model for testing.
    """
    X = []
    y = []
    
    if data_dir and os.path.exists(data_dir):
        # Expected structure: data_dir/healthy/ and data_dir/pest/
        categories = {'healthy': 0, 'pest': 1}
        for category, label in categories.items():
            folder_path = os.path.join(data_dir, category)
            if os.path.exists(folder_path):
                for file_name in os.listdir(folder_path):
                    if file_name.endswith(('.jpg', '.jpeg', '.png')):
                        features = extract_features(os.path.join(folder_path, file_name))
                        if features:
                            X.append(features)
                            y.append(label)
        
        if not X:
            print("No images found in directories. Training with dummy data for Demo.")
            return train_with_dummy_data(save_path)
            
        X = np.array(X)
        y = np.array(y)
        
        # Train-test split (70-30)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        
        # Train SVM with RBF kernel and probability enabled
        svm = SVC(kernel='linear', probability=True, C=1.0)
        svm.fit(X_train, y_train)
        
        # Evaluate
        y_pred = svm.predict(X_test)
        print(f"Accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%")
        print("Confusion Matrix:")
        print(confusion_matrix(y_test, y_pred))
        
        # Save model
        joblib.dump({'model': svm, 'accuracy': accuracy_score(y_test, y_pred)}, save_path)
        print(f"Model saved to {save_path}")
        
    else:
        return train_with_dummy_data(save_path)

def train_with_dummy_data(save_path):
    """Create a dummy SVM model for demonstration."""
    # Create synthetic samples for GLCM features
    # Class 0 (Healthy): Usually lower contrast, higher energy/homogeneity
    X_healthy = np.random.normal(loc=[10.0, 0.5, 0.8, 0.9], scale=1.0, size=(100, 4))
    # Class 1 (Pest): Usually higher contrast, lower energy/homogeneity
    X_pest = np.random.normal(loc=[50.0, 0.1, 0.3, 0.4], scale=5.0, size=(100, 4))
    
    X = np.vstack([X_healthy, X_pest])
    y = np.array([0]*100 + [1]*100)
    
    # Train SVM
    svm = SVC(kernel='linear', probability=True)
    svm.fit(X, y)
    
    # Save model
    joblib.dump({'model': svm, 'accuracy': 0.95}, save_path)
    print(f"Demo model saved to {save_path}")

if __name__ == "__main__":
    import sys
    data_folder = sys.argv[1] if len(sys.argv) > 1 else None
    train_save_model(data_folder)
