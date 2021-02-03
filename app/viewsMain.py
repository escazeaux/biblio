# viewsMain.py

from flask import Blueprint, render_template, redirect, url_for, request, current_app

from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    TEAM = [('Brais', 'Crispr/CAS 9 scientist', 'brais.jpg'),
            ('Yew Mun', 'Bioinformatics researcher', 'yewmun.jpg'),
            ('Pascal', 'Serial entrepreneur', 'pascal.jpg')]
    return render_template('index.html', team=TEAM)

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

"""
TODO = FAIRE UN EXEMPLE D'EXTRACTION (par exemple, la table des matières)
+ mettre la transfo dans utils et expliquer à Brais & Yew Mun que modifier (en particulier; virtual env + requirements + format retour: soit image, soit texte)
{{url_for('main.album')}}
@main.route('/extract/info/article')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)
"""

"""
@main.route('/')
@main.route('/profile')

@main.route('/dashboard')
@main.route('/signin')
@main.route('/upload')
@main.route('/register')
@main.route("/album")
@main.route('/album_view/<article_name>')

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

@main.errorhandler(413)
@main.errorhandler(RequestEntityTooLarge)
def app_handle_413(e):
    return 'File Too Large', 413


@main.route('/upload', methods=['GET', 'POST'])
@login_required
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
            return redirect(url_for('main.album'))
    max_size_Mo = int(current_app.config['MAX_CONTENT_LENGTH'] / 1024 / 1024)
    return render_template("upload.html", max_size_Mo = max_size_Mo)


@main.route('/dashboard')
@login_required
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

@main.route("/album")
def album():
    LIST_OF_ARTICLES = os.listdir(UPLOAD_FOLDER)
    print(LIST_OF_ARTICLES)
    return render_template('album.html',list_of_articles=LIST_OF_ARTICLES, nb_of_articles = range(len(LIST_OF_ARTICLES)))


@main.route('/album_view/<article_name>')
def show_article(article_name):
    with open(UPLOAD_FOLDER + article_name, 'rb') as myPdf:
        pdfReader = PyPDF2.PdfFileReader(myPdf)
        page_one = pdfReader.getPage(0)
        text = page_one.extractText()
    return render_template('album_view.html', article_name = article_name, article_text = text[:1500])

@main.route('/album_delete/<article_name>')
@login_required
def delete_article(article_name):
    if os.path.isfile(UPLOAD_FOLDER + article_name):
        os.remove(UPLOAD_FOLDER + article_name)
    return render_template('album_delete.html', article_name = article_name)
