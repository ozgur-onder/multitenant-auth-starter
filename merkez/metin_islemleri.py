def turkce_buyuk_harf(metin: str) -> str:
    # str.upper() "i" harfini "I" yapar; Türkçede "İ" olmalı.
    return metin.replace("i", "İ").replace("ı", "I").upper()