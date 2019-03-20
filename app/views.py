from flask import request, abort, jsonify, render_template
from app import app


@app.route("/form/", methods=["GET", "POST"])
def fform():
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

from .models import User, Member, Chat, Message, Attachment


### Creation API methods


@app.route("/api/create_member", methods=["POST"])
def create_member():
    """Create Member of chat"""
    if not request.form.get("user_id", type=int):
        raise RuntimeError("Missing user_id")

    if not request.form.get("chat_id", type=int):
        raise RuntimeError("Missing chat_id")

    user_id = request.form.get("user_id", type=int)
    chat_id = request.form.get("chat_id", type=int)
    new_messages = request.form.get("new_messages", default=0, type=int)
    last_read_message_id = request.form.get(
        "last_read_message_id", default=None, type=int
    )

    member = Member(user_id, chat_id, new_messages, last_read_message_id)
    db.session.add(member)
    db.session.commit()
    return member.__repr__()


@app.route("/api/create_chat/<string:chatname>", methods=["POST"])
def create_chat(chatname):
    """Create Chat"""
    if not request.form.get("is_public", type=bool):
        raise RuntimeError("Missing is_public")

    is_public = request.form.get("is_public", type=bool)
    last_message = request.form.get("last_message", default=None, type=int)

    chat = Chat(chatname, is_public, last_message)
    db.session.add(chat)
    db.session.commit()
    return chat.__repr__()


@app.route("/api/create_message", methods=["POST"])
def create_message():
    """Create Message in chat"""
    if not request.form.get("chat_id", type=int):
        raise RuntimeError("Missing chat_id")

    if not request.form.get("user_id", type=int):
        raise RuntimeError("Missing user_id")

    chat_id = request.form.get("chat_id", type=int)
    user_id = request.form.get("user_id", type=int)
    text = request.form.get("text", default=None, type=str)

    message = Message(chat_id, user_id, text)
    db.session.add(message)
    db.session.commit()
    return message.__repr__()


@app.route("/api/create_attachment", methods=["POST"])
def create_attachment():
    """Create Attachment in message"""
    if not request.form.get("attachment_type", type=str):
        raise RuntimeError("Missing attachment_type")

    if not request.form.get("url", type=str):
        raise RuntimeError("Missing url")

    attachment_type = request.form.get("attachment_type", type=str)
    url = request.form.get("url", type=str)
    user_id = request.form.get("user_id", type=int)
    chat_id = request.form.get("chat_id", type=int)
    message_id = request.form.get("message_id", type=int)

    attachment = Attachment(attachment_type, url, user_id, chat_id, message_id)
    db.session.add(attachment)
    db.session.commit()
    return attachment.__repr__()


### Deletion API methods


# https://flask-russian-docs.readthedocs.io/ru/latest/quickstart.html#public-server


from flask import render_template
from app import app


@app.route("/")
@app.route("/home/")
@app.route("/<string:username>/")
def index(username="guest"):
    return render_template("home.html", title="Home", username=username)


###################3

from flask import jsonify, request, make_response, url_for
from app import app, db

from .models import User, Member, Chat, Message, Attachment, model_as_dict

from .forms import UserForm


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({"error": "Bad request"}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)


# API methods with User


def make_public_user(user):
    """Create URI for User"""
    new_user = {}
    for field in user:
        if field == "user_id":
            new_user["uri"] = url_for(
                "get_user", username=user["username"], _external=True
            )
        else:
            new_user[field] = user[field]
    return new_user


@app.route("/api/users/", methods=["GET"])
def get_users():
    """Get Users"""
    users = User.query.all()
    users = [model_as_dict(user) for user in users]
    return jsonify({"users": list(map(make_public_user, users))})


@app.route("/api/users/<string:username>/", methods=["GET"])
def get_user(username):
    """Get User"""
    user = User.query.filter(User.username == username).first_or_404()
    return jsonify({"user": make_public_user(model_as_dict(user))})


@app.route("/api/users/", methods=["POST"])
def create_user():
    """Create User"""
    if (
        not request.json
        or not "username" in request.json
        or not "first_name" in request.json
        or not "last_name" in request.json
    ):
        abort(400)

    username = request.json["username"]

    if User.query.filter(User.username == username).first() is not None:
        abort(400)

    first_name = request.json["first_name"]
    last_name = request.json["last_name"]

    if "email" in request.json:
        email = request.json["email"]
        user = User(username, first_name, last_name, email)
    else:
        user = User(username, first_name, last_name)

    db.session.add(user)
    db.session.commit()
    return jsonify({"user": make_public_user(model_as_dict(user))}), 201


# from wtforms.ext.sqlalchemy.orm import model_form

import wtforms_json

wtforms_json.init()


@app.route("/api/users/<string:username>/", methods=["PUT"])
def update_user(username):
    # if not request.form:
    #     abort(400)

    user = User.query.filter(User.username == username).first_or_404()

    # UserForm = model_form(User)
    form = UserForm.from_json(request.json)
    print(form.validate())

    # form = UserForm(request.form)
    print(request.form)
    print(form.data)
    print(request.form)
    print(form.data)

    print(form.validate())
    print(form.errors)
    # form.errors

    # form.populate_obj(user)

    # db.session.add(user)
    # db.session.commit()

    # user = User.query.filter(User.username == username).first()
    #############################
    # if "title" in request.json and type(request.json["title"]) != unicode:
    #     abort(400)
    # if (
    #     "description" in request.json
    #     and type(request.json["description"]) is not unicode
    # ):
    #     abort(400)
    # if "done" in request.json and type(request.json["done"]) is not bool:
    #     abort(400)
    # task[0]["title"] = request.json.get("title", task[0]["title"])
    # task[0]["description"] = request.json.get("description", task[0]["description"])
    # task[0]["done"] = request.json.get("done", task[0]["done"])
    return jsonify({"user": make_public_user(model_as_dict(user))})


##################


@app.route("/api/users/<string:username>", methods=["DELETE"])
def delete_user(username):
    user = User.query.filter(User.username == username).first()
    if user is None:
        abort(404)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"result": True})


# user = User()
# form = UserForm(request.form)
# form.populate_obj(user)
# print(request.json)

