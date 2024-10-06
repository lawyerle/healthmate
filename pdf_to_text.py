import pdfplumber, os
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document 
from langchain.document_loaders import PyPDFLoader
from langchain.prompts import ChatPromptTemplate
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# import pytesseract
import easyocr
from PIL import Image
import io
import numpy as np

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
    "답변을 위해 참고한 문서의 페이지 번호를 포함하여 답변해주세요. "
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

def readPdf(folder_path):
    print("PDF 파일을 읽어들이는 중...") 
    raw_documents = []
    
    # 지정된 폴더 내 모든 파일을 확인
    for filename in os.listdir(folder_path):
        # 파일이 PDF 형식인 경우에만 처리
        if filename.endswith(".pdf"):
            print(f'{filename} 처리 시작...')
             # PDF 파일을 로드하여 raw_documents에 저장
            raw_documents = PyPDFLoader(folder_path + '/' + filename).load()

            # 로드된 문서를 분할하여 documents에 저장
            documents = text_splitter.split_documents(raw_documents)

            # 분할된 텍스트를 리스트에 추가
            all_text.extend(documents)
            
            print(f'{filename} 처리 완료...')
    #         with pdfplumber.open(filename) as pdf:  
    #             print(f'{filename} 페이지 수 : {len(pdf.pages)}')
    #             for page in pdf.pages:  
    #                 text = page.extract_text()
                    
    #                 page_width = page.width  
    #                 page_height = page.height 
                    
    #                 for img_index, img in enumerate(page.images):
    #                     # 이미지의 bbox 가져오기  
    #                     x0, top, x1, bottom = img['x0'], img['top'], img['x1'], img['bottom']  
    #                     img_bbox = (x0, top, x1, bottom)  

    #                     # 이미지의 bounding box가 페이지 내에 완전히 포함되었는지 확인  
    #                     if (x0 < 0 or top < 0 or x1 > page_width or bottom > page_height):  
    #                         print(f"Skipping image {img_index + 1} on page {page.page_number + 1} due to out-of-bounds coordinates.")  
    #                         continue 
    #                     # 이미지 추출  
    #                     img_within_bbox = page.within_bbox(img_bbox).to_image()  
    #                     image_obj = img_within_bbox.original  
                        
    #                     image_filename = f"{filename}_page_{page.page_number + 1}_img_{img_index + 1}.png"  
    #                     image_output_path = os.path.join("./", image_filename)  
    #                     image_obj.save(image_output_path)
                        
    #                     # 메모리에서 이미지 객체 생성  
    #                     # image_obj = Image.open(io.BytesIO(img_bytes)) 
    #                     image_text = reader.readtext(np.array(image_obj), detail=0)    
    #                     # image_text =  pytesseract.image_to_string(image_obj)
                        
    #                     if image_text:
    #                         print(image_text)
    #                         text += " ".join(image_text)
                    
                    
    #                 print(text.strip()) 
    #                 if text.strip():  # 텍스트가 있는 경우에만 추가  
    #                     raw_documents.append(Document(page_content=text, metadata={"page": page.page_number, "file": filename}))
                    
    #                     # print(f'Documents Size : {len(raw_documents)}')
    #                     # for document in raw_documents:
    #                     #      print(document)

    # # 로드된 문서를 분할하여 documents에 저장  
    # documents = text_splitter.split_documents(raw_documents)  

    # 분할된 텍스트를 리스트에 추가  
    # all_text.extend(documents) 
    print(f"총 읽어들인 텍스트 : {len(all_text)}")  


def chat_with_user(user_message):
    ai_message = chain.invoke(user_message)
    return ai_message


def main():
    init_api()
    
    folder_path = f"./"

    readPdf(folder_path)
    make_chain()

    while True:
         message = input("USER: (quit or q : 종료) ")
         if message.lower() == 'quit' or message.lower() == 'q':
              break
         
         ai_message = chat_with_user(message)

         print(f" AI : {ai_message}")


if __name__ == "__main__":
    main()
    
