from flask import Blueprint
from config import STATICFILES_DIR,TEMPLATES_DIR


views = Blueprint('views', __name__,
                  static_folder=STATICFILES_DIR,
                  template_folder=TEMPLATES_DIR)


@views.route('/')
def index():
    return 'Hello, World'
