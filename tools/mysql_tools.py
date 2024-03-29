from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# 引入多条件查询
from sqlalchemy import and_,func
import pymysql

pymysql.install_as_MySQLdb()

app = Flask(__name__)


class Config(object):
    """配置参数"""
    # 设置连接数据库的URL
    user = 'root'
    password = 'Mocuiliniubi&*&123'
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
    author_id = db.Column(db.Integer)
    author_name = db.Column(db.String(255), unique=True, index=True)
    introduction = db.Column(db.String(1000), unique=True, index=True)
    book_cover_url = db.Column(db.String(255), unique=True, index=True)
    wechat_book_id = db.Column(db.Integer)
    type = db.Column(db.Integer)

class Tag(db.Model):
    # 定义表名
    __tablename__ = 'tag'
    # 定义字段
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), unique=True, index=True)


class BookTagRelation(db.Model):
    # 定义表名
    __tablename__ = 'book_tag_relation'
    # 定义字段
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    wechat_book_id = db.Column(db.Integer)
    book_id = db.Column(db.Integer)
    tag_id = db.Column(db.Integer)

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

class Video(db.Model):
    # 定义表名
    __tablename__ = 'video'
    # 定义字段
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(30))
    subtitle = db.Column(db.String(50))
    bilibili_title = db.Column(db.String(100))
    end = db.Column(db.String(100))
    comment_guide = db.Column(db.String(100))
    text = db.Column(db.String(2000))
    background_url = db.Column(db.String(500))
    bgm_name = db.Column(db.String(100))
    cover_url = db.Column(db.String(200))
    font_cover_ratio = db.Column(db.Integer)
    video_url = db.Column(db.String(200))
    bilibili_tid = db.Column(db.Integer)
    description = db.Column(db.String(1000))
    tag = db.Column(db.String(200))
    open_id = db.Column(db.String(100))
    status = db.Column(db.Integer)
    contribute_time = db.Column(db.String(30))

class PlatformToken(db.Model):
    # 定义表名
    __tablename__ = 'platform_token'
    # 定义字段
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    platform = db.Column(db.String(100), unique=True, index=True)
    refresh_token = db.Column(db.String(200), unique=True, index=True)
    access_token = db.Column(db.String(200), unique=True, index=True)

def insert_book(wechat_book_id,book_name,type):
    # 插入一条数据
    with app.app_context():
        book = Book(wechat_book_id=wechat_book_id,name=book_name,type=type)
        db.session.add(book)
        db.session.flush()
        book_id = book.id
        db.session.commit()
        return book_id


def update_book(wechat_book_id,author_name,book_cover_url,author_id,type):
    with app.app_context():
        Book.query.filter_by(wechat_book_id=wechat_book_id).update({"author_name": author_name,"book_cover_url": book_cover_url,"author_id":author_id,"type":type})
        db.session.commit()

def select_book_list():
    with app.app_context():
        book_list = Book.query.filter_by().all()
    return book_list

def select_book_by_condition(type,author_id,book_id_list):
    with app.app_context():
        book_list = Book.query.filter( (Book.type == type) if type else 1==1,
                                       (Book.author_id == author_id) if author_id else 1==1,
                                        Book.id.in_(book_id_list) if len(book_id_list) > 0 else 1==1
                                        ).all()

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

def batch_insert_book(book_sentence_list):
    with app.app_context():
        db.session.execute(
            BookSentence.__table__.insert(),
            [{"sentence":book_sentence[0] , "book_id":book_sentence[1] ,
              "wechat_book_id":book_sentence[2] ,"book_name":book_sentence[3],
              "author_id": book_sentence[4],"author_name":book_sentence[5],
              "underline_num":book_sentence[6],"type":book_sentence[7]} for book_sentence in book_sentence_list]
        )
        db.session.commit()

def select_book_sentence(sentence,wechat_book_id):
    with app.app_context():
        book_sentence_list = BookSentence.query.filter_by(sentence=sentence,wechat_book_id=wechat_book_id).all()

    return book_sentence_list

