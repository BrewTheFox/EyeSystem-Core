import pymysql
import sqlite3
import os
import logging
import dotenv
from misc import getCurrentPath

class Database():
    def __init__(self):
        dotenv.load_dotenv(f"{getCurrentPath()}/.env", override=True)
        self.localdb = os.getenv("localdb").lower()
        if self.localdb == "true":
            logging.log(msg="Se usara base de datos local", level=1)
            self.conn = sqlite3.connect(f"{getCurrentPath()}/database.sql")
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
        usuario VARCHAR(20) NOT NULL, contrasena VARCHAR(61), rol INT);"""

        # Se ejecutan las consultas y se confirman en la base de datos
        self.cur.execute(student_table)
        self.cur.execute(asistance_table)
        self.cur.execute(user_table)
        self.conn.commit()
        if not self.localdb == "true":
            self.disconnect()
    
    def _mysqltosqlite(self, query:str) -> str:
        return query.replace("%s", "?")
    
    def commit(self, query:str, arguments:tuple) -> None:
        if self.localdb == "true":
            self.cur.execute(self._mysqltosqlite(query), arguments)
            self.conn.commit()
            return
        self.connect()
        self.cur.execute(query, arguments)
        self.conn.commit()
        self.disconnect()
        return

    def fetchone(self, query:str, arguments:tuple) -> tuple | None:
        if self.localdb == "true":
            self.cur.execute(self._mysqltosqlite(query), arguments)
            return self.cur.fetchone()
        self.connect()
        self.cur.execute(query, arguments)
        data = self.cur.fetchone()
        self.disconnect()
        return data
    
    def fetchall(self, query:str, arguments:tuple) -> tuple | None:
        if self.localdb == "true":
            self.cur.execute(self._mysqltosqlite(query), arguments)
            return self.cur.fetchall()
        self.connect()
        self.cur.execute(query, arguments)
        data = self.cur.fetchall()
        self.disconnect()
        return data

    def fetchmany(self, query:str, arguments:tuple, size:int) -> tuple | None:
        if self.localdb == "true":
            self.cur.execute(self._mysqltosqlite(query), arguments)
            return self.cur.fetchmany(size)
        self.connect()
        self.cur.execute(query, arguments)
        data = self.cur.fetchmany(size)
        self.disconnect()
        return data
    
    def connect(self):
        if not self.localdb == "true":
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
        if not self.localdb == "true":
            self.cur.close()
            self.conn.close()
            self.cur = None
            self.conn = None