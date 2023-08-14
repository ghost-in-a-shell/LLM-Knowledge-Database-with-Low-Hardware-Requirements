import os
import shutil

def clear_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

def find_file_type(path,type):
    res=[]
    for root, dirs, files in os.walk(path):
        for file_name in files:
            if file_name.lower().endswith('.'+type):
                # TYPE 文件
                file_path = os.path.join(root, file_name)
                res.append(file_path)
    return res