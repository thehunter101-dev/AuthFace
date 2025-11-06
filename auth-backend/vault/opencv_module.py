import numpy as np
import cv2
from PIL import Image
import insightface

# Inicializamos el modelo globalmente para no cargarlo cada vez
model = insightface.app.FaceAnalysis(name="buffalo_l")  # Modelo base de InsightFace
model.prepare(ctx_id=-1)  # Usa CPU; cambia a 0 si tienes GPU

def encode_embedding(rostro):
    # Leer imagen desde el archivo ContentFile
    img_array = np.frombuffer(rostro.read(), np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    if img is None:
        print(f"No se pudo decodificar {rostro.name}")

    # Detectar rostros y generar embeddings
    faces = model.get(img)

    if len(faces) == 0:
        print(f"No se detectó rostro en {rostro.name}")

    # Tomar el embedding del primer rostro encontrado
    embedding = faces[0].embedding
    return embedding

def generar_embeddings(rostros):
    """
    Genera embeddings faciales (vectores de características) a partir de una lista de imágenes.

    Parámetros:
        rostros: lista de archivos tipo ContentFile (imágenes capturadas)

    Retorna:
        Lista de embeddings (vectores numpy convertidos a listas para serialización)
    """
    embeddings = []

    for rostro in rostros:
        embedding = encode_embedding(rostro)
        embeddings.append(embedding.tolist())
    embedding_prom = np.mean(np.array(embeddings),axis=0)

    return embedding_prom.tolist()