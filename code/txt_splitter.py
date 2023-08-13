from langchain.text_splitter import CharacterTextSplitter
with open('./txt_srcfiles/hetangyuese.txt', encoding='utf-8') as f:

    htys = f.read()

## 后期版本换成CharacterTextSplitter"()
text_splitter = CharacterTextSplitter(

    # 这里设置了一个很小的chunk_size，只是为了演示。

    chunk_size = 50,

    chunk_overlap  = 20,

    length_function = len,
    separator='\n'

)

texts = text_splitter.create_documents([htys])

print(texts[0])

print(texts[1])