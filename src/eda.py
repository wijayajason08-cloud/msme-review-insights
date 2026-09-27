"""
Script EDA (Exploratory Data Analysis) untuk data review yang sudah dibersihkan.
Input:  data/processed/reviews_clean.csv
Output: gambar visualisasi disimpan di docs/images/

Catatan: analisis "top kata negatif" berbasis frekuensi mentah sudah DIHAPUS dari
sini karena bias terhadap kata generik (lihat src/keyword_analysis.py yang
menggantikannya dengan metode distinctiveness yang lebih akurat).
"""

import os

import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Kata generik yang sering muncul tapi tidak mengandung informasi sentimen.
# Sama dengan daftar di keyword_analysis.py, supaya wordcloud tidak didominasi
# kata-kata yang tidak informatif.
DOMAIN_STOPWORDS = {
    "aplikasi", "apk", "app", "nya", "min", "kak", "ka", "tolong",
    "banget", "sih", "deh", "dong", "ya", "yah", "saya", "kami",
    "bukuwarung", "kasirpintar", "buku", "warung", "kasir", "pintar",
}

os.makedirs("docs/images", exist_ok=True)


def load_data():
    df = pd.read_csv("data/processed/reviews_clean.csv")
    print(f"Data dimuat: {len(df)} baris")
    return df


def plot_rating_distribution(df):
    plt.figure(figsize=(6, 4))
    df["rating"].value_counts().sort_index().plot(kind="bar", color="#4C72B0")
    plt.title("Distribusi Rating Review")
    plt.xlabel("Rating")
    plt.ylabel("Jumlah Review")
    plt.tight_layout()
    plt.savefig("docs/images/rating_distribution.png")
    plt.close()
    print("Tersimpan: docs/images/rating_distribution.png")


def plot_wordcloud(df, rating_filter, label, filename):
    subset = df[df["rating"].isin(rating_filter)]
    text = " ".join(subset["content_clean"].astype(str))
    if not text.strip():
        print(f"  -> Lewati '{label}': tidak ada data untuk filter rating ini")
        return
    wc = WordCloud(
        width=800,
        height=400,
        background_color="white",
        stopwords=DOMAIN_STOPWORDS,
    ).generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.title(label)
    plt.tight_layout()
    plt.savefig(f"docs/images/{filename}")
    plt.close()
    print(f"Tersimpan: docs/images/{filename}")


def main():
    df = load_data()

    print("\nMembuat grafik distribusi rating...")
    plot_rating_distribution(df)

    print("\nMembuat wordcloud review negatif (rating 1-2)...")
    plot_wordcloud(df, [1, 2], "Wordcloud - Review Negatif", "wordcloud_negatif.png")

    print("Membuat wordcloud review positif (rating 4-5)...")
    plot_wordcloud(df, [4, 5], "Wordcloud - Review Positif", "wordcloud_positif.png")

    print("\nSelesai! Semua visualisasi tersimpan di folder docs/images/")
    print("(Analisis top kata/frasa negatif yang lebih akurat ada di src/keyword_analysis.py)")


if __name__ == "__main__":
    main()