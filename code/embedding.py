from sentence_transformers import SentenceTransformer
from pydantic import BaseModel
from typing import List
from langchain.embeddings.base import Embeddings


class multilinguale5b(Embeddings, BaseModel):
    """embedding model."""
    model = SentenceTransformer('../intfloat_multilingual-e5-base')
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        input_texts=[]
        for text in texts:
            input_texts.append("passage: "+text)
        print(input_texts)
        embeddings = self.model.encode(input_texts, normalize_embeddings=True)
        return embeddings

    def embed_query(self, text: str) -> List[float]:
        input_texts=[]
        input_texts.append("query: "+text)
        return self.model.encode(input_texts, normalize_embeddings=True)[0]