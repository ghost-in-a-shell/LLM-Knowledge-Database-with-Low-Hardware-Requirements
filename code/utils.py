import os
import shutil

def error_handler(name,code):
    print(name)
    exit(code)

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

def use_existing_data():
    useornot=input("Use existing data？（Y/N） : ")
    if useornot=="Y" or useornot=="y":
        return True
    if useornot=="N" or useornot=="n":
        return False
    else:
        error_handler("NOT A PROPER SELECTION",666)

def get_npy(path):
    npylist=find_file_type(path,'npy')
    if len(npylist) == 1:
        unique_file_name = npylist[0]
        return unique_file_name
    else:
        error_handler("ARRAY FOLDER CHAOS",777)