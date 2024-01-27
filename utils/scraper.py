import os
import requests

from bs4 import BeautifulSoup


def download_flag_image(url, parent_directory):
    content = requests.get(url)
    page = BeautifulSoup(content.content, "html.parser")

    flag_elem = page.find("div", class_="image").find("img")
    flag_url = flag_elem.get("src")
    flag_country_name = "".join(flag_elem.get("alt").split("Flag of")).lstrip()

    image_path = os.path.join(parent_directory, flag_country_name)
    os.makedirs(image_path, exist_ok=True)

    flag_picture_name = flag_country_name.replace(" ", "_").lower() + ".png"

    flag_image_data = requests.get(flag_url)
    with open(os.path.join(image_path, flag_picture_name), "wb") as file:
        file.write(flag_image_data.content)


def main():
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    images_folder = os.path.join(parent_dir, "..", "images")
    os.makedirs(images_folder, exist_ok=True)

    main_url = "https://www.countryflags.com/"
    response = requests.get(main_url)
    page = BeautifulSoup(response.content, "html.parser")

    flags_urls = [
        x.find("a").get("href")
        for x in page.find("div", class_="tiles").find_all("div", class_="thumb")
    ]

    for url in flags_urls:
        download_flag_image(url, parent_directory=images_folder)


if __name__ == "__main__":
    main()
