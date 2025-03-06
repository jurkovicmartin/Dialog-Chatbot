function toggle_chat() {
    const chatbox = document.getElementById("chatbox");
    const toggleBtn = document.getElementById("toggle_btn");
    
    if (chatbox.style.display === "block") {
        chatbox.style.display = "none";
        toggleBtn.style.display = "block";
    } else {
        chatbox.style.display = "block";
        toggleBtn.style.display = "none";
    }
}

function send_message() {
    // Prevent default behavior (showing jsonify data)
    event.preventDefault();
  
    const input = document.getElementById("chat_input");
    const submitButton = document.getElementById("submit");
    // Get the user's message
    const message = input.value.trim();
    if (message !== "") {
        // Disable the input field and submit button
        input.disabled = true;
        submitButton.disabled = true;

        const chatBody = document.getElementById("chatbox_body");
        // Create a massage element for user's message
        const msgElement = document.createElement("div");
        msgElement.textContent = message;
        msgElement.className = "message user_message";
        chatBody.appendChild(msgElement);
        // Scroll to the bottom (for case of long conversation)
        chatBody.scrollTop = chatBody.scrollHeight;

        // Clear the input field
        input.value = "";
        
        // Create a message element for the bot's response
        const responseElement = document.createElement("div");
        responseElement.className = "message response_message";
        // Loading indicator
        responseElement.textContent = "...";
        chatBody.appendChild(responseElement);
        chatBody.scrollTop = chatBody.scrollHeight;

        // Send a POST request to /send_message with the user's message
        fetch("/send_message", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ chat_input: message })
        })
        .then(response => response.json())
        .then(data => {
        // Response
        responseElement.textContent = data.response;
        chatBody.scrollTop = chatBody.scrollHeight;
        // Enable the input field and submit button again
        input.disabled = false;
        submitButton.disabled = false;
        });
    }
}