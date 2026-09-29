import sys

import pandas as pd


def main():
    if len(sys.argv) < 2:
        print('Pakai: python src/inspect_phrase.py "frasa yang dicari"')
        return

    phrase = sys.argv[1].lower()
    df = pd.read_csv("data/processed/reviews_clean.csv")
    matches = df[df["content_clean"].str.contains(phrase, case=False, na=False, regex=False)]

    print(f"Ditemukan {len(matches)} review mengandung '{phrase}'\n")
    for _, row in matches.head(10).iterrows():
        print(f"[{row['app']} | rating {row['rating']}] {row['content']}")
        print()


if __name__ == "__main__":
    main()