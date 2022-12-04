import os
import math


def split_file(file_name, size_limit):
    if size_limit <= 0:
        return

    file_size = os.stat(file_name).st_size
    if file_size <= size_limit:
        return

    only_file_name = os.path.basename(file_name)
    file_name_without_extension, file_extension = os.path.splitext(only_file_name)

    folder_id = 1
    result_path = f"ravaillac_result/splits/{only_file_name}_{int(size_limit)}B"
    while os.path.exists(result_path):
        result_path = f"ravaillac_result/splits/{only_file_name}_{int(size_limit)}B-{folder_id}"
        folder_id += 1

    os.makedirs(result_path)

    splits = math.ceil(file_size / size_limit)

    with open(file_name, "rb") as file:
        file_value = file.read()

    fragment_size = file_size // splits

    i = 0
    fragment_number = 1
    while i <= len(file_value) - fragment_size:
        with open(f"{result_path}/{file_name_without_extension}--fragment{fragment_number}{file_extension}",
                  "wb") as fragment:
            fragment.write(file_value[i:i + fragment_size])

        i += fragment_size
        fragment_number += 1

    # we treat the rest
    # <=> if file_size % splits > 0
    if i != len(file_value):
        with open(f"{result_path}/{file_name_without_extension}--fragment{fragment_number}{file_extension}",
                  "wb") as fragment:
            fragment.write(file_value[i:len(file_value)])

    return result_path


def merge_fragments(path):
    fragments = os.listdir(path)
    fragments.sort(key=lambda x: int(x.split("--fragment", 1)[1].split(".", 1)[0]))

    for fragment_name in fragments:
        with open(os.path.join(path, fragment_name), "rb") as fragment:
            fragment_value = fragment.read()

        fragment_name_without_extension, fragment_extension = os.path.splitext(fragment_name)

        with open(fragment_name_without_extension.split("--fragment", 1)[0] + fragment_extension, "ab") as original_file:
            original_file.write(fragment_value)
