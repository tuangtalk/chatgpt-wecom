
from revChatGPT.Official import Chatbot
import yaml
import json


with open("src/config/data.yml","r") as f:
    datayml=yaml.load(f.read(),Loader=yaml.Loader)
    OPENAI_API_KEY=datayml["OPENAI_API_KEY"]
    ChatgptModel=datayml["ChatgptModel"]

class Chatgptwx():
    def __init__(self):
        try:
            self.ChatgptModel = ChatgptModel
            self.OPENAI_API_KEY = OPENAI_API_KEY
        except Exception as e:
            print(e)
            return "请检查data.yml"
    #创建一个机器人
    def NewChatgptFromeuser(self,wxuser):
        try:
            chatbot=Chatbot(OPENAI_API_KEY[wxuser],engine=self.ChatgptModel)
            return chatbot
        except Exception as Argument:
            print(Argument)
            return "请联系管理员为你添加密钥"

    #发送信息
    def send_gpt(self,question,wxuser,chatbot):
    # print (Chatgptwx().NewChatgptFromeuser())
        try:
            response = chatbot.ask(question,user=wxuser)
            # print(response["choices"][0]["text"])
            return response["choices"][0]["text"]
        except Exception as Argument:
            print("向chatgpt发送信息返回失败")
            print(Argument)
            return "error"





        