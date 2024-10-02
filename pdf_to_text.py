import pdfplumber, os
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document 
# from langchain.document_loaders import PyPDFLoader
from langchain.prompts import ChatPromptTemplate
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

all_text = []
# all_image = []
chain = None

text_splitter = CharacterTextSplitter(
     separator="\n",
     chunk_size=2000,
     chunk_overlap=100
)

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
    "한국어로 작성합니다.\n\n"
    "질문: {question}\n"
    "문맥: {context}\n"
    "답변:"
)

def make_chain(): 
    global chain

    db = Chroma.from_documents(all_text, OpenAIEmbeddings())
    retriever = db.as_retriever(search_kwargs={"k": 10})

    chain = (
         {"context": retriever, "question": RunnablePassthrough()} |
         prompt_template |
         ChatOpenAI() |
         StrOutputParser()
    )

def readPdf(pdfFile):
    print("PDF 파일을 읽어들이는 중...") 
    raw_documents = []
    with pdfplumber.open(pdfFile) as pdf:  
        print(f'총 페이지 수 : {len(pdf.pages)}')
        for page in pdf.pages:  
            text = page.extract_text()  
            if text:  # 텍스트가 있는 경우에만 추가  
                    raw_documents.append(Document(page_content=text, metadata={"page": page.page_number}))

    # print(f'Documents Size : {len(raw_documents)}')
    # for document in raw_documents:
    #      print(document)

    # 로드된 문서를 분할하여 documents에 저장  
    documents = text_splitter.split_documents(raw_documents)  

    # 분할된 텍스트를 리스트에 추가  
    all_text.extend(documents) 
    print(f"{pdfFile}을 읽어들였습니다. : {len(all_text)}")  

def chat_with_user(user_message):
    ai_message = chain.invoke(user_message)
    return ai_message

def main():
    init_api()
    
    pdf_file_name = f"요양보호사+양성+표준교재(2023년+개정판).pdf"

    readPdf(pdf_file_name)
    make_chain()

    while True:
         message = input("USER: (quit or q : 종료) ")
         if message.lower() == 'quit' or message.lower() == 'q':
              break
         
         ai_message = chat_with_user(message)

         print(f" AI : {ai_message}")


if __name__ == "__main__":
    main()
    
