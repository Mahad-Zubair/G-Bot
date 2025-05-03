async function sendMessage() {
    const userInputField = document.getElementById("user-input");
    const userInput = userInputField.value.trim();
    const chatBox = document.getElementById("chat-box");

    if (!userInput) return;

    // Display user's message
    const userMessage = `<div class="user-message"><strong>You:</strong> ${userInput}</div>`;
    chatBox.innerHTML += userMessage;
    userInputField.value = "";

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: userInput })
        });

        const data = await response.json();
        const botResponseHTML = data.response || "⚠️ No response from the bot.";

        // Display bot's response (already HTML formatted via markdown2 on the backend)
        const botMessage = `<div class="bot-message"><strong>Bot:</strong><br>${botResponseHTML}</div>`;
        chatBox.innerHTML += botMessage;
    } catch (error) {
        console.error("Error:", error);
        chatBox.innerHTML += `<div class="bot-message"><strong>Bot:</strong> ⚠️ Error: Could not connect to the server.</div>`;
    }

    chatBox.scrollTop = chatBox.scrollHeight;
}

// Send message on Enter key
document.getElementById("user-input").addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
        event.preventDefault();
        sendMessage();
    }
});
