import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, wait
from PIL import Image
from .descramble import descramble


def get_all_images(series_name: str, vol_num: int):
    pages = get_num_pages(series_name, vol_num)
    image_list = []
    base_url = "https://comic-meteor.jp/ptdata/" + series_name + "/" + f"{vol_num:04d}" + "/data/"
    image_futures = []

    with ThreadPoolExecutor() as pool:

        for page_num in range(1, pages + 1):

            image_futures.append(pool.submit(get_image, base_url, page_num))

    wait(image_futures)
    for image_future in image_futures:
        image_list.append(image_future.result())

    return image_list


def get_image(base_url: str, page_num: int):
    page_num_string = str.format(f"{page_num:04d}")
    json_request = requests.get(base_url + page_num_string + ".ptimg.json")
    if json_request.status_code != 404:
        json_dict = json_request.json()
        image_url = base_url + json_dict["resources"]["i"]["src"]
        image_request = requests.get(image_url, stream=True)
        scrambled_image = Image.open(image_request.raw)
        return descramble(scrambled_image, json_dict)


def get_num_pages(series_name: str, vol_num: int):
    url = "https://comic-meteor.jp/ptdata/" + series_name + "/" + f"{vol_num:04d}"
    page_request = requests.get(url)
    soup = BeautifulSoup(page_request.text, features="html.parser")
    content_div = soup.find("div", {"id": "content"})
    return len(content_div.findChildren())
