import random
from utils import add_score

# ── Oyun durumları ─────────────────────────────────────────────────────────────
_games: dict[str, dict] = {}

# ══════════════════════════════════════════════════════════════════════════════
# SAYI TAHMİN
# ══════════════════════════════════════════════════════════════════════════════
def cmd_tahmin(tid: str, args: str) -> str:
    sayi = random.randint(1, 100)
    _games[tid] = {"type": "tahmin", "sayi": sayi, "deneme": 0, "starter": None}
    return "🎮 Sayı tahmin oyunu başladı! 1-100 arası bir sayı tuttum. !t <sayı> ile tahmin et!"

def cmd_t(tid: str, args: str, username: str) -> str:
    g = _games.get(tid)
    if not g or g["type"] != "tahmin":
        return "❌ Aktif oyun yok. !tahmin ile başlat!"
    if not args.strip().lstrip("-").isdigit():
        return "Sayı gir! Örnek: !t 42"
    tahmin = int(args.strip())
    g["deneme"] += 1
    gercek = g["sayi"]
    if tahmin == gercek:
        _games.pop(tid, None)
        add_score(username, 3)
        return f"🎉 {username} {g['deneme']}. denemede buldu! Sayı {gercek}'di! (+3 puan)"
    hint = "📈 Daha büyük!" if tahmin < gercek else "📉 Daha küçük!"
    return f"{hint} ({g['deneme']}. deneme)"

# ══════════════════════════════════════════════════════════════════════════════
# ADAM ASMACA (kelime)
# ══════════════════════════════════════════════════════════════════════════════
KELIMELER = [
    "bilgisayar","telefon","araba","pencere","kapı","elma","masa","kalem",
    "deniz","güneş","ay","yıldız","çiçek","ağaç","kuş","balık","kedi","köpek",
    "ekmek","su","ateş","toprak","hava","bulut","yağmur","kar","rüzgar",
    "ev","okul","hastane","market","uçak","gemi","tren","bisiklet",
]

def cmd_kelime(tid: str, args: str) -> str:
    kelime = random.choice(KELIMELER)
    _games[tid] = {"type": "kelime", "kelime": kelime, "haklar": 7, "harfler": []}
    return f"🔤 Adam asmaca başladı! {len(kelime)} harfli kelime. !harf <harf> ile tahmin et!\n{'_ ' * len(kelime)}\n❤️ x7"

def cmd_harf(tid: str, args: str, username: str) -> str:
    g = _games.get(tid)
    if not g or g["type"] != "kelime":
        return "❌ Aktif kelime oyunu yok. !kelime ile başlat!"
    if not args or len(args.strip()) != 1:
        return "Bir harf gir! Örnek: !harf a"
    harf = args.strip().lower()
    if harf in g["harfler"]:
        return f"'{harf}' zaten denendi! Denenenler: {', '.join(g['harfler'])}"
    g["harfler"].append(harf)
    kelime = g["kelime"]
    if harf in kelime:
        goster = " ".join(h if h in g["harfler"] else "_" for h in kelime)
        if "_" not in goster:
            _games.pop(tid, None)
            add_score(username, 5)
            return f"🎉 {username} kelimeyi buldu: {kelime.upper()}! (+5 puan)"
        return f"✅ '{harf}' var!\n{goster}\n❤️ x{g['haklar']}  |  Denenenler: {', '.join(g['harfler'])}"
    g["haklar"] -= 1
    ASAC = ["😐","😟","😨","😰","😱","💀"]
    emoji = ASAC[min(7 - g["haklar"], len(ASAC)-1)]
    if g["haklar"] <= 0:
        gizli = kelime
        _games.pop(tid, None)
        return f"💀 Oyun bitti! Kelime: {gizli.upper()}\n{emoji}"
    goster = " ".join(h if h in g["harfler"] else "_" for h in kelime)
    return f"❌ '{harf}' yok! {emoji}\n{goster}\n❤️ x{g['haklar']}  |  Denenenler: {', '.join(g['harfler'])}"

