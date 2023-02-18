import os
import web
from flask import request
from receivewx.handle import Handle
from sendwx.weixin import WeChat 
from chatgptmain.judgeChatgpt import judgeChatpt
from chatgptmain.judgeuser import Judgeuser
from chatgptmain.Chatgpt import Chatgptwx
import threading
def sendtogpt(webinput,webdata):
        try:
            question,wxuser=Handle().POST(webinput,webdata)
            if question == "//新对话":
                chatbot=judgeChatpt().judgeChatptfuction(wxuser)
                print(chatbot.conversation_id)
                if chatbot.conversation_id is None:
                    message_list=[str.lstrip("您还未开始对话,请先开始对话")]
                    WeChat().send_text(message_list, wxuser)
                    exit()
                else:
                    try:
                        chatbot.delete_conversation(chatbot.conversation_id)
                        botloaded,panduan=Judgeuser(wxuser)
                        botloaded.newChatgpt(wxuser)
                        botloaded.chatbot
                        message_list=[str.lstrip("上下文已清除，以下是新的对话")]
                        WeChat().send_text(message_list, wxuser)
                    except Exception as Argument:
                        message_list=[str.lstrip("对话清除失败,请重试")]
                        WeChat().send_text(message_list, wxuser)
                        exit()
                    exit()
            chatbot=judgeChatpt().judgeChatptfuction(wxuser)
            ask=Chatgptwx().send_gpt(question, wxuser, chatbot)
            # ask=str(chatgptwx().send_to_chagpt(question,wxuser))
            # lstripask=str.lstrip(ask)
            print(str.lstrip(ask))
            message_list=[str.lstrip(ask)]
            # print(ask)
            WeChat().send_text(message_list, wxuser)
            exit(0)
            return
        except Exception as Argument:
            return (Argument)
class Request(object):
    def GET(self):
        sEchoStr=Handle().GET()
        return sEchoStr
    def POST(self):
        webinput=web.input()
        webdata=web.data()
        t = threading.Thread(target=sendtogpt,args=(webinput,webdata,))
        t.start()
        
    