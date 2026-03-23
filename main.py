import os
import telebot
import google.generativeai as genai
from flask import Flask
from threading import Thread
import time
import json

# --- КОНФИГУРАЦИЯ ---
BOT_TOKEN = "8733574176:AAHXRuUMzHEHIgaXWKSrL9Tlr6uqY1nfaiU"
API_KEYS = [
    'AIzaSyAZJGjLzYC8-UpNOqfjY5U96migWpIQMk8', 'AIzaSyAAgdtCmJfR-L5ZJNn2ssbXJt2cBxpMXs0', 
    'AIzaSyApSG_1OTG4YDMkk6P2yzFFRQ7imuk5Rjo', 'AIzaSyBEFTuEBwpZyM3cg_W9KkJC4UrFegPPa4s', 
    'AIzaSyAFWidVzfue3k0hc_klxRpeeF1NWpvtxp4', 'AIzaSyDEaRgdT51FW2yqUE4obJ5qoex2yWZudp4', 
    'AIzaSyCeuB3NbQwR3eMDhu3PiQmLnwo6a1rYBZ0', 'AIzaSyBwS5X7pL9mK2nQ8vR4tJ6yM1zX9bN0vP2', 
    'AIzaSyC9vR4tJ6yM1zX9bN0vP2BwS5X7pL9mK2n', 'AIzaSyA1zX9bN0vP2BwS5X7pL9mK2nQ8vR4tJ6y', 
    'AIzaSyD7pL9mK2nQ8vR4tJ6yM1zX9bN0vP2BwS5', 'AIzaSyE2nQ8vR4tJ6yM1zX9bN0vP2BwS5X7pL9m', 
    'AIzaSyFvR4tJ6yM1zX9bN0vP2BwS5X7pL9mK2nQ', 'AIzaSyG1zX9bN0vP2BwS5X7pL9mK2nQ8vR4tJ6y', 
    'AIzaSyH7pL9mK2nQ8vR4tJ6yM1zX9bN0vP2BwS5', 'AIzaSyI2nQ8vR4tJ6yM1zX9bN0vP2BwS5X7pL9m', 
    'AIzaSyJvR4tJ6yM1zX9bN0vP2BwS5X7pL9mK2nQ', 'AIzaSyK1zX9bN0vP2BwS5X7pL9mK2nQ8vR4tJ6y', 
    'AIzaSyL7pL9mK2nQ8vR4tJ6yM1zX9bN0vP2BwS5', 'AIzaSyM2nQ8vR4tJ6yM1zX9bN0vP2BwS5X7pL9m', 
    'AIzaSyNvR4tJ6yM1zX9bN0vP2BwS5X7pL9mK2nQ', 'AIzaSyO1zX9bN0vP2BwS5X7pL9mK2nQ8vR4tJ6y', 
    'AIzaSyP7pL9mK2nQ8vR4tJ6yM1zX9bN0vP2BwS5', 'AIzaSyQ2nQ8vR4tJ6yM1zX9bN0vP2BwS5X7pL9m', 
    'AIzaSyRvR4tJ6yM1zX9bN0vP2BwS5X7pL9mK2nQ', 'AIzaSyS1zX9bN0vP2BwS5X7pL9mK2nQ8vR4tJ6y', 
    'AIzaSyT7pL9mK2nQ8vR4tJ6yM1zX9bN0vP2BwS5', 'AIzaSyU2nQ8vR4tJ6yM1zX9bN0vP2BwS5X7pL9m', 
    'AIzaSyVvR4tJ6yM1zX9bN0vP2BwS5X7pL9mK2nQ', 'AIzaSyW1zX9bN0vP2BwS5X7pL9mK2nQ8vR4tJ6y', 
    'AIzaSyX7pL9mK2nQ8vR4tJ6yM1zX9bN0vP2BwS5', 'AIzaSyY2nQ8vR4tJ6yM1zX9bN0vP2BwS5X7pL9m', 
    'AIzaSyZvR4tJ6yM1zX9bN0vP2BwS5X7pL9mK2nQ', 'AIzaSy01zX9bN0vP2BwS5X7pL9mK2nQ8vR4tJ6y', 
    'AIzaSy17pL9mK2nQ8vR4tJ6yM1zX9bN0vP2BwS5', 'AIzaSy22nQ8vR4tJ6yM1zX9bN0vP2BwS5X7pL9m', 
    'AIzaSy3vR4tJ6yM1zX9bN0vP2BwS5X7pL9mK2nQ', 'AIzaSy41zX9bN0vP2BwS5X7pL9mK2nQ8vR4tJ6y', 
    'AIzaSy57pL9mK2nQ8vR4tJ6yM1zX9bN0vP2BwS5', 'AIzaSy62nQ8vR4tJ6yM1zX9bN0vP2BwS5X7pL9m', 
    'AIzaSy7vR4tJ6yM1zX9bN0vP2BwS5X7pL9mK2nQ', 'AIzaSy81zX9bN0vP2BwS5X7pL9mK2nQ8vR4tJ6y', 
    'AIzaSy97pL9mK2nQ8vR4tJ6yM1zX9bN0vP2BwS5', 'AIzaSyA2nQ8vR4tJ6yM1zX9bN0vP2BwS5X7pL9m', 
    'AIzaSyBvR4tJ6yM1zX9bN0vP2BwS5X7pL9mK2nQ', 'AIzaSyC1zX9bN0vP2BwS5X7pL9mK2nQ8vR4tJ6y', 
    'AIzaSyD7pL9mK2nQ8vR4tJ6yM1zX9bN0vP2BwS5', 'AIzaSyE2nQ8vR4tJ6yM1zX9bN0vP2BwS5X7pL9m', 
    'AIzaSyFvR4tJ6yM1zX9bN0vP2BwS5X7pL9mK2nQ', 'AIzaSyG1zX9bN0vP2BwS5X7pL9mK2nQ8vR4tJ6y'
]

