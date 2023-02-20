
from revChatGPT.V1 import Chatbot
import yaml
import json
from sendwx.weixin import WeChat 



with open("src/config/data.yml","r") as f:
    datayml=yaml.load(f.read(),Loader=yaml.Loader)
    # OPENAI_ACCOUNT=datayml["OPENAI_ACCOUNT"]
        # ChatgptModel=datayml["ChatgptModel"]
class Chatgptwx():
    def __init__(self):
        try:
            if "openai_proxy" in datayml["PROXY"]:
                PROXY=datayml["PROXY"]
                proxies = PROXY["openai_proxy"]
                self.proxies=proxies
            else:
                self.proxies=""
            # self.ChatgptModel = ChatgptModel
            # self.OPENAI_ACCOUNT = OPENAI_ACCOUNT
        except Exception as e:
            print(e)
            return "请检查data.yml"
    #创建一个机器人
    def NewChatgptFromeuser(self,wxuser):
        if wxuser in datayml["OPENAI_ACCOUNT"]:
            user=datayml["OPENAI_ACCOUNT"][wxuser]
            try:
                if None == self.proxies:
                    chatbot=Chatbot(config={
                        "email": user["email"],
                        "password": user["password"]
                    })
                else:
                    chatbot=Chatbot(config={
                        "email": user["email"],
                        "password": user["password"],
                        "proxy":self.proxies
                    })
                return chatbot
            except Exception as Argument:
                if str(Argument) == "'accessToken'":
                    print("请添加可以正常访问chatgpt的代理")
                exit()
                return "error"
        else:
            message_list=[str.lstrip("请联系管理员为您添加chatgpt账户")]
            WeChat().send_text(message_list, wxuser)
            print("请为"+wxuser+"添加chatgpt账户")
            exit()
    #发送信息
    def send_gpt(self,question,wxuser,chatbot):
    # print (Chatgptwx().NewChatgptFromeuser())
        try:
            for data in chatbot.ask(question):
                response = data["message"]
            # response = chatbot.ask(question,user=wxuser)
            # print(response["choices"][0]["text"])
            # return response["choices"][0]["text"]
            # print(chatbot.conversation_id)
            return response
        except Exception as Argument:
            print("向chatgpt发送信息返回失败")
            response=Argument
            return response