from unittest import result
from keras_vggface.utils import preprocess_input
from keras_vggface.vggface import VGGFace
from src.utils.all_utils import read_yaml,  create_dir
import pickle
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st
from PIL import Image
import os
import cv2
from mtcnn import MTCNN
import numpy as np
import base64
from static.load_css import local_css


local_css("static/style.css")


def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    body {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)


set_background('artifacts/images.jpg')


config = read_yaml("config/config.yaml")
params = read_yaml('params.yaml')

artifacts = config['artifacts']
artifacts_dirs = artifacts['artifacts_dir']

upload_image_dir = artifacts['upload_image_dir']
upload_path = os.path.join(artifacts_dirs, upload_image_dir)

pickle_format_dirs = artifacts['pickle_format_data_dir']
img_pickle_file_name = artifacts['img_pickle_file_name']
pickle_actor_name = artifacts['pickle_actor_names']

pickle_dir_path = os.path.join(artifacts_dirs, pickle_format_dirs)
pickle_file = os.path.join(pickle_dir_path, img_pickle_file_name)
pickle_actor = os.path.join(pickle_dir_path, pickle_actor_name)

feature_extractor_dir = artifacts['feature_extraction_dir']
extracted_feature_name = artifacts['extracted_features_name']

feature_extractor_path = os.path.join(artifacts_dirs, feature_extractor_dir)
feature_name = os.path.join(feature_extractor_path, extracted_feature_name)

data = params['base']['data_path']

model_name = params['base']['BASE_MODEL']
include_top = params['base']['include_top']
pooling = params['base']['pooling']

detector = MTCNN()
model = VGGFace(model=model_name, include_top=include_top,
                input_shape=(244, 244, 3), pooling=pooling)

filenames = pickle.load(open(pickle_file, 'rb'))
feature_list = pickle.load(open(feature_name, 'rb'))
actor_names = pickle.load(open(pickle_actor, 'rb'))


def extracted_features(img_path, model, detector):
    img = cv2.imread(img_path)
    result = detector.detect_faces(img)

    x, y, width, heigth = result[0]['box']
    face = img[y:y+heigth, x:x+width]
    image = Image.fromarray(face)
    image = image.resize((244, 244))

    face_array = np.asarray(image)
    face_array = face_array.astype('float32')

    expanded_img = np.expand_dims(face_array, axis=0)
    preprocess_img = preprocess_input(expanded_img)
    result = model.predict(preprocess_img).flatten()

    return result


def recommed(feature_list, features):
    similarity = []
    for i in range(len(feature_list)):
        similarity.append(cosine_similarity(features.reshape(
            1, -1), feature_list[i].reshape(1, -1))[0][0])

    result = sorted(list(enumerate(similarity)),
                    reverse=True, key=lambda x: x[1])[0]
    index_pos = result[0]
    percentage = result[1]

    return index_pos, percentage


def save_upload_image(upload_image):
    try:
        create_dir([upload_path])
        with open(os.path.join(upload_path, upload_image.name), 'wb') as f:
            f.write(upload_image.getbuffer())
        return True
    except:
        return False


main_title = "<center><div><p class='highlight grey' style='font-size:47px'><span class='bold'>Guess your look alike celebrity</span></span></div></center>"
st.markdown(main_title, unsafe_allow_html=True)


uploaded_image = st.file_uploader('Choose a image')
if uploaded_image is not None:
    if save_upload_image(uploaded_image):

        display_image = Image.open(uploaded_image)
        resized_display_img = display_image.resize((260, 320), Image.ANTIALIAS)

        upload_image_path = os.path.join(upload_path, uploaded_image.name)
        features = extracted_features(upload_image_path, model, detector)
        img_path, percentage = recommed(feature_list, features)
        actor_path = filenames[img_path]

        predicted_actor = " ".join(actor_path.split('\\')[2].split('_'))

        actor_root_name = actor_path.split('\\')[2]
        pred_actor_path = os.path.join(data, actor_root_name, '1.jpg')

        pred_actor_image = Image.open(pred_actor_path)
        resized_actor_img = pred_actor_image.resize(
            (260, 320), Image.ANTIALIAS)

        st.header(
            f'You look like {predicted_actor} with {np.round(percentage*100,0)}% similarity')

        col1, col2 = st.beta_columns(2)

        with col1:
            st.markdown("Thats you")
            st.image(resized_display_img)

        with col2:
            st.markdown("Your look alike celelb")
            st.image(resized_actor_img)
