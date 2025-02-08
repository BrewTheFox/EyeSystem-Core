from database import Database
from misc import *

db = Database()

def checklogin(username:str, password:str) -> dict:
    global db
    datos = db.fetchone("SELECT contrasena, rol From usuarios where usuario=%s;", (username,))
    if datos is None:
        return {"status":"El usuario es inexistente", "type":"error", "color":"red"}
    if checkpassword(datos[0], password):
        return {"status":"Login Exitoso", "type":"success", "role":datos[1], "color":"green"}
    return {"status": "La contraseña es invalida", "type":"error", "color":"red"}

def registeruser(username:str, password:str, account_type:int):
    global db
    if len(username) < 4:
        return {"status":"El usuario es muy pequeño", "type":"error", "color":"red"}
    if len(username) >= 20:
        return {"status":"El usuario es muy largo", "type":"error", "color":"red"}
    
    datos = db.fetchone("SELECT rol From usuarios where usuario=%s;", (username,))
    if datos is not None:
        return {"status":"El usuario ya existe", "type":"error", "color":"red"}
    db.commit("INSERT INTO usuarios(usuario, contrasena, rol) VALUES (%s, %s, %s);", (username, hashpassword(password), account_type))
    return {"status":"Exito al registrar la cuenta!", "type":"error", "color":"green"}
    
