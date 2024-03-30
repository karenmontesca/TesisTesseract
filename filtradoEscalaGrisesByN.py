import pytesseract
from pytesseract import Output
import cv2
import numpy as np

#Convierte la imagen a escala de grises.
#Aplica un umbral para convertir la imagen en blanco y negro.
#Aumenta el contraste de la imagen.
#Utiliza Tesseract en la imagen preprocesada y resalta el texto reconocido.



img = cv2.imread("glaysEDIT.png")

# Convertir la imagen a escala de grises
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


# Aplicar filtro gaussiano para suavizar la imagen y reducir el ruido
smooth_img = cv2.GaussianBlur(gray_img, (5, 5), 0)



# Aplicar detección de bordes con el algoritmo de Canny
edges_img = cv2.Canny(smooth_img, 50, 150)


# Aplicar transformaciones morfológicas para eliminar líneas horizontales y verticales
kernel = np.ones((5, 5), np.uint8)
dilated_img = cv2.dilate(edges_img, kernel, iterations=1)
eroded_img = cv2.erode(dilated_img, kernel, iterations=1)







# Aplicar un umbral para convertir la imagen en blanco y negro
_, binary_img = cv2.threshold(gray_img, 128, 255, cv2.THRESH_BINARY)

# Aumentar el contraste de la imagen
alpha = 1.5  # Factor de contraste
beta = 30    # Ajuste del brillo
contrast_img = cv2.convertScaleAbs(binary_img, alpha=alpha, beta=beta)

height, width, _ = img.shape

# Usar la función image_to_data en la imagen preprocesada
myconfig = r"--psm 6 --oem 3"
data = pytesseract.image_to_data(contrast_img, config=myconfig, output_type=Output.DICT)

amount_boxes = len(data['text'])
for i in range(amount_boxes):
    if float(data['conf'][i]) > 20:
        (x, y, width, height) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
        contrast_img = cv2.rectangle(contrast_img, (x, y), (x+width, y+height), (0,255,0), 2)
        contrast_img = cv2.putText(contrast_img, data['text'][i], (x, y+height+20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2, cv2.LINE_AA)
        
        # Imprimir el texto reconocido en la terminal
        print(data['text'][i])

# Mostrar la imagen preprocesada y resaltada
cv2.imshow("Preprocesada y Resaltada", contrast_img)
cv2.waitKey(0)
