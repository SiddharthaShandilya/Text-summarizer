"""
Through this approach, we can get maximum correct results for any given document. 
Here we will be trying to extract information from an invoice using the exact same approach.
"""
# use this command to install open cv2
# pip install opencv-python

# use this command to install PIL
# pip install Pillow

from pytesseract import pytesseract
import cv2
from PIL import Image
import os


IMG_PATH = "uploads/template4.jpg"
TEXT_LIST = []

def marked_image_text(uploaded_img,line_items_coordinates ):
    path_to_tesseract = r'src/Tesseract-OCR/tesseract.exe' # here put the name of tesseract ocr files
    pytesseract.tesseract_cmd = path_to_tesseract
    for x in range(len(line_items_coordinates)):
        c = line_items_coordinates[x]
        # cropping image img = image[y0:y1, x0:x1]
        img = uploaded_img[c[0][1]:c[1][1], c[0][0]:c[1][0]]            
        #cv2.imshow("lined",img)
        # convert the image to black and white for better OCR
        ret,thresh1 = cv2.threshold(img,120,255,cv2.THRESH_BINARY)

        # pytesseract image to string to get results
        text = str(pytesseract.image_to_string(thresh1, config='--psm 6'))
        #print( text)
        TEXT_LIST.append(text)
    
    return TEXT_LIST


def mark_region(image_path=IMG_PATH):
    
    img = cv2.imread(image_path)
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9,9), 0)
    thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,11,30)

    # Dilate to combine adjacent text contours
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9,9))
    dilate = cv2.dilate(thresh, kernel, iterations=4)

    # Find contours, highlight text areas, and extract ROIs
    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    line_items_coordinates = []
    for c in cnts:
        area = cv2.contourArea(c)
        x,y,w,h = cv2.boundingRect(c)

        if y >= 600 and x <= 1000:
            if area > 10000:
                image = cv2.rectangle(img, (x,y), (2200, y+h), color=(255,0,255), thickness=3)
                line_items_coordinates.append([(x,y), (2200, y+h)])

        if y >= 2400 and x<= 2000:
            image = cv2.rectangle(img, (x,y), (2200, y+h), color=(255,0,255), thickness=3)
            line_items_coordinates.append([(x,y), (2200, y+h)])
            
    print(line_items_coordinates)
    text = marked_image_text(image, line_items_coordinates)
    cv2.imwrite("artifacts/cropped_image/marked_image.jpg", image)
    #print(f"marked text :{text}")
    return text



if __name__=="__main__":
    try:
        print("Calling information_extraction.py file")
        mark_region(image_path=IMG_PATH)
    except Exception as e:
        print(e)

