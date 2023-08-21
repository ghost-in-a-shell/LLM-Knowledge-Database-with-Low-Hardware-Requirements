#paths
CHROMADB_PATH="../chroma_vectordb/"
FILEARRAY_PATH="../arrays/"
SRCFILE_PATH="./srcfiles/"
EMBEDDING_PATH="../intfloat_multilingual-e5-base"

#split params
SPLITRCTS_CHUNKSIZE=150
SPLITRCTS_OVERLAP=0
SPLITRCTS_SEPARATORS=["\n\n", "\n", "(?<=\. )","(?<=。)", " ", ""]

#llm params
NEAREST_K=5
HALF_SEARCH_RANGE=3

#debug
DEBUG=False

#poe
TOKEN="xxx"
CHAT_ID=60643403
POE_BOT='chinchilla'