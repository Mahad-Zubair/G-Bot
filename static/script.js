async function sendMessage(){
    let userInput = document.getElementById("user-input").value;
    if (!userInput) return;

    let chatBox = document.getElementById("chat-box");

    // Display User Message
    let userMessage = `<p class="user-message"><strong>You:</strong> ${userInput}</p>`;
    chatBox.innerHTML += userMessage;

    document.getElementById("user-input").value = "";

    // Send Message to Backend
    let response = await fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: userInput })
    });

    let data = await response.json();

    // Format Bot Response: replace newline characters with <br> tags
    let formattedBotMessage = data.response.replace(/\n/g, "<br>");

    // Display Bot Response
    let botMessage = `<p class="bot-message"><strong>Bot:</strong> ${formattedBotMessage}</p>`;
    chatBox.innerHTML += botMessage;

    // Auto-scroll to the latest message
    chatBox.scrollTop = chatBox.scrollHeight;
}

document.getElementById("user-input").addEventListener("keypress", function(event){
    if (event.key === "Enter"){
        event.preventDefault();
        sendMessage();
    }
});
