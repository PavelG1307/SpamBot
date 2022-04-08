import random
class Account(object):

    message_list=['Привет', 'Как дела', 'Хорошо']

    number_chat=-1
    timeout=5

    def __init__(self, client):
        self.client=client

    # def get_str(self):
    #     return self.client.export_session_string()

    def spam_message(self):
        self.number_chat+=1
        if self.number_chat >= len(self.chats_list):
            number_chat=0
        return random.choice(self.message_list), str(self.chats_list[self.number_chat])

    def print_all(self):
        print(self.client, self.message_list, self.timeout, self.number_chat)

        # Client(session_string)