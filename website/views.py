from flask import Blueprint, render_template, jsonify, request, flash, session, url_for
from flask_login import login_required, current_user
from sqlalchemy import func
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import redirect
from website import db
from website.auth import verification
from website.models import Book, User, BookChapters, BookGenres, Library, BookHistory, BookmarkedChapters
import json
# This file SHOULD contain all Routes/Views that a non signed in user can see

views = Blueprint('views', __name__)


@views.route("view-chapter", methods=['POST', 'GET'])
def chapter_page():
    verification()
    chapter_id = request.args.get('chapter')
    chapter = BookChapters.query.filter_by(id=chapter_id).first()
    book = Book.query.filter_by(id=chapter.book_id).first()
    return render_template('chapter.html', user=current_user, chapter=chapter, book=book)


@views.route("edit-chapter", methods=['POST', 'GET'])
def edit_chapter():
    if request.method == "POST":
        # pulling information from form and assigning them
        chapter_id = request.form.get('chapter-id')
        book_id = request.form.get('book-id')
        chapter_title = request.form.get('form-title')
        context = request.form.get('form-context')
        # querying databases using assigned values above
        chapter = BookChapters.query.get(chapter_id)
        # updating values on the database
        chapter.chapter_title = chapter_title
        chapter.context = context
        db.session.commit()
        flash("changes saved", category="success")
        return redirect(url_for('views.simulator_page', bookId=book_id))

    chapter_id = request.args.get('chapterId')
    book_id = request.args.get('bookId')
    chapter = BookChapters.query.filter_by(id=chapter_id).first()
    book = Book.query.filter_by(id=book_id).first()
    return render_template('edit_chapter.html', user=current_user, chapter=chapter, book=book)


def profile_post_methods():
    if request.form.get('form') == 'email-modal':
        email = request.form.get('email-form-email')
        password = request.form.get('email-form-password')
        user = User.query.filter_by(email=current_user.email).first()
        if check_password_hash(user.password, password) and User.query.filter_by(email=email).first() is None:
            user.email = email
            db.session.commit()
            flash("email was updated", category="success")
        else:
            flash("passwords do not match or email already exists", category="error")

    if request.form.get('form') == 'username-modal':
        username = request.form.get('modal-username')
        password = request.form.get('modal-password')
        user = User.query.filter_by(email=current_user.email).first()
        if check_password_hash(user.password, password) and User.query.filter_by(username=username).first() is None:
            user.username = username
            db.session.commit()
            flash("username was updated", category="success")
        else:
            flash("username was taken or password did not match", category="error")

    if request.form.get('form') == 'password-modal':
        existing_password = request.form.get('existing-password')
        new_password = request.form.get('new-password')
        user = User.query.filter_by(email=current_user.email).first()
        if user and check_password_hash(user.password, existing_password):
            user.password = generate_password_hash(
                new_password, method='sha256')
            db.session.commit()
            flash("password has been updated", category="success")
        else:
            flash("error updating password, please try again", category="error")

    if request.form.get('form') == 'account-modal':
        confirmation = request.form.get('confirmation')
        if confirmation == 'Delete Account':
            user = User.query.filter_by(email=current_user.email).first()
            db.session.delete(user)
            db.session.commit()


@views.route('stats-page')
@login_required
def stats_page():
    return render_template("base.html", user=current_user)


@views.route('delete-book', methods=['POST'])
def delete_book():
    book = json.loads(request.data)
    bookId = book['bookId']
    book = Book.query.get(bookId)
    if book:
        if book.author == current_user.id:
            db.session.delete(book)
            db.session.commit()
            flash('book removed', category='success')
    return jsonify({})


@views.route('delete-chapter', methods=['POST', 'GET'])
def delete_chapter():
    data = json.loads(request.data)
    book_id = data['bookId']
    chapter_id = data['chapterId']
    book = Book.query.get(book_id)
    chapter = BookChapters.query.get(chapter_id)
    if chapter:
        if book.author == current_user.username:
            db.session.delete(chapter)
            db.session.commit()
        flash('chapter has been removed', category='success')
        return jsonify({})
    else:
        flash('chapter was not successfully removed', category='error')
        return jsonify({})


