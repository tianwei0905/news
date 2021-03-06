#/usr/bin/env python3
from flask import Flask,render_template,abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from pymongo import MongoClient

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root@localhost:3306/shiyanlou'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
client = MongoClient('127.0.0.1',27017)
mdb = client.shiyanlou

class File(db.Model):
    __tablename__ = 'file'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    created_time = db.Column(db.DateTime)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    content = db.Column(db.Text)
    category = db.relationship('Category',
        backref=db.backref('files', lazy='dynamic'))
    def __init__(self,title,created_time,category,content):
        self.title = title
        self.created_time = created_time
        self.category = category
        self.content = content
    def add_tag(self,tag_name):
        list_now = mdb.tag.find_one({'id':self.id})
        if list_now:
            tags = list_now['tags']
            if not tag_name in tags:
                tags.append(tag_name)
                mdb.tag.update_one({'id':self.id},{'$set':{'tags':tags}})
        else:
            mdb.tag.insert_one({'id':self.id,'tags':[tag_name]})
    def remove_tag(self,tag_name):
        list_now = mdb.tag.find_one({'id':self.id})
        if list_now:
            tags = list_now['tags']
            if tag_name in tags:
                tags.remove(tag_name)
                mdb.tag.update_one({'id':self.id},{'$set':{'tags':tags}})
    @property
    def tags(self):
        return mdb.tag.find_one({'id': self.id})['tags']
#        return ['1','2']
    def __repr__(self):
        return '<File %r>' % self.title

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    def __init__(self,name):
        self.name = name
    def __repr__(self):
        return  '<Category %r>' % self.name

@app.errorhandler(404)
def not_found(error): 
    return render_template('404.html'),404

@app.route('/')
def index():
    news_list = File.query.all()
    return render_template('index.html',news_list=news_list)

@app.route('/files/<file_id>')
def file(file_id):
    findfile = File.query.filter_by(id=file_id).first()
    if findfile == None:
        abort(404)
    else:
        return render_template('file.html', file=findfile)

if __name__ == "__main__":
    app.run()
