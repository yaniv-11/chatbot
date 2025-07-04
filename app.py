from flask import Flask, render_template, request,session
from config import Config
import google.generativeai as genai
# Initialize Flask app with configuration
app = Flask(__name__)
app.config.from_object(Config)



# Create Gemini model
genai.configure(api_key=app.config["GEMINI_API_KEY"])
model = genai.GenerativeModel(model_name="models/gemini-2.0-flash")
chat = model.start_chat(history=[])

@app.route("/", methods=["GET", "POST"])
def index():
    if "chat" not in session:
        session["chat"] = []

    if request.method == "POST":
        user_input = request.form["message"]
        if user_input:
            # Add user message
            session["chat"].append(("user", user_input))

            # Get bot response
            valid_chat_history = []
            for role, text in session["chat"]:
                if role in ["user", "model"]:
                    valid_chat_history.append({"role": role, "parts": [text]})
                else:
                    print("⚠️ Invalid role found in session history:", role)
            # Use the global 'chat' instance
            response = chat.send_message(user_input)
            session["chat"].append(("model", response.text))
            session.modified = True  # Required to update session

    return render_template("index.html", chat=session["chat"])

if __name__ == "__main__":
    app.run(debug=True)
