// Get references to the elements
const addLicensePlateButton = document.querySelector(".addLicensePlate");
const licensePlateTableBody = document.getElementById("licensePlateTableBody");
const modal = document.getElementById("myModal");
const btn = document.getElementById("updateButton");
const backButton = document.getElementById("backButton");

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

// Function to add a new row with input fields and a "Lưu" button
function addLicensePlateRow() {
    const newRow = document.createElement("tr");
    newRow.innerHTML = `
        <td>${licensePlateTableBody.children.length + 1}</td>
        <td><input type="text" class="licensePlateInput" placeholder="Nhập biển số"></td>
        <td><button class="saveButton">Lưu</button></td>`;

    // Add event listener to the "Lưu" button within the new row
    newRow.querySelector(".saveButton").addEventListener("click", saveLicensePlate);

    licensePlateTableBody.appendChild(newRow);
}

// Function to handle the "Lưu" button click event
function saveLicensePlate(event) {
    const licensePlateValue = event.target.parentElement.previousElementSibling.querySelector("input").value;
    // Perform any necessary actions with the entered license plate value
    console.log("Lưu clicked with value: " + licensePlateValue);
}

// Add event listener to the "Thêm biển số" button
addLicensePlateButton.addEventListener("click", addLicensePlateRow);