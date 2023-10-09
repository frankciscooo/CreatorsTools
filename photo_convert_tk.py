import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image
import os
from tkinterdnd2 import DND_FILES, TkinterDnD

def convert_photos():
    # Función para abrir el diálogo de selección de archivos
    def open_file_dialog():
        file = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        if file:
            file_entry.delete(0, tk.END)
            file_entry.insert(tk.END, file)

    # Función para manejar el archivo arrastrado y soltado
    def drop_file(event):
        file = event.data
        if file:
            file_entry.delete(0, tk.END)
            file_entry.insert(tk.END, file)

    # Función para guardar la imagen convertida en un archivo
    def save_file(image, directory, file_name):
        if os.path.exists(os.path.join(directory, file_name)):
            base_name, extension = os.path.splitext(file_name)
            counter = 1
            while True:
                new_name = f"{base_name}_{counter}{extension}"
                if not os.path.exists(os.path.join(directory, new_name)):
                    file_name = new_name
                    break
                counter += 1
        image.save(os.path.join(directory, file_name))

    # Función para convertir la imagen
    def convert():
        file = file_entry.get()
        if not file:
            messagebox.showerror("Error", "Selecciona un archivo")
            return
        try:
            image = Image.open(file)
        except OSError:
            messagebox.showerror("Error", "El archivo no ha sido encontrado, vuelve a intentar")
            return
        image_format = image.format
        messagebox.showinfo("Información", f"Tu archivo es: {image_format, image.size, image.mode}")
        request = extension_var.get()
        downloads_dir = os.path.expanduser("~" + os.sep + "Downloads")
        if request in ["JPEG", "JPG"]:
            image_png = image.convert("RGB")
            extension = "jpeg" if request == "JPEG" else "jpg"
        elif request == "PNG":
            image_png = image.convert("RGBA")
            extension = "png"
        else:
            messagebox.showerror("Error", "Extensión del archivo incorrecto")
            return
        file_name = "converted_image." + extension
        save_file(image_png, downloads_dir, file_name)
        messagebox.showinfo("Conversión completada")
        file_entry.delete(0, tk.END)

    # Crear la ventana principal de tkinter
    root = TkinterDnD.Tk()
    root.title("Photo Converter")
    root.geometry("400x260")
    root.configure(bg="#222222")
    root.resizable(False, False)

    # Etiqueta de título
    title_label = tk.Label(root, text="Arrastra o haz click en el botón:", fg="white", bg="#7e3bb7", width=50, height=1)
    title_label.pack(pady=10)

    # Campo de entrada de archivo
    file_entry = tk.Entry(root, width=24)
    file_entry.pack(pady=10)

    # Botón para abrir el diálogo de selección de archivos
    open_button = tk.Button(root, text="Buscar archivo", command=open_file_dialog, fg="white", bg="#7e3bb7", width=20)
    open_button.pack(pady=10)

    # Etiqueta para seleccionar la extensión del archivo
    extension_label = tk.Label(root, text="Selecciona la extensión que deseas:", fg="white", bg="#7e3bb7", width=50, height=1)
    extension_label.pack(pady=10)

    # Variable para almacenar la extensión seleccionada
    extension_var = tk.StringVar()

    # Variable para almacenar la extensión seleccionada
    extension = tk.StringVar()

    # Función para actualizar la variable de extensión seleccionada
    def update_extension_var():
        extension_var.set(extension.get())

    # Casillas para seleccionar la extensión del archivo
    extension_frame = tk.Frame(root, bg="#222222")
    extension_frame.pack()

    jpeg_radio = tk.Radiobutton(extension_frame, text="JPEG", variable=extension, value="JPEG", command=update_extension_var, fg="white", bg="#222222", selectcolor="#7e3bb7")
    jpeg_radio.pack(side=tk.LEFT, padx=5)

    jpg_radio = tk.Radiobutton(extension_frame, text="JPG", variable=extension, value="JPG", command=update_extension_var, fg="white", bg="#222222", selectcolor="#7e3bb7")
    jpg_radio.pack(side=tk.LEFT, padx=5)

    png_radio = tk.Radiobutton(extension_frame, text="PNG", variable=extension, value="PNG", command=update_extension_var, fg="white", bg="#222222", selectcolor="#7e3bb7")
    png_radio.pack(side=tk.LEFT, padx=5)

    # Botón para convertir la imagen
    convert_button = tk.Button(root, text="Convertir", command=convert, fg="white", bg="#7e3bb7", width=20)
    convert_button.pack(pady=10)

    # Registrar el destino de arrastrar y soltar archivos
    root.drop_target_register(DND_FILES)
    root.dnd_bind('<<Drop>>', drop_file)

    # Ejecutar el bucle principal de la aplicación
    root.mainloop()

# Llamar a la función principal para iniciar la aplicación
convert_photos()