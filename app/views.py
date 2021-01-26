# views.py

from flask import render_template

from app import app

TEAM = [('Brais', 'Crispr/CAS 9 scientist', 'brais.jpg'),
        ('Yew Mun', 'Bioinformatics researcher', 'yewmun.jpg'),
        ('Pascal', 'Serial entrepreneur', 'pascal.jpg')]

import os
import PyPDF2
DIR_PATH = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = DIR_PATH + '/uploads/'

@app.route('/')
def index():
    return render_template("index.html", team=TEAM)

@app.route("/album")
def album():
    LIST_OF_ARTICLES = os.listdir(UPLOAD_FOLDER)
    print(LIST_OF_ARTICLES)
    return render_template('album.html',list_of_articles=LIST_OF_ARTICLES, nb_of_articles = range(len(LIST_OF_ARTICLES)))


@app.route('/album_view/<article_name>')
def affiche_article(article_name):
    with open(UPLOAD_FOLDER + article_name, 'rb') as myPdf:
        pdfReader = PyPDF2.PdfFileReader(myPdf)
        page_one = pdfReader.getPage(0)
        text = page_one.extractText()
    return render_template('album_view.html', article_name = article_name, article_text = text[:1500])
