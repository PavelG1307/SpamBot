import random
class Account(object):

    message_list=[]
    mode = 'None'
    number_chat = 0
    timeout=300
    spam = False
    count_success = 0
    chats_list = []
    last_message = 0
    message_id = None
    w_chat=""
    p_chat=""
    id_chat=0

    def __init__(self, client):
        self.client=client

    def spam_chat(self):
        self.number_chat+=1
        if self.number_chat >= len(self.chats_list):
            number_chat=0
        return self.chats_list[self.number_chat].rsplit('https://t.me/', 1)[1][:-1]
    
    def spam_message(self):
        return random.choice(self.message_list)

    def print_all(self):
        print(self.client, self.message_list, self.timeout, self.number_chat)
