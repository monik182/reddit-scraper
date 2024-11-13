from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()

client = OpenAI()


def paraphraser(text):
    prompt = (
        "You are a helpful assistant. Paraphrase the following text, maintaining its meaning and length:\n\n" + text
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    paraphrased_text = response.choices[0].message.content
    return paraphrased_text
