function getRandomElement(nodeList) {
    var array = Array.from(nodeList);
    return array[Math.floor(Math.random() * array.length)];
}

function updateImageSource(country, difficulty) {
    var dropdown = document.getElementById("country-dropdown");
    var selectedCountry = dropdown.value;

    var flag_part_imgs = document.querySelectorAll('img[class*="sub_image_"]');

    random_flag_part = getRandomElement(flag_part_imgs);
    classes = Array.from(random_flag_part.classList);
    image_path = 'static/images/' + country + "/" + difficulty + "/" + classes[1] + ".png";
    random_flag_part.src = image_path;
    random_flag_part.classList.remove(classes[1]);

    dropdown.options[dropdown.selectedIndex].disabled = true;

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/", true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.setRequestHeader("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
    xhr.send("selected-country=" + selectedCountry);

    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            var response = JSON.parse(xhr.responseText);
            handleUserGuess(
                response.user_selected_country,
                response.distance,
                response.direction_png_src
            )
        }
    };
}

function handleUserGuess(pickedCountry, distance, directionPictureSrc) {
    // Enable the table
    var table = document.getElementById("user-guesses");
    table.style.display = "table";

    table = table.getElementsByTagName('tbody')[0];
    var newRow = table.insertRow(table.rows.length);

    var cell1 = newRow.insertCell(0);
    var cell2 = newRow.insertCell(1);

    cell1.innerHTML = pickedCountry;
    cell2.innerHTML = distance;

    cell1.style.textAlign = "center";
    cell1.style.verticalAlign = "middle";

    cell2.style.textAlign = "center";
    cell2.style.verticalAlign = "middle";

    var cell3 = newRow.insertCell(2);
    var directionImage = document.createElement("img");
    directionImage.src = directionPictureSrc;
    directionImage.style.width = "50px";
    directionImage.style.height = "auto";
    cell3.appendChild(directionImage);
    cell3.style.textAlign = "center";
    cell3.style.verticalAlign = "middle";
}




