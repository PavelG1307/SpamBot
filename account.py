import random
class Account(object):

    message_list=['Привет', 'Hi', 'Hello', 'hi']

    number_chat=10
    timeout=20

    def __init__(self, client):
        self.client=client

    # def get_str(self):
    #     return self.client.export_session_string()

    def spam_chat(self):
        self.number_chat+=1
        if self.number_chat >= len(self.chats_list):
            number_chat=0
            # https://t.me/
        # return self.chats_list[self.number_chat][13:-1]
        return self.chats_list[self.number_chat].rsplit('https://t.me/', 1)[1][:-1]
    
    def spam_message(self):
        return random.choice(self.message_list)

    def print_all(self):
        print(self.client, self.message_list, self.timeout, self.number_chat)

        # Client(session_string)