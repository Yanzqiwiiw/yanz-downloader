# Tambahkan di awal script
def check_dependencies():
    missing = []
    
    if not check_cli("python"):
        missing.append("python")
    if not check_cli("ffmpeg"):
        missing.append("ffmpeg")
    if not check_cli("yt-dlp"):
        missing.append("yt-dlp")
    
    if missing:
        print(f"{R}❌ Dependencies missing: {', '.join(missing)}{X}")
        print(f"{Y}🔧 Auto installing...{X}")
        os.system("pkg install python ffmpeg -y")
        os.system("pip install yt-dlp requests")
        print(f"{H}✅ Dependencies installed!{X}")

# Tambahkan welcome message
def welcome():
    print(f"{H}========================================{X}")
    print(f"{H}      YANZ DOWNLOADER TOOL v1.0        {X}")
    print(f"{H}========================================{X}")
    print(f"{Y}👤 Author: YanzXNexuz666xZ{X}")
    print(f"{Y}📧 Support: YourContact@email.com{X}")
    print(f"{Y}🐙 GitHub: github.com/username{X}")
    print(f"{H}========================================{X}")
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YANZ DOWNLOADER TOOL
Author: YanzXNexuz666xZ
Description: Ultimate Social Media Downloader for Termux
Version: 1.0
"""

import os
import time
import subprocess
import datetime
import json
import shlex
import re
import requests
import sqlite3
import sys
from pathlib import Path

# ====== KONFIGURASI ======
CONFIG_FILE = os.path.expanduser("~/.yanz_config.json")
DB_FILE = os.path.expanduser("~/.yanz_database.db")
VERSION = "1.0"

# Config default
default_config = {
    "storage_type": "EXTERNAL",
    "download_dir": "/storage/emulated/0/Download/Termux_Downloads",
    "upload_method": "transfer.sh",
    "default_quality": "best",
    "auto_upload": False,
    "max_file_size": 500,
    "keep_days": 30,
    "theme": "default",
    "language": "id",
    "github_token": "",
    "github_repo": "",
    "telegram_bot_token": "",
    "telegram_chat_id": ""
}

# Load config
def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return {**default_config, **json.load(f)}
        except:
            return default_config
    return default_config

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

config = load_config()

# Setup directories
DOWNLOAD_DIR = config['download_dir']
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Warna themes
THEMES = {
    "default": {
        "H": "\033[92m", "R": "\033[91m", "Y": "\033[93m", 
        "B": "\033[94m", "M": "\033[95m", "C": "\033[96m", "X": "\033[0m"
    },
    "dark": {
        "H": "\033[32m", "R": "\033[31m", "Y": "\033[33m",
        "B": "\033[34m", "M": "\033[35m", "C": "\033[36m", "X": "\033[0m"
    },
    "neon": {
        "H": "\033[92m", "R": "\033[91m", "Y": "\033[93m",
        "B": "\033[94m", "M": "\033[95m", "C": "\033[96m", "X": "\033[0m"
    }
}

colors = THEMES[config['theme']]
H, R, Y, B, M, C, X = colors.values()

# ====== DATABASE SETUP ======
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS downloads
                 (id INTEGER PRIMARY KEY, filename TEXT, url TEXT, 
                  status TEXT, timestamp DATETIME, file_size INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS history
                 (id INTEGER PRIMARY KEY, command TEXT, 
                  timestamp DATETIME, success INTEGER)''')
    conn.commit()
    conn.close()

init_db()

def log_download(filename, url, status, file_size=0):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO downloads (filename, url, status, timestamp, file_size) VALUES (?, ?, ?, ?, ?)",
              (filename, url, status, datetime.datetime.now(), file_size))
    conn.commit()
    conn.close()

def log_command(command, success):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO history (command, timestamp, success) VALUES (?, ?, ?)",
              (command, datetime.datetime.now(), success))
    conn.commit()
    conn.close()

# ====== UTILITY FUNCTIONS ======
def welcome():
    print(f"{H}=================================================={X}")
    print(f"{H}          YANZ DOWNLOADER TOOL v{VERSION}         {X}")
    print(f"{H}=================================================={X}")
    print(f"{Y}👤 Author: YanzXNexuz666xZ{X}")
    print(f"{Y}📧 GitHub: github.com/YanzXNexuz666xZ{X}")
    print(f"{Y}🐍 Powered by Python & yt-dlp{X}")
    print(f"{H}=================================================={X}")

def banner():
    os.system("clear")
    welcome()
    print(f"""{R}
      ██╗   ██╗ █████╗ ███╗   ██╗███████╗
      ╚██╗ ██╔╝██╔══██╗████╗  ██║╚══███╔╝
       ╚████╔╝ ███████║██╔██╗ ██║  ███╔╝
        ╚██╔╝  ██╔══██║██║╚██╗██║ ███╔╝
         ██║   ██║  ██║██║ ╚████║███████╗
         ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝
 ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈╭╮╮╱▔▔▔▔╲╭╭╮┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
 ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈ ╰╲╲▏▂╲╱▂▕╱╱╯┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
 ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈╲▏▇▏▕▇▕╱┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
 ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈ ╱╲▔▕▍▔╱╲┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
 ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈ ╭╱╱ {B}▕╋╋╋╋▏╲╲╮┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
                  ╰╯╯┈╲▂▂╱┈╰╰╯
 {H}╔═══════════════════════════════════════════╗
 ║          {Y}TIKTOK {R}•{Y} INSTAGRAM {R}•{Y} SPOTIFY{H}       ║
 ║               DOWNLOADER TOOL               ║
 ║         {B}Creditz : {R}YanzXNexuz666xZ{H}         ║
 ╚═══════════════════════════════════════════╝
    {X}Lokasi: {B}{DOWNLOAD_DIR}{X} | Theme: {B}{config['theme']}{X}
    {X}Quality: {B}{config['default_quality']}{X} | Auto Upload: {B}{config['auto_upload']}{X}
