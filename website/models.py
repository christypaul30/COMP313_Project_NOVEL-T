from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
# This file contains all models used by the application

# -----------------------------------------------------------------------------------------------
# class example(db.Model):                                                                      |
#     __tablename__ = 'exampleTable'                                                            |
#     objects_id = db.Column(db.Integer, primary_key=True)                                      |
#     persons_name = db.Column(db.String(50))                                                   |
#     time_when_created = db.Column(db.DateTime(timezone=True), default=func.now)               |
#                                                                                               |
#     __init__ is the constructor for the class example                                         |
#     object_id is not needed since database auto creates ID                                    |
#     time_when_created is set to None since database will overwrite it on object creation      |
#                                                                                               |
#     def __init__(self, persons_name, time_when_created=None):                                 |
#         self.persons_name = persons_name                                                      |
#         self.time_when_created = time_when_created                                            |
# ------------------------------------------------------------------------------------------------


class CharacterSheet(db.Model):
    __tablename__ = 'charactersheet'
    id = db.Column(db.Integer, primary_key=True)
    character = db.Column(db.String(50))
    character_level = db.Column(db.Integer)
    talents = db.Column(db.String())
    date = db.Column(db.DateTime(timezone=True), default=func.now)
    username = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, character, character_level=None, talents=None, date=None, username=None):
        self.character = character
        self.character_level = character_level
        self.talents = talents
        self.date = date
        self.username = username


class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    book_title = db.Column(db.String(150), unique=True, nullable=False)
    author = db.Column(db.Integer, db.ForeignKey('user.id'))
    prologue = db.Column(db.String, nullable=True)
    publish_date = db.Column(db.DateTime(timezone=True),
                             default=func.now(), nullable=False)
    book_genres = db.relationship(
        'BookGenres', backref=db.backref('book_genres', lazy=True))
    book_chapters = db.relationship(
        'BookChapters', backref=db.backref('book_chapters', lazy=True))
    date_updated = db.Column(db.DateTime(timezone=True), nullable=False)
    visibility = db.Column(db.String, nullable=False)

    def __init__(self, book_title, author, visibility, prologue=None, book_genres=None, book_chapters=None, date_updated=None):
        if book_chapters is None:
            book_chapters = []
        if book_genres is None:
            book_genres = []
        self.book_title = book_title
        self.author = author
        self.prologue = prologue
        self.book_genres = book_genres
        self.book_chapters = book_chapters
        self.date_updated = date_updated
        self.visibility = visibility


class BookChapters(db.Model):
    __tablename__ = 'bookchapters'
    id = db.Column(db.Integer, primary_key=True)
    chapter_title = db.Column(db.String(150))
    context = db.Column(db.String(50000))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)

    def __init__(self, chapter_title, book_id, context=None):
        self.chapter_title = chapter_title
        self.context = context
        self.book_id = book_id


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    security_question = db.Column(db.String(150), nullable=True)
    security_answer = db.Column(db.String(150), nullable=True)
    sheets = db.relationship('CharacterSheet')
    book = db.relationship('Book', backref=db.backref('books', lazy=True))
    library = db.relationship(
        'Library', backref=db.backref('library', lazy=True))

    def __init__(self, email, username, password, security_question=None, security_answer=None, sheets=None, book=None):
        if book is None:
            book = []
        if sheets is None:
            sheets = []
        self.email = email
        self.username = username
        self.password = password
        self.security_question = security_question
        self.security_answer = security_answer
        self.sheets = sheets
        self.book = book


