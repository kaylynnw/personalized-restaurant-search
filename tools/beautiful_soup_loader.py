import requests
from bs4 import BeautifulSoup


def get_website_content(url):
    try:
        # Make a GET request to the URL
        response = requests.get(url)
        # Check if the request was successful (Status Code 200)
        response.raise_for_status()
    except requests.RequestException as e:
        # Handle request errors
        print(f"Failed to get the website content: {e}")
        return None

    # Parse the website content with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    return find_menu_in_content(soup)


def find_menu_in_content(soup):
    likely_menus = []

    # Look for the word "menu" in various HTML elements
    for tag in ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'div', 'span', 'href']:
        elements = soup.find_all(tag, string=lambda text: 'menu' in text.lower() if text else False)
        likely_menus.extend(elements)

    # Extract and print the text from the elements
    for element in likely_menus:
        print(f"{element.name}: {element.get_text(strip=True)}")

    # Return the likely menu elements
    return likely_menus


def get_likely_menu(url):
    likely_options = get_website_content(url)
    print(likely_options)
    return likely_options
