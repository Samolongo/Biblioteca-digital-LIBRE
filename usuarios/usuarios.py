import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import pandas as pd
import requests
from io import BytesIO


# Archivo CSV de usuarios
csv_path = 'index/usuarios.csv'

# Cargar usuarios (si existe)
if os.path.exists(csv_path):
    df_usuarios = pd.read_csv(csv_path)
else:
    df_usuarios = pd.DataFrame(columns=['usuario', 'contraseña', 'nombre', 'apellido'])


def cargar_tabla():
    for row in tree.get_children():
        tree.delete(row)
    for _, row in df_usuarios.iterrows():
        tree.insert("", "end", values=(row['usuario'], row['contraseña'], row['nombre'], row['apellido']))


def seleccionar_usuario(event):
    selected = tree.focus()
    if not selected:
        return
    values = tree.item(selected, 'values')
    entry_usuario.delete(0, tk.END)
    entry_usuario.insert(0, values[0])
    entry_contraseña.delete(0, tk.END)
    entry_contraseña.insert(0, values[1])
    entry_nombre.delete(0, tk.END)
    entry_nombre.insert(0, values[2])
    entry_apellido.delete(0, tk.END)
    entry_apellido.insert(0, values[3])


def guardar_cambios():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Advertencia", "Selecciona un usuario para editar.", parent=users_window)
        return

    idx = tree.index(selected)
    df_usuarios.at[idx, 'usuario'] = entry_usuario.get()
    df_usuarios.at[idx, 'contraseña'] = entry_contraseña.get()
    df_usuarios.at[idx, 'nombre'] = entry_nombre.get()
    df_usuarios.at[idx, 'apellido'] = entry_apellido.get()

    df_usuarios.to_csv(csv_path, index=False)
    cargar_tabla()
    messagebox.showinfo("Éxito", "Datos actualizados correctamente.", parent=users_window)


def eliminar_usuario():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Advertencia", "Selecciona un usuario para eliminar.", parent=users_window)
        return

    idx = tree.index(selected)
    confirm = messagebox.askyesno("Confirmar", "¿Seguro que deseas eliminar este usuario?", parent=users_window)
    if confirm:
        global df_usuarios
        df_usuarios = df_usuarios.drop(df_usuarios.index[idx]).reset_index(drop=True)
        df_usuarios.to_csv(csv_path, index=False)
        cargar_tabla()
        limpiar_campos()


def limpiar_campos():
    entry_usuario.delete(0, tk.END)
    entry_contraseña.delete(0, tk.END)
    entry_nombre.delete(0, tk.END)
    entry_apellido.delete(0, tk.END)


def show_users_window(parent):
    global entry_usuario, entry_contraseña, entry_nombre, entry_apellido
# PARÁMETROS_______________________________________________________________
    global users_window
    users_window = tk.Toplevel(parent)
    users_window.title('Libre.')

    # Tamaño de la pantalla
    screen_width = users_window.winfo_screenwidth()
    screen_height = users_window.winfo_screenheight()

    # Definir el tamaño de la ventana
    window_width = 800
    window_height = 500

    # Calcular la posición para centrar la ventana
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    # Establecer la geometría de la ventana
    users_window.geometry(f'{window_width}x{window_height}+{x}+{y}')

    users_window.iconbitmap('index/index_media/libre_isotype.ico')
    users_window.configure(bg='#F8F9FA')



    # UI ELEMENTOS_____________________________________________________________

    # Barra superior
    topbar = tk.Frame(users_window, bg='#FFFFFF')
    topbar.place(relx=0, rely=0, relwidth=1, relheight=0.08)

    label_users = tk.Label(topbar, text='Usuarios', bg='#FFFFFF', fg='#000000')
    label_users.config(font=('Questrial', 10, 'bold'))
    label_users.place(relx=0.05, rely=0.5, anchor='w')




# --- Tabla usuarios ---
    columns = ['usuario', 'contraseña', 'nombre', 'apellido']
    style = ttk.Style()
    style.configure("Treeview.Heading", font=('Questrial', 10, 'bold'))
    global tree
    tree = ttk.Treeview(users_window, columns=columns, show='headings', selectmode='browse')
    for col in columns:
        tree.heading(col, text=col.capitalize())
        tree.column(col, width=180, anchor='center')

    tree.pack(fill='x', padx=20, pady=(55,10))
    tree.bind('<<TreeviewSelect>>', seleccionar_usuario)

    # --- Formulario para editar ---
    form_frame = tk.Frame(users_window, bg='#F8F9FA')
    form_frame.pack(fill='x', padx=20, pady=10)

    tk.Label(form_frame, text="Usuario:", bg='#F8F9FA').grid(row=0, column=0, sticky='w', padx=5, pady=5)
    entry_usuario = tk.Entry(form_frame)
    entry_usuario.grid(row=0, column=1, sticky='ew', padx=5, pady=5)

    tk.Label(form_frame, text="Contraseña:", bg='#F8F9FA').grid(row=1, column=0, sticky='w', padx=5, pady=5)
    entry_contraseña = tk.Entry(form_frame)
    entry_contraseña.grid(row=1, column=1, sticky='ew', padx=5, pady=5)

    tk.Label(form_frame, text="Nombre:", bg='#F8F9FA').grid(row=2, column=0, sticky='w', padx=5, pady=5)
    entry_nombre = tk.Entry(form_frame)
    entry_nombre.grid(row=2, column=1, sticky='ew', padx=5, pady=5)

    tk.Label(form_frame, text="Apellido:", bg='#F8F9FA').grid(row=3, column=0, sticky='w', padx=5, pady=5)
    entry_apellido = tk.Entry(form_frame)
    entry_apellido.grid(row=3, column=1, sticky='ew', padx=5, pady=5)

    form_frame.columnconfigure(1, weight=1)

    # --- Botones ---
    btn_frame = tk.Frame(users_window, bg='#F8F9FA')
    btn_frame.pack(fill='x', padx=20, pady=10)

    btn_guardar = tk.Button(btn_frame, text="Guardar Cambios", bg="#3498DB", fg="white", font=('DM Sans', 10, 'bold'),
                            command=guardar_cambios)
    btn_guardar.pack(side='left', padx=20, pady=5)

    btn_eliminar = tk.Button(btn_frame, text="Eliminar Usuario", bg="#E74C3C", fg="white", font=('DM Sans', 10, 'bold'),
                            command=eliminar_usuario)
    btn_eliminar.pack(side='right', padx=20, pady=5)


    # Cargar tabla al iniciar
    cargar_tabla()

