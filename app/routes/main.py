from flask import Blueprint, render_template
from flask_login import login_required
from app.models import Book

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/index')
def index():
    books = Book.query.limit(10).all()
    return render_template('index.html', title='Home', books=books)
