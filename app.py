# 1. Flask 모듈을 import 한다.
from flask import Flask, render_template, request, jsonify, url_for, redirect, make_response
# import pymongo for using MongoDB
from pymongo import MongoClient
# import werkzeug.utils(>=1.0.0 version) for secure_filename method
from werkzeug.utils import secure_filename

from mongoengine import *

import gridfs
import os
import imageio
import json
import joblib
import numpy as np

# 2. Flask 객체를 app 변수에 할당한다.
app = Flask(__name__)
# load the model file which is already trained.
#model = joblib.load('./model_train_32x32.pkl')

ALLOWED_EXTENSIONS = set(['aedat4', 'aedat', 'jpg'])
# representing upload folder
UPLOAD_FOLDER = '/images'
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

''' make Database using mongoDB '''
class BuildDB:
    def __init__(self):
        # make DataBase, I think 270107 is basic port number of MongoDB
        self.client = MongoClient('localhost', 27017)

        # db = client."dbname", create database
        self.db = self.client.modelDB
        print('MongoDB connected!')

    def insertDataToDataBase(self, _id, _filename):
        print('insertDataToDataBase function executed!')
        # db."collection name".insert_one(document, dictionary)
        doc = {'file_id': _id, 'file_name': _filename}
        self.db.data.insert_one(doc)

    def findOneData(self, _id):
        data = self.db.data.find_one({'file_id': _id})
        return data

    def eraseData(self, _id):
        self.db.data.find_one({'file_id': _id})

#buildDB = BuildDB()

'''
buildDB.insertDataToDataBase('1', '1.aedat4')
buildDB.insertDataToDataBase('2', '2.aedat4')
'''

'''
# db."collection name".insert_one(document, dictionary)
doc = {'file_id': 1, 'file_name': '1.aedat4'}
db.data.insert_one(doc)
'''

''' make Database using mongoDB '''

# 3. app 객체를 이용해서 routing 경로를 설정한다.
# 4. 해당 routing 경로로 요처이 들어올 때 실행할 함수를 바로 밑에 작성한다.
#  - 해당 웹페이지에 대한 경로를 URI로 만들어준다고 이해하면 된다고 한다.

'''
HTTP 요청 명령어 목록?
GET: 암호화되지 않은 형태의 데이터를 서버로 전송하는데 사용되는 가장 일반적 방법
HEAD: GET과 유사한 방법으로 Response body를 포함하지 않고 사용
POST: 특정 양식의 데이터를 암호화하여 서버로 전송하는데 사용
PUT: 특정 대상의 데이터를 갱신(Update)하는데 사용
DELETE: URL에 지정된 대상을 삭제(DELETE)하는데 사용
'''

@app.route("/")
def main():
    return render_template('index.html')

# 여러 개의 복잡한 URI를 함수로 쉽게 연결하는 방법을 제공한다.
@app.route("/profile/<username>")
def hello_flask(username):
    return "profile: " + username




def allowed_file(filename):
    # filename contains '.' and file type is allowed.
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# 이미지 파일은 HTTP POST 요청을 통해서 보내진다.
# aedat file도 마찬가지라고 생각한다.
@app.route('/predict', methods=['POST'])
def make_prediciton():
    # check HTTP method using request object.
    if request.method == 'POST':

        if "file" not in request.files:
            return "No file in your request!"

        # 업로드 파일 처리 분기
        file = request.files['file']
        string = request.form['string']
        if file and allowed_file(file.filename):
            try:
                fileName = secure_filename(file.filename)
                file.save("./images/" + fileName)
                return fileName
            except:
                return "file save error!", 200
            # os.path.join method return UPLOAD_FOLDER/filename
            #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            '''
            model should be imported in this section
            '''
            label = '3'
            # 숫자가 10인 경우 0으로 처리한다.
            if(label == '10'):
                label = '0'
            print(label)
            return render_template('index.html', label="Your image is {}".format(label))
        else:
            # load the 'index.html' file in templates folder.
            return render_template('index.html', label="No Files")

@app.route("/send_post", methods=['POST'])
def send_post():
    if request.method == 'POST':
        if "file" not in request.files:
            return "No file in your request!"
        file = request.files['file']
        string = request.form['string']
        try:
            fileName = secure_filename(file.filename)
            file.save("./images/" + fileName)
            return fileName
        except:
            return "file save error!", 200
    else:
        return "No File!", 200
'''
@app.route("/upload", methods=['POST'])
def upload():
    ## file upload ##
    img = request.files['image']

    ## GridFs 이용해서 파일을 분할하여 DB에 저장.
    fs = gridfs.GridFS(buildDB.db)
    fs.put(img, filename='name')

    ## file find ##
    data = buildDB.db.fs.files.find_one({'filename': 'name'})
    print(data)
    ## file download ##
    my_id = data['_id']
    outputdata = fs.get(my_id).read()
    output = open('./images/' + 'back.png', 'wb')
    output.write(outputdata)
    return jsonify({'msg': 'save complete'})
'''

@app.route('/show/<string:filename>', methods=['GET'])
def showResult(filename):
    file_dir = os.path.join("./upload")
    if request.method == 'GET':
        if filename is None:
            pass
        else:
            image_data = open(os.path.join(file_dir, '%s' % filename), "rb").read()
            response = make_response(image_data)
            response.headers['Content-Type'] = 'image/png'
            return response
    else:
        pass

# 5. 메인 모듈로 실행할 때 플라스크 서버가 구동된다. (서버로 구동한 IP와 포트를 옵션으로 넣어줄 수 있다.)
local_addr = "127.0.0.1"
open_addr = "0.0.0.0"
port_num = "5000"

if __name__ == '__main__':
    app.run(host=open_addr)
