// auth.js

// Function to handle sign-up
function handleSignUp(event) {
    event.preventDefault();
    const username = document.getElementById("signup-username").value;
    const password = document.getElementById("signup-password").value;

    if (username === "" || password === "") {
        alert("Please fill in all fields.");
        return;
    }

    // Check if user already exists
    if (localStorage.getItem(username)) {
        alert("User already exists. Please sign in.");
        return;
    }

    // Save credentials to localStorage
    localStorage.setItem(username, password);
    alert("Sign up successful! You can now sign in.");
    window.location.href = "signin.html";
}

// Function to handle sign-in
function handleSignIn(event) {
    event.preventDefault();
    const username = document.getElementById("signin-username").value;
    const password = document.getElementById("signin-password").value;

    const storedPassword = localStorage.getItem(username);

    if (!storedPassword) {
        alert("No such user found. Please sign up.");
    } else if (storedPassword !== password) {
        alert("Incorrect password. Try again.");
    } else {
        alert("Login successful!");
        localStorage.setItem("currentUser", username);  // Save current user
        window.location.href = "profile.html";
    }
}

// Function to display current user's profile
function loadProfile() {
    const currentUser = localStorage.getItem("currentUser");
    if (!currentUser) {
        alert("You must log in first.");
        window.location.href = "signin.html";
    } else {
        document.getElementById("profile-username").innerText = currentUser;
    }
}

// Function to log out
function handleLogout() {
    localStorage.removeItem("currentUser");
    window.location.href = "signin.html";
}