def select_book_sentence_by_wechat_id(wechat_book_id):
    with app.app_context():
        book_sentence_list = BookSentence.query.filter_by(wechat_book_id=wechat_book_id).all()

    return book_sentence_list

def select_book_sentence_by_condition(key_words,wechat_book_id,book_id_list):
    with app.app_context():
        book_sentence_list = BookSentence.query.filter(
                                                    # func.length(BookSentence.sentence) < 150,
                                                    BookSentence.underline_num > 1000,
                                                    BookSentence.sentence.like("%" + key_words + "%" if key_words else '%%'),
                                                    (BookSentence.wechat_book_id == wechat_book_id) if wechat_book_id else 1==1,
                                                    BookSentence.book_id.in_(book_id_list) if len(book_id_list) > 0 else 1==1,

                                                ).order_by(func.rand()).limit(1000).all()
                                                    # ).order_by(BookSentence.underline_num.desc()).limit(1000).all()

    return book_sentence_list


def update_book_sentence(wechat_book_id,author_id,author_name):
    with app.app_context():
        BookSentence.query.filter_by(wechat_book_id=wechat_book_id).update({"author_id":author_id,"author_name": author_name})
        db.session.commit()

def insert_tag(tag_name):
    with app.app_context():
        tag = Tag(name=tag_name)
        db.session.add(tag)
        db.session.flush()
        tag_id = tag.id
        db.session.commit()
        return tag_id

def insert_book_tag_relation(wechat_book_id,book_id,tag_id):
    with app.app_context():
        bookTagRelation = BookTagRelation(wechat_book_id=wechat_book_id,book_id=book_id,tag_id=tag_id)
        db.session.add(bookTagRelation)
        db.session.commit()

def select_tag(tag_name):
    with app.app_context():
        tag_list = Tag.query.filter_by(name=tag_name).all()

    return tag_list

def select_tag_list():
    with app.app_context():
        tag_list = Tag.query.filter_by().all()

    return tag_list

def select_book_tag_relation(wechat_book_id,tag_id):
    with app.app_context():
        book_tag_relation_list = BookTagRelation.query.filter_by(wechat_book_id=wechat_book_id,tag_id=tag_id).all()

    return book_tag_relation_list

def select_relation_by_tag_id(tag_id):
    with app.app_context():
        book_tag_relation_list = BookTagRelation.query.filter_by(tag_id=tag_id).all()

    return book_tag_relation_list

def select_author(author_name):
    with app.app_context():
        author_list = Author.query.filter_by(name=author_name).all()

    return author_list

def select_author_list():
    with app.app_context():
        author_list = Author.query.filter_by().all()

    return author_list

def insert_author(author_name):
    with app.app_context():
        author = Author(name=author_name)
        db.session.add(author)
        db.session.flush()
        author_id = author.id
        db.session.commit()
        return author_id

def insert_video(title,subtitle,bilibiliTitle,end,comment_guide,text,
                 background_url,bgm_name,
                 font_cover_ratio,bilibili_tid,
                 description,tag,status
                 ):
    with app.app_context():
        video = Video(title=title,subtitle=subtitle,bilibili_title=bilibiliTitle,end=end,comment_guide=comment_guide,
                      text=text,background_url=background_url,bgm_name=bgm_name,
                      font_cover_ratio=font_cover_ratio,
                      bilibili_tid=bilibili_tid,description=description,tag=tag,status=status)
        db.session.add(video)
        db.session.flush()
        video_id = video.id
        db.session.commit()
        return video_id

def select_video(id):
    with app.app_context():
        video = Video.query.get(id)

    return video

def select_video_list():
    with app.app_context():
        video_list = Video.query.filter_by().all()
    return video_list

def update_video(id,cover_url,video_url,description):
    with app.app_context():
        Video.query.filter_by(id=id).update({"cover_url":cover_url,"video_url": video_url,"description":description})
        db.session.commit()

