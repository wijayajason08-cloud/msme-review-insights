import joblib

from pain_point_categories import match_categories
from text_cleaning import clean_text_flat

MODEL_PATH = "models/sentiment_model.pkl"
VECTORIZER_PATH = "models/tfidf_vectorizer.pkl"

_model = None
_vectorizer = None


def load_model():
    """Load model sekali saja (lazy loading), supaya file tidak dibaca ulang
    setiap kali fungsi predict dipanggil."""
    global _model, _vectorizer
    if _model is None:
        _model = joblib.load(MODEL_PATH)
        _vectorizer = joblib.load(VECTORIZER_PATH)
    return _model, _vectorizer


def predict_sentiment(text: str):
    """Return (label, confidence). label: 'positif' atau 'negatif'.
    Label 1 = negatif (sesuai df["y"] = (rating <= 2) saat training)."""
    model, vectorizer = load_model()
    cleaned = clean_text_flat(text)
    X = vectorizer.transform([cleaned])
    proba = model.predict_proba(X)[0]  # urutan kolom: [P(positif=0), P(negatif=1)]
    pred = model.predict(X)[0]
    label = "negatif" if pred == 1 else "positif"
    confidence = float(proba[pred])
    return label, confidence


def detect_categories(text: str):
    """Return list kategori pain point yang cocok (bisa kosong, bisa lebih dari satu)."""
    cleaned = clean_text_flat(text)
    return match_categories(cleaned)


def analyze_feedback(text: str):
    """Fungsi utama dipanggil UI: gabungkan sentiment + kategori jadi satu hasil."""
    if not text or not text.strip():
        return {"error": "Teks tidak boleh kosong."}

    label, confidence = predict_sentiment(text)
    categories = detect_categories(text)

    return {
        "text": text,
        "sentiment": label,
        "confidence": confidence,
        "categories": categories,
    }