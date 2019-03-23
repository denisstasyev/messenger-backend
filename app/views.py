from flask import jsonify, request, abort, make_response, url_for, session
from flask import render_template
import wtforms_json
from flask_login import current_user, login_user, logout_user, login_required

from app import app, db

from .tasks import send_email
from .models import User, Member, Chat, Message, Attachment, model_as_dict, load_user
from .forms import (
    UserForm,
    MemberForm,
    ChatForm,
    MessageForm,
    AttachmentForm,
    LoginForm,
    RegistrationForm,
)


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
        elif field == "password":
            pass
        else:
            new_user[field] = user[field]
    return new_user


# curl -X GET http://std-messenger.com/api/users/ --cookie "remember_token=...; session=..."
@app.route("/api/users/", methods=["GET"])
@login_required
def get_users():
    """Get Users"""
    users = User.query.all()
    users = [model_as_dict(user) for user in users]
    return jsonify({"users": list(map(make_public_uri_user, users))}), 200


# curl -X GET http://std-messenger.com/api/users/denis/ --cookie "remember_token=...; session=..."
@app.route("/api/users/<string:username>/", methods=["GET"])
@login_required
def get_user(username):
    """Get User"""
    user = User.query.filter(User.username == username).first_or_404()
    return jsonify({"user": make_public_uri_user(model_as_dict(user))}), 200


# TODO: DELETE create_user function or not allow User to create another User


# curl -i -H "Content-Type: application/json" -X POST -d '{"username": "ddenis",
#  "first_name": "DDenis", "last_name": "Stasyev"}' http://std-messenger.com/api/users/
#  --cookie "remember_token=...; session=..."
@app.route("/api/users/", methods=["POST"])
@login_required
def create_user():
    """Create User"""
    if not request.json:
        abort(400)

    form = UserForm.from_json(request.json)

    if not form.validate():
        print(form.errors)
        abort(400)

    user = User()
    form.populate_obj(user)

    db.session.add(user)
    db.session.commit()
    return jsonify({"user": make_public_uri_user(model_as_dict(user))}), 201


# curl -i -H "Content-Type: application/json" -X PUT -d '{"username": "denis",
#  "first_name": "Denis", "last_name": "Stasyev"}' http://std-messenger.com/api/users/ddenis/
#  --cookie "remember_token=...; session=..."
@app.route("/api/users/<string:username>/", methods=["PUT"])
@login_required
def update_user(username):
    """Update User"""
    if not request.json:
        abort(400)

    form = UserForm.from_json(request.json)

    if not form.validate():
        print(form.errors)
        abort(400)

    user = User.query.filter(User.username == username).first_or_404()

    # if not current_user.user_id == user.user_id:
    #     abort(400)

    form.populate_obj(user)

    db.session.query(User).filter(User.user_id == user.user_id).update(
        model_as_dict(user)
    )
    db.session.commit()
    return jsonify({"user": make_public_uri_user(model_as_dict(user))}), 202


# curl -X DELETE  http://std-messenger.com/api/users/denis/
#  --cookie "remember_token=...; session=..."
@app.route("/api/users/<string:username>/", methods=["DELETE"])
@login_required
def delete_user(username):
    """Delete User"""
    user = User.query.filter(User.username == username).first()
    if user is None:
        abort(404)

    # if not current_user.user_id == user.user_id:
    #     abort(400)

    # logout()
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
@login_required
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
@login_required
def create_member():
    """Create Member"""
    if not request.json:
        abort(400)

    form = MemberForm.from_json(request.json)

    if not form.validate():
        print(form.errors)
        abort(400)

    member = Member()
    form.populate_obj(member)

    db.session.add(member)
    db.session.commit()
    return jsonify({"member": make_public_uri_member(model_as_dict(member))}), 201


@app.route("/api/members/<int:member_id>/", methods=["PUT"])
@login_required
def update_member(member_id):
    """Update Member"""
    if not request.json:
        abort(400)

    member = Member.query.filter(Member.member_id == member_id).first_or_404()
    form = MemberForm.from_json(request.json)

    if not form.validate():
        print(form.errors)
        abort(400)

    form.populate_obj(member)

    db.session.query(Member).filter(Member.member_id == member.member_id).update(
        model_as_dict(member)
    )
    db.session.commit()
    return jsonify({"member": make_public_uri_member(model_as_dict(member))}), 202


@app.route("/api/members/<int:member_id>/", methods=["DELETE"])
@login_required
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
@login_required
def get_chats():
    """Get Chats"""
    chats = Chat.query.all()
    chats = [model_as_dict(chat) for chat in chats]
    return jsonify({"chats": list(map(make_public_uri_chat, chats))}), 200


@app.route("/api/chats/<string:chatname>/", methods=["GET"])
@login_required
def get_chat(chatname):
    """Get Chat"""
    chat = Chat.query.filter(Chat.chatname == chatname).first_or_404()
    return jsonify({"chat": make_public_uri_chat(model_as_dict(chat))}), 200


