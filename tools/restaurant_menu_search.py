import requests
from bs4 import BeautifulSoup


def get_website_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to get the website content: {e}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    return find_menu_in_content(soup)


def find_menu_in_content(soup):
    likely_menus = []

    for tag in ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'div', 'span', 'href']:
        elements = soup.find_all(tag, string=lambda text: 'menu' in text.lower() if text else False)
        likely_menus.extend(elements)

    return likely_menus


def get_likely_menu(url):
    likely_options = get_website_content(url)
    print("------ Likely Options for the Restaurant Menu ------")
    print(likely_options)
    print("-------------------")
    return likely_options
