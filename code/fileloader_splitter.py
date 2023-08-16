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

def fileloader_splitter(path):
    all_files_pages=[]
# 使用os.walk()遍历文件夹及其子文件夹
    for inputtype in variables.INUPT_TYPES:
        filenamelist=utils.find_file_type(path,inputtype)
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


    splits=rcts_splitter(all_files_pages,variables.SPLITRCTS_CHUNKSIZE,variables.SPLITRCTS_OVERLAP,variables.SPLITRCTS_SEPARATORS)
    #print(splits)
    for i in range(len(splits)):
        splits[i].metadata["p_index"]=i
    np_filename=variables.FILEARRAY_PATH+"splits"+datetime.now().strftime("-%Y-%m-%d-%H-%M-%S")+".npy"
    np.save(np_filename,splits )
    print("splits array saved at: "+np_filename)
    return np_filename




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
