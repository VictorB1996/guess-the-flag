import os
import shutil

from utils.images import get_random_image
from utils.directions import (
    get_coordinates,
    calculate_direction,
    calculate_distance,
    get_direction_png,
)

from flask import Flask, render_template, request, session, jsonify

app = Flask(__name__)
app.secret_key = "test"

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
        allowed_guesses = 6
        current_guesses = 0

        country, flag, parts = get_random_image(images_dir)
        session["country"], session["flag"], session["parts"] = country, flag, parts
        session["allowed_guesses"] = allowed_guesses
        session["current_guesses"] = current_guesses

        country_latitiude, country_longitude = get_coordinates(country)
        session.update(
            {
                "country_latitiude": country_latitiude,
                "country_longitude": country_longitude,
            }
        )

    else:
        user_selected_country = request.form.get("selected-country")
        user_selected_country_latitude, user_selected_country_longitude = (
            get_coordinates(user_selected_country)
        )

        distance = calculate_distance(
            (session.get("country_latitiude"), session.get("country_longitude")),
            (user_selected_country_latitude, user_selected_country_longitude),
        )

        distance = "{:,}".format(int(distance))
        distance = str(distance) + " Km"

        direction = calculate_direction(
            user_selected_country_latitude,
            user_selected_country_longitude,
            session.get("country_latitiude"),
            session.get("country_longitude")
        )

        direction_png_src = get_direction_png(direction)

        return jsonify(
            {
                "user_selected_country": user_selected_country,
                "distance": distance,
                "direction_png_src": direction_png_src
            }
        )

    # Reset session when the game ends
    # (user either guesses the flag or runs out of choices)

    return render_template(
        "index.html",
        country=session["country"],
        flag=session["flag"][0],
        parts=session["parts"],
        countries=session["countries"],
        user_picked_countries=user_picked_countries,
    )


if __name__ == "__main__":
    move_images()
    app.run(debug=True)
