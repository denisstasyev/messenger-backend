-- Get from console: pg_dump -s messanger

--
-- PostgreSQL database dump
--

-- Dumped from database version 10.5 (Ubuntu 10.5-0ubuntu0.18.04)
-- Dumped by pg_dump version 10.5 (Ubuntu 10.5-0ubuntu0.18.04)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: messanger; Type: SCHEMA; Schema: -; Owner: messanger
--

CREATE SCHEMA messanger;


ALTER SCHEMA messanger OWNER TO messanger;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: attachments; Type: TABLE; Schema: messanger; Owner: messanger
--

CREATE TABLE messanger.attachments (
    attach_id integer NOT NULL,
    chat_id integer NOT NULL,
    user_id integer NOT NULL,
    message_id integer NOT NULL,
    type text NOT NULL,
    url text NOT NULL,
    CONSTRAINT attachment_type_check CHECK ((length(type) < 16)),
    CONSTRAINT attachment_url_check CHECK ((length(url) < 64))
);


ALTER TABLE messanger.attachments OWNER TO messanger;

--
-- Name: attachments_attach_id_seq; Type: SEQUENCE; Schema: messanger; Owner: messanger
--

CREATE SEQUENCE messanger.attachments_attach_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE messanger.attachments_attach_id_seq OWNER TO messanger;

--
-- Name: attachments_attach_id_seq; Type: SEQUENCE OWNED BY; Schema: messanger; Owner: messanger
--

ALTER SEQUENCE messanger.attachments_attach_id_seq OWNED BY messanger.attachments.attach_id;


--
-- Name: chats; Type: TABLE; Schema: messanger; Owner: messanger
--

CREATE TABLE messanger.chats (
    chat_id integer NOT NULL,
    is_group_chat boolean NOT NULL,
    topic text DEFAULT ''::text NOT NULL,
    last_message text NOT NULL,
    CONSTRAINT chat_last_message_check CHECK ((length(last_message) < 65536)),
    CONSTRAINT chat_topic_check CHECK ((length(topic) < 100))
);


ALTER TABLE messanger.chats OWNER TO messanger;

--
-- Name: chats_chat_id_seq; Type: SEQUENCE; Schema: messanger; Owner: messanger
--

CREATE SEQUENCE messanger.chats_chat_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE messanger.chats_chat_id_seq OWNER TO messanger;

--
-- Name: chats_chat_id_seq; Type: SEQUENCE OWNED BY; Schema: messanger; Owner: messanger
--

ALTER SEQUENCE messanger.chats_chat_id_seq OWNED BY messanger.chats.chat_id;


--
-- Name: members; Type: TABLE; Schema: messanger; Owner: messanger
--

CREATE TABLE messanger.members (
    member_id integer NOT NULL,
    user_id integer NOT NULL,
    chat_id integer NOT NULL,
    new_messages integer NOT NULL,
    last_read_message_id integer NOT NULL
);


ALTER TABLE messanger.members OWNER TO messanger;

--
-- Name: members_member_id_seq; Type: SEQUENCE; Schema: messanger; Owner: messanger
--

CREATE SEQUENCE messanger.members_member_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE messanger.members_member_id_seq OWNER TO messanger;

--
-- Name: members_member_id_seq; Type: SEQUENCE OWNED BY; Schema: messanger; Owner: messanger
--

ALTER SEQUENCE messanger.members_member_id_seq OWNED BY messanger.members.member_id;


--
-- Name: messages; Type: TABLE; Schema: messanger; Owner: messanger
--

CREATE TABLE messanger.messages (
    message_id integer NOT NULL,
    chat_id integer NOT NULL,
    user_id integer NOT NULL,
    content text NOT NULL,
    added_at timestamp without time zone DEFAULT now() NOT NULL,
    CONSTRAINT message_content_check CHECK ((length(content) < 65536))
);


ALTER TABLE messanger.messages OWNER TO messanger;

--
-- Name: messages_message_id_seq; Type: SEQUENCE; Schema: messanger; Owner: messanger
--

CREATE SEQUENCE messanger.messages_message_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE messanger.messages_message_id_seq OWNER TO messanger;

