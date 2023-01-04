from utils.all_utils import read_yaml, create_dir
import os
import pickle
from mtcnn import MTCNN
from tensorflow.keras.preprocessing import image
from tqdm import tqdm
import cv2


def extract_face_from_image(image_path, required_size=(224, 224)):
    img = cv2.imread(image_path)

    detector = MTCNN()
    faces = detector.detect_faces(img)
    if len(faces) > 0:

        x, y, width, height = faces[0]['box']
        face_boundary = img[y:y + height, x:x+width]

        image = cv2.resize(face_boundary, required_size)
        return image


def generate_image_pickle_file(config_path, params_path):
    config = read_yaml(config_path)
    params = read_yaml(params_path)

    artifacts = config['artifacts']
    artifacts_dir = artifacts['artifacts_dir']
    pickle_format_dir = artifacts['pickle_format_data_dir']
    img_pickle_filename = artifacts['img_pickle_file_name']
    pickle_actors_name = artifacts['pickle_actor_names']
    cropped_dir = artifacts['cropped_dir']

    raw_local_dir_path = os.path.join(artifacts_dir, pickle_format_dir)

    create_dir([raw_local_dir_path])

    pickle_file = os.path.join(raw_local_dir_path, img_pickle_filename)
    pickle_actor = os.path.join(raw_local_dir_path, pickle_actors_name)

    data = params['base']['data_path']
    create_dir([os.path.join(data, cropped_dir)])

    actors = os.listdir(data)
    filenames = []

    for actor in tqdm(actors):
        count = 0
        actor_crop_dir = os.path.join(data, cropped_dir, actor)
        create_dir([actor_crop_dir])

        for file in os.listdir(os.path.join(data, actor)):
            file_dir = os.path.join(data, actor, file)

            try:
                detected_face = extract_face_from_image(file_dir)
                cropped_file_name = actor + "_" + str(count) + ".jpg"

                cv2.imwrite(os.path.join(actor_crop_dir,
                            cropped_file_name), detected_face)
                count += 1
            except:
                pass

        for file in os.listdir(actor_crop_dir):
            filenames.append(os.path.join(data, cropped_dir, actor, file))

    print(f'Total celeb are: {len(actors)}')
    print(f'Total celeb images: {len(filenames)}')

    pickle.dump(filenames, open(pickle_file, 'wb'))
    pickle.dump(actors, open(pickle_actor, 'wb'))


if __name__ == '__main__':
    generate_image_pickle_file('config/config.yaml', 'params.yaml')
