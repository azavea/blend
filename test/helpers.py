import os

def create_test_files(paths_to_files):
    if isinstance(paths_to_files, basestring):
        internal_paths_to_files = [paths_to_files]
    else:
        internal_paths_to_files = paths_to_files
    for path_to_file in internal_paths_to_files:
        if not os.path.exists(path_to_file):
            if os.path.dirname(path_to_file) != '' and not os.path.exists(os.path.dirname(path_to_file)):
                os.makedirs(os.path.dirname(path_to_file))
            open(path_to_file, 'w').close()

def create_test_file_with_content(path_to_test_file, content):
    create_test_files(path_to_test_file)
    f = open(path_to_test_file, 'w')
    try:
        f.write(content)
    finally:
        f.close()

def clean_up_test_files(paths_to_files):
    if isinstance(paths_to_files, basestring):
        internal_paths_to_files = [paths_to_files]
    else:
        internal_paths_to_files = paths_to_files
    for path_to_file in internal_paths_to_files:
        if os.path.exists(path_to_file):
            os.remove(path_to_file)