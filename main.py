import os
# from uuid import uuid4
# from openai import OpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
# from langchain.text_splitter import CharacterTextSplitter
from langchain.text_splitter import RecursiveCharacterTextSplitter, SentenceTransformersTokenTextSplitter
from langchain_experimental.text_splitter import SemanticChunker
from langchain_chroma import Chroma

from pdf_to_image_to_text import extract_text_from_converted_pdf
from pdf_to_text_using_pdfplumber import readPdf
import shutil

chain = None
folder_path = './pdf_data'
persist_directory = './chroma_db'  # Chroma 데이터베이스를 저장할 디렉토리

def init_api():
    with open("chatgpt_kict2409.env") as env:
          for line in env:
               key, value = line.strip().split("=")
               os.environ[key] = value

    os.environ["OPENAI_API_KEY"] = os.environ.get("API_KEY")

prompt_template = ChatPromptTemplate.from_template(
    "당신은 의료 상담 전문가입니다. "
    "일상적인 대화는 그냥 ChatGPT를 사용하세요. "
    "모르는 내용은 '해당 질문에 대한 정보가 없습니다. 전문가를 통해 상담받으세요.'라고 답변하세요. "
    "답변은 한국어로 작성하며, context을 통해 전달된 내용을 우선적으로 사용하여 답변을 해주세요. "
    "답변은 '질병관리청1399콜센터 질환별상담사례', '질병관리청1399콜센터 질환별치료및예방교육', '건강보험심사평가원 생활속질병통계100선', '국민건강보험공단 생활속자가건강관리', '보건복지부 요양보호사양성표준교재(2023년개정판)' 소스 순으로 참고하여 답변해주세요."
    "답변을 위해 참고한 문서가 있는 경우 메타정보의 소스정보를 참고문헌으로 답변해 주세요. "
    "질문 내용에 '진료과', '증상', '예방'이란 키워드가 포함되면 진료과, 질병 정보, 위험 요인, 증상, 예방 방법을 포함한 상세한 답변을 제공하세요. "
    "질병과 관련된 경우 해당 질병에 대한 추천 검색어도 3개정도 제시해 주세요."
    "질병과 관련된 답변은 아래 형식을 따라서 답변해주고, 기타 질문은 자유로운 형식으로 답변해주세요. "
    "\n추천진료과 : 진료과명\n"
    "\n질병정보 : 질병정보를 찾아 내용을 적어주세요. \n"
    "\n관련요인 : 어떤 관련 요인이 있는지 개조식(bullet style)으로 적어주세요. \n"
    "\n증상 : 질문을 분석하여 나타날 수 있는 증상을 개조식(bullet style)으로 적어주세요. \n"
    "\n예방 : 치료 및 예방방법을 개조식(bullet style)으로 적어주세요. \n"
    "\n추천검색어 : \n"
    "\n참고문헌: 참고문헌을 개조식(bullet style)으로 적어주세요.\n"
    "질문: {question}\n"
    "문맥: {context}\n"
    "답변:"
)

def make_chain(): 
    global chain
    
    db = create_or_load_db()
    
    retriever = db.as_retriever(search_kwargs={"k": 5})

    chain = (
         {"context": retriever, "question": RunnablePassthrough()} |
         prompt_template |
         ChatOpenAI(temperature=0, model="gpt-4o-mini-2024-07-18") |
        #  ChatOpenAI(model="ft:gpt-4o-mini-2024-07-18:::AHOKExui") |
         StrOutputParser()
    )
    
    
def create_or_load_db():
    # text_splitter = RecursiveCharacterTextSplitter(
    #     # separator="\n",
    #     chunk_size=1000,
    #     chunk_overlap=50
    # )
    text_splitter = SemanticChunker(OpenAIEmbeddings(model="text-embedding-3-large"))
    
    # 기존 데이터베이스 로드
    db = Chroma(persist_directory=persist_directory, embedding_function=OpenAIEmbeddings(model="text-embedding-3-large"))
    
    for filename in os.listdir(folder_path):
        # 파일이 PDF 형식인 경우에만 처리
        if filename.endswith(".pdf"):
            print(f'{filename} 처리중...')
            raw_document = readPdf(folder_path, filename)
            
            text_check = True
            
            for doc in raw_document:
                if doc.page_content.strip() != "":
                    text_check = False
                    break;
            
            if text_check:    
                raw_document = extract_text_from_converted_pdf(folder_path, filename)
            
            documents = text_splitter.split_documents(raw_document)
            
            existing_docs = db.get(where={"file": filename})
            if existing_docs['ids']:
                print(f'Deleting : {filename}')
                db.delete(ids=existing_docs['ids'])
            
            try:
                db.add_documents(documents)
                shutil.move(os.path.join(folder_path, filename), './pdf_data/processed')
                print(f'{filename} 처리완료...')
            except ValueError:
                print(f'{filename} 읽기 싪패 : 처리할 수 없는 pdf 파일입니다.')
            except Exception:
                print(f'{filename} 처리실패')
                
            
    return db
    
    
def chat_with_user(user_message):
    ai_message = chain.invoke(user_message)
    return ai_message.replace("~", "\~")


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
    
