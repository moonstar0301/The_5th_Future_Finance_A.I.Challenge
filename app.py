from flask import Flask, render_template, request, jsonify
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

app = Flask(__name__)

os.environ["OPENAI_API_KEY"] = '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'

# PyPDFLoader를 사용하여 'investment.pdf' 파일을 로드합니다.
loader = PyPDFLoader('./researches/investment.pdf')
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
prompt_template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.
you are competent financial advisor. Today's date is August 18, 2023.

{context}

Question: {question}

Don't answer with short answers, answer with complete sentences. 
Your answers should be detailed based on evidence, and don't say unnecessary things. Let's think step by step.
Answer in Korean:"""
# PROMPT에 'context'와 'question'을 입력 변수로하는 프롬프트 템플릿을 저장합니다.
PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)
# 'chain_type_kwargs'변수에 딕셔너리를 할당합니다.
chain_type_kwargs = {"prompt": PROMPT}

# 'as_retriever'메서드를 호출하여 'vectordb'에서 생성된 벡터 데이터베이스를 검색 가능한 형태로 변환합니다.
# 유사도가 높은 상위 3개의 문서만 반환하도록 지정합니다.
retriever = vectordb.as_retriever(search_kwargs={"k": 3})
# 'gpt-3.5-turbo-16k'모델을 사용합니다.
# temperature값이 낮은수록 더 일관성 있는 문장이 생성됩니다.
llm = ChatOpenAI(temperature=0.0,model_name='gpt-3.5-turbo-16k')

# 체인타입을 결정합니다.
qa_chain = RetrievalQA.from_chain_type(
    # 언어모델을 할당합니다.
    llm=llm,
    # 체인의 유형을 지정합니다.
    chain_type="stuff",
    retriever=retriever,
    # 응답과 함께 소스 문서를 반환합니다.
    return_source_documents=True,
    chain_type_kwargs=chain_type_kwargs)

# 언어 모델의 응답을 처리하는 함수를 정의합니다.
def process_llm_response(llm_response):
    # 언어 모델의 응답 결과를 출력합니다.
    return(llm_response['result'])

    # 언어 모델 응답의 소스 문서 목록을 반환합니다.
    #print('\n\nSources:')
    #for source in llm_response["source_documents"]:
    #    print(source.metadata["page"])

query_list = []

def process_query(query):
  if(len(query_list)==0):
    query_list.append(query)
    return query
  elif(len(query_list)==1):
    result = "지금 질문은'{}', 이전질문은 '{}'이야. 이전질문은 현재질문과 관련있을때만 고려해서 답해줘.".format(query, query_list[-1])
    query_list.append(query)
    return result
  else:
    result = "{}, 이전질문은 '{}'이니까 참고해서 답해줘. 이전질문은 현재질문과 관련있을때만 고려해서 답해줘.".format(query, ', '.join(query_list))
    query_list.append(query)
    query_list.pop(0)
    return result


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    # Get message from request data
    user_message = request.form.get("message")
    user_message = process_query(user_message)

    # Process user message using the chatbot logic
    bot_response = process_llm_response(qa_chain(user_message))

    # Return chatbot response as JSON
    return jsonify(bot_response)


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
