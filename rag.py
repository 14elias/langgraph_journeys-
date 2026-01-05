from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv
import os

load_dotenv()

loader = PyPDFLoader(file_path='agents.pdf')
docs = loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=30
)

result = splitter.split_documents(docs)


model = "sentence-transformers/all-mpnet-base-v2"
hf = HuggingFaceEndpointEmbeddings(
    model=model,
    task="feature-extraction",
    huggingfacehub_api_token=os.getenv('HUGGING_API_KEY'),
)



vector_store = Chroma.from_documents(
    documents=docs,
    embedding=hf,
    collection_name='test_db'
)

query = 'what is AIagent'
result = vector_store.similarity_search(query='', k=2)
print(result[0].page_content)


