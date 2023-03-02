import json
import requests
import yaml
import time
tokentime=0 #检查access_token是否过期如果
access_token="1"

with open("src/config/data.yml","r") as f:
    datayml=yaml.load(f.read(),Loader=yaml.Loader)
    WEIXIN_PUSH=datayml["WEIXIN_PUSH"]

class WeChat():
    def __init__(self):
        try:
            if "WEXIN_PROXY" in datayml:
                PROXY=datayml["WEXIN_PROXY"]
                proxies = {
                "http": PROXY,
                "https": PROXY,
                }
                self.proxies=proxies
            else:
                self.proxies=""
            self.agentid = WEIXIN_PUSH['agentid']
            self.secret = WEIXIN_PUSH['secret']
            self.corpid = WEIXIN_PUSH['corpid']
        except Exception as e:
            print(e)
            return "请检查data.yml"

    def get_access_token(self):
        '''
        获取access_token
        '''
        global tokentime
        global access_token
        #检查access_token是否过期如果
        if time.time()> tokentime:
           response = requests.get(
            f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={self.corpid}&corpsecret={self.secret}")
        #    access_token=WeChat().get_access_token()
           data = json.loads(response.text)
           access_token=data['access_token']
           tokentime=time.time()+7000
           return access_token
        else:
            return access_token

    def get_media_id(self, path):
        '''
        获取图片媒体文件id
        '''
        if path != None:
            access_token = self.get_access_token()
            curl = f'https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token={access_token}&type=image'
            files = {'image': open(path, 'rb')}
            response = requests.post(curl, files=files)
            data = json.loads(response.text)
            return data['media_id']

    @staticmethod
    def set_geshi(message_list):
        digest = '\n'.join(message_list)
        content = digest.replace('\n', '<br \>')
        return content, digest

    def send_text(self, message_list,towxuser):
        '''
        推送文本消息
        '''
        messages = WeChat.set_geshi(message_list)[1]
        text_dict = {
            "touser": towxuser,
            "msgtype": "text",
            "agentid": self.agentid,
            "text": {
                "content": messages
            },
            "safe": 0,
            "enable_id_trans": 0,
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        }
        return self.send(text_dict)


    def send_image(self,towxuser, path=None):
        '''
        推送图片
        '''
        media_id = self.get_media_id(path)
        tupian_dict = {
            "touser": towxuser,
            "msgtype": "image",
            "agentid": self.agentid,
            "image": {
                "media_id": media_id
            },
            "safe": 0,
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        }

        self.send(tupian_dict)

    def send_tuwen(self, title,towxuser, message_list):
        '''
        推送图文消息
        '''
        messages, digest = WeChat.set_geshi(message_list)
        tuwen_dict = {
            "touser": towxuser,
            "msgtype": "mpnews",
            "agentid": self.agentid,
            "mpnews": {
                "articles": [
                    {
                        "title": title,
                        "thumb_media_id": self.wx['media_id'],
                        "author": "雨园",
                        "content": messages,
                        "digest": digest,
                    }
                ]
            },
            "safe": 0,
            "enable_id_trans": 0,
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        }

        self.send(tuwen_dict)

    def send(self, dict):
        access_token = self.get_access_token()
        json_str = json.dumps(dict)
        res = requests.post(
            f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}", data=json_str,proxies=self.proxies)
        return json.loads(res.text)