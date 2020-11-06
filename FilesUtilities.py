from glob import glob
import os
from pathlib import Path
import pathlib


def get_folders_in_directory(full_path=True, location=os.getcwd()):
    folders = []
    dir_path = location
    directories = glob(f"{dir_path}\\*")

    for folder in directories:
        if os.path.isdir(folder):
            path = ""
            if full_path:
                path = folder
            else:
                path = folder.split('\\')[-1]
            folders.append(path)

    return folders


def get_files_in_directory(full_path=True, location=os.getcwd(), file_type=""):
    files = []
    dir_path = location
    _path = Path(dir_path)
    directories = os.listdir(dir_path)

    print("")
    for file in directories:
        file = _path / file
        if os.path.isfile(file):
            if file_type != "":
                if file.endswith(file_type):
                    path = ""
                    if full_path:
                        path = _path / file
                    else:
                        path = file
                    files.append(path)
            else:
                if full_path:
                    path = _path / file
                else:
                    path = file
                files.append(path)

    return files


def rename_file(path, new_name):
    file_type = path.split('.')[-1]
    parent = str(Path(path).parent)
    new_path = parent + "//" + new_name + "." + file_type
    os.rename(path, new_path)


def get_file_extension(file_path):
    return pathlib.Path(file_path).suffix


def get_file_name(file_path, extension=False):
    if extension:
        return pathlib.Path(file_path).name
    else:
        return pathlib.Path(file_path).name.split('.')[0]


def get_folder_in_path(path, folder_name):
    return pathlib.Path(path) / folder_name


def print_char_line(char, amount, end_line):
    for x in range(amount):
        print(char, end='')
    if end_line:
        print("")


class FaceFileObject:
    def __init__(self, _name, _faces):
        self.name = _name
        self.faces = _faces