# ══════════════════════════════════════════════════════════════════════════════
# TRİVİA (kategorili)
# ══════════════════════════════════════════════════════════════════════════════
TRIVIA_DB = {
    "bilim": [
        ("Işık hızı yaklaşık kaç km/s?", "300000"),
        ("Su'nun kimyasal formülü nedir?", "h2o"),
        ("DNA'nın açılımı nedir?", "deoksiribonükleik asit"),
        ("İnsan vücudunda kaç kemik var?", "206"),
        ("Fotosentezi yapan organel?", "kloroplast"),
        ("Periyodik tabloda Au sembolü hangi element?", "altın"),
        ("En hafif element hangisi?", "hidrojen"),
        ("Işığın 1 yılda aldığı yol?", "ışık yılı"),
    ],
    "tarih": [
        ("Türkiye Cumhuriyeti hangi yıl kuruldu?", "1923"),
        ("Fatih Sultan Mehmet İstanbul'u hangi yıl fethetti?", "1453"),
        ("1. Dünya Savaşı hangi yıl bitti?", "1918"),
        ("Kurtuluş Savaşı hangi yıllar arasında?", "1919-1923"),
        ("Atatürk hangi yıl doğdu?", "1881"),
        ("Osmanlı İmparatorluğu kaç yıl sürdü?", "600"),
    ],
    "coğrafya": [
        ("Türkiye'nin başkenti?", "ankara"),
        ("Dünyanın en uzun nehri?", "nil"),
        ("En büyük okyanus?", "pasifik"),
        ("Türkiye kaç ile ayrılmıştır?", "81"),
        ("Avrupa'nın en yüksek dağı?", "elbrus"),
        ("Dünyanın en büyük ülkesi?", "rusya"),
        ("Amazon ormanları hangi kıtada?", "güney amerika"),
    ],
    "spor": [
        ("FIFA Dünya Kupası kaç yılda bir düzenlenir?", "4"),
        ("Bir futbol maçı kaç dakika sürer?", "90"),
        ("Olimpiyatlar kaç yılda bir düzenlenir?", "4"),
        ("Basketbolda bir sayı kaç puan?", "2"),
        ("Formül 1'de şampiyon olan ilk Türk?", "yok"),
    ],
    "eğlence": [
        ("Minecraft'ı kim yaptı?", "notch"),
        ("En çok izlenen YouTube kanalı?", "t-series"),
        ("İlk iPhone hangi yıl çıktı?", "2007"),
        ("GTA'yı yapan şirket?", "rockstar"),
        ("Fortnite'ı yapan şirket?", "epic games"),
    ],
}

def cmd_trivia(tid: str, args: str) -> str:
    kategori = args.strip().lower() if args.strip() else None
    if kategori and kategori not in TRIVIA_DB:
        cats = ", ".join(TRIVIA_DB.keys())
        return f"❌ Kategori bulunamadı. Mevcut: {cats}"
    if not kategori:
        kategori = random.choice(list(TRIVIA_DB.keys()))
    soru_list = TRIVIA_DB[kategori]
    soru, cevap = random.choice(soru_list)
    _games[tid] = {"type": "trivia", "cevap": cevap, "soru": soru, "kategori": kategori}
    return f"🧠 [{kategori.upper()}] {soru}\n\n!cevap <cevabın> diyerek yanıtla!"

def cmd_cevap(tid: str, args: str, username: str) -> str:
    g = _games.get(tid)
    if not g or g["type"] != "trivia":
        return "❌ Aktif trivia sorusu yok. !trivia ile başlat!"
    verilen = args.strip().lower()
    dogru = g["cevap"].lower()
    _games.pop(tid, None)
    if verilen == dogru or dogru in verilen or verilen in dogru:
        add_score(username, 2)
        return f"✅ Doğru! Cevap: {g['cevap']} 🎉 {username} +2 puan kazandı!"
    return f"❌ Yanlış! Doğru cevap: {g['cevap']}"

# ══════════════════════════════════════════════════════════════════════════════
# TAŞ KAĞIT MAKAS
# ══════════════════════════════════════════════════════════════════════════════
TKM_MAP = {"taş": "🪨", "kağıt": "📄", "makas": "✂️"}
TKM_BEATS = {"taş": "makas", "kağıt": "taş", "makas": "kağıt"}

def cmd_tkm(tid: str, args: str, username: str) -> str:
    secim = args.strip().lower()
    if secim not in TKM_MAP:
        return f"❌ Geçersiz seçim! !tkm <taş/kağıt/makas>"
    bot_secim = random.choice(list(TKM_MAP.keys()))
    user_e = TKM_MAP[secim]
    bot_e = TKM_MAP[bot_secim]
    if secim == bot_secim:
        return f"{user_e} vs {bot_e} — 🤝 Berabere!"
    elif TKM_BEATS[secim] == bot_secim:
        add_score(username, 1)
        return f"{user_e} vs {bot_e} — 🎉 {username} kazandı! (+1 puan)"
    else:
        return f"{user_e} vs {bot_e} — 🤖 Bot kazandı! Daha iyi dene."

