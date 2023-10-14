import cv2
import requests
import pytesseract
import os
import easyocr

from PIL import Image
from langchain.chat_models import ChatOpenAI

def image_menu_search(image_url):
    if not os.path.exists("images"):
        os.mkdir("images")
    img_path = "images/image.jpg"
    with open(img_path, 'wb') as f:
        f.write(requests.get(image_url).content)
    image_data = extract_image_data(img_path)
    return image_data

def extract_image_data(img_path):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(img_path, detail = 0)
    joined_result = " ".join(result)
    return joined_result

if __name__ == "__main__":
    print(image_menu_search("https://imenupro.com/img/menu-template-steakhouse.png"))
