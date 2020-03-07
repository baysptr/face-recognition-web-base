import face_recognition
from PIL import Image

def check_resolution(filename):
    im = Image.open(filename)
    width, height = im.size
    return str(width) + "x" + str(height)

def encode_img(img):
    picture_of_me = face_recognition.load_image_file(img)
    my_face_encoding = face_recognition.face_encodings(picture_of_me)[0]
    return my_face_encoding.tolist()

def pretty_respon_train(obj):
    resp = {}
    resp['code'] = 200
    resp['message'] = "Data Training"
    resp_data = []
    st = 1
    for i in obj:
        row = {}
        row['id'] = str(i['_id'])
        row['nama'] = i['name']
        row['alias'] = i['alias']
        row['resolution'] = i['resolution']
        row['count_encode'] = len(i['face_encode'])
        resp_data.insert(st, row)
        st += 1
    resp['data'] = resp_data
    return resp