class Account(object):

    message_list=[]

    number_chat=0
    timeout=15

    def __init__(self, client):
        self.client=client

    def get_str(self):
        return self.client.export_session_string()

    def send_message(self, text, chat):
        print('send message: ' + text + ' в чат ' + str(chat))
        return True
    
    def start(self):
        return self.start()

    def print_all(self):
        print(self.client, self.message_list, self.timeout, self.number_chat)

        # Client(session_string)