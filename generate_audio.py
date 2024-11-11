import os
from pydub import AudioSegment
import uuid
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()


def split_text_into_chunks(text, max_length=3500):
    sentences = text.split('. ')
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= max_length:
            current_chunk += sentence + ". "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + ". "
    
    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

def create_audio_chunk(text, file_name, voice="echo", speed=1.0):
    response = client.audio.speech.create(
        model="tts-1-hd",
        input=text,
        voice=voice,
        speed=speed,
    )
    response.stream_to_file(file_name)

def merge_audio_chunks(chunk_files, output_file):
    combined = AudioSegment.empty()
    for file in chunk_files:
        audio = AudioSegment.from_mp3(file)
        combined += audio
    combined.export(output_file, format="mp3")

def generate_audio(text, output_file="full_speech.mp3", voice="echo", speed=1.0):
    chunks = split_text_into_chunks(text)
    print(f"Total chunks: {len(chunks)}")
    chunk_files = []

    for _, chunk in enumerate(chunks):
        chunk_file_name = f"chunk_{uuid.uuid4().hex}.mp3"
        create_audio_chunk(chunk, chunk_file_name, voice, speed)
        chunk_files.append(chunk_file_name)
    # print(chunk_files)

    merge_audio_chunks(chunk_files, output_file)

    for file in chunk_files:
        os.remove(file)
