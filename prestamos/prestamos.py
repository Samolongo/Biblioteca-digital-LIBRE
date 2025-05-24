import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pandas as pd
import requests
from io import BytesIO
from datetime import datetime


# --- Cargar datos del CSV ---


def show_loan_window(parent):

    df_prestamos = pd.read_csv('prestamos.csv')
    df_libros = pd.read_csv('book_database/books_clean_short.csv')

# PARÁMETROS_______________________________________________________________
    loans_window = tk.Toplevel(parent)
    loans_window.title('Libre.')

    # Tamaño de la pantalla
    screen_width = loans_window.winfo_screenwidth()
    screen_height = loans_window.winfo_screenheight()

    # Definir el tamaño de la ventana
    window_width = 800
    window_height = 500

    # Calcular la posición para centrar la ventana
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    # Establecer la geometría de la ventana
    loans_window.geometry(f'{window_width}x{window_height}+{x}+{y}')

    loans_window.iconbitmap('index/index_media/libre_isotype.ico')
    loans_window.configure(bg='#F8F9FA')

    # UI ELEMENTOS_____________________________________________________________

    # Barra superior
    topbar = tk.Frame(loans_window, bg='#FFFFFF')
    topbar.place(relx=0, rely=0, relwidth=1, relheight=0.08)

    label_loans = tk.Label(topbar, text='Préstamos', bg='#FFFFFF', fg='#000000')
    label_loans.config(font=('Questrial', 10, 'bold'))
    label_loans.place(relx=0.1, rely=0.5, anchor='e')


    # CREAR VENTANA DESLIZABLE______________________________________________

    # Crear ventana deslizable dentro de la ventana principal
    scrollable_frame = tk.Frame(loans_window, bg='#F8F9FA')
    scrollable_frame.place(relx=1, rely=0.08, relwidth=1, relheight=0.9, anchor='ne')

    # Crear un canvas dentro de la ventana deslizable
    canvas = tk.Canvas(scrollable_frame, bg='#F8F9FA')
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Añadir una barra deslizante a la ventana
    scrollbar = tk.Scrollbar(scrollable_frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Configurar el canvas para que use la barra deslizante
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # Crear un marco dentro del canvas
    content_frame = tk.Frame(canvas, bg='#F8F9FA')
    canvas.create_window((0, 0), window=content_frame, anchor="nw")

    # Función para actualizar la región de desplazamiento
    def on_mouse_wheel(event):
        canvas.yview_scroll(-1 * (event.delta // 120), "units")  # Adjust scrolling speed

    canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", on_mouse_wheel))
    canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

    # Crear y mostrar cada préstamo en un frame individual
    for index, row in df_prestamos.iterrows():
        frame = tk.Frame(content_frame, bg='#FFFFFF', bd=0, relief='solid')
        frame.pack(fill='x', padx=10, pady=5, expand=True)

        # Buscar información del libro
        libro_info = df_libros[df_libros['id'] == row['id']]
        if libro_info.empty:
            continue
        libro = libro_info.iloc[0]

        # Cargar imagen
        try:
            response = requests.get(libro['imagen_2'])
            img_data = Image.open(BytesIO(response.content)).resize((80, 110), Image.LANCZOS)
            foto = ImageTk.PhotoImage(img_data)
            img_label = tk.Label(frame, image=foto, bg='#FFFFFF')
            img_label.image = foto
            img_label.pack(side=tk.LEFT, padx=10, pady=10)
        except:
            pass  # Si falla la imagen, continúa

        # Crear frame de texto
        texto_frame = tk.Frame(frame, bg='#FFFFFF', relief='solid')
        texto_frame.pack(side=tk.LEFT, fill='both', expand=True)

        # Título
        titulo = tk.Label(texto_frame, text=row['título'], bg='#FFFFFF', fg='#000000', font=('Questrial', 11, 'bold'))
        titulo.pack(anchor='w', pady=(8, 0))

        # Autor
        autor = tk.Label(texto_frame, text=f"Autor: {row['autor']}", bg='#FFFFFF', fg='#333333', font=('DM Sans', 9))
        autor.pack(anchor='w', pady=2)

        # Fechas
        fechas = f"Fecha de préstamo: {row['fecha_prestamo']}  |  Fecha de devolución: {row['fecha_devolucion']}"
        fechas_lbl = tk.Label(texto_frame, text=fechas, bg='#FFFFFF', fg='#666666', font=('DM Sans', 8))
        fechas_lbl.pack(anchor='w', pady=(0, 4))

        # Cálculo del estado del préstamo
        try:
            fecha_dev = datetime.strptime(row['fecha_devolucion'], '%Y-%m-%d')
            hoy = datetime.today()
            dias_restantes = (fecha_dev - hoy).days
            if dias_restantes >= 0:
                estado = f"Estado: Vigente ({dias_restantes} días restantes)"
                color_estado = '#28A745'  # verde
            else:
                estado = f"Estado: Vencido ({-dias_restantes} días de retraso)"
                color_estado = '#DC3545'  # rojo
            estado_lbl = tk.Label(texto_frame, text=estado, bg='#FFFFFF', fg=color_estado, font=('DM Sans', 9, 'italic'))
            estado_lbl.pack(anchor='w', pady=(0, 10))
        except:
            pass