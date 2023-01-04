from fileinput import filename
from sklearn import preprocessing
from utils.all_utils import read_yaml, create_dir
import os
import pickle
from tensorflow.keras.preprocessing import image
from keras_vggface.utils import preprocess_input
from keras_vggface.vggface import VGGFace
import numpy as np
from tqdm import tqdm
from PIL import Image


def extractor(img_path, model):
    img = Image.open(img_path)
    resized_img = img.resize((244, 244), Image.ANTIALIAS)
    img_array = image.img_to_array(resized_img)

    expanded_img = np.expand_dims(img_array, axis=0)
    preproecess_img = preprocess_input(expanded_img)

    reselt = model.predict(preproecess_img).flatten()
    return reselt

def feature_extraction(config_path, params_path):
    config = read_yaml(config_path)
    params = read_yaml(params_path)

    artifacts = config['artifacts']
    artifacts_dirs = artifacts['artifacts_dir']
    pickle_format_dirs = artifacts['pickle_format_data_dir']
    img_pickle_filename = artifacts['img_pickle_file_name']


    img_pickle_filename = os.path.join(artifacts_dirs, pickle_format_dirs, img_pickle_filename)
    filename = pickle.load(open(img_pickle_filename, 'rb'))



    feature_dir = artifacts['feature_extraction_dir']
    feature_pickle_filename = artifacts['extracted_features_name']

    create_dir([os.path.join(artifacts_dirs, feature_dir)])
        

    model_name = params['base']['BASE_MODEL']
    include_top = params['base']['include_top']
    pooling = params['base']['pooling']
     
    model = VGGFace(model= model_name, include_top= include_top,input_shape= (244,244,3), pooling = pooling)

    features = []

    for file in tqdm(filename):
        features.append(extractor(file, model))
        
    
    feature_path = os.path.join(artifacts_dirs, feature_dir, feature_pickle_filename)
    pickle.dump(features, open(feature_path, 'wb'))
    

if __name__ == '__main__':
    feature_extraction('config/config.yaml', 'params.yaml')