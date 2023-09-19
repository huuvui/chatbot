from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from langdetect import detect

app = Flask(__name__)

english_bot = ChatBot("Chatterbot", storage_adapter="chatterbot.storage.SQLStorageAdapter")
trainer = ChatterBotCorpusTrainer(english_bot)
trainer.train("chatterbot.corpus.english")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    userText = userText.lower()  # Biến đổi chuỗi thành chữ thường
    
    # Kiểm tra ngôn ngữ của yêu cầu
    language = detect(userText)
    
    # Nếu ngôn ngữ không phải tiếng Anh, thì mới xử lý
    if language != 'en':
        # Lấy kết quả từ ChatBot
        bot_response = english_bot.get_response(userText)
    
        # Kiểm tra xem kết quả có phù hợp không
        if float(bot_response.confidence) < 0.5:
            return "Xin lỗi, không tìm thấy kết quả phù hợp!"
    
        return str(bot_response)
    else:
        return "Xin lỗi, không tìm thấy kết quả phù hợp!"

if __name__ == "__main__":
    app.run()
