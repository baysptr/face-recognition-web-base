from app import dict_face
from PIL import Image
import face_recognition

collection_face_recognition = dict_face

def check_resolution(filename):
    im = Image.open(filename)
    width, height = im.size
    return str(width) + "x" + str(height)

def fakerMenteri(nama, jabatan, img):
    picture_of_me = face_recognition.load_image_file(img)
    my_face_encoding = face_recognition.face_encodings(picture_of_me)[0]

    menteri = {}
    menteri['name'] = nama
    menteri['alias'] = jabatan
    menteri['resolution'] = check_resolution(img)
    menteri['face_encode'] = my_face_encoding.tolist()
    collection_face_recognition.insert_one(menteri)
    print("Data seeder ["+nama+"] is success!")

fakerMenteri("Mochamad Basoeki Hadimoeljono", "Menteri Pekerjaan Umum dan Perumahan Rakyat", "data_seeder/basuki.jpg")
fakerMenteri("Erick Thohir", "Menteri Badan Usaha Milik Negara", "data_seeder/erick.jpg")
fakerMenteri("Nadiem Anwar Makarim", "Menteri Pendidikan dan Kebudayaan Indonesia", "data_seeder/nadiem.jpeg")
fakerMenteri("Mohammad Mahfud MD", "Menteri Koordinator Hukum dan HAM", "data_seeder/mahfud.jpg")
fakerMenteri("Wishnutama Kusubandio", "Menteri Pariwisata dan Ekonomi Kreatif", "data_seeder/wishnutama.jpg")

# for x in range(7,13):
#     img_file = "seeder" + str(x) + ".jpg"
#     picture_of_me = face_recognition.load_image_file("data_seeder/" + img_file)
#     my_face_encoding = face_recognition.face_encodings(picture_of_me)[0]
#     my_face = {}
#     my_face['name'] = "Erick Thohir"
#     my_face['alias'] = "Menteri Badan Usaha Milik Negara"
#     my_face['resolution'] = check_resolution(img_file)
#     my_face['face_encode'] = my_face_encoding.tolist()
#     collection_face_recognition.insert(my_face)
#     print("Seeder success [" + str(x) + "] Erick Thohir")

print("")
print("All Seeder success!")