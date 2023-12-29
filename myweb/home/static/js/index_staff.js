var inputField_in = document.getElementById('user_time_in');
var inputField_out = document.getElementById('user_time_out');

function updateTime() {
    var currentTime = new Date();
    var hours = currentTime.getHours();
    var minutes = currentTime.getMinutes();
    var seconds = currentTime.getSeconds();

    // Định dạng thời gian
    hours = (hours < 10 ? "0" : "") + hours;
    minutes = (minutes < 10 ? "0" : "") + minutes;
    seconds = (seconds < 10 ? "0" : "") + seconds;

    // Chuyển đổi thời gian thành chuỗi trong định dạng "HH:MM:SS"
    var timeString = hours + ":" + minutes + ":" + seconds;

    // Hiển thị thời gian trong trường input
    inputField_in.value = timeString;
    inputField_out.value = timeString;
}

// Cập nhật thời gian mỗi giây
setInterval(updateTime, 1000);


var inputFieldDate_in = document.getElementById('user_date_in');
var inputFieldDate_out = document.getElementById('user_date_out');

function updateDate() {
    var currentDate = new Date();
    var year = currentDate.getFullYear();
    var month = (currentDate.getMonth() + 1).toString().padStart(2, '0');
    var day = currentDate.getDate().toString().padStart(2, '0');

    // Hiển thị ngày trong trường input
    inputFieldDate_in.value = year + "-" + month + "-" + day;
    inputFieldDate_out.value = year + "-" + month + "-" + day;
}

// Cập nhật ngày mỗi giây
setInterval(updateDate, 1000);


// Cập nhật Username
function updateInputUserName() {
    var selectBox = document.getElementById("user_plate_in");
    var selectBox_name = document.getElementById("user_name_in");
    selectBox_name_val = selectBox_name.value;

    document.getElementById("fullname_in").innerText = selectBox_name_val;
}


// Get the modal
var modalIn = document.getElementById("myModalIn");
var submitButtonIn = document.getElementById("submitButtonIn");
var exitButtonIn = document.getElementById("exitButtonIn");
var modalOut = document.getElementById("myModalOut");
var submitButtonOut = document.getElementById("submitButtonOut");
var exitButtonOut = document.getElementById("exitButtonOut");


