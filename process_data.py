import json

def process_json_to_html_table(response_data):
    # Obtener las predicciones
    predictions = response_data.get('result', [])[0].get('prediction', [])
    
    # Crear la tabla HTML
    html_table = "<table border='1'>"
    
    # Iterar sobre cada predicción
    for prediction in predictions:
        cells = prediction.get('cells', [])
        
        # Verificar si hay celdas
        if cells:
            # Obtener el número máximo de filas y columnas
            max_row = max(cell.get('row', 0) for cell in cells)
            max_col = max(cell.get('col', 0) for cell in cells)
            
            # Crear una matriz para contener el texto de cada celda
            cell_texts = [['' for _ in range(max_col)] for _ in range(max_row)]
            
            # Iterar sobre cada celda y colocar el texto en la matriz
            for cell in cells:
                row = cell.get('row', 0) - 1
                col = cell.get('col', 0) - 1
                cell_text = cell.get('text', '')
                cell_texts[row][col] = cell_text
                
            # Agregar filas y celdas a la tabla HTML
            for row in cell_texts:
                html_table += "<tr>"
                for cell_text in row:
                    html_table += f"<td><textarea style='width:100%; height:100%;'>{cell_text}</textarea></td>"
                html_table += "</tr>"
    
    # Cerrar la tabla HTML
    html_table += "</table>"
    
    # Guardar la tabla en un archivo HTML con codificación UTF-8
    with open("output.html", "w", encoding="utf-8") as html_file:
        html_file.write(html_table)

# Ejemplo de uso
response_data = {
    "result": [{
        "prediction": [
            {"text": "Juan", "col": 1, "row": 1},
            {"text": "25", "col": 1, "row": 2},
            {"text": "María", "col": 2, "row": 1},
            {"text": "30", "col": 2, "row": 2}
        ]
    }]
}

process_json_to_html_table(response_data)
