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
