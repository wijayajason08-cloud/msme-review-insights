import re
import pandas as pd
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

SLANG_DICT = {
    "gk": "tidak", "ga": "tidak", "gak": "tidak", "nggak": "tidak", "ngga": "tidak",
    "bgt": "banget", "yg": "yang", "udh": "sudah", "udah": "sudah",
    "tp": "tapi", "sy": "saya", "aq": "aku", "gw": "saya", "gua": "saya",
    "dr": "dari", "krn": "karena", "karna": "karena", "jd": "jadi",
    "utk": "untuk", "dgn": "dengan", "bs": "bisa", "trs": "terus",
    "sm": "sama", "gmn": "bagaimana", "knp": "kenapa", "dr": "dari",
    "aja": "saja", "emg": "memang", "emang": "memang",
}


def normalize_slang(text: str) -> str:
    words = text.split()
    normalized = [SLANG_DICT.get(w, w) for w in words]
    return " ".join(normalized)


def clean_text(text: str) -> str:
    text = str(text).lower()                       # case folding
    text = re.sub(r"http\S+", "", text)             # hapus URL
    text = re.sub(r"[^a-z\s]", " ", text)           # hapus angka, tanda baca, emoji
    text = re.sub(r"\s+", " ", text).strip()        # hapus spasi berlebih
    text = normalize_slang(text)
    return text


def main():
    print("Membaca data mentah...")
    df = pd.read_csv("data/raw/reviews_raw.csv")
    print(f"  -> {len(df)} baris data dimuat")

    # 1. Hapus duplikat
    before = len(df)
    df = df.drop_duplicates(subset="content")
    print(f"Menghapus duplikat: {before - len(df)} baris dihapus")

    # 2. Hapus review kosong/NaN
    before = len(df)
    df = df.dropna(subset=["content"])
    df = df[df["content"].astype(str).str.strip() != ""]
    print(f"Menghapus review kosong: {before - len(df)} baris dihapus")

    print("Membersihkan teks...")
    df["content_clean"] = df["content"].apply(clean_text)

    print("Menghapus stopword Bahasa Indonesia...")
    stopword_remover = StopWordRemoverFactory().create_stop_word_remover()
    df["content_clean"] = df["content_clean"].apply(lambda x: stopword_remover.remove(x))

    before = len(df)
    df = df[df["content_clean"].str.strip() != ""]
    print(f"Menghapus hasil cleaning yang kosong: {before - len(df)} baris dihapus")

    df.to_csv("data/processed/reviews_clean.csv", index=False)
    print(f"\nSelesai! {len(df)} baris data bersih tersimpan di data/processed/reviews_clean.csv")


if __name__ == "__main__":
    main()