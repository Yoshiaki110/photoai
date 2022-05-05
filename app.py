from dis import dis
from flask import Flask, request, render_template, make_response, jsonify
from flask_cors import CORS
from keras.preprocessing import image
from keras.applications.inception_resnet_v2 import InceptionResNetV2, preprocess_input, decode_predictions
import numpy as np
import pickle
import os
import base64
from PIL import Image
from io import BytesIO

DTFILE = 'data.dat'

print('@@ 起動')
def load(filename):
    feature_list=[]
    try:
        with open(filename, "rb") as f:
            feature_list = pickle.load(f)   
    except Exception as e:
        print('load err:' + str(e))
    return feature_list

def save(filename):
    try:
        with open(filename, "wb") as f:
            pickle.dump(feature_list, f)
    except Exception as e:
        print('write err:' + str(e))

def get_feature(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    #feature = model.predict(x)[0]
    feature = model.predict(x)
    ar = np.array(feature[:])
    return ar

def get_nearest(feature_list, feature):
    min_dist = 999999
    name = ''
    for n, v in feature_list:
        dist = np.sum((v-feature)*(v-feature))
        #print(n, dist)
        if dist < min_dist:
            min_dist = dist
            name = n
    return name, min_dist

def get_nearlist(feature_list, feature):
    list = []
    for n, v in feature_list:
        dist = np.sum((v-feature)*(v-feature))
        list.append([n, int(dist)])
    list.sort(reverse=False, key=lambda x:x[1])
    return list[:10]

# 画像リスト作成
def makelist(feature_list):
  try:
    path = './'
    filedirs = os.listdir(path)
    dirs = [f for f in filedirs if os.path.isdir(os.path.join(path, f))]
    for dir in dirs:
        filedirs = os.listdir(path + dir)
        # jpgファイルの抽出
        files = [f for f in filedirs if f.endswith('.jpg')]
        for fname in files:
            feature = get_feature(path + dir + '/' + fname)
            feature_list.append([dir, feature])
            print('データ読み込み', dir, fname)
  except:
    pass

# 保存解析データをロード
print('@@ 保存解析データをロード 開始')
feature_list = load(DTFILE)
print('@@ 保存解析データをロード 完了')

# 学習済みデータをロード
print('@@ 学習済みデータをロード 開始')
model = InceptionResNetV2(weights='imagenet', include_top=False)
print('@@ 学習済みデータをロード 完了')
# 画像を解析
#makelist(feature_list)
#save(DTFILE)

app = Flask(__name__)
CORS(app)

# robots.txt
@app.route('/robots.txt')
def robots():
    print("** /robots.txt")
    response = make_response(open('./static/robots.txt').read())
    response.headers["Content-type"] = "text/plain"
    return response

# sitemap.xml
@app.route('/sitemap.xml')
def sitemap():
    print("** /sitemap.xml")
    response = make_response(open('./static/sitemap.xml').read())
    response.headers["Content-type"] = "text/plain"
    return response

# トップページ
@app.route('/')
def root():
    print("** /")
    return render_template('index.html')

# トップページ
@app.route('/index.html')
def index():
    print("** /index.html")
    return render_template('index.html')

# analyzerページ
@app.route('/analyzer.html')
def analyzer():
    print("** /analyzer.html")
    return render_template('analyzer.html')

@app.route("/api/similar", methods=['POST'])
def api_similar():
    print("** /api/similar start")
    base64_png = request.form['image']
    code = base64.b64decode(base64_png.split(',')[1])  # remove header
    image_decoded = Image.open(BytesIO(code))
    fname = os.path.join('./', 'image.png')
    image_decoded.save(fname)
    # 解析データを保存
    feature = get_feature(fname)
    # 確認
    list = get_nearlist(feature_list, feature)
    os.remove(fname)
    print("** /api/similar end")
    return jsonify(list)

@app.route("/api/similar2", methods=['POST'])
def api_similar2():
    print("** /api/similar start")
    img = request.files['image']
    name = img.filename
    fname = os.path.join('./', name)
    img.save(fname)
    # 解析データを保存
    feature = get_feature(fname)
    # 確認
    #name, dist = get_nearest(feature_list, feature)
    list = get_nearlist(feature_list, feature)
    print("** /api/similar end")

    #return jsonify({'data': {'name': name, 'dist': int(dist)}})
    #return jsonify({'data': list})
    return jsonify(list)

# 写真情報の取得
@app.route("/api", methods=['GET'])
def api():
    ret = ''
    for fname in [
        './cafune_photostudio/test/2022-01-05_10-25-01_UTC.jpg',
        './cafune_photostudio/test/2022-03-21_10-03-16_UTC_2.jpg',
        './cocoanoborito/test/2022-03-06_01-55-55_UTC_1.jpg',
        './cocoanoborito/test/2022-03-17_04-05-31_UTC.jpg',
        './holidaysphotoservice/test/2022-01-30_00-57-20_UTC_2.jpg',
        './holidaysphotoservice/test/2022-02-13_23-37-57_UTC_3.jpg',
        './mitulle_studio/test/2022-03-03_08-05-24_UTC_1.jpg',
        './mitulle_studio/test/2022-03-03_08-05-24_UTC_3.jpg',
        './photostudiochelsea2524/test/2022-02-20_12-53-23_UTC_6.jpg',
        './photostudiochelsea2524/test/2022-03-14_14-36-49_UTC_3.jpg',
        ]:
        # 解析データを保存
        feature = get_feature(fname)
        # 確認
        name, dist= get_nearest(feature_list, feature)
        print(fname, name, dist)
        ret += '[' + fname + ' ' + name + ' ' + str(dist) + ']\n'

    return ret


if __name__ == '__main__':
  print('@@ Flask起動 開始')
  app.run(debug=True)
  print('@@ Flask起動 完了')
