import requests
from bs4 import BeautifulSoup

CHAR_LIMIT = 4000


def parse_menu_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to get the website content: {e}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    texts = soup.stripped_strings

    text = []

    tags = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'div', 'span', 'li']

    text = ""
    for tag in tags:
        for element in soup.find_all(tag):
            # Append text and ensure it does not exceed the character limit
            text += element.get_text(strip=True) + " "
            if len(text) >= CHAR_LIMIT:
                return text[:CHAR_LIMIT]

    return text
