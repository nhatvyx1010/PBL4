// main.js
$(document).ready(function () {
    // Khai báo biến
    var loginButton = $("#loginButton");
    var registerButton = $("#registerButton");
    var modalOverlay = $(".modal__overlay");
    var authFormControlsBack = $(".auth-form__controls-back");
    var modalBody = $(".modal__body");

    // Function to show the login modal
    loginButton.click(function () {
        var modalId = $(this).data("modal");
        $("#" + modalId).fadeIn();
    });

    // Function to show the register modal when the "Đăng ký" button is clicked
    registerButton.click(function () {
        var modalId = $(this).data("modal");
        $("#" + modalId).fadeIn();
    });

    // Function to close the modals
    modalOverlay.click(function () {
        closeModal();
    });

    authFormControlsBack.click(function () {
        closeModal();
    });

    // Prevent modal from closing when clicking inside the modal content
    modalBody.click(function (e) {
        e.stopPropagation();
    });

    // Function to close the modals
    function closeModal() {
        $(".modal").fadeOut();
    }
});


// let previousUsername = "";
// let previousPassword = "";
// let previousRegisterData = {
//     name: "",
//     email: "",
//     dob: "",
//     address: "",
//     phone: "",
//     username: "",
//     password: "",
//     passwordConfirm: "",
// };
// // Get references to the login and register buttons and modal elements
// const loginButton = document.getElementById("loginButton");
// const registerButton = document.getElementById("registerButton");
// const loginModal = document.getElementById("loginModal");
// const registerModal = document.getElementById("registerModal");

// // Get references to the "Trở lại" buttons inside the modals
// const loginBackButton = document.querySelector("#loginModal .auth-form__controls-back");
// const registerBackButton = document.querySelector("#registerModal .auth-form__controls-back");

// // Function to show the login modal
// function showLoginModal() {
//     loginModal.style.display = "block";
//     // Set the input fields to their previous values
//     document.querySelector("#loginUsername").value = previousUsername;
//     document.querySelector("#loginPassword").value = previousPassword;
// }

// // Function to hide the login modal
// function hideLoginModal() {
//     loginModal.style.display = "none";
//     // Clear the error message
//     document.getElementById("loginError").textContent = "";
// }

// // Function to show the register modal
// function showRegisterModal() {
//     registerModal.style.display = "block";
//     // Set the input fields to their previous values
//     document.querySelector("#registerName").value = previousRegisterData.name;
//     document.querySelector("#registerEmail").value = previousRegisterData.email;
//     document.querySelector("#registerDob").value = previousRegisterData.dob;
//     document.querySelector("#registerAddress").value = previousRegisterData.address;
//     document.querySelector("#registerPhone").value = previousRegisterData.phone;
//     document.querySelector("#registerUsername").value = previousRegisterData.username;
//     document.querySelector("#registerPassword").value = previousRegisterData.password;
//     document.querySelector("#registerPasswordConfirm").value = previousRegisterData.passwordConfirm;
// }

// // Function to hide the register modal
// function hideRegisterModal() {
//     registerModal.style.display = "none";
// }

// // Add event listeners to the buttons
// loginButton.addEventListener("click", showLoginModal);
// registerButton.addEventListener("click", showRegisterModal);

// // Add event listeners to the "Trở lại" buttons inside the modals
// loginBackButton.addEventListener("click", hideLoginModal);
// registerBackButton.addEventListener("click", hideRegisterModal);

// // Function to handle login
// function loginUser(event) {
//     event.preventDefault(); // Prevent default form submission

//     const username = document.querySelector("#loginUsername").value;
//     const password = document.querySelector("#loginPassword").value;
//     const errorElement = document.querySelector("#loginError");
//     if (username.trim() === '' && password.trim() === '') {
//         errorElement.textContent = "Bạn cần phải nhập username và password.";
//     } else if (username.trim() === '') {
//         errorElement.textContent = "Bạn cần nhập username.";
//     } else if (password.trim() === '') {
//         errorElement.textContent = "Bạn cần nhập password.";
//     } else {
//         // Example username and password for demonstration
//         const validUsername = "your_username";
//         const validPassword = "your_password";

//         if (username === validUsername && password === validPassword) {
//             alert("Login successful!");
//             // You can also redirect the user to another page here
//         } else {
//             errorElement.textContent = "Invalid username or password. Please try again.";
//         }
//         // Store the input values for future use
//         previousUsername = username;
//         previousPassword = password;
//     }
// }

// // Function to handle registration
// function registerUser(event) {
//     event.preventDefault(); // Prevent default form submission

//     const name = document.querySelector("#registerName").value;
//     const email = document.querySelector("#registerEmail").value;
//     const dob = document.querySelector("#registerDob").value;
//     const address = document.querySelector("#registerAddress").value;
//     const phone = document.querySelector("#registerPhone").value;
//     const username = document.querySelector("#registerUsername").value;
//     const password = document.querySelector("#registerPassword").value;
//     const passwordConfirm = document.querySelector("#registerPasswordConfirm").value;
//     const errorElement = document.querySelector("#registerError");

//     // Check for empty fields
//     if (
//         name.trim() === '' ||
//         email.trim() === '' ||
//         dob.trim() === '' ||
//         address.trim() === '' ||
//         phone.trim() === '' ||
//         username.trim() === '' ||
//         password.trim() === '' ||
//         passwordConfirm.trim() === ''
//     ) {
//         errorElement.textContent = "Bạn cần phải nhập tất cả các trường.";
//         return;
//     }

//     // Check if passwords match
//     if (password !== passwordConfirm) {
//         errorElement.textContent = "Password và xác nhận password phải giống nhau.";
//         return;
//     }

//     // Registration logic here
//     alert("Registration successful!");
// }

// // Add event listeners to the login and register buttons
// const loginSubmitButton = document.querySelector("#loginSubmitButton");
// loginSubmitButton.addEventListener("click", loginUser);
// const registerSubmitButton = document.querySelector("#registerSubmitButton");
// registerSubmitButton.addEventListener("click", registerUser);