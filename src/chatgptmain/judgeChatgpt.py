from chatgptmain.judgeuser import Judgeuser

class judgeChatpt():
    def judgeChatptfuction(self,wxuser):
        print(wxuser)
        #在这一步执行Judgeuser进行判断
        botloaded,panduan=Judgeuser(wxuser)
        if panduan is False:#如果没有此用户,就生成一个
            # judgeChatpt().judgeChatptfuction("clear").clear_conversations()
            # botloaded.newChatgpt(wxuser) 
            try:
                botloaded.newChatgpt(wxuser)
                if botloaded.chatbot is False:
                    botloaded.deleteuser(wxuser)
                    exit()
                else:
                    print(botloaded.chatbot)
                    return botloaded.chatbot
            except Exception as Argument:
                return Argument
        else:
            if None ==botloaded.chatbot:
                print("程序出错已经存在用户wxuser,但是对应的机器人实例不存在，将重新创建一次")
                try:
                    botloaded.newChatgpt(wxuser)
                    print(botloaded.chatbot)
                    return botloaded.chatbot
                except Exception as Argument:
                    return Argument
            else:
                print(botloaded.chatbot)
                return botloaded.chatbot