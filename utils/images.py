import os
import sys
import random
import argparse

from PIL import Image


def split_image(image_path, diff_width, diff_height):
    image = Image.open(image_path)

    width, height = image.size
    sub_width = width // diff_width
    sub_height = height // diff_height

    sub_images = []
    for row in range(diff_height):
        for col in range(diff_width):
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


def get_random_image(images_dir, difficulty):
    images_folder = os.listdir(images_dir)
    random_country = random.choice(images_folder)
    country_path_difficulty = os.path.join(images_dir, random_country, difficulty)

    # Filter images folder
    sub_images = os.listdir(country_path_difficulty)
    flag_image = [p for p in os.listdir(os.path.join(images_dir, random_country)) if p.endswith(".png")][0]

    return random_country, flag_image, list(sub_images)

def get_difficulty_width_height(difficulty):
    if difficulty == "easy":
        return 2, 2
    elif difficulty == "medium": 
        return 3, 2
    elif difficulty == "hard":
        return 3, 3
    else:
        return None

def main(difficulty):

    parent_dir = os.path.dirname(os.path.abspath(__file__))
    images_folder = os.path.join(parent_dir, "..", "static", "images")

    countries = os.listdir(images_folder)

    width, height = get_difficulty_width_height(difficulty)
    if not difficulty:
        print("Invalid difficulty passed.")
        sys.exit()

    for country in countries:
        folder_path = os.path.join(images_folder, country)
        full_image_path = os.path.join(folder_path, [p for p in os.listdir(folder_path) if p.endswith("png")][0])
        splitted_images = split_image(full_image_path, width, height)
        difficulty_path = os.path.join(folder_path, difficulty)
        if not os.path.exists(difficulty_path):
            os.makedirs(difficulty_path)
        save_sub_images(splitted_images, difficulty_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("difficulty")
    args = parser.parse_args()

    if not args:
        print("Please specifiy difficulty (easy, medium, hard)")
        sys.exit()

    difficulty = args.difficulty

    main(difficulty)