(function () {
    'use strict';
    window.addEventListener('load', function () {
        const forms = document.getElementsByClassName('needs-validation');
        Array.prototype.filter.call(forms, function (form) {
            form.addEventListener('submit', function (event) {
                if (form.checkValidity() === false) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            }, false);
        });
    }, false);
})();

const days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
const dd = new Date();
let day = days[dd.getDay()];
let month = months[dd.getMonth()];
$('.JDate').text(day + ' ' + dd.getDate() + '/' + month + '/' + dd.getFullYear());
$('.JTime').text(dd.toLocaleString('en-US', {
    hour: 'numeric',
    minute: 'numeric',
    second: 'numeric',
    hour12: true
}));
$('.JYear').text(dd.getFullYear());

let copyright = `<P>&copy; ${dd.getFullYear()} All Rights Reserved. Developed By <a href="https://fb.com/fawadkhan546" target="blank" class="text-success">Fawad</a><br><span class="small">Ver 2.5.2</span></P>`;
document.getElementById("Footer").innerHTML = copyright;