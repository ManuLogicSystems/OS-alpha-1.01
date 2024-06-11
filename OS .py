import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import os
import webbrowser
from datetime import datetime
import time

try:
    import pygame
    pygame.mixer.init()
    pygame_available = True
except ImportError:
    pygame_available = False

# Funciones básicas para las "aplicaciones"
def abrir_calculadora():
    calc_win = tk.Toplevel(root)
    calc_win.title("Calculadora")

    def calcular():
        try:
            a = int(entry_a.get())
            b = int(entry_b.get())
            resultado.set(a + b)
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa valores enteros válidos")

    tk.Label(calc_win, text="Valor1:").grid(row=0, column=0)
    entry_a = tk.Entry(calc_win)
    entry_a.grid(row=0, column=1)

    tk.Label(calc_win, text="Valor2:").grid(row=1, column=0)
    entry_b = tk.Entry(calc_win)
    entry_b.grid(row=1, column=1)

    resultado = tk.StringVar()
    tk.Label(calc_win, text="Resultado:").grid(row=2, column=0)
    tk.Label(calc_win, textvariable=resultado).grid(row=2, column=1)

    tk.Button(calc_win, text="Calcular", command=calcular).grid(row=3, columnspan=2)

def abrir_editor_texto():
    editor_win = tk.Toplevel(root)
    editor_win.title("Editor de texto")

    text_area = tk.Text(editor_win)
    text_area.pack(expand=True, fill='both')

    def guardar_como():
        archivo = filedialog.asksaveasfilename(defaultextension=".txt", 
                                               filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if archivo:
            with open(archivo, "w") as file:
                file.write(text_area.get(1.0, tk.END))
            messagebox.showinfo("Guardado", f"Archivo guardado en {archivo}")

    tk.Button(editor_win, text="Guardar como", command=guardar_como).pack()

def abrir_navegador_archivos():
    navegador_win = tk.Toplevel(root)
    navegador_win.title("Navegador de archivos")

    def abrir_archivo():
        archivo = filedialog.askopenfilename()
        if archivo:
            os.startfile(archivo)

    def copiar_archivo():
        archivo = filedialog.askopenfilename()
        if archivo:
            destino = filedialog.askdirectory()
            if destino:
                os.system(f'copy "{archivo}" "{destino}"')
                messagebox.showinfo("Copia de archivo", f"Archivo copiado a {destino}")

    def mover_archivo():
        archivo = filedialog.askopenfilename()
        if archivo:
            destino = filedialog.askdirectory()
            if destino:
                os.system(f'move "{archivo}" "{destino}"')
                messagebox.showinfo("Movimiento de archivo", f"Archivo movido a {destino}")

    def eliminar_archivo():
        archivo = filedialog.askopenfilename()
        if archivo:
            os.remove(archivo)
            messagebox.showinfo("Eliminar archivo", "Archivo eliminado")

    tk.Button(navegador_win, text="Abrir archivo", command=abrir_archivo).pack()
    tk.Button(navegador_win, text="Copiar archivo", command=copiar_archivo).pack()
    tk.Button(navegador_win, text="Mover archivo", command=mover_archivo).pack()
    tk.Button(navegador_win, text="Eliminar archivo", command=eliminar_archivo).pack()

def abrir_navegador_web():
    navegador_web_win = tk.Toplevel(root)
    navegador_web_win.title("Navegador web")

    def ir_a_url():
        url = entry_url.get()
        if not url.startswith("http"):
            url = "http://" + url
        webbrowser.open(url)

    entry_url = tk.Entry(navegador_web_win)
    entry_url.pack(fill='x', expand=True)
    tk.Button(navegador_web_win, text="Ir", command=ir_a_url).pack()

def abrir_reproductor_musica():
    if not pygame_available:
        messagebox.showerror("Error", "pygame no está disponible. Instala pygame para usar el reproductor de música.")
        return

    reproductor_win = tk.Toplevel(root)
    reproductor_win.title("Reproductor de Música")

    playlist = []

    def cargar_musica():
        archivos = filedialog.askopenfilenames(filetypes=[("Audio Files", "*.mp3 *.wav")])
        for archivo in archivos:
            playlist.append(archivo)
            listbox.insert(tk.END, os.path.basename(archivo))

    def reproducir():
        if playlist:
            pygame.mixer.music.load(playlist[listbox.curselection()[0]])
            pygame.mixer.music.play()

    def pausar():
        pygame.mixer.music.pause()

    def reanudar():
        pygame.mixer.music.unpause()

    def detener():
        pygame.mixer.music.stop()

    def ajustar_volumen(vol):
        pygame.mixer.music.set_volume(float(vol))

    tk.Button(reproductor_win, text="Cargar Música", command=cargar_musica).pack()
    listbox = tk.Listbox(reproductor_win)
    listbox.pack(expand=True, fill='both')
    tk.Button(reproductor_win, text="Reproducir", command=reproducir).pack()
    tk.Button(reproductor_win, text="Pausar", command=pausar).pack()
    tk.Button(reproductor_win, text="Reanudar", command=reanudar).pack()
    tk.Button(reproductor_win, text="Detener", command=detener).pack()

    tk.Label(reproductor_win, text="Volumen").pack()
    scale_volumen = tk.Scale(reproductor_win, from_=0, to=1, orient=tk.HORIZONTAL, resolution=0.1, command=ajustar_volumen)
    scale_volumen.set(0.5)
    scale_volumen.pack()

def abrir_ajustes():
    ajustes_win = tk.Toplevel(root)
    ajustes_win.title("Ajustes")

    def ajustar_volumen_sistema(vol):
        if pygame_available:
            pygame.mixer.music.set_volume(float(vol))

    def cambiar_fondo():
        archivo = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg")])
        if archivo:
            bg_image = tk.PhotoImage(file=archivo)
            pantalla.create_image(400, 300, image=bg_image)
            pantalla.image = bg_image

    tk.Label(ajustes_win, text="Volumen").pack()
    scale_volumen = tk.Scale(ajustes_win, from_=0, to=1, orient=tk.HORIZONTAL, resolution=0.1, command=ajustar_volumen_sistema)
    scale_volumen.set(0.5)
    scale_volumen.pack()

    # Simulación de selección de auriculares
    tk.Label(ajustes_win, text="Seleccionar Cascos").pack()
    combobox_cascos = ttk.Combobox(ajustes_win, values=["Auriculares 1", "Auriculares 2", "Auriculares 3"])
    combobox_cascos.pack()
    combobox_cascos.current(0)

    tk.Button(ajustes_win, text="Cambiar Fondo", command=cambiar_fondo).pack()

    # Información del autor y versión
    tk.Label(ajustes_win, text="Autor: ManuLogicSystems").pack()
    tk.Label(ajustes_win, text="Versión: alpha 1.01").pack()

# Ventana principal del "sistema operativo"
root = tk.Tk()
root.title("Mini Sistema Operativo")
root.geometry("800x600")

# Fondo de la "pantalla" con MLS
pantalla = tk.Canvas(root, bg="black")
pantalla.pack(expand=True, fill='both')
pantalla.create_text(400, 300, text="MLS", font=("Arial", 100), fill="white")

# Barra de tareas
barra_tareas = tk.Frame(root, bg="grey", height=30)
barra_tareas.pack(side=tk.BOTTOM, fill=tk.X)

# Reloj en la barra de tareas
def actualizar_reloj():
    now = datetime.now().strftime("%H:%M:%S %d/%m/%Y")
    reloj.config(text=now)
    root.after(1000, actualizar_reloj)

reloj = tk.Label(barra_tareas, text="", bg="grey", fg="white")
reloj.pack(side=tk.RIGHT)
actualizar_reloj()

# Botones de la barra de tareas
tk.Button(barra_tareas, text="Calculadora", command=abrir_calculadora).pack(side=tk.LEFT)
tk.Button(barra_tareas, text="Editor de texto", command=abrir_editor_texto).pack(side=tk.LEFT)
tk.Button(barra_tareas, text="Navegador de archivos", command=abrir_navegador_archivos).pack(side=tk.LEFT)
tk.Button(barra_tareas, text="Navegador web", command=abrir_navegador_web).pack(side=tk.LEFT)
tk.Button(barra_tareas, text="Reproductor de música", command=abrir_reproductor_musica).pack(side=tk.LEFT)
tk.Button(barra_tareas, text="Ajustes", command=abrir_ajustes).pack(side=tk.LEFT)

# Iniciar el bucle principal de la interfaz gráfica
root.mainloop()
