import pytesseract
import cv2

myconfig = r"--psm 6 --oem 3"
img = cv2.imread("IMG-20231124-WA0015.jpg")

if img is None:
    print("Error: No se pudo cargar la imagen.")
else:
    height, width, _ = img.shape

    # Convertimos la imagen en cajitas 
    boxes = pytesseract.image_to_boxes(img, config=myconfig)

    # Nos va a dar los caracteres individuales y las coordenadas
    for box in boxes.splitlines():
        box = box.split(" ")
        x, y, w, h = int(box[1]), height - int(box[2]), int(box[3]), height - int(box[4])
        
        # Dibujar rectángulos en cada carácter en la imagen original
        img = cv2.rectangle(img, (x, y), (w, h), (0, 255, 0), 2)

        # Obtener el texto del carácter y mostrarlo encima de la imagen
        char = box[0]
        cv2.putText(img, char, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    cv2.imshow("img", img)
    cv2.waitKey(0)
