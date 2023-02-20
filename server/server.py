from flask import Flask, request, jsonify, send_from_directory
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

import dlib
import face_recognition

# Load the celebrity database
celeb_database = [
    {'id': 1, 'name': 'Acharya JB', 'photo': 'face/Acharya-JB.jpg',
        'gender': 'Male', 'encoding': None},
    {'id': 2, 'name': 'Aruna Asaf Ali', 'photo': 'face/Aruna-Asaf-Ali.jpg',
        'gender': 'Female', 'encoding': None},
    {'id': 3, 'name': 'Ashfaqullah Khan', 'photo': 'face/Ashfaqullah-Khan.jpg',
        'gender': 'Male', 'encoding': None},
    {'id': 4, 'name': 'Bal Gangadhar Tilak ', 'photo': 'face/Bal-Gangadhar-Tilak.jpg',
        'gender': 'Male', 'encoding': None},
    {'id': 5, 'name': 'Begum Hazrat Mahal ', 'photo': 'face/Begum-Hazrat-Mahal.jpg',
        'gender': 'Female', 'encoding': None},
    {'id': 6, 'name': 'Bhagat Singh', 'photo': 'face/Bhagat-Singh.jpg',
        'gender': 'Male', 'encoding': None},
    {'id': 7, 'name': 'Bina Das', 'photo': 'face/Bina-Das.jpg',
        'gender': 'Female', 'encoding': None},
    {'id': 8, 'name': 'Bipin Chandra Pal', 'photo': 'face/Bipin-Chandra-Pal.jpg',
        'gender': 'Male', 'encoding': None},
    {'id': 9, 'name': 'C Rajagopalachari', 'photo': 'face/C-Rajagopalachari.jpg',
        'gender': 'Male', 'encoding': None},
    {'id': 10, 'name': 'Capt. Lakshmi Sehgal', 'photo': 'face/Capt-Lakshmi-Sehgal.jpg',
        'gender': 'Female', 'encoding': None},
    {'id': 11, 'name': 'Chandrashekhar Azad', 'photo': 'face/Chandrashekhar-Azad.jpg',
        'gender': 'Male', 'encoding': None},
    {'id': 12, 'name': 'Chittaranjan Das', 'photo': 'face/Chittaranjan-Das.jpg',
        'gender': 'Male', 'encoding': None},
    {'id': 13, 'name': 'Dr. Bhimrao Ambedkar', 'photo': 'face/Dr-Bhimrao-Ambedkar.jpg',
        'gender': 'Male', 'encoding': None},
    {'id': 14, 'name': 'Dr. Rajendra Prasad', 'photo': 'face/Dr-Rajendra-Prasad.jpg',
        'gender': 'Male', 'encoding': None},
    {'id': 15, 'name': 'Dr. Ram Manohar Lohia', 'photo': 'face/Dr-Ram-Manohar-Lohia.jpg',
        'gender': 'Male', 'encoding': None},
    {'id': 16, 'name': 'Durgavati Devi (Durga Bhabhi)', 'photo': 'face/Durgavati-Devi-(Durga-Bhabhi).jpg',
        'gender': 'Female', 'encoding': None},
    {'id': 17, 'name': 'Gopal Krishna Gokhale', 'photo': 'face/Gopal-Krishna-Gokhale.jpg',
        'gender': 'Male', 'encoding': None},
    {'id': 18, 'name': 'Govind Ballabh Pant', 'photo': 'face/Govind-Ballabh-Pant.jpg',
        'gender': 'Male', 'encoding': None},
    {'id': 19, 'name': 'Gurudev Rabindranath Tagore', 'photo': 'face/Gurudev-Rabindranath-Tagore.jpg',
        'gender': 'Male', 'encoding': None},
    {'id': 20, 'name': 'Jayaprakash Narayan', 'photo': 'face/Jayaprakash-Narayan.jpg',
        'gender': 'Male', 'encoding': None},
    {'id': 21, 'name': 'Kalpana Dutta', 'photo': 'face/Kalpana-Dutta.jpg',
        'gender': 'Female', 'encoding': None},
    {'id': 22, 'name': 'Kamladevi Chattopadhyay', 'photo': 'face/Kamladevi-Chattopadhyay.jpg',
        'gender': 'Female', 'encoding': None},
    {'id': 23, 'name': 'Kanaklata Barua', 'photo': 'face/Kanaklata-Barua.jpg',
        'gender': 'Female', 'encoding': None},
    {'id': 24, 'name': 'Kartar Singh Sarabha', 'photo': 'face/Kartar-Singh-Sarabha.jpg',
        'gender': 'Male', 'encoding': None},
    {'id': 25, 'name': 'Kasturba-Gandhi', 'photo': 'face/Kasturba-Gandhi.jpg',
        'gender': 'Female', 'encoding': None},
    {'id': 26, 'name': 'Lala Hardayal', 'photo': 'face/Lala-Hardayal.jpg',
        'gender': 'Male', 'encoding': None},
    {'id': 27, 'name': 'Lala Lajpat Rai', 'photo': 'face/Lala-Lajpat-Rai.jpg',
        'gender': 'Male', 'encoding': None},
    {'id': 28, 'name': 'Madam Bhikaji Cama', 'photo': 'face/Madam-Bhikaji-Cama.jpg',
        'gender': 'Female', 'encoding': None},
    {'id': 29, 'name': 'Madanlal Dhingra', 'photo': 'face/Madanlal-Dhingra.jpg',
        'gender': 'Male', 'encoding': None},
    {'id': 30, 'name': 'Mahatma Gandhi', 'photo': 'face/Mahatma-Gandhi.jpg',
        'gender': 'Male', 'encoding': None},
    {'id': 31, 'name': 'Maulana Abul Kalam Azad', 'photo': 'face/Maulana-Abul-Kalam-Azad.jpg',
        'gender': 'Male', 'encoding': None},
    {'id': 32, 'name': 'Motilal Nehru', 'photo': 'face/Motilal-Nehru.jpg',
        'gender': 'Male', 'encoding': None},
    {'id': 33, 'name': 'Netaji Subhas Chandra Bose', 'photo': 'face/Netaji-Subhas-Chandra-Bose.jpg',
        'gender': 'Male', 'encoding': None},
    {'id': 34, 'name': 'Pt. Deendayal Upadhyaya', 'photo': 'face/Pt-Deendayal-Upadhyaya.jpg',
        'gender': 'Male', 'encoding': None},
    {'id': 35, 'name': 'Pt. Madan Mohan Malaviya', 'photo': 'face/Pt-Madan-Mohan-Malaviya.jpg',
        'gender': 'Male', 'encoding': None},
    {'id': 36, 'name': 'Rajkumari Amrit Kaur', 'photo': 'face/Rajkumari-Amrit-Kaur.jpg',
        'gender': 'Female', 'encoding': None},
    {'id': 37, 'name': 'Ram Prasad Bismil', 'photo': 'face/Ram-Prasad-Bismil.jpg',
        'gender': 'Male', 'encoding': None},
    {'id': 38, 'name': 'Rani Gaindinliu', 'photo': 'face/Rani-Gaindinliu.jpg',
        'gender': 'Female', 'encoding': None},
    {'id': 39, 'name': 'Rani Lakshmi Bai', 'photo': 'face/Rani-Lakshmi-Bai.jpg',
        'gender': 'Female', 'encoding': None},
    {'id': 40, 'name': 'Rash Behari Bose', 'photo': 'face/Rash-Behari-Bose.jpg',
        'gender': 'Male', 'encoding': None},
    {'id': 41, 'name': 'Sardar Udham Singh', 'photo': 'face/Sardar-Udham-Singh.jpg',
        'gender': 'Male', 'encoding': None},
    {'id': 42, 'name': 'Sardar Vallabhbhai Patel', 'photo': 'face/Sardar-Vallabhbhai-Patel.jpg',
        'gender': 'Male', 'encoding': None},
    {'id': 43, 'name': 'Sarojini Naidu', 'photo': 'face/Sarojini-Naidu.jpg',
        'gender': 'Female', 'encoding': None},
    {'id': 44, 'name': 'Shri. Aurbindo Ghosh', 'photo': 'face/Shri-Aurbindo-Ghosh.jpg',
        'gender': 'Male', 'encoding': None},
    {'id': 45, 'name': 'Shyama Prasad Mukherjee', 'photo': 'face/Shyama-Prasad-Mukherjee.jpg',
        'gender': 'Male', 'encoding': None},
    {'id': 46, 'name': 'Shyamji Krishnavarma', 'photo': 'face/Shyamji-Krishnavarma.jpg',
        'gender': 'Male', 'encoding': None},
    {'id': 47, 'name': 'Subramanya Bharathi', 'photo': 'face/Subramanya-Bharathi.jpg',
        'gender': 'Male', 'encoding': None},
    {'id': 48, 'name': 'Sucheta Kriplani', 'photo': 'face/Sucheta-Kriplani.jpg',
        'gender': 'Female', 'encoding': None},
    {'id': 49, 'name': 'Swami Vivekanand', 'photo': 'face/Swami-vivekanand.jpg',
        'gender': 'Male', 'encoding': None},
    {'id': 50, 'name': 'Thakur Roshan Singh', 'photo': 'face/Thakur-Roshan-Singh.jpg',
        'gender': 'Male', 'encoding': None},
    {'id': 51, 'name': 'Vijay Lakshmi Pandit', 'photo': 'face/Vijay-Lakshmi-Pandit.jpg',
        'gender': 'Female', 'encoding': None},
    {'id': 52, 'name': 'Vinayak Damodar Savarkar', 'photo': 'face/Vinayak-Damodar-Savarkar.jpg',
        'gender': 'Male', 'encoding': None}
]

