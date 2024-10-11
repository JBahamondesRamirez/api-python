from db.client import db_client
from fastapi import Response



async def generate_chatbot(client_id: str):
    config_chatbot = db_client.chatbots.find_one({"clientId":(client_id)})

    position = config_chatbot["position"] 
    primaryColor = config_chatbot["primaryColor"]
    secondaryColor = config_chatbot["secondaryColor"]
    thirdColor = config_chatbot["thirdColor"]

    html_content = f"""
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
            <h2 class="logo-text">Chatbot</h2>
            </div>
            <button id="close-chatbot" class="material-symbols-rounded">
            keyboard_arrow_down
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
                xmlns="http://www.w3.org/2000/svg"
            >
                <path
                d="M21.928 11.607c-.202-.488-.635-.605-.928-.633V8c0-1.103-.897-2-2-2h-6V4.61c.305-.274.5-.668.5-1.11a1.5 1.5 0 0 0-3 0c0 .442.195.836.5 1.11V6H5c-1.103 0-2 .897-2 2v2.997l-.082.006A1 1 0 0 0 1.99 12v2a1 1 0 0 0 1 1H3v5c0 1.103.897 2 2 2h14c1.103 0 2-.897 2-2v-5a1 1 0 0 0 1-1v-1.938a1.006 1.006 0 0 0-.072-.455zM5 20V8h14l.001 3.996L19 12v2l.001.005.001 5.995H5z"
                />
                <ellipse cx="8.5" cy="12" rx="1.5" ry="2" />
                <ellipse cx="15.5" cy="12" rx="1.5" ry="2" />
                <path d="M8 16h8v2H8z" />
            </svg>
            <div class="message-text">
                Hola 😍<br />
                Como puedo ayudar hoy?
            </div>
            </div>
            <div class="message user-message">
            </div>
        </div>
        <div class="chat-footer">
            <form action="#" class="chat-form">
            <textarea
                placeholder="Message..."
                required
                class="message-input"
            ></textarea>
            <div class="chat-controls">
                <button
                type="submit"
                id="send-message"
                class="material-symbols-rounded"
                >
                arrow_upward
                </button>
            </div>
            </form>
        </div>
        </div>
        """

    script = f"""
    (function() {{
        window.Chatbot = {{
            init: function() {{
                const chatbotContainer = document.createElement('div');
                chatbotContainer.id = 'chatbot-container';
                chatbotContainer.style.position = 'fixed';
                var link = document.createElement('link');
                link.type = 'text/css';
                link.rel = 'stylesheet';
                link.href = 'http://localhost:8000/static/style.css'
                document.head.appendChild(link);
                var linkIcons = document.createElement('link');
                linkIcons.rel = 'stylesheet';
                linkIcons.href = 'https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@48,400,0,0'
                document.head.appendChild(linkIcons);
                chatbotContainer.style.{position.split('-')[0]} = '90px';
                chatbotContainer.style.{position.split('-')[1]} = '10px'; 

                chatbotContainer.style.setProperty('--primary-color', "{primaryColor}");
                chatbotContainer.style.setProperty('--secondary-color', "{secondaryColor}");
                chatbotContainer.style.setProperty('--thrid-color', "{thirdColor}");

                chatbotContainer.innerHTML = `{html_content}`;

                document.body.appendChild(chatbotContainer);
                const chatBody = document.querySelector(".chat-body");
                const messageInput = document.querySelector(".message-input");
                const sendMessageButton = document.querySelector("#send-message");
                const chatbotToggler = document.querySelector("#chatbot-toggler");
                const closeChatbot = document.querySelector("#close-chatbot");

                const ApiUrl = `http://localhost:8000/chatbot/mensajePrueba`;

                const userData = {{
                    message: null,
                }};

                const initialInputHeight = messageInput.scrollHeight;

                const createMessageElement = (content, ...classes) => {{
                    const div = document.createElement("div");
                    div.classList.add("message", ...classes);
                    div.innerHTML = content;
                    return div;
                }};

                generateBotResponse = async (incomingMessageDiv) => {{
                    const messageElement = incomingMessageDiv.querySelector(".message-text");

                    const requestOptions = {{
                        method: "POST",
                        headers: {{"Content-Type": "application/json"}},
                        body: JSON.stringify({{ text: userData.message }}),
                    }};

                    try {{
                        const response = await fetch(ApiUrl, requestOptions);
                        const data = await response.json();
                        if (!response.ok) throw new Error(data.error.message);
                        const apiResponseText = data.response;
                        messageElement.innerHTML = apiResponseText;
                    }} catch (error) {{
                        console.log(error);
                    }} finally {{
                        incomingMessageDiv.classList.remove("thinking");
                        chatBody.scrollTo({{ top: chatBody.scrollHeight, behavior: "smooth" }});
                    }}
                }};

                const handleOutgoingMessage = (e) => {{
                    e.preventDefault();
                    userData.message = messageInput.value.trim();
                    messageInput.value = "";
                    messageInput.dispatchEvent(new Event("input"));
                    const messageContent = `<div class="message-text"></div>`;
                    const outgoingMessageDiv = createMessageElement(
                        messageContent,
                        "user-message"
                    );
                    outgoingMessageDiv.querySelector(".message-text").textContent =
                        userData.message;
                    chatBody.appendChild(outgoingMessageDiv);
                    chatBody.scrollTo({{ top: chatBody.scrollHeight, behavior: "smooth" }});
                    setTimeout(() => {{
                        const messageContent = `<svg class="bot-avatar" fill="#000000" width="50px"height="50px"
                                viewBox="0 0 24 24"
                                xmlns="http://www.w3.org/2000/svg"
                            >
                            <path
                                d="M21.928 11.607c-.202-.488-.635-.605-.928-.633V8c0-1.103-.897-2-2-2h-6V4.61c.305-.274.5-.668.5-1.11a1.5 1.5 0 0 0-3 0c0 .442.195.836.5 1.11V6H5c-1.103 0-2 .897-2 2v2.997l-.082.006A1 1 0 0 0 1.99 12v2a1 1 0 0 0 1 1H3v5c0 1.103.897 2 2 2h14c1.103 0 2-.897 2-2v-5a1 1 0 0 0 1-1v-1.938a1.006 1.006 0 0 0-.072-.455zM5 20V8h14l.001 3.996L19 12v2l.001.005.001 5.995H5z"
                            />
                            <ellipse cx="8.5" cy="12" rx="1.5" ry="2" />
                            <ellipse cx="15.5" cy="12" rx="1.5" ry="2" />
                            <path d="M8 16h8v2H8z" />
                          </svg>
                          <div class="message-text">
                            <div class="thinking-indicator">
                              <div class="dot"></div>
                              <div class="dot"></div>
                              <div class="dot"></div>
                            </div>
                          </div>`;
                        const incomingMessageDiv = createMessageElement(
                          messageContent,
                          "bot-message",
                          "thinking"
                        );
                        chatBody.scrollTo({{ top: chatBody.scrollHeight, behavior: "smooth" }});
                        chatBody.appendChild(incomingMessageDiv);
                        generateBotResponse(incomingMessageDiv);
                    }}, 600);
                }};
                messageInput.addEventListener("keydown", (e) => {{
                    const userMessage = e.target.value.trim();
                    if (e.key == "Enter" && userMessage && !e.shiftKey && window.innerWidth > 768) {{
                        handleOutgoingMessage(e);
                    }}
                }});
                messageInput.addEventListener("input", () => {{
                    messageInput.style.height = `${{initialInputHeight}}px`
                    messageInput.style.height = `${{messageInput.scrollHeight}}px`
                    document.querySelector(".chat-form").computedStyleMap.borderRaduis = messageInput.scrollHeight >
                    initialInputHeight ? "15px" : "32px";
                }});
                sendMessageButton.addEventListener("click", (e) => handleOutgoingMessage(e));
                chatbotToggler.addEventListener("click", () => document.body.classList.toggle("show-chatbot"));
                closeChatbot.addEventListener("click", () => document.body.classList.remove("show-chatbot"));
            }}
        }};
        window.Chatbot.init();
    }})();
    """

    return Response(script, media_type="application/javascript")
