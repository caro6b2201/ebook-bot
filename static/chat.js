(() => {
  const widget   = document.getElementById("chat-widget");
  const toggle   = document.getElementById("chat-toggle");
  const form     = document.getElementById("chat-form");
  const input    = document.getElementById("chat-input");
  const messages = document.getElementById("chat-messages");
  const typing   = document.getElementById("chat-typing");

  const AMAZON_URL = "https://www.amazon.com/dp/B0GL9KVRDW";

  let isOpen = false;
  let hasGreeted = false;

  /* ---- Toggle chat ---- */
  toggle.addEventListener("click", () => {
    isOpen = !isOpen;
    widget.classList.toggle("open", isOpen);
    if (isOpen) {
      input.focus();
      if (!hasGreeted) {
        hasGreeted = true;
        sendMessage("hello");
      }
    }
  });

  /* ---- Send on submit ---- */
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const text = input.value.trim();
    if (!text) return;
    appendMessage(text, "user");
    input.value = "";
    sendMessage(text);
  });

  /* ---- Send message to API ---- */
  async function sendMessage(text) {
    showTyping(true);
    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text }),
      });
      const data = await res.json();
      showTyping(false);
      appendBotMessage(data);
    } catch {
      showTyping(false);
      appendMessage("Connection error. Please try again.", "bot");
    }
  }

  /* ---- Render bot message with optional buttons ---- */
  function appendBotMessage(data) {
    const wrapper = document.createElement("div");
    wrapper.classList.add("msg", "bot");

    /* Convert markdown bold **text** to <strong> */
    const htmlText = data.text
      .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
      .replace(/\n/g, "<br>");
    wrapper.innerHTML = htmlText;

    if (data.buttons && data.buttons.length) {
      const btnContainer = document.createElement("div");
      btnContainer.classList.add("msg-buttons");
      data.buttons.forEach((btn) => {
        const el = document.createElement("button");
        el.classList.add("msg-btn");
        el.textContent = btn.label;
        el.addEventListener("click", () => handleButton(btn));
        btnContainer.appendChild(el);
      });
      wrapper.appendChild(btnContainer);
    }

    messages.appendChild(wrapper);
    scrollToBottom();
  }

  /* ---- Handle button click ---- */
  function handleButton(btn) {
    if (btn.action.startsWith("http")) {
      window.open(btn.action, "_blank", "noopener");
    } else {
      appendMessage(btn.label, "user");
      sendMessage(btn.action);
    }
  }

  /* ---- Append plain message ---- */
  function appendMessage(text, role) {
    const el = document.createElement("div");
    el.classList.add("msg", role);
    el.textContent = text;
    messages.appendChild(el);
    scrollToBottom();
  }

  /* ---- Typing indicator ---- */
  function showTyping(show) {
    typing.classList.toggle("hidden", !show);
    if (show) scrollToBottom();
  }

  /* ---- Auto-scroll ---- */
  function scrollToBottom() {
    requestAnimationFrame(() => {
      messages.scrollTop = messages.scrollHeight;
    });
  }
})();
