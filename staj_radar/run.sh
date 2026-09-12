#!/bin/bash

echo "🚀 Staj Radar Uygulaması Başlatılıyor..."
cd "$(dirname "$0")"

# Open default web browser after 2 seconds
(sleep 2 && open "http://localhost:5050") &

# Start Flask server
python3 app.py
