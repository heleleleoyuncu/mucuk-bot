import random
from ai import ask_ai, clear_history
from games import (
    cmd_tahmin, cmd_t, cmd_kelime, cmd_harf,
    cmd_trivia, cmd_cevap, cmd_tkm, cmd_anagram,
    cmd_kelimecevap, cmd_matematik, cmd_mat,
    cmd_emoji, cmd_emojicevap, cmd_bitir,
)
from fun import (
    cmd_saka, cmd_fikra, cmd_gercek, cmd_ruh,
    cmd_8top, cmd_kim, cmd_ship, cmd_siir,
    cmd_rap, cmd_hikaye, cmd_yorum,
)
from utils import (
    check_spam, add_score, get_leaderboard, get_score,
    remember, show_memories, forget_all, get_weather,
)
from config import BOT_OWNER, PREFIX

YARDIM = """🤖 MUCUK BOT — KOMUTLAR

🎮 OYUNLAR:
!tahmin — Sayı tahmin (1-100)
!t <sayı> — Tahminde bulun
!kelime — Adam asmaca
!harf <harf> — Harf tahmin et
!trivia [kategori] — Bilgi sorusu
  Kategoriler: bilim, tarih, coğrafya, spor, eğlence
!cevap <cevap> — Trivia yanıtla
!tkm <taş/kağıt/makas> — Taş Kağıt Makas
!anagram — Karışık harf bul
!kelimecevap <kelime> — Anagram cevapla
!matematik — Matematik sorusu
!mat <cevap> — Matematik yanıtla
!emoji — Emoji quiz
!emojicevap <kelime> — Emoji cevapla
!bitir — Aktif oyunu bitir

🎭 EĞLENCE:
!şaka — Şaka yap
!fıkra — Fıkra anlat
!gerçek — İlginç bilgi
!8top <soru> — Sihirli 8 top
!kim <sıfat> — Gruptaki en ... kişi
!ship [@kullanıcı] — İki kişiyi eşleştir
!ruh — Ruh hayvanın
!şiir [konu] — AI şiiri
!rap [konu] — AI rap
!hikaye [konu] — Kısa hikaye
!yorum [@hedef] — Komik yorum

🏆 SKOR:
!sıralama — Skor tablosu
!skor — Skorun

🌦️ BİLGİ:
!hava <şehir> — Hava durumu
!sor <soru> — AI'ya sor

🧠 SOHBET:
@bot <mesaj> — Benimle sohbet et
!temizle — Sohbet geçmişini sil

💾 BELLEK:
!hatırla <şey> — Bir şey hatırlamamı söyle
!hatırladıkların — Hatırladıklarımı göster
!unut — Tüm hatırladıklarımı sil

🎲 HIZLI:
!zar — Zar at
!flip — Yazı/Tura
!yardim — Bu menü"""

def handle_command(text: str, tid: str = "", username: str = "",
                   thread_users: list = [], user_id: str = "") -> str | None:

    if check_spam(user_id or username):
        return None

    text = text.strip()
    if not text.startswith(PREFIX):
        return None

    raw = text[len(PREFIX):]
    parts = raw.split(" ", 1)
    cmd = parts[0].lower()
    args = parts[1] if len(parts) > 1 else ""

    # ── Yardım ────────────────────────────────────────────────────────────────
    if cmd in ("yardim", "yardım", "help"):
        return YARDIM

    # ── Hızlı ─────────────────────────────────────────────────────────────────
    if cmd == "zar":
        faces = ["⚀","⚁","⚂","⚃","⚄","⚅"]
        n = random.randint(0, 5)
        return f"🎲 {faces[n]} ({n+1})"
    if cmd == "flip":
        return f"🪙 {random.choice(['Yazı!', 'Tura!'])}"

    # ── AI ────────────────────────────────────────────────────────────────────
    if cmd == "sor":
        return ask_ai(args, tid) if args else "Kullanım: !sor <sorun>"
    if cmd in ("temizle", "resetle"):
        return clear_history(tid)

    # ── Oyunlar ───────────────────────────────────────────────────────────────
    if cmd == "tahmin": return cmd_tahmin(tid, args)
    if cmd == "t":      return cmd_t(tid, args, username)
    if cmd == "kelime": return cmd_kelime(tid, args)
    if cmd == "harf":   return cmd_harf(tid, args, username)
    if cmd == "trivia": return cmd_trivia(tid, args)
    if cmd == "cevap":  return cmd_cevap(tid, args, username)
    if cmd == "tkm":    return cmd_tkm(tid, args, username)
    if cmd == "anagram":     return cmd_anagram(tid, args)
    if cmd == "kelimecevap": return cmd_kelimecevap(tid, args, username)
    if cmd == "matematik":   return cmd_matematik(tid, args)
    if cmd == "mat":         return cmd_mat(tid, args, username)
    if cmd == "emoji":       return cmd_emoji(tid, args)
    if cmd == "emojicevap":  return cmd_emojicevap(tid, args, username)
    if cmd == "bitir":       return cmd_bitir(tid)

    # ── Eğlence ───────────────────────────────────────────────────────────────
    if cmd in ("şaka", "saka", "joke"):  return cmd_saka(args)
    if cmd == "fıkra":                   return cmd_fikra(args)
    if cmd in ("gerçek", "gercek"):      return cmd_gercek(args)
    if cmd == "ruh":                     return cmd_ruh(args, username)
    if cmd in ("8top", "8ball"):         return cmd_8top(args)
    if cmd == "kim":                     return cmd_kim(args, thread_users, username)
    if cmd == "ship":                    return cmd_ship(args, thread_users)
    if cmd in ("şiir", "siir"):          return cmd_siir(args)
    if cmd == "rap":                     return cmd_rap(args, username)
    if cmd == "hikaye":                  return cmd_hikaye(args)
    if cmd == "yorum":                   return cmd_yorum(args)

    # ── Skor ──────────────────────────────────────────────────────────────────
    if cmd in ("sıralama", "siralama", "leaderboard"):
        return get_leaderboard()
    if cmd in ("skor", "puan"):
        return get_score(username)

    # ── Hava ──────────────────────────────────────────────────────────────────
    if cmd == "hava":
        if not args.strip():
            return "❌ Kullanım: !hava <şehir>"
        return get_weather(args.strip())

    # ── Bellek ────────────────────────────────────────────────────────────────
    if cmd == "hatırla":
        return remember(tid, args) if args else "Ne hatırlamamı istiyorsun? !hatırla <şey>"
    if cmd in ("hatırladıkların", "hatirladiklarin"):
        return show_memories(tid)
    if cmd == "unut":
        return forget_all(tid)

    # ── Hakkında ──────────────────────────────────────────────────────────────
    if cmd in ("hakkinda", "hakkında"):
        return "🤖 Ben Mucuk Bot! Groq AI + oyunlar + eğlence. !yardim ile komutları gör."

    # ── Admin ─────────────────────────────────────────────────────────────────
    if cmd == "ping" and username == BOT_OWNER:
        return "🏓 Pong! Bot çalışıyor."

    # ── Bilinmeyen ────────────────────────────────────────────────────────────
    return f"❓ '{cmd}' bilinmiyor. !yardim yaz."
