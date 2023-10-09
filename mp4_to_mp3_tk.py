import tkinter as tk
from tkinter import filedialog, messagebox
from moviepy.editor import *
import threading

def show_menu():
    # Función para convertir el archivo MP4 a MP3
    def convert_to_mp3(mp4_file):
        try:
            # Cargar el video y extraer el audio
            video = VideoFileClip(mp4_file)
            audio = video.audio

            # Crear el nombre del archivo MP3
            mp3_file = mp4_file.replace(".mp4", ".mp3")

            # Abrir el cuadro de diálogo para seleccionar la ruta de guardado
            folder_path = filedialog.askdirectory()
            if folder_path:
                mp3_file = os.path.join(folder_path, os.path.basename(mp3_file))

                # Escribir el archivo de audio MP3
                audio.write_audiofile(mp3_file, codec="mp3", fps=44100, nbytes=2, logger=None)

                print(f"MP3 file '{mp3_file}' generated.")
                messagebox.showinfo("Conversión Completa", "La conversión del archivo se ha completado.")

                file_entry.delete(0, tk.END)  # Eliminar la ruta del archivo actual

        except Exception as e:
            print("Error converting file:", str(e))

    # Función para abrir el cuadro de diálogo para seleccionar un archivo
    def open_file_dialog():
        file = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4")])
        if file:
            file_entry.delete(0, tk.END)
            file_entry.insert(tk.END, file)

    # Función para iniciar la conversión
    def convert():
        file = file_entry.get()
        if not file:
            messagebox.showerror("Error", "Selecciona un archivo")
            return

        messagebox.showinfo("Iniciando Conversión", "Su archivo está siendo convertido...")

        # Ejecutar la conversión en un hilo separado para evitar bloquear la interfaz de usuario
        threading.Thread(target=convert_to_mp3, args=(file,)).start()

    # Crear la ventana principal
    root = tk.Tk()
    root.title("MP4 to MP3 Converter")
    root.geometry("400x180")
    root.configure(bg="#222222")
    root.resizable(False, False)

    # Etiqueta de título
    title_label = tk.Label(root, text="Arrastra y suelta o haz clic para seleccionar un archivo MP4:", fg="white", bg="#7e3bb7", width=50, height=1)
    title_label.pack(pady=10)

    # Campo de entrada de archivo
    file_entry = tk.Entry(root, width=30)
    file_entry.pack(pady=10)

    # Botón para abrir el cuadro de diálogo de selección de archivo
    open_button = tk.Button(root, text="Buscar Archivo", command=open_file_dialog, fg="white", bg="#7e3bb7", width=20)
    open_button.pack(pady=10)

    # Botón para iniciar la conversión
    convert_button = tk.Button(root, text="Convertir", command=convert, fg="white", bg="#7e3bb7", width=20)
    convert_button.pack(pady=10)

    root.mainloop()

# Llamar a la función para mostrar el menú
show_menu()