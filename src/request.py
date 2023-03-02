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
                message_list=[str.lstrip("上下文已清除，以下是新的对话")]
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
                    message_list=[str.lstrip("超时请联系管理员")]
                    WeChat().send_text(message_list, wxuser)
                    exit()
            print("[ chatgpt -> wecom ] " + str.lstrip(ask))
            message_list=[str.lstrip(ask)]
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
    