# Use dlib to detect faces in the celebrity photos and create encodings
for celeb in celeb_database:
    celeb_photo = cv2.imread(celeb['photo'])
    celeb_face_encoding = face_recognition.face_encodings(celeb_photo)[0]
    celeb['encoding'] = celeb_face_encoding


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


app = Flask(__name__, static_url_path='/static')
app.config['DEBUG'] = True
CORS(app)


# Serve the React app from the specified URL
@app.route('/')
def serve_react():
    return send_from_directory(app.static_folder, 'index.html')


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
        status = 200

    try:
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

            # Get the user's photo from a local file
            user_photo = cv2.imread('image.jpg')

            # Use face_recognition to detect the face in the user's photo
            user_face_encoding = face_recognition.face_encodings(user_photo)[0]

            sorted_celebs = [
                celeb for celeb in celeb_database if celeb['gender'] == gender]

            # Compare the user's face encoding to the celebrity encodings
            distances = []
            for celeb in sorted_celebs:
                distance = face_recognition.face_distance(
                    [celeb['encoding']], user_face_encoding)
                distances.append(distance)

            # Find the closest match and return the celebrity name
            closest_match_index = distances.index(min(distances))
            closest_match_name = sorted_celebs[closest_match_index]['name']
            closest_match_photo = sorted_celebs[closest_match_index]['photo']

        os.system(
            "python3 code/morphinit.py --img1 image.jpg --img2 " + closest_match_photo + " --output static/output.mp4")
    except:
        print("Something went wrong")
        gender = "Male"
        age = "25-32"
        status = 400

    response = jsonify(
        {"status": status, "name": closest_match_name, "gender": gender, "age": age, "result": str(min(distances))})

    return response


if __name__ == '__main__':
    app.run(port=8000, debug=True)
