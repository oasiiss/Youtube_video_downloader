import json, os
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
                    "message":"video longer than 10 minutes"
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
                        "message": "Video found and downloaded as audio",
                    }))

                elif video_format == 'mp4':
                    video_stream = yt_video.streams.filter(progressive=True).first()
                    video_stream.download(output_path='media/mp4')
                    self.send(text_data=json.dumps({
                        "status": 1,
                        "message": "Video found and downloaded as video"
                    }))

                else:
                    self.send(text_data=json.dumps({
                        "status": 3,
                        "message": "Invalid video format"
                    }))
        except Exception as error:
            self.send(text_data=json.dumps({
                "status":4,
                "message":str(error)
            }))

        