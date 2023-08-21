from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
import variables

def embedding_saving(splits):
    print("sectence embedding...")
    embedding=HuggingFaceEmbeddings(model_name=variables.EMBEDDING_PATH)

    #向量数据库保存位置
    persist_directory = variables.CHROMADB_PATH
    vectordb = Chroma.from_documents(
        documents=splits,
        embedding=embedding,
        persist_directory=persist_directory
    )
    vectordb.persist()
    print(vectordb._collection.count())
    print("done!\n")
    return vectordb

def update_db(splits,l):
    if l!=0:
        embedding_saving(splits[-l:])

def get_vectordb():
    return Chroma(persist_directory=variables.CHROMADB_PATH, embedding_function=HuggingFaceEmbeddings(model_name=variables.EMBEDDING_PATH))