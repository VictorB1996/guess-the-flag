function getRandomElement(nodeList) {
    // Convert NodeList to an array
    var array = Array.from(nodeList);

    // Return a random element
    return array[Math.floor(Math.random() * array.length)];
}

function updateImageSource(country) {
    var dropdown = document.getElementById("country-dropdown");
    var selectedCountry = dropdown.value;

    var flag_part_imgs = document.querySelectorAll('img[class*="sub_image_"]');

    random_flag_part = getRandomElement(flag_part_imgs);
    classes = Array.from(random_flag_part.classList);
    image_path = 'static/images/' + country + '/' + classes[1] + ".png";
    random_flag_part.src = image_path;
    random_flag_part.classList.remove(classes[1]);

    dropdown.options[dropdown.selectedIndex].disabled = true;

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/", true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.send("selected-country=" + selectedCountry);
    // xhr.onload = function () {
    //     if (xhr.status === 200) {
    //     }
    // };
}

