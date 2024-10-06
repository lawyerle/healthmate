from pdf2image import convert_from_path
import pytesseract
import os
from PIL import Image, ImageEnhance, ImageFilter
from langchain.schema import Document
from openai import OpenAI

def init_api():
    with open("chatgpt_kict2409.env") as env:
          for line in env:
               key, value = line.strip().split("=")
               os.environ[key] = value

    os.environ["OPENAI_API_KEY"] = os.environ.get("API_KEY")


def extract_text_from_converted_pdf(filename) -> list:
    images = convert_from_path(filename)
    
    custom_config = r'--oem 3 --psm 6'
    raw_documents = []
    all_text = []

    for index, image in enumerate(images):
        # file_name = os.path.join(output_dir, f'page_{index+1}.png')
        image = image.convert('L')
        image = image.filter(ImageFilter.SHARPEN)
        image = ImageEnhance.Contrast(image).enhance(2)
        # image.save(file_name, 'PNG')
        
        text = pytesseract.image_to_string(image, config=custom_config, lang='kor+eng')
        
        # client = OpenAI()
        response = OpenAI().chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "너는 아주 유능한 어시스턴트야."},
                {"role": "user", "content": f"다음 텍스트의 내용을 한글로 분석해줘: {text}"}
            ]
        )
        text = response.choices[0].message.content

        # print(f'{index}, {text}')
        
        raw_documents.append(Document(page_content=text, metadata={"page": index, "file": filename}))
    
    return raw_documents


def main(): 
    init_api()
    result_txt = extract_text_from_converted_pdf(f'example.pdf')
    print(result_txt)


if __name__ == "__main__":
    main()
