import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_PATH = os.path.join(BASE_DIR, '..', 'datasets', 'Crop_recommendation.csv')

def train_model():
    df = pd.read_csv(DATASET_PATH)

    X = df.drop('label', axis=1)
    y = df['label']

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    joblib.dump(model, os.path.join(BASE_DIR, 'crop_model.pkl'))
