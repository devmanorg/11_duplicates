import sys
import pathlib
import os
from collections import Counter


def get_list_of_files_info(path, files_list):
    try:
        if path.is_dir() and os.listdir(str(path)):
            for child in path.iterdir():
                get_list_of_files_info(child, files_list)
        elif path.is_file():
            files_list.append(('{}{}'.format(
                path.name.lower(), os.stat(str(path)).st_size
            ), str(path)))
    except PermissionError:
        print("Skipping, as Access denied to the path: ".format(path))
    return files_list


def validate_path_from_input():
    path_to_folder = None
    try:
        path_to_folder = pathlib.Path(sys.argv[1])
    except IndexError:
        return "please provide path to folder. " \
               "Example: python duplicates.py <path_to_folder>", None
    except OSError:
        return "Specified input {} is not a correct path".format(
            path_to_folder
        ), None
    if not path_to_folder.exists():
        return "Specified path {} does not exist ".format(
            path_to_folder
        ), None
    return None, path_to_folder


def get_duplicated_files(files_list):
    same_files_counter = Counter([file[0] for file in files_list])
    total_list_of_duplicates = []
    for filename_to_size_key, counter in same_files_counter.items():
        if counter > 1:
            total_list_of_duplicates.append(
                [file[1] for file in files_list
                 if file[0] == filename_to_size_key]
            )
    return total_list_of_duplicates

if __name__ == '__main__':
    list_of_collect_files = []
    error, path_to_folder = validate_path_from_input()
    if error:
        print(error)
        sys.exit(1)
    files_list = get_list_of_files_info(path_to_folder, list_of_collect_files)
    if not files_list:
        print("no files found in the specified path")
        sys.exit(1)
    duplicated_files = get_duplicated_files(files_list)
    if not duplicated_files:
        print("duplicated files not found in the specified folder")
        sys.exit(1)
    for duplicated_files_chain in duplicated_files:
        print(
            "following files are duplicates: {}".format(duplicated_files_chain)
        )
