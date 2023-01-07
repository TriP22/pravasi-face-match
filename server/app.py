import numpy as np
from PIL import Image
# import pickle
import matplotlib.pyplot as plt
import os

# https://gist.github.com/EncodeTS/6bbe8cb8bebad7a672f0d872561782d9
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


input_img_path = 'me.jpg'
encoding = img_to_encoding(input_img_path)
closest_person = find_closest(encodings, encoding)
closest_similarity = 1 - distance(closest_person['encoding'], encoding)
plot_images([input_img_path, closest_person['path']])
print('found '+closest_person['name']+' with ' +
      str(closest_similarity)+' similarity')
