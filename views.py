from flask import Blueprint, render_template, request, jsonify

from chatbot import Chatbot

views = Blueprint("views", __name__)

bot = Chatbot()
bot.load_dialogs("data/dialogs.txt")
print("Chatbot loaded")

@views.route("/")
def home():
    return render_template("index.html")

@views.route("/send_message", methods=["POST"])
def send_message():
    question = request.form.get("chat_input")
    response = bot.chat(question)
    return jsonify({"response": response})