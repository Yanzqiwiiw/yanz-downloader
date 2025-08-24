#!/bin/bash
echo "[+] Installing YANZ Downloader Tool..."
echo "[+] Credit: YanzXNexuz666xZ"

# Update package
pkg update -y
pkg upgrade -y

# Install dependencies
pkg install -y python ffmpeg git

# Install pip packages
pip install --upgrade pip
pip install requests yt-dlp

# Optional packages
pip install gdown PyGithub python-telegram-bot

# Download script
if [ ! -f "yanzkay1.py" ]; then
    echo "[+] Downloading main script..."
    # Ganti dengan link raw GitHub jika sudah diupload
    curl -O https://raw.githubusercontent.com/username/repo/main/yanz.py
fi

# Make executable
chmod +x yanz.py

echo "[+] Installation complete!"
echo "[+] Run: python yanzkay1.py"
echo "[+] atau: ./yanzkay1.py"