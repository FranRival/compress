import os
import subprocess
from PIL import Image
import tkinter as tk
from tkinter import messagebox

# === CONFIGURACION ===
MAX_ANCHO = 1000
CALIDAD = 75

carpeta_salida_global = None  # Para usarla en botón "Abrir"

def comprimir_imagenes():
    global carpeta_salida_global

    carpeta_entrada = entry_ruta.get()

    if not os.path.isdir(carpeta_entrada):
        messagebox.showerror("Error", "Ruta no válida")
        return

    carpeta_salida = os.path.join(carpeta_entrada, "New")
    carpeta_salida_global = carpeta_salida
    os.makedirs(carpeta_salida, exist_ok=True)

    contador = 0

    for archivo in os.listdir(carpeta_entrada):
        if archivo.lower().endswith((".jpg", ".jpeg", ".png")):
            ruta_entrada = os.path.join(carpeta_entrada, archivo)
            nombre_sin_ext = os.path.splitext(archivo)[0]
            ruta_salida = os.path.join(carpeta_salida, nombre_sin_ext + ".jpg")

            with Image.open(ruta_entrada) as img:
                img = img.convert("RGB")

                if img.width > MAX_ANCHO:
                    ratio = MAX_ANCHO / img.width
                    nuevo_alto = int(img.height * ratio)
                    img = img.resize((MAX_ANCHO, nuevo_alto), Image.LANCZOS)

                img.save(
                    ruta_salida,
                    "JPEG",
                    quality=CALIDAD,
                    optimize=True,
                    progressive=True,
                    subsampling=2
                )

            contador += 1

    messagebox.showinfo("Listo", f"Compresión terminada\nImágenes procesadas: {contador}")

def abrir_carpeta():
    if carpeta_salida_global and os.path.isdir(carpeta_salida_global):
        os.startfile(carpeta_salida_global)
    else:
        messagebox.showwarning("Aviso", "Primero debes comprimir imágenes.")

# === INTERFAZ ===
ventana = tk.Tk()
ventana.title("Image Compressor")
ventana.geometry("420x180")
ventana.resizable(False, False)

label = tk.Label(ventana, text="Ruta de las imágenes:")
label.pack(pady=5)

entry_ruta = tk.Entry(ventana, width=55)
entry_ruta.pack(pady=5)

frame_botones = tk.Frame(ventana)
frame_botones.pack(pady=15)

boton_compress = tk.Button(frame_botones, text="Compress", width=15, command=comprimir_imagenes)
boton_compress.grid(row=0, column=0, padx=10)

boton_abrir = tk.Button(frame_botones, text="Abrir carpeta", width=15, command=abrir_carpeta)
boton_abrir.grid(row=0, column=1, padx=10)

ventana.mainloop()
