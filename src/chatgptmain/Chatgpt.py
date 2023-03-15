
from revChatGPT.V3 import Chatbot
import yaml
from func_timeout import func_set_timeout
import json
from sendwx.weixin import WeChat 
class Chatgptwx():
    def NewChatgptFromeuser(self,wxuser):
        try:
            with open("src/config/data.yml","r") as f:
                datayml=yaml.load(f.read(),Loader=yaml.Loader)
                if datayml.get('OPENAI_ACCOUNT',None) is not None:
                    if datayml.get("OPENAI_ACCOUNT").get(wxuser) is not None:
                        Api_key=datayml["OPENAI_ACCOUNT"][wxuser]["Api_key"]
                        if datayml.get("SYSTEM_PROMPT") is not None:
                            data_system_prompt=datayml["SYSTEM_PROMPT"]
                            chatbot = Chatbot(api_key=Api_key,system_prompt=data_system_prompt)
                            return chatbot
                        else:
                            chatbot = Chatbot(api_key=Api_key)
                            return chatbot
                    else:
                        message_list=str.lstrip("请联系管理员为你配置账户")
                        WeChat().send_text(message_list, wxuser)
                        print("user"+wxuser +"not indata.yml")
                        return False
                else:
                    print("OPENAI_ACCOUNT not indata.yml")
                    return False
        except Exception as e:
            print("data.yml Wrong parame"+str(e))
            exit()
        # try:
        #     with open("src/config/data.yml","r") as f:
        #         datayml=yaml.load(f.read(),Loader=yaml.Loader)
        #         print("Load data from yml")
        # except Exception as e:
        #     print("data.yml Wrong parame"+str(e))
        #     exit()
        # try:
        #     Api_key=datayml["OPENAI_ACCOUNT"][wxuser]["Api_key"]
        # except Exception as e:
        #     print("data.yml Wrong parame"+str(e))
        #     exit()
        # chatbot = Chatbot(api_key=Api_key,system_prompt="你是呆瓜, 一个无所不能的大型语言模型")
        # return chatbot
    @func_set_timeout(60)
    def send_gpt(self,question,wxuser,chatbot):
            try:
                response=chatbot.ask(question)
                return response
            except Exception as e:
                if "Incorrect API key provided" in str(e):
                    print( "Incorrect API key provided")
                    return "请联系管理员为你添加正确的密钥"
                elif "SSLError" in str(e):
                    print(e)
                    return "网络出问题,请重试"
                elif "Your access was terminated due to violation of our policies" in str(e):
                    print(e)
                    return "Your access was terminated due to violation of our policies,请联系管理员"
                elif "Rate limit reached" in str(e):
                    print(e)
                    return "官方限制每分钟20个请求,请稍后重试"
                else:
                    print(e)
                    return "未知错误,请重试"
                