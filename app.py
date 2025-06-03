from flask import Flask, request, jsonify
from flask_cors import CORS
import difflib, re, json, os

app = Flask(__name__)
CORS(app)

# Base hardcoded FAQs
base_faq = {
    "what services do you offer": "We offer Electrical Drawing, Load Schedule, NOC Application (DEWA), and repairs.",
    "are you dewa licensed": "Yes, we are a DEWA-licensed electrical contracting company.",
    "how can i get a price quote": "Pricing depends on the project. Please contact us directly.",
    "do you do home electrical repairs": "Yes, we offer residential and commercial electrical repairs and installation.",
    "where are you located": "We are located in [residential oasis in Qusais].",
    "how can i contact you": "You can contact us at [0501229354]."
}

# Load learned Q&A from JSON file
def load_learned_faq(path="learned_faq.json"):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

learned_faq = load_learned_faq()
faq_data = {**base_faq, **learned_faq}  # Combine both

# --- Clean text ---
def clean(text):
    return re.sub(r'[^a-z ]', '', text.lower().strip())

# --- Log unmatched questions ---
def log_unmatched_question(user_input):
    with open("unmatched_questions.txt", "a", encoding="utf-8") as f:
        f.write(user_input + "\n")

# --- Get reply using fuzzy match ---
def get_bot_reply(user_input):
    user_input_clean = clean(user_input)
    questions = [clean(q) for q in faq_data.keys()]
    match = difflib.get_close_matches(user_input_clean, questions, n=1, cutoff=0.6)

    if match:
        matched_question = list(faq_data.keys())[questions.index(match[0])]
        return faq_data[matched_question]
    else:
        log_unmatched_question(user_input)
        return "Sorry, I didn't understand that. You can ask about our services, DEWA, or pricing."

# --- Chat route ---
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    reply = get_bot_reply(user_message)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
