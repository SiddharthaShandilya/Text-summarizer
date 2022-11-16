from PIL import Image
from pytesseract import pytesseract
import PyPDF2

def read_file(path,filename):
    #Define path to tessaract.exe
    path_to_tesseract = r'src/Tesseract-OCR/tesseract.exe' # here put the name of tesseract ocr files
    extension=filename.rsplit('.', 1)[1].lower()
    if extension in ('jpg','jpeg','png'):
        #Define path to image
        path_to_image = path
        #Point tessaract_cmd to tessaract.exe
        pytesseract.tesseract_cmd = path_to_tesseract
        #Open image with PIL
        img = Image.open(path_to_image)
        #Extract text from image
        text = pytesseract.image_to_string(img)
        return text
    elif extension=='pdf':
        # creating a pdf file object
        pdfFileObj = open(path, 'rb')
        # creating a pdf reader object
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        # creating a page object
        pageObj = pdfReader.getPage(0)
        return pageObj.extractText()
    elif extension=='txt':
        fileObj=open(path,'r')
        return fileObj.read()

<<<<<<< HEAD

=======
>>>>>>> b720957280014574aad85c5c05e90265d17ef3d7
