import os
from openai import OpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain.text_splitter import CharacterTextSplitter
from langchain_chroma import Chroma

from pdf_to_image_to_text import extract_text_from_converted_pdf
from pdf_to_text_using_pdfplumber import readPdf

# import chromadb
# from chromadb.api.types import Documents, EmbeddingFunction, Embeddings


# all_text = []
# all_image = []
chain = None
folder_path = './'
persist_directory = './chroma_db'  # Chroma 데이터베이스를 저장할 디렉토리

def init_api():
    with open("chatgpt_kict2409.env") as env:
          for line in env:
               key, value = line.strip().split("=")
               os.environ[key] = value

    os.environ["OPENAI_API_KEY"] = os.environ.get("API_KEY")

prompt_template = ChatPromptTemplate.from_template(
    "당신은 질문 답변 작업의 영리하고 창의적인 어시스턴트입니다. "
    "다음 문맥을 사용하여 질문에 답하세요. "
    "정확하고 신뢰성 있는 정보를 제공하고, 모르는 내용은 '모르겠습니다'라고 답변하세요. "
    "답변은 요청한 내용만을 포함하여 최대한 자세하게 작성하되 번호가 연결되어 있는 경우 연결된 번호의 내용을 모두 포함해주세요. 메타데이터나 추가적인 중요한 정보를 포함하도록 하세요. "
    "답변을 위해 참고한 문서의 페이지 번호를 포함하여 답변해주세요. "
    "한국어로 작성합니다.\n\n"
    "질문: {question}\n"
    "문맥: {context}\n"
    "답변:"
)

def parse_pdf_local_path(folder_path) -> list:
    '''지정된 폴더의 pdf 파일을 읽어들여 텍스트로 저장되는 함수'''
    
    all_texts = []
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=2000,
        chunk_overlap=100
    )
    
    for filename in os.listdir(folder_path):
        # 파일이 PDF 형식인 경우에만 처리
        if filename.endswith(".pdf"):
            raw_document = readPdf(filename)
            if len(raw_document) <= 0:
                raw_document = extract_text_from_converted_pdf(filename)
            
            doocuments = text_splitter.split_documents(raw_document)
            all_texts.extend(doocuments)
            
    return all_texts


def make_chain(): 
    global chain
    
    db = create_or_load_db()
    
    retriever = db.as_retriever(search_kwargs={"k": 10})

    chain = (
         {"context": retriever, "question": RunnablePassthrough()} |
         prompt_template |
         ChatOpenAI() |
         StrOutputParser()
    )
    
    
def create_or_load_db():
    global folder_path
    
    if os.path.exists(persist_directory):
        # 기존 데이터베이스 로드
        db = Chroma(persist_directory=persist_directory, embedding_function=OpenAIEmbeddings())
    else:
        # 새 데이터베이스 생성
        all_texts = parse_pdf_local_path(folder_path)
        db = Chroma.from_documents(all_texts, OpenAIEmbeddings(), persist_directory=persist_directory)
        # db.persist()  # 변경사항을 디스크에 저장
    return db
    
    
def chat_with_user(user_message):
    ai_message = chain.invoke(user_message)
    return ai_message


def main():
    init_api()
    
    make_chain()

    while True:
         message = input("USER: (quit or q : 종료) ")
         if message.lower() == 'quit' or message.lower() == 'q':
              break
         
         ai_message = chat_with_user(message)

         print(f" AI : {ai_message}")


if __name__ == "__main__":
    main()
    
