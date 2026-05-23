from groq import Groq
from config import GROQ_API_KEY, MAX_HISTORY

client = Groq(api_key=GROQ_API_KEY)

# Thread bazlı sohbet geçmişi
_histories: dict[str, list] = {}

SYSTEM_PROMPT = """Sen "Mucuk Bot" adında eğlenceli, zeki ve biraz yaramaz bir Instagram botusun.
- Türkçe konuş, genç ve samimi bir dil kullan
- Kısa cevap ver (max 3-4 cümle), uzatma
- Bazen emoji kullan ama abartma
- Espri yapabilirsin, biraz sinir bozucu olmak güzel
- Sana hakaret edilirse nazikçe geri ver
- Atatürk, din, siyaset gibi hassas konularda tarafsız kal
"""

def ask_ai(prompt: str, thread_id: str = "global") -> str:
    history = _histories.setdefault(thread_id, [])
    history.append({"role": "user", "content": prompt})
    if len(history) > MAX_HISTORY:
        history[:] = history[-MAX_HISTORY:]
    try:
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + history,
            max_tokens=350,
            temperature=0.85,
        )
        reply = resp.choices[0].message.content.strip()
        history.append({"role": "assistant", "content": reply})
        return reply
    except Exception as e:
        return f"⚠️ AI hatası: {e}"

def clear_history(thread_id: str) -> str:
    _histories.pop(thread_id, None)
    return "🧹 Sohbet geçmişi temizlendi!"

def ai_quick(prompt: str) -> str:
    """Geçmiş olmadan tek seferlik AI çağrısı."""
    try:
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Türkçe, kısa ve eğlenceli cevap ver."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=300,
            temperature=0.9,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ {e}"
