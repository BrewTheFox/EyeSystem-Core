import os
import bcrypt
import cv2
import numpy as np
import os
import datetime
import time
import json
import dbmanager

def getCurrentPath() -> str:
    currentdir = os.path.split(os.path.abspath(__file__))[0]
    currentdir = currentdir.split("/")
    del currentdir[-1]
    return '/'.join(currentdir)

def hashpassword(password:str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

def checkpassword(hashed:str, password:str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))

def autotrain():
    try:
        data = os.listdir(f"{getCurrentPath()}/data/")
    except:
        return
    faces = []
    labels = []
    personandcode = {}
    data.sort()
    for code, person in enumerate(data):
        personandcode[code] = person
        for image in os.listdir(f"{getCurrentPath()}/data/{person}"):
            if image.endswith(".jpg"):
                faces.append(cv2.imread(f"{getCurrentPath()}/data/{person}/{image}", 0))
                labels.append(int(code))
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.train(np.array(faces), np.array(labels))
    os.makedirs(f"{getCurrentPath()}/models/", exist_ok=True)
    os.makedirs(f"{getCurrentPath()}/codes/", exist_ok=True)
    currentmodels = os.listdir(f"{getCurrentPath()}/models/")
    ids = os.listdir(f"{getCurrentPath()}/codes/")
    if len(currentmodels) >= 5:
        currentmodels.sort()
        while len(currentmodels) >= 5:
            os.remove(f"{getCurrentPath()}/models/{currentmodels[0]}")
            currentmodels = os.listdir(f"{getCurrentPath()}/models/")
            currentmodels.sort()
    if len(ids) >= 5:
        ids.sort()
        while len(ids) >= 5:
            os.remove(f"{getCurrentPath()}/codes/{ids[0]}")
            ids = os.listdir(f"{getCurrentPath()}/codes/")
            ids.sort()

    today = datetime.date.today()
    timestamp = str(int(time.time()))
    face_recognizer.write(f"{getCurrentPath()}/models/{today}_{timestamp}_model.xml")
    with open(f"{getCurrentPath()}/codes/{today}_{timestamp}_model.codes", "w+") as codes:
        codes.write(json.dumps(personandcode))


async def RecognizeFromImg(image:bytes):
    faceclasif = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    os.makedirs(f"{getCurrentPath()}/models/", exist_ok=True)
    os.makedirs(f"{getCurrentPath()}/codes/", exist_ok=True)
    currentmodels = os.listdir(f"{getCurrentPath()}/models/")
    people = []
    if len(currentmodels) == 0:
        return
    currentmodels.sort()
    lastestmodel = currentmodels[-1]
    with open(f"{getCurrentPath()}/codes/{lastestmodel.replace(".xml", "")}.codes", "r") as file:
        codes = json.loads(file.read())
    facerecon = cv2.face.LBPHFaceRecognizer_create()
    facerecon.read(f"{getCurrentPath()}/models/{lastestmodel}")
    image = np.frombuffer(image, np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face = faceclasif.detectMultiScale(image, 1.2, 4, minSize=(40, 40))
    if type(face) == np.ndarray:
        for (x, y, w, h) in face:
            image = image[y:y+h, x:x+w]
            if facerecon.predict(image)[1] < 80:
                person = codes[str(facerecon.predict(image)[0])]
                people.append(person)
                person_data = f"{getCurrentPath()}/data/{person}"
                cv2.imwrite(f"{person_data}/rostro_{len(os.listdir(person_data))}.jpg", image)
                dbmanager.addassistance(person)
    return {"Se registraron las personas":people}


async def FaceCropper(image:bytes, person_code:str):
    faceclasif = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    image_np = np.frombuffer(image, np.uint8)
    image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
    image = cv2.resize(image, (320, int(image.shape[0] * 320 / image.shape[1])))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face = faceclasif.detectMultiScale(
        image, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40)
    )

    os.makedirs(f"{getCurrentPath()}/data/{person_code}/", exist_ok=True)
    currentImages = len(os.listdir(f"{getCurrentPath()}/data/{person_code}/"))
    if type(face) == np.ndarray:
        for (x, y, w, h) in face:
            image = image[y:y+h, x:x+w]
        image = cv2.resize(image, (150, 150))
        image = cv2.equalizeHist(image)
        cv2.imwrite(f"{getCurrentPath()}/data/{person_code}/rostro_{str(currentImages)}.jpg", image)
        return {"status": "Rostro reconocido", "imagenes_obtenidas":currentImages}
    
    return {"status": "No se pudo reconocer el rostro", "imagenes_obtenidas": currentImages}