--
-- Name: messages_message_id_seq; Type: SEQUENCE OWNED BY; Schema: messanger; Owner: messanger
--

ALTER SEQUENCE messanger.messages_message_id_seq OWNED BY messanger.messages.message_id;


--
-- Name: users; Type: TABLE; Schema: messanger; Owner: messanger
--

CREATE TABLE messanger.users (
    user_id integer NOT NULL,
    name text NOT NULL,
    nick text NOT NULL,
    avatar text DEFAULT ''::text NOT NULL,
    CONSTRAINT user_avatar_check CHECK ((length(avatar) < 100)),
    CONSTRAINT user_name_check CHECK ((length(name) < 64)),
    CONSTRAINT user_nick_check CHECK ((length(nick) < 32))
);


ALTER TABLE messanger.users OWNER TO messanger;

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: messanger; Owner: messanger
--

CREATE SEQUENCE messanger.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE messanger.users_user_id_seq OWNER TO messanger;

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: messanger; Owner: messanger
--

ALTER SEQUENCE messanger.users_user_id_seq OWNED BY messanger.users.user_id;


--
-- Name: attachments attach_id; Type: DEFAULT; Schema: messanger; Owner: messanger
--

ALTER TABLE ONLY messanger.attachments ALTER COLUMN attach_id SET DEFAULT nextval('messanger.attachments_attach_id_seq'::regclass);


--
-- Name: chats chat_id; Type: DEFAULT; Schema: messanger; Owner: messanger
--

ALTER TABLE ONLY messanger.chats ALTER COLUMN chat_id SET DEFAULT nextval('messanger.chats_chat_id_seq'::regclass);


--
-- Name: members member_id; Type: DEFAULT; Schema: messanger; Owner: messanger
--

ALTER TABLE ONLY messanger.members ALTER COLUMN member_id SET DEFAULT nextval('messanger.members_member_id_seq'::regclass);


--
-- Name: messages message_id; Type: DEFAULT; Schema: messanger; Owner: messanger
--

ALTER TABLE ONLY messanger.messages ALTER COLUMN message_id SET DEFAULT nextval('messanger.messages_message_id_seq'::regclass);


--
-- Name: users user_id; Type: DEFAULT; Schema: messanger; Owner: messanger
--

ALTER TABLE ONLY messanger.users ALTER COLUMN user_id SET DEFAULT nextval('messanger.users_user_id_seq'::regclass);


--
-- Name: attachments attachments_pkey; Type: CONSTRAINT; Schema: messanger; Owner: messanger
--

ALTER TABLE ONLY messanger.attachments
    ADD CONSTRAINT attachments_pkey PRIMARY KEY (attach_id);


--
-- Name: chats chats_pkey; Type: CONSTRAINT; Schema: messanger; Owner: messanger
--

ALTER TABLE ONLY messanger.chats
    ADD CONSTRAINT chats_pkey PRIMARY KEY (chat_id);


--
-- Name: members members_pkey; Type: CONSTRAINT; Schema: messanger; Owner: messanger
--

ALTER TABLE ONLY messanger.members
    ADD CONSTRAINT members_pkey PRIMARY KEY (member_id);


--
-- Name: messages messages_pkey; Type: CONSTRAINT; Schema: messanger; Owner: messanger
--

