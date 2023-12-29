document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("myModal");
    const modal_add = document.getElementById("myModal_add");
    const updateButton = document.getElementById("updateButton");
    const addButton = document.getElementById("addButton_add");
    const backButton = document.getElementById("backButton");
    const backButton_add = document.getElementById("backButton_add");

    addButton.onclick = function() {
        modal_add.style.display = "block";
    }
    
    updateButton.onclick = function() {
        modal.style.display = "block";
    };

    backButton.onclick = function() {
        modal.style.display = "none";
    };

    backButton_add.onclick = function() {
        modal_add.style.display = "none";
    };

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
        if (event.target == modal_add) {
            modal_add.style.display = "none";
        }
    };

});
