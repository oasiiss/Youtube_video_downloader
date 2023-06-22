import json, os, time
from channels.generic.websocket import WebsocketConsumer
from pytube import YouTube
from moviepy.editor import VideoFileClip


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
                self.send(text_data=json.dumps({"status":2, "progress":10}))

                video_title = yt_video.title

                self.send(text_data=json.dumps({"status":2, "progress":20}))

                if video_format == 'mp3':
                    video = yt_video.streams.filter(only_audio=True).first()
                    self.send(text_data=json.dumps({"status":2, "progress":30}))
                    out_file = video.download(output_path='media/mp3')
                    self.send(text_data=json.dumps({"status":2, "progress":70}))
                    base, ext = os.path.splitext(out_file)
                    self.send(text_data=json.dumps({"status":2, "progress":75}))
                    new_file = base + '.mp3'
                    self.send(text_data=json.dumps({"status":2, "progress":80}))
                    os.rename(out_file, new_file)
                    self.send(text_data=json.dumps({"status":2, "progress":95}))
                    file_name = new_file.split('/')[-1].replace('\\', '/')
                    video_id = video_url.split("=")[-1]
                    self.send(text_data=json.dumps({"status":2, "progress":100}))
                    self.send(text_data=json.dumps({
                        "status": 3,
                        "video_id": video_id,
                        "file_name": file_name,
                        "message": "Video bulundu ve mp4 olarak yüklendi",
                    }))

                elif video_format == 'mp4':
                    self.send(text_data=json.dumps({"status":2, "progress":10}))
                    try:
                        self.send(text_data=json.dumps({"status":2, "progress":20}))
                        time.sleep(1)
                        self.send(text_data=json.dumps({"status":2, "progress":50}))
                        out_file = yt_video.streams.filter(progressive = True, file_extension = "mp4").first().download(output_path = "media/mp4")
                        self.send(text_data=json.dumps({"status":2, "progress":85}))
                        video_id = video_url.split("=")[-1]
                        out_file = out_file.split('/')[-1].replace("\\", "/")
                        self.send(text_data=json.dumps({"status":2, "progress":100}))
                        self.send(text_data=json.dumps({
                            "status": 1,
                            "file_name": out_file,
                            "video_id": video_id,
                        }))
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

        