import random
from ai import ai_quick

SAKALAR = [
    "Annem: 'Ders çalışıyor musun?' Ben: 'Evet.' Telefon: 'Haha, yalan söylüyor.' 😂",
    "Matematik sınavı: x'i bul. Ben: İşte x, buldum. Öğretmen: 💀",
    "Sabah 3'te uyumaya çalışırken beyin: 'Dur, 2015'te söylediğin o aptalca şeyi hatırlayalım.'",
    "Diyetim var diyorum... bisküvit paketi: 'Ama ben tek başımayım üzülüyorum.' 😅",
    "Telefon %1'de. Ben sakin. Şarj cihazı odada değil. Ben: PANİK.",
    "Öğretmen: 'Neden geç kaldın?' Ben: 'Trafik vardı.' Okul: '2. katta oturuyorsun.' 💀",
    "Uyku vakti: 23:00. Gerçek: 02:47. Sebebi: YouTube önerileri.",
    "Arkadaş: 'Yavaş ye, hazımsızlık olur.' Ben: 'Hayır ol-' Ben: 💀",
]

FIKRALAR = [
    "Temel bakkaldan patates almış, eve gelmiş, karısı sormuş: 'Ne aldın?' Temel: 'Patates.' Karısı: 'Kaç kilo?' Temel: 'Kilogram bilmiyorum, kilo aldım.' 😂",
    "Doktor hastaya: 'Sigara içiyor musunuz?' Hasta: 'Hayır doktor.' Doktor: 'Alkol?' Hasta: 'Hayır.' Doktor: 'Peki neden yaşıyorsunuz?' 💀",
    "Temel uçağa binmiş, hostese sormuş: 'Bu uçak ne kadar hızlı gidiyor?' Hostes: 'Saatte 800 km.' Temel: 'Peki yakıtı bitirsek dururuz değil mi?' 😂",
    "Adam doktora gitmiş: 'Doktor her yerimi burnumla dokunduğumda acıyor.' Doktor: 'Parmağın kırık.' 😅",
]

GERCEKLER = [
    "🧠 Ahtapotların 3 kalbi ve mavi kanı vardır.",
    "🐝 Bal arıları birbirlerini dans ederek bilgilendirir.",
    "🌊 Okyanus yüzeyinin sadece %5'i keşfedilmiştir.",
    "🦒 Zürafa dili 45 cm uzunluğundadır ve mavimsidir.",
    "⚡ Yıldırım saniyede 270.000 km hızla hareket eder.",
    "🐘 Filler birbirlerini isimleriyle çağırabilir.",
    "🍯 Arı balı asla bozulmaz, Mısır piramitlerinde 3000 yıllık bal bulunmuştur.",
    "🌙 Ay'da ses yoktur, çünkü hava yoktur.",
    "🐙 Ahtapotlar acı çekebilir ve duygularını hissedebilir.",
    "🦋 Kelebekler tatları ayaklarıyla hisseder.",
    "🎵 Müzik dinlemek dopamin salgılatır, bu yüzden mutlu eder.",
    "💤 İnsan ömrünün 1/3'ünü uyuyarak geçirir.",
]

HAYVAN_RUHLAR = [
    ("🦁 Aslan", "Lidersin! Güçlü, karizmatik, doğal bir lider. Ama bazen çok bencil olabilirsin."),
    ("🦊 Tilki", "Zekisin! Kurnaz, yaratıcı ve hızlı düşünürsün. İnsanlar sana güvenmekte zorlanabilir."),
    ("🐺 Kurt", "Sadakatisin! Ailenle her şeyi paylaşırsın ama yabancılara kapalısın."),
    ("🦅 Kartal", "Özgürsün! Bağımsız, geniş bakış açılı ve iddialısın. Rutine tahammül edemezsin."),
    ("🐬 Yunus", "Sosyalsin! Neşeli, zeki, empati gücü yüksek. Herkesle iyi anlaşırsın."),
    ("🐻 Ayı", "Sakinsin! Güçlü ama uyumlu, ailesini koruyan biri. Uyandırılınca korkutucusun."),
    ("🦋 Kelebek", "Yaratıcısın! Sürekli değişim içinde, sanatçı ruhlusun. Odaklanmakta zorlanırsın."),
    ("🐢 Kaplumbağa", "Sabırlısın! Yavaş ama emin adımlarla ilerlersin. Uzun vadede hep kazanırsın."),
]

