// Get the modal
var modal = document.getElementById("myModal");
var btn = document.getElementById("Add");
var backButton = document.getElementById("backButton");

// Function to open the modal
btn.onclick = function() {
    modal.style.display = "block";
};

// Function to close the modal when the back button is clicked
backButton.onclick = function() {
    modal.style.display = "none";
};

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
};
