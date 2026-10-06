import pandas as pd
from pain_point_categories import PAIN_POINTS

CROSS_CUTTING = {"Menyebut kata 'update' (lintas kategori, sebab beragam)": ["update"]}


def load_negative_bukuwarung():
    df = pd.read_csv("data/processed/reviews_clean.csv")
    subset = df[(df["app"] == "BukuWarung") & (df["rating"].isin([1, 2]))].copy()
    return subset


def contains_any(text, keywords):
    text = str(text)
    return any(kw in text for kw in keywords)


def report_group(df, total, group_dict, title):
    print(f"\n{'#' * 60}\n{title}\n{'#' * 60}")
    results = []
    for label, keywords in group_dict.items():
        mask = df["content_clean"].apply(lambda t: contains_any(t, keywords))
        matched = df[mask]
        pct = len(matched) / total * 100
        results.append((label, len(matched), pct, mask))

        print(f"\n{'=' * 60}\n{label}: {len(matched)} review ({pct:.1f}%)\n{'=' * 60}")
        examples = matched.sample(min(3, len(matched)), random_state=42)
        for _, row in examples.iterrows():
            print(f"  [rating {row['rating']}] {row['content']}")
    return results


def main():
    df = load_negative_bukuwarung()
    total = len(df)
    print(f"Total review negatif BukuWarung: {total}")

    results = report_group(df, total, PAIN_POINTS, "PAIN POINTS")
    report_group(df, total, CROSS_CUTTING, "POLA LINTAS-KATEGORI (bukan pain point tersendiri)")

    any_match = pd.Series(False, index=df.index)
    for _, _, _, mask in results:
        any_match = any_match | mask

    print(f"\n{'#' * 60}\nRINGKASAN PAIN POINT (terurut dari paling sering)\n{'#' * 60}")
    for label, count, pct, _ in sorted(results, key=lambda x: -x[2]):
        print(f"  {pct:5.1f}% ({count:4d} review) - {label}")

    print(f"\nReview yang cocok MINIMAL SATU pain point: "
          f"{any_match.sum()} dari {total} ({any_match.mean() * 100:.1f}%)")


if __name__ == "__main__":
    main()