from chatgptmain.Chatgpt import Chatgptwx
class Judgeuser():
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
        newchatbot=Chatgptwx().NewChatgptFromeuser(wxuser)
        self.chatbot=newchatbot
    