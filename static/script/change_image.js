function getRandomElement(nodeList) {
    var array = Array.from(nodeList);
    return array[Math.floor(Math.random() * array.length)];
}

function updateFlagPartImageSource(imageElement, country, difficulty) {
    var elementClasses = Array.from(imageElement.classList);
    var imagePath = 'static/images/' + country + "/" + difficulty + "/" + elementClasses[1] + ".png";
    imageElement.src = imagePath
    imageElement.classList.remove(elementClasses[1]);
}

function handlePostRequest(country, difficulty) {
    var dropdown = document.getElementById("country-dropdown");
    var selectedCountry = dropdown.value;

    var flag_part_imgs = document.querySelectorAll('img[class*="sub_image_"]');

    random_flag_part = getRandomElement(flag_part_imgs);
    updateFlagPartImageSource(random_flag_part, country, difficulty)

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
                response.direction_png_src,
                response.user_guessed_correctly,
                country,
                difficulty,
                response.info_text,
                response.game_over
            )
        }
    };
}

function showUserText(infoText) {
    var infoTextElem = document.getElementById("user-info");
    var optionsDiv = document.querySelector(".options");

    infoTextElem.style.opacity = 0;
    void infoTextElem.offsetWidth;

    setTimeout(function () {
        infoTextElem.textContent = infoText;
        infoTextElem.style.opacity = 1;
    }, 10);

    var options = ["easy", "medium", "hard"]
    for (var i = 0; i <= 2; i++) {
        var anchorTag = document.createElement('a');
        anchorTag.textContent = options[i];
        anchorTag.href = '?difficulty=' + encodeURIComponent(options[i]);
        optionsDiv.appendChild(anchorTag);
    }

    setTimeout(function () {
        infoTextElem.classList.add("fade-in");
        optionsDiv.classList.add('fade-in');
    }, 20);
}



function handleUserGuess(pickedCountry, distance, directionPictureSrc, userGuessedCorrectly, country, difficulty, infoText, gameOver) {
    var flag_part_imgs = document.querySelectorAll('img[class*="sub_image_"]');

    if (userGuessedCorrectly === true) {
        flag_part_imgs.forEach(function(imageElement) {
            updateFlagPartImageSource(imageElement, country, difficulty)
        })

        var containerElement = document.querySelector('.container.mt-5');
        containerElement.style.pointerEvents = 'none';

        showUserText(infoText);
    }
    else if (gameOver === true) {
        flag_part_imgs.forEach(function(imageElement) {
            updateFlagPartImageSource(imageElement, country, difficulty)
        })
        var containerElement = document.querySelector('.container.mt-5');
        containerElement.style.pointerEvents = 'none';
        showUserText(infoText);
    }
    else {
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
}




