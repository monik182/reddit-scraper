import os
import tempfile
import yt_dlp

file_path = os.path.join(os.path.dirname(__file__), "vimeo_links.txt")
output_folder = os.path.join(os.path.dirname(__file__), "output_videos")
batch_size = 5

yt_dlp_options = {
    "format": "bestvideo+bestaudio",
    # "referer": "CHANGE YOUR REFERER HERE",
    "external_downloader": "aria2c",
    "external_downloader_args": ["-x", "16", "-s", "16", "-k", "5M", "--max-concurrent-downloads=16"],
    "outtmpl": os.path.join(output_folder, "%(title)s (%(format_id)s).%(ext)s"),
    "clean_infojson": False,
    "nooverwrites": True,
    "verbose": True,
    "tempdir": tempfile.gettempdir(),
}

os.makedirs(output_folder, exist_ok=True)

with open(file_path, "r") as file:
    video_lines = [line.strip() for line in file]

for i in range(0, len(video_lines), batch_size):
    batch_lines = video_lines[i:i + batch_size]
    ydl = yt_dlp.YoutubeDL(yt_dlp_options)

    for line in batch_lines:
        url, password = line.split("::") if "::" in line else (line, None)

        ydl.params['videopassword'] = password
        try:
            ydl.download([url])
        except Exception as e:
            print(f"Error downloading {url}: {e}")

for file_name in os.listdir(output_folder):
    file_path = os.path.join(output_folder, file_name)
    if os.path.isfile(file_path) and not file_name.lower().endswith(".mp4"):
        os.remove(file_path)
