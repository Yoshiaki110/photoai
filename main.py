from flask import Flask, render_template, make_response, jsonify
from flask_cors import CORS
import os
import random

app = Flask(__name__)
CORS(app)

# robots.txt
@app.route('/robots.txt')
def robots():
    response = make_response(open('./static/robots.txt').read())
    response.headers["Content-type"] = "text/plain"
    return response

# sitemap.xml
@app.route('/sitemap.xml')
def sitemap():
    response = make_response(open('./static/sitemap.xml').read())
    response.headers["Content-type"] = "text/plain"
    return response

# トップページ
@app.route('/')
def root():
    return render_template('index.html')

# トップページ
@app.route('/index.html')
def index():
    return render_template('index.html')

# 写真情報の取得
@app.route("/api/photos", methods=['GET'])
def api_photos():
    # ディレクトリ一覧
    data = []
    path = './static/studios/'
    filedirs = os.listdir(path)
    dirs = [f for f in filedirs if os.path.isdir(os.path.join(path, f))]
    for dir in dirs:
        filedirs = os.listdir('./static/studios/' + dir)
        # jpgファイルのみ抽出
        files = [f for f in filedirs if f.endswith('.jpg')]
        #print(dir + files)
        for file in files:
            data.append([file, dir])
        # jpgファイルのみ抽出
        files = [f for f in filedirs if f.endswith('.webp')]
        #print(dir + files)
        for file in files:
            data.append([file, dir])

    print(data)
    random.shuffle(data)
    return jsonify(data[:50])


if __name__ == '__main__':
  app.run(debug=True)
