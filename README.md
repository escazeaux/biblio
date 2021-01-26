https://morioh.com/p/5d8eca44372e

VIRTUAL ENV
- python -m venv myvenv
- myvenv\Scripts\activate (Windows) or source myvenv/bin/activate (Mac)

DEPENDENCIES
- pip install flask flask-sqlalchemy flask-login
or pip install  --requirement path/requirements.txt

in fact, installing Flask also installs a few other dependencies, which you will see when you run
- pip freeze
  (=> Click itsdangerous Jinja2 MarkupSafe Werkzeug)
    Click         (Command Line Interface Creation Kit) => allows you to add custom shell commands for your app
    itsdangerous  provides security when sending data using cryptographical signing
    Jinja2        template engine for Python
    MarkupSafe    HTML string handling library
    Werkzeug      utility library for WSGI, a protocol that ensures web apps and web servers can communicate effectively


FLASK ENV VARIABLES
Windows CMD:
  set FLASK_APP=run.py (WINDOWS) or export  (LINUX, MAC)
  set FLASK_DEBUG=1

  flask run
The flask command is separate from the flask.run method. It doesn't see the app or its configuration. To change the host and port, pass them as options to the command.
- flask run -h localhost -p 3000


ALTERNATIVE (DANS LAQUELLE ON CONTROLE MIEUX LES CHOSES [notamment le port] sans avoir à passer de variables d'environnement):
app.run(port=1234) dans app.py
ET PUIS python app.py
