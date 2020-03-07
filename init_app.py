import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
dblist = myclient.list_database_names()
if "face_recognition" in dblist:
    myclient['face_recognition'].create_collection("encode_face")
    print("Collection telah terbuat")
else:
    print("Maaf database name anda tidak kami ketahui! periksa kembali konfigurasi anda")