import tkinter as tk
from tkinter import filedialog, messagebox
from pytube import YouTube
from moviepy.editor import *
import os
import urllib.request
from PIL import Image, ImageTk

# Sección de funciones
def show_menu():
    def download_video():
        url = url_entry.get()
        if not is_valid_url(url):
            messagebox.showerror("Error", "El enlace que has introducido no es válido")
            url_entry.delete(0, tk.END)
            return
        root.destroy()
        download_video_with_url(url)

    def paste_from_clipboard():
        clipboard_content = root.clipboard_get()
        url_entry.insert(tk.END, clipboard_content)

    def is_valid_url(url):
        try:
            YouTube(url)
            return True
        except:
            return False

    root = tk.Tk()
    root.title("Creators Tools")
    root.configure(bg="#222222")
    root.geometry("300x150")
    root.resizable(False, False)

    title_label = tk.Label(root, text="Ingresa la URL del video de YouTube:", fg="white", bg="#7e3bb7", width=50, height=1)
    title_label.pack(pady=10)

    url_entry = tk.Entry(root, width=40)
    url_entry.pack(pady=10)

    paste_button = tk.Button(root, text="Pegar URL", command=paste_from_clipboard, fg="white", bg="#7e3bb7", width=10)
    paste_button.pack(pady=15, padx=40, side="left")

    download_button = tk.Button(root, text="Descargar", command=download_video, fg="white", bg="#7e3bb7", width=10)
    download_button.pack(pady=15, padx=40, side="right")

    root.mainloop()

def download_video_with_url(url):
    def select_folder():
        folder_selected = filedialog.askdirectory()
        return folder_selected

    def show_download_complete():
        messagebox.showinfo("Descarga completa", "El archivo ha sido descargado")

    def download_selected_video():
        selected_quality_index = variable.get()
        selected_video_stream = yt_quality[selected_quality_index]
        folder_path = select_folder()
        if folder_path:
            selected_video_stream.download(output_path=folder_path)
            show_download_complete()
            root.destroy()
            show_menu()

    def download_selected_audio():
        selected_audio_stream = yt_audio[answer_var.get() - len(yt_quality)]
        folder_path = select_folder()
        if folder_path:
            audio_path = selected_audio_stream.download(folder_path)
            mp3_path = os.path.splitext(audio_path)[0] + ".mp3"
            audio = AudioFileClip(audio_path)
            audio.write_audiofile(mp3_path)
            os.remove(audio_path)
            show_download_complete()
            root.destroy()
            show_menu()

    # Variables
    check = True
    yt = YouTube(url)
    yt_title = yt.title
    yt_thumbnail = yt.thumbnail_url
    yt_quality = yt.streams.filter(progressive=True).order_by('resolution')
    yt_audio = yt.streams.filter(only_audio=True)

    # Crear ventana de tkinter
    root = tk.Tk()
    root.title("Creators Tools")
    root.configure(bg="#222222")
    root.geometry("460x400")
    root.resizable(False, False)

    # Descargar la miniatura del video
    urllib.request.urlretrieve(yt_thumbnail, "thumbnail.png")
    thumbnail_image = Image.open("thumbnail.png")
    thumbnail_image = thumbnail_image.resize((185, 110), Image.ANTIALIAS)
    thumbnail_image = ImageTk.PhotoImage(thumbnail_image)

    # Mostrar miniatura del video
    thumbnail_label = tk.Label(root, image=thumbnail_image, bg="#7e3bb7", border=2)
    thumbnail_label.grid(row=0, column=0, padx=10, pady=25, rowspan=2)

    # Mostrar título del video
    if len(yt_title) > 20:
        yt_title = yt_title[:17] + "..."
    title_label = tk.Label(root, text=yt_title ,fg="white", bg="#7e3bb7", border=5)
    title_label.grid(row=2, column=0, padx=10, pady=10)

    # Creators Tools
    quality_label = tk.Label(root, text="Creators Tools",font=("Lemon Milk Bold",8) ,fg="white", bg="#7e3bb7", border=5, width=18)
    quality_label.grid(row=0, column=3, padx=45, pady=10)

    # Mostrar opciones de calidad de video y audio
    quality_label = tk.Label(root, text="Seleccione la calidad:", fg="white", bg="#7e3bb7", border=5)
    quality_label.grid(row=1, column=3, padx=10, pady=10)

    answer_var = tk.IntVar()

    # Bucle For en conjunto para las casillas de Video y Audio
    yt_streams = list(yt_quality) + list(yt_audio)
    variable = tk.IntVar()  # Crear una variable compartida para los botones de radio

    for i, stream in enumerate(yt_streams):
        if i < len(yt_quality):
            text = f"{stream.resolution} / mp4"
            row = i + 2
        else:
            webm = stream.mime_type.replace("audio/webm", "mp3")
            if webm in stream.mime_type:
                text = f"{stream.abr} / mp3"
                row = i + len(yt_audio)
            else:
                continue
        radio_button = tk.Radiobutton(root, text=text, variable=variable, value=i, fg="white", bg="#222222",
                                      selectcolor="#7e3bb7")
        radio_button.grid(row=row, column=3)

    # Botón de descarga
    def download_selected():
        if variable.get() < len(yt_quality):
            download_selected_video()
        elif variable.get() >= len(yt_quality):
            download_selected_audio()
        else:
            messagebox.showerror("Error", "Selecciona una opción de descarga")

    download_button = tk.Button(root, text="Descargar", command=download_selected, fg="white", bg="#7e3bb7", width=20)
    download_button.grid(row=4, column=0, padx=10, pady=10)

    root.mainloop()

show_menu()