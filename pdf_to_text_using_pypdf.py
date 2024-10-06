import os
from langchain_community.document_loaders import PyPDFLoader


def readPdf(filename):
    '''pypdf 패키지를 사용하여 pdf 파일을 읽어서 텍스트로 리턴'''
    
    raw_documents = []
    all_text = []
    
    # PDF 파일을 로드하여 raw_documents에 저장
    raw_documents = PyPDFLoader(filename).load() # 파일명을 메타정보로 넣는 부분이 추가 필요해 보임
   
    return raw_documents


def main():
    filename = f"요양보호사+양성+표준교재(2023년+개정판).pdf"

    all_text = readPdf(filename)
    
    print(all_text)
    

if __name__ == "__main__":
    main()
    
