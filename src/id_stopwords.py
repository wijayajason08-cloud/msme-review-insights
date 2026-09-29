NEGATION_WORDS = {"tidak", "tak", "bukan", "belum", "jangan", "kurang", "tanpa"}

FUNCTION_WORDS = {
    # preposisi & konjungsi
    "yang", "di", "ke", "dari", "dan", "atau", "untuk", "pada", "dengan", "oleh",
    "kepada", "terhadap", "dalam", "sebagai", "agar", "supaya", "karena",
    "sehingga", "jika", "kalau", "ketika", "saat", "sambil", "serta",
    # penunjuk & kata ganti
    "ini", "itu", "tersebut", "dia", "ia", "mereka", "kita", "kami", "kamu",
    "anda", "saya", "aku",
    # partikel & filler
    "nya", "lah", "kah", "pun", "sih", "deh", "dong", "kok", "ya", "yah",
    "nih", "tuh", "kan",
    # kopula, aspek, kuantitas umum
    "adalah", "ialah", "yaitu", "yakni", "akan", "telah", "sedang", "juga",
    "saja", "hanya", "para", "suatu", "sebuah", "hal",
}

DOMAIN_FILLER = {
    "aplikasi", "apk", "app", "min", "kak", "ka", "tolong", "mohon", "banget",
    "bukuwarung", "kasirpintar", "buku", "warung", "kasir", "pintar",
}

STOPWORDS = sorted(FUNCTION_WORDS | DOMAIN_FILLER)

UNIGRAM_DISPLAY_EXCLUDE = {
    "tidak", "bisa", "mau", "malah", "padahal", "makin", "tiba", "sama", "ada",
}

STOPWORDS_FOR_TOPICS = sorted(set(STOPWORDS) | UNIGRAM_DISPLAY_EXCLUDE)

assert not (NEGATION_WORDS & set(STOPWORDS)), "Kata negasi tidak boleh menjadi stopword"


if __name__ == "__main__":
    print(f"STOPWORDS: {len(STOPWORDS)} kata")
    print(f"STOPWORDS_FOR_TOPICS: {len(STOPWORDS_FOR_TOPICS)} kata")
    print(f"Kata negasi yang dijaga: {sorted(NEGATION_WORDS)}")
    print("OK: tidak ada kata negasi di dalam STOPWORDS.")