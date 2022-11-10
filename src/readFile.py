from PIL import Image
from pytesseract import pytesseract


def read_file(image_path):
    #Define path to tessaract.exe
    print(image_path)
    path_to_tesseract = r'src/Tesseract-OCR/tesseract.exe'
    #Define path to image
    #path_to_image = 'C:/Users/manvithakankata/Downloads/text_summarizer/image2.jpg'
    #Point tessaract_cmd to tessaract.exe
    pytesseract.tesseract_cmd = path_to_tesseract
    #Open image with PIL
    img = Image.open(image_path)
    #Extract text from image
    text = pytesseract.image_to_string(img)
    return text


