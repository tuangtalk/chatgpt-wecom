from chatgptmain.Chatgpt import Chatgptwx
from revChatGPT.Official import Chatbot

class Judgeuser():
    # 判断用户是否存在已经创建好的chatgpt实例
   ##定义类实例化对象字典，即不同的实例对象对应不同的对象空间地址引用
   _loaded = {}
   def __init__(self,name):
       self.name = name
       self.xml_load()
   def __new__(cls,name,*args):
       if cls._loaded.get(name) is not None:
           client = cls._loaded.get(name)
           print(f"使用已存在的对象 {name}")
           return client,True
       print(f"创建新的访问对象 {name}")
       client = super().__new__(cls)
       cls._loaded[name] = client
    #    print(client)
       return client,False

   def xml_load(self):
       print("初始化init",self.name)

    #为用户创建一个Chagpt实例
   def newChatgpt(self,wxuser):
        try:
            newchatbot=Chatgptwx().NewChatgptFromeuser(wxuser)
            self.chatbot=newchatbot
            # print("创建成功返回")
            return newchatbot
        except Exception as Argument:
            return False
    