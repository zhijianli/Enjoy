from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql

pymysql.install_as_MySQLdb()

app = Flask(__name__)


class Config(object):
    """配置参数"""
    # 设置连接数据库的URL
    user = 'root'
    password = '123456'
    database = 'enjoy'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@47.98.124.127:3306/%s' % (user, password, database)

    # 设置sqlalchemy自动更跟踪数据库
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # 查询时会显示原始SQL语句
    app.config['SQLALCHEMY_ECHO'] = True

    # 禁止自动提交数据处理
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False


# 读取配置
app.config.from_object(Config)

# 创建数据库sqlalchemy工具对象
db = SQLAlchemy(app)


class Author(db.Model):
    # 定义表名
    __tablename__ = 'author'
    # 定义字段
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, index=True)
    author_avatar_url = db.Column(db.String(255), unique=True)

class Book(db.Model):
    # 定义表名
    __tablename__ = 'book'
    # 定义字段
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, index=True)
    wechat_book_id = db.Column(db.Integer)

class BookSentence(db.Model):
    # 定义表名
    __tablename__ = 'book_sentence'
    # 定义字段
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sentence = db.Column(db.String(255), unique=True, index=True)
    book_id = db.Column(db.Integer)
    book_name = db.Column(db.String(255))
    author_id = db.Column(db.Integer)
    author_name = db.Column(db.String(255))
    underline_num = db.Column(db.Integer)
    type = db.Column(db.Integer)
    comment = db.Column(db.String(255))
    wechat_book_id = db.Column(db.Integer)


def insert_book(wechat_book_id,book_name):
    # 插入一条数据
    with app.app_context():
        book = Book(wechat_book_id=wechat_book_id,name=book_name)
        db.session.add(book)
        db.session.commit()

def select_book_list():
    with app.app_context():
        book_list = Book.query.filter_by().all()
    return book_list

def select_book(wechat_book_id,book_name):
    with app.app_context():
        book_list = Book.query.filter_by(wechat_book_id=wechat_book_id,name=book_name).all()

    return book_list

def select_book_by_wechat_book_id(wechat_book_id):
    with app.app_context():
        book_list = Book.query.filter_by(wechat_book_id=wechat_book_id).all()

    return book_list

def insert_book_sentence(sentence,book_id,wechat_book_id,book_name,underline_num,type):
    with app.app_context():
        bookSentence = BookSentence(sentence=sentence,
                                    book_id=book_id,
                                    wechat_book_id=wechat_book_id,
                                    book_name=book_name,
                                    underline_num=underline_num,
                                    type=type)
        db.session.add(bookSentence)
        db.session.commit()

def select_book_sentence(sentence,wechat_book_id):
    with app.app_context():
        book_sentence_list = BookSentence.query.filter_by(sentence=sentence,wechat_book_id=wechat_book_id).all()

    return book_sentence_list

def select_book_sentence_by_wechat_id(wechat_book_id):
    with app.app_context():
        book_sentence_list = BookSentence.query.filter_by(wechat_book_id=wechat_book_id).all()

    return book_sentence_list

if __name__ == '__main__':

    # # 插入一条数据
    # with app.app_context():
    #     author1 = Author(name='弗洛伊德')
    #     db.session.add(author1)
    #     db.session.commit()

    # # 插入一条数据
    # with app.app_context():
    #     book = Book(name='天龙八部')
    #     db.session.add(book)
    #     db.session.commit()
    # 插入书籍名字到表中
    book_list = select_book(111,'天龙八部1')
    if len(book_list) == 0:
        insert_book(111,'天龙八部1')
    # book_sentence_list = select_book_sentence('两句名言1',11111)
    # if len(book_sentence_list) == 0:
    #     insert_book_sentence('两句名言1',1,11111,'天龙八部',119,1)

    # book_list = select_book_by_wechat_book_id(11111)
    # print(book_list[0].name)
