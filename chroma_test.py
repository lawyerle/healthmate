import os
from openai import OpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_chroma import Chroma

def init_api():
    with open("chatgpt_kict2409.env") as env:
        for line in env:
            key, value = line.strip().split("=")
            os.environ[key] = value

init_api()
os.environ["OPENAI_API_KEY"] = os.environ.get("API_KEY")

prompt_template = ChatPromptTemplate.from_template(
    "당신은 질문 답변 작업의 영리하고 창의적인 어시스턴트입니다. "
    "다음 문맥을 사용하여 질문에 답하세요. "
    "정확하고 신뢰성 있는 정보를 제공하고, 모르는 내용은 '모르겠습니다'라고 답변하세요. "
    "답변은 명확하고 간결하게, 최대 세 문장 이내로 작성하세요. 메타데이터나 추가적인 중요한 정보를 포함하도록 하세요. "
    "한국어로 작성합니다.\n\n"
    "질문: {question}\n"
    "문맥: {context}\n"
    "답변:"
)

folder_path = './'
persist_directory = './chroma_db'  # Chroma 데이터베이스를 저장할 디렉토리

def load_and_process_documents():
    all_texts = []
    text_splitter = CharacterTextSplitter(
        separator = "\n",
        chunk_size = 1000,
        chunk_overlap = 50
    )

    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            raw_documents = PyPDFLoader(os.path.join(folder_path, filename)).load()
            documents = text_splitter.split_documents(raw_documents)
            all_texts.extend(documents)

    return all_texts

def create_or_load_db():
    if os.path.exists(persist_directory):
        # 기존 데이터베이스 로드
        db = Chroma(persist_directory=persist_directory, embedding_function=OpenAIEmbeddings())
    else:
        # 새 데이터베이스 생성
        all_texts = load_and_process_documents()
        db = Chroma.from_documents(all_texts, OpenAIEmbeddings(), persist_directory=persist_directory)
        db.persist()  # 변경사항을 디스크에 저장
    return db

db = create_or_load_db()
retriever = db.as_retriever(search_kwargs={"k": 10})

chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt_template
    | ChatOpenAI()
    | StrOutputParser()
)

def chat_with_user(user_message):
    ai_message = chain.invoke(user_message)
    return ai_message

# 대화 루프 시작
while True:
    message = input("USER :(quit or q : 종료)  ")
    if message.lower() in ["quit", "q"]:
        break

    ai_message = chat_with_user(message)
    print(f" AI : {ai_message}")