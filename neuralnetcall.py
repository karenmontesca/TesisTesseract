import requests
import json

url = 'https://app.nanonets.com/api/v2/OCR/Model/42a2bdf2-d95b-4371-9df6-65976f407e27/LabelFile/?async=false'

data = {'file': open('IMG-20231124-WA0015.jpg', 'rb')}

response = requests.post(url, auth=requests.auth.HTTPBasicAuth('a3d1b60f-edf6-11ee-be10-fa9fdd46a972', ''), files=data)

# Verificar si la solicitud fue exitosa (código de estado HTTP 200)
if response.status_code == 200:
    # Obtener la respuesta en formato JSON
    formatted_response = response.json()
else:
    # Imprimir el código de estado HTTP si la solicitud no fue exitosa
    print("Error:", response.status_code)

# Crear una tabla HTML con estilos CSS
html_table = """
<!DOCTYPE html>
<html>
<head>
<style>
table {
  border-collapse: collapse;
  width: 100%;
}

th, td {
  border: 1px solid #dddddd;
  text-align: left;
  padding: 8px;
}

th {
  background-color: #f2f2f2;
}
</style>
</head>
<body>

<table>
  <tr>
    <th>ID</th>
    <th>Text</th>
  </tr>
"""

for item in formatted_response['result'][0]['prediction']:
    html_table += f"<tr><td>{item['id']}</td><td>{item['ocr_text']}</td></tr>"

html_table += """
</table>

</body>
</html>
"""

# Guardar el contenido de la tabla en un archivo HTML
with open("output.html", "w") as html_file:
    html_file.write(html_table)
