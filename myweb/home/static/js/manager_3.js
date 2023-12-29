// Get the modal
var modal_1 = document.getElementById("myModal_1");
var btn = document.getElementById("Chinhsua");
var backButton = document.getElementById("backButton_1");

// Function to open the modal
btn.onclick = function() {
    modal_1.style.display = "block";
};

// Function to close the modal when the back button is clicked
backButton.onclick = function() {
    modal_1.style.display = "none";
};

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal_1) {
        modal_1.style.display = "none";
    }
};

