import os
from flask import Flask, jsonify, request, send_file
from bson.objectid import ObjectId
import pymongo
import time
from helper import pretty_respon_train, encode_img, check_resolution
from recognition import compare

app = Flask(__name__)
PROJECT_HOME = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = '{}/_tmp/'.format(PROJECT_HOME)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
pmongo = pymongo.MongoClient('mongodb://localhost:27017/')
db = pmongo['face_recognition']
dict_face = db['encode_face']

@app.route('/', methods=['GET', 'POST'])
def init():
    return "Hello World!"

@app.route('/data_train', defaults={'id': None}, methods=['GET'])
@app.route('/data_train/<id>', methods=['GET'])
def data_train(id):
    if id:
        result = dict_face.find({"_id":ObjectId(id)})
    else:
        result = dict_face.find()

    return jsonify(pretty_respon_train(result))

@app.route('/add_data_train', methods=['POST'])
def add_data_train():
    img = request.files['foto']
    img_name = "TRAIN_"+str(int(time.time())) + '.' + img.filename.rsplit('.', 1)[1].lower()
    saved_path = os.path.join(app.config['UPLOAD_FOLDER'], img_name)
    img.save(saved_path)
    ei = encode_img("_tmp/"+img_name)
    menteri = {}
    menteri['name'] = request.form['nama']
    menteri['alias'] = request.form['jabatan']
    menteri['face_encode'] = ei
    menteri['resolution'] = check_resolution("_tmp/"+img_name)
    dict_face.insert_one(menteri)
    return jsonify({"code": 200, "message": "Data train success saved!"})

@app.route('/recognition', methods=['POST'])
def recognition():
    img = request.files['foto']
    img_name = str(int(time.time()))+'.'+img.filename.rsplit('.', 1)[1].lower()
    saved_path = os.path.join(app.config['UPLOAD_FOLDER'], img_name)
    img.save(saved_path)
    # ei = encode_img("_tmp/"+img_name)
    result = compare(img_name)
    os.remove("_tmp/"+img_name)
    return send_file("_tmp/"+result, mimetype="image/jpg")

if __name__ == '__main__':
    app.run()