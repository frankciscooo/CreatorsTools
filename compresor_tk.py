import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import subprocess
import os
import platform
from tkinterdnd2 import DND_FILES, TkinterDnD

def get_downloads_folder():
    system = platform.system()
    if system == 'Windows':
        return os.path.expanduser('~\\Downloads')
    elif system == 'Linux' or system == 'Darwin':
        return os.path.expanduser('~/Downloads')
    else:
        raise NotImplementedError("Unsupported operating system")

def compress_image(input_image, output_folder, output_quality=85):
    try:
        img = Image.open(input_image)
        output_image = os.path.join(output_folder, f'compressed_{os.path.basename(input_image)}')
        img.save(output_image, quality=output_quality, optimize=True)
        print(f"Image '{input_image}' compressed and saved as '{output_image}'")
        messagebox.showinfo("Compresión Completa", f"La imagen '{input_image}' se ha comprimido y guardado como '{output_image}'")
    except Exception as e:
        print(f"An error occurred: {e}")
        messagebox.showerror("Error", f"Ocurrió un error: {e}")

def compress_video(input_video, output_folder, crf=30):
    try:
        output_video = os.path.join(output_folder, f'compressed_{os.path.basename(input_video)}')
        subprocess.run(['ffmpeg', '-i', input_video, '-c:v', 'libx264', '-crf', str(crf), '-c:a', 'aac', output_video])
        print(f"Video '{input_video}' compressed and saved as '{output_video}'")
        messagebox.showinfo("Compresión Completa", f"El video '{input_video}' se ha comprimido y guardado como '{output_video}'")
    except Exception as e:
        print(f"An error occurred: {e}")
        messagebox.showerror("Error", f"Ocurrió un error: {e}")

def compress_file():
    def open_file_dialog():
        file = filedialog.askopenfilename()
        if file:
            file_entry.delete(0, tk.END)
            file_entry.insert(tk.END, file)

    def drop_file(event):
        file = event.data
        if file:
            file_entry.delete(0, tk.END)
            file_entry.insert(tk.END, file)

    def compress():
        file = file_entry.get()
        if not file:
            messagebox.showerror("Error", "Selecciona un archivo")
            return

        output_folder = filedialog.askdirectory()
        if not output_folder:
            return

        if file.endswith(('.jpg', '.jpeg', '.png')):
            quality = quality_scale.get()
            compress_image(file, output_folder, output_quality=quality)
        elif file.endswith(('.mp4', '.avi', '.mov')):
            crf = crf_scale.get()
            compress_video(file, output_folder, crf=crf)
        else:
            messagebox.showerror("Error", "Formato de archivo no compatible")

        file_entry.delete(0, tk.END)

    root = TkinterDnD.Tk()
    root.title("Compresor de Archivos")
    root.geometry("400x290")
    root.configure(bg="#222222")
    root.resizable(False, False)

    title_label = tk.Label(root, text="Selecciona un archivo para comprimir:", fg="white", bg="#7e3bb7", width=50, height=1)
    title_label.pack(pady=10)

    file_entry = tk.Entry(root, width=30)
    file_entry.pack(pady=10)

    open_button = tk.Button(root, text="Buscar Archivo", command=open_file_dialog, fg="white", bg="#7e3bb7", width=20)
    open_button.pack(pady=10)

    if platform.system() == 'Windows':
        quality_label = tk.Label(root, text="Calidad (1-100):", fg="white", bg="#7e3bb7", width=28, height=1)
        quality_label.pack(pady=10)

        quality_scale = tk.Scale(root, from_=1, to=100, orient=tk.HORIZONTAL, length=200, bg="#7e3bb7", fg="white")
        quality_scale.set(85)
        quality_scale.pack(pady=10)
    else:
        crf_label = tk.Label(root, text="CRF (18-30):", fg="white", bg="#7e3bb7", width=50, height=1)
        crf_label.pack(pady=10)

        crf_scale = tk.Scale(root, from_=18, to=30, orient=tk.HORIZONTAL, length=200)
        crf_scale.set(30)
        crf_scale.pack(pady=10)

    compress_button = tk.Button(root, text="Comprimir", command=compress, fg="white", bg="#7e3bb7", width=20)
    compress_button.pack(pady=10)

    root.drop_target_register(DND_FILES)
    root.dnd_bind('<<Drop>>', drop_file)

    root.mainloop()

compress_file()