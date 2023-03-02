# chatgpt-WeCom

### V0.2 版本使用 acheong08 的 ChatGPT V3，实现了企业微信与 ChatGPT 聊天。

### 这个版本使用的 chatgpt 开放的 gpt-3.5-turbo API，v0.11 和 V.14 版本教程请看 wiki 文件夹

> 该版本基于`acheong08的reChatGPT`开发，

#### 实现的功能

- 多用户使用隔离,建议一个用户对应一个 api key(多个用户用一个 api key 有可能会有其他问题),api 的使用这是需要付费的(每个账户赠送的有 18 刀),如果想用久一点就一个 openai 账户一个密钥,
- 支持上下文关联
- 支持用户清除上下文，开始新的对话
- 除了企业微信需要固定 ip 来配置可信 ip vps 可以不用代理,nas 等无公网 ip 的用户需要配置`data.yml`中的`WEXIN_PROXY`

#####需要准备的!!!!!!!!

- 企业微信账号
- 自建 http 代理(服务器部署用户不需要)
- chatgpt api key

### 获取 OpenAI 账户

- 建议参考谷歌获取

## 部署

#### docker 部署

- docker 端口 `-p 6364:6364`
- 需要挂载的 `-v /你自己创建的文件夹/config:/app/src/config`

- dokerhub [地址](https://hub.docker.com/r/yummys/chatgpt-wecom)选 latest 为最新版

  在本地目录下新建一个 config 文件夹在文件夹下新建 `data.yml` 文件,填写以下内容:

```YML
OPENAI_ACCOUNT:
  userA:
    Api_key: xxxx
  userB:
    Api_key: xxxx
  userC:
    Api_key: xxxx
WEIXIN_RECEIVE:
  Token: XXXX
  EncodingAESKey: XXXX
  CorpID: XXX
WEIXIN_PUSH:
  agentid: XXX
  secret: XXXX
  corpid: XXX
WEXIN_PROXY: http://domain:port
#WEXIN_PROXY为可选配置，配置登录微信推送所用的ip，企业bot可信ip里填的,VPS部署用户用不到可以删除
```

- 第一项`OPENAI_ACCOUNT` 其中 userA,userB,userC 改成企业微信用户账号, `Api_key`不同用户使用一个可能会有问题，
  <a href="https://sm.ms/image/cVypGqJbvgnSmRO" target="_blank"><img src="https://s2.loli.net/2023/02/10/cVypGqJbvgnSmRO.png" ></a>
- 第二项`WEIXIN_RECEIVE`是对应的企业微信自建机器人 api,目的是为了接收到用户发送的消息。
  CorpID 为个人企业微信的企业 id,回调需要的参数先填好需要的三个参数,最后 docker 跑起来后再在企业微信下图 url 中,然后保存即可,填入 `https:你的域名:端口/api` ,配置企业微信 api 接收消息,所需要的数据具体获取[教程](https://blog.csdn.net/zhaofuqiangmycomm/article/details/121633551)
  <a href="https://sm.ms/image/MfTPKUzNHI3Lrjq" target="_blank"><img src="https://s2.loli.net/2023/02/10/MfTPKUzNHI3Lrjq.png" ></a>
- 第三项`WEIXIN_PUSH`则是用于向用户返回 chatgpt 处理用户发送消息后的回答时使用。
  `agentid`,`secret`分别为为企业微信自建 bot 的 id,和 secret,`corpid`则依旧是企业 id, 获取填入数据[教程](https://www.pushplus.plus/doc/extend/cp.html#%E5%85%B7%E4%BD%93%E6%AD%A5%E9%AA%A4%E5%A6%82%E4%B8%8B)
  //////////
- 第四项`WEXIN_PROXY`则是用于配置企业微信代理。(vps 部署的用户不需要，`WEXIN_PROXY`(用不到可以删除),
  ~~默认还是在 docker 创建时的环境变量中填入 http 代理，将`PROXY`(不能删除)下子项目删除，再遇到 chatgpt 账户登陆问题或者是需要改微信可信代理 ip 时填入需要的子项，~~
  不需要环境变量配置代理,nas 或其他非 vps 的用户请配置`WEXIN_PROXY`
- 配置代理和可信 ip 参考(vps 用户也要在企业微信添加可信 ip 为 vps 的 ip 即可,不需要 WEXIN_PROXY 代理):
  最后一步需要一个 http 代理, 因为企业微信目前需要可信任 ip ,nas 的动态 ip 经常变更,因此需要在 `data.yml `中设置`WEXIN_PROXY`可以是 http 代理或者 sock 代理,微信可信任域名中填入对应的代理 ip,如图我的 http 代理为`http://10.0.0.45:8888`对应的服务器 ip 为`54.xxx.xxx.xxx`我在企业微信中加入可信任 ip``54.xxx.xxx.xxx`即可,有关代理搭建 http 代理或者 sock 代理请善用搜索
  <a href="https://sm.ms/image/ehZ7JEHQA6c53xm" target="_blank"><img src="https://s2.loli.net/2023/02/10/ehZ7JEHQA6c53xm.png" ></a>
  <a href="https://sm.ms/image/cz7yPgkrJLl2I1q" target="_blank"><img src="https://s2.loli.net/2023/02/10/cz7yPgkrJLl2I1q.png" ></a>

- 清空上下文指令 ,微信用户输入`//新对话`

  ### 最后 docker 跑起来后填入可信任 ip 与完成上面的 api 接收信息就可以正常使用了。
