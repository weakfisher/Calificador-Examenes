
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import cv2
import json
from algoritmo import obtenerRespuesta

class CalculadoraCalificacion:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title('Calculadora de Calificación')
        self.ventana.geometry('600x400')
        self.ventana.config(bg="#f2f2f2")
        
        self.resultado = tk.StringVar()
        self.respuestasMostradas = tk.StringVar()
        self.archivo_imagen = None

        self.respuestas_correctas = self.cargar_respuestas()

        if not self.respuestas_correctas:
            messagebox.showerror("Error", "No se pudieron cargar las respuestas correctas.")
            self.ventana.destroy()

        self.crear_ui()

    def cargar_respuestas(self):
        try:
            with open('respuestas_correctas.json', 'r') as file:
                respuestas = json.load(file)
            return respuestas
        except FileNotFoundError:
            messagebox.showerror("Error", "No se encontró el archivo de respuestas correctas.")
            return []

    def crear_ui(self):
        titulo = ttk.Label(self.ventana, text="Calculadora de Calificación", font=("Helvetica", 18, "bold"), background="#f2f2f2", foreground="#4CAF50")
        titulo.pack(pady=20)
        
        
        instrucciones = ttk.Label(self.ventana, text="Haz clic en 'Calificar' para cargar la imagen y calcular la calificación", 
                                  font=("Arial", 12), background="#f2f2f2", foreground="#555")
        instrucciones.pack(pady=10)

        etiqueta_respuestas = ttk.Label(self.ventana, textvariable=self.respuestasMostradas, font=("Arial", 12), background="#f2f2f2", foreground="#333")
        etiqueta_respuestas.pack(pady=10)

        etiqueta_calificacion = ttk.Label(self.ventana, textvariable=self.resultado, font=("Arial", 14, "bold"), background="#f2f2f2", foreground="#4CAF50")
        etiqueta_calificacion.pack(pady=20)

        boton_calcular = ttk.Button(self.ventana, text="Calificar", command=self.calcular_calificacion, style="TButton")
        boton_calcular.pack(pady=20)

        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12), padding=10, relief="raised", background="#4CAF50", foreground="black", width=20)

    def calcular_calificacion(self):
        archivo_imagen = filedialog.askopenfilename(title="Seleccionar Imagen", filetypes=[("Archivos de imagen", "*.png;*.jpg;*.jpeg")])
        
        if archivo_imagen:
            img = cv2.imread(archivo_imagen, 0)
                   
            respuestas_usuario = obtenerRespuesta(img)
            respuestas_str = ", ".join(respuestas_usuario)
            self.respuestasMostradas.set(f"Respuestas obtenidas: {respuestas_str}")
            # Comparar las respuestas 
            correctas = sum(1 for i in range(len(self.respuestas_correctas)) if respuestas_usuario[i] == self.respuestas_correctas[i])           
            calificacion = (correctas / len(self.respuestas_correctas)) * 10         
            calificacion_str = f"Tu calificación es: {calificacion:.2f}"
            self.resultado.set(calificacion_str)
        else:
            messagebox.showwarning("Advertencia", "No se seleccionó ninguna imagen.")
            
if __name__ == "__main__":
    ventana = tk.Tk()
    calculadora = CalculadoraCalificacion(ventana)
    ventana.mainloop()
