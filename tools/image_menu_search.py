import cv2
import requests
import pytesseract
import os
import easyocr

from PIL import Image
from langchain.chat_models import ChatOpenAI

def image_menu_search(img_path: str):
    image_data = extract_image_data(img_path)
    return image_data

def extract_image_data(img_path):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(img_path, detail = 0)
    joined_result = " ".join(result)
    return joined_result

if __name__ == "__main__":
    print(image_menu_search("https://imenupro.com/img/menu-template-steakhouse.png"))
