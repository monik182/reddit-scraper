import json
from scripts.youtube_upload import upload_video


output = "gs8x5u-MaliciousCompliance-20200528-160046"
video_path = f"output/{output}/{output}_final_video.mp4"
thumbnail_path = f"output/{output}/{output}_thumbnail.png"
with open(f"output/{output}/{output}_metadata.json", "r", encoding='utf-8') as file:
    metadata = json.load(file)
video_title = metadata.get("title", "Example Title")
video_description = metadata.get("summary", "This is a description of your video.")
video_tags = metadata.get("tags", [])
tags = video_tags[0].split("#")
video_tags = [tag.strip() for tag in tags if tag.strip().isalnum()]

upload_video(video_path, video_title, video_description, video_tags, thumbnail_path)