@views.route('edit-book', methods=['POST', 'GET'])
def edit_book():
    if request.method == 'POST':
        book_title = request.form.get('book-title')
        author = request.form.get('author')
        genre = request.form.get('genre')
        prologue = request.form.get('prologue')

        book = Book.query.filter_by(id=(request.args.get("bookId"))).first()

        book.book_title = book_title
        book.author = book.author
        book.prologue = prologue
        book.updated_date = func.now()

        db.session.commit()
        # updated_book = Book(id=book_id, book_title=book_title, author=author, prologue=prologue, publish_date=publish_date)
        # db.session.delete(book)
        # db.session.commit()
        # db.session.add(updated_book)
        # db.session.commit()
        flash("book has been successfully updated", category="Success")
        return render_template("book.html", user=current_user)
    """print("hello world! --------------------------")
    print(request.data.decode())
    bookId = Book.query.get(request.data.decode())
    return render_template("edit_book.html", user=current_user, book=bookId)"""
    book = Book.query.get(request.args.get("bookId"))
    return render_template("edit_book.html", user=current_user, book=book)


@views.route('backup-page')
def backup_page():
    return render_template("home.html", user=current_user)


@views.route('register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        verification()
        return render_template('home.html', user=current_user)
    return render_template("register.html", user=current_user)


@views.route('author-summary', methods=['POST', 'GET'])
def author_book_page():
    book = Book.query.get(request.args.get("bookId"))
    chapters = BookChapters.query.filter_by(book_id="bookId")
    if request.method == 'POST':
        chapter_title = request.form.get('chapter-title')
        context = request.form.get('chapter-context')
        book_id = book.id
        existing_chapters = BookChapters.query.filter_by(
            chapter_title=chapter_title).first()
        chapter = BookChapters(chapter_title=chapter_title,
                               context=context, book_id=book_id)
        if existing_chapters:
            flash("chapter has failed to upload", category="error")
        else:
            db.session.add(chapter)
            db.session.commit()
            flash("chapter has been added", category="success")
    return render_template("simulator.html", user=current_user, book=book)


@views.route('simulator', methods=['POST', 'GET'])
def simulator_page():
    verification()
    book = Book.query.get(request.args.get("bookId"))
    chapters = BookChapters.query.filter_by(book_id="bookId")
    book_genres = BookGenres.query.filter_by(
        book_id=(request.args.get("bookId"))).first()
    da_book_genres = BookGenres.query.filter_by(
        book_id=(request.args.get("bookId"))).first().toString()
    # print("columns")
    # print(BookGenres.__table__.columns.keys())
    if da_book_genres is None:
        da_book_genres = ''
    if request.method == 'GET':
        if current_user.is_authenticated:
            bookmarkedChapters = []
            for chapter in db.engine.execute(f"SELECT * FROM bookmarkedchapters WHERE user_id='{current_user.id}' AND book_id='{book.id}'"):
                bookmarkedChapters.append(chapter.chapter_id)
            if current_user.id == book.author:
                return render_template("simulator.html", user=current_user, book=book, chapters=chapters, book_genres=da_book_genres, bookmarkedChapters=bookmarkedChapters)
            else:
                return render_template("viewer_book_page.html", user=current_user, book=book, bookmarkedChapters=bookmarkedChapters)
        else:
            bookmarkedChapters = []
            return render_template("viewer_book_page.html", user=current_user, book=book, book_genres=da_book_genres, bookmarkedChapters=bookmarkedChapters)
    if request.method == 'POST':
        chapter_title = request.form.get('chapter-title')
        context = request.form.get('chapter-context')
        book_id = book.id
        existing_chapters = BookChapters.query.filter_by(
            chapter_title=chapter_title).first()
        chapter = BookChapters(chapter_title=chapter_title,
                               context=context, book_id=book_id)
        if existing_chapters:
            flash("chapter has failed to upload", category="error")
        else:
            db.session.add(chapter)
            db.session.commit()
            flash("chapter has been added", category="success")

    return render_template("viewer_book_page.html", user=current_user, book=book, book_genres=da_book_genres)


@views.route('profile', methods=['POST', 'GET'])
@login_required
def profile_page():
    if request.method == 'POST':
        profile_post_methods()
    return render_template("user_profile.html", user=current_user)


@views.route('calender')
def calender_page():
    return render_template("calender.html", user=current_user)


@views.route('book', methods=['POST', 'GET'])
def book_page():
    verification()
    return render_template("book.html", user=current_user)


@views.route('password_reset')
def reset_page():
    return render_template("password_reset.html", user=current_user)


@views.route('bookmark-chapter', methods=['POST'])
def bookmark_chapter():
    if current_user.is_authenticated:
        bookmark = json.loads(request.data)
        print(bookmark)
        bookId = bookmark['bookId']
        chapterId = bookmark['chapterId']
        book = Book.query.get(bookId)
        if book:
            chapter = BookChapters.query.get(chapterId)
            if chapter:
                existing_chapter_bookmarked = BookmarkedChapters.query.filter_by(
                    book_id=bookId, chapter_id=chapterId, user_id=current_user.id).first()
                if existing_chapter_bookmarked:
                    db.session.delete(existing_chapter_bookmarked)
                    db.session.commit()
                    flash('Chapter bookmark removed.', category='success')
                else:
                    insert_request = BookmarkedChapters(
                        chapter_id=chapterId, book_id=bookId, user_id=current_user.id
                    )
                    db.session.add(insert_request)
                    db.session.commit()
                    flash('Chapter has been successfully bookmarked!',
                          category='success')
    else:
        flash('You must be logged in to bookmark chapters!',
              category='error')
    return jsonify({})


@views.route('bookmark-book', methods=['POST'])
def bookmark_book():
    if current_user.is_authenticated:
        bookmark = json.loads(request.data)
        bookId = bookmark['bookId']
        book = Book.query.get(bookId)
        if book:
            insert_request = Library(
                book_title=book.book_title, book_id=bookId, user_id=current_user.id)
            existing_book_in_library = Library.query.filter_by(
                book_id=bookId, user_id=current_user.id).first()
            if existing_book_in_library:
                db.session.delete(existing_book_in_library)
                db.session.commit()
                flash('book removed from personal library', category='success')
            else:
                db.session.add(insert_request)
                db.session.commit()
                flash('book added to personal library', category='success')
    else:
        flash('You must be logged in to bookmark books!',
              category='error')
    return jsonify({})


@views.route('/bookhistory/<bid>', methods=['GET'])
def add_book_read_history(bid):
    if current_user.is_authenticated:
        if db.session.query(BookHistory).filter(BookHistory.book_id == bid, BookHistory.user_id == current_user.id).first():
            return jsonify({'msg': 'history exists'})
        db.session.add(BookHistory(bid, current_user.id))
        db.session.commit()
        return jsonify({'msg': 'history added'})


@views.route('/bookhistory', methods=['GET'])
def bookhistory_page():
    if current_user.is_authenticated:
        books = []
        for history in db.engine.execute(f"SELECT * FROM bookhistory WHERE user_id='{current_user.id}'"):
            book = db.session.query(Book).filter(
                Book.id == history.book_id).first()
            if hasattr(history, "last_chapter"):
                book.last_chapter = str(history.last_chapter)
            books.append(book)
        return render_template("book_history.html", user=current_user, books=books)
    else:
        flash('You must be logged in to check the book history!',
              category='error')
        return redirect("/")


@views.route('/bookhistory/<bid>/<cid>', methods=['GET'])
def add_last_chapter(bid, cid):
    if current_user.is_authenticated:
        h = db.session.query(BookHistory).filter(
            BookHistory.book_id == bid, BookHistory.user_id == current_user.id
        ).first()
        h.last_chapter = cid
        db.session.commit()
        return jsonify({'msg': 'last chapter updated'})
