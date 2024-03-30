import requests

def llamar_api_cognitive_services(image_path):
    # URL de la API
    endpoint = "https://ocrarzobispado.cognitiveservices.azure.com/vision/v3.2/analyze"
    subscription_key = "1e9e3d717a7e41c8845a266ef91f9e7c"
    
#https://ocrarzobispado.cognitiveservices.azure.com/


    # Parámetros y encabezados de la solicitud
    params = {
        "features": "tags, objects, caption",
        "language": "en"
    }
    headers = {
        "Content-Type": "application/octet-stream",
        "Ocp-Apim-Subscription-Key": subscription_key
    }

    # Leer la imagen desde el disco
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()

    # Realizar la solicitud a la API
    response = requests.post(endpoint, params=params, headers=headers, data=image_data)

    # Manejar la respuesta
    if response.status_code == 200:
        print("Respuesta exitosa:")
        print(response.json())
    else:
        print("Error al llamar a la API:")
        print(response.status_code, response.text)

# Ruta de la imagen en tu disco
ruta_imagen = "Gladys.jpg"

# Llamar a la función para ejecutar la solicitud
llamar_api_cognitive_services(ruta_imagen)
