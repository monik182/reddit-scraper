    
import json
import random
from pathlib import Path

from generate_audio import generate_audio

from main import load_logged_video_ids

from scraper import create_audio, translate_text

output_dir = Path("output_test")
root_dir = Path(".")
reddit_output_dir = Path("output_reddit_posts")
output_dir.mkdir(exist_ok=True)


def main():
    subreddit_name = "FamilySecrets"
    logged_video_ids = load_logged_video_ids()

    scraped_posts = list(reddit_output_dir.glob("*.json"))

    posts_without_videos = [post for post in scraped_posts if post.stem not in logged_video_ids and subreddit_name in post.stem]
    selected_post = random.choice(posts_without_videos)
    post_id = selected_post.stem
    output_folder = output_dir / post_id
    output_folder.mkdir(exist_ok=True)

    audio_path = output_folder / f"{post_id}.mp3"
    with open(selected_post, "r", encoding="utf-8") as file:
        post_data = json.load(file)
        content = post_data.get("selftext", "")
        title = post_data.get("title", "")
        id = post_data.get("id", "")
        
        print(f"ID: {id}")
        full_text = title + "\n" + content
        # translated_text = translate_text(full_text, "es")
        # create_audio(translated_text, str(audio_path), "nova")
        # create_audio(full_text, str(audio_path), "echo", 1.2)
        generate_audio(full_text, str(audio_path), "echo", 1.2)

if __name__ == "__main__":
    main()
