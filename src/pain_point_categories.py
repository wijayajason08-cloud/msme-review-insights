PAIN_POINTS = {
    "CS respons lambat": ["cs", "respon", "chat"],
    "Saldo/QRIS/verifikasi bermasalah": ["saldo", "qris", "verifikasi", "rekening"],
    "Data/catatan hilang": [
        "data hilang", "hilang data", "catatan hilang", "hilang catatan",
        "pembukuan hilang", "hilang pembukuan", "hilang semua", "semua hilang",
        "saldo hilang", "hilang saldo",
    ],
    "Aplikasi keluar sendiri / crash": ["keluar", "force close", "crash"],
    "UI/navigasi: tombol & angka 0 tidak bisa diketik": [
        "tombol", "navigasi", "layar", "angka 0", "angka nol", "pencet nol", "ketik nol",
    ],
}


def match_categories(cleaned_text: str) -> list:
    """cleaned_text harus sudah melalui text_cleaning.clean_text_flat()."""
    return [label for label, keywords in PAIN_POINTS.items()
            if any(kw in cleaned_text for kw in keywords)]