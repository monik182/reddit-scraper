import json
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

input_dir = Path("output_reddit_posts")


def generate_youtube_metadata(post_path, output_path):
    with open(post_path, "r", encoding="utf-8") as file:
        post_data = json.load(file)

    post_title = post_data.get("title", "")
    post_content = post_data.get("selftext", "")

    messages = [
        {"role": "system", "content": "You are a youtube video creator."},
        {
            "role": "user",
            "content": (
                f"The following is a Reddit post titled '{post_title}':\n\n"
                f"{post_content}\n\n"
                "Generate a short summary of at most 5 lines for a YouTube video based on this post, and provide related tags."
            ),
        },
    ]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_completion_tokens=150,
        temperature=0.7,
        n=1,
    )

    response_text = response.choices[0].message.content.strip()

    summary, tags = response_text.split("**Tags:**") if "**Tags:**" in response_text else (response_text, "")
    tags_list = [tag.strip() for tag in tags.replace("#", "").split(" ") if tag.strip() and tag.isalnum()]


    metadata = {
        "title": post_title,
        "summary": summary.strip().replace("\n", " ").replace("**Video Summary:**", ""),
        "tags": tags_list
    }
    with open(output_path, "w", encoding="utf-8") as metadata_file:
        json.dump(metadata, metadata_file, indent=4)

    return metadata
