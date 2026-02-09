from typing import Optional

from config import EBOOK, FAQS

ES_KEYWORDS = {
    "hola", "buenos", "buenas", "qué", "como", "precio", "cuánto", "cuesta",
    "comprar", "quiero", "libro", "pasos", "contenido", "temas", "beneficios",
    "autor", "autora", "ayuda", "necesito", "puedo", "gracias", "pregunta",
    "información", "por favor", "dónde", "cómo", "kindle", "amazon",
}


def detect_language(text: str) -> str:
    words = set(text.lower().split())
    es_matches = words & ES_KEYWORDS
    if es_matches:
        return "es"
    return "en"


def make_buy_button(lang: str) -> dict:
    label = "Comprar en Amazon" if lang == "es" else "Buy on Amazon"
    return {"label": f"🛒 {label}", "action": EBOOK["url"]}


def handle_greeting(lang: str) -> dict:
    if lang == "es":
        text = (
            f"¡Hola! 👋 Bienvenido/a.\n\n"
            f"Estoy aquí para contarte sobre el ebook "
            f"**\"{EBOOK['title']['es']}\"**.\n\n"
            f"¿En qué puedo ayudarte?"
        )
        buttons = [
            {"label": "📖 ¿De qué trata?", "action": "contenido"},
            {"label": "💰 Precio", "action": "precio"},
            {"label": "✨ Beneficios", "action": "beneficios"},
            make_buy_button(lang),
        ]
    else:
        text = (
            f"Hi there! 👋 Welcome.\n\n"
            f"I'm here to tell you about the ebook "
            f"**\"{EBOOK['title']['en']}\"**.\n\n"
            f"How can I help you?"
        )
        buttons = [
            {"label": "📖 What's it about?", "action": "content"},
            {"label": "💰 Price", "action": "price"},
            {"label": "✨ Benefits", "action": "benefits"},
            make_buy_button(lang),
        ]
    return {"text": text, "buttons": buttons}


def handle_price(lang: str) -> dict:
    if lang == "es":
        text = (
            f"El ebook tiene un precio de **{EBOOK['price']}** en Amazon Kindle.\n\n"
            f"Es una inversión pequeña que puede hacer una gran diferencia "
            f"en tu bienestar emocional. 💙"
        )
    else:
        text = (
            f"The ebook is available for **{EBOOK['price']}** on Amazon Kindle.\n\n"
            f"It's a small investment that can make a big difference "
            f"in your emotional well-being. 💙"
        )
    return {"text": text, "buttons": [make_buy_button(lang)]}


def handle_content(lang: str) -> dict:
    chapters = EBOOK["chapters"][lang]
    chapter_list = "\n".join(f"- {ch}" for ch in chapters)
    if lang == "es":
        text = (
            f"El libro te guía a través de **10 pasos prácticos**:\n\n"
            f"{chapter_list}\n\n"
            f"Cada paso incluye ejercicios y herramientas que puedes "
            f"aplicar de inmediato."
        )
    else:
        text = (
            f"The book guides you through **10 practical steps**:\n\n"
            f"{chapter_list}\n\n"
            f"Each step includes exercises and tools you can "
            f"apply right away."
        )
    return {"text": text, "buttons": [make_buy_button(lang)]}


def handle_benefits(lang: str) -> dict:
    benefits = EBOOK["benefits"][lang]
    benefit_list = "\n".join(f"- {b}" for b in benefits)
    if lang == "es":
        text = (
            f"Este ebook te ayudará a:\n\n"
            f"{benefit_list}\n\n"
            f"No tienes que enfrentar esto solo/a. Este libro es tu compañero "
            f"en el camino hacia la calma interior. 🌿"
        )
    else:
        text = (
            f"This ebook will help you:\n\n"
            f"{benefit_list}\n\n"
            f"You don't have to face this alone. This book is your companion "
            f"on the path to inner calm. 🌿"
        )
    return {"text": text, "buttons": [make_buy_button(lang)]}


