import os
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
from src.readFile import read_file
from src.tsummarizer import nltk_summarizer
from src.doc_layout import doc_layout


app=Flask(__name__)

app.secret_key = "secret key"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

path = os.getcwd()
# file Upload
UPLOAD_FOLDER = os.path.join(path, 'uploads')

if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'csv','pdf'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        print("\n post method called \n")
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):

            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File successfully uploaded')
            #checking the layout of the image
            img_path = os.path.join(UPLOAD_FOLDER,filename)
            layout = doc_layout(img_path)
            # converting the image uploaded to text
            text=read_file(img_path,filename)
            #print(text)
            sum_text=nltk_summarizer(text)
            
            img_analysis = {"layout": layout, "Extracted_text": text, "Summarized_text": sum_text}

            return layout
        else:
            flash('Allowed file types are txt, pdf, png, jpg, jpeg, csv, pdf')
            return redirect(request.url)


if __name__ == "__main__":
    app.run(host = '127.0.0.1',port = 5000, debug = True)