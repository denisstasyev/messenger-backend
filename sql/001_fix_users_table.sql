DROP SCHEMA IF EXISTS messanger;
CREATE SCHEMA IF NOT EXISTS messanger AUTHORIZATION denis;
ALTER SCHEMA messanger OWNER TO messanger;

DROP TABLE IF EXISTS messanger.users;
CREATE TABLE IF NOT EXISTS messanger.users (
    user_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL CONSTRAINT user_name_check CHECK (length(name) < 64),
    nick TEXT NOT NULL CONSTRAINT user_nick_check CHECK (length(nick) < 32),
    avatar TEXT NOT NULL DEFAULT '' CONSTRAINT user_avatar_check CHECK (length(avatar) < 100)
);

DROP TABLE IF EXISTS messanger.chats;
CREATE TABLE IF NOT EXISTS messanger.chats (
    chat_id SERIAL PRIMARY KEY,
    is_group_chat BOOLEAN NOT NULL,
    topic TEXT NOT NULL DEFAULT '' CONSTRAINT chat_topic_check CHECK (length(topic) < 100),
    last_message TEXT CONSTRAINT chat_last_message_check CHECK (length(last_message) < 65536)
);

DROP TABLE IF EXISTS messanger.messages;
CREATE TABLE IF NOT EXISTS messanger.messages (
    message_id SERIAL PRIMARY KEY,
    chat_id INTEGER NOT NULL REFERENCES messanger.chats(chat_id),
    user_id INTEGER NOT NULL REFERENCES messanger.users(user_id),
    content TEXT NOT NULL CONSTRAINT message_content_check CHECK (length(content) < 65536),
    added_at TIMESTAMP NOT NULL DEFAULT NOW()
);

DROP TABLE IF EXISTS messanger.members;
CREATE TABLE IF NOT EXISTS messanger.members (
    member_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES messanger.users(user_id),
    chat_id INTEGER NOT NULL references messanger.chats(chat_id),
    new_messages INTEGER NOT NULL,
    last_read_message_id INTEGER NOT NULL REFERENCES messanger.messages(message_id)
);

DROP TABLE IF EXISTS messanger.attachments;
CREATE TABLE IF NOT EXISTS messanger.attachments (
    attach_id SERIAL PRIMARY KEY,
    chat_id INTEGER NOT NULL REFERENCES messanger.chats(chat_id),
    user_id INTEGER NOT NULL REFERENCES messanger.users(user_id),
    message_id INTEGER NOT NULL REFERENCES messanger.messages(message_id),
    type TEXT NOT NULL CONSTRAINT attachment_type_check CHECK (length(type) < 16),
    url TEXT NOT NULL CONSTRAINT attachment_url_check CHECK (length(url) < 64)
);
