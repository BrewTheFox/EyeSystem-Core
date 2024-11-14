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