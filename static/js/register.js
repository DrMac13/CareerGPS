console.log("🚀 JavaScript loaded successfully");

// CSRF Helper
function getCookie(name) {
    let cookieValue = null;

    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");

        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();

            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );
                break;
            }
        }
    }

    return cookieValue;
}

const csrftoken = getCookie("csrftoken");

// Wait for page to load
document.addEventListener("DOMContentLoaded", () => {

    console.log("📄 DOM Loaded");

    const registerForm = document.getElementById("registerForm");

    if (!registerForm) {
        console.error("❌ registerForm not found");
        return;
    }

    registerForm.addEventListener("submit", handleRegistration);

    console.log("✅ Registration form connected");

});

// Registration

async function handleRegistration(event) {

    event.preventDefault();

    clearErrors();

    const firstName = document.getElementById("firstName").value.trim();
    const lastName = document.getElementById("lastName").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirmPassword").value;

    let hasErrors = false;

    // First Name
    if (!firstName) {
        showError("firstNameError", "First name is required");
        hasErrors = true;
    }

    // Last Name
    if (!lastName) {
        showError("lastNameError", "Last name is required");
        hasErrors = true;
    }

    // Email
    if (!email) {
        showError("emailError", "Email is required");
        hasErrors = true;
    } else {

        const emailRegex =
            /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if (!emailRegex.test(email)) {
            showError(
                "emailError",
                "Enter a valid email address"
            );
            hasErrors = true;
        }
    }

    // Password
    if (!password) {
        showError(
            "passwordError",
            "Password is required"
        );
        hasErrors = true;
    }
    else if (password.length < 8) {
        showError(
            "passwordError",
            "Password must be at least 8 characters"
        );
        hasErrors = true;
    }

    // Confirm Password
    if (password !== confirmPassword) {
        showError(
            "confirmError",
            "Passwords do not match"
        );
        hasErrors = true;
    }

    if (hasErrors) {
        console.log("❌ Validation failed");
        return;
    }

    console.log("✅ Validation passed");

    const submitButton =
        document.querySelector(
            "#registerForm button[type='submit']"
        );

    submitButton.disabled = true;
    submitButton.textContent = "Creating Account...";

    try {

        const response = await fetch(
            "/api/register/",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrftoken
                },
                body: JSON.stringify({
                    first_name: firstName,
                    last_name: lastName,
                    email: email,
                    password: password
                })
            }
        );

        const data = await response.json();

        console.log("Server Response:", data);

        if (response.ok && data.success) {

            alert(
                "Registration successful!"
            );

            document
                .getElementById("registerForm")
                .reset();

        }
        else {

            showError(
                "emailError",
                data.error || "Registration failed"
            );

        }

    }
    catch (error) {

        console.error(error);

        showError(
            "emailError",
            "Network error"
        );

    }
    finally {

        submitButton.disabled = false;
        submitButton.textContent = "Register";

    }

}

// Helpers

function showError(id, message) {

    const element =
        document.getElementById(id);

    if (element) {
        element.textContent = message;
    }

}

function clearErrors() {

    const errors =
        document.querySelectorAll(
            ".form-error"
        );

    errors.forEach(error => {
        error.textContent = "";
    });

}