
import os
from langchain.vectorstores import Chroma, ElasticKnnSearch
from langchain.embeddings import OpenAIEmbeddings, cohere as ce
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter, CharacterTextSplitter
)
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA, ConversationChain
from langchain.document_loaders import (
    TextLoader, DirectoryLoader, PyPDFLoader
)
from langchain.prompts import (
    PromptTemplate, SystemMessagePromptTemplate, ChatPromptTemplate
)
from langchain.chat_models import ChatOpenAI
from langchain.memory import (
    ChatMessageHistory, ConversationBufferMemory, ConversationBufferWindowMemory
)
import random

def database_generator():

    # PyPDFLoader를 사용하여 'investment.pdf' 파일을 로드합니다.
    loader = PyPDFLoader('./researches/total_research.pdf')
    # 로더를 사용하여 PDF 파일의 내용을 documents 변수에 로드합니다.
    documents = loader.load()
    # 'CharacterTextSplitter'를 사용하여 텍스트를 크기 1000의 청크로 분할합니다. 청크 간의 겹침은 없습니다.
    text_splitter = CharacterTextSplitter(chunk_size = 1000, chunk_overlap = 0)
    # 분할자를 사용하여 'documents'를 청크로 분할하고 결과를 texts 변수에 저장합니다.
    texts = text_splitter.split_documents(documents)
    #벡터 데이터베이스가 저장될 디렉토리의 이름을 변수에 저장합니다.
    persist_directory = 'db'
    # 텍스트 문서의 임베딩을 생성하는데 사용할 모델을 변수에 할당합니다.
    embedding = OpenAIEmbeddings()
    # Chroma 클래스의 'from_documents' 메서드를 호출하여 문서의 임베딩을 생성하고 벡터데이터 베이스를 초기화합니다.
    vectordb = Chroma.from_documents(
        documents=documents,
        embedding=embedding,
        persist_directory=persist_directory)
    # persist 메서드를 호출하여 'vectordb'에서 생성된 벡터 데이터베이스를 디스크에 저장합니다.
    # 이렇게 하면 나중에 데이터베이스를 다시 로드하여 사용할 수 있습니다.
    vectordb.persist()
    # 메모리에서 데이터베이스를 제거합니다.
    vectordb = None
    # Chroma 클래스를 인스턴스화하여 vectordb 변수에 할당합니다. 문서의 임베딩을 저장하고 검색하는데 사용됩니다.
    vectordb = Chroma(
        persist_directory=persist_directory,
        embedding_function=embedding)
    # 프롬프트를 'prompt_template'변수에 저장합니다.
    return vectordb
