function getCookie(name) {
    const cookies = document.cookie ? document.cookie.split(";") : [];

    for (const cookie of cookies) {
        const trimmed = cookie.trim();

        if (trimmed.startsWith(`${name}=`)) {
            return decodeURIComponent(trimmed.substring(name.length + 1));
        }
    }

    return "";
}

function setText(id, message) {
    const element = document.getElementById(id);
    if (element) element.textContent = message || "";
}

function clearLoginErrors() {
    setText("loginEmailError", "");
    setText("loginPasswordError", "");
    setText("loginMessage", "");
}

async function handleLogin(event) {
    event.preventDefault();
    clearLoginErrors();

    const email = document.getElementById("loginEmail").value.trim();
    const password = document.getElementById("loginPassword").value;
    const button = document.querySelector("#loginForm button[type='submit']");

    let hasErrors = false;

    if (!email) {
        setText("loginEmailError", "Email is required");
        hasErrors = true;
    }

    if (!password) {
        setText("loginPasswordError", "Password is required");
        hasErrors = true;
    }

    if (hasErrors) return;

    button.disabled = true;
    button.textContent = "Signing in...";

    try {
        const response = await fetch("/api/login/", {
            method: "POST",
            credentials: "same-origin",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken"),
            },
            body: JSON.stringify({ email, password }),
        });

        const data = await response.json();

        if (!response.ok || !data.success) {
            setText("loginMessage", data.error || "Login failed");
            return;
        }

        window.location.href = data.redirect_url || "/dashboard/";
    } catch (error) {
        console.error(error);
        setText("loginMessage", "Network error. Please try again.");
    } finally {
        button.disabled = false;
        button.textContent = "Login";
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.getElementById("loginForm");
    if (loginForm) loginForm.addEventListener("submit", handleLogin);
});
