# 🌱 AgroTech — Smart Agriculture Platform

> Empowering farmers with AI-driven crop predictions and data-backed farming insights.

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.x-092E20?style=flat-square&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Gemini AI](https://img.shields.io/badge/Google-Gemini%20AI-4285F4?style=flat-square&logo=google&logoColor=white)](https://ai.google.dev/)
[![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![SCSS](https://img.shields.io/badge/SCSS-CC6699?style=flat-square&logo=sass&logoColor=white)](https://sass-lang.com/)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen?style=flat-square)](LICENSE)

---

**AgroTech** is an intelligent web platform built to modernize Indian agriculture. It combines a Django-powered backend, a curated ML crop predictor, and **Google Gemini AI** to deliver real-time, natural-language farming advice — putting the power of data science directly in the hands of farmers.

---

## 📌 Table of Contents

- [✨ Features](#-features)
- [🗂️ Project Structure](#️-project-structure)
- [🛠️ Tech Stack](#️-tech-stack)
- [🤖 Google Gemini AI Integration](#-google-gemini-ai-integration)
- [⚙️ Installation](#️-installation)
- [🔑 Environment Configuration](#-environment-configuration)
- [🚀 Usage](#-usage)
- [🌿 How the Predictor Works](#-how-the-predictor-works)
- [📁 Dataset Schema](#-dataset-schema)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

## ✨ Features

| Module | Description |
|---|---|
| 🌾 **Crop Predictor** | ML-powered engine recommending the best crop based on soil & climate inputs |
| 🤖 **Gemini AI Advisor** | Google Gemini API provides natural-language farming tips, fertilizer advice, and pest control guidance |
| 📊 **Smart Datasets** | Curated agricultural datasets covering soil nutrients, rainfall, temperature, and humidity |
| 🖥️ **Responsive Dashboard** | Clean, mobile-friendly UI built with HTML5, SCSS, and vanilla JavaScript |
| ⚙️ **Django Backend** | Robust server-side logic handling predictions, routing, and data processing |
| 🔒 **Secure Architecture** | Environment-based configuration, Django ORM, and modular app design |

---

## 🗂️ Project Structure

```
AgroTech/
│
├── Predictor/             # ML model logic — crop prediction engine
│   └── ...                # Saved models (.pkl / .joblib), inference scripts
│
├── backend/               # Django app — views, URLs, models, forms
│   └── ...
│
├── datasets/              # Raw & processed agricultural datasets (.csv)
│   └── ...
│
├── static/                # Static assets — CSS, SCSS, JavaScript, images
│   ├── css/
│   ├── js/
│   └── images/
│
├── templates/             # Django HTML templates — pages and partials
│   └── ...
│
├── manage.py              # Django management entry point
├── requirements.txt       # Python dependencies
├── .gitignore
└── README.md
```

---

## 🛠️ Tech Stack

**Backend**
- [Python 3.10+](https://www.python.org/)
- [Django](https://www.djangoproject.com/) — web framework
- [scikit-learn](https://scikit-learn.org/) — ML crop predictor
- [Pandas & NumPy](https://pandas.pydata.org/) — data processing
- [Google Gemini API](https://ai.google.dev/) — generative AI farming advisor

**Frontend**
- HTML5, SCSS / CSS3, JavaScript (ES6+)
- Django Templating Engine

**Data**
- Custom curated CSV datasets (soil nutrients, weather parameters, crop labels)

---

## 🤖 Google Gemini AI Integration

AgroTech uses the **Google Gemini API** to provide farmers with intelligent, conversational farming advice — going beyond simple predictions.

### What Gemini Powers in AgroTech

- 🌿 **Fertilizer Recommendations** — Based on soil nutrient levels (N, P, K), Gemini suggests organic and chemical fertilizer options in plain language
- 🐛 **Pest & Disease Guidance** — Farmers can describe symptoms and Gemini returns actionable pest control advice
- 🌦️ **Climate-Aware Tips** — Seasonal and weather-aware crop care suggestions tailored to local conditions
- 💬 **Natural Language Interface** — Farmers interact with the platform conversationally, not just through forms

### How It Works

```
Farmer Input (soil data / question)
        │
        ▼
  Django Backend receives request
        │
        ▼
  Prompt constructed with farming context
        │
        ▼
  Google Gemini API call (gemini-pro model)
        │
        ▼
  AI-generated advice returned to UI
```

### Setting Up Your Gemini API Key

1. Visit [https://ai.google.dev/](https://ai.google.dev/) and sign in with your Google account
2. Click **"Get API Key"** → **"Create API Key in new project"**
3. Copy the generated key
4. Add it to your `.env` file as shown in the [Environment Configuration](#-environment-configuration) section below

> ⚠️ **Never commit your API key to version control.** Always use environment variables.

---

## ⚙️ Installation

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Git
- A Google Gemini API key ([get one free here](https://ai.google.dev/))

### Step 1 — Clone the Repository

```bash
git clone https://github.com/Lucky-939/AgroTech.git
cd AgroTech
```

### Step 2 — Create a Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate on Linux / macOS
source venv/bin/activate

# Activate on Windows
venv\Scripts\activate
```

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Configure Environment Variables

Create a `.env` file in the project root (see [Environment Configuration](#-environment-configuration) below).

### Step 5 — Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6 — Run the Development Server

```bash
python manage.py runserver
```

Visit: **http://127.0.0.1:8000/**

---

## 🔑 Environment Configuration

Create a `.env` file in the root of the project with the following variables:

```env
# Django
SECRET_KEY=your_django_secret_key_here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# Google Gemini AI
GEMINI_API_KEY=your_google_gemini_api_key_here
```

> 💡 **Tip:** Generate a Django secret key using:
> ```bash
> python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
> ```

Make sure `.env` is listed in your `.gitignore` — **never push API keys to GitHub**.

---

## 🚀 Usage

1. **Open** your browser and go to `http://127.0.0.1:8000/`
2. **Enter** your field parameters — nitrogen (N), phosphorus (P), potassium (K), temperature, humidity, pH, and rainfall
3. **Submit** to get an instant ML-based crop recommendation
4. **Ask Gemini** — use the AI advisor to get fertilizer tips, pest control advice, or farming guidance in natural language
5. **Explore** the dashboard to understand why a specific crop is recommended for your local conditions

---

## 🌿 How the Predictor Works

```
User Input (Soil + Climate Parameters)
        │
        ▼
  Feature Preprocessing
  (Normalization / Encoding)
        │
        ▼
  Trained ML Model
  (Random Forest / Decision Tree)
        │
        ▼
  Crop Recommendation Output
  e.g., "Rice", "Wheat", "Cotton"
        │
        ▼
  Gemini AI adds natural-language advice
  e.g., "Apply urea fertilizer before sowing..."
```

The `Predictor/` module contains the pre-trained model, label encoders, and the Python inference script. The Django backend calls this module to serve predictions, then passes context to Gemini for enriched AI guidance.

---

## 📁 Dataset Schema

The `datasets/` folder contains curated agricultural data with the following feature columns:

| Column | Description | Unit |
|---|---|---|
| `N` | Nitrogen content in soil | mg/kg |
| `P` | Phosphorus content in soil | mg/kg |
| `K` | Potassium content in soil | mg/kg |
| `temperature` | Average ambient temperature | °C |
| `humidity` | Relative humidity | % |
| `ph` | Soil pH value | 0–14 scale |
| `rainfall` | Annual rainfall | mm |
| `label` | Recommended crop (target variable) | crop name |

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

```bash
# 1. Fork the repository on GitHub

# 2. Clone your fork
git clone https://github.com/YOUR-USERNAME/AgroTech.git

# 3. Create a new feature branch
git checkout -b feature/your-feature-name

# 4. Make your changes and commit
git add .
git commit -m "feat: describe your change here"

# 5. Push to your fork and open a Pull Request
git push origin feature/your-feature-name
```

Please follow [PEP 8](https://peps.python.org/pep-0008/) for Python code and include comments where needed.

### 🐛 Reporting Issues

Found a bug or have a suggestion? [Open an issue](https://github.com/Lucky-939/AgroTech/issues) with:
- A clear description of the problem
- Steps to reproduce it
- Expected vs. actual behaviour
- Screenshots if applicable

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

*Made with ❤️ for Indian Farmers — [Lucky-939](https://github.com/Lucky-939)*
