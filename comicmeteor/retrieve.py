import requests
from bs4 import BeautifulSoup
from PIL import Image
from .descramble import descramble


def get_all_images(series_name: str, vol_num: int):
    pages = get_num_pages(series_name, vol_num)
    image_list = []
    base_url = "https://comic-meteor.jp/ptdata/" + series_name + "/"
    not_found = False
    current_count = 1

    while not not_found:
        vol_num_string = str.format(f"{vol_num:04d}")
        current_count_string = str.format(f"{current_count:04d}")
        num_base_url = base_url + vol_num_string + "/data/"
        json_request = requests.get(num_base_url + current_count_string + ".ptimg.json")
        if json_request.status_code != 404:
            json_dict = json_request.json()
            image_url = num_base_url + json_dict["resources"]["i"]["src"]
            image_request = requests.get(image_url, stream=True)
            scrambled_image = Image.open(image_request.raw)
            image_list.append(descramble(scrambled_image, json_dict))
            current_count += 1
        else:
            not_found = True

    return image_list


def get_num_pages(series_name: str, vol_num: int):
    url = "https://comic-meteor.jp/ptdata/" + series_name + "/" + f"{vol_num:04d}"
    page_request = requests.get(url)
    soup = BeautifulSoup(page_request.text, features="html.parser")
    content_div = soup.find("div", {"id": "content"})
    return len(content_div.findChildren())
