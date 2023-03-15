from chatgptmain.Chatgpt import Chatgptwx
class Judgeuser():
   _loaded = {}
   def __init__(self,name):
       self.name = name
       self.xml_load()
   def __new__(cls,name,*args):
       if cls._loaded.get(name) is not None:
           client = cls._loaded.get(name)
           return client,True
       client = super().__new__(cls)
       cls._loaded[name] = client
    #    print(client)
       return client,False
   def xml_load(self):
       print(self.name)
   def newChatgpt(self,wxuser):
        newchatbot=Chatgptwx().NewChatgptFromeuser(wxuser)
        self.chatbot=newchatbot

   def deleteuser(cls,name):
        del cls._loaded[name]