document.getElementById("AddIn").onclick = function(event) {
    event.preventDefault(); // Prevent default form submission
    // Check if display_user_plate_in is empty
    var displayUserPlateIn = document.getElementById("display_user_plate_in").innerText.trim();
    if (displayUserPlateIn === "") {
        alert("Biển số xe không được trống!");
        return; // Stop execution if display_user_plate_in is empty
    }
        // Capture form data
    var plateImgIn = document.getElementById("plate_img_in").src;
    var characterImgIn = document.getElementById("character_img_in").src;
    var characterIn = document.getElementById("character_in").innerText;
    var userNameIn = document.getElementById("user_name_in").value;
    var userPlateIn = document.getElementById("user_plate_in").value;
    var userTimeIn = document.getElementById("user_time_in").value;
    var userDateIn = document.getElementById("user_date_in").value;

    // Display form data in the modal
    document.getElementById("full-name-in").innerText = "Họ và tên: " + userNameIn;
    document.getElementById("license-plate-in").innerText = "Biển số xe: " + userPlateIn;
    document.getElementById("time-in").innerText = "Thời gian vào: " + userTimeIn;
    document.getElementById("date-in").innerText = "Ngày vào: " + userDateIn;

    // Show the modal
    modalIn.style.display = "block";
};
document.getElementById("AddOut").onclick = function(event) {
    event.preventDefault(); // Prevent default form submission
    // Check if display_user_plate_in is empty
    var displayUserPlateOut = document.getElementById("display_user_plate_out").innerText.trim();
    if (displayUserPlateOut === "") {
        alert("Biển số xe không được trống!");
        return; // Stop execution if display_user_plate_in is empty
    }
    // Capture form data
    var userNameOut = document.getElementById("user_name_out").value;
    var userPlateOut = document.getElementById("user_plate_out").value;
    var userTimeOut = document.getElementById("user_time_out").value;
    var userDateOut = document.getElementById("user_date_out").value;

    // Tạo đối tượng FormData và thêm dữ liệu vào đó
    var formData = new FormData();
    formData.append('userPlateOut', userPlateOut);
    formData.append('userTimeOut', userTimeOut);
    formData.append('userDateOut', userDateOut);

    // Gửi yêu cầu POST bằng Fetch API đến đường dẫn của getTotal
    fetch('/getTotal/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.text())
    .then(data => {
        var getTotal = data; // Lưu giá trị tính toán được trả về từ getTotal
        // Hiển thị form data và giá trị tính toán trong modal
        document.getElementById("full-name-out").innerText = "Họ và tên: " + userNameOut;
        document.getElementById("license-plate-out").innerText = "Biển số xe: " + userPlateOut;
        document.getElementById("time-out").innerText = "Thời gian ra: " + userTimeOut;
        document.getElementById("date-out").innerText = "Ngày ra: " + userDateOut;
        document.getElementById("total-price").innerText = "Tổng chi phí: " + getTotal; // Hiển thị tổng chi phí tính toán được

        // Show the modal
        modalOut.style.display = "block";
    })
    .catch(error => {
        console.error('Có lỗi khi gửi yêu cầu.');
    });
};


// Function to close the modal when the back button is clicked
function sendDataInToServer() {
    var userPlateIn = document.getElementById("user_plate_in").value;
    var userTimeIn = document.getElementById("user_time_in").value;
    var userDateIn = document.getElementById("user_date_in").value;

    var formData = new FormData();
    formData.append('userPlateIn', userPlateIn);
    formData.append('userTimeIn', userTimeIn);
    formData.append('userDateIn', userDateIn);

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/historyIn/', true);
    xhr.onload = function () {
        if (xhr.status === 200) {
            message = xhr.responseText;
            if (message !== 'Đăng ký xe vào không thành công') {
                if (confirm(message)) {
                    controlServo();
                }
            }
        } else {
            // Xử lý lỗi nếu có
            console.error('Có lỗi khi gửi yêu cầu.');
        }
    };
    xhr.onerror = function () {
        // Xử lý lỗi kết nối
        console.error('Lỗi kết nối.');
    };
    xhr.send(formData);
}
function sendDataOutToServer() {
    var userPlateOut = document.getElementById("user_plate_out").value;
    var userTimeOut = document.getElementById("user_time_out").value;
    var userDateOut = document.getElementById("user_date_out").value;

    var formData = new FormData();
    formData.append('userPlateOut', userPlateOut);
    formData.append('userTimeOut', userTimeOut);
    formData.append('userDateOut', userDateOut);

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/historyOut/', true);
    xhr.onload = function () {
        if (xhr.status === 200) {
            message = xhr.responseText;
            // Bạn có thể sử dụng biến message ở đây hoặc trong các hàm khác
            if (message !== 'Đăng ký xe ra không thành công') {
                if (confirm(message)) {
                    controlServo();
                }
            }
        } else {
            // Xử lý lỗi nếu có
            console.error('Có lỗi khi gửi yêu cầu.');
        }
    };
    xhr.onerror = function () {
        // Xử lý lỗi kết nối
        console.error('Lỗi kết nối.');
    };
    xhr.send(formData);
}
submitButtonIn.onclick = function() {
    modalIn.style.display = "none";
    sendDataInToServer();
};

exitButtonIn.onclick = function() {
    modalIn.style.display = "none";
}
submitButtonOut.onclick = function() {
    modalOut.style.display = "none";
    sendDataOutToServer();
};
exitButtonOut.onclick = function() {
    modalOut.style.display = "none";
}


// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
};


// ====================================================
function checkValue(input) {
    if (input.value === "1") {
        setTimeout(function() {
            captureFrameIn(1);
        }, 2000);
    } else if (input.value === "2") {
        setTimeout(function() {
            captureFrameOut(1);
        }, 2000); 
    }
}


