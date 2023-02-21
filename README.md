# chatgpt-WeCom

### V0.12 版本使用 acheong08 的 ChatGPT V1，实现了企业微信与 ChatGPT 聊天。

### 这个版本使用的真正的 chatgpt 而不再是 gpt-3，不知道什么时候会和谐（acheong08 的 ChatGPT 原因），所以建议大家保留 v0.11 版本，新建一个 docker 和企业微信 bot 使用，v0.11 版本教程请看 wiki 文件夹

> 该版本基于`acheong08的reChatGPT`开发，

#### 实现的功能

- 多用户使用隔离,一个用户一个账号
- 支持使用 access_token登录
- 支持上下文关联
- 支持用户清除上下文，开始新的对话
- 支持 chatgpt 登录 和微信推送分别使用不同的代理(由于登录 chatgpt 账户比较挑代理，所以代理分出来)

#####需要准备的!!!!!!!!
###对于代理或者vps网络的要求较高，如果网络差使用体验会差很多
- 企业微信账号
- 自建 http 代理(服务器部署用户不需要)，
- 可以使用 chatgpt 的账户

### 获取 OpenAI 账户

- 建议参考谷歌获取

## 部署

#### docker 部署

- docker 端口 `-p 6364:6364`
- 需要挂载的 `-v /你自己创建的文件夹/config:/app/src/config`

- dokerhub [地址](https://hub.docker.com/r/yummys/chatgpt-wecom)选 latest 或者 0.12 为最新版

  在本地目录下新建一个 config 文件夹在文件夹下新建 data.yml 文件,填写以下内容:

```YML
OPENAI_ACCOUNT:
  userA:
    email: xxxx
    password: xxxx
    access_token:xxxx
    #access_token和账户秘密二选一即可，优先使用账户密码
  userB:
    email: xxxx
    password: xxxx
  userC:
    email: xxxx
    password: xxxx
WEIXIN_RECEIVE:
  Token: XXXX
  EncodingAESKey: XXXX
  CorpID: XXX
WEIXIN_PUSH:
  agentid: XXX
  secret: XXXX
  corpid: XXX
PROXY:
#PROXY:这个大项不可以删除，会报错，子项可以删除不需要的
  openai_proxy: xxxxxx
  #openai_proxy为可选配置，配置登录chatgpt所用的ip
  weixinpush_proxy: xxxxxx
  #weixinpush_proxy为可选配置，配置登录微信推送所用的ip，企业bot可信ip里填的
```

- 第一项`OPENAI_ACCOUNT` 其中 userA,userB,userC 改成企业微信用户账号, `email`,`password`不同用户使用一个会有问题，acheong08 的 reChatGPT 的问题或者是 chatgpt 对这个有限制，
  <a href="https://sm.ms/image/cVypGqJbvgnSmRO" target="_blank"><img src="https://s2.loli.net/2023/02/10/cVypGqJbvgnSmRO.png" ></a>
- 第二项`WEIXIN_RECEIVE`是对应的企业微信自建机器人 api,目的是为了接收到用户发送的消息。
  CorpID 为个人企业微信的企业 id,回调需要的参数先填好需要的三个参数,最后 docker 跑起来后再在企业微信下图 url 中,然后保存即可,填入 `https:你的域名:端口/api` ,配置企业微信 api 接收消息,所需要的数据具体获取[教程](https://blog.csdn.net/zhaofuqiangmycomm/article/details/121633551)
  <a href="https://sm.ms/image/MfTPKUzNHI3Lrjq" target="_blank"><img src="https://s2.loli.net/2023/02/10/MfTPKUzNHI3Lrjq.png" ></a>
- 第三项`WEIXIN_PUSH`则是用于向用户返回 chatgpt 处理用户发送消息后的回答时使用。
  `agentid`,`secret`分别为为企业微信自建 bot 的 id,和 secret,`corpid`则依旧是企业 id, 获取填入数据[教程](https://www.pushplus.plus/doc/extend/cp.html#%E5%85%B7%E4%BD%93%E6%AD%A5%E9%AA%A4%E5%A6%82%E4%B8%8B)
  //////////
- 第四项`PROXY`则是用于配置 chatgpt 和者企业微信代理。(vps 部署且并且 vps 的 ip 可以正常访问 chatgpt 的用户不需要，`PROXY`(不能删除),子项可删除)
  默认还是在 docker 创建时的环境变量中填入 http 代理，将`PROXY`(不能删除)下子项目删除，再遇到 chatgpt 账户登陆问题或者是需要改微信可信代理 ip 时填入需要的子项，
- 配置代理和可信 ip 参考(vps 用户也要在企业微信添加可信 ip):
  最后一步需要一个 http 代理, 因为企业微信目前需要可信任 ip ,nas 的动态 ip 经常变更,因此需要在 docker 创建时的环境变量中填入 http 代理,微信可信任域名中填入对应的代理 ip,如图我的 http 代理为`http://10.0.0.45:8888`对应的服务器 ip 为`54.xxx.xxx.xxx`我在企业微信中加入可信任 ip``54.xxx.xxx.xxx`即可,有关代理搭建和如何在 docker run 时添加环境变量请善用搜索。
  <a href="https://sm.ms/image/ehZ7JEHQA6c53xm" target="_blank"><img src="https://s2.loli.net/2023/02/10/ehZ7JEHQA6c53xm.png" ></a>
  <a href="https://sm.ms/image/cz7yPgkrJLl2I1q" target="_blank"><img src="https://s2.loli.net/2023/02/10/cz7yPgkrJLl2I1q.png" ></a>

- 清空上下文指令 ,微信用户输入`//新对话`

  ### 最后 docker 跑起来后填入可信任 ip 与完成上面的 api 接收信息就可以正常使用了。

  ### 最后 最后，不知道这样是否会封 chatgpt 的账户，请自行斟酌
