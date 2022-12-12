from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import func, column
from werkzeug.security import generate_password_hash, check_password_hash
import json
import website
from . import db
from .models import User, Book, BookGenres
from sqlalchemy.sql import text
# This file SHOULD contain all Web routes/views that would require users to be signed in
auth = Blueprint('auth', __name__)

def convert(element):
    print("to be decided")


def verification():
    if request.method == 'POST':
        if request.form.get('type') == 'login':
            email = request.form.get('email')
            password = request.form.get('password')
            user = User.query.filter_by(email=email).first()
            if user:
                if check_password_hash(user.password, password):
                    login_user(user, remember=True)
                    flash(f'Welcome back {current_user.username}', category='success')
                else:
                    flash('login failed', category='error')
            else:
                flash('login failed', category='error')
        if request.form.get('type') == 'register':
            email = request.form.get('email')
            username = request.form.get('username')
            password1 = request.form.get('password1')
            password2 = request.form.get('password2')

            user = User.query.filter_by(email=email).first()
            user_name = User.query.filter_by(username=username).first()

            if user:
                flash('email already exists', category='error')
            if user_name:
                flash('username is taken', category='error')
            if len(email) < 7:
                flash('The email must be greater than 7 characters', category='error')
            if len(username) < 3:
                flash('name must me greater than 3 characters', category='error')
            if len(password1) < 8:
                flash('password must be greater than 8 characters', category='error')
            elif password1 != password2:
                flash('passwords do not match', category='error')
            else:
                new_user = User(email=email,
                                username=username,
                                password=generate_password_hash(password1, method='sha256'))

                db.session.add(new_user)
                db.session.commit()
                user = User.query.filter_by(email=email).first()
                login_user(user, remember=True)
                flash(f'Hello {current_user.username} welcome to novel-t!', category='success')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        verification()
        if current_user.is_authenticated:
            return redirect(url_for('auth.home'))
    return render_template("login.html", user=current_user)


@auth.route('/', methods=['GET', 'POST'])
def home():
    if request.form.get('type') == 'search':
        print("this was hit")
        form = request.form
        search_value = form['search_string']
        search = "%{}%".format(search_value)
        result = Book.query.filter(Book.book_title.like(search)).all()
        print(result)
        return render_template('home.html', books=result, user=current_user)
    if not current_user.is_authenticated:
        verification()
        
        if current_user.is_authenticated:
        if not current_user.accepted_terms:
            return redirect(url_for('views.terms_of_service_page'))
        
    books = Book.query.order_by(Book.book_title)
    return render_template("home.html", user=current_user, books=books)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    # return redirect('/') also works but if changed in future would need to come back and code it again
    return redirect(url_for('auth.home'))


@auth.route('/delete-account', methods=['POST', 'GET'])
def delete_account():
    print('delete account reached')
    if request.method == 'POST':
        delete_existing_user = User.query.filter_by(username=current_user.username).first()
        if delete_existing_user:
            db.session.remove(delete_existing_user)
            db.session.commit()
        else:
            flash('Error removing account.', category='error')
            return redirect(url_for('views.profile'))


@auth.route('/create-account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        security_question = request.form.get('security_question')
        security_answer = request.form.get('security_answer')

        user = User.query.filter_by(email=email).first()
        user_name = User.query.filter_by(username=username).first()
        if user:
            flash('email already exists', category='error')
        elif user_name:
            flash('username is taken', category='error')
        elif len(email) < 7:
            flash('The email must be greater than 7 characters', category='error')
        elif len(username) < 3:
            flash('name must me greater than 3 characters', category='error')
        elif len(password1) < 8:
            flash('password must be greater than 8 characters', category='error')
        elif password1 != password2:
            flash('passwords do not match', category='error')
        elif len(security_question) < 10:
            flash("security question isn't long enough", category='error')
        elif len(security_answer) < 3:
            flash("security answer isn't long enough", category='error')
        else:
            new_user = User(email=email,
                            username=username,
                            password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            user = User.query.filter_by(email=email).first()
            login_user(user, remember=True)
            flash('More fodder for the skittergate i see...', category='success')
            #  return redirect('/') also works but if changed in future would need to come back and code it again
            return redirect(url_for('auth.home'))

    return render_template("sign_up.html", user=current_user)


@auth.route('add_book', methods=['Get', 'Post'])
def add_book_page():
    if request.method == 'POST':
        genre_object = {}
        for item in request.form.items():
            if item[1] == "True":
                genre_object[item[0]] = bool(item[1])
            else:
                genre_object[item[0]] = item[1]
        q = website.db.session.query(User).filter(User.username == current_user.username)
        existing_book = website.db.session.query(Book).filter(Book.book_title == genre_object.get("book_title")).first()
        website.db.session.query(q.exists())
        if existing_book:
            flash('book already exists in your collection.', category='error')
        else:
            new_book = Book(
                book_title=genre_object.get("book_title"),
                author=current_user.id,
                prologue=genre_object.get("prologue"),
                date_updated=func.now(),
                visibility=request.form.get("visibility")
            )
            db.session.add(new_book)
            db.session.commit()
            new_genre_entry = BookGenres(
                book_title=genre_object.get("book_title").title(),
                book_id=new_book.id,
                sci_fi=genre_object.get("sci_fi"),
                fantasy=genre_object.get("fantasy"),
                romance=genre_object.get("romance"),
                action_adventure=genre_object.get("action_adventure"),
                slice_of_life=genre_object.get("slice_of_life"),
                comedy=genre_object.get("comedy"),
                tragedy=genre_object.get("tragedy"),
                mystery=genre_object.get("mystery"),
                thriller=genre_object.get("thriller"),
                horror=genre_object.get("horror"),
                isekai=genre_object.get("isekai"),
                reincarnation=genre_object.get("reincarnation"),
                transmigration=genre_object.get("transmigration"),
                historical=genre_object.get("historical"),
                military=genre_object.get("military"),
                school=genre_object.get("school"),
                spy=genre_object.get("spy"),
                martial_arts=genre_object.get("martial_arts")
            )
            db.session.add(new_genre_entry)
            db.session.commit()
            flash('Book was successfully added to your collection.', category='success')
            return redirect(url_for('views.book_page'))


    genre_table_keys = list(BookGenres.__table__.columns.keys())
    del genre_table_keys[0:3]
    genres = []
    form_checkbox_names = []
    for i in genre_table_keys:
        if "_" in i:
            i = i.replace('_', ' ')
            print(i)
        genres.append(i)
    for i in range(1, genres.__len__()+1):
        form_checkbox_names.append("checkbox" + str(i))
    return render_template('add_book.html', user=current_user, form_checkboxes=genres, form_checkbox_names=form_checkbox_names)
