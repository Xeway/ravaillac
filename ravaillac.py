import os
import math

def ravaillac(file_name, size_limit):
    # with open(file_name, "rb") as file:
    #     print(file.read())
    if size_limit <= 0:
        return

    file_size = os.stat(file_name).st_size
    if file_size <= size_limit:
        return

    splits = math.ceil(file_size/size_limit)

    folder_id = 0
    result_path = f"ravaillac_result/{os.path.basename(file_name)}_{int(size_limit)}B"
    while os.path.exists(result_path):
        result_path = f"ravaillac_result/{os.path.basename(file_name)}_{int(size_limit)}B({folder_id})"
        folder_id += 1

    os.makedirs(result_path)


ravaillac("test_files/debian-11.5.0-amd64-netinst.iso", 8e6)