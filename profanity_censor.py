import re


def censor_word(match):
    word = match.group()
    if len(word) <= 2:
        return word[0] + '*' * (len(word) - 1)
    return word[0] + '*' * (len(word) - 2) + word[-1]


def censor_profanities(text, language="en"):
    with open(f'profanity_list_{language}.txt', 'r', encoding='utf-8') as file:
        profanities = [line.strip() for line in file if line.strip()]

    pattern = re.compile(r'\b(' + '|'.join(re.escape(word) for word in profanities) + r')\b', re.IGNORECASE)
    censored_text = pattern.sub(censor_word, text)
    return censored_text
