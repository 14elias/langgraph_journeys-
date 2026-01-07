from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from dotenv import load_dotenv
import os

load_dotenv()


loader = PyPDFLoader(file_path='agents.pdf')
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
chunks = text_splitter.split_documents(docs)

model = "sentence-transformers/all-mpnet-base-v2"
hf = HuggingFaceEndpointEmbeddings(
    model=model,
    task="feature-extraction",
    huggingfacehub_api_token=os.getenv('HUGGING_API_KEY'),
)


vectore_store = Chroma.from_documents(
    embedding=hf,
    documents=chunks,
    collection_name='rag_llm'
)


retriever = vectore_store.as_retriever(
    search_type='mmr',
    search_kwargs={"k": 2, "lambda_mult": 0.25}
)

os.environ["OPENAI_API_KEY"] = os.getenv('API_KEY')
os.environ["OPENAI_BASE_URL"] = "https://openrouter.ai/api/v1"
llm = ChatOpenAI(model="gpt-4o-mini")



prompt = PromptTemplate(
    template="""
    you are an ai assistant .  use the following context to answer the question
    if the answer is not present in the context, say you do not know.
    context: {context}
    input: {question}
    """,
    input_variables=['context', 'question']
)

parser = StrOutputParser()

def format_docs(docs):
    return '\n\n'.join(doc.page_content for doc in docs)

rag_chain = (
    {
        'context':retriever | format_docs,
        'question':lambda x:x
    } | prompt | llm | parser
)


query = 'what is this document mainly about'
result = rag_chain.invoke(query)

print(result)