# ══════════════════════════════════════════════════════════════════════════════
# ANAGrAM
# ══════════════════════════════════════════════════════════════════════════════
ANAGRAM_WORDS = [
    "elma","masa","kalem","araba","deniz","balık","güneş","yıldız",
    "bulut","rüzgar","çiçek","ağaç","kuş","toprak","bilgisayar","telefon",
]

def cmd_anagram(tid: str, args: str) -> str:
    kelime = random.choice(ANAGRAM_WORDS)
    karisik = list(kelime)
    random.shuffle(karisik)
    while "".join(karisik) == kelime:
        random.shuffle(karisik)
    karisik_str = "".join(karisik).upper()
    _games[tid] = {"type": "anagram", "kelime": kelime}
    return f"🔀 Anagram! Bu harfleri sırala: {karisik_str}\n!kelimecevap <cevabın>"

def cmd_kelimecevap(tid: str, args: str, username: str) -> str:
    g = _games.get(tid)
    if not g or g["type"] != "anagram":
        return "❌ Aktif anagram oyunu yok. !anagram ile başlat!"
    verilen = args.strip().lower()
    dogru = g["kelime"]
    _games.pop(tid, None)
    if verilen == dogru:
        add_score(username, 2)
        return f"🎉 Doğru! Kelime '{dogru}' idi! {username} +2 puan!"
    return f"❌ Yanlış! Doğru kelime: {dogru}"

# ══════════════════════════════════════════════════════════════════════════════
# MATEMATİK YARIŞMASI
# ══════════════════════════════════════════════════════════════════════════════
def cmd_matematik(tid: str, args: str) -> str:
    a, b = random.randint(1, 50), random.randint(1, 50)
    op = random.choice(["+", "-", "×"])
    if op == "+":
        ans = a + b
    elif op == "-":
        ans = a - b
    else:
        a, b = random.randint(1, 12), random.randint(1, 12)
        ans = a * b
    _games[tid] = {"type": "matematik", "cevap": ans}
    return f"🧮 Matematik sorusu: {a} {op} {b} = ?\n!mat <cevabın>"

def cmd_mat(tid: str, args: str, username: str) -> str:
    g = _games.get(tid)
    if not g or g["type"] != "matematik":
        return "❌ Aktif matematik sorusu yok. !matematik ile başlat!"
    if not args.strip().lstrip("-").isdigit():
        return "Sayı gir! Örnek: !mat 42"
    verilen = int(args.strip())
    dogru = g["cevap"]
    _games.pop(tid, None)
    if verilen == dogru:
        add_score(username, 1)
        return f"✅ Doğru! Cevap {dogru} idi. {username} +1 puan!"
    return f"❌ Yanlış! Doğru cevap: {dogru}"

# ══════════════════════════════════════════════════════════════════════════════
# EMOJİ QUİZ
# ══════════════════════════════════════════════════════════════════════════════
EMOJI_QUIZ = [
    ("🍎", "elma"), ("🚗", "araba"), ("🐱", "kedi"), ("🐶", "köpek"),
    ("🌍", "dünya"), ("⚽", "futbol"), ("🎸", "gitar"), ("🍕", "pizza"),
    ("✈️", "uçak"), ("🏠", "ev"), ("📚", "kitap"), ("🎮", "oyun"),
    ("🌙", "ay"), ("⭐", "yıldız"), ("🌊", "dalga"), ("🦁", "aslan"),
    ("🐘", "fil"), ("🦋", "kelebek"), ("🎵", "müzik"), ("💻", "bilgisayar"),
]

def cmd_emoji(tid: str, args: str) -> str:
    emoji, cevap = random.choice(EMOJI_QUIZ)
    _games[tid] = {"type": "emoji", "cevap": cevap, "emoji": emoji}
    return f"🤔 Bu emoji ne? {emoji}\n!emojicevap <cevabın>"

def cmd_emojicevap(tid: str, args: str, username: str) -> str:
    g = _games.get(tid)
    if not g or g["type"] != "emoji":
        return "❌ Aktif emoji sorusu yok. !emoji ile başlat!"
    verilen = args.strip().lower()
    dogru = g["cevap"]
    _games.pop(tid, None)
    if verilen == dogru or dogru in verilen:
        add_score(username, 1)
        return f"✅ Doğru! {g['emoji']} = {dogru}! {username} +1 puan!"
    return f"❌ Yanlış! {g['emoji']} = {dogru}"

# ══════════════════════════════════════════════════════════════════════════════
# GENEL
# ══════════════════════════════════════════════════════════════════════════════
def cmd_bitir(tid: str) -> str:
    if tid in _games:
        _games.pop(tid)
        return "🛑 Oyun bitirildi."
    return "❌ Aktif oyun yok."

def get_game(tid: str):
    return _games.get(tid)
