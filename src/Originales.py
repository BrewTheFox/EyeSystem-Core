import os
import cv2
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import time

def load_image(image_path):
    """Carga y prepara una imagen para el entrenamiento"""
    try:
        img = cv2.imread(image_path, 0)  # Cargar en escala de grises
        img = cv2.resize(img, (150, 150))  # Tamaño consistente
        img = cv2.equalizeHist(img)  # Mejorar contraste
        return img
    except Exception as e:
        print(f"Error al cargar {image_path}: {str(e)}")
        return None

def ejecutar_entrenamiento():
    """Procesa las fotos de la carpeta data y genera el archivo XML de entrenamiento"""
    print("Iniciando proceso de entrenamiento...")
    start_time = time.time()
    
    # Ruta de la carpeta data
    dataPath = 'D:/USUARIO/Music/Eye_System/Interfaz-3.0-main/formularios/base_de_datos/data'
    
    # Verificar si existe la carpeta data
    if not os.path.exists(dataPath):
        print("Error: No se encontró la carpeta data")
        return
    
    # Obtener lista de personas (carpetas)
    peopleList = os.listdir(dataPath)
    if not peopleList:
        print("Error: No hay carpetas de personas en data")
        return
    
    faces = []
    labels = []
    
    # Procesar cada carpeta de persona
    with ThreadPoolExecutor(max_workers=4) as executor:
        for person_id, person in enumerate(peopleList):
            person_path = os.path.join(dataPath, person)
            print(f"Procesando imágenes de: {person}")
            
            # Obtener todas las imágenes de la persona
            image_files = [os.path.join(person_path, f) 
                         for f in os.listdir(person_path) 
                         if f.endswith(('.jpg', '.jpeg', '.png'))]
            
            # Cargar imágenes en paralelo
            processed_images = list(executor.map(load_image, image_files))
            
            # Agregar imágenes válidas y etiquetas
            for img in processed_images:
                if img is not None:
                    faces.append(img)
                    labels.append(person_id)
            
            print(f"- Procesadas {len(image_files)} fotos")
    
    if not faces:
        print("Error: No se encontraron imágenes válidas para procesar")
        return
    
    print("\nCreando modelo de reconocimiento...")
    
    # Crear y entrenar el reconocedor
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.train(np.array(faces), np.array(labels))
    
    # Guardar el modelo
    face_recognizer.write('modelo_entrenado.xml')
    
    # Mostrar resumen
    tiempo_total = time.time() - start_time
    print("\nProceso completado exitosamente:")
    print(f"- Personas procesadas: {len(peopleList)}")
    print(f"- Total de fotos procesadas: {len(faces)}")
    print(f"- Tiempo de procesamiento: {tiempo_total:.2f} segundos")
    print("- Modelo guardado como: modelo_entrenado.xml")

