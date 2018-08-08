#/usr/bin/env python3
from flask import Flask,render_template,request
import json,os

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

class Read_Json(object):
    def __init__(self,Json_File_Path):
        self.path = Json_File_Path
        Json_dict = Read_json_file(path)
    def Read_Json_File(path):
        with open(path,'r') as f:
            return json.loads(f.read())

dc1 = Read_Json.Read_Json_File('/home/shiyanlou/news/files/helloshiyanlou.json')
dc2 = Read_Json.Read_Json_File('/home/shiyanlou/news/files/helloworld.json')
#print(dc['title'])

@app.errorhandler(404)
def not_found(error): 
    return render_template('404.html'),404

@app.route('/')
def index():
    return render_template('index.html',dc1=dc1,dc2=dc2)

@app.route('/files/<filename>')
def file(filename):
    if filename == 'helloshiyanlou':
        return render_template('file.html',dc=dc1)
    elif filename == 'helloworld':
        return render_template('file.html',dc=dc2)

