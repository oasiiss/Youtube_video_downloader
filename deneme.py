from yt_dlp import YoutubeDL
import re

def progress_hook(d):
    if d['status'] == 'downloading':
        percent = d['_percent_str']
        percent = re.findall(r'\d+\.\d+', percent)[0]
        with open('deneme.txt', 'a') as file:
            file.write(percent)

ydl_opts = {
    'format': 'bestaudio/best',  # En iyi ses kalitesini seçer
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',  # Ses dosyası formatı olarak MP3 seçer
        'preferredquality': '192',  # Ses kalitesini belirler (Varsayılan: 192kbps)
    }],
    'outtmpl': 'media/mp3/%(title)s.%(ext)s',  # İndirilen MP3 dosyasının çıktı yolu ve adı
    'progress_hooks': [progress_hook]
}

with YoutubeDL(ydl_opts) as ydl:
    ydl.download(['http://www.youtube.com/watch?v=BaW_jenozKc'])