import os

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from id_stopwords import STOPWORDS, STOPWORDS_FOR_TOPICS

MIN_NEG_REVIEWS = 300

os.makedirs("docs/images", exist_ok=True)


def load_data():
    df = pd.read_csv("data/processed/reviews_clean.csv")
    print(f"Data dimuat: {len(df)} baris")
    return df


def get_top_distinctive_ngrams(df, ngram_range, stop_words, top_n=30, min_df=3, min_count=10):
    negatif = df[df["rating"].isin([1, 2])]["content_clean"].astype(str)
    positif = df[df["rating"].isin([4, 5])]["content_clean"].astype(str)

    vectorizer = CountVectorizer(stop_words=stop_words, ngram_range=ngram_range, min_df=min_df)
    count_neg_matrix = vectorizer.fit_transform(negatif)
    vocab = vectorizer.get_feature_names_out()

    count_neg = count_neg_matrix.sum(axis=0).A1
    freq_neg = count_neg / count_neg.sum()

    count_pos = vectorizer.transform(positif).sum(axis=0).A1
    total_pos = count_pos.sum()
    freq_pos = count_pos / total_pos if total_pos > 0 else count_pos

    distinctiveness = pd.Series(freq_neg - freq_pos, index=vocab)
    distinctiveness = distinctiveness[pd.Series(count_neg, index=vocab) >= min_count]
    return distinctiveness.sort_values(ascending=False).head(top_n)


def plot_ngrams(top_words, title, filename, n_show=15):
    top_words = top_words.head(n_show)
    plt.figure(figsize=(9, 7))
    plt.barh(top_words.index[::-1], top_words.values[::-1], color="#C44E52")
    plt.title(title)
    plt.xlabel("Skor Distinctiveness (proporsi negatif − proporsi positif)")
    plt.tight_layout()
    plt.savefig(f"docs/images/{filename}")
    plt.close()
    print(f"Tersimpan: docs/images/{filename}")


def analyze_subset(df, tag, judul):
    n_neg = int(df["rating"].isin([1, 2]).sum())
    n_pos = int(df["rating"].isin([4, 5]).sum())
    print(f"\n{'=' * 60}\n{judul}: {n_neg} review negatif vs {n_pos} review positif\n{'=' * 60}")

    if n_neg < MIN_NEG_REVIEWS:
        print(f"⏭️  DILEWATI: review negatif < {MIN_NEG_REVIEWS}.")
        return None, None

    top_uni = get_top_distinctive_ngrams(df, (1, 1), STOPWORDS_FOR_TOPICS, top_n=30, min_df=3, min_count=10)
    top_bi = get_top_distinctive_ngrams(df, (2, 2), STOPWORDS, top_n=30, min_df=2, min_count=5)

    print("\nTop 15 KATA TUNGGAL:")
    for w, s in top_uni.head(15).items():
        print(f"  {w}: {s:.6f}")
    print("\nTop 15 FRASA 2-KATA:")
    for w, s in top_bi.head(15).items():
        print(f"  {w}: {s:.6f}")

    plot_ngrams(top_uni, f"Kata Tunggal Khas Review Negatif — {judul}", f"keywords_{tag}_unigram.png")
    plot_ngrams(top_bi, f"Frasa 2-Kata Khas Review Negatif — {judul}", f"keywords_{tag}_bigram.png")
    return top_uni, top_bi


def compare(pooled, single, jenis, nama):
    if pooled is None or single is None:
        return
    p, s = set(pooled.index), set(single.index)
    print(f"\n--- Perbandingan {jenis}: gabungan vs {nama} saja ---")
    print("Muncul di KEDUANYA:")
    print("  " + (", ".join(sorted(p & s)) or "-"))
    print("Hanya di GABUNGAN (dicurigai efek confound aplikasi):")
    print("  " + (", ".join(sorted(p - s)) or "-"))
    print(f"Hanya di {nama} saja:")
    print("  " + (", ".join(sorted(s - p)) or "-"))


def main():
    df = load_data()
    pooled_uni, pooled_bi = analyze_subset(df, "gabungan", "Data gabungan")
    bw_uni, bw_bi = analyze_subset(df[df["app"] == "BukuWarung"], "bukuwarung", "BukuWarung saja")
    analyze_subset(df[df["app"] == "KasirPintar"], "kasirpintar", "KasirPintar saja")
    compare(pooled_uni, bw_uni, "kata tunggal", "BukuWarung")
    compare(pooled_bi, bw_bi, "frasa 2-kata", "BukuWarung")


if __name__ == "__main__":
    main()