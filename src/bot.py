import web
from request import Request
import yaml
from chatgptmain.balance import ckBalance
urls = (
    '/api', 'Request',
    '/balance', 'balance'
)

class MyApplication(web.application):
    def run(self, port=6364, *middleware):
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, ('0.0.0.0', port))
render=web.template.render('src/chatgptmain')
class balance:
    def GET(self):
        try:
            with open("src/config/data.yml","r") as f:
                datayml=yaml.load(f.read(),Loader=yaml.Loader)
                if datayml.get('BALANCE',None) is not None:
                    if datayml.get("BALANCE").get("CKBALANCE") is not None:
                        if datayml.get("BALANCE").get("CKBALANCE") is True:
                            balancelist=ckBalance(datayml["OPENAI_ACCOUNT"])
                            return render.index(balancelist)
                        else:
                            balancelist="404 not found"
                            return render.error(balancelist)
                    else:
                        balancelist="404 not found"
                        return render.error(balancelist)
                else:
                    balancelist="404 not found"
                    return render.error(balancelist)
        except Exception as e:
            print("data.yml Wrong parame"+str(e))
            balancelist="yml data error"
            return render.error(balancelist)
if __name__ == "__main__":
    app = MyApplication(urls, globals())
    app.run()
