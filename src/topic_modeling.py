import pandas as pd
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
from id_stopwords import STOPWORDS_FOR_TOPICS

APP_FILTER = "BukuWarung"
N_TOPICS = 5
N_TOP_WORDS = 10


def load_negative_reviews():
    df = pd.read_csv("data/processed/reviews_clean.csv")
    subset = df[(df["app"] == APP_FILTER) & (df["rating"].isin([1, 2]))]
    texts = subset["content_clean"].astype(str)
    print(f"Review negatif {APP_FILTER}: {len(texts)}")
    return texts


def run_lda(texts):
    vectorizer = CountVectorizer(stop_words=STOPWORDS_FOR_TOPICS, min_df=5, max_df=0.5)
    matrix = vectorizer.fit_transform(texts)
    lda = LatentDirichletAllocation(n_components=N_TOPICS, random_state=42, max_iter=20)
    lda.fit(matrix)
    return lda, vectorizer.get_feature_names_out()


def print_and_save_topics(lda, feature_names, n_docs):
    lines = [f"# Topic Modeling Results (LDA)\n\n- App: {APP_FILTER} (n = {n_docs})\n"]
    for idx, topic in enumerate(lda.components_):
        top_words = [feature_names[i] for i in topic.argsort()[-N_TOP_WORDS:][::-1]]
        print(f"\nTopik #{idx + 1}: {', '.join(top_words)}")
        lines.append(f"\n## Topic #{idx + 1}\n**Top words:** {', '.join(top_words)}\n")
        lines.append("**Suggested label:** _(fill in)_\n")
    with open("docs/topic-modeling-results.md", "w", encoding="utf-8") as f:
        f.writelines(lines)
    print("\nTersimpan: docs/topic-modeling-results.md")


def main():
    texts = load_negative_reviews()
    lda, feature_names = run_lda(texts)
    print_and_save_topics(lda, feature_names, len(texts))


if __name__ == "__main__":
    main()