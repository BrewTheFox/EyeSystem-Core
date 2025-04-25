from database import Database
from misc import *
from datetime import datetime

db = Database()

def getasistenciacurso(curso:str) -> int:
    global db
    date = datetime.now().strftime('%Y-%m-%d')
    datos = db.fetchone("SELECT COUNT(*) FROM asistencia JOIN estudiante ON asistencia.estudiante_id = estudiante.codigo_est WHERE estudiante.grupo = %s AND asistencia.fecha = %s;", (curso, date))[0]
    return datos

def getasistenciajornada(jornada:str) -> int:
    global db
    date = datetime.now().strftime('%Y-%m-%d')
    datos = db.fetchone("SELECT COUNT(*) FROM asistencia JOIN estudiante ON asistencia.estudiante_id = estudiante.codigo_est WHERE estudiante.jornada = %s AND asistencia.fecha = %s;", (jornada, date))
    return datos

def getcursos() -> tuple:
    global db
    datos = db.fetchall("SELECT DISTINCT grupo FROM estudiante", ())
    return datos

def getjornadas() -> tuple:
    global db
    datos = db.fetchall("SELECT DISTINCT jornada FROM estudiante", ())
    return datos

def getasistance(group:str, studytime:str, date:str) -> tuple:
    global db
    datos = db.fetchall("SELECT estudiante.nombres, estudiante.apellidos, asistencia.hora  FROM asistencia JOIN estudiante ON asistencia.estudiante_id = estudiante.codigo_est WHERE estudiante.grupo = %s AND asistencia.fecha = %s and estudiante.jornada = %s;", (group, date, studytime))
    return datos

def changepassword(username:str, current:str, new:str) -> dict:
    global db
    datos = db.fetchone("SELECT contrasena From usuarios where usuario=%s;", (username,))
    if datos is None:
        return {"status":"El usuario es inexistente", "type":"error", "color":"red"}
    if checkpassword(datos[0], current):
        db.commit("UPDATE usuarios SET contrasena=%s WHERE usuario=%s;", (hashpassword(new), username))
        return {"status": "La contraseña se actualizo correctamente!", "type":"success", "color":"green"}
    return {"status": "La contraseña es invalida", "type":"error", "color":"red"}

def checklogin(username:str, password:str) -> dict:
    global db
    datos = db.fetchone("SELECT contrasena, rol From usuarios where usuario=%s;", (username,))
    if datos is None:
        return {"status":"El usuario es inexistente", "type":"error", "color":"red"}
    if checkpassword(datos[0], password):
        return {"status":"Login Exitoso", "type":"success", "role":datos[1], "color":"green"}
    return {"status": "La contraseña es invalida", "type":"error", "color":"red"}

def registeruser(username:str, password:str, account_type:int) -> dict:
    global db
    if len(username) < 4:
        return {"status":"El usuario es muy pequeño", "type":"error", "color":"red"}
    if len(username) >= 20:
        return {"status":"El usuario es muy largo", "type":"error", "color":"red"}
    
    datos = db.fetchone("SELECT rol From usuarios where usuario=%s;", (username,))
    if datos is not None:
        return {"status":"El usuario ya existe", "type":"error", "color":"red"}
    db.commit("INSERT INTO usuarios(usuario, contrasena, rol) VALUES (%s, %s, %s);", (username, hashpassword(password), account_type))
    return {"status":"Exito al registrar la cuenta!", "type":"success", "color":"green"}
    
def adduser(code:str, name:str, surname:str, grade:str, schooltime:str)-> dict:
    datos = db.fetchone("SELECT nombres From estudiante where codigo_est=%s;", (code,))
    if datos is not None:
        return {"status":"El usuario ya existe", "type":"error", "color":"red"}
    db.commit("INSERT INTO estudiante (codigo_est, apellidos, nombres, grupo, jornada) VALUES (%s, %s, %s, %s, %s)", (code, surname, name, grade, schooltime))
    return {"status":"Exito al registrar al estudiante!", "type":"success", "color":"green"}

def getuserquantity():
    return db.fetchone("SELECT COUNT(*) FROM estudiante", ())[0]

def getassistancequantity():
    date = datetime.now().strftime('%Y-%m-%d')
    return db.fetchone("SELECT COUNT(*) FROM asistencia WHERE fecha = %s" , (date))[0]

def addassistance(id:str):
    date = datetime.now().strftime('%Y-%m-%d')
    hour = datetime.now().strftime('%H:%M:%S')
    registro = db.fetchone("SELECT * FROM asistencia WHERE estudiante_id = %s AND fecha = %s", (id, date))
    if registro is not None:
        return
    db.commit("INSERT INTO asistencia (estudiante_id, fecha, hora) VALUES (%s, %s, %s)", (id, date, hour))