@app.route("/api/chats/", methods=["POST"])
@login_required
def create_chat():
    """Create Chat"""
    if not request.json:
        abort(400)

    form = ChatForm.from_json(request.json)

    if not form.validate():
        print(form.errors)
        abort(400)

    chat = Chat()
    form.populate_obj(chat)

    db.session.add(chat)
    db.session.commit()
    return jsonify({"chat": make_public_uri_chat(model_as_dict(chat))}), 201


@app.route("/api/chats/<string:chatname>/", methods=["PUT"])
@login_required
def update_chat(chatname):
    """Update Chat"""
    if not request.json:
        abort(400)

    chat = Chat.query.filter(Chat.chatname == chatname).first_or_404()
    form = ChatForm.from_json(request.json)

    if not form.validate():
        print(form.errors)
        abort(400)

    form.populate_obj(chat)

    db.session.query(Chat).filter(Chat.chat_id == chat.chat_id).update(
        model_as_dict(chat)
    )
    db.session.commit()
    return jsonify({"chat": make_public_uri_chat(model_as_dict(chat))}), 202


@app.route("/api/chats/<string:chatname>/", methods=["DELETE"])
@login_required
def delete_chat(chatname):
    """Delete Chat"""
    chat = Chat.query.filter(Chat.chatname == chatname).first()
    if chat is None:
        abort(404)
    db.session.delete(chat)
    db.session.commit()
    return jsonify({"result": True}), 200


# REST API for Message


def make_public_uri_message(message):
    """Create URI for Message"""
    new_message = {}
    for field in message:
        if field == "message_id":
            new_message["uri"] = url_for(
                "get_message", message_id=message["message_id"], _external=True
            )
        else:
            new_message[field] = message[field]
    return new_message


@app.route("/api/messages/", methods=["GET"])
@login_required
def get_messages():
    """Get Messages"""
    messages = Message.query.all()
    messages = [model_as_dict(message) for message in messages]
    return jsonify({"messages": list(map(make_public_uri_message, messages))}), 200


@app.route("/api/messages/<int:message_id>/", methods=["GET"])
@login_required
def get_message(message_id):
    """Get Message"""
    message = Message.query.filter(Message.message_id == message_id).first_or_404()
    return jsonify({"message": make_public_uri_message(model_as_dict(message))}), 200


@app.route("/api/messages/", methods=["POST"])
@login_required
def create_message():
    """Create Message"""
    if not request.json:
        abort(400)

    form = MessageForm.from_json(request.json)

    if not form.validate():
        print(form.errors)
        abort(400)

    message = Message()
    form.populate_obj(message)

    db.session.add(message)
    db.session.commit()
    return jsonify({"message": make_public_uri_message(model_as_dict(message))}), 201


@app.route("/api/messages/<int:message_id>/", methods=["PUT"])
@login_required
def update_message(message_id):
    """Update Message"""
    if not request.json:
        abort(400)

    message = Message.query.filter(Message.message_id == message_id).first_or_404()
    form = MessageForm.from_json(request.json)

    if not form.validate():
        print(form.errors)
        abort(400)

    form.populate_obj(message)

    db.session.query(Message).filter(Message.message_id == message.message_id).update(
        model_as_dict(message)
    )
    db.session.commit()
    return jsonify({"message": make_public_uri_message(model_as_dict(message))}), 202


@app.route("/api/messages/<int:message_id>/", methods=["DELETE"])
@login_required
def delete_message(message_id):
    """Delete Message"""
    message = Message.query.filter(Message.message_id == message_id).first()
    if message is None:
        abort(404)
    db.session.delete(message)
    db.session.commit()
    return jsonify({"result": True}), 200


# REST API for Attachment


def make_public_uri_attachment(attachment):
    """Create URI for Attachment"""
    new_attachment = {}
    for field in attachment:
        if field == "attachment_id":
            new_attachment["uri"] = url_for(
                "get_attachment",
                attachment_id=attachment["attachment_id"],
                _external=True,
            )
        else:
            new_attachment[field] = attachment[field]
    return new_attachment


@app.route("/api/attachments/", methods=["GET"])
@login_required
def get_attachments():
    """Get Attachments"""
    attachments = Attachment.query.all()
    attachments = [model_as_dict(attachment) for attachment in attachments]
    return (
        jsonify({"attachments": list(map(make_public_uri_attachment, attachments))}),
        200,
    )


@app.route("/api/attachments/<int:attachment_id>/", methods=["GET"])
@login_required
def get_attachment(attachment_id):
    """Get Attachment"""
    attachment = Attachment.query.filter(
        Attachment.attachment_id == attachment_id
    ).first_or_404()
    return (
        jsonify({"attachment": make_public_uri_attachment(model_as_dict(attachment))}),
        200,
    )


@app.route("/api/attachments/", methods=["POST"])
@login_required
def create_attachment():
    """Create Attachment"""
    if not request.json:
        abort(400)

    form = AttachmentForm.from_json(request.json)

    if not form.validate():
        print(form.errors)
        abort(400)

    attachment = Attachment()
    form.populate_obj(attachment)

    db.session.add(attachment)
    db.session.commit()
    return (
        jsonify({"attachment": make_public_uri_attachment(model_as_dict(attachment))}),
        201,
    )


