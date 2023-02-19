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

    video = cv2.VideoCapture('image.jpg')
    # while cv2.waitKey(1) < 0:
    hasFrame, frame = video.read()

    resultImg, faceBoxes = highlightFace(faceNet, frame)
    if not faceBoxes:
        print("No face detected")
        gender = "Male"
        age = "25-32"
        status = 400

    if faceBoxes:
        print('sone ja raha ')
        status = 200
        print('uth gaya')

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

    os.system(
        "python3 code/morphinit.py --img1 image.jpg --img2 edawrd.png --output output.mp4")

    response = jsonify({"status": status, "gender": gender, "age": age})

    return response


if __name__ == '__main__':
    app.run(port=8000, debug=True)
