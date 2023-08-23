import os
import shutil
import numpy as np
import ast


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

def find_file_type_from_array(arr,type,root=""):
    res=[]
    for file_name in arr:
        if file_name.lower().endswith('.'+type):
            # TYPE 文件
            file_path = os.path.join(root, file_name)
            res.append(file_path)
    return res

def use_existing_data():
    useornot=input("Use existing data？（Y/N） : ")
    if useornot=="Y" or useornot=="y" or useornot=="":
        return True
    if useornot=="N" or useornot=="n":
        return False
    else:
        error_handler("NOT A PROPER SELECTION",666)

def use_update_mode():
    useornot=input("just update files？(n for start over)（Y/N） : ")
    if useornot=="Y" or useornot=="y" or useornot=="":
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

def compare_filelist(srcpath,path):
    filename = ".src_filename_cookies.npy"
    file_path = os.path.join(path, filename)

    if not os.path.exists(file_path):
        # 创建一个新的空nparray并保存到文件
        empty_array = np.array([])
        np.save(file_path, empty_array)
        print("cookie file generated")

    # 加载现有的nparray
    existing_array = np.load(file_path)
    
    # 示例比较数组 b
    b = get_filelist_array(srcpath)
    
    # 查找多余的元素和缺少的元素
    extra_elements = np.setdiff1d(b, existing_array)
    missing_elements = np.setdiff1d(existing_array, b)
    
    if len(extra_elements) > 0:
        print("increased files:", extra_elements)
    else:
        print("no new files added")
    
    if len(missing_elements) > 0:
        print("reduced files:", missing_elements)
    else:
        print("no file reduced")
    np.save(file_path,b)
    return extra_elements,missing_elements

def get_filelist_array(srcpath):
    file_names = os.listdir(srcpath)
    file_names_array = np.array(file_names)
    return file_names_array


def busy_wait():
    i=1
    while True:
        i+=1

def get_list_from_str(string):
    # 寻找最后一个列表的起始位置和结束位置
    start_index = string.rfind("[")
    end_index = string.rfind("]")

    # 确保找到的起始位置在最后一个结束位置之前
    while start_index >= 0 and start_index > end_index:
        start_index = string.rfind("[", 0, start_index - 1)

    # 提取最后一个列表部分
    list_string = string[start_index:end_index + 1]
    if (list_string[-2]=='\\'):
        list_string=list_string[:-2]+list_string[-1]

    # 将列表字符串转换成实际的列表
    my_list = ast.literal_eval(list_string)

    return my_list