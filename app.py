from flask import Flask, request, jsonify, render_template
import requests
import json
import os

app = Flask(__name__)

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")

from prompts import CHANNELS


@app.route("/")
def index():
    channels = [{"id": k, "name": v["name"], "description": v["description"]} for k, v in CHANNELS.items()]
    return render_template("index.html", channels=channels)


@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    channel_id = data.get("channel")
    topic = data.get("topic", "").strip()
    brief = data.get("brief", "").strip()
    post_type = data.get("post_type", "post")

    if not channel_id or channel_id not in CHANNELS:
        return jsonify({"error": "Канал не выбран"}), 400
    if not topic:
        return jsonify({"error": "Укажите тему поста"}), 400

    channel = CHANNELS[channel_id]
    user_prompt = _build_user_prompt(topic, brief, post_type)

    try:
        result = _call_ollama(channel["system_prompt"], user_prompt)
        return jsonify({"text": result})
    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Ollama не запущена. Запустите: ollama serve"}), 503
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health")
def health():
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=3)
        models = [m["name"] for m in r.json().get("models", [])]
        return jsonify({"status": "ok", "ollama": True, "models": models})
    except Exception:
        return jsonify({"status": "ok", "ollama": False, "models": []})


def _build_user_prompt(topic, brief, post_type):
    type_instructions = {
        "post": "Напиши полноценный пост для Telegram.",
        "ideas": "Предложи 5 идей для постов по этой теме. Для каждой — заголовок и 1-2 строки о чём.",
        "short": "Напиши короткий пост для Telegram (до 80 слов).",
    }
    instruction = type_instructions.get(post_type, type_instructions["post"])

    prompt = f"Тема: {topic}\n\n"
    if brief:
        prompt += f"Дополнительный контекст / тезисы:\n{brief}\n\n"
    prompt += instruction
    return prompt


def _call_ollama(system_prompt, user_prompt):
    payload = {
        "model": OLLAMA_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "stream": False,
        "options": {
            "temperature": 0.8,
            "top_p": 0.9,
        },
    }
    response = requests.post(f"{OLLAMA_URL}/api/chat", json=payload, timeout=120)
    response.raise_for_status()
    return response.json()["message"]["content"]


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
