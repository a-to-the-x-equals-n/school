


// CAROUSEL

let images = [];
let currentIndex = 0;
const imgElement = document.getElementById("carouselImage");

fetch("../assets/gooses/images.json")
    .then(response => response.json())
    .then(data => {
        images = data.map(img => `../assets/gooses/${img}`);
        updateImage();
    })
    .catch(error => console.error("Error loading images:", error));

function updateImage() {
    if (images.length > 0) {
        imgElement.src = images[currentIndex];
    }
}

document.getElementById("prevBtn").addEventListener("click", () => {
    currentIndex = (currentIndex === 0) ? images.length - 1 : currentIndex - 1;
    updateImage();
});

document.getElementById("nextBtn").addEventListener("click", () => {
    currentIndex = (currentIndex === images.length - 1) ? 0 : currentIndex + 1;
    updateImage();
});
