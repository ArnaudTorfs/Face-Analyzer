import face_recognition
from PIL import Image
import numpy as np
from math import sqrt, ceil
import pickle
import FilesUtilities


class FaceRecognition:
    def __init__(self):
        self.known_faces_encodings = []
        self.known_faces_names = []

    def add_known_face(self, name, image_path):
        image = face_recognition.load_image_file(image_path)
        face_encoding = face_recognition.face_encodings(image)[0]
        self.known_faces_encodings.append(face_encoding)
        self.known_faces_names.append(name)

    def compare_faces(self, known_person_index, image_path):
        image = face_recognition.load_image_file(image_path)
        face_encodings = face_recognition.face_encodings(image)
        for face_encoding in face_encodings:
            results = face_recognition.compare_faces(self.known_faces_encodings[known_person_index], face_encoding)
            if results:
                return results
        return False

    def get_known_faces(self, image_path):
        faces = []

        image = face_recognition.load_image_file(image_path)
        face_encodings = face_recognition.face_encodings(image)
        for face_encoding in face_encodings:
            results = face_recognition.compare_faces(self.known_faces_encodings, face_encoding)
            index = 0
            for result in results:
                if result:
                    faces.append(self.known_faces_names[index])
                index += 1

        return faces


def get_faces_location(image_path):
    return face_recognition.face_locations(image_path)


def get_faces(image_path):
    faces = []
    image = face_recognition.load_image_file(image_path)
    face_locations = face_recognition.face_locations(image)

    for face_location in face_locations:
        top, right, bottom, left = face_location
        face_image = image[top:bottom, left:right]
        faces.append(Image.fromarray(face_image))
    return faces


def get_faces_from_multiples_images_on_1_image(imageList):
    faces = [[] for x in range(len(imageList))]
    number_of_faces = 0

    index = 0
    print_progress_bar(index, len(imageList), prefix='Progress:', suffix='Complete', length=50)
    for imagePath in imageList:
        image = face_recognition.load_image_file(imagePath)
        face_locations = face_recognition.face_locations(image)

        for face_location in face_locations:
            top, right, bottom, left = face_location
            face_image = image[top:bottom, left:right]
            faces[index].append(Image.fromarray(face_image))
            number_of_faces += 1

        index += 1
        print_progress_bar(index, len(imageList), prefix='Progress:', suffix='Complete', length=50)

    faces_per_line = ceil(sqrt(number_of_faces))
    face_width = 500
    width = faces_per_line * face_width
    final_array = np.zeros((width, width, 3), dtype=np.uint8)

    index = 0
    for picture in faces:
        for image in picture:
            image = image.resize((face_width, face_width))
            y = int((index / faces_per_line)) * face_width
            x = int((index % faces_per_line) * face_width)
            final_array[y:y + face_width, x:x + face_width] = image
            index += 1

    img = Image.fromarray(final_array, 'RGB')
    img.save('Results/faces.jpg')
    img.show()


class FolderFacesRecognitionObject:
    def __init__(self, location):
        try:
            self.face_recognition_object = pickle.load(open("face_recognizer.fr", "rb"))

        except FileNotFoundError:
            self.face_recognition_object = FaceRecognition()

        try:
            self.files_in_folder_info = pickle.load(open("files_in_folder_info.fr", "rb"))

        except FileNotFoundError:
            self.files_in_folder_info = []

        self.location = location

    def check_if_image_is_known(self, image_file):
        image_is_known = False

        for known_image in self.files_in_folder_info:
            image_file = FilesUtilities.get_file_name(image_file)
            if image_file == known_image.name:
                image_is_known = True
                break
        return image_is_known

    def check_if_name_is_known(self, name):
        if name in self.face_recognition_object.known_faces_names:
            return True
        else:
            return False

    def parse_images(self):
        files = FilesUtilities.get_files_in_directory(full_path=True, location=self.location)

        for file in files:
            file_name = FilesUtilities.get_file_name(file)
            if FilesUtilities.get_file_extension(file) in [".jpeg", ".jpg"]:
                image_is_known = self.check_if_image_is_known(file)
                if not image_is_known:
                    print(file)
                    faces = self.face_recognition_object.get_known_faces(file)
                    information = FilesUtilities.FaceFileObject(file_name, faces)
                    self.files_in_folder_info.append(information)

    def add_known_face(self, image_path):
        file_name = FilesUtilities.get_file_name(image_path)
        if not self.check_if_name_is_known(file_name):
            print(f'ADDED {file_name}')
            self.face_recognition_object.add_known_face(file_name, image_path)

    def add_know_faces_from_folder(self):
        location = FilesUtilities.get_folder_in_path(self.location, "KNOWN PEOPLES")
        files = FilesUtilities.get_files_in_directory(location=location)
        for file in files:
            file_name = FilesUtilities.get_file_name(file)
            if not self.check_if_name_is_known(file_name):
                print(f'ADDED {file_name}')
                self.face_recognition_object.add_known_face(file_name, file)

    def show_folders_face_information(self):
        width = 20
        for file in self.files_in_folder_info:
            file_name = FilesUtilities.get_file_name(file.name)
            FilesUtilities.print_char_line('-', width, True)
            print(file_name)
            if len(file.faces) == 0:
                print(f'    - NO KNOWN FACE')
            for face in file.faces:
                print(f'    - {face}')

    def save(self):
        pickle.dump(self.face_recognition_object, open("face_recognizer.fr", "wb"))
        pickle.dump(self.files_in_folder_info, open("files_in_folder_info.fr", "wb"))


# Print iterations progress
def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', print_end="\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=print_end)
    # Print New Line on Complete
    if iteration == total:
        print()
