import web
from request import Request
#接口配置
urls = (
    '/api', 'Request',
)
class MyApplication(web.application):
    def run(self, port=6364, *middleware):
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, ('0.0.0.0', port))

if __name__ == "__main__":
    app = MyApplication(urls, globals())
    app.run()