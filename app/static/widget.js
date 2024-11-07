const chatbot = {
  init: function (config) {
    const container = document.querySelector(config.container);
    const position = config.position;
    const primaryColor = config.primaryColor;
    const secondaryColor = config.secondaryColor;
    const thirdColor = config.thirdColor;
    const welcomeMessage = config.welcomeMessage;
    const fontSize = config.fontSize;
    const chatbot_id = config.chatbot_id;
    const name = config.name;
    
    container.style.setProperty("--primary-color", primaryColor);
    container.style.setProperty("--secondary-color", secondaryColor);
    container.style.setProperty("--third-color", thirdColor);
    container.style.setProperty("--scale-factor-chatbot", fontSize);
    container.classList.add(position);

    container.innerHTML = `
          <button id="chatbot-toggler">
                <span class="material-symbols-rounded">mode_comment</span>
                <span class="material-symbols-rounded">close</span>
            </button>
            <div class="chatbot-popup">
                <div class="chat-header">
                    <div class="header-info">
                        <svg
                            class="chatbot-logo"
                            fill="#000000"
                            width="50px"
                            height="50px"
                            viewBox="0 0 24 24"
                            xmlns="http://www.w3.org/2000/svg">
                            <path
                            d="M21.928 11.607c-.202-.488-.635-.605-.928-.633V8c0-1.103-.897-2-2-2h-6V4.61c.305-.274.5-.668.5-1.11a1.5 1.5 0 0 0-3 0c0 .442.195.836.5 1.11V6H5c-1.103 0-2 .897-2 2v2.997l-.082.006A1 1 0 0 0 1.99 12v2a1 1 0 0 0 1 1H3v5c0 1.103.897 2 2 2h14c1.103 0 2-.897 2-2v-5a1 1 0 0 0 1-1v-1.938a1.006 1.006 0 0 0-.072-.455zM5 20V8h14l.001 3.996L19 12v2l.001.005.001 5.995H5z"
                            />
                            <ellipse cx="8.5" cy="12" rx="1.5" ry="2" />
                            <ellipse cx="15.5" cy="12" rx="1.5" ry="2" />
                            <path d="M8 16h8v2H8z" />
                        </svg>
                        <h2 class="logo-text">${name}</h2>
                    </div>
                    <button id="close-chatbot">
                        <svg fill="#fff " height="24px" width="24px" version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" 
                        viewBox="0 0 330 330" xml:space="preserve"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" 
                        stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> 
                        <path id="XMLID_225_" d="M325.607,79.393c-5.857-5.857-15.355-5.858-21.213,0.001l-139.39,139.393L25.607,79.393 c-5.857-5.857-15.355-5.858-21.213,0.001c-5.858,5.858-5.858,15.355,0,21.213l150.004,150c2.813,2.813,6.628,4.393,10.606,4.393 s7.794-1.581,10.606-4.394l149.996-150C331.465,94.749,331.465,85.251,325.607,79.393z"></path> </g></svg>
                    </button>
                </div>
                <div class="chat-body">
                    <div class="message bot-message">
                        <svg
                            class="bot-avatar"
                            fill="#000000"
                            width="50px"
                            height="50px"
                            viewBox="0 0 24 24"
                            xmlns="http://www.w3.org/2000/svg">
                            <path
                            d="M21.928 11.607c-.202-.488-.635-.605-.928-.633V8c0-1.103-.897-2-2-2h-6V4.61c.305-.274.5-.668.5-1.11a1.5 1.5 0 0 0-3 0c0 .442.195.836.5 1.11V6H5c-1.103 0-2 .897-2 2v2.997l-.082.006A1 1 0 0 0 1.99 12v2a1 1 0 0 0 1 1H3v5c0 1.103.897 2 2 2h14c1.103 0 2-.897 2-2v-5a1 1 0 0 0 1-1v-1.938a1.006 1.006 0 0 0-.072-.455zM5 20V8h14l.001 3.996L19 12v2l.001.005.001 5.995H5z"
                            />
                            <ellipse cx="8.5" cy="12" rx="1.5" ry="2" />
                            <ellipse cx="15.5" cy="12" rx="1.5" ry="2" />
                            <path d="M8 16h8v2H8z" />
                        </svg>
                        <div class="message-text">
                            ${welcomeMessage}
                        </div>
                    </div>
                        <div class="message user-message">
                        </div>
                </div>
                <div class="chat-footer">
                    <form action="#" class="chat-form">
                        <textarea
                            placeholder="Escribe tu consulta.."
                            required
                            class="message-input"
                        ></textarea>
                        <div class="chat-controls">
                            <button id="send-message">
                                <svg
                                viewBox="0 0 24 24"
                                fill="none"
                                xmlns="http://www.w3.org/2000/svg"
                                >
                                <g id="SVGRepo_bgCarrier"></g>
                                <g id="SVGRepo_tracerCarrier"></g>
                                <g id="SVGRepo_iconCarrier">
                                    <path
                                    d="M12 5V19M12 5L6 11M12 5L18 11"
                                    stroke="#fff"
                                    ></path>
                                </g>
                                </svg>
                            </button>
                        </div>
                    </form>
                </div>
            </div>`;

    const chatBody = document.querySelector(".chat-body");
    const messageInput = document.querySelector(".message-input");
    const sendMessageButton = document.querySelector("#send-message");
    const chatbotToggler = document.querySelector("#chatbot-toggler");
    const closeChatbot = document.querySelector("#close-chatbot");

    const ApiUrl = "https://7efb-191-115-199-8.ngrok-free.app/search";

    const userData = {
      chat_id: chatbot_id,
      question: null,
    };

    const initialInputHeight = messageInput.scrollHeight;

    const createMessageElement = (content, ...classes) => {
      const div = document.createElement("div");
      div.classList.add("message", ...classes);
      div.innerHTML = content;
      return div;
    };

    generateBotResponse = async (incomingMessageDiv) => {
      const messageElement = incomingMessageDiv.querySelector(".message-text");

      const requestOptions = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(userData),
      };

      try {
        const response = await fetch(ApiUrl, requestOptions);
        const data = await response.json();

        if (!response.ok) throw new Error(data.error.message);

        const apiResponseText = data.response;
        messageElement.innerHTML = apiResponseText;
      } catch (error) {
        messageElement.innerHTML = "Error al obtener la respuesta del bot.";
      } finally {
        incomingMessageDiv.classList.remove("thinking");
        chatBody.scrollTo({ top: chatBody.scrollHeight, behavior: "smooth" });
      }
    };

    const handleOutgoingMessage = (e) => {
      e.preventDefault();

      userData.question = messageInput.value.trim();
      messageInput.value = "";
      messageInput.style.height = `${initialInputHeight}px`;

      const messageContent = `<div class="message-text"></div>`;
      const outgoingMessageDiv = createMessageElement(
        messageContent,
        "user-message"
      );
      outgoingMessageDiv.querySelector(".message-text").textContent =
        userData.question;
      chatBody.appendChild(outgoingMessageDiv);

      chatBody.scrollTo({ top: chatBody.scrollHeight, behavior: "smooth" });

      setTimeout(() => {
        const botThinkingContent = `<svg class="bot-avatar" fill="#000000" width="50px" height="50px" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path d="M21.928 11.607c-.202-.488-.635-.605-.928-.633V8c0-1.103-.897-2-2-2h-6V4.61c.305-.274.5-.668.5-1.11a1.5 1.5 0 0 0-3 0c0 .442.195.836.5 1.11V6H5c-1.103 0-2 .897-2 2v2.997l-.082.006A1 1 0 0 0 1.99 12v2a1 1 0 0 0 1 1H3v5c0 1.103.897 2 2 2h14c1.103 0 2-.897 2-2v-5a1 1 0 0 0 1-1v-1.938a1.006 1.006 0 0 0-.072-.455zM5 20V8h14l.001 3.996L19 12v2l.001.005.001 5.995H5z"/>
                    <ellipse cx="8.5" cy="12" rx="1.5" ry="2" />
                    <ellipse cx="15.5" cy="12" rx="1.5" ry="2" />
                    <path d="M8 16h8v2H8z"/>
                </svg>
                <div class="message-text">
                    <div class="thinking-indicator">
                        <div class="dot"></div>
                        <div class="dot"></div>
                        <div class="dot"></div>
                    </div>
                </div>`;

        const incomingMessageDiv = createMessageElement(
          botThinkingContent,
          "bot-message",
          "thinking"
        );
        chatBody.appendChild(incomingMessageDiv);
        chatBody.scrollTo({ top: chatBody.scrollHeight, behavior: "smooth" });
        generateBotResponse(incomingMessageDiv);
      }, 1000);
    };

    messageInput.addEventListener("keydown", (e) => {
      const userMessage = e.target.value.trim();
      if (
        e.key == "Enter" &&
        userMessage &&
        !e.shiftKey &&
        window.innerWidth > 768
      ) {
        handleOutgoingMessage(e);
      }
    });

    messageInput.addEventListener("input", () => {
      messageInput.style.height = `${initialInputHeight}px`;
      messageInput.style.height = `${messageInput.scrollHeight}px`;
      document.querySelector(".chat-form").computedStyleMap.borderRaduis =
        messageInput.scrollHeight > initialInputHeight ? "15px" : "32px";
    });

    //probarEste
    /*messageInput.addEventListener("input", () => {
      messageInput.style.height = `${initialInputHeight}px`;
      messageInput.style.height = `${messageInput.scrollHeight}px`;
      const borderRadius =
        messageInput.scrollHeight > initialInputHeight ? "15px" : "32px";
      messageInput.style.borderRadius = borderRadius;
    });*/

    sendMessageButton.addEventListener("click", (e) =>
      handleOutgoingMessage(e)
    );

    chatbotToggler.addEventListener("click", () => {
      container.classList.toggle("show-chatbot");
    });

    closeChatbot.addEventListener("click", () => {
      container.classList.remove("show-chatbot");
    });
  },
};
