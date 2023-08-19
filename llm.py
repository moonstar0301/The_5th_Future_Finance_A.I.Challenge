
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


def ready_proc(vectordb):
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
    return qa_chain

# 언어 모델의 응답을 처리하는 함수를 정의합니다.
def process_llm_response(llm_response, vectordb):
    qa_chain = ready_proc(vectordb)
    # 언어 모델의 응답 결과를 출력합니다.
    return(qa_chain(llm_response)['result'])

    # 언어 모델 응답의 소스 문서 목록을 반환합니다.
    #print('\n\nSources:')
    #for source in llm_response["source_documents"]:
    #    print(source.metadata["page"])
    
    
def q_generator(vectordb):
    # Suggested Question Generator

    prompt_template_generator = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.
    you are competent financial advisor. You need to create a suggested question,

    {context}

    Question: {question}

    Don't answer with short answers, answer with complete sentences.
    Answer in Korean:"""
    # PROMPT에 'context'와 'question'을 입력 변수로하는 프롬프트 템플릿을 저장합니다.
    PROMPT_generator = PromptTemplate(
        template=prompt_template_generator, input_variables=["context", "question"]
    )
    # 'chain_type_kwargs'변수에 딕셔너리를 저장합니다.
    chain_type_kwargs_generator = {"prompt": PROMPT_generator}
    # 'as_retriever'메서드를 호출하여 'vectordb'에서 생성된 벡터 데이터베이스를 검색 가능한 형태로 변환합니다.
    # 유사도가 높은 상위 3개의 문서만 반환하도록 지정합니다.
    retriever_generator = vectordb.as_retriever(search_kwargs={"k": 3})
    # 'gpt-3.5-turbo-16k'모델을 사용합니다.
    # temperature값이 낮은수록 더 일관성 있는 문장이 생성됩니다.
    llm_generator = ChatOpenAI(temperature=0.0,model_name='gpt-3.5-turbo-16k')

    # 체인타입을 결정합니다.
    qa_chain_generator = RetrievalQA.from_chain_type(
        # 언어모델을 할당합니다.
        llm=llm_generator,
        # 체인의 유형을 지정합니다.
        chain_type="stuff",
        retriever=retriever_generator,
        # 응답과 함께 소스 문서를 반환합니다.
        return_source_documents=True,
        chain_type_kwargs=chain_type_kwargs_generator)

    # 언어 모델의 응답을 처리하는 함수를 정의합니다.
    def process_llm_response_generator(llm_response_generator):
        # 언어 모델의 응답 결과를 출력합니다.
        return(llm_response_generator['result'])

    question = ['올해 금리관련해서 질문 하나만 만들어줄 수 있어?', '올해 경기관련해서 질문 하나만 만들어줄 수 있어?', '은퇴후,건강보험료 관련해서 질문 하나만 만들어줄 수 있어?',\
                '인컴투자 관련해서 질문 하나만 만들어줄 수 있어?','투자원칙 관련해서 질문 하나만 만들어줄 수 있어?', '적립식투자 관련해서 질문 하나만 만들어줄 수 있어?']
    answer = []
    for i in range(6) :
        result = process_llm_response_generator(llm_response_generator = qa_chain_generator(question[i]))
        answer.append(result)

    num1 = random.randrange(0, 3)
    num2 = random.randrange(4, 6)

    suggested_question_list = []
    suggested_question_list.append(answer[num1])
    suggested_question_list.append(answer[num2])
    return suggested_question_list

def mindmap_generator(vectordb, query):
    prompt_template_mindmap = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.
    you are competent financial advisor.

    {context}

    Question: {question}

    Answer in Korean
    소주제'들은 주제의 하위주제들로 네가 선정해줘.  '내용'은 문장형식으로, 소주제에 대한 구체적인 너의 설명을 담고 있어야해.  또한 '내용'은 반드시 '~입니다'와 같이 끝나야하고, '소주제'에 대해서 설명하는 어투여야해. let's think step by step.  다음과 같은 형식으로 결과물을 반환해줘. 결과물 이외의 다른 말은 하지마.

    '''
    small_subject = [소주제1, 소주제2, 소주제3, 소주제4]
    contents = [['소주제1'와 관련된 내용1, '소주제1'와 관련된 내용2,'소주제1'와 관련된 내용3],['소주제2'와 관련된 내용1, '소주제2'와 관련된 내용2,'소주제2'와 관련된 내용3],['소주제3'와 관련된 내용1, '소주제3'와 관련된 내용2,'소주제3'와 관련된 내용3],['소주제4'와 관련된 내용1, '소주제4'와 관련된 내용2,'소주제4'와 관련된 내용3]]
    '''

    """
    # PROMPT에 'context'와 'question'을 입력 변수로하는 프롬프트 템플릿을 저장합니다.
    PROMPT_mindmap = PromptTemplate(
        template=prompt_template_mindmap, input_variables=["context", "question"]
    )
    # 'chain_type_kwargs'변수에 딕셔너리를 저장합니다.
    chain_type_kwargs_mindmap = {"prompt": PROMPT_mindmap}
    # 'as_retriever'메서드를 호출하여 'vectordb'에서 생성된 벡터 데이터베이스를 검색 가능한 형태로 변환합니다.
    # 유사도가 높은 상위 3개의 문서만 반환하도록 지정합니다.
    retriever_mindmap = vectordb.as_retriever(search_kwargs={"k": 3})
    # 'gpt-3.5-turbo-16k'모델을 사용합니다.
    # temperature값이 낮은수록 더 일관성 있는 문장이 생성됩니다.
    llm_mindmap = ChatOpenAI(temperature=0.0,model_name='gpt-3.5-turbo-16k')

    # 체인타입을 결정합니다.
    qa_chain_mindmap = RetrievalQA.from_chain_type(
        # 언어모델을 할당합니다.
        llm=llm_mindmap,
        # 체인의 유형을 지정합니다.
        chain_type="stuff",
        retriever=retriever_mindmap,
        # 응답과 함께 소스 문서를 반환합니다.
        return_source_documents=True,
        chain_type_kwargs=chain_type_kwargs_mindmap)

    # 언어 모델의 응답을 처리하는 함수를 정의합니다.
    def process_llm_response_mindmap(llm_response_mindmap):
        # 언어 모델의 응답 결과를 출력합니다.
        return(llm_response_mindmap['result'])

    result = process_llm_response_mindmap(qa_chain_mindmap(query))
    small_subject = []
    contents = []
    local_vars = locals()
    try:
        exec(result, globals(), local_vars)
    except Exception as e:
        pass
    return local_vars['small_subject'], local_vars['contents']
