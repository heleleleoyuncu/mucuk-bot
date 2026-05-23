#!/bin/bash
echo "🔧 Mucuk Bot kurulumu başlıyor..."
pip install -r requirements.txt -q
mkdir -p data
[ -f data/scores.json ] || echo "{}" > data/scores.json
[ -f data/memories.json ] || echo "{}" > data/memories.json
echo "✅ Kurulum tamamlandı! Başlatmak için: bash start.sh"