ALTER TABLE ONLY messanger.messages
    ADD CONSTRAINT messages_pkey PRIMARY KEY (message_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: messanger; Owner: messanger
--

ALTER TABLE ONLY messanger.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: attachments attachments_chat_id_fkey; Type: FK CONSTRAINT; Schema: messanger; Owner: messanger
--

ALTER TABLE ONLY messanger.attachments
    ADD CONSTRAINT attachments_chat_id_fkey FOREIGN KEY (chat_id) REFERENCES messanger.chats(chat_id);


--
-- Name: attachments attachments_message_id_fkey; Type: FK CONSTRAINT; Schema: messanger; Owner: messanger
--

ALTER TABLE ONLY messanger.attachments
    ADD CONSTRAINT attachments_message_id_fkey FOREIGN KEY (message_id) REFERENCES messanger.messages(message_id);


--
-- Name: attachments attachments_user_id_fkey; Type: FK CONSTRAINT; Schema: messanger; Owner: messanger
--

ALTER TABLE ONLY messanger.attachments
    ADD CONSTRAINT attachments_user_id_fkey FOREIGN KEY (user_id) REFERENCES messanger.users(user_id);


--
-- Name: members members_chat_id_fkey; Type: FK CONSTRAINT; Schema: messanger; Owner: messanger
--

ALTER TABLE ONLY messanger.members
    ADD CONSTRAINT members_chat_id_fkey FOREIGN KEY (chat_id) REFERENCES messanger.chats(chat_id);


--
-- Name: members members_last_read_message_id_fkey; Type: FK CONSTRAINT; Schema: messanger; Owner: messanger
--

ALTER TABLE ONLY messanger.members
    ADD CONSTRAINT members_last_read_message_id_fkey FOREIGN KEY (last_read_message_id) REFERENCES messanger.messages(message_id);


--
-- Name: members members_user_id_fkey; Type: FK CONSTRAINT; Schema: messanger; Owner: messanger
--

ALTER TABLE ONLY messanger.members
    ADD CONSTRAINT members_user_id_fkey FOREIGN KEY (user_id) REFERENCES messanger.users(user_id);


--
-- Name: messages messages_chat_id_fkey; Type: FK CONSTRAINT; Schema: messanger; Owner: messanger
--

ALTER TABLE ONLY messanger.messages
    ADD CONSTRAINT messages_chat_id_fkey FOREIGN KEY (chat_id) REFERENCES messanger.chats(chat_id);


--
-- Name: messages messages_user_id_fkey; Type: FK CONSTRAINT; Schema: messanger; Owner: messanger
--

ALTER TABLE ONLY messanger.messages
    ADD CONSTRAINT messages_user_id_fkey FOREIGN KEY (user_id) REFERENCES messanger.users(user_id);


--
-- Name: SCHEMA messanger; Type: ACL; Schema: -; Owner: messanger
--

GRANT USAGE ON SCHEMA messanger TO denis;


--
-- Name: TABLE attachments; Type: ACL; Schema: messanger; Owner: messanger
--

GRANT ALL ON TABLE messanger.attachments TO denis;


--
-- Name: SEQUENCE attachments_attach_id_seq; Type: ACL; Schema: messanger; Owner: messanger
--

GRANT ALL ON SEQUENCE messanger.attachments_attach_id_seq TO denis;


--
-- Name: TABLE chats; Type: ACL; Schema: messanger; Owner: messanger
--

GRANT ALL ON TABLE messanger.chats TO denis;


--
-- Name: SEQUENCE chats_chat_id_seq; Type: ACL; Schema: messanger; Owner: messanger
--

GRANT ALL ON SEQUENCE messanger.chats_chat_id_seq TO denis;


--
-- Name: TABLE members; Type: ACL; Schema: messanger; Owner: messanger
--

GRANT ALL ON TABLE messanger.members TO denis;


--
-- Name: SEQUENCE members_member_id_seq; Type: ACL; Schema: messanger; Owner: messanger
--

GRANT ALL ON SEQUENCE messanger.members_member_id_seq TO denis;


--
-- Name: TABLE messages; Type: ACL; Schema: messanger; Owner: messanger
--

GRANT ALL ON TABLE messanger.messages TO denis;


--
-- Name: SEQUENCE messages_message_id_seq; Type: ACL; Schema: messanger; Owner: messanger
--

GRANT ALL ON SEQUENCE messanger.messages_message_id_seq TO denis;


--
-- Name: TABLE users; Type: ACL; Schema: messanger; Owner: messanger
--

GRANT ALL ON TABLE messanger.users TO denis;


--
-- Name: SEQUENCE users_user_id_seq; Type: ACL; Schema: messanger; Owner: messanger
--

GRANT ALL ON SEQUENCE messanger.users_user_id_seq TO denis;


--
-- PostgreSQL database dump complete
--

