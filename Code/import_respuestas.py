import json

# Respuestas correctas (hardcodeadas)
respuestas_correctas = ["B", 'C', 'D', 'E', "B", 'C', 'C', 'A', "A", 'B', 'C', 'A', 
                        "E", 'A', 'A', 'A', "B", 'C', 'A', 'A', "B", 'C', 'A', 'A', 
                        'B', 'C']

# Guardar las respuestas correctas en un archivo JSON
def guardar_respuestas(respuestas):
    with open('respuestas_correctas.json', 'w') as file:
        json.dump(respuestas, file)
        
guardar_respuestas(respuestas_correctas)