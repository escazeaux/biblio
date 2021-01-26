# run.py

"""
To use the command flask run like we did before, we would need to set the FLASK_APP environment variable to run.py, like so:

$ set FLASK_APP=run.py (WINDOWS) export (LINUX/MAC)
$ flask run
"""

from app import app

if __name__ == '__main__':
    app.run()
