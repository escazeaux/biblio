# config.py

"""
CONFIG.py
- one variable / line
- example: DEBUG = True
- loaded in the __init__.py

BIGGER APPS:
  - have different config.py files for tests, dev & prod
  - put them in a config directory (use classes & inheritance)

SECURITY:
  - passwords, secret keys... should remain private
  - => instance/config.py file, NOT pushed to version control.
"""


# Enable Flask's debugging features. Should be False in production
DEBUG = True
MAX_CONTENT_LENGTH = 3 * 1024 * 1024
SECRET_KEY = 'mySecretKey'
SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
