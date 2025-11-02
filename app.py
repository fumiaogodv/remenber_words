from flask import Flask,url_for,render_template

app=Flask(__name__)

# ##################################################################
#  关键修改部分：添加一个中间件来处理 URL 前缀
# ##################################################################
class PrefixMiddleware(object):
    def __init__(self, app, prefix=''):
        self.app = app
        self.prefix = prefix

    def __call__(self, environ, start_response):
        # 如果请求路径以指定的前缀开头，则移除前缀
        # 例如，将 /hello/wuziqi 修改为 /wuziqi
        if environ['PATH_INFO'].startswith(self.prefix):
            environ['PATH_INFO'] = environ['PATH_INFO'][len(self.prefix):]
            environ['SCRIPT_NAME'] = self.prefix
            return self.app(environ, start_response)
        else:
            # 如果不匹配前缀，直接返回 404
            start_response('404', [('Content-Type', 'text/plain')])
            return ["This URL does not belong to the app.".encode()]

# 将你的 Flask 应用包装在这个中间件中
app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix='/hello')
# ##################################################################


@app.route("/",methods=["GET"])
def mian():
    return render_template("index.html")

@app.route("/random_create",methods=["GET","POST"])
def random():
    return render_template('random.html')

@app.route("/date_list",methods=["GET","POST"])
def date_word():
    return render_template('date.html')

if __name__=="__main__":
    app.run(debug=True)