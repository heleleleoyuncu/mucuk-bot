"""
Mucuk Bot — Ultra Mega Süper Instagram Botu
Çalıştır: python main.py
"""
import time
import traceback
from instagrapi import Client
from config import IG_SESSION_ID, IG_USERNAME, PREFIX
from commands import handle_command
from ai import ask_ai

# ── Bağlantı ──────────────────────────────────────────────────────────────────
def connect() -> Client:
    cl = Client()
    cl.delay_range = [1, 3]
    cl.login_by_sessionid(IG_SESSION_ID)
    return cl

def reconnect(cl: Client) -> Client:
    print("🔄 Yeniden bağlanılıyor...")
    try:
        cl.login_by_sessionid(IG_SESSION_ID)
        print("✅ Yeniden bağlandı!")
        return cl
    except Exception:
        print("❌ Yeniden bağlanma başarısız, 30s bekleniyor...")
        time.sleep(30)
        return connect()

# ── Ana döngü ─────────────────────────────────────────────────────────────────
def main():
    cl = connect()
    BOT_USER_ID = str(cl.user_id)
    print(f"✅ Mucuk Bot başladı! (@{IG_USERNAME} | ID: {BOT_USER_ID})")
    print(f"   Prefix: {PREFIX}  |  @ komutu: @{IG_USERNAME} <mesaj>")
    print(f"   Yardım için: {PREFIX}yardim")

    checked: dict[str, str] = {}
    error_count = 0

    while True:
        try:
            threads = cl.direct_threads(amount=20)
            for thread in threads:
                tid = thread.id
                msgs = cl.direct_messages(tid, amount=1)
                if not msgs:
                    continue
                msg = msgs[0]

                if checked.get(tid) == str(msg.id):
                    continue
                checked[tid] = str(msg.id)

                if str(msg.user_id) == BOT_USER_ID:
                    continue

                text = (msg.text or "").strip()
                if not text:
                    continue

                is_group = len(thread.users) > 1

                # Kullanıcı adını ekstra istek atmadan al
                try:
                    sender = next(
                        (u.username for u in thread.users if str(u.pk) == str(msg.user_id)),
                        str(msg.user_id)
                    )
                except Exception:
                    sender = str(msg.user_id)

                try:
                    thread_users = [u.username for u in thread.users if str(u.pk) != BOT_USER_ID]
                except Exception:
                    thread_users = []

                reply = None

                if is_group:
                    mention = f"@{IG_USERNAME}"
                    if mention.lower() in text.lower():
                        clean = text.lower().replace(mention.lower(), "").strip()
                        reply = ask_ai(clean, thread_id=tid) if clean else "Ne yapmamı istiyorsun? 😊 !yardim yaz."
                    elif text.startswith(PREFIX):
                        reply = handle_command(
                            text, tid=tid, username=sender,
                            thread_users=thread_users, user_id=str(msg.user_id)
                        )
                else:
                    if text.startswith(PREFIX):
                        reply = handle_command(
                            text, tid=tid, username=sender,
                            thread_users=thread_users, user_id=str(msg.user_id)
                        )
                    else:
                        reply = ask_ai(text, thread_id=tid)

                if reply:
                    tag = "👥 GRUP" if is_group else "👤 DM"
                    print(f"{tag} 📩 @{sender}: {text[:80]}")
                    try:
                        cl.direct_send(reply, thread_ids=[tid])
                        print(f"   ✉️  {reply[:80]}")
                    except Exception as send_err:
                        print(f"   ⚠️ Gönderme hatası: {send_err}")

            error_count = 0

        except KeyboardInterrupt:
            print("\n👋 Bot kapatıldı.")
            break
        except Exception as e:
            error_count += 1
            print(f"⚠️ Hata #{error_count}: {e}")
            if error_count >= 3:
                traceback.print_exc()
                cl = reconnect(cl)
                BOT_USER_ID = str(cl.user_id)
                error_count = 0
            time.sleep(5)

        time.sleep(0.1)

if __name__ == "__main__":
    main()
