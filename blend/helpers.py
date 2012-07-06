import os


def first_file_name_in_path_matching_regex(path, regex):
    if os.path.exists(path):
        for file_name in os.listdir(path):
            if regex.match(file_name):
                return os.path.join(path, file_name)
    return None