function captureFrameIn() {
    var alerts = document.getElementsByClassName('alert');
    for (var i = 0; i < alerts.length; i++) {
        alerts[i].style.display = 'none';
    }
    $.ajax({
        type: "GET",
        url: "{% url 'capture_image_in' %}",
        success: function (data) {
            // if (!checkDataValidity(data) && retryCount > 0) {
            //     setTimeout(function() {
            //         captureFrameIn(retryCount - 1);
            //     }, 100); // Thực hiện lại sau 1 giây
            // } else {
                // Nếu data hợp lệ hoặc đã hết số lần thử lại, xử lý dữ liệu
                processDataIn(data);
            // }
        }
    });
}

// Attach click event to the button
$("#captureButtonIn").on("click", function() {
    captureFrameIn();
});


function captureFrameOut(retryCount) {
    var alerts = document.getElementsByClassName('alert');
    for (var i = 0; i < alerts.length; i++) {
        alerts[i].style.display = 'none';
    }
    $.ajax({
        type: "GET",
        url: "{% url 'capture_image_out' %}",
        success: function (data) {
            if (!checkDataValidity(data) && retryCount > 0) {
                setTimeout(function() {
                    captureFrameOut(retryCount - 1);
                }, 100); // Thực hiện lại sau 1 giây
            } else {
                // Nếu data hợp lệ hoặc đã hết số lần thử lại, xử lý dữ liệu
                processDataOut(data);
            }
        }
    });
}
// Attach click event to the button
$("#captureButtonOut").on("click", function() {
    captureFrameOut();
});

function checkDataValidity(data) {
    var dataArr = data.split('|');
    var fullname = dataArr[4];
    return fullname != 'Chưa đăng ký';
}
// Hàm xử lý dữ liệu
function processDataIn(data) {
    var dataArr = data.split('|');
    // Xử lý dữ liệu từ 'capture_image_in' hoặc 'capture_image_data' endpoint
    // Hiển thị dữ liệu, cập nhật các phần tử trên trang, vv
    var img1 = new Image();
    var img2 = new Image();
    img1.src = 'data:image/jpeg;base64,' + dataArr[0];
    img2.src = 'data:image/jpeg;base64,' + dataArr[1];
    var kitu = dataArr[2];
    var id = dataArr[3];
    var fullname = dataArr[4];
    var license_plates = dataArr[5];

    document.getElementById('plate_img_in').src = img1.src;
    document.getElementById('character_img_in').src = img2.src;
    document.getElementById('character_in').innerText = kitu;
    document.getElementById('user_name_in').value = fullname;
    document.getElementById('display_user_name_in').value = fullname;
    document.getElementById('user_plate_in').value = license_plates;
    document.getElementById('display_user_plate_in').innerText = license_plates;
}

function processDataOut(data) {
    var dataArr = data.split('|');
    // Xử lý dữ liệu từ 'capture_image_in' hoặc 'capture_image_data' endpoint
    // Hiển thị dữ liệu, cập nhật các phần tử trên trang, vv
    var img1 = new Image();
    var img2 = new Image();
    img1.src = 'data:image/jpeg;base64,' + dataArr[0];
    img2.src = 'data:image/jpeg;base64,' + dataArr[1];
    var kitu = dataArr[2];
    var id = dataArr[3];
    var fullname = dataArr[4];
    var license_plates = dataArr[5];

    document.getElementById('plate_img_out').src = img1.src;
    document.getElementById('character_img_out').src = img2.src;
    document.getElementById('character_out').innerText = kitu;
    document.getElementById('user_name_out').value = fullname;
    document.getElementById('display_user_name_out').value = fullname;
    document.getElementById('user_plate_out').value = license_plates;
    document.getElementById('display_user_plate_out').innerText = license_plates;
}
// =====================================================================

var espServer = "http://192.168.43.124"
function controlServo() {
    // const angle = document.getElementById("servoAngle").value;
    // ${angle}
    fetch(espServer+`/servo?angle=1`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            console.log("Servo controlled");
        })
        .catch(error => console.error('Error:', error));
}