if __name__ == '__main__':
    ejecutar_entrenamiento()

    def cargar_datos():
        # Limpiar tabla
        for item in tabla_frame.tree.get_children():
            tabla_frame.tree.delete(item)
            
        try:
            conn = obtener_conexion()
            with conn.cursor() as cursor:
                # Construir la consulta SQL base
                sql = """
                SELECT i.id_ingreso, i.codigo_est, 
                       CONCAT(e.apellidos, ', ', e.nombres) as estudiante,
                       e.grupo, e.jornada, i.fecha, i.hora
                FROM ingreso i
                JOIN estudiante e ON i.codigo_est = e.codigo_est
                WHERE 1=1
                """
                params = []
                
                # Aplicar filtros
                if fecha_inicio.get_date():
                    sql += " AND i.fecha >= %s"
                    params.append(fecha_inicio.get_date())
                if fecha_fin.get_date():
                    sql += " AND i.fecha <= %s"
                    params.append(fecha_fin.get_date())
                
                if grupo_var.get():
                    sql += " AND e.grupo LIKE %s"
                    params.append(f"%{grupo_var.get()}%")
                
                if jornada_var.get() != "Todas":
                    sql += " AND e.jornada = %s"
                    params.append(jornada_var.get())
                
                if busqueda_var.get():
                    busqueda = f"%{busqueda_var.get()}%"
                    sql += """ AND (
                        e.codigo_est LIKE %s OR
                        e.nombres LIKE %s OR
                        e.apellidos LIKE %s
                    )"""
                    params.extend([busqueda, busqueda, busqueda])
                
                sql += " ORDER BY i.fecha DESC, i.hora DESC"
                
                cursor.execute(sql, params)
                resultados = cursor.fetchall()
                
                for row in resultados:
                    tabla_frame.tree.insert("", "end", values=row)
                
        except Exception as e:
            print(f"Error al cargar datos: {e}")
        finally:
            if conn:
                conn.close()

    def iniciar_reconocimiento(self, label_camera):
        if self.is_running:
            return
        
        self.is_running = True
        self.face_recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.face_recognizer.read('prueba.xml')
        self.cap = cv2.VideoCapture(0)
        
        # Iniciar el reconocimiento en un hilo separado
        threading.Thread(target=self.proceso_reconocimiento, args=(label_camera,), daemon=True).start()
    
    def detener_reconocimiento(self):
        self.is_running = False
        if self.cap is not None:
            self.cap.release()
    
    def registrar_asistencia(self, codigo_est):
        try:
            # Obtener la fecha actual
            fecha_actual = datetime.now().strftime('%Y-%m-%d')
            registro_key = f"{codigo_est}_{fecha_actual}"
            
            # Verificar si ya se registró hoy
            if registro_key not in self.registros_hoy:
                # Conexión a la base de datos remota
                conexion = pymysql.connect(
                    host='b4qhbwwqys2nhher1vul-mysql.services.clever-cloud.com',
                    port=3306,
                    db='b4qhbwwqys2nhher1vul',
                    user='upvge9afjesbmmgv',
                    password='BS2bxJNACO1XYEmWBqA0'
                )

                cursor = conexion.cursor()

                # Verificar si el estudiante existe
                consulta_estudiante = "SELECT * FROM estudiante WHERE codigo_est = %s"
                cursor.execute(consulta_estudiante, (codigo_est,))
                estudiante = cursor.fetchone()

                if estudiante:
                    # Obtener hora actual
                    hora_actual = datetime.now().strftime("%H:%M:%S")

                    # Insertar asistencia en la tabla
                    insertar_asistencia = "INSERT INTO ingreso (codigo_est, fecha, hora) VALUES (%s, %s, %s)"
                    cursor.execute(insertar_asistencia, (codigo_est, fecha_actual, hora_actual))
                    conexion.commit()

                    print(f"Asistencia registrada para el estudiante: {estudiante[2]} {estudiante[1]} (Grupo: {estudiante[3]}, Jornada: {estudiante[4]})")
                    
                    # Agregar a los registros de hoy
                    self.registros_hoy.add(registro_key)
                    return True
                else:
                    print("Estudiante no encontrado.")
                    return False
                    
            return False
        except Exception as e:
            print(f"Error al registrar asistencia: {e}")
            return False
    
    def proceso_reconocimiento(self, label_camera):
        data_path = 'D:/USUARIO/Music/Eye_System/Interfaz-3.0-main/formularios/base_de_datos/data'
        image_path = os.listdir(data_path)
        faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        while self.is_running:
            ret, frame = self.cap.read()
            if not ret:
                break
                
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = faceClassif.detectMultiScale(gray, 1.2, 4, minSize=(30, 30))
            
            for (x, y, w, h) in faces:
                rostro = gray[y:y+h, x:x+w]
                rostro = cv2.resize(rostro, (200, 200), interpolation=cv2.INTER_CUBIC)
                result = self.face_recognizer.predict(rostro)
                
                if result[1] < 80:
                    codigo_est = image_path[result[0]]
                    # Intentar registrar asistencia
                    if self.registrar_asistencia(codigo_est):
                        color = (0, 255, 0)  # Verde si se registró
                        texto = f'{codigo_est} - Registrado'
                    else:
                        color = (255, 255, 0)  # Amarillo si ya estaba registrado
                        texto = f'{codigo_est} - Ya registrado'
                    
                    cv2.putText(frame, texto, (x, y-25), 2, 1.1, color, 1, cv2.LINE_AA)
                    cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                else:
                    cv2.putText(frame, 'Desconocido', (x, y-20), 2, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
            
            # Convertir el frame para mostrarlo en la interfaz
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            photo = ctk.CTkImage(light_image=img, dark_image=img, size=(640, 480))
            label_camera.configure(image=photo)
            label_camera.image = photo

mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

def ejecutar(nombre_carpeta):
    rutadata = "D:/USUARIO/Music/Eye_System/Interfaz-3.0-main/formularios/base_de_datos/data"
    personadata = os.path.join(rutadata, nombre_carpeta)

    if not os.path.exists(personadata):
        print("Carpeta creada:", personadata)
        os.makedirs(personadata)

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)
    
    if not cap.isOpened():
        print("Error al abrir la cámara")
        exit()

    faceclasif = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    count = 0
    
    # Buffer más simple usando deque
    fps_update_counter = 0
    current_fps = 0
    
    with mp_face_mesh.FaceMesh(
        static_image_mode=False,
        max_num_faces=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7,
        refine_landmarks=True) as face_mesh:
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Error al leer frame")
                break

            frame = imutils.resize(frame, width=320)
            frame = cv2.flip(frame, 1)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.equalizeHist(gray)
            auxframe = frame.copy()

            faces = faceclasif.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags=cv2.CASCADE_SCALE_IMAGE
            )

            # Actualizar FPS cada 30 frames
            fps_update_counter += 1
            if fps_update_counter >= 30:
                current_fps = int(cap.get(cv2.CAP_PROP_FPS))
                fps_update_counter = 0

            # Dibujar FPS en formato pequeño
            cv2.putText(frame, f"FPS:{current_fps}", (5, 15), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)

            if len(faces) > 0:
                for (x, y, w, h) in faces:
                    padding = int(0.1 * w)
                    x1 = max(0, x - padding)
                    y1 = max(0, y - padding)
                    x2 = min(frame.shape[1], x + w + padding)
                    y2 = min(frame.shape[0], y + h + padding)
                    
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    rostro = auxframe[y1:y2, x1:x2]
                    
                    if rostro.size > 0:
                        rostro = cv2.resize(rostro, (720, 720), interpolation=cv2.INTER_LANCZOS4)
                        
                        filename = f'rostro_{count}.jpg'
                        path = os.path.join(personadata, filename)
                        cv2.imwrite(path, rostro)
                        count += 1

                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = face_mesh.process(frame_rgb)

                if results.multi_face_landmarks:
                    for face_landmarks in results.multi_face_landmarks:
                        mp_drawing.draw_landmarks(
                            frame,
                            face_landmarks,
                            mp_face_mesh.FACEMESH_TESSELATION,
                            mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=1, circle_radius=1),
                            mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=1))

            cv2.imshow("Captura de Rostros con Malla Facial", frame)
            k = cv2.waitKey(1) & 0xFF
            if k == 27 or count >= 200:
                break

    cap.release()
    cv2.destroyAllWindows()

    def obtener_datos():
        try:
            conn = pymysql.connect(**db_config)
            cursor = conn.cursor()

            # Consulta para ingresos por jornada
            cursor.execute("""
                SELECT e.jornada, COUNT(*) as cantidad 
                FROM estudiante e
                JOIN ingreso i ON e.codigo_est = i.codigo_est
                WHERE i.fecha = CURDATE()
                GROUP BY e.jornada
            """)
            datos_jornada = pd.DataFrame(cursor.fetchall(), columns=['Jornada', 'Cantidad'])

            # Consulta para horas de llegada del día actual
            cursor.execute("""
                SELECT HOUR(i.hora) as hora, COUNT(*) as cantidad 
                FROM ingreso i
                WHERE i.fecha = CURDATE()
                GROUP BY HOUR(i.hora)
                ORDER BY hora
            """)
            datos_horas = pd.DataFrame(cursor.fetchall(), columns=['Hora', 'Cantidad'])

            # Consulta para total de estudiantes
            cursor.execute("SELECT COUNT(*) FROM estudiante")
            total_estudiantes = cursor.fetchone()[0]

            # Consulta para ingresos del día
            cursor.execute("SELECT COUNT(*) FROM ingreso WHERE fecha = CURDATE()")
            ingresos_hoy = cursor.fetchone()[0]

            # Consulta para obtener distribución por grupos
            cursor.execute("""
                SELECT grupo, COUNT(*) as cantidad
                FROM estudiante
                GROUP BY grupo
            """)
            datos_grupos = pd.DataFrame(cursor.fetchall(), columns=['Grupo', 'Cantidad'])

            cursor.close()
            conn.close()

            return datos_jornada, datos_horas, total_estudiantes, ingresos_hoy, datos_grupos

        except Exception as e:
            print(f"Error al obtener datos: {e}")
            return None, None, 0, 0, None