import json, os, time
from channels.generic.websocket import WebsocketConsumer
from pytube import YouTube
from moviepy.editor import VideoFileClip
from yt_dlp import YoutubeDL
import re


class DownloadConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

        self.send(text_data=json.dumps({
            "type":"connection_established",
            "message":"You are now connected!"
        }))

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        video_url = text_data_json["video_url"]
        video_format = text_data_json["video_format"]

        try:
            yt_video = YouTube(video_url)
            video_duration = yt_video.length
            video_duration_minutes = video_duration / 60

            if video_duration_minutes > 10:
                self.send(text_data=json.dumps({
                    "status":4,
                    "message":" Video maksimum 10 dakika olmalı"
                }))
            else:
                video_title = yt_video.title
                video_title = video_title.replace("/", "-")
                video_title = video_title.replace("\\", "-")
                video_title = video_title.replace("|", "-")
                video_title = video_title.replace("│", "-")
                video_title = video_title.replace("'", "")

                if video_format == 'mp3':
                    try:
                        def progress_hook(d):
                            if d['status'] == 'downloading':
                                percent = d['_percent_str']
                                percent = re.findall(r'\d+\.\d+', percent)[0]
                                percent = percent.replace("%", "")
                                self.send(text_data=json.dumps({"status":2, "progress":percent}))
                                

                            elif d['status'] == 'finished':
                                video_id = video_url.split("=")[-1]
                                # file_name = str(str(d['filename']).replace("\\", "/").split(".")[-2]) + ".mp3"
                                file_name = str(d["filename"]).replace("\\", "/").split(".")
                                file_name = ".".join(file_name[:-1]) + ".mp3"
                                self.send(text_data=json.dumps({
                                    "status": 3,
                                    "video_id": video_id,
                                    "file_name": file_name,
                                    "message": "Video bulundu ve mp3 olarak yüklendi",
                                }))

                        ydl_opts = {
                            'format': 'bestaudio/best',  # En iyi ses kalitesini seçer
                            'postprocessors': [{
                                'key': 'FFmpegExtractAudio',
                                'preferredcodec': 'mp3',  # Ses dosyası formatı olarak MP3 seçer
                                'preferredquality': '192',  # Ses kalitesini belirler (Varsayılan: 192kbps)
                            }],
                            'outtmpl': f'media/mp3/{video_title}.%(ext)s',  # İndirilen MP3 dosyasının çıktı yolu ve adı
                            'progress_hooks': [progress_hook]
                        }

                        with YoutubeDL(ydl_opts) as ydl:
                            ydl.download([video_url])

                    except Exception as error:
                        self.send(text_data=json.dumps({
                            "status": 4,
                            "message": error
                        }))



                elif video_format == 'mp4':

                    try:
                        def progress_hook(d):
                            if d['status'] == 'downloading':
                                percent = d['_percent_str']
                                percent = re.findall(r'\d+\.\d+', percent)[0]
                                percent = percent.replace("%", "")
                                self.send(text_data=json.dumps({"status":2, "progress":percent}))

                        def post_hook(d):
                            video_id = video_url.split("=")[-1]
                            # file_name = str(str(d['filename']).split(".")[0].replace("\\", "/")) + ".mp4"
                            file_name = d.replace("\\", "/")
                            file_name = "media/mp4/" + "/".join(file_name.split("mp4/")[1:])
                            # file_name = ".".join(file_name[:-2]).replace("\\", "/") + ".mp4"
                            self.send(text_data=json.dumps({
                                "status": 1,
                                "video_id": video_id,
                                "file_name": file_name,
                                "message": "Video bulundu ve mp4 olarak yüklendiiiii",
                            }))

                        ydl_opts = {
                            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',  # En iyi mp4 formatında videoyu seçer
                            'outtmpl': 'media/mp4/%(title)s.%(ext)s',  # İndirilen MP3 dosyasının çıktı yolu ve adı
                            'progress_hooks': [progress_hook],
                                'postprocessors': [{
                                'key': 'FFmpegVideoConvertor',
                                'preferedformat': 'mp4',  # Video formatını mp4 olarak değiştirir
                            }],
                            'post_hooks': [post_hook]
                        }

                        with YoutubeDL(ydl_opts) as ydl:
                            ydl.download([video_url])

                    except Exception as error:
                        self.send(text_data=json.dumps({
                            "status": 4,
                            "message": error
                        }))
                else:
                    self.send(text_data=json.dumps({
                        "status": 4,
                        "message": "Video formatı geçersiz"
                    }))
                    
        except Exception as error:
            self.send(text_data=json.dumps({
                "status":4,
                "message":str(error)
            }))

        