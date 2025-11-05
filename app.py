from flask import Flask,url_for,render_template,jsonify,request
import os,json
from  datetime import  datetime

FORGET_PATH = "static/forget.json"
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
app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix='/app4')
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

@app.route("/forget_word",methods=["GET","POST"])
def forget():
    return render_template('forget.html')

@app.route("/api/forget", methods=["POST"])
def add_forget():
    data = request.get_json()
    date = data.get("date")
    word = data.get("word")
    meaning = data.get("meaning")
    path = "static/forget.json"

    if not os.path.exists(path):
        forget_data = {}
    else:
        with open(path, "r", encoding="utf-8") as f:
            try:
                forget_data = json.load(f)
            except json.JSONDecodeError:
                forget_data = {}

    # 日期下是一个 dict，而不是列表
    forget_data.setdefault(date, {})
    forget_data[date][word] = meaning

    with open(path, "w", encoding="utf-8") as f:
        json.dump(forget_data, f, ensure_ascii=False, indent=2)

    return jsonify({"status": "ok", "message": f"{word} 已加入 {date}"})

# 删除单词接口
@app.route("/api/forget/delete", methods=["POST"])
def delete_forget_word():
    data = request.get_json()
    date = data["date"]
    english = data["english"]

    if not os.path.exists(FORGET_PATH):
        return jsonify({"error": "forget.json 不存在"}), 404

    with open(FORGET_PATH, "r", encoding="utf-8") as f:
        forget_data = json.load(f)

    if date in forget_data and english in forget_data[date]:
        del forget_data[date][english]
        # 若该日期下已无单词，则删除该日期键
        if not forget_data[date]:
            del forget_data[date]

        with open(FORGET_PATH, "w", encoding="utf-8") as f:
            json.dump(forget_data, f, ensure_ascii=False, indent=2)

    return jsonify({"message": "删除成功"})

if __name__=="__main__":
    app.run(debug=True)