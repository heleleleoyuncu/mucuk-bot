#!/bin/bash
echo "🤖 Mucuk Bot Kurulumu"
echo "─────────────────────"

# Pip kur
echo "📦 Gereksinimler kuruluyor..."
pip install -r requirements.txt -q

# Data klasörü
mkdir -p data
[ -f data/scores.json ] || echo "{}" > data/scores.json
[ -f data/memories.json ] || echo "{}" > data/memories.json

# Config kontrol
CONFIG_FILE="config.py"

get_value() {
    python3 -c "import os; exec(open('$CONFIG_FILE').read()); print(eval('$1'))" 2>/dev/null
}

echo ""
echo "⚙️  Yapılandırma"
echo "─────────────────────"

# IG_USERNAME
CUR_USER=$(get_value IG_USERNAME)
if [ -z "$CUR_USER" ] || [ "$CUR_USER" = "uwu._.mucuk" ]; then
    read -p "📱 Instagram kullanıcı adın: " IG_USERNAME
else
    IG_USERNAME=$CUR_USER
    echo "📱 Kullanıcı adı: $IG_USERNAME"
fi

# IG_SESSION_ID
CUR_SESSION=$(get_value IG_SESSION_ID)
if [ -z "$CUR_SESSION" ]; then
    read -p "🔑 Session ID: " IG_SESSION_ID
else
    IG_SESSION_ID=$CUR_SESSION
    echo "🔑 Session ID: mevcut"
fi

# GROQ_API_KEY
CUR_GROQ=$(get_value GROQ_API_KEY)
if [ -z "$CUR_GROQ" ]; then
    read -p "🤖 Groq API Key: " GROQ_API_KEY
else
    GROQ_API_KEY=$CUR_GROQ
    echo "🤖 Groq API Key: mevcut"
fi

# BOT_OWNER
CUR_OWNER=$(get_value BOT_OWNER)
if [ -z "$CUR_OWNER" ]; then
    read -p "👑 Bot sahibi kullanıcı adı: " BOT_OWNER
else
    BOT_OWNER=$CUR_OWNER
    echo "👑 Bot sahibi: $BOT_OWNER"
fi

# config.py yaz
cat > $CONFIG_FILE << PYEOF
import os

IG_USERNAME = os.environ.get("IG_USERNAME", "$IG_USERNAME")
IG_PASSWORD = os.environ.get("IG_PASSWORD", "")
IG_SESSION_ID = os.environ.get("IG_SESSION_ID", "$IG_SESSION_ID")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "$GROQ_API_KEY")
BOT_OWNER = os.environ.get("BOT_OWNER", "$BOT_OWNER")
PREFIX = "!"
MAX_HISTORY = 10
SCORES_FILE = "data/scores.json"
MEMORIES_FILE = "data/memories.json"
SPAM_COOLDOWN = 3
PYEOF

echo ""
echo "✅ Kurulum tamamlandı!"
echo "🚀 Başlatmak için: bash start.sh"

