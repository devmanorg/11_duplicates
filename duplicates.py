import sys
import pathlib
import os
import argparse
import logging
import operator
import itertools


VERBOSITY_TO_LOGGING_LEVELS = {
    0: logging.WARNING,
    1: logging.INFO,
    2: logging.DEBUG,
}


class File:

    def __init__(self, path):
        self._path = path

    @property
    def f_name(self):
        return self._path.name.lower()

    @property
    def f_path(self):
        return str(self._path)

    @property
    def f_size(self):
        return os.stat(str(self._path)).st_size

    @property
    def duplicate_indicator(self):
        return '{}{}'.format(self.f_name, self.f_size)


class FilesCollection(list):

    def __init__(self, *args):
        super(FilesCollection, self).__init__(args)

    def grouped_by_file_name_and_size(self):
        get_attr = operator.attrgetter('duplicate_indicator')
        return [list(g) for k, g in itertools.groupby(
            sorted(self, key=get_attr), get_attr
        )]


def get_list_of_files(path, list_of_files):
    try:
        if path.is_dir() and os.listdir(str(path)):
            for child in path.iterdir():
                get_list_of_files(child, list_of_files)
        elif path.is_file():
            list_of_files.append(File(path))
    except PermissionError:
        logging.error("Skipping, as Access denied to the path: ".format(path))
    return list_of_files


def is_correct_path(directory):
    if directory:
        return pathlib.Path(directory).exists()
    return False


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', '-v', action='count', default=0)
    parser.add_argument('--directory', '-d', default=None)
    args = parser.parse_args()
    logging_level = VERBOSITY_TO_LOGGING_LEVELS[args.verbose]

    logging.basicConfig(level=logging_level)

    if not is_correct_path(args.directory):
        logging.error(
            "Specified path is not correct: {dir}".format(dir=args.directory)
        )
        sys.exit(1)

    files_collection = FilesCollection()

    collected_files = get_list_of_files(
        pathlib.Path(args.directory), files_collection
    )
    if not collected_files:
        logging.error("no files found in the specified path")
        sys.exit(1)

    list_of_files_grouped_by_duplicate_indicator = collected_files.\
        grouped_by_file_name_and_size()

    for group_of_file in list_of_files_grouped_by_duplicate_indicator:
        if len(group_of_file) > 1:
            logging.info(
                "following files are duplicates: {duplicated_files}".format(
                    duplicated_files=", ".join(
                        [_file.f_path for _file in group_of_file]
                    )
                )
            )
