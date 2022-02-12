from flask import Flask, request, render_template
from datetime import datetime
import json

app = Flask(__name__)  # создание веб сервера

db_file = "./data/db.json"  # Путь к файлу
json_db = open(db_file, "rb")  # Открываем файл
data = json.load(json_db)  # Загружаем данные из файла
messages_list = data["messages_list"]  # Берем сообщения из структуры и кладем в переменную


# Функция сохранения сообщений в файл
def save_messages():
    data = {
        "messages_list": messages_list,
    }
    json_db = open(db_file, "w")
    json.dump(data, json_db)


# Открываем файл на запись
json_db = open(db_file, "w")
json.dump(data, json_db)  # Записываем данные в файл

# Функция добавления нового сообщения
def add_message(name, txt):
    message = {
        "text": txt,
        "sender": name,
        "date": datetime.now().strftime("%H:%M")
    }
    messages_list.append(message)

# Главная страница
@app.route("/")
def index_page():
    return "Hello world!"


# Раздел со списком сообщений
@app.route("/get_messages")
def get_messages():
    return {"messages": messages_list}


# # Раздел для отправки сообщения
@app.route("/send_message")
def send_message():
    name = request.args["name"]
    text = request.args["text"]
    if len(name) > 50 or len(name) < 3:
        return "Invalid name"
    add_message(name, text)
    save_messages()
    return "OK"


# Раздел с визуальным интерфейсом
@app.route("/form")
def form():
    return render_template("form.html")

app.run()  # host="0.0.0.0", port=80 запуск веб сервера