""")

def menu():
    print(f"\n{Y}📥 DOWNLOAD MENU:{X}")
    print(f"{Y}[1]{X} TikTok Video")
    print(f"{Y}[2]{X} Instagram Video/Reels")
    print(f"{Y}[3]{X} Spotify → MP3/M4A")
    print(f"{Y}[4]{X} YouTube Video")
    print(f"{Y}[5]{X} Facebook Video")
    print(f"{Y}[6]{X} Twitter Video")
    print(f"\n{Y}⚙️  SETTINGS MENU:{X}")
    print(f"{Y}[7]{X} Ganti Kualitas")
    print(f"{Y}[8]{X} Ganti Metode Upload")
    print(f"{Y}[9]{X} Ganti Lokasi Penyimpanan")
    print(f"{Y}[10]{X} Upload File External")
    print(f"{Y}[11]{X} History Download")
    print(f"{Y}[12]{X} Cleanup Files")
    print(f"{Y}[13]{X} Settings")
    print(f"{Y}[14]{X} 🔍 Debug Telegram")
    print(f"{Y}[15]{X} 📢 Check Update")
    print(f"{Y}[16]{X} 💌 Send Feedback")
    print(f"{Y}[0]{X} Keluar")

def ts():
    return datetime.datetime.now().strftime("%Y-%m-d_%H%M%S")

def check_cli(name):
    return subprocess.call(f"command -v {shlex.quote(name)} >/dev/null 2>&1", shell=True) == 0

def ytdlp_cmd():
    return "yt-dlp" if check_cli("yt-dlp") else "python -m yt_dlp"

def sanitize_filename(name):
    name = re.sub(r"[\\/:*?\"<>|]+", "_", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name[:100]

def get_file_size(file_path):
    if os.path.exists(file_path):
        size = os.path.getsize(file_path) / (1024 * 1024)
        return round(size, 2)
    return 0

def check_file_size(file_path):
    size = get_file_size(file_path)
    if size < 0.1:
        print(f"{Y}⚠️  File sangat kecil ({size}MB), mungkin gagal{X}")
        return False
    elif size > config['max_file_size']:
        print(f"{R}❌ File terlalu besar ({size}MB){X}")
        return False
    return True

def check_dependencies():
    missing = []
    
    if not check_cli("python"):
        missing.append("python")
    if not check_cli("ffmpeg"):
        missing.append("ffmpeg")
    if not check_cli("yt-dlp"):
        missing.append("yt-dlp")
    
    if missing:
        print(f"{R}❌ Dependencies missing: {', '.join(missing)}{X}")
        print(f"{Y}🔧 Auto installing...{X}")
        os.system("pkg install python ffmpeg -y")
        os.system("pip install yt-dlp requests")
        print(f"{H}✅ Dependencies installed!{X}")
        return False
    return True

# ====== UPLOAD METHODS ======
def upload_transfer_sh(file_path):
    if not os.path.exists(file_path):
        print(f"{R}❌ File tidak ditemukan.{X}")
        return None
        
    file_size = get_file_size(file_path)
    if file_size > 100:
        print(f"{R}❌ File terlalu besar ({file_size}MB). Max 100MB.{X}")
        return None
        
    print(f"{Y}⏳ Upload ke transfer.sh...{X}")
    try:
        with open(file_path, 'rb') as f:
            response = requests.post(
                'https://transfer.sh/',
                files={'file': f},
                timeout=60,
                headers={'User-Agent': 'Mozilla/5.0'}
            )
        if response.status_code == 200:
            download_url = response.text.strip()
            print(f"{H}✅ Link: {B}{download_url}{X}")
            return download_url
        else:
            print(f"{R}❌ Upload gagal. Code: {response.status_code}{X}")
    except Exception as e:
        print(f"{R}❌ Error: {e}{X}")
    return None

def upload_gdrive(file_path):
    if not os.path.exists(file_path):
        print(f"{R}❌ File tidak ditemukan.{X}")
        return None
        
    print(f"{Y}⏳ Upload ke Google Drive...{X}")
    
    if check_cli("gdown"):
        try:
            cmd = f"gdown --upload {shlex.quote(file_path)}"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120)
            if result.returncode == 0:
                print(f"{H}✅ Berhasil upload ke Google Drive{X}")
                for line in result.stdout.split('\n'):
                    if 'https://drive.google.com' in line:
                        print(f"{H}📎 Link: {B}{line.strip()}{X}")
                        return line.strip()
                return "Google Drive Upload Success"
            else:
                print(f"{R}❌ Gagal: {result.stderr}{X}")
        except subprocess.TimeoutExpired:
            print(f"{R}❌ Timeout saat upload{X}")
        except Exception as e:
            print(f"{R}❌ Error: {e}{X}")
    else:
        print(f"{R}❌ gdown tidak terinstall.{X}")
        print(f"{B}Install: pip install gdown{X}")
    return None

def upload_github(file_path):
    if not os.path.exists(file_path):
        print(f"{R}❌ File tidak ditemukan.{X}")
        return None
        
    if not config['github_token'] or not config['github_repo']:
        print(f"{R}❌ Token/Repo GitHub belum dikonfig{X}")
        return None
        
    try:
        from github import Github
    except ImportError:
        print(f"{R}❌ Install PyGithub: pip install PyGithub{X}")
        return None
        
    print(f"{Y}⏳ Upload ke GitHub...{X}")
    
    try:
        g = Github(config['github_token'])
        repo = g.get_repo(config['github_repo'])
        file_name = os.path.basename(file_path)
        
        with open(file_path, 'rb') as f:
            content = f.read()
        
        try:
            contents = repo.get_contents(file_name)
            result = repo.update_file(contents.path, f"Update {file_name}", content, contents.sha)
            print(f"{H}✅ File diperbarui di GitHub{X}")
        except:
            result = repo.create_file(file_name, f"Upload {file_name}", content, branch="main")
            print(f"{H}✅ File diupload ke GitHub{X}")
        
        download_url = f"https://github.com/{config['github_repo']}/blob/main/{file_name}?raw=true"
        print(f"{H}📎 Link: {B}{download_url}{X}")
        return download_url
        
    except Exception as e:
        print(f"{R}❌ Error GitHub: {e}{X}")
        return None

def upload_telegram(file_path):
    if not config['telegram_bot_token']:
        print(f"{R}❌ Token bot belum diatur{X}")
        return None
        
    if not config['telegram_chat_id']:
        print(f"{R}❌ Chat ID belum diatur{X}")
        return None
        
    print(f"{Y}⏳ Upload ke Telegram...{X}")
    
    try:
        url = f"https://api.telegram.org/bot{config['telegram_bot_token']}/sendDocument"
        
        with open(file_path, 'rb') as f:
            files = {'document': f}
            data = {'chat_id': config['telegram_chat_id']}
            
            response = requests.post(url, files=files, data=data, timeout=60)
            result = response.json()
            
            if result['ok']:
                print(f"{H}✅ Berhasil upload ke Telegram{X}")
                return "Telegram Upload Success"
            else:
                error_msg = result.get('description', 'Unknown error')
                print(f"{R}❌ Gagal upload: {error_msg}{X}")
                
    except Exception as e:
        print(f"{R}❌ Error: {e}{X}")
        
    return None

def upload_file(file_path):
    methods = {
        "transfer.sh": upload_transfer_sh,
        "gdrive": upload_gdrive,
        "github": upload_github,
        "telegram": upload_telegram
    }
    
    if config['upload_method'] in methods:
        return methods[config['upload_method']](file_path)
    else:
        print(f"{R}❌ Method upload tidak valid{X}")
        return None

# ====== DEBUG TELEGRAM ======
def debug_telegram():
    print(f"{Y}🔍 DEBUG TELEGRAM BOT{X}")
    
    if not config['telegram_bot_token']:
        print(f"{R}❌ Token bot belum diatur{X}")
        print(f"{Y}💡 Masukkan token bot dulu di settings{X}")
        return
    
    try:
        url = f"https://api.telegram.org/bot{config['telegram_bot_token']}/getMe"
        response = requests.get(url, timeout=10)
        bot_info = response.json()
        
        if bot_info['ok']:
            bot_name = bot_info['result']['first_name']
            print(f"{H}✅ Bot Valid: {bot_name}{X}")
        else:
            print(f"{R}❌ Token invalid: {bot_info['description']}{X}")
            return
    except Exception as e:
        print(f"{R}❌ Error test bot: {e}{X}")
        return
    
    try:
        print(f"{Y}⏳ Mencari chat ID...{X}")
        url = f"https://api.telegram.org/bot{config['telegram_bot_token']}/getUpdates"
        response = requests.get(url, timeout=30)
        data = response.json()
        
        if data['ok'] and data['result']:
            print(f"\n{Y}📋 DAFTAR CHAT YANG TERDETEKSI:{X}")
            for i, update in enumerate(data['result'], 1):
                if 'message' in update:
                    chat = update['message']['chat']
                    chat_id = chat['id']
                    chat_type = chat['type']
                    
                    if chat_type == 'private':
                        chat_name = chat.get('first_name', 'Private Chat')
                        print(f"{Y}{i}. 👤 {chat_name} {B}(ID: {chat_id}){X}")
                    elif chat_type == 'group':
                        chat_name = chat.get('title', 'Group')
                        print(f"{Y}{i}. 👥 {chat_name} {B}(ID: {chat_id}){X}")
                    
                elif 'channel_post' in update:
                    chat = update['channel_post']['chat']
                    chat_id = chat['id']
                    chat_name = chat.get('title', 'Channel')
                    print(f"{Y}{i}. 📢 {chat_name} {B}(ID: {chat_id}){X}")
                    
            print(f"\n{H}💡 CARA PAKAI:{X}")
            print(f"{Y}1. Pilih chat ID yang ingin digunakan{X}")
            print(f"{Y}2. Masukkan chat ID ke settings{X}")
            print(f"{Y}3. Test kirim file{X}")
            
        else:
            print(f"{R}❌ Tidak ada chat yang terdeteksi{X}")
            print(f"{Y}💡 Kirim pesan '/start' ke bot dulu!{X}")
            print(f"{Y}💡 Pastikan bot sudah diadd ke group/channel{X}")
            
    except Exception as e:
        print(f"{R}❌ Error: {e}{X}")

# ====== DOWNLOAD FUNCTIONS ======
def download_video(url, platform, quality=None):
    if not check_cli("ffmpeg"):
        print(f"{R}❌ Install ffmpeg dulu: pkg install ffmpeg{X}")
        return None
        
    quality = quality or config['default_quality']
    quality_map = {
        "best": "bestvideo+bestaudio/best",
        "hd": "bestvideo[height<=1080]+bestaudio/best",
        "sd": "bestvideo[height<=720]+bestaudio/best",
        "low": "worst"
    }
    quality_cmd = quality_map.get(quality, "best")
    
    out_name = f"{platform}_{ts()}.mp4"
    out_path = os.path.join(DOWNLOAD_DIR, out_name)
    
    cmd = (
        f'{ytdlp_cmd()} -f "{quality_cmd}" '
        f'--merge-output-format mp4 '
        f'--continue --no-overwrites '
        f'--progress --newline '
        f'-o "{out_path}" {shlex.quote(url)}'
    )
    
    print(f"{Y}⏳ Download {platform} ({quality})...{X}")
    print(f"{C}📁 Output: {out_name}{X}")
    
    try:
        start_time = time.time()
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        
        for line in process.stdout:
            if 'ETA' in line or '%' in line:
                print(f"{C}{line.strip()}{X}", end='\r')
        
        process.wait()
        end_time = time.time()
        
        if os.path.exists(out_path) and check_file_size(out_path):
            file_size = get_file_size(out_path)
            duration = round(end_time - start_time, 2)
            print(f"\n{H}✅ Selesai! {file_size}MB ({duration}s){X}")
            log_download(out_name, url, "success", file_size)
            return out_path
        else:
            print(f"\n{R}❌ Download gagal{X}")
            log_download(out_name, url, "failed")
            
    except Exception as e:
        print(f"\n{R}❌ Error: {e}{X}")
        log_download(out_name, url, "error")
    
    return None

def download_audio(url, format="mp3"):
    if not check_cli("ffmpeg"):
        print(f"{R}❌ Install ffmpeg dulu: pkg install ffmpeg{X}")
        return None
        
    out_name = f"audio_{ts()}.{format}"
    out_path = os.path.join(DOWNLOAD_DIR, out_name)
    
    cmd = (
        f'{ytdlp_cmd()} -x --audio-format {format} '
        f'--audio-quality 0 '
        f'--progress --newline '
        f'-o "{out_path}" {shlex.quote(url)}'
    )
    
    print(f"{Y}⏳ Download audio ({format})...{X}")
    
    try:
        start_time = time.time()
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        
        for line in process.stdout:
            if 'ETA' in line or '%' in line:
                print(f"{C}{line.strip()}{X}", end='\r')
        
        process.wait()
        end_time = time.time()
        
        if os.path.exists(out_path) and check_file_size(out_path):
            file_size = get_file_size(out_path)
            duration = round(end_time - start_time, 2)
            print(f"\n{H}✅ Selesai! {file_size}MB ({duration}s){X}")
            log_download(out_name, url, "success", file_size)
            return out_path
        else:
            print(f"\n{R}❌ Download gagal{X}")
            log_download(out_name, url, "failed")
            
    except Exception as e:
        print(f"\n{R}❌ Error: {e}{X}")
        log_download(out_name, url, "error")
    
    return None

def download_spotify(url):
    try:
        response = requests.get("https://open.spotify.com/oembed", 
                               params={"url": url}, timeout=10)
        data = response.json()
        title = data.get("title", "").strip()
        artist = data.get("author_name", "").strip()
        
        if artist and artist.lower() not in title.lower():
            query = f"{artist} - {title}"
        else:
            query = title
            
        print(f"{Y}🔎 Mencari: {B}{query}{X}")
        
        yt_url = f"ytsearch1:{query}"
        return download_audio(yt_url, "mp3")
        
    except Exception as e:
        print(f"{R}❌ Gagal mendapatkan info Spotify: {e}{X}")
        return download_audio(url, "mp3")

# ====== UPDATE & FEEDBACK ======
def check_update():
    try:
        response = requests.get("https://raw.githubusercontent.com/YanzXNexuz666xZ/yanz-downloader/main/version.txt", timeout=10)
        latest_version = response.text.strip()
        
        if VERSION != latest_version:
            print(f"{Y}🔄 Update available: v{latest_version}{X}")
            print(f"{Y}💡 Run: git pull https://github.com/YanzXNexuz666xZ/yanz-downloader{X}")
            return True
    except:
        pass
    print(f"{H}✅ You have the latest version (v{VERSION}){X}")
    return False

def send_feedback():
    print(f"{Y}💌 Kirim Feedback ke Developer{X}")
    message = input(f"{Y}Pesan kamu: {X}")
    
    if message:
        print(f"{H}✅ Terima kasih atas feedbacknya!{X}")
        print(f"{Y}📧 Untuk bug reports, email: yanzdeveloper@example.com{X}")
    else:
        print(f"{R}❌ Pesan tidak boleh kosong{X}")

# ====== SETTINGS MENU ======
def change_quality():
    print(f"\n{Y}🎬 PILIH KUALITAS:{X}")
    print(f"{Y}[1]{X} Best (Auto)")
    print(f"{Y}[2]{X} HD (1080p)")
    print(f"{Y}[3]{X} SD (720p)") 
    print(f"{Y}[4]{X} Low (240p)")
    
    choice = input(f"{B}>>> {X}").strip()
    qualities = {"1": "best", "2": "hd", "3": "sd", "4": "low"}
    
    if choice in qualities:
        config['default_quality'] = qualities[choice]
        save_config(con
