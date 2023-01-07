from flask import Flask, request, jsonify
from flask_cors import CORS,  cross_origin
import os
from time import sleep
import random

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

from vggFaceModel import vgg_face

model = vgg_face('vggFace/vgg_face_weights.h5')
print(model.summary())


def reshapeImage(path):
    im = Image.open(path)
    im = im.resize((224, 224))
    im = np.array(im).astype(np.float32) / 255
    im = np.expand_dims(im, axis=0)
    return im


def img_to_encoding(path):
    im = reshapeImage(path)
    out = model.predict(im)
    return out


def distance(encoding1, endcoding2):
    return np.linalg.norm(encoding1 - endcoding2)


def triplet_loss(anchor, postive, negative, margin=0.2):
    loss = (distance(anchor, postive)**2) - \
        (distance(anchor, negative)**2) + margin
    loss = max(loss, 0)
    return loss


def find_closest(database, encoding):
    lowest_similarity = 100
    closest_person = None
    for person in database:
        current_similarity = distance(person['encoding'], encoding)
        if current_similarity < lowest_similarity:
            closest_person = person
            lowest_similarity = current_similarity
    return closest_person


faces_dir = os.listdir('./faces')
names = [name.strip('.jpg').replace('-', ' ') for name in faces_dir]
encodings = []
for i in range(len(names)):
    path = f'faces/{faces_dir[i]}'
    encoding = img_to_encoding(path)
    encodings.append({
        "name": names[i],
        "path": path,
        "encoding": encoding
    })


def plot_images(paths):
    f, axarr = plt.subplots(1, len(paths))
    for i in range(len(paths)):
        axarr[i].imshow(Image.open(paths[i]))


app = Flask(__name__)
app.config['DEBUG'] = True
CORS(app, origins=['http://127.0.0.1:3000', 'http://localhost:3000'])


@app.route('/api/v1/user', methods=['POST'])
def create_user():

    file = request.files['file']
    file.save(os.path.join(os.getcwd(), "me.jpg"))

    sleep(2)

    input_img_path = 'me.jpg'
    encoding = img_to_encoding(input_img_path)
    closest_person = find_closest(encodings, encoding)
    closest_similarity = 1 - distance(closest_person['encoding'], encoding)
    plot_images([input_img_path, closest_person['path']])
    print('found '+closest_person['name']+' with ' +
          str(closest_similarity)+' similarity')

    # validate and save user to database
    faces_dir = os.listdir('./faces')
    names = [name.strip('.jpg').replace('-', ' ') for name in faces_dir]

    response = jsonify(
        {"name": closest_person['name'], "similarity": closest_similarity, "random_name": names[random.randint(0, 19)]})
    return response


if __name__ == '__main__':
    app.run()
