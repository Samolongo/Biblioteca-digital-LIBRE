import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import main.main

# PARÁMETROS_______________________________________________________________
start_screen = tk.Tk()
start_screen.title('Login')

# Tamaño de la pantalla
screen_width = start_screen.winfo_screenwidth()
screen_height = start_screen.winfo_screenheight()

# Definir el tamaño de la ventana
window_width = 300
window_height = 350

# Calcular la posición para centrar la ventana
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

# Establecer la geometría de la ventana
start_screen.geometry(f'{window_width}x{window_height}+{x}+{y}')

start_screen.iconbitmap('index/index_media/libre_isotype.ico')
start_screen.configure(bg='#F8F9FA')



# UI ELEMENTOS_____________________________________________________________
# Logo
imagotype = Image.open('index/index_media/libre_imagotype_img.png')
imagotype = imagotype.resize((100, 100))
imagotype = ImageTk.PhotoImage(imagotype)
label_imagotype = tk.Label(start_screen, image=imagotype, bg='#F8F9FA')
label_imagotype.place(relx=0.5, rely=0.2, anchor='center')

# Etiqueta Usuario
label_usuario = tk.Label(start_screen, text='Usuario', bg='#F8F9FA', fg='#7E7E7E')
label_usuario.config(font=('DM Sans', 8))
label_usuario.place(relx=0.225, rely=0.37, anchor='center')

# Caja de texto para usuario
entry_usuario = tk.Entry(start_screen, bg='#FFFFFF', fg='#7E7E7E', font=('DM Sans', 10))
entry_usuario.place(relx=0.5, rely=0.42, anchor='center', width=200)

# Etiqueta Contraseña
label_password = tk.Label(start_screen, text='Contraseña', bg='#F8F9FA', fg='#7E7E7E')
label_password.config(font=('DM Sans', 8))
label_password.place(relx=0.255, rely=0.57, anchor='center')

# Caja de texto para contraseña
entry_password = tk.Entry(start_screen, bg='#FFFFFF', fg='#7E7E7E', font=('DM Sans', 10), show='*')
entry_password.place(relx=0.5, rely=0.62, anchor='center', width=200)


# Función para verificar el usuario desde el CSV
# Función para verificar el usuario desde el CSV
def verificar_login():
    usuario = entry_usuario.get().strip()
    contraseña = entry_password.get().strip()
    
    try:
        # Cargar la base de datos de usuarios
        usuarios_db = pd.read_csv(
            'index/usuarios.csv',
            sep=',',
            encoding='utf-8'
        )
        usuarios_db['usuario'] = usuarios_db['usuario'].astype(str).str.strip()
        usuarios_db['contraseña'] = usuarios_db['contraseña'].astype(str).str.strip()
        # Verificar credenciales
        usuario_valido = usuarios_db[
            (usuarios_db['usuario'] == usuario) & 
            (usuarios_db['contraseña'] == contraseña)
        ]
        
        if not usuario_valido.empty:
            start_screen.destroy()  # Cerrar la ventana de inicio de sesión
            main.main.show_main_window()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrecta")
    
    except FileNotFoundError:
        messagebox.showerror("Error", "No se encontró el archivo de usuarios")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al leer la base de datos: {e}")


# Botón de Ingresar
style = ttk.Style()
style.configure('Custom.TButton', background='#0080FE', foreground='white', font=('DM Sans', 10))
boton = ttk.Button(start_screen, text='Ingresar', command=verificar_login)
boton.place(relx=0.5, rely=0.8, anchor='center')


start_screen.mainloop()