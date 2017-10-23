import dlib
from skimage import io
from scipy.spatial import distance
from os import listdir
from os.path import join
import sys
from functools import partial

COEF = 0.6

sp = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
facerec = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')
detector = dlib.get_frontal_face_detector()


def get_descriptors(photo_path):
    img = io.imread(photo_path)
    dets = detector(img, 1)
    for d in dets:
        shape = sp(img, d)
        yield facerec.compute_face_descriptor(img, shape)


if __name__ == '__main__':
    main_photo = (sys.argv[1:2] or [None])[0] or "webka.jpg"
    photo_dir = (sys.argv[2:3] or [None])[0] or "photos"

    main_descr = next(get_descriptors(main_photo))

    with open('text.txt', 'w', encoding='utf-8') as f:
        for photo_path in map(partial(join, photo_dir), listdir(photo_dir)):
            if min(map(partial(distance.euclidean, main_descr), get_descriptors(photo_path))) <= COEF:
                print(photo_path, file=f)
