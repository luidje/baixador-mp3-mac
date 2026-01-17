import yt_dlp
import os
import sys
import platform

# Define a funcao para obter o caminho interno do PyInstaller
def get_ffmpeg_path(filename):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, filename)

# Tenta ler o link, com suporte a fechamento repentino
try:
    video_url = input("Por favor, cole o LINK do YouTube e pressione Enter: ").strip()
except EOFError:
    sys.exit()

if not video_url:
    print("[ERRO] Nenhuma URL fornecida.")
    sys.exit()

# 2. Define as opcoes de download com "disfarce" contra bloqueio
ydl_opts = {
    'outtmpl': '%(title)s.%(ext)s',
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'ffmpeg_location': get_ffmpeg_path('ffmpeg'), 
    'compat_opts': ['no-js-runtime'],
    # Disfarces para o YouTube nao bloquear como BOT
    'http_headers': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-us,en;q=0.5',
        'Sec-Fetch-Mode': 'navigate',
    }
}

print(f"Iniciando download e conversao: {video_url}...")

try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
    print("\n[SUCESSO] O arquivo MP3 foi salvo na pasta.")
except Exception as e:
    print(f"\n[ERRO] Ocorreu um erro: {e}")

# Pausa a tela de forma segura
try:
    if platform.system() == "Windows":
        os.system("pause")
    else:
        print("\nProcesso finalizado.")
        input("Pressione Enter para fechar esta janela...")
except (EOFError, KeyboardInterrupt):
    pass
