console.log("Hello from My App!");
// Get elements from the HTML
const message = document.getElementById("message");
const button = document.getElementById("changeBtn");

// Add a click event to the button
button.addEventListener("click", function() {
    message.textContent = "You clicked the button! 🎉";
});
