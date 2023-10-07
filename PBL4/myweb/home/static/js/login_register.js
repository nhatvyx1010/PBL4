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