class BookGenres(db.Model):
    __tablename__ = 'bookgenres'
    id = db.Column(db.Integer, primary_key=True)
    book_title = db.Column(db.String(150), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    sci_fi = db.Column(db.Boolean(), nullable=False, default=False)
    fantasy = db.Column(db.Boolean(), nullable=False, default=False)
    romance = db.Column(db.Boolean(), nullable=False, default=False)
    action_adventure = db.Column(db.Boolean(), nullable=False, default=False)
    slice_of_life = db.Column(db.Boolean(), nullable=False, default=False)
    comedy = db.Column(db.Boolean(), nullable=False, default=False)
    tragedy = db.Column(db.Boolean(), nullable=False, default=False)
    mystery = db.Column(db.Boolean(), nullable=False, default=False)
    thriller = db.Column(db.Boolean(), nullable=False, default=False)
    horror = db.Column(db.Boolean(), nullable=False, default=False)
    isekai = db.Column(db.Boolean(), nullable=False, default=False)
    reincarnation = db.Column(db.Boolean(), nullable=False, default=False)
    transmigration = db.Column(db.Boolean(), nullable=False, default=False)
    historical = db.Column(db.Boolean(), nullable=False, default=False)
    military = db.Column(db.Boolean(), nullable=False, default=False)
    school = db.Column(db.Boolean(), nullable=False, default=False)
    spy = db.Column(db.Boolean(), nullable=False, default=False)
    martial_arts = db.Column(db.Boolean(), nullable=False, default=False)

    def __init__(self, book_title, book_id, sci_fi, fantasy, romance, action_adventure, slice_of_life, comedy, tragedy,
                 mystery, thriller,
                 horror, isekai, reincarnation, transmigration, historical, military, school, spy, martial_arts):
        self.book_title = book_title
        self.book_id = book_id
        self.sci_fi = sci_fi
        self.fantasy = fantasy
        self.romance = romance
        self.action_adventure = action_adventure
        self.slice_of_life = slice_of_life
        self.comedy = comedy
        self.tragedy = tragedy
        self.mystery = mystery
        self.thriller = thriller
        self.horror = horror
        self.isekai = isekai
        self.reincarnation = reincarnation
        self.transmigration = transmigration
        self.historical = historical
        self.military = military
        self.school = school
        self.spy = spy
        self.martial_arts = martial_arts

    def __attributes__(self):
        temp_attributes = list(self.__dict__.keys())
        del temp_attributes[0:1]
        attributes = list(temp_attributes)
        return attributes

    def toString(self):
        genre_dictionary = list(self.__dict__.items())
        string = ''
        genre_dictionary.pop(0)
        for element in genre_dictionary:
            if element[0] == "book_id" or element[0] == "book_title" or element[0] == "id":
                pass
            elif element[1] is True:
                string += element[0] + ", "
            else:
                pass
        return string[:-2]


class Library(db.Model):
    __tablename__ = 'library'
    id = db.Column(db.Integer, primary_key=True)
    book_title = db.Column(db.String(150), unique=False, nullable=False)
    book_id = db.Column(db.Integer, unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, book_title, book_id, user_id):
        self.book_title = book_title
        self.book_id = book_id
        self.user_id = user_id


class BookmarkedChapters(db.Model):
    __tablename__ = 'bookmarkedchapters'
    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column("chapter_id", db.ForeignKey(
        'bookchapters.id'), nullable=False)
    book_id = db.Column("book_id", db.ForeignKey('book.id'), nullable=False)
    user_id = db.Column("user_id", db.ForeignKey('user.id'), nullable=False)

    def __init__(self, chapter_id, book_id, user_id):
        self.chapter_id = chapter_id
        self.book_id = book_id
        self.user_id = user_id


class BookHistory(db.Model):
    __tablename__ = 'bookhistory'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column("user_id", db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column("book_id", db.ForeignKey('book.id'), nullable=False)
    last_chapter = db.Column("last_chapter", db.ForeignKey(
        'bookchapters.id'), nullable=True)

    def __init__(self, book_id, user_id, last_chapter=None):
        self.user_id = user_id
        self.book_id = book_id
        self.last_chapter = last_chapter

class Comments(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column("book_id", db.ForeignKey('book.id'), nullable=False)
    user_id = db.Column("user_id", db.ForeignKey('user.id'), nullable=False)
    username = db.Column("username", db.ForeignKey('user.username'), nullable=False)
    message = db.Column(db.String(360))

    def __init__(self, book_id, user_id, username, message):
        self.book_id = book_id
        self.user_id = user_id
        self.username = username
        self.message = message
