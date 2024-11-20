import re
from pathlib import Path

resources_dir = Path("resources")


def censor_word(match):
    word = match.group()
    if len(word) <= 2:
        return word[0] + '*' * (len(word) - 1)
    return word[0] + '*' * (len(word) - 2) + word[-1]


def censor_profanities(text, language="en"):
    file_path = resources_dir / f'profanity_list_{language}.txt'
    with open(file_path, 'r', encoding='utf-8') as file:
        profanities = [line.strip() for line in file if line.strip()]

    pattern = re.compile(r'\b(' + '|'.join(re.escape(word) for word in profanities) + r')\b', re.IGNORECASE)
    censored_text = pattern.sub(censor_word, text)
    return censored_text