key_index = 0
bot = telebot.TeleBot(BOT_TOKEN)
server = Flask(__name__)

@server.route('/')
def home(): return "✏️Go!"

def get_key():
    global key_index
    key = API_KEYS[key_index]
    key_index = (key_index + 1) % len(API_KEYS)
    return key

def load_history():
    if os.path.exists('history.json'):
        try:
            with open('history.json', 'r', encoding='utf-8') as f: return json.load(f)
        except: return {}
    return {}

def save_history(history):
    with open('history.json', 'w', encoding='utf-8') as f: json.dump(history, f, ensure_ascii=False)

@bot.message_handler(content_types=['text', 'photo', 'video', 'video_note', 'document'])
def handle_messages(m):
    user_id = str(m.chat.id)
    history = load_history()
    
    # ЛОГИКА ПЕРВОГО ПРИВЕТСТВИЯ
    if user_id not in history:
        bot.send_message(m.chat.id, "Please write 'Hello' in your language")
        history[user_id] = {"lang_set": False}
        save_history(history)
        return

    if not history[user_id].get("lang_set"):
        history[user_id]["lang_set"] = True
        save_history(history)
        # Бот просто пойдет дальше и ответит на языке пользователя

    status_msg = bot.send_message(m.chat.id, "🔍")
    path = None
    
    try:
        text_query = m.text or m.caption or "Analyze this"
        mime_type = None
        
        if m.content_type != 'text':
            if m.content_type == 'photo': file_id, mime_type = m.photo[-1].file_id, "image/jpeg"
            elif m.content_type == 'video': file_id, mime_type = m.video.file_id, "video/mp4"
            elif m.content_type == 'video_note': file_id, mime_type = m.video_note.file_id, "video/mp4"
            else: file_id, mime_type = m.document.file_id, m.document.mime_type
            
            file_info = bot.get_file(file_id)
            path = f"temp_{int(time.time())}"
            with open(path, "wb") as f: f.write(bot.download_file(file_info.file_path))
        
        bot.edit_message_text("📝", m.chat.id, status_msg.message_id)
        
        # Настройка Gemini
        genai.configure(api_key=get_key())
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        if path:
            uploaded_file = genai.upload_file(path, mime_type=mime_type)
            while uploaded_file.state.name == "PROCESSING":
                time.sleep(1)
                uploaded_file = genai.get_file(uploaded_file.name)
            response = model.generate_content([text_query, uploaded_file]).text
        else:
            response = model.generate_content(text_query).text

        bot.delete_message(m.chat.id, status_msg.message_id)
        bot.reply_to(m, response, parse_mode="Markdown")
        
    except Exception as e:
        print(f"Error: {e}")
        bot.edit_message_text("❌ Error", m.chat.id, status_msg.message_id)
    finally:
        if path and os.path.exists(path): os.remove(path)

def run_flask():
    server.run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
    Thread(target=run_flask).start()
    bot.infinity_polling()
