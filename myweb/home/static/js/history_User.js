var modal = document.getElementById("myModal");
var editButtons = document.getElementsByClassName("edit");
var backButton = document.getElementById("backButton");

for (var i = 0; i < editButtons.length; i++) {
    editButtons[i].onclick = function() {
        var historyId = this.value;
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/history_staff_modal_view/', true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4 && xhr.status === 200) {
                var data = JSON.parse(xhr.responseText);
                // Hiển thị dữ liệu trong modal ở đây
            }
        };
        xhr.send('history_id=' + historyId);
    };
}

backButton.onclick = function() {
    modal.style.display = "none";
};

window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
};