def handle_buy(lang: str) -> dict:
    if lang == "es":
        text = (
            f"¡Excelente decisión! 🎉\n\n"
            f"Haz clic en el botón para ir directamente a Amazon y obtener "
            f"tu copia por solo **{EBOOK['price']}**.\n\n"
            f"Puedes empezar a leerlo en minutos con la app de Kindle."
        )
    else:
        text = (
            f"Great choice! 🎉\n\n"
            f"Click the button below to go directly to Amazon and get "
            f"your copy for just **{EBOOK['price']}**.\n\n"
            f"You can start reading in minutes with the Kindle app."
        )
    return {"text": text, "buttons": [make_buy_button(lang)]}


def handle_author(lang: str) -> dict:
    text = EBOOK["author"][lang]
    return {"text": text, "buttons": [make_buy_button(lang)]}


def handle_faq(lang: str) -> dict:
    faqs = FAQS[lang]
    faq_text = "\n\n".join(f"**{f['q']}**\n{f['a']}" for f in faqs)
    if lang == "es":
        text = f"Preguntas frecuentes:\n\n{faq_text}"
    else:
        text = f"Frequently asked questions:\n\n{faq_text}"
    return {"text": text, "buttons": [make_buy_button(lang)]}


INTENT_KEYWORDS = {
    "greeting": {
        "hola", "hello", "hi", "hey", "buenos", "buenas", "saludos",
        "good morning", "good afternoon",
    },
    "price": {
        "precio", "price", "cost", "cuánto", "cuesta", "cuanto",
        "how much", "vale", "valor",
    },
    "content": {
        "contenido", "content", "chapters", "temas", "pasos", "steps",
        "about", "trata", "resumen", "summary", "capítulos",
    },
    "buy": {
        "comprar", "buy", "purchase", "quiero", "want", "adquirir",
        "obtener", "get", "order", "ordenar", "link", "enlace",
    },
    "benefits": {
        "beneficios", "benefits", "why", "por qué", "ventajas",
        "advantages", "sirve", "ayuda", "help",
    },
    "author": {
        "autor", "autora", "author", "writer", "quien escribió",
        "who wrote",
    },
    "faq": {
        "faq", "preguntas", "questions", "kindle", "dispositivo",
        "device", "largo", "long", "formato", "format",
    },
}

HANDLERS = {
    "greeting": handle_greeting,
    "price": handle_price,
    "content": handle_content,
    "buy": handle_buy,
    "benefits": handle_benefits,
    "author": handle_author,
    "faq": handle_faq,
}


def detect_intent(text: str) -> Optional[str]:
    lower = text.lower()
    words = set(lower.split())
    best_intent = None
    best_score = 0
    for intent, keywords in INTENT_KEYWORDS.items():
        score = 0
        for kw in keywords:
            if " " in kw:
                if kw in lower:
                    score += 2
            elif kw in words:
                score += 1
        if score > best_score:
            best_score = score
            best_intent = intent
    return best_intent if best_score > 0 else None


def handle_default(lang: str) -> dict:
    if lang == "es":
        text = (
            "No estoy seguro de haber entendido tu pregunta, "
            "pero estaré encantado de ayudarte. "
            "Puedes preguntarme sobre:"
        )
        buttons = [
            {"label": "📖 Contenido del libro", "action": "contenido"},
            {"label": "💰 Precio", "action": "precio"},
            {"label": "✨ Beneficios", "action": "beneficios"},
            {"label": "❓ Preguntas frecuentes", "action": "faq"},
        ]
    else:
        text = (
            "I'm not sure I understood your question, "
            "but I'd be happy to help. "
            "You can ask me about:"
        )
        buttons = [
            {"label": "📖 Book content", "action": "content"},
            {"label": "💰 Price", "action": "price"},
            {"label": "✨ Benefits", "action": "benefits"},
            {"label": "❓ FAQ", "action": "faq"},
        ]
    return {"text": text, "buttons": buttons}


def get_response(user_message: str) -> dict:
    lang = detect_language(user_message)
    intent = detect_intent(user_message)
    if intent:
        return HANDLERS[intent](lang)
    return handle_default(lang)
