# -*- coding: utf-8 -*-

from keras.preprocessing import image
from keras.applications.inception_resnet_v2 import InceptionResNetV2, preprocess_input, decode_predictions
import numpy as np
import pickle
import os
import json
import instaloader

DTFILE = '../../data.dat'
os.chdir('./static/studios')
#var = instaloader.Instaloader()

def save(filename, feature_list):
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


# 画像のダウンロード
def download(arg):
  try:
    print('<><>' + arg + '<><>')
    #var.download_profile(arg, profile_pic=False, fast_update=True)
    cmd = 'instaloader --no-videos --no-captions --no-metadata-json --no-compress-json --fast-update ' + arg
    returncode = os.system(cmd)
  except:
    pass

# 画像リスト作成
def makelist():
  try:
    feature_list = []
    path = './'
    filedirs = os.listdir(path)
    dirs = [f for f in filedirs if os.path.isdir(os.path.join(path, f))]
    for dir in dirs:
        filedirs = os.listdir('./' + dir)
        # jpgファイルの抽出
        files1 = [f for f in filedirs if f.endswith('.jpg')]
        # webpファイルの抽出
        files2 = [f for f in filedirs if f.endswith('.webp')]
        files1.extend(files2)
        # ソート
        files1.reverse()
        i = 0
        for file in files1:
          i += 1
          # 指定以上のファイル数になったらそれは削除
          if i >= 50:
            os.remove(path + dir + '/' + file)
            continue
          # 画像リスト作成
          print('解析中', dir, file)
          feature = get_feature(path + dir + '/' + file)
          feature_list.append([dir, feature])
    save(DTFILE, feature_list)
    print('学習ファイル作成 (' + len(feature_list) + ')件')
  except:
    pass

def alldownload():
  download('mitulle_studio')
  download('mitullephoto')
  download('holidaysphotoservice')
  download('cafune_photostudio')
  download('studiococoahitachi')
  download('studiococoamito')
  download('studiococoatsukuba')
  download('studiococoakashiwa')
  download('cocoainzai')
  download('cocoatokyofutakotamagawa')
  download('cocoanoborito')
  download('cocoashinkawasaki')
  download('studiococoakohoku')
  download('cocoashinyokohama')
  download('cocoayokohamakonan')
  download('cocoayokohamatotsuka')
  download('studiococoayamate')
  download('adamasnewbornphoto')
  download('photostudiochelsea2524')
  

alldownload()
# 学習済みデータをロード
model = InceptionResNetV2(weights='imagenet', include_top=False)
makelist()


'''
mitulle_studio          mitulle photo studio 月島店と有明店
mitullephoto            mitullephotostudio waterfront
holidaysphotoservice    家族写真スタジオ「Holidays」
studiococoahitachi      フォトスタジオCocoa日立店
studiococoamito         フォトスタジオcocoa水戸店
studiococoatsukuba      フォトスタジオcocoa つくば店
studiococoakashiwa      フォトスタジオCocoa柏マルイ店
cocoainzai              フォトスタジオCocoa印西店
cocoatokyofutakotamagawa    cocoa東京二子玉川店
cocoanoborito           フォトスタジオCocoa川崎登戸店
cocoashinkawasaki       フォトスタジオCocoa新川崎店
studiococoakohoku       フォトスタジオcocoa横浜港北店
cocoashinyokohama       フォトスタジオCocoa新横浜店
cocoayokohamakonan      フォトスタジオCocoa横浜港南店
cocoayokohamatotsuka    フォトスタジオCocoa横浜戸塚店
studiococoayamate       フォトスタジオcocoa横浜山手店
adamasnewbornphoto      AdAmAs newbornphoto
photostudiochelsea2524  フォトスタジオチェルシー
cafune_photostudio      Photo studio CAFUNÉ

'''