import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer

DOMAIN_STOPWORDS = [
    "aplikasi", "apk", "app", "nya", "min", "kak", "ka", "tolong",
    "banget", "sih", "deh", "dong", "ya", "yah", "saya", "kami",
    "bukuwarung", "kasirpintar", "buku", "warung", "kasir", "pintar", 
    "tiba", "kesini", "verifikasi", "mau", "bisa", "malah", "update",
    "padahal", "di", "makin", "semua", "angka", "saldo", "hp", "qris",
    "log", "in", "hutang", "masuk", "kode", "tombol", "hati", "pas", "login",
    "catatan", "tidak", "tanggung", "jawab", "catatan", "chat", "cs", "navigasi",
    "minta", "ampun", "berkali", "kali", "nonaktifkan", "sama", "sekali",
    "berhari", "hari", "versi", "terbaru", "nol", "tertutup", "rekening",
    "kebawah", "kok", "bawah", "unduh", "laporan",

]


def load_data():
    df = pd.read_csv("data/processed/reviews_clean.csv")
    print(f"Data dimuat: {len(df)} baris")
    return df


def get_top_distinctive_ngrams(df, ngram_range, top_n=15, min_df=3, min_count=10):
    negatif = df[df["rating"].isin([1, 2])]["content_clean"].astype(str)
    positif = df[df["rating"].isin([4, 5])]["content_clean"].astype(str)

    vectorizer = CountVectorizer(
        stop_words=DOMAIN_STOPWORDS,
        ngram_range=ngram_range,
        min_df=min_df,
    )
    count_negatif_matrix = vectorizer.fit_transform(negatif)
    vocab = vectorizer.get_feature_names_out()

    count_negatif = count_negatif_matrix.sum(axis=0).A1
    total_negatif = count_negatif.sum()
    freq_negatif = count_negatif / total_negatif

    count_positif_matrix = vectorizer.transform(positif)
    count_positif = count_positif_matrix.sum(axis=0).A1
    total_positif = count_positif.sum()
    freq_positif = count_positif / total_positif if total_positif > 0 else count_positif

    score_negatif = pd.Series(freq_negatif, index=vocab)
    score_positif = pd.Series(freq_positif, index=vocab)
    distinctiveness = score_negatif - score_positif

    count_series = pd.Series(count_negatif, index=vocab)
    distinctiveness = distinctiveness[count_series >= min_count]

    return distinctiveness.sort_values(ascending=False).head(top_n)


def plot_ngrams(top_words, title, filename):
    plt.figure(figsize=(9, 7))
    plt.barh(top_words.index[::-1], top_words.values[::-1], color="#C44E52")
    plt.title(title)
    plt.xlabel("Skor Distinctiveness (proporsi negatif − proporsi positif)")
    plt.tight_layout()
    plt.savefig(f"docs/images/{filename}")
    plt.close()
    print(f"Tersimpan: docs/images/{filename}")


def main():
    df = load_data()

    print("\n=== Top KATA TUNGGAL paling khas di review negatif ===")
    top_unigram = get_top_distinctive_ngrams(df, ngram_range=(1, 1), top_n=15, min_df=3, min_count=10)
    for word, score in top_unigram.items():
        print(f"  {word}: {score:.6f}")
    plot_ngrams(
        top_unigram,
        "Kata Tunggal Paling Khas di Review Negatif",
        "top_keywords_negatif_unigram.png",
    )

    print("\n=== Top FRASA 2-KATA paling khas di review negatif ===")
    top_bigram = get_top_distinctive_ngrams(df, ngram_range=(2, 2), top_n=15, min_df=2, min_count=5)
    for word, score in top_bigram.items():
        print(f"  {word}: {score:.6f}")
    plot_ngrams(
        top_bigram,
        "Frasa 2-Kata Paling Khas di Review Negatif",
        "top_keywords_negatif_bigram.png",
    )


if __name__ == "__main__":
    main()