import os
from keras.preprocessing import image
from keras.applications.inception_resnet_v2 import InceptionResNetV2, preprocess_input, decode_predictions
import numpy as np
import pickle

DTFILE = 'data.dat'

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
feature_list = load(DTFILE)
# 学習済みデータをロード
model = InceptionResNetV2(weights='imagenet', include_top=False)
# 画像を解析
#makelist(feature_list)
#save(DTFILE)

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
