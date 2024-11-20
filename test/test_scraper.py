import os
import praw

from dotenv import load_dotenv
from pathlib import Path
from openai import OpenAI
import whisper

# Initialize Whisper model (you need to have whisper installed and configured properly)
# Whisper model sizes: "tiny, base, small, medium, large
whisper_model = whisper.load_model("base")

load_dotenv()

client = OpenAI()

use_openai = False


reddit = praw.Reddit(
    client_id=os.getenv('REDDIT_CLIENT_ID'),
    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
    user_agent=os.getenv('REDDIT_USER_AGENT')
)


def translate_text(text, target_language="en"):
    response = client.chat.completions.create(
    # model="gpt-3.5-turbo",
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": f"Translate the following text to {target_language}:\n{text}"}
    ],
    max_tokens=1000,
    temperature=0.3)
    return response.choices[0].message.content

def create_audio(text, file_name="speech.mp3", voice="echo", speed=1.0):
    speech_file_path = Path(__file__).parent / file_name

    response = client.audio.speech.create(
        model="tts-1-hd",
        input=text,
        voice=voice,
        speed=speed,
    )

    response.stream_to_file(speech_file_path)


def scrape_post(url):
    submission = reddit.submission(url=url)
    print(submission)
    submission_id = submission.id
    post_data = {
        'id': submission_id,
        'title': submission.title,
        'content': submission.selftext
    }
    return post_data


# def main():
#     url = 'https://www.reddit.com/r/ChatGPT/comments/1glqv2o/chatgpt_saved_my_life_and_im_still_freaking_out/'
#     post = scrape_post(url)

#     post_id = post['id']
#     full_text = post['title'] + post['content']
#     target_language = "es-419"

#     title = post['title'].replace(" ", "_").lower()
#     clean_title = ''.join(e for e in title if e.isalnum() or e == "_").lower()
#     file_name = f"{id}_en_{clean_title}.mp3"
#     translate_text_file_name = f"{id}_{target_language}_{clean_title}.mp3"

#     if use_openai:
#         translated_text = translate_text(full_text, target_language)
#         create_audio(full_text, file_name)
#         create_audio(translated_text, translate_text_file_name)
#         generate_cc(file_name)
#         generate_cc(translate_text_file_name, target_language)
#     generate_cc("en.mp3", "es")
