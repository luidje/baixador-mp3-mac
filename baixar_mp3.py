import yt_dlp
import os
import sys
import platform

# Define a funcao para obter o caminho interno do PyInstaller
def get_ffmpeg_path(filename):
    # Verifica se o programa foi empacotado pelo PyInstaller
    if getattr(sys, 'frozen', False):
        # O caminho interno aponta para a pasta temporaria _MEI...
        base_path = sys._MEIPASS
    else:
        # Se nao estiver empacotado, usa o diretorio atual para testes
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    # Retorna o caminho completo para o executavel do FFmpeg/FFprobe
    return os.path.join(base_path, filename)

# Define o link do YouTube pedindo ao usuario
video_url = input("Por favor, cole o NOVO LINK do YouTube e pressione Enter: ").strip()

# Se o usuario nao fornecer um link, encerra o script
if not video_url:
    print("[ERRO] Nenhuma URL fornecida. Encerrando o programa.")
    sys.exit() # sys.exit é suficiente para fechar sem 'pause'

# 2. Define as opcoes de download
ydl_opts = {
    'outtmpl': '%(title)s.mp3',
    'format': 'bestaudio/best',

    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],

    # CORREÇÃO: Usamos 'ffmpeg' sem .exe
    'ffmpeg_location': get_ffmpeg_path('ffmpeg'), 
    
    'compat_opts': ['no-js-runtime'], 
}

print(f"Iniciando download e conversao do audio: {video_url}...")

try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    print("\n[SUCESSO] Conversao concluida. O arquivo MP3 foi salvo na pasta.")

except Exception as e:
    print(f"\n[ERRO] Ocorreu um erro durante o download: {e}")

# Pausa a tela de forma multiplataforma
if platform.system() == "Windows":
    os.system("pause")
else:
    # Comando de pausa para Mac/Linux
    input("Pressione Enter para continuar...")