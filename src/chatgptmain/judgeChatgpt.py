from chatgptmain.judgeuser import Judgeuser

class judgeChatpt():
        
        #利用Judgeuser判断用户是否存在已经创建好的chatgpt实例如果有返回,没有就创建
    def judgeChatptfuction(self,wxuser):
        # print("多例模式实例")
        print(wxuser)
        #在这一步执行Judgeuser进行判断
        botloaded,panduan=Judgeuser(wxuser)
        if panduan is False:#如果没有此用户,就生成一个
            # judgeChatpt().judgeChatptfuction("clear").clear_conversations()
            try:

                botloaded.newChatgpt(wxuser)
                a=botloaded.chatbot
                print(botloaded.chatbot)
                a.clear_conversations()
                print("清除"+wxuser+"账户的历史对话成功")
                #利用Judgeuser(wxuser)的返回值再掉用Judgeuser 中的newChatgpt()方法生成一个chatgpt实例
                botloaded.newChatgpt(wxuser)
                #取值
                botloaded.chatbot
                # newchatbot=Chatgptwx().NewChatgptFromeuser()
                # self.chatbot=newchatbot
                # print("botloaded.chatbot赋值成功")
                print(botloaded.chatbot)
                return botloaded.chatbot
            except Exception as Argument:
                return False
        else:
            try:
                print(botloaded.chatbot)
                return botloaded.chatbot
            except Exception as e:
                print("程序出错已经存在用户wxuser,但是对应的机器人实例不存在")
                return False