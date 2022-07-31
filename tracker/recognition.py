from math import sqrt
from os import listdir
from pickle import dump

from face_recognition import face_locations, face_encodings, load_image_file
from sklearn.neighbors import KNeighborsClassifier

knn_clf: KNeighborsClassifier


def get_nbr_photos() -> int:
    try:
        return len(listdir('static/photos'))
    except Exception as e:
        print(e)
        return 0


def get_dataset():
    dataset = [[], []]
    for photo in listdir('static/photos'):
        photo_file = load_image_file(f'static/photos/{photo}')
        locations = face_locations(photo_file)
        if len(locations) != 1:
            print(f'Photo should have one exact face, skipping photo at {photo}')
            continue
        dataset[0].append(face_encodings(photo_file, known_face_locations=locations)[0])
        dataset[1].append(photo.split('_')[0])
    return dataset


def train():
    global knn_clf
    encodings, labels = get_dataset()
    n_neighbors = int(round(sqrt(len(encodings))))

    # Create and train the KNN classifier
    knn_clf = KNeighborsClassifier(n_neighbors=n_neighbors, algorithm='ball_tree', weights='distance')
    knn_clf.fit(encodings, labels)

    # Save the trained KNN classifier
    with open('static/model', 'wb') as f:
        dump(knn_clf, f)


def predict(paths, distance_threshold=0.6):
    global knn_clf
    res = []
    for path in paths:
        photo_file = load_image_file(path)
        locations = face_locations(photo_file)
        if len(locations) != 1:
            print(f'Photo should have one exact face')
            continue
        encodings = face_encodings(photo_file, known_face_locations=locations)[0]
        closest_distances = knn_clf.kneighbors(encodings, n_neighbors=1)
        are_matches = closest_distances[0][0][0] <= distance_threshold

        res.append([(pred, loc) if rec else ("unknown", loc) for pred, loc, rec in
                    zip(knn_clf.predict(encodings), locations, are_matches)])
    return res
