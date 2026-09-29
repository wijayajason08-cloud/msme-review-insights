import os

import joblib
import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, average_precision_score,
                              classification_report, confusion_matrix, roc_auc_score)
from sklearn.model_selection import train_test_split
from id_stopwords import STOPWORDS

TARGET_NAMES = ["positif", "negatif"]
os.makedirs("models", exist_ok=True)


def load_labeled_data():
    df = pd.read_csv("data/processed/reviews_clean.csv")
    df = df[df["rating"] != 3].copy()
    df["y"] = (df["rating"] <= 2).astype(int)
    df["content_clean"] = df["content_clean"].astype(str)
    print("Data berlabel per aplikasi:")
    print(df.groupby("app")["y"].agg(total="size", negatif="sum"))
    return df


def new_vectorizer():
    return TfidfVectorizer(stop_words=STOPWORDS, ngram_range=(1, 2), min_df=3)


def report(y_true, y_pred, y_proba, judul):
    print(f"\n--- {judul} ---")
    print(classification_report(y_true, y_pred, target_names=TARGET_NAMES, digits=3))
    cm = confusion_matrix(y_true, y_pred, labels=[0, 1])
    print(pd.DataFrame(cm, index=["Aktual: positif", "Aktual: negatif"],
                        columns=["Prediksi: positif", "Prediksi: negatif"]))
    print(f"ROC-AUC: {roc_auc_score(y_true, y_proba):.4f}")
    print(f"Average Precision: {average_precision_score(y_true, y_proba):.4f} "
          f"(tebakan acak = {np.mean(y_true):.4f})")


def experiment_in_domain(df):
    print("\n" + "=" * 60 + "\nEKSPERIMEN A: dalam BukuWarung saja (split 80/20)\n" + "=" * 60)
    bw = df[df["app"] == "BukuWarung"]
    X_train, X_test, y_train, y_test = train_test_split(
        bw["content_clean"], bw["y"], test_size=0.2, random_state=42, stratify=bw["y"]
    )
    vec = new_vectorizer()
    Xtr, Xte = vec.fit_transform(X_train), vec.transform(X_test)
    baseline = DummyClassifier(strategy="most_frequent").fit(Xtr, y_train)
    print(f"Baseline: akurasi = {accuracy_score(y_test, baseline.predict(Xte)):.4f}")
    model = LogisticRegression(class_weight="balanced", max_iter=1000).fit(Xtr, y_train)
    print(f"Model: akurasi = {accuracy_score(y_test, model.predict(Xte)):.4f}")
    report(y_test, model.predict(Xte), model.predict_proba(Xte)[:, 1], "Hasil Eksperimen A")


def experiment_cross_app(df):
    print("\n" + "=" * 60 + "\nEKSPERIMEN B: latih BukuWarung, uji KasirPintar\n" + "=" * 60)
    bw = df[df["app"] == "BukuWarung"]
    kp = df[df["app"] == "KasirPintar"]
    vec = new_vectorizer()
    Xtr, Xte = vec.fit_transform(bw["content_clean"]), vec.transform(kp["content_clean"])
    model = LogisticRegression(class_weight="balanced", max_iter=1000).fit(Xtr, bw["y"])
    print(f"Test set KasirPintar: {len(kp)} review, {int(kp['y'].sum())} negatif")
    print(f"Baseline tebak-positif: {(1 - kp['y'].mean()) * 100:.1f}% -- akurasi TIDAK informatif di sini.")
    report(kp["y"], model.predict(Xte), model.predict_proba(Xte)[:, 1], "Hasil Eksperimen B")


def train_final_model(df, top_n=15):
    print("\n" + "=" * 60 + "\nMODEL FINAL: semua data, class_weight='balanced'\n" + "=" * 60)
    print("Catatan: sebelumnya dicoba pembobotan per (aplikasi, label), tapi itu")
    print("memperkuat pengaruh review dengan label noise (teks positif, rating")
    print("rendah) di kelas kecil KasirPintar hingga ~7x lipat. Disederhanakan")
    print("jadi class_weight='balanced' biasa untuk menghindari masalah itu.")

    vec = new_vectorizer()
    X = vec.fit_transform(df["content_clean"])
    model = LogisticRegression(class_weight="balanced", max_iter=1000).fit(X, df["y"])

    names = vec.get_feature_names_out()
    coefs = model.coef_[0]
    print("\nKata/frasa yang paling mendorong prediksi NEGATIF:")
    for i in coefs.argsort()[-top_n:][::-1]:
        print(f"  {names[i]}: {coefs[i]:.4f}")
    print("\nKata/frasa yang paling mendorong prediksi POSITIF:")
    for i in coefs.argsort()[:top_n]:
        print(f"  {names[i]}: {coefs[i]:.4f}")

    joblib.dump(model, "models/sentiment_model.pkl")
    joblib.dump(vec, "models/tfidf_vectorizer.pkl")
    print("\nTersimpan: models/sentiment_model.pkl, models/tfidf_vectorizer.pkl")


def main():
    df = load_labeled_data()
    experiment_in_domain(df)
    experiment_cross_app(df)
    train_final_model(df)


if __name__ == "__main__":
    main()