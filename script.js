const sendBtn = document.getElementById("send-btn");
        const chatbox = document.getElementById("chatbox");
        const userInput = document.getElementById("userInput");

        // Mock chatbot response
        function getBotResponse(input) {
            const responses = {
                "hi" : "Hello! How can I assist you today?",
                "hii":"Hello! How can I assist you today?",
                "hello": "Hello! How can I assist you today?",
                "how are you": "I'm just a chatbot, but I'm here to help you!",
                "bye": "Goodbye! Have a great day!"
            };

            return responses[input.toLowerCase()] || "Sorry, I don't understand that.";
        }

        // Add message to chatbox
        function addMessage(content, type) {
            const chat = document.createElement("li");
            chat.classList.add("chat", type === "incoming" ? "chat-incoming" : "chat-outgoing");

            if (type === "incoming") {
                chat.innerHTML = `
                    <span class="material-symbols-outlined">smart_toy</span>
                    <p>${content}</p>
                `;
            } else {
                chat.innerHTML = `<p>${content}</p>`;
            }

            chatbox.appendChild(chat);
            chatbox.scrollTop = chatbox.scrollHeight;
        }

        // Send message
        sendBtn.addEventListener("click", () => {
            const message = userInput.value.trim();

            if (message) {
                addMessage(message, "outgoing");
                userInput.value = "";
                setTimeout(() => {
                    const botResponse = getBotResponse(message);
                    addMessage(botResponse, "incoming");
                }, 500);
            }
        });