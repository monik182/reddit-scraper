import json
import os
from dotenv import load_dotenv

load_dotenv()

def create_cookies():
    cookies = os.getenv('COOKIES')
    COOKIES_FILE = os.getenv('COOKIES_FILE', "cookies.txt")

    if not cookies:
        return
    
    cookies = json.loads(cookies)

    print(cookies)
    print(COOKIES_FILE)

    with open(COOKIES_FILE, "w") as f:
        for cookie in cookies:
            domain = cookie.get("domain", ".youtube.com")
            flag = "TRUE" if domain.startswith(".") else "FALSE"
            path = cookie.get("path", "/")
            secure = "TRUE" if cookie.get("secure") else "FALSE"
            expiration = "2147483647"
            name = cookie["name"]
            value = cookie["value"]
            f.write(f"{domain}\t{flag}\t{path}\t{secure}\t{expiration}\t{name}\t{value}\n")
