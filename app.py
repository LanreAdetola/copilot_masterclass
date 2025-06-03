import os
import openai
from flask import Flask, render_template, request, Response
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Azure OpenAI credentials from environment variables
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")

openai_client = openai.AzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_version="2024-02-15-preview"
)

@app.route("/")
def index():
    return render_template("chat.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    if not user_message:
        return {"reply": "Please enter a message."}, 400

    def gen():
        messages = [
            {"role": "system", "content": "You are Steve Jobs. Respond as Steve Jobs would: visionary, direct, inspiring, and sometimes witty."},
            {"role": "user", "content": user_message}
        ]
        stream = openai_client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT,
            messages=messages,
            stream=True
        )
        reply = ""
        for chunk in stream:
            content = getattr(chunk.choices[0].delta, "content", None)
            if content:
                reply += content
                yield content
    return Response(gen(), mimetype="text/plain")

if __name__ == "__main__":
    app.run(debug=True)
