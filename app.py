from __future__ import unicode_literals
from flask import Flask,flash,render_template,url_for,request,redirect
from readFile import read_file
import os
from werkzeug.utils import secure_filename

from spacy_summarization import text_summarizer
from nltk_summarization import nltk_summarizer
import time
import spacy
nlp = spacy.load("en_core_web_sm")
app = Flask(__name__)

app.secret_key = "secret key"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

path = os.getcwd()
UPLOAD_FOLDER = os.path.join(path, 'uploads')

if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'csv','pdf'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Web Scraping Pkg
from bs4 import BeautifulSoup
from urllib.request import urlopen


# Sumy Pkg
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

# Sumy 
def sumy_summary(docx):
	parser = PlaintextParser.from_string(docx,Tokenizer("english"))
	lex_summarizer = LexRankSummarizer()
	summary = lex_summarizer(parser.document,3)
	summary_list = [str(sentence) for sentence in summary]
	result = ' '.join(summary_list)
	return result


# Reading Time
def readingTime(mytext):
	total_words = len([ token.text for token in nlp(mytext)])
	estimatedTime = total_words/200.0
	return estimatedTime

# Fetch Text From Url
def get_text(url):
	page = urlopen(url)
	soup = BeautifulSoup(page)
	fetched_text = ' '.join(map(lambda p:p.text,soup.find_all('p')))
	return fetched_text

@app.route('/')
def index():
	return render_template('index.html')


@app.route('/analyze',methods=['GET','POST'])
def analyze():
	start = time.time()
	if request.method == 'POST':
		rawtext = request.form['rawtext']
		final_reading_time = readingTime(rawtext)
		final_summary = text_summarizer(rawtext)
		summary_reading_time = readingTime(final_summary)
		end = time.time()
		final_time = end-start
	return render_template('index.html',ctext=rawtext,final_summary=final_summary,final_time=final_time,final_reading_time=final_reading_time,summary_reading_time=summary_reading_time)

@app.route('/analyze_url',methods=['GET','POST'])
def analyze_url():
	start = time.time()
	if request.method == 'POST':
		raw_url = request.form['raw_url']
		rawtext = get_text(raw_url)
		final_reading_time = readingTime(rawtext)
		final_summary = text_summarizer(rawtext)
		summary_reading_time = readingTime(final_summary)
		end = time.time()
		final_time = end-start
	return render_template('index.html',ctext=rawtext,final_summary=final_summary,final_time=final_time,final_reading_time=final_reading_time,summary_reading_time=summary_reading_time)



@app.route('/compare_summary')
def compare_summary():
	return render_template('compare_summary.html')

@app.route('/comparer',methods=['GET','POST'])
def comparer():
	start = time.time()
	if request.method == 'POST':
		rawtext = request.form['rawtext']
		final_reading_time = readingTime(rawtext)
		final_summary_spacy = text_summarizer(rawtext)
		summary_reading_time = readingTime(final_summary_spacy)
		#NLTK
		final_summary_nltk = nltk_summarizer(rawtext)
		summary_reading_time_nltk = readingTime(final_summary_nltk)
		# Sumy
		final_summary_sumy = sumy_summary(rawtext)
		summary_reading_time_sumy = readingTime(final_summary_sumy) 

		end = time.time()
		final_time = end-start
	return render_template('compare_summary.html',ctext=rawtext,final_summary_spacy=final_summary_spacy,final_summary_nltk=final_summary_nltk,final_time=final_time,final_reading_time=final_reading_time,summary_reading_time=summary_reading_time,final_summary_sumy=final_summary_sumy,summary_reading_time_sumy=summary_reading_time_sumy,summary_reading_time_nltk=summary_reading_time_nltk)

@app.route('/upload_file',methods=['GET','POST'])

def upload_compare():
	if request.method == 'POST':
		start= time.time()
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
			rawtext=read_file(os.path.join(UPLOAD_FOLDER,filename),filename)
			final_reading_time = readingTime(rawtext)
			final_summary_spacy = text_summarizer(rawtext)
			summary_reading_time = readingTime(final_summary_spacy)
			#NLTK
			final_summary_nltk = nltk_summarizer(rawtext)
			summary_reading_time_nltk = readingTime(final_summary_nltk)
			# Sumy
			final_summary_sumy = sumy_summary(rawtext)
			summary_reading_time_sumy = readingTime(final_summary_sumy) 
			end = time.time()
			final_time = end-start
			return render_template('compare_summary.html',ctext=rawtext,final_summary_spacy=final_summary_spacy,final_summary_nltk=final_summary_nltk,final_time=final_time,final_reading_time=final_reading_time,summary_reading_time=summary_reading_time,final_summary_sumy=final_summary_sumy,summary_reading_time_sumy=summary_reading_time_sumy,summary_reading_time_nltk=summary_reading_time_nltk)
		else:
			flash('Allowed file types are txt, pdf, png, jpg, jpeg, csv, pdf')
			return redirect(request.url)


@app.route('/upload')
def upload():
	return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_file():
	start = time.time()
	if request.method == 'POST':
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
			rawtext=read_file(os.path.join(UPLOAD_FOLDER,filename),filename)
			final_reading_time = readingTime(rawtext)
			final_summary = text_summarizer(rawtext)
			summary_reading_time = readingTime(final_summary)
			end = time.time()
			final_time = end-start
			return render_template('upload.html',ctext=rawtext,final_summary=final_summary,final_time=final_time,final_reading_time=final_reading_time,summary_reading_time=summary_reading_time)
		else:
			flash('Allowed file types are txt, pdf, png, jpg, jpeg, csv, pdf')
			return redirect(request.url)

@app.route('/about')
def about():
	return render_template('index.html')

if __name__ == '__main__':
	app.run(debug=True)