from flask import Flask, request, jsonify
from flask_cors import CORS,  cross_origin
import os
from time import sleep
import random
import base64
from io import BytesIO
from base64 import b64decode
import imghdr


import numpy as np
from PIL import Image
import matplotlib.pyplot as plt


import cv2
import math
import argparse


def highlightFace(net, frame, conf_threshold=0.7):
    frameOpencvDnn = frame.copy()
    frameHeight = frameOpencvDnn.shape[0]
    frameWidth = frameOpencvDnn.shape[1]
    blob = cv2.dnn.blobFromImage(frameOpencvDnn, 1.0, (300, 300), [
                                 104, 117, 123], True, False)

    net.setInput(blob)
    detections = net.forward()
    faceBoxes = []
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > conf_threshold:
            x1 = int(detections[0, 0, i, 3]*frameWidth)
            y1 = int(detections[0, 0, i, 4]*frameHeight)
            x2 = int(detections[0, 0, i, 5]*frameWidth)
            y2 = int(detections[0, 0, i, 6]*frameHeight)
            faceBoxes.append([x1, y1, x2, y2])
            cv2.rectangle(frameOpencvDnn, (x1, y1), (x2, y2),
                          (0, 255, 0), int(round(frameHeight/150)), 8)
    return frameOpencvDnn, faceBoxes


faceProto = "opencv_face_detector.pbtxt"
faceModel = "opencv_face_detector_uint8.pb"
ageProto = "age_deploy.prototxt"
ageModel = "age_net.caffemodel"
genderProto = "gender_deploy.prototxt"
genderModel = "gender_net.caffemodel"


MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
ageList = ['(0-2)', '(4-6)', '(8-12)', '(15-20)',
           '(25-32)', '(38-43)', '(48-53)', '(60-100)']
genderList = ['Male', 'Female']

faceNet = cv2.dnn.readNet(faceModel, faceProto)
ageNet = cv2.dnn.readNet(ageModel, ageProto)
genderNet = cv2.dnn.readNet(genderModel, genderProto)

padding = 20


# from vggFaceModel import vgg_face

# model = vgg_face('vggFace/vgg_face_weights.h5')
# print(model.summary())


# def reshapeImage(path):
#     im = Image.open(path)
#     im = im.resize((224, 224))
#     im = np.array(im).astype(np.float32) / 255
#     im = np.expand_dims(im, axis=0)
#     return im


# def img_to_encoding(path):
#     im = reshapeImage(path)
#     out = model.predict(im)
#     return out


# def distance(encoding1, endcoding2):
#     return np.linalg.norm(encoding1 - endcoding2)


# def triplet_loss(anchor, postive, negative, margin=0.2):
#     loss = (distance(anchor, postive)**2) - \
#         (distance(anchor, negative)**2) + margin
#     loss = max(loss, 0)
#     return loss


# def find_closest(database, encoding):
#     lowest_similarity = 100
#     closest_person = None
#     for person in database:
#         current_similarity = distance(person['encoding'], encoding)
#         if current_similarity < lowest_similarity:
#             closest_person = person
#             lowest_similarity = current_similarity
#     return closest_person


# faces_dir = os.listdir('./faces')
# names = [name.strip('.jpg').replace('-', ' ') for name in faces_dir]
# encodings = []
# for i in range(len(names)):
#     path = f'faces/{faces_dir[i]}'
#     encoding = img_to_encoding(path)
#     encodings.append({
#         "name": names[i],
#         "path": path,
#         "encoding": encoding
#     })


# def plot_images(paths):
#     f, axarr = plt.subplots(1, len(paths))
#     for i in range(len(paths)):
#         axarr[i].imshow(Image.open(paths[i]))


app = Flask(__name__)
app.config['DEBUG'] = True
CORS(app)


@app.route('/api/v1/user', methods=['POST'])
def create_user():

    # Get the image data from the request
    image_data = request.form['image']

    # Remove the substring from the original string
    modified_string = image_data.replace('data:image/jpeg;base64,', '')

    # Decode the image data
    decoded_data = base64.b64decode(modified_string)

    # Get the current directory of the Flask script
    script_dir = os.path.dirname(__file__)

    # Save the file to the current directory of the Flask script
    with open(os.path.join(script_dir, 'image.jpg'), 'wb') as f:
        f.write(decoded_data)
        f.close()

    print('sone ja raha ')
    sleep(5)
    print('uth gaya')

    video = cv2.VideoCapture('image.jpg')
    while cv2.waitKey(1) < 0:
        hasFrame, frame = video.read()
        if not hasFrame:
            cv2.waitKey()
            break

        resultImg, faceBoxes = highlightFace(faceNet, frame)
        if not faceBoxes:
            print("No face detected")
            gender = "Male"
            age = "25-32"

        for faceBox in faceBoxes:
            face = frame[max(0, faceBox[1]-padding):
                         min(faceBox[3]+padding, frame.shape[0]-1), max(0, faceBox[0]-padding):min(faceBox[2]+padding, frame.shape[1]-1)]

            blob = cv2.dnn.blobFromImage(
                face, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
            genderNet.setInput(blob)
            genderPreds = genderNet.forward()
            gender = genderList[genderPreds[0].argmax()]
            print(f'Gender: {gender}')

            ageNet.setInput(blob)
            agePreds = ageNet.forward()
            age = ageList[agePreds[0].argmax()]
            print(f'Age: {age[1:-1]} years')

    # # input_img_path = 'me.jpg'
    # input_img_path = 'image.jpg'
    # encoding = img_to_encoding(input_img_path)
    # closest_person = find_closest(encodings, encoding)
    # closest_similarity = 1 - distance(closest_person['encoding'], encoding)
    # plot_images([input_img_path, closest_person['path']])
    # print('found '+closest_person['name']+' with ' +
    #       str(closest_similarity)+' similarity')

    # # validate and save user to database
    faces_dir = os.listdir('./faces')
    names = [name.strip('.jpg').replace('-', ' ') for name in faces_dir]

    response = jsonify(
        # {"name": closest_person['name'], "similarity": closest_similarity, "random_name": names[random.randint(0, 19)]})
        {"gender": gender, "age": age, "random_name": names[random.randint(0, 19)]})
    return response


if __name__ == '__main__':
    app.run()
