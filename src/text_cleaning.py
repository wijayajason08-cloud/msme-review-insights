import re

from id_stopwords import STOPWORDS

STOPWORD_SET = set(STOPWORDS)
CLAUSE_SPLIT_PATTERN = re.compile(r"[.,!?;]+")

SLANG_DICT = {
    "gk": "tidak", "ga": "tidak", "gak": "tidak", "nggak": "tidak", "ngga": "tidak", "tdk": "tidak",
    "bgt": "banget", "yg": "yang", "udh": "sudah", "udah": "sudah",
    "tp": "tapi", "sy": "saya", "aq": "aku", "gw": "saya", "gua": "saya",
    "dr": "dari", "krn": "karena", "karna": "karena", "jd": "jadi",
    "utk": "untuk", "dgn": "dengan", "bs": "bisa", "trs": "terus",
    "sm": "sama", "gmn": "bagaimana", "knp": "kenapa",
    "aja": "saja", "emg": "memang", "emang": "memang",
}


def normalize_slang(text: str) -> str:
    return " ".join(SLANG_DICT.get(w, w) for w in text.split())


def remove_stopwords(text: str) -> str:
    return " ".join(w for w in text.split() if w not in STOPWORD_SET)


def clean_clause(clause: str) -> str:
    clause = re.sub(r"[^a-z\s]", " ", clause)
    clause = re.sub(r"\s+", " ", clause).strip()
    clause = normalize_slang(clause)
    clause = remove_stopwords(clause)
    return clause


def clean_text_with_clauses(text: str) -> str:
    """Pecah jadi klausa berdasar tanda baca asli, bersihkan tiap klausa,
    gabung kembali dengan '|' (dipakai untuk analisis bigram sadar-klausa)."""
    text = str(text).lower()
    text = re.sub(r"http\S+", "", text)
    raw_clauses = CLAUSE_SPLIT_PATTERN.split(text)
    cleaned = [clean_clause(c) for c in raw_clauses]
    cleaned = [c for c in cleaned if c.strip()]
    return "|".join(cleaned)


def clean_text_flat(text: str) -> str:
    """Versi satu string datar (tanpa '|') -- INI yang dipakai sebagai input
    ke TF-IDF vectorizer, harus identik dengan cara kolom content_clean
    dibuat saat training, atau prediksi akan tidak akurat."""
    return clean_text_with_clauses(text).replace("|", " ")