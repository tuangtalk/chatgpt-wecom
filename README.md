# chatgpt-WeCom

### 使用 acheong08 的 ChatGPT 接口，实现了企业微信与 ChatGPT 聊天

> 该版本基于`ChatGPT`开发，

#### 实现的功能

- 多用户使用隔离,虽然做了用户隔离,但是在使用的过程中发现两个用户调用一个密钥生成两个不同实例时候,最先创建的那个实例正常,后面那个实例比较呆傻,因此选择多个密钥与多个用户实例一一关联
- 支持上下文关联
- 支持使用代理请求 chatgpt

#####需要准备的!!!!!!!!

- 企业微信账号
- 自建 http 代理(服务器部署用户不需要)
- OPEN AI 密钥

### 获取 OpenAI API KEY

- 建议参考[此教程](https://blog.csdn.net/hekaiyou/article/details/128303729)获取

## 部署

#### docker 部署

- docker 端口 `-p 6364:6364`
- 需要挂载的 `-v /你自己创建的文件夹/config:/app/src/config`

- dokerhub [地址](https://hub.docker.com/r/yummys/chatgpt-wecom)
  在本地目录下新建一个 config 文件夹在文件夹下新建 data.yml 文件,填写以下内容:

```YML
OPENAI_API_KEY:
  userA: XXXXX
  userB: XXXXX
WEIXIN_RECEIVE:
  Token: XXXXX
  EncodingAESKey: XXXXX
  CorpID: XXXXX
WEIXIN_PUSH:
  agentid: XXXXX
  secret: XXXXX
  corpid: XXXXX
#   media_id: media_id
ChatgptModel: text-davinci-002
```

- 第一项`OPENAI_API_KEY` 其中 userA,userB,userC 改成企业微信用户账号,xxxx 填从 openai 中获取的密钥。
  <a href="https://sm.ms/image/cVypGqJbvgnSmRO" target="_blank"><img src="https://s2.loli.net/2023/02/10/cVypGqJbvgnSmRO.png" ></a>
- 第二项`WEIXIN_RECEIVE`是对应的企业微信自建机器人 api,目的是为了接收到用户发送的消息。
  CorpID 为个人企业微信的企业 id,回调需要的参数先填好需要的三个参数,最后 docker 跑起来后再在企业微信下图 url 中,然后保存即可,填入 `https:你的域名:端口/api` ,配置企业微信 api 接收消息,所需要的数据具体获取[教程](https://blog.csdn.net/zhaofuqiangmycomm/article/details/121633551)
  <a href="https://sm.ms/image/MfTPKUzNHI3Lrjq" target="_blank"><img src="https://s2.loli.net/2023/02/10/MfTPKUzNHI3Lrjq.png" ></a>
- 第三项`WEIXIN_PUSH`则是用于向用户返回 chatgpt 处理用户发送消息后的回答时使用。
  `agentid`,`secret`分别为为企业微信自建 bot 的 id,和 secret,`corpid`则依旧是企业 id, 获取填入数据[教程](https://www.pushplus.plus/doc/extend/cp.html#%E5%85%B7%E4%BD%93%E6%AD%A5%E9%AA%A4%E5%A6%82%E4%B8%8B)
  //////////
- 第四项 `ChatgptModel`是 chatgpt 模型,泄露的模型已经撤销了,gpt-3 非常不稳定,因此使用的为 gpt-2,如果你发现了更好的模型可以更改。
- (如果是在服务器部署则不需要)最后一步需要一个 http 代理, 因为企业微信目前需要可信任 ip ,nas 的动态 ip 经常变更,因此需要在 docker 创建时的环境变量中填入 http 代理,微信可信任域名中填入对应的代理 ip,如图我的 http 代理为`http://10.0.0.45:8888`对应的服务器 ip 为`54.xxx.xxx.xxx`我在企业微信中加入可信任 ip``54.xxx.xxx.xxx`即可,有关代理搭建和如何在 docker run 时添加环境变量请善用搜索。
  <a href="https://sm.ms/image/ehZ7JEHQA6c53xm" target="_blank"><img src="https://s2.loli.net/2023/02/10/ehZ7JEHQA6c53xm.png" ></a>
  <a href="https://sm.ms/image/cz7yPgkrJLl2I1q" target="_blank"><img src="https://s2.loli.net/2023/02/10/cz7yPgkrJLl2I1q.png" ></a> #####最后 docker 跑起来后填入可信任 ip 与完成上面的 api 接收信息就可以正常使用了。
