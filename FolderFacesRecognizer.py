import FaceRecognitionUtilities
import os
from argparse import ArgumentParser

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-p', "--path", type=str, nargs=1, help='Path of the folder to analyse')
    parser.add_argument("-a", "--add", action='store_true',
                        help="Add Known Faces from the Knows Faces Folder")

    parser.add_argument("-s", "--show", action='store_true',
                        help="Show the Faces Information of the folder")
    parser.add_argument("--analyse", action='store_true',
                        help="Analyse de face on the images in the current folder")

    args = parser.parse_args()

    if args.path is None:
        current_directory = os.getcwd()
    else:
        current_directory = args.path

    face_recognizer = FaceRecognitionUtilities.FolderFacesRecognitionObject(current_directory)

    if args.add and args.analyse:
        print("One action at the time please")
    else:
        if args.add:
            face_recognizer.add_know_faces_from_folder()

        if args.analyse:
            face_recognizer.parse_images()

        if args.show:
            face_recognizer.show_folders_face_information()

    face_recognizer.save()
