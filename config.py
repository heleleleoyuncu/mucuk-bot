import os

IG_USERNAME = os.environ.get("IG_USERNAME", "")
IG_PASSWORD = os.environ.get("IG_PASSWORD", "")
IG_SESSION_ID = os.environ.get("IG_SESSION_ID", "")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
BOT_OWNER = os.environ.get("BOT_OWNER", "")
PREFIX = "!"
MAX_HISTORY = 10
SCORES_FILE = "data/scores.json"
MEMORIES_FILE = "data/memories.json"
SPAM_COOLDOWN = 3
