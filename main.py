import requests
from process_data import process_json_to_html_table

def main():
    # Hacer la solicitud HTTP
    url = 'https://app.nanonets.com/api/v2/OCR/Model/42a2bdf2-d95b-4371-9df6-65976f407e27/LabelFile/?async=false'
    data = {'file': open('IMG-20231124-WA0015.jpg', 'rb')}
    response = requests.post(url, auth=requests.auth.HTTPBasicAuth('a3d1b60f-edf6-11ee-be10-fa9fdd46a972', ''), files=data)

    # Verificar si la solicitud fue exitosa (código de estado HTTP 200)
    if response.status_code == 200:
        # Obtener la respuesta en formato JSON
        formatted_response = response.json()
        print("JSON recibido:")
        print(formatted_response)  # Imprimir el JSON recibido
        # Enviar los datos a la función de procesamiento
        process_json_to_html_table(formatted_response)
    else:
        # Imprimir el código de estado HTTP si la solicitud no fue exitosa
        print("Error:", response.status_code)

if __name__ == "__main__":
    main()
