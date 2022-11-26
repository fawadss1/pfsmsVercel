const togglePassword = document.querySelector("#togglePass");
const password = document.getElementById("password");
const confirmPassword = document.getElementById("confirm_password");

togglePassword.addEventListener("click", function () {
    const Ptype = password.getAttribute("type") === "password" ? "text" : "password";
    const CPtype = confirmPassword.getAttribute("type") === "password" ? "text" : "password";
    let icon = togglePassword.getAttribute("class");
    if (icon == "icofont icofont-eye-blocked")
        icon = "icofont icofont-eye";
    else
        icon = "icofont icofont-eye-blocked";
    password.setAttribute("type", Ptype);
    confirmPassword.setAttribute("type", CPtype);
    $(this).removeClass();
    $(this).toggleClass(icon);
});

function validatePassword() {
    if (password.value !== confirmPassword.value) {
        confirmPassword.setCustomValidity("Sorry! Your Passwords Don't Match");
    } else {
        confirmPassword.setCustomValidity('');
    }
}
password.onchange = validatePassword;
confirmPassword.onkeyup = validatePassword;