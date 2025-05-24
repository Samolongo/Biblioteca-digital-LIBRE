import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import pandas as pd
import requests
from io import BytesIO
import os


def show_admloan_window(parent):
# PARÁMETROS_______________________________________________________________
    adm_loan_window = tk.Toplevel(parent)
    adm_loan_window.title('Libre.')

    # Tamaño de la pantalla
    screen_width = adm_loan_window.winfo_screenwidth()
    screen_height = adm_loan_window.winfo_screenheight()

    # Definir el tamaño de la ventana
    window_width = 800
    window_height = 500

    # Calcular la posición para centrar la ventana
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    # Establecer la geometría de la ventana
    adm_loan_window.geometry(f'{window_width}x{window_height}+{x}+{y}')

    adm_loan_window.iconbitmap('index/index_media/libre_isotype.ico')
    adm_loan_window.configure(bg='#F8F9FA')

    # UI ELEMENTOS_____________________________________________________________

    # Barra superior
    topbar = tk.Frame(adm_loan_window, bg='#FFFFFF')
    topbar.place(relx=0, rely=0, relwidth=1, relheight=0.08)

    label_adm_loan = tk.Label(topbar, text='Administrar Préstamos', bg='#FFFFFF', fg='#000000')
    label_adm_loan.config(font=('Questrial', 10, 'bold'))
    label_adm_loan.place(relx=0.2, rely=0.5, anchor='e')


    # CREAR VENTANA DESLIZABLE______________________________________________

    # Crear ventana deslizable dentro de la ventana principal
    scrollable_frame = tk.Frame(adm_loan_window, bg='#F8F9FA')
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
    global content_frame
    content_frame = tk.Frame(canvas, bg='#F8F9FA')
    canvas.create_window((0, 0), window=content_frame, anchor="nw")

    # Función para actualizar la región de desplazamiento
    def on_mouse_wheel(event):
        canvas.yview_scroll(-1 * (event.delta // 120), "units")  # Adjust scrolling speed

    canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", on_mouse_wheel))
    canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

    cargar_prestamos()


# FUNCIONES_______________________________________________________________

# Rutas de archivos
csv_path = 'prestamos.csv'
libros_path = 'book_database/books_clean_short.csv'

# Cargar libros solo una vez
df_libros = pd.read_csv(libros_path)

# Lista para mantener referencias a imágenes
imagenes_cache = []

# Función para cargar y mostrar los préstamos
def cargar_prestamos():
    for widget in content_frame.winfo_children():
        widget.destroy()

    if not os.path.exists(csv_path):
        return

    try:
        df = pd.read_csv(csv_path)

        for index, row in df.iterrows():
            frame_prestamo = tk.Frame(content_frame, bg='#FFFFFF', bd=1, relief='solid')
            frame_prestamo.pack(fill='x', padx=10, pady=5)

            # Buscar la imagen correspondiente en df_libros
            libro_info = df_libros[df_libros['id'] == row['id']]
            if not libro_info.empty:
                imagen_url = libro_info.iloc[0]['imagen_2']
                try:
                    response = requests.get(imagen_url)
                    img_data = Image.open(BytesIO(response.content)).resize((80, 110), Image.LANCZOS)
                    foto = ImageTk.PhotoImage(img_data)
                    imagenes_cache.append(foto)  # Evita que la imagen sea eliminada por el recolector de basura

                    lbl_imagen = tk.Label(frame_prestamo, image=foto, bg='#FFFFFF')
                    lbl_imagen.pack(side='left', padx=10, pady=10)
                except:
                    pass  # Si falla la imagen, continúa

            info_text = f"Título: {row['título']}\nAutor: {row['autor']}\n" \
                        f"Fecha Préstamo: {row['fecha_prestamo']}\nFecha Devolución: {row['fecha_devolucion']}"

            lbl_info = tk.Label(frame_prestamo, text=info_text, justify='left', bg='#FFFFFF', font=('DM Sans', 9))
            lbl_info.pack(side='left', padx=10, pady=5)

            btn_eliminar = tk.Button(frame_prestamo, text="Eliminar", bg="#E74C3C", fg="white", font=('DM Sans', 9, 'bold'),
                                    command=lambda i=index: eliminar_prestamo(i))
            btn_eliminar.pack(side='right', padx=10, pady=10)

    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron cargar los préstamos: {e}")

# Función para eliminar un préstamo por índice
def eliminar_prestamo(index):
    try:
        df = pd.read_csv(csv_path)
        df = df.drop(index)
        df.to_csv(csv_path, index=False)
        cargar_prestamos()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo eliminar el préstamo: {e}")