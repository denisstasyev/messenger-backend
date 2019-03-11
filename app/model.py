from app import db


def list_messages_by_chat(chat_id: int=0, limit: int=0):
    return db.query_all("""
        SELECT user_id, name, nick, message_id, content, added_at
        FROM messanger.messages
        JOIN users USING (user_id)
        WHERE chat_id = %(chat_id)s
        ORDER BY added_at DESC
        LIMIT %(limit)s
    """, chat_id=int(chat_id), limit=int(limit))


def search_user(text: str="", limit: int=0):
    return db.query_all("""
        SELECT name, nick, avatar
        FROM messanger.users
        WHERE name = %(text)s OR nick = %(text)s
        LIMIT %(limit)s
    """, text=str(text), limit=int(limit))


def create_chat(is_group_chat: bool=False, topic: str=""):
    return db.insert_one("""
        INSERT INTO messanger.chats (is_group_chat, topic)
        VALUES (%(is_group_chat)s, %(topic)s);
    """, is_group_chat=bool(is_group_chat), topic=str(topic))


def list_of_chats(limit: int=0):
    return db.query_all("""
        SELECT *
        FROM messanger.chats
        LIMIT %(limit)s
    """, limit=int(limit))
