import re

import pandas as pd

PROBE_WORDS = [
    "tidak", "bisa", "gak", "ga", "nggak", "tdk", "malah", "mau",
    "update", "qris", "saldo", "verifikasi", "otp", "tombol", "hilang", "data",
]


def count_docs(series, word):
    pattern = re.compile(rf"\b{re.escape(word)}\b")
    return int(series.str.lower().apply(lambda t: bool(pattern.search(t))).sum())


def main():
    df = pd.read_csv("data/processed/reviews_clean.csv")
    raw = df["content"].astype(str)
    clean = df["content_clean"].astype(str)

    print(f"Total review: {len(df)}\n")
    print(f"{'kata':<12}{'di teks mentah':>16}{'di teks bersih':>16}")
    print("-" * 44)
    for w in PROBE_WORDS:
        print(f"{w:<12}{count_docs(raw, w):>16}{count_docs(clean, w):>16}")

    print("\nContoh 8 review negatif (mentah -> bersih):")
    sample = df[df["rating"] <= 2].sample(8, random_state=1)
    for _, row in sample.iterrows():
        print(f"\n  MENTAH: {row['content']}")
        print(f"  BERSIH: {row['content_clean']}")


if __name__ == "__main__":
    main()