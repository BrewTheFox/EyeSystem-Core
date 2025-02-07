import pymysql
import sqlite3
import os
import logging

class Database():
    def __init__(self):
        if os.getenv("localdb").lower() == "true":
            logging.log(msg="Se usara base de datos local", level=1)
            self.conn = sqlite3.connect("../database.sql")
            self.cur = self.conn.cursor()
        else:
            logging.log(msg="Se usara base de datos remota", level=1)
            self.connect()
        student_table = """
            CREATE TABLE IF NOT EXISTS estudiante (
            id INT AUTO_INCREMENT PRIMARY KEY,
            codigo_est VARCHAR(11) NOT NULL,
            apellidos VARCHAR(30) NOT NULL,
            nombres VARCHAR(40) NOT NULL,
            grupo VARCHAR(5) NOT NULL,
            jornada VARCHAR(7) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
                """
        asistance_table = """
            CREATE TABLE IF NOT EXISTS asistencia (
            id INT AUTO_INCREMENT PRIMARY KEY,
            estudiante_id INT,
            nombre VARCHAR(40) NOT NULL,
            fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
            estado VARCHAR(20) NOT NULL,
            FOREIGN KEY (estudiante_id) REFERENCES estudiante(id)
            );
            """
        user_table = """
        CREATE TABLE IF NOT EXISTS usuarios (
        usuario VARCHAR(20) NOT NULL, contrasena VARCHAR(61));"""

        # Se ejecutan las consultas y se confirman en la base de datos
        self.cur.execute(student_table)
        self.cur.execute(asistance_table)
        self.cur.execute(user_table)
        self.conn.commit()
        if not os.getenv("localdb").lower() == "true":
            self.disconnect()
        
    def connect(self):
        if not os.getenv("localdb").lower() == "true":
            try:
                # Se declaran los parametros de conexion en base a las variables de entorno
                connection_params = {
                'host': os.getenv("db_host"),
                'port': int(os.getenv("db_port")),
                'db': os.getenv("db_name"),
                'user': os.getenv("db_user"),
                'password': os.getenv("db_password")
                    }
            except ValueError:
                raise ValueError("No se puede conectar a la base de datos remota, el puerto suministrado es invalido")
            try:
                self.conn = pymysql.connect(**connection_params)
                self.cur = self.conn.cursor()
            except:
                raise ConnectionError("No se pudo conectar a la base de datos remota, porfavor verifica que las credenciales sean validas")
        
    def disconnect(self):
        if not os.getenv("localdb").lower() == "true":
            self.cur.close()
            self.conn.close()
            self.cur = None
            self.conn = None
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv("../.env")
    db = Database()