import web
from receivewx.WXBizMsgCrypt import WXBizMsgCrypt
import yaml
import xml.etree.ElementTree as ET
import requests
import json


with open("src/config/data.yml","r") as f:
    datayml=yaml.load(f.read(),Loader=yaml.Loader)
    WEIXIN_RECEIVE=datayml["WEIXIN_RECEIVE"]

class Handle(object):
    def __init__(self):
        try:
            self.sToken = WEIXIN_RECEIVE["Token"]
            self.sEncodingAESKey = WEIXIN_RECEIVE["EncodingAESKey"]
            self.sCorpID = WEIXIN_RECEIVE["CorpID"]
        except Exception as e:
            print(e)
            return "请检查data.yml"
    #回调验证接口
    def GET(self):  
        try:
            data = web.input()
            if len(data) == 0:
                return "no data"
            sVerifyMsgSig = data.msg_signature
            sVerifyTimeStamp = data.timestamp
            sVerifyNonce = data.nonce
            sVerifyEchoStr = data.echostr
            if sVerifyEchoStr is not None:
                wxcpt=WXBizMsgCrypt(self.sToken,self.sEncodingAESKey,self.sCorpID)
                ret,sEchoStr=wxcpt.VerifyURL(sVerifyMsgSig, sVerifyTimeStamp,sVerifyNonce,sVerifyEchoStr)
                if(ret!=0):
                    print("ERR: VerifyURL ret: " + str(ret))
                    # print(sEchoStr)
                else:
                    # print(sEchoStr)
                    return sEchoStr
        except Exception as Argument:
            print(Argument)
    #回调API调用是post
    def POST(self,webinput,webdata):
        try:
            data=webinput
            # print("question")
            # data = web.input()
            if len(data) == 0:
                return "no data"
            sReqMsgSig = data.msg_signature
            sReqTimeStamp = data.timestamp
            sReqNonce = data.nonce
            sReqData = webdata
            # sReqData = web.data()
            if len(sReqData) == 0:
                return "hello, this is handle view"
            wxcpt=WXBizMsgCrypt(self.sToken,self.sEncodingAESKey,self.sCorpID)
            ret,sMsg=wxcpt.DecryptMsg( sReqData, sReqMsgSig, sReqTimeStamp, sReqNonce)
            if( ret!=0 ):
                print("ERR: DecryptMsg ret: " + str(ret))
            xml_tree = ET.fromstring(sMsg)
            # for i in xml_tree:
            #     print(i.tag, i.attrib)  # 打印孩子节点的标签和属性值
            ToUserName = xml_tree.find("ToUserName").text
            CreateTime = xml_tree.find("CreateTime").text
            FromUserName = xml_tree.find("FromUserName").text
            MsgType = xml_tree.find("MsgType").text
            AgentID = xml_tree.find("AgentID").text
            content =  xml_tree.find("Content").text
            question=str(content)
            wxuser=str(FromUserName)
            print("[ wecom -> chatgpt ] " + question)
            # ask=str(chatgptwx().send_to_chagpt(question))
            # print(ask)
            # message_list=[ask]
            # WeChat().send_text(message_list)
            # try:
            #     ask=str(chatgptwx().send_to_chagpt(question))
            #     message_list=[ask]
            #     print(ask)
            #     WeChat().send_text(message_list)
            # except Exception as Argument:
            #     return(Argument)
            # Event = xml_tree.find("Event").text
            # EventKey = xml_tree.find("EventKey").text
          
            # print(content)
            # if MsgType=='event' and Event=='click':
            #     if EventKey == '自定义菜单的健值1':
            #         #你自己的数据处理
            #         content =  "你要返回的处理内容";
            #     if EventKey == '自定义菜单的健值2':
            #         #你自己的数据处理
            #         content =  "你要返回的处理内容";     
            # sRespData = "<xml><ToUserName>"+ToUserName+"</ToUserName><FromUserName>"+FromUserName+"</FromUserName><CreateTime>"+CreateTime+"</CreateTime><MsgType>text</MsgType><Content>"+content+"</Content><AgentID>"+AgentID+"</AgentID></xml>"
            # print(sRespData)
            # ret,sEncryptMsg=wxcpt.EncryptMsg(sRespData, sReqNonce, sReqTimeStamp)
            # if( ret!=0 ):
            #     print ("ERR: EncryptMsg ret: " + str(ret))
            #     sys.exit(1)
            # print(xml_tree)
            return question,wxuser     
        except Exception as Argument:
            print(Argument)
            return(Argument)
