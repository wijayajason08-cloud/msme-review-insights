import pandas as pd
from text_cleaning import clean_text_with_clauses


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

    print("Membersihkan teks (per klausa, agar batas kalimat asli tidak hilang)...")
    df["content_clauses"] = df["content"].apply(clean_text_with_clauses)
    df["content_clean"] = df["content_clauses"].str.replace("|", " ", regex=False)

    before = len(df)
    df = df[df["content_clean"].str.strip() != ""]
    print(f"Menghapus hasil cleaning yang kosong: {before - len(df)} baris dihapus")

    df.to_csv("data/processed/reviews_clean.csv", index=False)
    print(f"\nSelesai! {len(df)} baris data bersih tersimpan di data/processed/reviews_clean.csv")


if __name__ == "__main__":
    main()