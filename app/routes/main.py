from flask import Blueprint, render_template, request, url_for
from flask_login import login_required
from app.models.models import Book
from app import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/index')
def index():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    author = request.args.get('author', '')
    isbn = request.args.get('isbn', '')
    publisher = request.args.get('publisher', '')
    year_start = request.args.get('year_start', type=int)
    year_end = request.args.get('year_end', type=int)

    query = Book.query
    if search:
        query = query.filter(Book.title.contains(search))
    if author:
        query = query.filter(Book.author.contains(author))
    if isbn:
        query = query.filter(Book.isbn == isbn)
    if publisher:
        query = query.filter(Book.publisher.contains(publisher))
    if year_start:
        query = query.filter(Book.publication_year >= year_start)
    if year_end:
        query = query.filter(Book.publication_year <= year_end)

    pagination = query.paginate(page=page, per_page=12, error_out=False)
    books = pagination.items

    next_url = url_for('main.index', page=pagination.next_num, search=search, author=author, isbn=isbn, publisher=publisher, year_start=year_start, year_end=year_end) \
        if pagination.has_next else None
    prev_url = url_for('main.index', page=pagination.prev_num, search=search, author=author, isbn=isbn, publisher=publisher, year_start=year_start, year_end=year_end) \
        if pagination.has_prev else None

    return render_template('index.html', title='Home', books=books, next_url=next_url, prev_url=prev_url, 
                           search=search, author=author, isbn=isbn, publisher=publisher, 
                           year_start=year_start, year_end=year_end)

@main_bp.route('/book/<isbn>')
def book_detail(isbn):
    book = Book.query.get_or_404(isbn)
    return render_template('book_detail.html', title=book.title, book=book)
