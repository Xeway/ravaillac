import os
import math

def ravaillac(file_name, size_limit):
    # with open(file_name, "rb") as file:
    #     print(file.read())
    file_size = os.stat(file_name).st_size

    if file_size <= size_limit:
        return

    splits = math.ceil(file_size/size_limit)

    print(splits)

ravaillac("./test_files/debian-11.5.0-amd64-netinst.iso", 8e6)