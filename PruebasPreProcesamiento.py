import cv2
import numpy as np

# Cargar la imagen
img = cv2.imread("IMGPrueba.jpg", cv2.IMREAD_GRAYSCALE)

# Aplicar umbral adaptativo
binary_img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 4)

# Aplicar operaciones morfológicas para limpiar y resaltar las letras
kernel = np.ones((3,3),np.uint8)
opening = cv2.morphologyEx(binary_img, cv2.MORPH_OPEN, kernel, iterations=1)
result = cv2.bitwise_and(binary_img, opening)

# Mostrar la imagen resultante
cv2.imshow("Resultado", result)
cv2.waitKey(0)
cv2.destroyAllWindows()
