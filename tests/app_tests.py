import unittest
from app import app


class AppTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_index(self):
        rv = self.app.get('/world/')
        self.assertEqual(200, rv.status_code)
        self.assertEqual(b'Hello, world!', rv.data)
        self.assertEqual("text/html", rv.mimetype)
        # print(rv, dir(rv))
        # print(rv.data)

    def test_form(self):
        rv = self.app.post('/form/', data={'first_name': "Denis",\
                                           'last_name': "Stasyev"})
        self.assertEqual(b'{"first_name":"Denis","last_name":"Stasyev"}\n', rv.data)

    def tearDown(self):
        pass
##########

    def test_login(self):
        rv = self.app.get('/login/')
        self.assertEqual(200, rv.status_code)
        self.assertEqual("text/html", rv.mimetype)

        rv = self.app.post('/login/', data={'username': "testusername",\
                                            'password': "testpassword"})
        self.assertEqual(200, rv.status_code)
        self.assertEqual(b'{"password":"testpassword","username":"testusername"}\n', rv.data)
        self.assertEqual("application/json", rv.mimetype)

    def test_register(self):
        rv = self.app.get('/register/')
        self.assertEqual(200, rv.status_code)
        self.assertEqual("text/html", rv.mimetype)

        # ToDo
        # rv = self.app.post('/register/', data={'username': "testusername",\
        #                                    'password': "testpassword"})
        # self.assertEqual(200, rv.status_code)
        # self.assertEqual(b'{"password":"testpassword","username":"testusername"}\n', rv.data)
        # self.assertEqual("application/json", rv.mimetype)
##########

    def test_search_users(self):
        rv = self.app.get('/search_users/')
        self.assertEqual(200, rv.status_code)
        self.assertEqual(b'{"users":["User1","User2"]}\n', rv.data)
        self.assertEqual("application/json", rv.mimetype)

    def test_search_chats(self):
        rv = self.app.get('/search_chats/')
        self.assertEqual(200, rv.status_code)
        self.assertEqual(b'{"chats":["Chat1","Chat2"]}\n', rv.data)
        self.assertEqual("application/json", rv.mimetype)

    def test_list_chats(self):
        rv = self.app.get('/list_chats/')
        self.assertEqual(200, rv.status_code)
        self.assertEqual(b'{"chats":["Chat1","Chat2"]}\n', rv.data)
        self.assertEqual("application/json", rv.mimetype)

    def test_create_pers_chat(self):
        rv = self.app.get('/create_pers_chat/')
        self.assertEqual(200, rv.status_code)
        self.assertEqual("text/html", rv.mimetype)

        rv = self.app.post('/create_pers_chat/', data={'chat': "Chat"})
        self.assertEqual(200, rv.status_code)
        self.assertEqual(b'{"chat":"Chat"}\n', rv.data)
        self.assertEqual("application/json", rv.mimetype)

    def test_create_group_chat(self):
        rv = self.app.get('/create_group_chat/')
        self.assertEqual(200, rv.status_code)
        self.assertEqual("text/html", rv.mimetype)

        rv = self.app.post('/create_group_chat/', data={'chat': "Chat"})
        self.assertEqual(200, rv.status_code)
        self.assertEqual(b'{"chat":"Chat"}\n', rv.data)
        self.assertEqual("application/json", rv.mimetype)

    def test_add_members_to_group_chat(self):
        rv = self.app.post('/add_members_to_group_chat/')
        self.assertEqual(200, rv.status_code)
        self.assertEqual(b'{}\n', rv.data)
        self.assertEqual("application/json", rv.mimetype)

    def test_leave_group_chat(self):
        rv = self.app.post('/leave_group_chat/')
        self.assertEqual(200, rv.status_code)
        self.assertEqual(b'{}\n', rv.data)
        self.assertEqual("application/json", rv.mimetype)

    def test_send_message(self):
        rv = self.app.post('/send_message/')
        self.assertEqual(200, rv.status_code)
        self.assertEqual(b'{"message":"Message"}\n', rv.data)
        self.assertEqual("application/json", rv.mimetype)

    def test_read_message(self):
        rv = self.app.get('/read_message/')
        self.assertEqual(200, rv.status_code)
        self.assertEqual(b'{"chat":"Chat"}\n', rv.data)
        self.assertEqual("application/json", rv.mimetype)

    def test_upload_file(self):
        rv = self.app.post('/upload_file/')
        self.assertEqual(200, rv.status_code)
        self.assertEqual(b'{"attach":"Attachment"}\n', rv.data)
        self.assertEqual("application/json", rv.mimetype)


if __name__ == "__main__":
    app.config.from_object('config.TestingConfig')
    unittest.main()


############################################################
class JSONRPCTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_get_name(self):
        rv = self.app.post('/api/', data='{"jsonrpc": "2.0", "method": \
                                    "print_name", "params": [], "id": 1}')
        # print(rv.data)
        self.assertEqual(b'{"id":1,"jsonrpc":"2.0","result":{"name":"Ivan"}}\n',\
                        rv.data)
