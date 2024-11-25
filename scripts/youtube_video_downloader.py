import os

from scripts.cookie_creator import create_cookies
import yt_dlp


def download_videos(video_list, save_folder):
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    
    if not os.path.exists(os.getenv('COOKIES_FILE')):
        create_cookies()

    for idx, video_url in enumerate(video_list):
        output_name = f"video{idx}-yt"
        
        try:
            ydl_opts = {
                'merge_output_format': 'mp4',
                'outtmpl': os.path.join(save_folder, f"{output_name}.mp4"),
                'cookies': 'cookies.txt',
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
                print(f"Downloaded: {output_name}")
        except Exception as e:
            print(f"Failed to download {video_url}: {e}")


if __name__ == "__main__":
    video_links = [
        'https://www.youtube.com/watch?v=VS3D8bgYhf4',
        'https://www.youtube.com/watch?v=XBIaqOm0RKQ',
        'https://www.youtube.com/watch?v=ZtLrNBdXT7M',
        'https://www.youtube.com/watch?v=u7kdVe8q5zs',
        'https://www.youtube.com/watch?v=uVKxtdMgJVU',
        'https://www.youtube.com/watch?v=VAGmUv___iQ',
    ]
    download_videos(video_links, "videos/input_videos")
