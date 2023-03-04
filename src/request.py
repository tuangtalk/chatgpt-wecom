import web
from receivewx.handle import Handle
from sendwx.weixin import WeChat 
from chatgptmain.judgeChatgpt import judgeChatpt
from chatgptmain.judgeuser import Judgeuser
from chatgptmain.Chatgpt import Chatgptwx
from func_timeout import func_set_timeout
import func_timeout
import threading
def sendtogpt(webinput,webdata):
        try:
            question,wxuser=Handle().POST(webinput,webdata)
            if question == "//新对话":
                botloaded,panduan=Judgeuser(wxuser)
                botloaded.newChatgpt(wxuser)
                botloaded.chatbot
                message_list=str.lstrip("上下文已清除，以下是新的对话")
                WeChat().send_text(message_list, wxuser)
                exit()
            chatbot=judgeChatpt().judgeChatptfuction(wxuser)
            try:
                ask=Chatgptwx().send_gpt(question, wxuser, chatbot)
            except func_timeout.exceptions.FunctionTimedOut as e:
                try:
                    botloaded,panduan=Judgeuser(wxuser)
                    botloaded.newChatgpt(wxuser)
                    ask=Chatgptwx().send_gpt(question, wxuser, botloaded.chatbot)
                except func_timeout.exceptions.FunctionTimedOut as e:
                    message_list=str.lstrip("超时请联系管理员")
                    WeChat().send_text(message_list, wxuser)
                    return e
                    exit()
            ask_bytes = ask.encode('utf-8')
            if len(ask_bytes) <= 2037:
                message_list=str.lstrip(ask)
                print("[ chatgpt -> wecom ] " + message_list)
                WeChat().send_text(message_list, wxuser)
                exit()
            else:
                i=1;start = 0
                while start < len(ask_bytes):
                    end = start + 2037
                    if end >= len(ask_bytes):
                        end = len(ask_bytes)
                    elif ask_bytes[end] & 0xC0 == 0x80:
                        while end >= start and ask_bytes[end] & 0xC0 == 0x80:
                            end -= 1
                    sub_string = ask_bytes[start:end].decode('utf-8')
                    message_list=f"Part {i}: {sub_string}"
                    print("[ chatgpt -> wecom ] " + message_list)
                    i=i+1
                    start = end
                    WeChat().send_text(message_list, wxuser)
        except Exception as Argument:
            print(Argument)
            exit(0)
class Request(object):
    def GET(self):
        sEchoStr=Handle().GET()
        return sEchoStr
    def POST(self):
        webinput=web.input()
        webdata=web.data()
        t = threading.Thread(target=sendtogpt,args=(webinput,webdata,))
        t.start()
    
