# views.py

from flask import render_template, redirect, url_for, request
from werkzeug.utils import secure_filename

from app import app

"""
@app.route('/')
@app.route('/dashboard')
@app.route('/signin')
@app.route('/upload')
@app.route('/register')
@app.route("/album")
@app.route('/album_view/<article_name>')

A FAIRE:
- upload article pdf (avec contrôle type fichier + taille + nombre de fichier totaux (max 10?)
- delete article (avec contrôle des droits)
- user management
- dashboard/admin management
- user profile
"""

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    """
    Checks the filename for allowed file extension.
    If file type is supported the function returns True otherwise it returns False.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


import os
import PyPDF2
DIR_PATH = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = DIR_PATH + '/uploads/'

from werkzeug.exceptions import RequestEntityTooLarge

@app.errorhandler(413)
@app.errorhandler(RequestEntityTooLarge)
def app_handle_413(e):
    return 'File Too Large', 413



@app.route('/')
def index():
    TEAM = [('Brais', 'Crispr/CAS 9 scientist', 'brais.jpg'),
            ('Yew Mun', 'Bioinformatics researcher', 'yewmun.jpg'),
            ('Pascal', 'Serial entrepreneur', 'pascal.jpg')]
    return render_template("index.html", team=TEAM)

@app.route('/signin')
def signin():
    return render_template("signin.html")

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """
    cf. https://viveksb007.wordpress.com/2018/04/07/uploading-processing-and-downloading-files-in-flask/
    """
    if request.method == 'POST':
        if 'file' not in request.files:
            print('No file attached in request')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print('No file selected')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print(os.path.join(UPLOAD_FOLDER, filename))
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return redirect(url_for('album'))
    max_size_Mo = int(app.config['MAX_CONTENT_LENGTH'] / 1024 / 1024)
    return render_template("upload.html", max_size_Mo = max_size_Mo)

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/dashboard')
def dashboard():
    DATA = [[1001, 'Lorem', 'ipsum', 'dolor', 'sit'],
    [1002, 'amet', 'consectetur', 'adipiscing', 'elit'],
    [1003, 'Integer', 'nec', 'odio', 'Praesent'],
    [1003, 'libero', 'Sed', 'cursus', 'ante'],
    [1004, 'dapibus', 'diam', 'Sed', 'nisi'],
    [1005, 'Nulla', 'quis', 'sem', 'at'],
    [1006, 'nibh', 'elementum', 'imperdiet', 'Duis'],
    [1007, 'sagittis', 'ipsum', 'Praesent', 'mauris'],
    [1008, 'Fusce', 'nec', 'tellus', 'sed'],
    [1009, 'augue', 'semper', 'porta', 'Mauris'],
    [1010, 'massa', 'Vestibulum', 'lacinia', 'arcu'],
    [1011, 'eget', 'nulla', 'Class', 'aptent'],
    [1012, 'taciti', 'sociosqu', 'ad', 'litora'],
    [1013, 'torquent', 'per', 'conubia', 'nostra'],
    [1014, 'per', 'inceptos', 'himenaeos', 'Curabitur'],
    [1015, 'sodales', 'ligula', 'in', 'libero'],
    ]
    return render_template("dashboard.html", data=DATA)

@app.route("/album")
def album():
    LIST_OF_ARTICLES = os.listdir(UPLOAD_FOLDER)
    print(LIST_OF_ARTICLES)
    return render_template('album.html',list_of_articles=LIST_OF_ARTICLES, nb_of_articles = range(len(LIST_OF_ARTICLES)))


@app.route('/album_view/<article_name>')
def show_article(article_name):
    with open(UPLOAD_FOLDER + article_name, 'rb') as myPdf:
        pdfReader = PyPDF2.PdfFileReader(myPdf)
        page_one = pdfReader.getPage(0)
        text = page_one.extractText()
    return render_template('album_view.html', article_name = article_name, article_text = text[:1500])

@app.route('/album_delete/<article_name>')
def delete_article(article_name):
    if os.path.isfile(UPLOAD_FOLDER + article_name):
        os.remove(UPLOAD_FOLDER + article_name)
    return render_template('album_delete.html', article_name = article_name)
