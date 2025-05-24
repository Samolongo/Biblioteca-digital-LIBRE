import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import pandas as pd
import requests
from io import BytesIO
from datetime import datetime, timedelta



# Base de datos de libros
libros_df = pd.read_csv(
    'book_database/books_clean_short.csv',
    encoding='utf-8'
)

# Lista para almacenar préstamos temporales
lista_prestamos = []


def show_adloan_window(parent):
# PARÁMETROS_______________________________________________________________
    r_pres_window = tk.Toplevel(parent)
    r_pres_window.title('Libre.')

    # Tamaño de la pantalla
    screen_width = r_pres_window.winfo_screenwidth()
    screen_height = r_pres_window.winfo_screenheight()

    # Definir el tamaño de la ventana
    window_width = 512
    window_height = 434

    # Calcular la posición para centrar la ventana
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    # Establecer la geometría de la ventana
    r_pres_window.geometry(f'{window_width}x{window_height}+{x}+{y}')

    r_pres_window.iconbitmap('index/index_media/libre_isotype.ico')
    r_pres_window.configure(bg='#F8F9FA')



    # UI ELEMENTOS_____________________________________________________________
    # Etiqueta Ingresar el código del libro
    label_book_code = tk.Label(r_pres_window, text='Ingresa el Código del Material', bg='#F8F9FA', fg='#000000')
    label_book_code.config(font=('Questrial', 12, 'bold'))
    label_book_code.place(relx=0.5, rely=0.1, anchor='center')

    global entry_search_id
    entry_search_id = tk.Entry(r_pres_window, bg='#FFFFFF', fg='#7E7E7E', font=('DM Sans', 10))
    entry_search_id.place(relx=0.42, rely=0.18, anchor='center', width=150)

    style_ad = ttk.Style()
    style_ad.configure('Custom.TButton', background='#FFFFFF', foreground='#000000', font=('DM Sans', 8))
    boton_ad = ttk.Button(r_pres_window, text='Agregar', command=agregar_libro)
    boton_ad.place(relx=0.66, rely=0.1755, anchor='center')

    # Botón para realizar el préstamo
    style_ad_loan = ttk.Style()
    style_ad_loan.configure('Custom.TButton', background='#FFFFFF', foreground='#000000', font=('DM Sans', 8))
    boton_ad_loan = ttk.Button(r_pres_window, text='Realizar Préstamo', command=realizar_prestamo)
    boton_ad_loan.place(relx=0.5, rely=0.85, anchor='center')

    label_loan_discl = tk.Label(r_pres_window, 
                            text='El préstamo es por 14 días.\n'
                            'Tras ese plazo, el material se eliminará automáticamente.\n'
                            'Puedes volver a solicitarlo si está disponible.\n',
                            bg='#F8F9FA',
                            fg='#000000')
    label_loan_discl.config(font=('DM Sans', 7))
    label_loan_discl.place(relx=0.5, rely=0.75, anchor='center')

    # CREAR VENTANA DESLIZABLE______________________________________________

    # Crear ventana deslizable dentro de la ventana principal
    scrollable_frame = tk.Frame(r_pres_window, bg='#F8F9FA')
    scrollable_frame.place(relx=0.5, rely=0.45, relwidth=0.8, relheight=0.4, anchor='center')

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

    # Vincular el evento de desplazamiento del mouse al canvas
    canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", on_mouse_wheel))
    canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))



# Función para agregar libro por ID
def agregar_libro():
    codigo = entry_search_id.get().strip()
    if codigo == "":
        messagebox.showwarning("Código vacío", "Por favor, ingresa un código de libro.")
        return

    libro = libros_df[libros_df['id'].astype(str) == codigo]
    if libro.empty:
        messagebox.showerror("No encontrado", f"No se encontró ningún libro con el código {codigo}.")
        return

    titulo = libro.iloc[0]['título']
    autor = libro.iloc[0]['autor']

    lista_prestamos.append({
        'id': codigo,
        'título': titulo,
        'autor': autor,
        'fecha_prestamo': datetime.now().strftime("%Y-%m-%d"),
        'fecha_devolucion': (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
    })

    # Mostrar en interfaz
    tk.Label(content_frame, text=f"{codigo} - {titulo}", bg='#F8F9FA', font=('DM Sans', 10)).pack(anchor='w', pady=2)
    entry_search_id.delete(0, tk.END)

# Función para guardar préstamos
def realizar_prestamo():
    if not lista_prestamos:
        messagebox.showinfo("Sin libros", "Agrega al menos un libro para realizar el préstamo.")
        return

    try:
        prestamos_df = pd.DataFrame(lista_prestamos)
        archivo = 'prestamos.csv'

        try:
            df_existente = pd.read_csv(archivo)
            prestamos_df = pd.concat([df_existente, prestamos_df], ignore_index=True)
        except FileNotFoundError:
            pass  # Se creará un nuevo archivo

        prestamos_df.to_csv(archivo, index=False, encoding='utf-8')
        messagebox.showinfo("Éxito", "Préstamo guardado correctamente.")
        lista_prestamos.clear()
        for widget in content_frame.winfo_children():
            widget.destroy()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar el préstamo: {e}")