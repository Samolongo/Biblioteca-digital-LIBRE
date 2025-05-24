import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import FuncFormatter

def abrir_dashboard(parent, csv_path="book_database/books_clean_short.csv"):
    class DashboardBiblioteca(tk.Toplevel):
        def __init__(self, parent,csv_path):
            super().__init__(parent)
            self.title("Análisis de Libros")
            self.geometry("1200x800")
            self.configure(bg="#f5f5f5")
            self.iconbitmap('index/index_media/libre_isotype.ico')

            # Estilo de gráficos (usando un estilo disponible)
            plt.style.use('ggplot')  # Cambiado de 'seaborn' a 'ggplot' que es un estilo disponible
            self.colors = ['#3498db', '#2ecc71', '#e74c3c', '#9b59b6', '#f1c40f', 
                            '#1abc9c', '#34495e', '#e67e22', '#95a5a6', '#d35400']

            # Cargar datos
            try:
                self.df = pd.read_csv(csv_path)
                # Limpieza y preparación de datos
                self.df['año_publicación'] = pd.to_numeric(self.df['año_publicación'], errors='coerce')
                self.df['calificación_promedio'] = pd.to_numeric(self.df['calificación_promedio'], errors='coerce')
                self.df['num_calificaciones'] = pd.to_numeric(self.df['num_calificaciones'], errors='coerce').fillna(0)
                self.df['copias'] = pd.to_numeric(self.df['copias'], errors='coerce').fillna(0)
                
                # Limpiar nombres de autores (tomar solo el primer autor)
                self.df['autor_principal'] = self.df['autor'].str.split(',').str[0].str.strip()
                
                # Calcular popularidad combinando calificaciones y número de reseñas
                self.df['popularidad'] = self.df['calificación_promedio'] * (self.df['num_calificaciones'] / 1000)
                
            except Exception as e:
                tk.messagebox.showerror("Error", f"No se pudo cargar el CSV:\n{e}")
                self.destroy()
                return

            # Título
            titulo = tk.Label(self, text="Análisis de Libros", font=("Helvetica", 24, "bold"), bg="#f5f5f5", fg="#2c3e50")
            titulo.pack(pady=20)

            # Crear frame principal con scrollbar
            main_frame = tk.Frame(self, bg="#f5f5f5")
            main_frame.pack(fill=tk.BOTH, expand=True)

            # Canvas para el scroll
            canvas = tk.Canvas(main_frame, bg="#f5f5f5", highlightthickness=0)
            scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg="#f5f5f5")

            # Configurar el canvas
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
            )
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            # Empaquetar canvas y scrollbar
            canvas.pack(side="left", fill="both", expand=True, padx=10)
            scrollbar.pack(side="right", fill="y")

            # Cuadro de filtros
            filtro_frame = tk.Frame(scrollable_frame, bg="#f5f5f5", padx=10, pady=10)
            filtro_frame.pack(fill=tk.X)

            # Filtro por año
            tk.Label(filtro_frame, text="Filtrar por Año:", bg="#f5f5f5", font=("Helvetica", 12)).pack(side=tk.LEFT)
            self.anios = sorted(self.df['año_publicación'].dropna().unique().astype(int))
            self.anio_var = tk.StringVar()
            anio_menu = ttk.Combobox(filtro_frame, textvariable=self.anio_var, 
                                    values=["Todos"] + [str(a) for a in self.anios], 
                                    state="readonly", width=10)
            anio_menu.current(0)
            anio_menu.pack(side=tk.LEFT, padx=10)
            anio_menu.bind("<<ComboboxSelected>>", self.actualizar_dashboard)

            # Filtro por género
            tk.Label(filtro_frame, text="Filtrar por Género:", bg="#f5f5f5", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=(20,5))
            self.generos = sorted(self.df['género'].dropna().unique())
            self.genero_var = tk.StringVar()
            genero_menu = ttk.Combobox(filtro_frame, textvariable=self.genero_var, 
                                        values=["Todos"] + self.generos, 
                                        state="readonly", width=15)
            genero_menu.current(0)
            genero_menu.pack(side=tk.LEFT)
            genero_menu.bind("<<ComboboxSelected>>", self.actualizar_dashboard)

            # Panel de gráficos
            self.graficos_frame = tk.Frame(scrollable_frame, bg="#f5f5f5")
            self.graficos_frame.pack(fill=tk.BOTH, expand=True, padx=10)

            # Configurar el evento de scroll con la rueda del mouse
            canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1*(event.delta/120)), "units"))

            self.crear_graficos()

        def filtrar_datos(self):
            df_filtrado = self.df.copy()
            
            # Filtrar por año si no es "Todos"
            if self.anio_var.get() != "Todos" and self.anio_var.get() != "":
                df_filtrado = df_filtrado[df_filtrado['año_publicación'] == int(self.anio_var.get())]
            
            # Filtrar por género si no es "Todos"
            if self.genero_var.get() != "Todos" and self.genero_var.get() != "":
                df_filtrado = df_filtrado[df_filtrado['género'] == self.genero_var.get()]
                
            return df_filtrado

        def crear_graficos(self):
            # Limpiar panel
            for widget in self.graficos_frame.winfo_children():
                widget.destroy()

            df_filtrado = self.filtrar_datos()

            # Panel superior (2 gráficas)
            top_frame = tk.Frame(self.graficos_frame, bg="#f5f5f5")
            top_frame.pack(fill=tk.BOTH, expand=True, pady=10)

            self.agregar_grafico(
                top_frame, "Distribución de Calificaciones", self.plot_calificaciones(df_filtrado), side=tk.LEFT)

            self.agregar_grafico(
                top_frame, "Top 4 Géneros", self.plot_top_generos(df_filtrado), side=tk.LEFT)

            # Panel medio (2 gráficas)
            middle_frame = tk.Frame(self.graficos_frame, bg="#f5f5f5")
            middle_frame.pack(fill=tk.BOTH, expand=True, pady=10)

            self.agregar_grafico(
                middle_frame, "Evolución de Publicaciones", self.plot_libros_por_anio(), side=tk.LEFT)

            self.agregar_grafico(
                middle_frame, "Autores Más Prolíficos", self.plot_top_autores(df_filtrado), side=tk.LEFT)

            # Panel inferior (2 gráficas)
            bottom_frame = tk.Frame(self.graficos_frame, bg="#f5f5f5")
            bottom_frame.pack(fill=tk.BOTH, expand=True, pady=10)

            self.agregar_grafico(
                bottom_frame, "Libros Más Populares", self.plot_libros_populares(df_filtrado), side=tk.LEFT)

            

        def agregar_grafico(self, parent, titulo, fig, side=tk.LEFT):
            panel = tk.Frame(parent, bg="white", bd=2, relief=tk.GROOVE)
            panel.pack(side=side, expand=True, fill=tk.BOTH, padx=10, pady=5)

            lbl = tk.Label(panel, text=titulo, font=("Helvetica", 12, "bold"), bg="white", fg="#2c3e50")
            lbl.pack(pady=10)

            canvas = FigureCanvasTkAgg(fig, master=panel)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
            plt.close(fig)  # Cerrar la figura para liberar memoria

        def plot_top_generos(self, df):
            fig, ax = plt.subplots(figsize=(6, 4.5))
            genre_counts = df['género'].value_counts().nlargest(10)
            genre_counts.plot(kind='barh', ax=ax, color=self.colors)
            
            # Añadir etiquetas de datos
            for i, v in enumerate(genre_counts):
                ax.text(v + 0.5, i, f"{v}", color='black', va='center')
                
            ax.set_xlabel("Cantidad de Libros", fontsize=10)
            ax.set_ylabel("Género", fontsize=10)
            ax.invert_yaxis()
            ax.grid(axis='x', linestyle='--', alpha=0.6)
            plt.tight_layout()
            return fig

        def plot_calificaciones(self, df):
            fig, ax = plt.subplots(figsize=(6, 4.5))
            ratings = df['calificación_promedio'].dropna()
            
            # Histograma mejorado
            n, bins, patches = ax.hist(ratings, bins=20, color=self.colors[0], 
                                    edgecolor='white', alpha=0.7)
            
            # Resaltar la moda
            max_bin = bins[n.argmax()]
            ax.axvline(max_bin, color='red', linestyle='--', linewidth=1.5)
            ax.annotate(f'Moda: {max_bin:.1f}', xy=(max_bin, n.max()), 
                    xytext=(10, 10), textcoords='offset points',
                    bbox=dict(boxstyle='round,pad=0.5', fc='white', alpha=0.8))
            
            ax.set_xlabel("Calificación Promedio (1-5 estrellas)", fontsize=10)
            ax.set_ylabel("Frecuencia", fontsize=10)
            ax.grid(axis='y', linestyle='--', alpha=0.6)
            plt.tight_layout()
            return fig

        def plot_libros_por_anio(self):
            fig, ax = plt.subplots(figsize=(6, 4.5))
            yearly_counts = self.df['año_publicación'].dropna().astype(int).value_counts().sort_index()
            
            # Gráfico de área para mejor visualización
            ax.fill_between(yearly_counts.index, yearly_counts.values, 
                        color=self.colors[1], alpha=0.4)
            ax.plot(yearly_counts.index, yearly_counts.values, 
                color=self.colors[1], linewidth=2.5, marker='o', markersize=6)
            
            # Resaltar puntos importantes
            max_year = yearly_counts.idxmax()
            ax.plot(max_year, yearly_counts[max_year], 'ro', markersize=8)
            ax.annotate(f'Máximo: {max_year}', 
                    xy=(max_year, yearly_counts[max_year]), 
                    xytext=(10, 10), textcoords='offset points',
                    bbox=dict(boxstyle='round,pad=0.5', fc='white', alpha=0.8))
            
            ax.set_xlabel("Año de Publicación", fontsize=10)
            ax.set_ylabel("Cantidad de Libros Publicados", fontsize=10)
            plt.xticks(rotation=45)
            ax.grid(True, linestyle='--', alpha=0.6)
            plt.tight_layout()
            return fig

        def plot_top_autores(self, df):
            fig, ax = plt.subplots(figsize=(6, 4.5))
            top_authors = df['autor_principal'].value_counts().nlargest(10)
            
            # Gráfico de barras horizontales con colores
            bars = ax.barh(top_authors.index, top_authors.values, color=self.colors)
            
            # Añadir etiquetas de datos
            for bar in bars:
                width = bar.get_width()
                ax.text(width + 0.5, bar.get_y() + bar.get_height()/2,
                    f"{int(width)}", va='center')
                
            ax.set_xlabel("Cantidad de Libros", fontsize=10)
            ax.set_ylabel("Autor", fontsize=10)
            ax.invert_yaxis()
            ax.grid(axis='x', linestyle='--', alpha=0.6)
            plt.tight_layout()
            return fig

        def plot_libros_populares(self, df):
            fig, ax = plt.subplots(figsize=(6, 4.5))
            
            # Obtener los 10 libros más populares
            top_books = df.nlargest(10, 'popularidad')[['título', 'calificación_promedio', 'num_calificaciones']]
            
            # Acortar títulos largos y crear etiquetas
            top_books['título_corto'] = top_books['título'].apply(
                lambda x: (x[:18] + '...') if len(x) > 20 else x)
            
            # Gráfico de barras horizontales
            y_pos = range(len(top_books))
            bars = ax.barh(y_pos, top_books['calificación_promedio'], 
                        color=self.colors, alpha=0.8)
            
            # Añadir información detallada
            for i, (rating, reviews, title) in enumerate(zip(
                top_books['calificación_promedio'], 
                top_books['num_calificaciones'], 
                top_books['título_corto'])):
                
                # Mostrar título a la izquierda
                ax.text(0.05, i, title, ha='left', va='center', color='black', 
                    fontsize=9, transform=ax.get_yaxis_transform())
                
                # Mostrar rating y reseñas a la derecha
                ax.text(rating + 0.1, i, 
                    f"{rating:.2f} ★ ({reviews/1000:.1f}k)", 
                    va='center', fontsize=9)
            
            ax.set_xlim(0, 5.5)
            ax.set_xlabel("Calificación Promedio (1-5 estrellas)", fontsize=10)
            ax.set_yticks(y_pos)
            ax.set_yticklabels([''] * len(y_pos))  # Ocultar etiquetas Y ya que usamos texto
            ax.invert_yaxis()
            ax.grid(axis='x', linestyle='--', alpha=0.6)
            plt.tight_layout()
            return fig

        def plot_generos_por_anio(self):
            fig, ax = plt.subplots(figsize=(6, 4.5))
            
            # Preparar datos: contar géneros por año
            genre_year = self.df.groupby(['año_publicación', 'género']).size().unstack().fillna(0)
            
            # Tomar los 5 géneros más comunes
            top_genres = self.df['género'].value_counts().nlargest(5).index
            genre_year = genre_year[top_genres]
            
            # Gráfico de líneas para mejor claridad
            for i, genre in enumerate(top_genres):
                ax.plot(genre_year.index, genre_year[genre], 
                        label=genre, color=self.colors[i], linewidth=2.5, marker='o')
            
            ax.set_xlabel("Año de Publicación", fontsize=10)
            ax.set_ylabel("Cantidad de Libros", fontsize=10)
            ax.legend(title='Género', bbox_to_anchor=(1.05, 1), loc='upper left')
            ax.grid(True, linestyle='--', alpha=0.6)
            
            # Formatear el eje Y para mostrar números enteros
            ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: int(x)))
            
            plt.tight_layout()
            return fig

        def actualizar_dashboard(self, event=None):
            self.crear_graficos()

    DashboardBiblioteca(parent, csv_path)
