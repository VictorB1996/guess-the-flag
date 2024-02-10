import os
import shutil

from utils.images import (
    get_random_image,
    get_difficulty_width_height,
    resize_image,
    get_image_size,
)
from utils.directions import (
    get_coordinates,
    calculate_direction,
    calculate_distance,
    get_direction_png,
)

from flask import Flask, render_template, request, session, jsonify

app = Flask(__name__)
app.secret_key = "test"

allowed_difficulties = ("easy", "medium", "hard")

base_path = os.path.abspath(os.path.dirname(__file__))
images_dir = os.path.join(base_path, "static", "images")

user_picked_countries = []


def move_images():
    images_dir = os.path.join(base_path, "images")
    static_dir = os.path.join(base_path, "static")
    if "images" not in os.listdir(static_dir):
        shutil.move(images_dir, static_dir)


@app.route("/static/<path:filename>")
def static_files(filename):
    return app.send_static_file(filename)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        difficulty = request.args.get("difficulty")
        if not difficulty or difficulty not in allowed_difficulties:
            difficulty = "medium"

        width, height = get_difficulty_width_height(difficulty)

        country, flag, parts = get_random_image(images_dir, difficulty)
        country_latitiude, country_longitude = get_coordinates(country)

        session.update(
            {
                "country": country,
                "flag": flag,
                "parts": parts,
                "countries": os.listdir(images_dir),
                "allowed_guesses": len(parts),
                "current_guesses": 1,
                "game_over": False,
                "country_latitiude": country_latitiude,
                "country_longitude": country_longitude,
            }
        )

        # Resize background image as per flag parts
        background_picture_path = os.path.join(
            images_dir, "..", "background", "part_background.png"
        )
        background_new_width, background_new_height = get_image_size(
            os.path.join(images_dir, country, difficulty, "sub_image_1.png")
        )
        resize_image(
            background_new_width, background_new_height, background_picture_path
        )

    else:
        user_selected_country = request.form.get("selected-country")

        response = {
            "distance": None,
            "direction_png_src": None,
            "user_selected_country": user_selected_country,
            "user_guessed_correctly": False,
            "info_text": "",
        }

        if user_selected_country == session.get("country"):
            response.update(
                {
                    "user_guessed_correctly": True,
                    "info_text": "You guessed correctly - The answer is {}! Retry below.".format(
                        session.get("country")
                    ),
                }
            )
        else:
            print("Current Guesses: {}".format(session.get("current_guesses")))
            if session.get("current_guesses") >= len(session.get("parts")):
                response.update(
                    {
                        "game_over": True,
                        "info_text": "You failed to guess the country - The answer was {}. Retry below.".format(
                            session.get("country")
                        ),
                    }
                )
            else:
                session["current_guesses"] += 1

                user_selected_country_latitude, user_selected_country_longitude = (
                    get_coordinates(user_selected_country)
                )

                distance = calculate_distance(
                    (
                        session.get("country_latitiude"),
                        session.get("country_longitude"),
                    ),
                    (user_selected_country_latitude, user_selected_country_longitude),
                )

                distance = "{:,}".format(int(distance))
                distance = str(distance) + " Km"

                direction = calculate_direction(
                    user_selected_country_latitude,
                    user_selected_country_longitude,
                    session.get("country_latitiude"),
                    session.get("country_longitude"),
                )

                direction_png_src = get_direction_png(direction)
                response.update(
                    {"distance": distance, "direction_png_src": direction_png_src}
                )

        return jsonify(response)

    return render_template(
        "index.html",
        country=session["country"],
        flag=session["flag"],
        parts=session["parts"],
        countries=session["countries"],
        user_picked_countries=user_picked_countries,
        difficulty=difficulty,
        difficulty_columns=width,
        difficulty_rows=height,
    )


if __name__ == "__main__":
    move_images()
    app.run(debug=True)
