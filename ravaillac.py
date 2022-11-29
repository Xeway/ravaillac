import os
import math

def ravaillac(file_name, size_limit):
    if size_limit <= 0:
        return

    file_size = os.stat(file_name).st_size
    if file_size <= size_limit:
        return

    folder_id = 1
    result_path = f"ravaillac_result/{os.path.basename(file_name)}_{int(size_limit)}B"
    while os.path.exists(result_path):
        result_path = f"ravaillac_result/{os.path.basename(file_name)}_{int(size_limit)}B({folder_id})"
        folder_id += 1

    os.makedirs(result_path)

    splits = math.ceil(file_size / size_limit)

    with open(file_name, "rb") as file:
        file_value = file.read()

    fragment_size = file_size // splits

    i = 0
    while i <= len(file_value) - fragment_size:
        with open(f"{result_path}/{os.path.basename(file_name)}{i}", "wb") as file:
            file.write(file_value[i:i+fragment_size])

        i += fragment_size

    # we treat the rest
    # <=> if file_size % splits > 0
    if i != len(file_value):
        with open(f"{result_path}/{os.path.basename(file_name)}{i}", "wb") as file:
            file.write(file_value[i:len(file_value)])

ravaillac("test_files/debian-11.5.0-amd64-netinst.iso", 8e6)