def cmd_saka(args: str) -> str:
    return random.choice(SAKALAR)

def cmd_fikra(args: str) -> str:
    return random.choice(FIKRALAR)

def cmd_gercek(args: str) -> str:
    return random.choice(GERCEKLER)

def cmd_ruh(args: str, username: str) -> str:
    hayvan, aciklama = random.choice(HAYVAN_RUHLAR)
    return f"🔮 {username}'nin ruh hayvanı: {hayvan}\n\n{aciklama}"

def cmd_8top(args: str) -> str:
    if not args.strip():
        return "❓ Bir soru sor! Örnek: !8top Bugün şanslı mıyım?"
    cevaplar = [
        "✅ Kesinlikle evet!", "✅ Her şey işaret ediyor ki evet!",
        "✅ Güven içinde söyleyebilirim, evet.", "🔮 Belirsiz, tekrar sor.",
        "🔮 Şu an cevap veremem.", "🔮 Yoğunlaş ve tekrar sor.",
        "❌ Bekleme.", "❌ Cevabım hayır.", "❌ Kesinlikle hayır!",
        "🤷 Belki? Kim bilir.", "😂 Ciddi misin, bunu mu sordun?",
    ]
    return f"🎱 \"{args.strip()}\"\n→ {random.choice(cevaplar)}"

def cmd_kim(args: str, thread_users: list, username: str) -> str:
    if not args.strip():
        return "❌ Kullanım: !kim [en iyi/aptal/sevimli/...]"
    if not thread_users:
        secilen = username
    else:
        secilen = random.choice(thread_users) if thread_users else username
    return f"🎯 Grubun en {args.strip()} kişisi: @{secilen} 👀"

def cmd_ship(args: str, thread_users: list) -> str:
    if len(thread_users) >= 2:
        a, b = random.sample(thread_users, 2)
    elif args.strip():
        parts = args.strip().split()
        a = parts[0].lstrip("@")
        b = parts[1].lstrip("@") if len(parts) > 1 else "bot"
    else:
        return "❌ Yeterli kullanıcı yok!"
    yuzde = random.randint(0, 100)
    if yuzde >= 80:
        yorum = "Mükemmel çift! 💕"
    elif yuzde >= 60:
        yorum = "Fena değil! 😊"
    elif yuzde >= 40:
        yorum = "Olur da olur... 🤔"
    else:
        yorum = "Hmm... biraz zor. 😅"
    bar = "❤️" * (yuzde // 10) + "🖤" * (10 - yuzde // 10)
    return f"💘 {a} + {b}\n{bar}\n%{yuzde} uyum — {yorum}"

def cmd_siir(args: str) -> str:
    konu = args.strip() if args.strip() else "hayat"
    return ai_quick(f"'{konu}' hakkında güzel, kısa (4-6 satır) bir Türkçe şiir yaz.")

def cmd_rap(args: str, username: str) -> str:
    konu = args.strip() if args.strip() else username
    return ai_quick(f"'{konu}' hakkında kısa, eğlenceli bir Türkçe rap dörtlüğü yaz. Kafiyeli olsun.")

def cmd_hikaye(args: str) -> str:
    konu = args.strip() if args.strip() else "beklenmedik bir macera"
    return ai_quick(f"'{konu}' hakkında 4-5 cümlelik eğlenceli kısa Türkçe bir hikaye yaz.")

def cmd_yorum(args: str) -> str:
    hedef = args.strip() if args.strip() else "Instagram fenomeni"
    return ai_quick(f"'{hedef}' hakkında eğlenceli, biraz alaycı ama sevecen bir Instagram yorumu yaz. 2-3 cümle.")

def cmd_harf_zinciri(args: str) -> str:
    """Rastgele kelimeyi büyük harflerle yaz."""
    return ai_quick("Türkçe rastgele 1 kelime söyle.")
