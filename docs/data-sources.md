# Data Sources — Target Applications

This document explains which apps were selected for review scraping and why.

## Selected Applications

| App Name | Package ID | Installs | Rating | Category |
|---|---|---|---|---|
| BukuWarung | `com.bukuwarung` | 5,000,000+ | _(fill in — check Play Store listing)_ | Bookkeeping / Digital Payments |
| BukuKas | `GANTI_DENGAN_PACKAGE_ID_ASLI` (verify manually) | 5,000,000+ (per third-party sources) | 4.6★ (per third-party sources; verify on Play Store) | Bookkeeping |
| Kasir Pintar | `GANTI_DENGAN_PACKAGE_ID_ASLI` (verify manually) | _(fill in — check Play Store listing)_ | _(fill in — check Play Store listing)_ | POS / Cashier |

> Note: BukuKas and Kasir Pintar package IDs and current stats should be confirmed directly on the Play Store before finalizing, as they could not be independently verified from a primary source at the time of writing.

## Selection Criteria

- **High install count / review volume** — all three apps have large user bases, ensuring enough data for reliable NLP analysis
- **Represents the target user segment** — all apps target MSME/UMKM owners in Indonesia
- **Mix of app types** — BukuWarung and BukuKas are both bookkeeping-focused (good for direct comparison of pain points within the same category), while Kasir Pintar is POS/cashier-focused (captures a different set of complaints, e.g. inventory or transaction-processing issues, broadening the scope of findings)
- **Actively maintained** — all three are actively developed with regular updates and ongoing user reviews

## How Package IDs Were Found

1. Open the app's page on the Google Play Store (via browser)
2. Check the URL — the value after `id=` is the package ID
   Example: `https://play.google.com/store/apps/details?id=com.bukuwarung`
   → Package ID: `com.bukuwarung`

## Related Work

Academic research has previously analyzed sentiment in reviews of similar MSME financial apps (e.g., a comparative sentiment analysis study covering BukuWarung, Money Lover, and Kledo), providing useful context on common complaint categories within this app segment.

## Notes / Limitations

- Review data reflects the opinions of users who chose to leave a review, which may not represent the full user base
- Play Store reviews may skew toward extreme experiences (very positive or very negative)
- Third-party install/rating figures for BukuKas were sourced from secondary references and should be reverified directly on the Play Store listing
