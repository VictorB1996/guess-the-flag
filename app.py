import os
import shutil

from utils.images import get_random_image

from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = "test"

base_path = os.path.abspath(os.path.dirname(__file__))
images_dir = os.path.join(base_path, "static", "images")

allowed_guesses = 6
current_guesses = 0


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
    global current_guesses

    if "country" not in session:
        session["country"], session["flag"], session["parts"] = get_random_image(
            images_dir
        )
        session["countries"] = os.listdir(images_dir)
        session["current_guesses"] = 0

    user_selected_country = None

    if request.method == "POST":
        user_selected_country = request.form.get("selected-country")
        if user_selected_country == session["country"]:
            print("You guessed right!")
        else:
            session["current_guesses"] += 1

    session["selected_country"] = user_selected_country

    return render_template(
        "index.html",
        country=session["country"],
        flag=session["flag"][0],
        parts=session["parts"],
        countries=session["countries"],
        correct_guess=bool(user_selected_country),
        current_guesses=session["current_guesses"],
        selected_country=user_selected_country,
    )


if __name__ == "__main__":
    move_images()
    app.run(debug=True)
