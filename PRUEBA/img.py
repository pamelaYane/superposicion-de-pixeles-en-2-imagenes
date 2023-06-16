import cv2
import numpy as np

# Cargar las dos imágenes secuenciales
imagen1 = cv2.imread('img/a1.png')
imagen2 = cv2.imread('img/a2.png')

# Obtener las dimensiones de ambas imágenes
altura_imagen1, ancho_imagen1 = imagen1.shape[:2]
altura_imagen2, ancho_imagen2 = imagen2.shape[:2]

# Calcular el tamaño de la imagen panorámica resultante
altura_resultante = max(altura_imagen1, altura_imagen2)
ancho_resultante = ancho_imagen1 + ancho_imagen2

# Crear una imagen en blanco del tamaño resultante
imagen_resultante = np.zeros((altura_resultante, ancho_resultante, 3), dtype=np.uint8)

# Copiar la primera imagen en la región correspondiente de la imagen resultante
imagen_resultante[:altura_imagen1, :ancho_imagen1] = imagen1

# Convertir las imágenes a escala de grises
gris1 = cv2.cvtColor(imagen1, cv2.COLOR_BGR2GRAY)
gris2 = cv2.cvtColor(imagen2, cv2.COLOR_BGR2GRAY)

# Encontrar los puntos clave y descriptores utilizando el algoritmo ORB
orb = cv2.ORB_create()
puntos1, descriptores1 = orb.detectAndCompute(gris1, None)
puntos2, descriptores2 = orb.detectAndCompute(gris2, None)

# Encontrar las coincidencias de puntos clave utilizando el algoritmo de correspondencia de fuerza bruta
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
coincidencias = bf.match(descriptores1, descriptores2)
coincidencias = sorted(coincidencias, key=lambda x: x.distance)

# Extraer los puntos clave correspondientes en ambas imágenes
puntos1_correspondientes = np.float32([puntos1[m.queryIdx].pt for m in coincidencias]).reshape(-1, 1, 2)
puntos2_correspondientes = np.float32([puntos2[m.trainIdx].pt for m in coincidencias]).reshape(-1, 1, 2)

# Calcular la matriz de transformación de perspectiva utilizando los puntos clave correspondientes
matriz_transformacion, _ = cv2.findHomography(puntos2_correspondientes, puntos1_correspondientes, cv2.RANSAC, 5.0)

# Aplicar la transformación de perspectiva a la segunda imagen para unirla con la primera imagen
imagen2_transformada = cv2.warpPerspective(imagen2, matriz_transformacion, (ancho_resultante, altura_resultante))

# Combinar las imágenes resultantes utilizando una operación de fusión
imagen_resultante = cv2.addWeighted(imagen_resultante, 0.5, imagen2_transformada, 0.5, 0)

# Recortar las áreas negras en la imagen resultante
gris_resultante = cv2.cvtColor(imagen_resultante, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gris_resultante, 1, 255, cv2.THRESH_BINARY)
contornos, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
x, y, w, h = cv2.boundingRect(contornos[0])
imagen_resultante_recortada = imagen_resultante[y:y+h, x:x+w]

# Redimensionar la imagen resultante
alto_mostrar = 500
ancho_mostrar = int((w/h) * alto_mostrar)
imagen_resultante_mostrar = cv2.resize(imagen_resultante, (ancho_mostrar, alto_mostrar))

# Mostrar la imagen resultante y la imagen resultante recortada
cv2.imshow('Imagen Resultante', imagen_resultante_mostrar)
cv2.imshow('Imagen Resultante Recortada', imagen_resultante_recortada)
cv2.waitKey(0)
cv2.destroyAllWindows()
