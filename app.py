from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Simulate Steve Jobs responses
def steve_jobs_reply(user_message):
    # Simple hardcoded responses for demo
    responses = [
        "Innovation distinguishes between a leader and a follower.",
        "Your time is limited, so don’t waste it living someone else’s life.",
        "Stay hungry. Stay foolish.",
        "Design is not just what it looks like and feels like. Design is how it works.",
        "Sometimes life hits you in the head with a brick. Don’t lose faith."
    ]
    import random
    return random.choice(responses)

@app.route("/")
def index():
    return render_template("chat.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    steve_reply = steve_jobs_reply(user_message)
    return jsonify({"reply": steve_reply})

if __name__ == "__main__":
    app.run(debug=True)
