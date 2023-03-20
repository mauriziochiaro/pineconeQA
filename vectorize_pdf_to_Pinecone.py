import os
from langchain.document_loaders import UnstructuredPDFLoader, OnlinePDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

loader = UnstructuredPDFLoader("D:\\path\\to\\help.pdf")
data = loader.load()
print (f'You have {len(data)} document(s) in your data')
print (f'There are {len(data[0].page_content)} characters in your document')

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(data)
print (f'Now you have {len(texts)} documents')

from langchain.vectorstores import Chroma, Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
import pinecone

# OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
# PINECONE_API_KEY = os.environ["PINECONE_API_KEY"]
# PINECONE_API_ENV = os.environ["PINECONE_API_ENV"]

OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
PINECONE_API_KEY = st.secrets["PINECONE_API_KEY"]
PINECONE_API_ENV = "us-east-1-aws"

embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

# initialize pinecone
pinecone.init(
    api_key=PINECONE_API_KEY,  # find at app.pinecone.io
    environment=PINECONE_API_ENV  # next to api key in console
)
# create new index app.pinecone.io
index_name = "indexname"

# populate vectore db 
docsearch = Pinecone.from_texts([t.page_content for t in texts], embeddings, index_name=index_name)
