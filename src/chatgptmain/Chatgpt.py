
from revChatGPT.V3 import Chatbot
import yaml
from func_timeout import func_set_timeout
import json
from sendwx.weixin import WeChat 

with open("src/config/data.yml","r") as f:
    datayml=yaml.load(f.read(),Loader=yaml.Loader)

class Chatgptwx():
    #创建一个机器人
    def NewChatgptFromeuser(self,wxuser):
        try:
            Api_key=datayml["OPENAI_ACCOUNT"][wxuser]["Api_key"]
        except Exception as e:
            print("data.yml Wrong parame"+str(e))
            exit()
        chatbot = Chatbot(api_key=Api_key)
        return chatbot
    #发送信息
    @func_set_timeout(60)
    def send_gpt(self,question,wxuser,chatbot):
            try:
                response=chatbot.ask(question)
                return response
            except Exception as e:
                if "Incorrect API key provided" in str(e):
                    print( "Incorrect API key provided")
                    return "请联系管理员为你添加正确的密钥"
                else :
                    return e
                
