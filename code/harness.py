from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings, SentenceTransformerEmbeddings
import numpy as np
import os
import shutil

folder_path = "../chroma_vectordb/"  # 文件夹的路径

# 清空文件夹内容
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    if os.path.isfile(file_path):
        os.remove(file_path)
    elif os.path.isdir(file_path):
        shutil.rmtree(file_path)

folder_path = "../arrays/"  # 文件夹的路径

for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    if os.path.isfile(file_path):
        os.remove(file_path)
    elif os.path.isdir(file_path):
        shutil.rmtree(file_path)



print("loading source files...\t") 
loader = PyPDFLoader("./srcfiles/test.pdf")
pages = loader.load_and_split()
print("done!\n") 

print("splitting documents...\t") 
r_splitter = RecursiveCharacterTextSplitter(
    chunk_size=150,
    chunk_overlap=0,
    separators=["\n\n", "\n", "(?<=\. )","(?<=。)", " ", ""]
)
splits = np.array(r_splitter.split_documents(pages))

np.save('../arrays/splits.npy',splits )
s=np.load('../arrays/splits.npy', allow_pickle=True)
print(s)

for i in range(len(splits)):
    splits[i].metadata["p_index"]=i


print (len(splits))
print("done!\n") 


multilinguale5b=HuggingFaceEmbeddings(model_name="../intfloat_multilingual-e5-base")

 
#向量数据库保存位置
persist_directory = '../chroma_vectordb/'
vectordb = Chroma.from_documents(
    documents=splits,
    embedding=multilinguale5b,
    persist_directory=persist_directory
)
print(vectordb._collection.count())



question = "当前实验存在什么问题"
 
comp_res = vectordb.similarity_search_with_score(question,k=3)

feed_content=""
p_index=comp_res[0][0].metadata["p_index"]
for i in range(max(0,p_index-2),min(len(splits),p_index+3)):
    feed_content+=splits[i].page_content
#print(feed_content)

from POE import load_chat_id_map, clear_context, send_message, get_latest_message, set_auth

#Auth
set_auth('Quora-Formkey','xxx')
set_auth('Cookie','xxx')
bot='chinchilla'
chat_id = load_chat_id_map(bot)
clear_context(chat_id)
print("Context is now cleared")
message=f"从现在开始你是一个机器人客服，根据三重反引号分隔的文本中的内容，用中文回答三重中括号分隔的文本中的问题\n```{feed_content}```\n[[[{question}]]]"
#print(message)
send_message(message,bot,chat_id)
reply = get_latest_message(bot)
print(f"{bot} : {reply}")