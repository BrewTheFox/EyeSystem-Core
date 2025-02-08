import os
import bcrypt
import cv2
import numpy as np
import os

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

async def FaceCropper(image:bytes, person_code:str):
    faceclasif = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    image_np = np.frombuffer(image, np.uint8)
    image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
    image = cv2.resize(image, (320, int(image.shape[0] * 320 / image.shape[1])))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face = faceclasif.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40)
    )
    os.makedirs(f"{getCurrentPath()}/data/{person_code}/", exist_ok=True)
    currentImages = len(os.listdir(f"{getCurrentPath()}/data/{person_code}/"))
    if type(face) == np.ndarray:
        for (x, y, w, h) in face:
            image = image[y:y+h, x:x+w]
        image = cv2.resize(image, (720, 720), interpolation=cv2.INTER_LANCZOS4)
        cv2.imwrite(f"{getCurrentPath()}/data/{person_code}/rostro_{str(currentImages)}.jpg", image)
        return {"status": "Rostro reconocido", "imagenes_obtenidas":currentImages}
    return {"status": "No se pudo reconocer el rostro", "imagenes_obtenidas": currentImages}