def update_video_open_id_and_status(id,open_id,status):
    with app.app_context():
        Video.query.filter_by(id=id).update({"open_id":open_id,"status":status})
        db.session.commit()

def update_video_contribute_time_and_status(id,contribute_time,status):
    with app.app_context():
        Video.query.filter_by(id=id).update({"contribute_time":contribute_time,"status":status})
        db.session.commit()

def update_platform_token(platform,refresh_token,access_token):
    with app.app_context():
        PlatformToken.query.filter_by(platform=platform).update({"refresh_token":refresh_token,"access_token":access_token})
        db.session.commit()

def select_refresh_token(platform):
    with app.app_context():
        refresh_token_list = PlatformToken.query.filter_by(platform=platform).all()

    return refresh_token_list[0]

if __name__ == '__main__':

    # 插入一条数据
    # id = insert_author('弗洛伊德１１１')
    # print("作者id:",id)

    # # 插入一条数据
    # with app.app_context():
    #     book = Book(name='天龙八部')
    #     db.session.add(book)
    #     db.session.commit()
    # 插入书籍名字到表中
    # book_list = select_book(111,'天龙八部1')
    # if len(book_list) == 0:
    #     insert_book(111,'天龙八部1')
    # book_sentence_list = select_book_sentence('两句名言1',11111)
    # if len(book_sentence_list) == 0:
    #     insert_book_sentence('两句名言1',1,11111,'天龙八部',119,1)

    # book_list = select_book_by_wechat_book_id(11111)
    # print(book_list[0].name)

    # tag_id = insert_tag("yixue")
    # print(tag_id)
    # insert_book_tag_relation(2,3,2)
    # tag_list = select_tag("世界名著")
    # book_tag_relation_list = select_book_tag_relation(703157,7)
    # print(book_tag_relation_list)
    # tag_list = select_tag_list()
    # print(tag_list)

    # book_tag_relation_list = select_relation_by_tag_id(185)
    # print(book_tag_relation_list)
    # update_book(3001057944,"2","222")
    # list = select_author("欧文·亚隆")
    # print("list",list[0].id,list[0].name)

    # book_sentence_list = []
    # sentence = []
    # sentence2 = []
    # sentence.append("sentence")
    # sentence.append(1)
    # sentence.append(11)
    # sentence.append("book_name")
    # sentence2.append("author_id1")
    # sentence2.append("author_name1")
    # sentence.append(12)
    # sentence.append(1)
    # sentence2.append("sentence2")
    # sentence2.append(2)
    # sentence2.append(22)
    # sentence2.append("book_name2")
    # sentence2.append("author_id2")
    # sentence2.append("author_name2")
    # sentence2.append(22)
    # sentence2.append(2)
    # book_sentence_list.append(sentence)
    # book_sentence_list.append(sentence2)
    #
    # batch_insert_book(book_sentence_list)

    # book_list = select_book_list()
    # for book in book_list:
    #     wechat_book_id = book.wechat_book_id
    #     author_id = book.author_id
    #     author_name = book.author_name
    #     update_book_sentence(wechat_book_id,author_id,author_name)

    # title= "标题"
    # subtitle = "副标题"
    # end = "结尾"
    # comment_guide = "引导评论"
    # text = "文本"
    # background_url = "背景图片地址"
    # bgm_name = "BGM名字"
    # font_cover_ratio = 10
    # bilibili_tid = 124
    # description = "描述"
    # tag = "标签"
    # status = 0
    # index = insert_video(title,subtitle,end,comment_guide, text,
    #              background_url, bgm_name,
    #              font_cover_ratio, bilibili_tid,
    #              description, tag, status
    #              )
    #
    # print("index",index)
    # video = select_video(4)
    # print("video",video.end)
    # update_video(7,"cover_url","url")
    # update_video_open_id_and_status(8, "BV1Wv4y1y7yj",2)

    update_platform_token("bilibili","123","567")

    platform_token = select_refresh_token("bilibili")
    print("r_token",platform_token.refresh_token)
    print("access_token", platform_token.access_token)

