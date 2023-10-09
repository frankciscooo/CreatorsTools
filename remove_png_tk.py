import tkinter as tk
from tkinter import filedialog, messagebox
from rembg import remove
import os
from tkinterdnd2 import DND_FILES, TkinterDnD

def convert_file():
    try:
        input_path = file_entry.get()
        if input_path:
            # Generar el nombre del archivo modificado
            output_folder = filedialog.askdirectory()
            if output_folder:
                # Obtener el nombre base del archivo de entrada
                input_filename = os.path.basename(input_path)
                # Obtener el número disponible para el archivo modificado
                count = get_available_count(output_folder, input_filename)
                # Generar el nombre del archivo modificado
                modified_filename = f"background_deleted_{count}.png"
                # Generar la ruta completa del archivo de salida
                output_path = os.path.join(output_folder, modified_filename)
                with open(input_path, 'rb') as i:
                    with open(output_path, 'wb') as o:
                        input_data = i.read()
                        output_data = remove(input_data)
                        o.write(output_data)
                messagebox.showinfo(title="Borrado del fondo", message="Borrado completado")
                file_entry.delete(0, tk.END)  # Limpiar la zona de entrada de la ruta del archivo
        else:
            messagebox.showerror("Error", "Selecciona un archivo.")
    except Exception as e:
        messagebox.showerror("Error", "Corrige la ruta de tu archivo.")

def open_file_dialog():
    file = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*png;*jfif;*webm")])
    if file:
        file_entry.delete(0, tk.END)
        file_entry.insert(tk.END, file)

def drop_file(event):
    file = event.data
    if file:
        file_entry.delete(0, tk.END)
        file_entry.insert(tk.END, file)

def get_available_count(output_folder, filename):
    count = 1
    while os.path.exists(os.path.join(output_folder, f"background_deleted_{count}.png")):
        count += 1
    return count

root = TkinterDnD.Tk()
root.title("Eliminar Fondo de Imagen")
root.geometry("400x200")
root.configure(bg="#222222")
root.resizable(False, False)

title_label = tk.Label(root, text="Arrastra y suelta o haz clic para seleccionar una imagen:", fg="white", bg="#7e3bb7", width=50, height=1)
title_label.pack(pady=10)

file_entry = tk.Entry(root, width=30)
file_entry.pack(pady=10)

open_button = tk.Button(root, text="Buscar Archivo", command=open_file_dialog, fg="white", bg="#7e3bb7", width=20)
open_button.pack(pady=10)

convert_button = tk.Button(root, text="Empezar con el borrado del fondo", command=convert_file, fg="white", bg="#7e3bb7", width=30)
convert_button.pack(pady=10)

root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', drop_file)

root.mainloop()