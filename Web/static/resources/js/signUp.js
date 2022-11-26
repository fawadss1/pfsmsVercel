const inputDate = document.getElementById("summary_date");
inputDate.addEventListener("click", function (evt) {
    if (this.getAttribute("type") === "date") {
        this.showPicker();
    }
});

(function () {
    'use strict'
    const forms = document.querySelectorAll('.needs-validation');
    Array.prototype.slice.call(forms)
        .forEach(function (form) {
            form.addEventListener('submit', function (event) {
                if (!form.checkValidity()) {
                    event.preventDefault()
                    event.stopPropagation()
                }
                form.classList.add('was-validated')
            }, false)
        })
})()
$(":input").inputmask();
$(window).on('load', function () {
    $('#Agreement').modal('show');
});
const d = new Date();
document.getElementById("year").innerHTML = d.getFullYear().toString();

function goBack() {
    window.history.back();
}

$('#confirm_password').keyup(function () {
    const pass = $('#password');
    const confirmPass = $(this).val();
    if ($('#password').val() != confirmPass) {
        pass.css("border", "2px solid red");
        pass.css("box-shadow", "0 0 20px red");
        $(this).css("border", "2px solid red");
        $(this).css("box-shadow", "0 0 20px red");
    } else {
        pass.css("border", "2px solid green");
        pass.css("box-shadow", "0 0 5px green");
        $(this).css("border", "2px solid green");
        $(this).css("box-shadow", "0 0 5px green");
    }
});