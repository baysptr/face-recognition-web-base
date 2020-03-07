from PIL import Image, ImageDraw
import face_recognition
import numpy as np
import pymongo
import time

pmongo = pymongo.MongoClient('mongodb://localhost:27017/')
db = pmongo['face_recognition']
dict_face = db['encode_face']

def compare(filename):
    known_face_name = []
    known_face_encode = []

    query = dict_face.find()
    st = 1
    for x in query:
        known_face_encode.insert(st, np.array(x['face_encode']))
        known_face_name.insert(st, x['name'])
        st += 1
    # Load test data yaitu poster kampanye gus ipul dengan wakilnya
    unknown_image = face_recognition.load_image_file("_tmp/"+filename)

    # Encoding data test tersebut
    face_locations = face_recognition.face_locations(unknown_image)
    face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

    # Data test yang sudah di encode diubah menjadi array agar mudah di compare dengan data Train
    pil_image = Image.fromarray(unknown_image)
    # Buat image dari canvas
    draw = ImageDraw.Draw(pil_image)

    # Process compare dari train data dengan test data
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encode, face_encoding)

        # name = "Unknown"

        # if True in matches:
        #     first_match_index = matches.index(True)
        #     name = known_face_name[first_match_index]

        face_distances = face_recognition.face_distance(known_face_encode, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_name[best_match_index]
        else:
            name = "Unknown"

        # Buat kotak detecetion
        draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))

        # Buat label pada setiap kotak yang ditemukan
        text_width, text_height = draw.textsize(name)
        draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0, 0, 255), outline=(0, 0, 255))
        draw.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255, 255))

    del draw
    # pil_image.show()

    # Jika anda save hasil compare - nya
    result_name = "RESULT_"+str(int(time.time()))+".jpg"
    pil_image.save("_tmp/"+result_name)
    return result_name