import os
import random

from PIL import Image


def split_image(image_path):
    image = Image.open(image_path)

    width, height = image.size
    sub_width = width // 3
    sub_height = height // 2

    sub_images = []
    for row in range(2):
        for col in range(3):
            left = col * sub_width
            upper = row * sub_height
            right = (col + 1) * sub_width
            lower = (row + 1) * sub_height

            sub_image = image.crop((left, upper, right, lower))
            sub_images.append(sub_image)

    return sub_images


def save_sub_images(sub_images, output_folder):
    for i, sub_image in enumerate(sub_images):
        sub_image.save("{}/sub_image_{}.png".format(output_folder, i + 1))


def get_random_image(images_dir):
    images_folder = os.listdir(images_dir)
    random_country = random.choice(images_folder)
    country_path = os.path.join(images_dir, random_country)

    # Filter images folder
    images = os.listdir(country_path)
    sub_images = [i for i in images if "sub_image" in i]
    flag_image = set(images).difference(sub_images)

    return random_country, list(flag_image), list(sub_images)


def main():
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    images_folder = os.path.join(parent_dir, "..", "images")

    countries = os.listdir(images_folder)

    for country in countries:
        folder_path = os.path.join(images_folder, country)
        full_image_path = os.path.join(folder_path, os.listdir(folder_path)[0])
        splitted_images = split_image(full_image_path)
        save_sub_images(splitted_images, folder_path)


if __name__ == "__main__":
    main()
