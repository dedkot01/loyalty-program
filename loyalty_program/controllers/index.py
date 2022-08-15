from flask import Blueprint, render_template


index_page = Blueprint('index_page', __name__, template_folder='templates')


@index_page.route('/')
def index():
    return render_template('index.html')
