$(document).ready(() => {
    $(".chatbox-open").click(() =>
      $(".chatbox-popup, .chatbox-close").fadeIn()
    );
  
    $(".chatbox-close").click(() =>
      $(".chatbox-popup, .chatbox-close").fadeOut()
    );
  
    $(".chatbox-maximize").click(() => {
      $(".chatbox-popup, .chatbox-open, .chatbox-close").fadeOut();
      $(".chatbox-panel").fadeIn();
      $(".chatbox-panel").css({ display: "flex" });
    });
  
    $(".chatbox-minimize").click(() => {
      $(".chatbox-panel").fadeOut();
      $(".chatbox-popup, .chatbox-open, .chatbox-close").fadeIn();
    });
  
    $(".chatbox-panel-close").click(() => {
      $(".chatbox-panel").fadeOut();
      $(".chatbox-open").fadeIn();
    });
  });

  const chatboxPopupMessagesDiv = document.getElementById("chatbox-popup-messages");
  const chatboxPopupInput = document.getElementById("chatbox-popup-input");
  const chatboxPopupSendButton = document.getElementById("chatbox-popup-send-button");

  // Load previous messages from local storage when the page loads
  const savedMessages = JSON.parse(localStorage.getItem("chatboxPopupMessages")) || [];
  savedMessages.forEach(savedMessage => {
      displayChatboxPopupMessage(savedMessage.message, savedMessage.sender);
  });

  chatboxPopupSendButton.addEventListener("click", sendChatboxPopupMessage);

  function sendChatboxPopupMessage() {
      const userMessage = chatboxPopupInput.value.trim();
      if (userMessage !== "") {
          displayChatboxPopupMessage(userMessage, "user");
          respondToChatboxPopupMessage(userMessage);
          chatboxPopupInput.value = "";

          // Save the messages to local storage
          const messagesToSave = JSON.parse(localStorage.getItem("chatboxPopupMessages")) || [];
          messagesToSave.push({ message: userMessage, sender: "user" });
          localStorage.setItem("chatboxPopupMessages", JSON.stringify(messagesToSave));
      }
  }

  function displayChatboxPopupMessage(message, sender) {
      const messageDiv = document.createElement("div");
      messageDiv.className = `message ${sender}`;
      messageDiv.textContent = message;
      chatboxPopupMessagesDiv.appendChild(messageDiv);
      chatboxPopupMessagesDiv.scrollTop = chatboxPopupMessagesDiv.scrollHeight;
  }

  function respondToChatboxPopupMessage(message) {
      const response = getChatboxPopupResponse(message);
      displayChatboxPopupMessage(response, "bot");

      // Save the bot's response to local storage
      const messagesToSave = JSON.parse(localStorage.getItem("chatboxPopupMessages")) || [];
      messagesToSave.push({ message: response, sender: "bot" });
      localStorage.setItem("chatboxPopupMessages", JSON.stringify(messagesToSave));
  }

  function getChatboxPopupResponse(message) {
      // Define your response logic here
      // For this example, let's use a simple predefined response
      if (message.toLowerCase().includes("hi")) {
          return "Hello! How can I assist you?";
      } else if (message.toLowerCase().includes("how are you")) {
          return "I'm just a chatbot, but I'm here to help!";
      } else {
          return "I'm here to assist you!";
      }
  }