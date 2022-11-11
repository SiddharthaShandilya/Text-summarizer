FROM python:3.7
COPY . /app
WORKDIR /app
RUN sudo apt update sudo apt install tesseract-ocr && sudo apt install imagemagick
RUN pip install -r requirements.txt
EXPOSE $PORT
CMD gunicorn --workers=4 --bind 0.0.0.0:$PORT app:app