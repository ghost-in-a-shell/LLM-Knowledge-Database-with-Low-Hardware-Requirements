from langchain.text_splitter import CharacterTextSplitter
## 后期版本换成CharacterTextSplitter
article_text = content_div.get_text()
text_splitter = CharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size = 100,
    chunk_overlap  = 20,
    length_function = len,
)
print("11111")