import pdfplumber, os
from langchain.schema import Document


def readPdf(folder_path, filename) -> list: 
    '''pdfplumber 패키지를 사용하여 pdf 파일을 읽어서 텍스트로 리턴'''
    
    raw_documents = []
    error_cnt = 0
    file_path = os.path.join(folder_path, filename)
    with pdfplumber.open(file_path) as pdf:  
        # print(f'{filename} 페이지 수 : {len(pdf.pages)}')
        for page in pdf.pages:  
            text = page.extract_text()
            
            if text.strip():  # 텍스트가 있는 경우에만 추가  
                raw_documents.append(Document(page_content=text, metadata={"page": page.page_number, "file": filename}, id=page.page_number))
            else:
                error_cnt += 1
            
            if error_cnt > 10:
                break
    
    return raw_documents        


def main():
    filename = f"요양보호사+양성+표준교재(2023년+개정판).pdf"

    all_text = readPdf(filename)
    
    print(all_text)
    

if __name__ == "__main__":
    main()