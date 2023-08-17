from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import Docx2txtLoader
from langchain.document_loaders import UnstructuredPowerPointLoader
from langchain.document_loaders import UnstructuredFileLoader
from langchain.document_loaders import UnstructuredMarkdownLoader
from langchain.document_loaders.image import UnstructuredImageLoader
import utils
import numpy as np
from datetime import datetime
import os

import variables

def fileloader_fromarray(arr):
    all_files_pages=[]
    for inputtype in variables.INUPT_TYPES:
        filenamelist=utils.find_file_type_from_array(arr,inputtype,variables.SRCFILE_PATH)
        fp=get_content(filenamelist,inputtype)
        all_files_pages+=fp
    #print(all_files_pages)
    return all_files_pages

def addto_split(all_files_pages):
    new_splits=rcts_splitter(all_files_pages,variables.SPLITRCTS_CHUNKSIZE,variables.SPLITRCTS_OVERLAP,variables.SPLITRCTS_SEPARATORS)
    split_filename=utils.get_npy(variables.FILEARRAY_PATH)
    splits=np.load(split_filename, allow_pickle=True)
    splits=np.concatenate((splits, new_splits), axis=0)
    for i in range(len(splits)):
        splits[i].metadata["p_index"]=i
    np.save(split_filename,splits )
    print("new splits array saved at: "+split_filename)
    #print(splits)
    return splits,len(new_splits),split_filename

def updatesplits(extra,missing):
    fp=fileloader_fromarray(extra)
    return addto_split(fp)

def fileloader_splitter(path):

    file_names_scan = []
    for file_name_scan in os.listdir(variables.SRCFILE_PATH):
        file_names_scan.append(file_name_scan)

    file_names_array = np.array(file_names_scan)

    # 保存为.npy文件
    np.save(os.path.join(variables.COOKIE_PATH, ".src_filename_cookies.npy"), file_names_array)


    all_files_pages=[]
    for inputtype in variables.INUPT_TYPES:
        filenamelist=utils.find_file_type(path,inputtype)
        fp=get_content(filenamelist,inputtype)
        all_files_pages+=fp
    #print(all_files_pages)

    splits=rcts_splitter(all_files_pages,variables.SPLITRCTS_CHUNKSIZE,variables.SPLITRCTS_OVERLAP,variables.SPLITRCTS_SEPARATORS)
    #print(splits)
    for i in range(len(splits)):
        splits[i].metadata["p_index"]=i
    np_filename=variables.FILEARRAY_PATH+"splits"+datetime.now().strftime("-%Y-%m-%d-%H-%M-%S")+".npy"
    np.save(np_filename,splits )
    print("splits array saved at: "+np_filename)
    return np_filename

def get_content(filenamelist,inputtype):
    all_files_pages=[]
    if inputtype=='pdf':
        for file_path in filenamelist:
            print("loading pdf file : "+str(file_path))
            cur_pages=pdffileloader(file_path)
            all_files_pages+=cur_pages
    elif inputtype=='docx':
        for file_path in filenamelist:
            print("loading docx file : "+str(file_path))
            cur_pages=wordfileloader(file_path)
            #print(cur_pages)
            all_files_pages+=cur_pages
    elif inputtype=='pptx':
        for file_path in filenamelist:
            print("loading pptx file : "+str(file_path))
            cur_pages=pptfileloader(file_path)
            #print(cur_pages)
            all_files_pages+=cur_pages
    elif inputtype=='txt':
        for file_path in filenamelist:
            print("loading txt file : "+str(file_path))
            cur_pages=txtfileloader(file_path)
            #print(cur_pages)
            all_files_pages+=cur_pages
    elif inputtype=='md':
        for file_path in filenamelist:
            print("loading md file : "+str(file_path))
            cur_pages=mdfileloader(file_path)
            #print(cur_pages)
            all_files_pages+=cur_pages
    elif inputtype=='png':
        for file_path in filenamelist:
            print("loading png file : "+str(file_path))
            cur_pages=picfileloader(file_path)
            #print(cur_pages)
            all_files_pages+=cur_pages
    return all_files_pages




def pdffileloader(path):
    loader = PyPDFLoader(path)
    pages = loader.load_and_split()
    print("done!\n") 
    return pages

def wordfileloader(path):
    loader = Docx2txtLoader(path)
    data=loader.load()
    print("done!\n") 
    return data

def pptfileloader(path):
    loader = UnstructuredPowerPointLoader(path)
    data=loader.load()
    print("done!\n") 
    return data  

def txtfileloader(path):
    loader = UnstructuredFileLoader(path)
    data=loader.load()
    print("done!\n") 
    return data  

def mdfileloader(path):
    loader = UnstructuredMarkdownLoader(path)
    data=loader.load()
    print("done!\n") 
    return data  

def picfileloader(path):
    loader = UnstructuredImageLoader(path)
    data=loader.load()
    print("done!\n") 
    return data  


def rcts_splitter(pages,chksz,ovlp,sep):
    print("splitting documents...\t") 
    r_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chksz,
        chunk_overlap=ovlp,
        separators=sep
    )
    splits = np.array(r_splitter.split_documents(pages))
    print("done!\n")
    return splits
