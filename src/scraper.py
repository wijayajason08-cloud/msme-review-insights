"""
Script untuk scraping review aplikasi dari Google Play Store.
Output: data/raw/reviews_raw.csv
"""

from google_play_scraper import reviews, Sort
import pandas as pd
import time

# Package ID tiap aplikasi target (sudah diverifikasi manual via Play Store).
APP_IDS = {
    "BukuWarung": "com.bukuwarung",
    "KasirPintar": "org.owline.kasirpintar",
}

JUMLAH_REVIEW_PER_APP = 4000  # dinaikkan dari 2000 karena hanya 2 aplikasi, agar total data tetap cukup

def scrape_all_apps():
    all_reviews = []

    for app_name, package_id in APP_IDS.items():
        print(f"Scraping {app_name} ({package_id})...")
        try:
            result, _ = reviews(
                package_id,
                lang='id',
                country='id',
                sort=Sort.NEWEST,
                count=JUMLAH_REVIEW_PER_APP,
            )
            for r in result:
                all_reviews.append({
                    "app": app_name,
                    "content": r["content"],
                    "rating": r["score"],
                    "date": r["at"],
                })
            print(f"  -> Berhasil ambil {len(result)} review")
        except Exception as e:
            print(f"  -> GAGAL scraping {app_name}: {e}")

        time.sleep(2)  # jeda antar app biar tidak terlalu cepat request

    return pd.DataFrame(all_reviews)


if __name__ == "__main__":
    df = scrape_all_apps()
    df.to_csv("data/raw/reviews_raw.csv", index=False)
    print(f"\nSelesai! Total {len(df)} review tersimpan di data/raw/reviews_raw.csv")