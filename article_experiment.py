import json
from pathlib import Path

from scraper import generate_cc

from generate_audio import generate_audio
from paraphraser import paraphraser
from generate_thumbnail import generate_thumbnail
from generate_video import generate_video
from youtube_metadata import generate_youtube_metadata



output_dir = Path("output_articles")
root_dir = Path(".")
video_input_dir = Path("output_videos")
thumbnail_output_dir = Path("output_thumbnails")
output_dir.mkdir(exist_ok=True)
template_image = root_dir / "template_image.png"
audio_path = output_dir / "article.mp3"
metadata_path = output_dir / "article_metadata.json"
output_video_path = output_dir / "article_final_video.mp4"


def main():
    with open("article.json", "r", encoding='utf-8') as file:
        article = json.load(file)
        paraphrased_title = paraphraser(article.get("title", ""))
        paraphrased_content = paraphraser(article.get("selftext", ""))
        full_text = f"{paraphrased_title}\n\n{paraphrased_content}"
        print(full_text)
        generate_audio(full_text, str(audio_path), "nova")
        cc_path = generate_cc(str(audio_path))
        video_files = list(video_input_dir.glob("*.mp4"))
        selected_video = video_files[0]
        generate_thumbnail(paraphrased_title, template_image, str(output_dir / "article_thumbnail.png"))
        generate_youtube_metadata("article.json", metadata_path)
        generate_video(str(selected_video), str(audio_path), str(output_video_path), str(cc_path))


if __name__ == "__main__":
    main()