from flask import Blueprint, render_template
from config import STATICFILES_DIR, TEMPLATES_DIR


views = Blueprint('views', __name__,
                  static_folder=STATICFILES_DIR,
                  template_folder=TEMPLATES_DIR)


@views.route('/')
def index():
    return 'Hello, World'


@views.route('/login/')
def login():
    print(STATICFILES_DIR)
    return render_template('login.html')