@app.route("/api/attachments/<int:attachment_id>/", methods=["PUT"])
@login_required
def update_attachment(attachment_id):
    """Update Attachment"""
    if not request.json:
        abort(400)

    attachment = Attachment.query.filter(
        Attachment.attachment_id == attachment_id
    ).first_or_404()
    form = AttachmentForm.from_json(request.json)

    if not form.validate():
        print(form.errors)
        abort(400)

    form.populate_obj(attachment)

    db.session.query(Attachment).filter(
        Attachment.attachment_id == attachment.attachment_id
    ).update(model_as_dict(attachment))
    db.session.commit()
    return (
        jsonify({"attachment": make_public_uri_attachment(model_as_dict(attachment))}),
        202,
    )


@app.route("/api/attachments/<int:attachment_id>/", methods=["DELETE"])
@login_required
def delete_attachment(attachment_id):
    """Delete Attachment"""
    attachment = Attachment.query.filter(
        Attachment.attachment_id == attachment_id
    ).first()
    if attachment is None:
        abort(404)
    db.session.delete(attachment)
    db.session.commit()
    return jsonify({"result": True}), 200


# Authorization API's functions


@app.route("/api/login/", methods=["GET"])
def login():
    """Login User"""
    if not request.json:
        abort(400)
    if current_user.is_authenticated:
        return jsonify({"result": True}), 200

    form = LoginForm.from_json(request.json)

    if not form.validate():
        print(form.errors)
        abort(400)

    user = User.query.filter(User.username == form.username.data).first_or_404()
    if user is None or not (user.password == form.password.data):
        return jsonify({"result": False}), 401

    if not login_user(user, remember=form.remember_me.data):
        return jsonify({"result": False}), 401
    return jsonify({"result": True}), 202


# TODO: clean cookies after logout
@app.route("/api/logout/", methods=["GET"])
@login_required
def logout():
    """Logout User"""
    logout_user()
    # session.clear()
    # resp.delete_cookie('username', path='/', domain='yourdomain.com')
    return jsonify({"result": True}), 200


@app.route("/api/register/", methods=["POST"])
def register():
    """Register User"""
    if not request.json:
        abort(400)
    if current_user.is_authenticated:
        return jsonify({"result": True}), 200

    form = RegistrationForm.from_json(request.json)

    if not form.validate():
        print(form.errors)
        abort(400)

    user = User()
    form.populate_obj(user)

    db.session.add(user)
    db.session.commit()

    send_email.apply_async(
        (
            "Registration",
            [user.email],
            "Successful registration in the STD-messenger!",
            render_template(
                "email_registration.html", user=user, password=form.password.data
            ),
        )
    )
    return jsonify({"user": make_public_uri_user(model_as_dict(user))}), 201


# Some other API's functions


#################

# @app.route("/search_users/", methods=["GET"])
# def search_users(query=None, limit=None):
#     """Поиск пользователей"""
#     return jsonify(users=["User1", "User2"])


# @app.route("/search_chats/", methods=["GET"])
# def search_chats(query=None, limit=None):
#     """Поиск среди чатов пользователя"""
#     return jsonify(chats=["Chat1", "Chat2"])


# @app.route("/list_chats/", methods=["GET"])
# def list_chats():
#     """Получение списка чатов пользователя"""
#     return jsonify(chats=["Chat1", "Chat2"])


# @app.route("/create_pers_chat/", methods=["GET", "POST"])
# def create_pers_chat(user_id=None):
#     """Создание персонального чата"""
#     if request.method == "POST":
#         return jsonify(chat="Chat")
#         # return jsonify(request.form)
#     return render_template("chats/create_pers_chat.html")


# @app.route("/create_group_chat/", methods=["GET", "POST"])
# def create_group_chat(topic=None):
#     """Создание группового чата"""
#     if request.method == "POST":
#         return jsonify(chat="Chat")
#         # return jsonify(request.form)
#     return render_template("chats/create_group_chat.html")


# @app.route("/add_members_to_group_chat/", methods=["POST"])
# def add_members_to_group_chat(chat_id=None, user_ids=None):
#     """Добавление участников в групповой чат"""
#     return jsonify()


# @app.route("/leave_group_chat/", methods=["POST"])
# def leave_group_chat(chat_id=None):
#     """Выход из групового чата"""
#     return jsonify()


# @app.route("/send_message/", methods=["POST"])
# def send_message(chat_id=None, content=None, attach_id=None):
#     """Отправка сообщения в чат"""
#     return jsonify(message="Message")


# @app.route("/read_message/", methods=["GET"])
# def read_message(message_id=None):
#     """Прочтение сообщения"""
#     return jsonify(chat="Chat")


# @app.route("/upload_file/", methods=["POST"])
# def upload_file(content=None, chat_id=None):
#     """Загрузка файла"""
#     return jsonify(attach="Attachment")
