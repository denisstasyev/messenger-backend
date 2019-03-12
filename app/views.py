from flask import request, abort, jsonify, render_template
from app import app


@app.route("/<string:name>/")  # вызов, если в браузере путь .../name/
# @app.route('/')
def index(name="world"):
    return "Hello, {}!".format(name)


@app.route("/form/", methods=["GET", "POST"])
def form():
    if request.method == "GET":
        return render_template("form.html")
        # return '''<html><head></head><body>
        # <form method="POST" action="/form/">
        #     <input name="first_name" >
        #     <input name="last_name" >
        #     <input type="submit" >
        # </form>
        # </body></html>'''
    else:
        rv = jsonify(request.form)
        return rv
        # print(request.form)  # request.form - словарь
        # abort(404)


##########


@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return jsonify(request.form)
    else:
        return render_template("auth/login.html")


@app.route("/register/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        return jsonify(request.form)
    else:
        return render_template("auth/register.html")


##########


@app.route("/search_users/", methods=["GET"])
def search_users(query=None, limit=None):
    """Поиск пользователей"""
    return jsonify(users=["User1", "User2"])


@app.route("/search_chats/", methods=["GET"])
def search_chats(query=None, limit=None):
    """Поиск среди чатов пользователя"""
    return jsonify(chats=["Chat1", "Chat2"])


@app.route("/list_chats/", methods=["GET"])
def list_chats():
    """Получение списка чатов пользователя"""
    return jsonify(chats=["Chat1", "Chat2"])


@app.route("/create_pers_chat/", methods=["GET", "POST"])
def create_pers_chat(user_id=None):
    """Создание персонального чата"""
    if request.method == "POST":
        return jsonify(chat="Chat")
        # return jsonify(request.form)
    return render_template("chats/create_pers_chat.html")


@app.route("/create_group_chat/", methods=["GET", "POST"])
def create_group_chat(topic=None):
    """Создание группового чата"""
    if request.method == "POST":
        return jsonify(chat="Chat")
        # return jsonify(request.form)
    return render_template("chats/create_group_chat.html")


@app.route("/add_members_to_group_chat/", methods=["POST"])
def add_members_to_group_chat(chat_id=None, user_ids=None):
    """Добавление участников в групповой чат"""
    return jsonify()


@app.route("/leave_group_chat/", methods=["POST"])
def leave_group_chat(chat_id=None):
    """Выход из групового чата"""
    return jsonify()


@app.route("/send_message/", methods=["POST"])
def send_message(chat_id=None, content=None, attach_id=None):
    """Отправка сообщения в чат"""
    return jsonify(message="Message")


@app.route("/read_message/", methods=["GET"])
def read_message(message_id=None):
    """Прочтение сообщения"""
    return jsonify(chat="Chat")


@app.route("/upload_file/", methods=["POST"])
def upload_file(content=None, chat_id=None):
    """Загрузка файла"""
    return jsonify(attach="Attachment")


###########################################
from flask import jsonify
from app import app, db

from .models import User, Member, Chat, Message


@app.route("/api/create_user/<string:username>", methods=["POST"])
def create_user(username):
    """Add User"""
    if not request.form.get("first_name", type=str):
        raise RuntimeError("Missing first_name")

    if not request.form.get("last_name", type=str):
        raise RuntimeError("Missing last_name")

    first_name = request.form.get("first_name", type=str)
    last_name = request.form.get("last_name", type=str)
    email = request.form.get("email", default=None, type=str)

    user = User(username, first_name, last_name, email)
    db.session.add(user)
    db.session.commit()
    return user.__repr__()

