import random
class Account(object):

    message_list=["Hello, I am promoting telegram channels and adding traffic from other people's channels! If you are interested, write in PM", 'Hi, if you need traffic to your Telegram channel, write in private messages!']

    number_chat=220
    timeout=300
    spam = False
    count_success = 0
    chats_list = []

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
