import pandas as pd
 
 
def load_data():
    df = pd.read_csv("data/processed/reviews_clean.csv")
    df = df[df["rating"] != 3].copy()
    df["label"] = df["rating"].apply(lambda r: "positif" if r >= 4 else "negatif")
    return df
 
 
def check_app_confound(df):
    print("=" * 60)
    print("CEK 1: Proporsi sentimen per aplikasi")
    print("=" * 60)
 
    crosstab = pd.crosstab(df["app"], df["label"])
    crosstab["total"] = crosstab.sum(axis=1)
    crosstab["% negatif"] = (crosstab["negatif"] / crosstab["total"] * 100).round(1)
    print(crosstab)
 
    selisih = crosstab["% negatif"].max() - crosstab["% negatif"].min()
    print(f"\nSelisih persentase negatif antar aplikasi: {selisih:.1f} poin persen")
    if selisih > 20:
        print("⚠️  Selisih besar: ada risiko model belajar 'identitas aplikasi', bukan sentimen murni.")
    else:
        print("✅ Selisih relatif kecil.")
 
 
def check_length_confound(df):
    print("\n" + "=" * 60)
    print("CEK 2: Panjang review (jumlah kata) per sentimen")
    print("=" * 60)
 
    df = df.copy()
    df["word_count"] = df["content_clean"].astype(str).apply(lambda x: len(x.split()))
    summary = df.groupby("label")["word_count"].agg(["mean", "median", "std"]).round(2)
    print(summary)
 
    rasio_mean = summary.loc["negatif", "mean"] / summary.loc["positif", "mean"]
    rasio_median = summary.loc["negatif", "median"] / summary.loc["positif", "median"]
    print(f"\nRasio negatif/positif -> rata-rata: {rasio_mean:.2f}x | median: {rasio_median:.2f}x")
    print("ℹ️  Review negatif cenderung lebih panjang. Catat sebagai keterbatasan di dokumentasi.")
 
 
def check_temporal(df):
    print("\n" + "=" * 60)
    print("CEK 3: Rentang waktu & sebaran keluhan per aplikasi")
    print("=" * 60)
 
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])
 
    for app, g in df.groupby("app"):
        start, end = g["date"].min(), g["date"].max()
        span_days = max((end - start).days, 1)
        print(f"\n{app}: {start.date()} s/d {end.date()} "
              f"({span_days} hari, {len(g) / span_days:.1f} review/hari)")
 
        g = g.assign(bulan=g["date"].dt.to_period("M"))
        tabel = pd.crosstab(g["bulan"], g["label"]).reindex(
            columns=["negatif", "positif"], fill_value=0
        )
        tabel["total"] = tabel.sum(axis=1)
        tabel["% negatif"] = (tabel["negatif"] / tabel["total"] * 100).round(1)
        print(tabel.tail(12))
 
    print("\nCara membaca: kalau % negatif melonjak di 1-2 bulan terakhir saja,")
    print("keluhan kemungkinan didorong satu insiden (mis. bug versi tertentu),")
    print("bukan masalah yang persisten. Kalau rentang waktu antar aplikasi sangat")
    print("berbeda, perbandingan antar aplikasi juga tidak apple-to-apple.")
 
 
def main():
    df = load_data()
    print(f"Total data dianalisis: {len(df)} baris\n")
    check_app_confound(df)
    check_length_confound(df)
    check_temporal(df)
 
 
if __name__ == "__main__":
    main()
 