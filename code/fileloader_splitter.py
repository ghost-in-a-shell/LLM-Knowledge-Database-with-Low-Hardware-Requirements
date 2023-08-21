from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import utils
import numpy as np
from datetime import datetime

import variables

def fileloader_splitter(path):
    all_files_pages=[]
# 使用os.walk()遍历文件夹及其子文件夹
    pdf_filenamelist=utils.find_file_type(path,"pdf")
    for file_path in pdf_filenamelist:
        print("loading pdf file : "+str(file_path))
        cur_pages=pdffileloader(file_path)
        all_files_pages+=cur_pages
    splits=rcts_splitter(all_files_pages,variables.SPLITRCTS_CHUNKSIZE,variables.SPLITRCTS_OVERLAP,variables.SPLITRCTS_SEPARATORS)
    for i in range(len(splits)):
        splits[i].metadata["p_index"]=i
    np_filename=variables.FILEARRAY_PATH+"splits"+datetime.now().strftime("-%Y-%m-%d-%H-%M-%S")+".npy"
    np.save(np_filename,splits )
    print("splits array saved at: "+np_filename)
    return np_filename




def pdffileloader(path):
    print("loading source files...\t") 
    loader = PyPDFLoader(path)
    pages = loader.load_and_split()
    print("done!\n") 
    return pages




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
