import os
import praw

from dotenv import load_dotenv
from pathlib import Path
from openai import OpenAI

import whisper
# Initialize Whisper model (you need to have whisper installed and configured properly)
# Whisper model sizes: "tiny, base, small, medium, large
whisper_model = whisper.load_model("large")
load_dotenv()

client = OpenAI()

reddit = praw.Reddit(
    client_id=os.getenv('REDDIT_CLIENT_ID'),
    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
    user_agent=os.getenv('REDDIT_USER_AGENT')
)


def translate_text(text, target_language="es"):
    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": f"Translate the following text to {target_language}:\n{text}"}
    ],
    max_tokens=1000,
    temperature=0.3)
    return response.choices[0].message.content

def create_audio(text, file_name="speech.mp3"):
    speech_file_path = Path(__file__).parent / file_name
    response = client.audio.speech.create(
        model="tts-1",
        # voice="alloy",
        voice="echo",
        input=text
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


def format_time(seconds):
    hours, remainder = divmod(int(seconds), 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{hours:02}:{minutes:02}:{int(seconds):02},{milliseconds:03}"


def generate_cc(audio_path):
    result = whisper_model.transcribe(audio_path)
    segments = result['segments']

    cc_lines = []
    for segment in segments:
        start = segment['start']
        end = segment['end']
        text = segment['text']
        cc_lines.append(f"{format_time(start)} --> {format_time(end)}\n{text}\n")

    cc_file_path = Path(audio_path).with_suffix(".srt")
    with open(cc_file_path, "w") as cc_file:
        cc_file.writelines(cc_lines)


def main():
    url = 'https://www.reddit.com/r/ChatGPT/comments/1glqv2o/chatgpt_saved_my_life_and_im_still_freaking_out/'
    post = scrape_post(url)

    id = post['id']
    full_text = post['title'] + post['content']
    target_language = "es-419"
    # translated_text = translate_text(full_text, target_language)

    title = post['title'].replace(" ", "_").lower()
    clean_title = ''.join(e for e in title if e.isalnum() or e == "_").lower()
    file_name = f"{id}_en_{clean_title}.mp3"
    translate_text_file_name = f"{id}_{target_language}_{clean_title}.mp3"

    # print(file_name)
    # print(translate_text_file_name)
    # create_audio(full_text, file_name)
    # create_audio(translated_text, translate_text_file_name)
    # generate_cc(file_name)
    generate_cc("en.mp3")


if __name__ == "__main__":
    main()
