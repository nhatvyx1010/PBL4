// Counter for adding new license plates
let licensePlateCounter = 2; // Start from 2 since the first row is already there

// Function to add a new row for a license plate
function addLicensePlateRow() {
    const tableBody = document.getElementById('licensePlateTableBody');

    // Create a new row
    const newRow = document.createElement('tr');
    newRow.innerHTML = `
        <td>${licensePlateCounter++}</td>
        <td><input type="text" placeholder=""></td>
    `;

    // Append the new row to the table
    tableBody.appendChild(newRow);
}

// Add an event listener to the "Thêm biển số" button
const addLicensePlateButton = document.querySelector('.addLicensePlate');
addLicensePlateButton.addEventListener('click', addLicensePlateRow);
