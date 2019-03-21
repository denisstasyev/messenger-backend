from app import app


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

### Creation API methods


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

from flask import jsonify, request, abort, make_response, url_for
import wtforms_json

from app import app, db

from .models import User, Member, Chat, Message, Attachment, model_as_dict
from .forms import UserForm, MemberForm, ChatForm, MessageForm, AttachmentForm


wtforms_json.init()


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({"error": "Bad request"}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)


# REST API for User


def make_public_uri_user(user):
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
    return jsonify({"users": list(map(make_public_uri_user, users))}), 200


@app.route("/api/users/<string:username>/", methods=["GET"])
def get_user(username):
    """Get User"""
    user = User.query.filter(User.username == username).first_or_404()
    return jsonify({"user": make_public_uri_user(model_as_dict(user))}), 200


# curl -i -H "Content-Type: application/json" -X POST -d '{"username": "cool1", "first_name": "Mike", "last_name": "Linerg"}' http://std-messenger.com/api/users/
@app.route("/api/users/", methods=["POST"])
def create_user():
    """Create User"""
    if not request.json:
        abort(400)

    form = UserForm.from_json(request.json)

    if not form.validate():
        abort(400)

    user = User()
    form.populate_obj(user)

    db.session.add(user)
    db.session.commit()
    return jsonify({"user": make_public_uri_user(model_as_dict(user))}), 201


# curl -i -H "Content-Type: application/json" -X PUT -d '{"username": "cool", "first_name": "Mike", "last_name": "Linerg"}' http://std-messenger.com/api/users/cool/
@app.route("/api/users/<string:username>/", methods=["PUT"])
def update_user(username):
    """Update User"""
    if not request.json:
        abort(400)

    user = User.query.filter(User.username == username).first_or_404()
    form = UserForm.from_json(request.json)

    if not form.validate():
        abort(400)

    form.populate_obj(user)

    db.session.query(User).filter(User.user_id == user.user_id).update(
        model_as_dict(user)
    )
    db.session.commit()
    return jsonify({"user": make_public_uri_user(model_as_dict(user))}), 202


# curl -X DELETE  http://std-messenger.com/api/users/test/
@app.route("/api/users/<string:username>/", methods=["DELETE"])
def delete_user(username):
    """Delete User"""
    user = User.query.filter(User.username == username).first()
    if user is None:
        abort(404)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"result": True}), 200


# REST API for Member


def make_public_uri_member(member):
    """Create URI for Member"""
    new_member = {}
    for field in member:
        if field == "member_id":
            new_member["uri"] = url_for(
                "get_member", member_id=member["member_id"], _external=True
            )
        else:
            new_member[field] = member[field]
    return new_member


@app.route("/api/members/", methods=["GET"])
def get_members():
    """Get Members"""
    members = Member.query.all()
    members = [model_as_dict(member) for member in members]
    return jsonify({"members": list(map(make_public_uri_member, members))}), 200


@app.route("/api/members/<int:member_id>/", methods=["GET"])
def get_member(member_id):
    """Get Member"""
    member = Member.query.filter(Member.member_id == member_id).first_or_404()
    return jsonify({"member": make_public_uri_member(model_as_dict(member))}), 200


@app.route("/api/members/", methods=["POST"])
def create_member():
    """Create Members"""
    if not request.json:
        abort(400)

    form = MemberForm.from_json(request.json)

    if not form.validate():
        abort(400)

    member = Member()
    form.populate_obj(member)

    db.session.add(member)
    db.session.commit()
    return jsonify({"member": make_public_uri_member(model_as_dict(member))}), 201


@app.route("/api/members/<int:member_id>/", methods=["PUT"])
def update_member(member_id):
    """Update Member"""
    if not request.json:
        abort(400)

    member = Member.query.filter(Member.member_id == member_id).first_or_404()
    form = MemberForm.from_json(request.json)

    if not form.validate():
        abort(400)

    form.populate_obj(member)

    db.session.query(Member).filter(Member.member_id == member.member_id).update(
        model_as_dict(member)
    )
    db.session.commit()
    return jsonify({"member": make_public_uri_member(model_as_dict(member))}), 202


@app.route("/api/members/<int:member_id>/", methods=["DELETE"])
def delete_member(member_id):
    """Delete Member"""
    member = Member.query.filter(Member.member_id == member_id).first()
    if member is None:
        abort(404)
    db.session.delete(member)
    db.session.commit()
    return jsonify({"result": True}), 200


# REST API for Chat


def make_public_uri_chat(chat):
    """Create URI for Chat"""
    new_chat = {}
    for field in chat:
        if field == "chat_id":
            new_chat["uri"] = url_for(
                "get_chat", chat_id=chat["chat_id"], _external=True
            )
        else:
            new_chat[field] = chat[field]
    return new_chat


@app.route("/api/chats/", methods=["GET"])
def get_chats():
    """Get Chats"""
    chats = Chat.query.all()
    chats = [model_as_dict(chat) for chat in chats]
    return jsonify({"chats": list(map(make_public_uri_chat, chats))}), 200


@app.route("/api/chats/<string:chatname>/", methods=["GET"])
def get_chat(chatname):
    """Get Chat"""
    chat = Chat.query.filter(Chat.chatname == chatname).first_or_404()
    return jsonify({"chat": make_public_uri_chat(model_as_dict(chat))}), 200


@app.route("/api/chats/", methods=["POST"])
def create_chat():
    """Create Chat"""
    if not request.json:
        abort(400)

    form = ChatForm.from_json(request.json)

    if not form.validate():
        abort(400)

    chat = Chat()
    form.populate_obj(chat)

    db.session.add(chat)
    db.session.commit()
    return jsonify({"chat": make_public_uri_chat(model_as_dict(chat))}), 201


@app.route("/api/chats/<string:chatname>/", methods=["PUT"])
def update_chat(chatname):
    """Update Chat"""
    if not request.json:
        abort(400)

    chat = Chat.query.filter(Chat.chatname == chatname).first_or_404()
    form = ChatForm.from_json(request.json)

    if not form.validate():
        abort(400)

    form.populate_obj(chat)

    db.session.query(Chat).filter(Chat.chat_id == chat.chat_id).update(
        model_as_dict(chat)
    )
    db.session.commit()
    return jsonify({"chat": make_public_uri_chat(model_as_dict(chat))}), 202


@app.route("/api/chats/<string:chatname>/", methods=["DELETE"])
def delete_chat(chatname):
    """Delete Chat"""
    chat = Chat.query.filter(Chat.chatname == chatname).first()
    if chat is None:
        abort(404)
    db.session.delete(chat)
    db.session.commit()
    return jsonify({"result": True}), 200


# REST API for Message
