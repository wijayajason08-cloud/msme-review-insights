import re

import pandas as pd
from id_stopwords import STOPWORDS

STOPWORD_SET = set(STOPWORDS)

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
    words = text.split()
    normalized = [SLANG_DICT.get(w, w) for w in words]
    return " ".join(normalized)


def remove_stopwords(text: str) -> str:
    return " ".join(w for w in text.split() if w not in STOPWORD_SET)


def clean_text(text: str) -> str:
    text = str(text).lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    text = normalize_slang(text)
    text = remove_stopwords(text)
    return text


def main():
    print("Membaca data mentah...")
    df = pd.read_csv("data/raw/reviews_raw.csv")
    print(f"  -> {len(df)} baris data dimuat")

    before = len(df)
    df = df.drop_duplicates(subset="content")
    print(f"Menghapus duplikat: {before - len(df)} baris dihapus")

    before = len(df)
    df = df.dropna(subset=["content"])
    df = df[df["content"].astype(str).str.strip() != ""]
    print(f"Menghapus review kosong: {before - len(df)} baris dihapus")

    print("Membersihkan teks (case folding, hapus tanda baca, normalisasi slang, stopword)...")
    df["content_clean"] = df["content"].apply(clean_text)

    before = len(df)
    df = df[df["content_clean"].str.strip() != ""]
    print(f"Menghapus hasil cleaning yang kosong: {before - len(df)} baris dihapus")

    df.to_csv("data/processed/reviews_clean.csv", index=False)
    print(f"\nSelesai! {len(df)} baris data bersih tersimpan di data/processed/reviews_clean.csv")


if __name__ == "__main__":
    main()