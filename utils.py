import json, time, urllib.request, os
from config import SCORES_FILE, MEMORIES_FILE, SPAM_COOLDOWN

# ── Anti-spam ──────────────────────────────────────────────────────────────────
_last_cmd: dict[str, float] = {}

def check_spam(user_id: str) -> bool:
    """True döndürürse spam, False ise geçebilir."""
    now = time.time()
    last = _last_cmd.get(user_id, 0)
    if now - last < SPAM_COOLDOWN:
        return True
    _last_cmd[user_id] = now
    return False

# ── Skor sistemi ───────────────────────────────────────────────────────────────
def _load_scores() -> dict:
    try:
        with open(SCORES_FILE) as f:
            return json.load(f)
    except Exception:
        return {}

def _save_scores(data: dict):
    os.makedirs(os.path.dirname(SCORES_FILE), exist_ok=True)
    with open(SCORES_FILE, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_score(username: str, points: int = 1):
    data = _load_scores()
    data[username] = data.get(username, 0) + points
    _save_scores(data)

def get_leaderboard(top: int = 10) -> str:
    data = _load_scores()
    if not data:
        return "🏆 Henüz skor yok. Oyun oyna kazanmaya başla!"
    sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)[:top]
    medals = ["🥇", "🥈", "🥉"] + ["🏅"] * 20
    lines = ["🏆 SKOR TABLOSU"]
    for i, (user, pts) in enumerate(sorted_data):
        lines.append(f"{medals[i]} {user}: {pts} puan")
    return "\n".join(lines)

def get_score(username: str) -> str:
    data = _load_scores()
    pts = data.get(username, 0)
    return f"🎯 {username}: {pts} puan"

# ── Bellek sistemi ──────────────────────────────────────────────────────────────
def _load_memories() -> dict:
    try:
        with open(MEMORIES_FILE) as f:
            return json.load(f)
    except Exception:
        return {}

def _save_memories(data: dict):
    os.makedirs(os.path.dirname(MEMORIES_FILE), exist_ok=True)
    with open(MEMORIES_FILE, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def remember(thread_id: str, text: str) -> str:
    data = _load_memories()
    lst = data.setdefault(thread_id, [])
    lst.append(text)
    if len(lst) > 20:
        lst.pop(0)
    _save_memories(data)
    return f"🧠 Hatırladım: {text}"

def show_memories(thread_id: str) -> str:
    data = _load_memories()
    lst = data.get(thread_id, [])
    if not lst:
        return "🧠 Henüz hiçbir şey hatırlamıyorum."
    lines = ["🧠 Hatırladıklarım:"] + [f"• {x}" for x in lst]
    return "\n".join(lines)

def forget_all(thread_id: str) -> str:
    data = _load_memories()
    data.pop(thread_id, None)
    _save_memories(data)
    return "🗑️ Tüm hatırladıklarımı sildim!"

# ── Hava durumu ─────────────────────────────────────────────────────────────────
def get_weather(city: str) -> str:
    try:
        city_enc = urllib.parse.quote(city)  # type: ignore[name-defined]
        url = f"https://wttr.in/{city_enc}?format=4&lang=tr"
        req = urllib.request.Request(url, headers={"User-Agent": "curl/7.68.0"})
        with urllib.request.urlopen(req, timeout=5) as r:
            return r.read().decode("utf-8").strip()
    except Exception:
        try:
            city_enc = city.replace(" ", "+")
            url = f"https://wttr.in/{city_enc}?format=%l:+%C+%t+%h+%w&lang=tr"
            req = urllib.request.Request(url, headers={"User-Agent": "curl/7.68.0"})
            with urllib.request.urlopen(req, timeout=5) as r:
                result = r.read().decode("utf-8").strip()
                return f"🌤️ {result}"
        except Exception as e:
            return f"⚠️ Hava durumu alınamadı: {city}"

import urllib.parse
