import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import pandas as pd
import requests
from io import BytesIO
from tkinter.font import Font



CSV_PATH = 'book_database/books_clean_short.csv'

# Paleta de colores
# Paleta de colores
COLORS = {
    'background': '#F8F9FA',
    'primary': '#2C3E50',
    'secondary': '#E9ECEF',
    'accent': '#3498DB',
    'text': '#212529',
    'success': '#28A745',
    'warning': '#FFC107',
    'danger': '#DC3545'
}

def show_admlog_window(parent):
# PARÁMETROS_______________________________________________________________
    adm_log_window = tk.Toplevel() if parent else tk.Tk()
    adm_log_window.title('Administrar Catálogo')
    adm_log_window.configure(bg=COLORS['background'])

    # Tamaño de la pantalla
    screen_width = adm_log_window.winfo_screenwidth()
    screen_height = adm_log_window.winfo_screenheight()

    # Definir el tamaño de la ventana
    window_width = 1100
    window_height = 650

    # Calcular la posición para centrar la ventana
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    # Establecer la geometría de la ventana
    adm_log_window.geometry(f'{window_width}x{window_height}+{x}+{y}')

    adm_log_window.iconbitmap('index/index_media/libre_isotype.ico')
    adm_log_window.configure(bg='#F8F9FA')

    # Cargar datos con manejo de errores
    try:
        df = pd.read_csv(CSV_PATH)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar el archivo CSV:\n{str(e)}")
        adm_log_window.destroy()
        return

    # Columnas a ocultar en la tabla (pero no eliminar del DataFrame)
    HIDDEN_COLUMNS = [
        'año_publicación', 'calificación_promedio', 'num_calificaciones',
        '1_estrella', '2_estrellas', '3_estrellas', '4_estrellas', '5_estrellas',
        'imagen', 'imagen_2'
    ]

    columns = list(df.columns)  # Todas las columnas
    visible_columns = [col for col in columns if col not in HIDDEN_COLUMNS]  # Solo las visibles

    # Configurar fuentes
    title_font = Font(family='Helvetica', size=12, weight='bold')
    label_font = Font(family='Helvetica', size=10)
    button_font = Font(family='Helvetica', size=10, weight='bold')

    # Configurar estilo para los botones
    style = ttk.Style()
    #style.theme_use('clam')  # Usar tema 'clam' para mejor visualización
    
    #style.configure('TButton', 
                #font=button_font,
                #padding=6)
    
    style.configure('CatalogAccent.TButton', 
                foreground='black', 
                background=COLORS['accent'],
                font=button_font)

    style.configure('CatalogSuccess.TButton', 
                foreground='black', 
                background=COLORS['success'],
                font=button_font)

    style.configure('CatalogDanger.TButton', 
                foreground='black', 
                background=COLORS['danger'],
                font=button_font)
    
    # Configurar efectos hover
    for style_name in ['CatalogAccent.TButton', 'CatalogSuccess.TButton', 'CatalogDanger.TButton']:
        style.map(style_name,
                foreground=[('pressed', 'white'), ('active', 'white')],
                background=[('pressed', '!disabled', COLORS['primary']), 
                        ('active', COLORS['primary'])])

    # Marco superior con título
    header_frame = tk.Frame(adm_log_window, bg=COLORS['primary'], height=60)
    header_frame.pack(fill=tk.X, padx=0, pady=0)
    
    title_label = tk.Label(header_frame, 
                        text="ADMINISTRAR CATÁLOGO DE LIBROS", 
                        fg='white', 
                        bg=COLORS['primary'],
                        font=title_font)
    title_label.pack(side=tk.LEFT, padx=20)

    # Marco de búsqueda
    search_frame = tk.Frame(adm_log_window, bg=COLORS['secondary'], padx=10, pady=10)
    search_frame.pack(fill=tk.X, padx=10, pady=10)

    tk.Label(search_frame, 
            text="Buscar:", 
            bg=COLORS['secondary'], 
            font=label_font).pack(side=tk.LEFT, padx=(0, 5))

    search_var = tk.StringVar()
    search_entry = tk.Entry(search_frame, 
                            textvariable=search_var, 
                            width=40,
                            font=label_font)
    search_entry.pack(side=tk.LEFT, padx=5)

    search_combo = ttk.Combobox(search_frame, 
                                values=list(df.columns), 
                                state='readonly',
                                font=label_font)
    search_combo.pack(side=tk.LEFT, padx=5)
    search_combo.set(list(df.columns)[0])  # Establecer primera columna por defecto

    def perform_search():
        query = search_var.get().lower()
        col = search_combo.get()
        
        if not query:
            # Si la búsqueda está vacía, mostrar todos los registros
            for child in tree.get_children():
                tree.delete(child)
            for _, row in df.iterrows():
                tree.insert('', tk.END, values=list(row))
            return
            
        # Filtrar el DataFrame
        filtered_df = df[df[col].astype(str).str.lower().str.contains(query)]
        
        # Limpiar el árbol
        for child in tree.get_children():
            tree.delete(child)
            
        # Insertar resultados filtrados
        for _, row in filtered_df.iterrows():
            tree.insert('', tk.END, values=list(row))

    search_button = ttk.Button(search_frame, 
                                text="Buscar", 
                                command=perform_search,
                                style='CatalogAccent.TButton')
    search_button.pack(side=tk.LEFT, padx=5)


    # Marco principal con tabla y controles
    main_frame = tk.Frame(adm_log_window, bg=COLORS['background'])
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

    # Tabla Treeview con barra de desplazamiento
    tree_frame = tk.Frame(main_frame, bg=COLORS['background'])
    tree_frame.pack(fill=tk.BOTH, expand=True)

    scroll_y = ttk.Scrollbar(tree_frame)
    scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

    scroll_x = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
    scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

    columns = list(df.columns)
    tree = ttk.Treeview(tree_frame, 
                    columns=visible_columns, 
                    show='headings',
                    yscrollcommand=scroll_y.set,
                    xscrollcommand=scroll_x.set,
                    selectmode='browse')

    scroll_y.config(command=tree.yview)
    

    # Configurar columnas visibles
    for col in visible_columns:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor=tk.W)
    tree.pack(fill=tk.BOTH, expand=True)

    # Llenar la tabla con solo los valores visibles
    for _, row in df.iterrows():
        tree.insert('', tk.END, values=[row[col] for col in visible_columns])

    # Marco de controles de edición
    control_frame = tk.Frame(main_frame, bg=COLORS['background'], pady=10)
    control_frame.pack(fill=tk.X)

    # Botones principales
    button_frame = tk.Frame(control_frame, bg=COLORS['background'])
    button_frame.pack(side=tk.LEFT, padx=(0, 20))

    ttk.Button(button_frame, 
            text="Limpiar", 
            command=lambda: add_new_book(),
            style='CatalogSuccess.TButton').grid(row=0, column=0, padx=5, pady=5, sticky='ew')

    ttk.Button(button_frame, 
            text="Cargar Selección", 
            command=lambda: load_selected(),
            style='CatalogAccent.TButton').grid(row=0, column=1, padx=5, pady=5, sticky='ew')

    ttk.Button(button_frame, 
            text="Actualizar", 
            command=lambda: update_selected(),
            style='CatalogAccent.TButton').grid(row=0, column=2, padx=5, pady=5, sticky='ew')

    ttk.Button(button_frame, 
            text="Eliminar", 
            command=lambda: delete_selected(),
            style='CatalogDanger.TButton').grid(row=0, column=3, padx=5, pady=5, sticky='ew')

    ttk.Button(button_frame, 
            text="Guardar Cambios", 
            command=lambda: save_to_csv(),
            style='CatalogSuccess.TButton').grid(row=0, column=4, padx=5, pady=5, sticky='ew')

    # Marco de campos de edición
    edit_frame = tk.Frame(control_frame, bg=COLORS['background'])
    edit_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

    entries = {}
    visible_idx = 0
    max_cols_per_row = 3
    row_idx = 0

    for col in columns:
        if col in HIDDEN_COLUMNS:
            continue

        col_position = visible_idx % max_cols_per_row
        row_position = row_idx + (visible_idx // max_cols_per_row) * 2

        tk.Label(edit_frame,
                text=col,
                bg=COLORS['background'],
                font=label_font).grid(row=row_position, column=col_position, padx=5, pady=2, sticky='w')

        entry = tk.Entry(edit_frame,
                        font=label_font,
                        relief=tk.SOLID,
                        borderwidth=1)
        entry.grid(row=row_position + 1, column=col_position, padx=5, pady=2, sticky='ew')

        entries[col] = entry
        visible_idx += 1


    # Barra de estado
    status_frame = tk.Frame(adm_log_window, bg=COLORS['secondary'], height=30)
    status_frame.pack(fill=tk.X, padx=0, pady=0)

    status_var = tk.StringVar()
    status_var.set("Listo")
    status_label = tk.Label(status_frame, 
                        textvariable=status_var, 
                        fg=COLORS['text'], 
                        bg=COLORS['secondary'],
                        font=label_font)
    status_label.pack(side=tk.LEFT, padx=10)



    # Funciones de la aplicación

    def clear_entries():
        for col in columns:
            entries[col].delete(0, tk.END)
        status_var.set("Campos listos para nuevo libro")



    def add_new_book():
        """Limpia solo los campos de texto del formulario"""
        for entry in entries.values():
            entry.delete(0, tk.END)
        status_var.set("Campos listos para nuevo libro")


    def load_selected():
        """Cargar los datos del libro seleccionado en los campos de edición"""
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Por favor seleccione un libro de la lista.")
            return

        selected_values = tree.item(selected[0])['values']
        visible_row_data = dict(zip(visible_columns, selected_values))

        # Obtener la fila completa desde el DataFrame (incluyendo columnas ocultas)
        book_id = visible_row_data['id']
        row_data = df[df['id'].astype(str) == str(book_id)].iloc[0]

        for col in entries:
            entries[col].delete(0, tk.END)
            entries[col].insert(0, str(row_data[col]))

        status_var.set(f"Libro ID {book_id} cargado para edición")


    def update_selected():
        """Actualizar el libro seleccionado con los datos de los campos"""
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Por favor seleccione un libro para actualizar.")
            return

        if not entries['id'].get():
            messagebox.showerror("Error", "El campo ID es obligatorio")
            return

        book_id = tree.item(selected[0])['values'][visible_columns.index('id')]

        # Actualizar solo columnas editables
        for col in entries:
            df.loc[df['id'].astype(str) == str(book_id), col] = entries[col].get()

        # Actualizar fila visible en el Treeview
        matching_rows = df[df['id'].astype(str) == str(book_id)]
        if matching_rows.empty:
            messagebox.showerror("Error", f"No se encontró el libro con ID {book_id} en el archivo.")
            return
        updated_row = matching_rows.iloc[0]

        visible_values = [updated_row[col] for col in visible_columns]
        tree.item(selected[0], values=visible_values)

        status_var.set(f"Libro ID {book_id} actualizado (recuerde guardar cambios)")


    def delete_selected():
        """Eliminar el libro seleccionado"""
        nonlocal df  # <- importante: df está definido en la función externa
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Por favor seleccione un libro para eliminar.")
            return
    
        book_id = tree.item(selected[0])['values'][visible_columns.index('id')]
        if messagebox.askyesno("Confirmar", f"¿Está seguro que desea eliminar el libro ID {book_id}?"):
            # Eliminar del Treeview
            tree.delete(selected[0])
            # Eliminar del DataFrame
            df = df[df['id'].astype(str) != str(book_id)]
            clear_entries()
            status_var.set(f"Libro ID {book_id} eliminado (recuerde guardar cambios)")
            save_to_csv()


    def save_to_csv():
        try:
            # Cargar el archivo original para tener la estructura completa
            original_df = pd.read_csv(CSV_PATH)

            # Obtener solo las filas actuales del Treeview
            data = []
            for child in tree.get_children():
                row = tree.item(child)['values']
                row_dict = dict(zip(visible_columns, row))

                # Recuperar los datos faltantes desde original_df usando el ID
                original_row = original_df[original_df['id'] == row_dict['id']].iloc[0].to_dict()

                # Actualizar los datos visibles con los del treeview
                for col in visible_columns:
                    original_row[col] = row_dict[col]

                # Asegurar orden correcto
                ordered_row = [original_row[col] for col in original_df.columns]
                data.append(ordered_row)

            # Crear DataFrame con todas las columnas originales
            new_df = pd.DataFrame(data, columns=original_df.columns)

            # Verificar que todos los libros tengan un ID
            if new_df['id'].isnull().any() or (new_df['id'] == '').any():
                messagebox.showerror("Error", "Todos los libros deben tener un id válido")
                return

            # Guardar al CSV
            new_df.to_csv(CSV_PATH, index=False)
            messagebox.showinfo("Guardado", "Los cambios se han guardado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar en el archivo: {e}")


    # Configurar eventos
    search_entry.bind('<Return>', lambda e: perform_search())
    tree.bind('<Double-1>', lambda e: load_selected())

    if not parent:
        adm_log_window.mainloop()

if __name__ == "__main__":
    print("Aplicación iniciada correctamente")
    show_admlog_window()
