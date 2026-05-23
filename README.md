# 🤖 Mucuk Bot — Ultra Mega Süper Instagram Botu

## Kurulum

```bash
cd instagram-bot
pip install -r requirements.txt
python main.py
```

## Özellikler

### 🎮 Oyunlar (10 adet)
| Komut | Açıklama |
|-------|----------|
| `!tahmin` | 1-100 sayı tahmin oyunu |
| `!t <sayı>` | Sayı tahminini gönder |
| `!kelime` | Adam asmaca |
| `!harf <harf>` | Adam asmacada harf tahmin |
| `!trivia [kategori]` | Bilgi yarışması (bilim/tarih/coğrafya/spor/eğlence) |
| `!cevap <cevap>` | Trivia sorusunu yanıtla |
| `!tkm <taş/kağıt/makas>` | Taş Kağıt Makas (bota karşı) |
| `!anagram` | Karışık harfleri sırala |
| `!kelimecevap <kelime>` | Anagram cevapla |
| `!matematik` | Matematik yarışması |
| `!mat <cevap>` | Matematik yanıtla |
| `!emoji` | Emoji quiz |
| `!emojicevap <kelime>` | Emoji cevapla |

### 🎭 Eğlence
| Komut | Açıklama |
|-------|----------|
| `!şaka` | Komik şaka |
| `!fıkra` | Türk fıkrası |
| `!gerçek` | İlginç bilgi |
| `!8top <soru>` | Sihirli 8 top |
| `!kim <sıfat>` | Gruptaki en ... kişi |
| `!ship` | İki kişiyi eşleştir |
| `!ruh` | Ruh hayvanın |
| `!şiir [konu]` | AI şiiri yaz |
| `!rap [konu]` | AI rap dörtlüğü |
| `!hikaye [konu]` | Kısa hikaye |
| `!yorum [@hedef]` | Komik Instagram yorumu |

### 🏆 Skor Sistemi
- Oyun kazanınca otomatik puan
- `!sıralama` ile lider tablosu
- `!skor` ile kendi puanın
- Puanlar `data/scores.json`'a kalıcı kaydedilir

### 🌦️ Faydalı
| Komut | Açıklama |
|-------|----------|
| `!hava <şehir>` | Hava durumu |
| `!sor <soru>` | Groq AI'ya sor |
| `!hatırla <şey>` | Bot bir şeyi hatırlar |
| `!hatırladıkların` | Hatırladıklarını gösterir |
| `!unut` | Tüm hatırlananları siler |

### 💬 Sohbet
- **Gruplarda**: `@kullanıcı_adı mesaj` yaz → AI cevap verir
- **DM'de**: Direkt yaz → AI cevap verir
- Thread bazlı sohbet hafızası (grup kendi geçmişini hatırlar)
- `!temizle` ile sıfırla

### 🛡️ Güvenlik
- Anti-spam: 2 saniye cooldown
- Otomatik yeniden bağlanma (3 hata sonra)
- Session ID ile giriş (şifre kullanılmaz)

## Config

`config.py` dosyasında veya çevre değişkenleri ile:
- `INSTAGRAM_USERNAME`
- `IG_SESSION_ID`
- `GROQ_API_KEY`

## Puan Sistemi
- Sayı tahmin kazan: +3 puan
- Adam asmaca kazan: +5 puan
- Trivia doğru: +2 puan
- Anagram doğru: +2 puan
- Taş Kağıt Makas kazan: +1 puan
- Matematik doğru: +1 puan
- Emoji quiz doğru: +1 puan
