import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unicodedata
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pandas as pd
import requests
from io import BytesIO


import usuarios.usuarios
import realizar_prestamo.realizar_prestamo
import prestamos.prestamos
import administrar_prestamos.administrar_prestamos
import administrar_catalogo.administrar_catalogo
import datos.datos

image_cache = {}
def get_book_cover(image_url):
    if image_url in image_cache:
        return image_cache[image_url]
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        image_data = Image.open(BytesIO(response.content)).resize((70, 118))
        book_cover = ImageTk.PhotoImage(image_data)
    except Exception:
        book_cover = ImageTk.PhotoImage(Image.open('main/main_media/libre_logotype_img.png').resize((70, 118)))
    image_cache[image_url] = book_cover
    return book_cover

def normalize(s):
    if not isinstance(s, str):
        s = str(s)
    return unicodedata.normalize('NFKD', s).encode('ASCII', 'ignore').decode('ASCII').strip().lower()




def show_main_window():
    # PARÁMETROS_______________________________________________________________
    main_window = tk.Tk()
    main_window.title('Libre.')

    # Tamaño de la pantalla
    screen_width = main_window.winfo_screenwidth()
    screen_height = main_window.winfo_screenheight()

    # Definir el tamaño de la ventana
    window_width = 1024
    window_height = 668

    # Calcular la posición para centrar la ventana
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    # Establecer la geometría de la ventana
    main_window.geometry(f'{window_width}x{window_height}+{x}+{y}')

    main_window.iconbitmap('index/index_media/libre_isotype.ico')
    main_window.configure(bg='#F8F9FA')



    # UI ELEMENTOS_____________________________________________________________
    def filter_books(event=None):
        title = normalize(entry_search_title.get())
        autor = normalize(entry_search_autor.get())
        gender = normalize(entry_search_gender.get())

        filtered = database[
            database['título'].fillna('').apply(normalize).str.contains(title)
            & database['autor'].fillna('').apply(normalize).str.contains(autor)
            & database['género'].fillna('').apply(normalize).str.contains(gender)
        ]
        display_books(filtered)
    # Barra lateral
    sidebar = tk.Frame(main_window, bg='#FFFFFF')
    sidebar.place(relx=0, rely=0, relwidth=0.25, relheight=1)

    # Barra superior
    topbar = tk.Frame(main_window, bg='#FFFFFF')
    topbar.place(relx=0, rely=0, relwidth=1, relheight=0.1)

    # Logo
    logotype = Image.open('main/main_media/libre_imagotype_img.png')
    logotype = logotype.resize((110,110))
    logotype = ImageTk.PhotoImage(logotype)
    label_logotype = tk.Label(main_window, image=logotype, bg='#FFFFFF')
    label_logotype.place(relx=0.015, rely=0, anchor='nw')

    # Etiqueta Buscar por titulo
    label_search_title = tk.Label(topbar, text='Título', bg='#FFFFFF', fg='#7E7E7E')
    label_search_title.config(font=('DM Sans', 8))
    label_search_title.place(relx=0.147, rely=0.3, anchor='w')
    # Caja de texto para buscar por titulo
    entry_search_title = tk.Entry(topbar, bg='#FFFFFF', fg='#7E7E7E', font=('DM Sans', 10))
    entry_search_title.place(relx=0.15, rely=0.55, anchor='w', width=150)
    entry_search_title.bind('<KeyRelease>', filter_books)

    # Etiqueta Buscar por autor
    label_search_autor = tk.Label(topbar, text='Autor', bg='#FFFFFF', fg='#7E7E7E')
    label_search_autor.config(font=('DM Sans', 8))
    label_search_autor.place(relx=0.347, rely=0.3, anchor='w')
    # Caja de texto para buscar por autor
    entry_search_autor = tk.Entry(topbar, bg='#FFFFFF', fg='#7E7E7E', font=('DM Sans', 10))
    entry_search_autor.place(relx=0.35, rely=0.55, anchor='w', width=150)
    entry_search_autor.bind('<KeyRelease>', filter_books)

    # Etiqueta Buscar por genero
    label_search_gender = tk.Label(topbar, text='Género', bg='#FFFFFF', fg='#7E7E7E')
    label_search_gender.config(font=('DM Sans', 8))
    label_search_gender.place(relx=0.547, rely=0.3, anchor='w')
    # Caja de texto para buscar por genero
    entry_search_gender = tk.Entry(topbar, bg='#FFFFFF', fg='#7E7E7E', font=('DM Sans', 10))
    entry_search_gender.place(relx=0.55, rely=0.55, anchor='w', width=150)
    entry_search_gender.bind('<KeyRelease>', filter_books)

    # Botón para realizar préstamo
    style_ad_loan = ttk.Style()
    style_ad_loan.configure('Custom.TButton', background='#FFFFFF', foreground='#000000', font=('DM Sans', 8))
    boton_ad_loan = ttk.Button(topbar, text='Realizar Préstamo', command=lambda: realizar_prestamo.realizar_prestamo.show_adloan_window(main_window))
    boton_ad_loan.place(relx=.95, rely=0.5, anchor='e')

    # Botón para administrar catálogo
    style_adm_log = ttk.Style()
    style_adm_log.configure('Custom.TButton', background='#FFFFFF', foreground='#FFFFFF', font=('DM Sans', 8))
    boton_adm_log = ttk.Button(sidebar, text='Administrar Catálogo', command=lambda: administrar_catalogo.administrar_catalogo.show_admlog_window(main_window))
    boton_adm_log.place(relx=0.02, rely=0.90, anchor='w')

    # Botón para préstamos
    style_loans = ttk.Style()
    style_loans.configure('Custom.TButton', background='#FFFFFF', foreground='#000000', font=('DM Sans', 8))
    boton_loans = ttk.Button(topbar, text='Préstamos', command=lambda: prestamos.prestamos.show_loan_window(main_window))
    boton_loans.place(relx=0.84, rely=0.5, anchor='e')

    # Botón para usuarios
    style_users = ttk.Style()
    style_users.configure('Custom.TButton', background='#FFFFFF', foreground='#000000', font=('DM Sans', 8))
    boton_users = ttk.Button(sidebar, text='Usuarios', command=lambda: usuarios.usuarios.show_users_window(main_window))
    boton_users.place(relx=0.02, rely=0.85, anchor='w')

    # Botón para datos
    style_data = ttk.Style()
    style_data.configure('Custom.TButton', background='#FFFFFF', foreground='#000000', font=('DM Sans', 8))
    boton_data = ttk.Button(sidebar, text='Datos', command=lambda: datos.datos.abrir_dashboard(main_window))
    boton_data.place(relx=0.02, rely=0.80, anchor='w')

    # Botón para administrar préstamos
    style_adm_loan = ttk.Style()
    style_adm_loan.configure('Custom.TButton', background='#FFFFFF', foreground='#000000', font=('DM Sans', 8))
    boton_adm_loan = ttk.Button(sidebar, text='Administrar Préstamos', command=lambda: administrar_prestamos.administrar_prestamos.show_admloan_window(main_window))
    boton_adm_loan.place(relx=0.02, rely=0.95, anchor='w')

    # CREAR VENTANA DESLIZABLE______________________________________________

    # Crear ventana deslizable dentro de la ventana principal
    scrollable_frame = tk.Frame(main_window, bg='#F8F9FA')
    scrollable_frame.place(relx=0.15, rely=0.1, relwidth=0.85, relheight=0.9)

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

    # Vincular el evento de desplazamiento del mouse al canvas
    #canvas.bind_all("<MouseWheel>", on_mouse_wheel)
    canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", on_mouse_wheel))
    canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

    # LISTA DE LIBROS__________________________________________________________________

    # Cargar la base de datos de libros
    database = pd.read_csv('book_database/books_clean_short.csv', sep=',', encoding='utf-8')
    database['título'] = database['título'].astype(str).str.strip()
    database['autor'] = database['autor'].astype(str).str.strip()
    database['género'] = database['género'].astype(str).str.strip()

    # Permitir que la barra de desplazamiento se ajuste al contenido
    def update_scroll_region():
        canvas.update_idletasks()  # Update the canvas to reflect changes
        canvas.configure(scrollregion=canvas.bbox("all"))  # Set the scrollable region


    def display_books(df):
        for widget in content_frame.winfo_children():
            widget.destroy()
    # Etiquetas de contenido para cada libro
        for i in range(len(df)):
            new_frame = tk.Frame(content_frame, bg='#F2F3F4', relief='solid', height=150, width=2000)
            new_frame.pack(pady=5, padx=10, fill='x', expand=True)

            image_url = df.iloc[i]['imagen']
            book_cover = get_book_cover(image_url)  # Get the book cover image

            label_book_cover = tk.Label(new_frame, image=book_cover, bg='#F2F3F4')
            label_book_cover.image = book_cover  # Keep a reference to avoid garbage collection
            label_book_cover.place(relx=0.01, rely=0.5, anchor='w')

            book_title = df.iloc[i]['título']
            label_book_title = tk.Label(new_frame, text=book_title, bg='#F2F3F4', fg='#000000')
            label_book_title.config(font=('Questrial', 10, 'bold'))
            label_book_title.place(relx=0.06, rely=0.5, anchor='w')

            book_autor = df.iloc[i]['autor']
            label_book_autor = tk.Label(new_frame, text=book_autor, bg='#F2F3F4', fg='#000000')
            label_book_autor.config(font=('DM Sans', 8))
            label_book_autor.place(relx=0.06, rely=0.62, anchor='w')

            book_gender = df.iloc[i]['género']
            label_book_gender = tk.Label(new_frame, text=book_gender, bg='#F2F3F4', fg='#7E7E7E')
            label_book_gender.config(font=('DM Sans', 7))
            label_book_gender.place(relx=0.06, rely=0.75, anchor='w')

            book_year = df.iloc[i]['año_publicación']
            label_book_year = tk.Label(new_frame, text=book_year, bg='#F2F3F4', fg='#7E7E7E')
            label_book_year.config(font=('DM Sans', 7))
            label_book_year.place(relx=0.08, rely=0.75, anchor='w')

            book_id = df.iloc[i]['id']
            label_book_id = tk.Label(new_frame, text=book_id, bg='#F2F3F4', fg='#7E7E7E')
            label_book_id.config(font=('DM Sans', 15, 'bold'))
            label_book_id.place(relx=0.4, rely=0.5, anchor='w')

            if df.iloc[i]['copias'] < 1:
                label_soldout = tk.Label(new_frame, text='Agotado', bg='#F2F3F4', fg='red')
                label_soldout.config(font=('DM Sans', 10))
                label_soldout.place(relx=0.35, rely=0.51, anchor='w')
            
        # Display the star rating
            try:
                book_stars = int(round(df.iloc[i]['calificación_promedio']))  # Round to nearest integer
                star_image_path = f'main/main_media/stars/{book_stars}_star.png'  # Path to star image
                star_image = Image.open(star_image_path).resize((100, 20))  # Resize as needed
                star_image = ImageTk.PhotoImage(star_image)
            except Exception as e:
                print(f"Error {df.iloc[i]['título']}: {e}")
                star_image = None

            if star_image:
                label_star_rating = tk.Label(new_frame, image=star_image, bg='#F2F3F4')
                label_star_rating.image = star_image  # Keep a reference to avoid garbage collection
                label_star_rating.place(relx=0.25, rely=0.5, anchor='w')
            pass
        update_scroll_region()

    display_books(database)

    main_window.mainloop()