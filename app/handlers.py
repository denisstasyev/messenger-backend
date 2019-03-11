from flask import request, jsonify
from app import model
from app import app


@app.route('/messages/', methods=['GET'])
def messages():
    chat_id = str(request.args.get('chat_id'))
    messages = model.list_messages_by_chat(chat_id)
    return jsonify(messages)


@app.route('/create_chat/', methods=['POST', 'GET'])
def create_chat():
    topic = str(request.args.get('topic'))
    is_group_chat = bool(request.args.get('is_group_chat'))
    model.create_chat(topic, is_group_chat)
    return jsonify({
        'topic': topic,
        'is_group_chat': is_group_chat
    })


@app.route('/search_users/', methods=['GET'])
def search_user():
    if request.method == 'GET':
        word = request.args.get('word')
        users = model.search_user(word)
        return jsonify(users)
