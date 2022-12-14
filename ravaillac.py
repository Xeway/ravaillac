import os
import math


def split_file(file_path, size_limit):
    if size_limit <= 0:
        return

    file_size = os.stat(file_path).st_size
    if file_size <= size_limit:
        return

    file_name = os.path.basename(file_path)
    file_name_without_extension, file_extension = os.path.splitext(file_name)

    directory_id = 1
    result_path = f"ravaillac_result/fragments/{file_name}_{int(size_limit)}B"
    while os.path.exists(result_path):
        result_path = f"ravaillac_result/fragments/{file_name}_{int(size_limit)}B-{directory_id}"
        directory_id += 1

    os.makedirs(result_path)

    splits = math.ceil(file_size / size_limit)

    with open(file_path, "rb") as file:
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


def merge_fragments(directory_path):
    fragments = os.listdir(directory_path)
    fragments.sort(key=lambda x: int(x.split("--fragment", 1)[1].split(".", 1)[0]))

    for fragment_name in fragments:
        with open(os.path.join(directory_path, fragment_name), "rb") as fragment:
            fragment_value = fragment.read()

        fragment_name_without_extension, fragment_extension = os.path.splitext(fragment_name)

        result_path = fragment_name_without_extension.split("--fragment", 1)[0] + fragment_extension

        with open(result_path, "ab") as original_file:
            original_file.write(fragment_value)

    return result_path
