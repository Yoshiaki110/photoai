from keras.preprocessing import image
from keras.applications.mobilenet import MobileNet, preprocess_input, decode_predictions
import numpy as np

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

feature_list = []
model = MobileNet(weights='imagenet', include_top=False)

for fname in ['elephant01.jpg', 'elephant02.jpg', 'elephant03.jpg','giraffe01.jpg', 'giraffe02.jpg', 'giraffe03.jpg']:
    feature = get_feature(fname)
    feature_list.append([fname,feature])

feature = get_feature('elephant04.jpg')
name, dist= get_nearest(feature_list, feature)

print(name, dist)
