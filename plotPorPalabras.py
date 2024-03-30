import pytesseract
from pytesseract import Output
import cv2
import numpy as np



myconfig = r"""--psm 6 --oem 3 
# Configuración para Tesseract OCR
tessedit_char_whitelist ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789áéíóúüñÁÉÍÓÚÜÑ

# Palabras adicionales a tener en cuenta
tessedit_word_list_clear 1
tessedit_unrej_any_wd 1
tessedit_fix_fuzzy_words 1

# Agrega palabras específicas a tener en cuenta (nombres en español)
user_words
    María
    José
    Alejandro
    Gabriela
    Carlos
    Sofía
    Veronica
    Ricardina
    Marina
    Mirta
    Maria
    Dina
    Gladys
    Abel
    Alejandro
    Miguel
    Lázaro
    Enrique
    Jorge
    Padre
    Madre
    Madrina
    Elías
    Elias
    Urrioña
    Elvira
    Carmen
    Teresa
    Rosa
    Berta
    Ayde
    Caloggero
    Caycho
    Peña
    Camacho
    El
    Obispo
    que
    suscribe
    certifica
    Padre
    Madre
    Padrino
    Madrina

# Configuración adicional
another_config_option 123
"""


img_path = "IMGPrueba.jpg"

# Cargar la imagen original
img = cv2.imread(img_path)

if img is None:
    print(f"Error: No se pudo cargar la imagen {img_path}")
else:
    # Convertir la imagen a escala de grises
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)



    
    # Aplicar un umbral para convertir la imagen en blanco y negro
    _, binary_img = cv2.threshold(gray_img, 128, 255, cv2.THRESH_BINARY)
      
    # Aumentar el contraste de la imagen
    alpha = 1.5  # Factor de contraste
    beta = 30    # Ajuste del brillo
    contrast_img = cv2.convertScaleAbs(binary_img, alpha=alpha, beta=beta)


    # Ejemplo de suavización con filtro gaussiano
    smoothed_img = cv2.GaussianBlur(contrast_img, (5, 5), 0)


    # Eliminar caracteres no deseados directamente en la configuración de Tesseract
    unwanted_chars = [';','“','¿','/','_','?','ö','%','&','*','»','º',',','.','/','!','"','#','$','(',')']
    for char in unwanted_chars:
        myconfig += f'\nunlv_tilde_{ord(char)} 0'
  
  

    # Aplicar un filtro de alta frecuencia para mejorar la nitidez
    kernel = np.array([[-1, -1, -1],
                      [-1,  9, -1],
                      [-1, -1, -1]])
    
    
    sharpened_img = cv2.filter2D(smoothed_img, -1, kernel)
   
      # Antes de aplicar OCR, realizar preprocesamiento adicional

    

    # Aplica OCR a la imagen umbralizada usando Tesseract
    data = pytesseract.image_to_data(sharpened_img, config=myconfig, output_type=Output.DICT)

    amount_boxes = len(data['text'])

    # Diccionario para almacenar el texto por línea
    text_by_line = {}

    for i in range(amount_boxes):
        if float(data['conf'][i]) > 1:
            (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])

            # Agrega el texto reconocido al diccionario por línea
            line_key = y // 40  # Aproximadamente 40 píxeles por línea
            if line_key not in text_by_line:
                text_by_line[line_key] = []

            # Eliminar caracteres no deseados (por ejemplo, '|') de cada palabra
            cleaned_text = data['text'][i].replace('|', '')
            text_by_line[line_key].append(cleaned_text)

            # Dibuja rectángulo en verde alrededor de la palabra en la imagen original
            img = cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # Agrega el texto reconocido encima de la imagen en azul
            img = cv2.putText(img, cleaned_text, (x, y+h+20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2, cv2.LINE_AA)

    # Imprime el texto por línea en la consola
    for line_key in sorted(text_by_line.keys()):
        line_text = ' '.join(text_by_line[line_key])
        print(f"Línea {line_key + 1}: {line_text}")

    # Mostrar la imagen original con texto resaltado y preprocesado
    cv2.imshow("img", img)
    cv2.imshow("sharpened_img", sharpened_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
