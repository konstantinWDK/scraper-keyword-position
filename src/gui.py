#!/usr/bin/env python3
"""
Interfaz Gráfica para Keyword Position Scraper
GUI moderna y profesional usando CustomTkinter
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import customtkinter as ctk
import threading
import time
import json
import os
import sys
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
from PIL import Image

# Añadir directorio padre al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import Config, config
from stealth_scraper import StealthSerpScraper
from utils import KeywordManager, ResultsAnalyzer

# Configurar tema de CustomTkinter
ctk.set_appearance_mode("Dark")  # Modos: "Dark", "Light", "System"
ctk.set_default_color_theme("blue")  # Temas: "blue", "green", "dark-blue"

class KeywordScraperGUI:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Keyword Position Scraper - Anti-detección 2025")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Variables de estado
        self.scraper = None
        self.is_running = False
        self.current_results = []
        self.keywords_list = []
        
        # Configurar layout
        self.setup_gui()
        
    def setup_gui(self):
        """Configura la interfaz gráfica principal"""
        # Crear pestañas principales
        self.tabview = ctk.CTkTabview(self.root)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Crear pestañas
        self.tab_config = self.tabview.add("⚙️ Configuración")
        self.tab_keywords = self.tabview.add("🔑 Keywords")
        self.tab_scraping = self.tabview.add("🚀 Scraping")
        self.tab_results = self.tabview.add("📊 Resultados")
        self.tab_analysis = self.tabview.add("📈 Análisis")
        
        # Configurar cada pestaña
        self.setup_config_tab()
        self.setup_keywords_tab()
        self.setup_scraping_tab()
        self.setup_results_tab()
        self.setup_analysis_tab()
        
    def setup_config_tab(self):
        """Configura la pestaña de configuración"""
        # Frame principal
        main_frame = ctk.CTkFrame(self.tab_config)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título
        title_label = ctk.CTkLabel(main_frame, text="Configuración del Scraper", 
                                  font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(pady=(10, 20))
        
        # Frame de configuración en dos columnas
        config_frame = ctk.CTkFrame(main_frame)
        config_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Columna izquierda - Configuración básica
        left_frame = ctk.CTkFrame(config_frame)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        # Dominio objetivo
        domain_frame = ctk.CTkFrame(left_frame)
        domain_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(domain_frame, text="Dominio objetivo:").pack(anchor="w")
        self.domain_entry = ctk.CTkEntry(domain_frame, placeholder_text="ejemplo.com")
        self.domain_entry.pack(fill="x", pady=(5, 0))
        
        # Páginas a scrapear
        pages_frame = ctk.CTkFrame(left_frame)
        pages_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(pages_frame, text="Páginas a scrapear:").pack(anchor="w")
        self.pages_var = ctk.DoubleVar(value=1.0)
        pages_slider = ctk.CTkSlider(pages_frame, from_=1, to=10, number_of_steps=9,
                                   variable=self.pages_var, command=self.update_pages_label)
        pages_slider.pack(fill="x", pady=(5, 0))
        self.pages_label = ctk.CTkLabel(pages_frame, text="1 página")
        self.pages_label.pack()
        
        # País e idioma
        geo_frame = ctk.CTkFrame(left_frame)
        geo_frame.pack(fill="x", padx=10, pady=5)
        
        geo_inner = ctk.CTkFrame(geo_frame)
        geo_inner.pack(fill="x", pady=5)
        
        ctk.CTkLabel(geo_inner, text="País:").pack(side="left", padx=(0, 10))
        self.country_var = ctk.StringVar(value="US")
        country_combo = ctk.CTkComboBox(geo_inner, values=["US", "ES", "FR", "DE", "IT", "UK", "BR", "MX"],
                                      variable=self.country_var, width=100)
        country_combo.pack(side="left", padx=(0, 20))
        
        ctk.CTkLabel(geo_inner, text="Idioma:").pack(side="left", padx=(0, 10))
        self.language_var = ctk.StringVar(value="en")
        language_combo = ctk.CTkComboBox(geo_inner, values=["en", "es", "fr", "de", "it", "pt", "ru"],
                                       variable=self.language_var, width=100)
        language_combo.pack(side="left")
        
        # Columna derecha - Delays y proxies
        right_frame = ctk.CTkFrame(config_frame)
        right_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        # Delays
        delays_frame = ctk.CTkFrame(right_frame)
        delays_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(delays_frame, text="Delays (segundos):", font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        
        # Delay mínimo
        min_delay_frame = ctk.CTkFrame(delays_frame)
        min_delay_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(min_delay_frame, text="Mínimo:").pack(side="left")
        self.min_delay_var = ctk.StringVar(value="5")
        min_delay_entry = ctk.CTkEntry(min_delay_frame, textvariable=self.min_delay_var, width=60)
        min_delay_entry.pack(side="right")
        
        # Delay máximo
        max_delay_frame = ctk.CTkFrame(delays_frame)
        max_delay_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(max_delay_frame, text="Máximo:").pack(side="left")
        self.max_delay_var = ctk.StringVar(value="15")
        max_delay_entry = ctk.CTkEntry(max_delay_frame, textvariable=self.max_delay_var, width=60)
        max_delay_entry.pack(side="right")
        
        # Proxies
        proxies_frame = ctk.CTkFrame(right_frame)
        proxies_frame.pack(fill="both", expand=True, padx=10, pady=5)
        ctk.CTkLabel(proxies_frame, text="Proxies (desde archivos):", font=ctk.CTkFont(weight="bold")).pack(anchor="w")

        # Controles de carga de proxies
        proxies_controls = ctk.CTkFrame(proxies_frame)
        proxies_controls.pack(fill="x", pady=5)

        # Grupo de botones para CSV
        csv_frame = ctk.CTkFrame(proxies_controls)
        csv_frame.pack(side="left", padx=(0, 5))
        self.load_csv_button = ctk.CTkButton(csv_frame, text="📊 Importar CSV",
                                           command=self.load_proxies_from_csv, width=130)
        self.load_csv_button.pack()

        # Grupo de botones para TXT
        txt_frame = ctk.CTkFrame(proxies_controls)
        txt_frame.pack(side="left", padx=(0, 10))
        self.load_txt_button = ctk.CTkButton(txt_frame, text="📄 Cargar TXT",
                                          command=self.load_proxies_from_txt, width=130)
        self.load_txt_button.pack()

        # Botones adicionales
        extra_buttons = ctk.CTkFrame(proxies_controls)
        extra_buttons.pack(side="right")
        self.test_proxies_button = ctk.CTkButton(extra_buttons, text="🧪 Probar Proxies",
                                              command=self.test_loaded_proxies, width=130)
        self.test_proxies_button.pack(pady=(0, 2))
        self.clear_proxies_button = ctk.CTkButton(extra_buttons, text="🗑️ Limpiar",
                                                command=self.clear_proxies, width=130, fg_color="gray")
        self.clear_proxies_button.pack()

        self.proxies_count_label = ctk.CTkLabel(proxies_frame, text="Proxies cargados: 0")
        self.proxies_count_label.pack(anchor="w")

        # Text area para proxies (solo visualización)
        self.proxies_text = ctk.CTkTextbox(proxies_frame, height=100)
        self.proxies_text.pack(fill="both", expand=True, pady=5)
        self.proxies_text.configure(state="disabled")  # Solo lectura
        self.proxies_text.insert("1.0", "# Proxies se cargan desde CSV\n")
        
        # Botones de acción
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkButton(button_frame, text="💾 Guardar Configuración", 
                     command=self.save_config).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="🔄 Cargar Configuración", 
                     command=self.load_config).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="✅ Validar Configuración", 
                     command=self.validate_config).pack(side="left", padx=5)
        
    def setup_keywords_tab(self):
        """Configura la pestaña de gestión de keywords"""
        main_frame = ctk.CTkFrame(self.tab_keywords)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título
        title_label = ctk.CTkLabel(main_frame, text="Gestión de Keywords", 
                                  font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(pady=(10, 20))
        
        # Frame principal en dos partes
        top_frame = ctk.CTkFrame(main_frame)
        top_frame.pack(fill="x", padx=10, pady=5)
        
        bottom_frame = ctk.CTkFrame(main_frame)
        bottom_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Parte superior - Controles
        controls_frame = ctk.CTkFrame(top_frame)
        controls_frame.pack(fill="x", pady=5)
        
        # Botones de carga
        load_frame = ctk.CTkFrame(controls_frame)
        load_frame.pack(side="left", padx=5)
        ctk.CTkButton(load_frame, text="📁 Cargar desde Archivo", 
                     command=self.load_keywords_file).pack(side="left", padx=2)
        ctk.CTkButton(load_frame, text="📝 Editar Manualmente", 
                     command=self.edit_keywords_manual).pack(side="left", padx=2)
        
        # Google Suggest
        suggest_frame = ctk.CTkFrame(controls_frame)
        suggest_frame.pack(side="left", padx=5)
        ctk.CTkLabel(suggest_frame, text="Google Suggest:").pack(side="left", padx=(5, 2))
        self.suggest_entry = ctk.CTkEntry(suggest_frame, placeholder_text="Keyword base", width=150)
        self.suggest_entry.pack(side="left", padx=2)
        ctk.CTkButton(suggest_frame, text="🔍 Generar", 
                     command=self.generate_suggestions).pack(side="left", padx=2)
        
        # Contador de keywords
        count_frame = ctk.CTkFrame(controls_frame)
        count_frame.pack(side="right", padx=5)
        ctk.CTkLabel(count_frame, text="Keywords:").pack(side="left", padx=(5, 2))
        self.keywords_count_label = ctk.CTkLabel(count_frame, text="0", font=ctk.CTkFont(weight="bold"))
        self.keywords_count_label.pack(side="left", padx=2)
        
        # Parte inferior - Lista de keywords
        keywords_frame = ctk.CTkFrame(bottom_frame)
        keywords_frame.pack(fill="both", expand=True, pady=5)
        
        # Text area para keywords
        self.keywords_text = ctk.CTkTextbox(keywords_frame, font=ctk.CTkFont(family="Consolas", size=12))
        self.keywords_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Botones de acción para keywords
        action_frame = ctk.CTkFrame(bottom_frame)
        action_frame.pack(fill="x", pady=5)
        
        ctk.CTkButton(action_frame, text="🧹 Limpiar Duplicados", 
                     command=self.deduplicate_keywords).pack(side="left", padx=5)
        ctk.CTkButton(action_frame, text="🚫 Filtrar Keywords", 
                     command=self.filter_keywords).pack(side="left", padx=5)
        ctk.CTkButton(action_frame, text="💾 Guardar Keywords", 
                     command=self.save_keywords).pack(side="left", padx=5)
        
    def setup_scraping_tab(self):
        """Configura la pestaña de scraping"""
        main_frame = ctk.CTkFrame(self.tab_scraping)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título
        title_label = ctk.CTkLabel(main_frame, text="Scraping en Tiempo Real", 
                                  font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(pady=(10, 20))
        
        # Frame de controles
        controls_frame = ctk.CTkFrame(main_frame)
        controls_frame.pack(fill="x", padx=10, pady=5)
        
        # Información de configuración
        info_frame = ctk.CTkFrame(controls_frame)
        info_frame.pack(fill="x", pady=5)
        
        config_info = f"Configuración actual: {len(self.keywords_list)} keywords | Dominio: {self.domain_entry.get() or 'Todos'}"
        self.config_info_label = ctk.CTkLabel(info_frame, text=config_info)
        self.config_info_label.pack()
        
        # Botones de control
        button_frame = ctk.CTkFrame(controls_frame)
        button_frame.pack(fill="x", pady=10)
        
        self.start_button = ctk.CTkButton(button_frame, text="🚀 Iniciar Scraping", 
                                         command=self.start_scraping, 
                                         fg_color="green", hover_color="dark green")
        self.start_button.pack(side="left", padx=5)
        
        self.stop_button = ctk.CTkButton(button_frame, text="⏹️ Detener", 
                                        command=self.stop_scraping,
                                        fg_color="red", hover_color="dark red",
                                        state="disabled")
        self.stop_button.pack(side="left", padx=5)
        
        # Progreso
        progress_frame = ctk.CTkFrame(main_frame)
        progress_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(progress_frame, text="Progreso:").pack(anchor="w")
        self.progress_bar = ctk.CTkProgressBar(progress_frame)
        self.progress_bar.pack(fill="x", pady=5)
        self.progress_bar.set(0)
        
        self.progress_label = ctk.CTkLabel(progress_frame, text="Listo para comenzar")
        self.progress_label.pack()
        
        # Logs en tiempo real
        logs_frame = ctk.CTkFrame(main_frame)
        logs_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        ctk.CTkLabel(logs_frame, text="Logs de Actividad:").pack(anchor="w")
        self.logs_text = ctk.CTkTextbox(logs_frame, font=ctk.CTkFont(family="Consolas", size=11))
        self.logs_text.pack(fill="both", expand=True, pady=5)
        self.logs_text.configure(state="disabled")
        
    def setup_results_tab(self):
        """Configura la pestaña de resultados"""
        main_frame = ctk.CTkFrame(self.tab_results)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título
        title_label = ctk.CTkLabel(main_frame, text="Resultados del Scraping", 
                                  font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(pady=(10, 20))
        
        # Frame de controles
        controls_frame = ctk.CTkFrame(main_frame)
        controls_frame.pack(fill="x", padx=10, pady=5)
        
        # Botones de exportación
        export_frame = ctk.CTkFrame(controls_frame)
        export_frame.pack(side="left", padx=5)
        ctk.CTkButton(export_frame, text="📊 Exportar CSV", 
                     command=lambda: self.export_results("csv")).pack(side="left", padx=2)
        ctk.CTkButton(export_frame, text="📋 Exportar JSON", 
                     command=lambda: self.export_results("json")).pack(side="left", padx=2)
        ctk.CTkButton(export_frame, text="📈 Exportar Excel", 
                     command=lambda: self.export_results("excel")).pack(side="left", padx=2)
        
        # Filtros
        filter_frame = ctk.CTkFrame(controls_frame)
        filter_frame.pack(side="right", padx=5)
        ctk.CTkLabel(filter_frame, text="Filtrar:").pack(side="left", padx=(5, 2))
        self.filter_entry = ctk.CTkEntry(filter_frame, placeholder_text="Buscar...", width=150)
        self.filter_entry.pack(side="left", padx=2)
        ctk.CTkButton(filter_frame, text="🔍 Aplicar", 
                     command=self.apply_filter).pack(side="left", padx=2)
        
        # Tabla de resultados
        table_frame = ctk.CTkFrame(main_frame)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Crear treeview para mostrar resultados
        columns = ("keyword", "position", "title", "domain", "page")
        self.results_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        # Configurar columnas
        self.results_tree.heading("keyword", text="Keyword")
        self.results_tree.heading("position", text="Posición")
        self.results_tree.heading("title", text="Título")
        self.results_tree.heading("domain", text="Dominio")
        self.results_tree.heading("page", text="Página")
        
        self.results_tree.column("keyword", width=200)
        self.results_tree.column("position", width=80)
        self.results_tree.column("title", width=300)
        self.results_tree.column("domain", width=150)
        self.results_tree.column("page", width=80)
        
        # Scrollbar para la tabla
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=scrollbar.set)
        
        self.results_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Estadísticas rápidas
        stats_frame = ctk.CTkFrame(main_frame)
        stats_frame.pack(fill="x", padx=10, pady=5)
        
        self.stats_label = ctk.CTkLabel(stats_frame, text="Total resultados: 0 | Keywords únicas: 0 | Posición promedio: 0.0")
        self.stats_label.pack()
        
    def setup_analysis_tab(self):
        """Configura la pestaña de análisis"""
        main_frame = ctk.CTkFrame(self.tab_analysis)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título
        title_label = ctk.CTkLabel(main_frame, text="Análisis Avanzado", 
                                  font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(pady=(10, 20))
        
        # Frame de controles
        controls_frame = ctk.CTkFrame(main_frame)
        controls_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkButton(controls_frame, text="📊 Generar Análisis", 
                     command=self.generate_analysis).pack(side="left", padx=5)
        ctk.CTkButton(controls_frame, text="📈 Actualizar Gráficos", 
                     command=self.update_charts).pack(side="left", padx=5)
        
        # Frame para gráficos
        charts_frame = ctk.CTkFrame(main_frame)
        charts_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Crear figura para matplotlib
        self.fig, ((self.ax1, self.ax2), (self.ax3, self.ax4)) = plt.subplots(2, 2, figsize=(12, 8))
        self.fig.tight_layout(pad=3.0)
        
        # Canvas para matplotlib
        self.canvas = FigureCanvasTkAgg(self.fig, charts_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        
    # ========== MÉTODOS DE UTILIDAD ==========
    
    def update_pages_label(self, value):
        """Actualiza la etiqueta de páginas"""
        pages = int(float(value))
        self.pages_label.configure(text=f"{pages} página{'s' if pages > 1 else ''}")
        
    def log_message(self, message):
        """Añade mensaje a los logs"""
        self.logs_text.configure(state="normal")
        timestamp = time.strftime("%H:%M:%S")
        self.logs_text.insert("end", f"[{timestamp}] {message}\n")
        self.logs_text.see("end")
        self.logs_text.configure(state="disabled")
        
    def update_progress(self, current, total, message=""):
        """Actualiza la barra de progreso"""
        progress = current / total if total > 0 else 0
        self.progress_bar.set(progress)
        self.progress_label.configure(text=f"{current}/{total} - {message}")
        
    def update_keywords_count(self):
        """Actualiza el contador de keywords"""
        keywords_text = self.keywords_text.get("1.0", "end-1c")
        keywords_list = [k.strip() for k in keywords_text.split('\n') if k.strip()]
        self.keywords_list = keywords_list
        self.keywords_count_label.configure(text=str(len(keywords_list)))
        
    # ========== MÉTODOS DE PROXIES ==========

    def load_proxies_from_csv(self):
        """Carga proxies desde archivo CSV"""
        try:
            file_path = filedialog.askopenfilename(
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )

            if file_path:
                from utils import ProxyManager

                # Cargar y convertir proxies
                proxies = ProxyManager.import_from_csv(file_path)

                if proxies:
                    # Mostrar proxies en el text area
                    self.proxies_text.configure(state="normal")
                    self.proxies_text.delete("1.0", "end")
                    self.proxies_text.insert("1.0", "\n".join(proxies))
                    self.proxies_text.configure(state="disabled")

                    # Actualizar contador
                    self.proxies_count_label.configure(text=f"Proxies cargados: {len(proxies)}")

                    # Mostrar estadísticas
                    ProxyManager.show_proxy_stats(proxies)
                    self.log_message(f"✅ Cargados {len(proxies)} proxies desde {file_path}")
                else:
                    messagebox.showerror("Error", "No se pudieron importar proxies desde el CSV")

        except Exception as e:
            messagebox.showerror("Error", f"Error cargando proxies: {e}")
            self.log_message(f"❌ Error cargando proxies desde CSV: {e}")

    def load_proxies_from_txt(self):
        """Carga proxies desde archivo TXT"""
        try:
            file_path = filedialog.askopenfilename(
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )

            if file_path:
                from utils import ProxyManager

                # Cargar proxies usando el ProxyManager
                proxies = ProxyManager.load_proxies(file_path)

                if proxies:
                    # Mostrar proxies en el text area
                    self.proxies_text.configure(state="normal")
                    self.proxies_text.delete("1.0", "end")
                    self.proxies_text.insert("1.0", "\n".join(proxies))
                    self.proxies_text.configure(state="disabled")

                    # Actualizar contador
                    self.proxies_count_label.configure(text=f"Proxies cargados: {len(proxies)}")

                    # Mostrar estadísticas
                    ProxyManager.show_proxy_stats(proxies)
                    self.log_message(f"✅ Cargados {len(proxies)} proxies desde {file_path}")
                else:
                    messagebox.showerror("Error", "No se pudieron cargar proxies desde el archivo TXT")

        except Exception as e:
            messagebox.showerror("Error", f"Error cargando proxies: {e}")
            self.log_message(f"❌ Error cargando proxies desde TXT: {e}")

    def test_loaded_proxies(self):
        """Prueba los proxies cargados actualmente"""
        try:
            # Obtener proxies del text area
            proxies_text = self.proxies_text.get("1.0", "end-1c").strip()

            if not proxies_text:
                messagebox.showwarning("Advertencia", "No hay proxies cargados para probar")
                return

            proxies = [line.strip() for line in proxies_text.split('\n') if line.strip()]

            if not proxies:
                messagebox.showwarning("Advertencia", "No hay proxies válidos para probar")
                return

            # Preguntar confirmación para pruebas masivas
            if len(proxies) > 10:
                response = messagebox.askyesno(
                    "Confirmar",
                    f"¿Estás seguro de probar {len(proxies)} proxies? Esto puede tomar tiempo."
                )
                if not response:
                    self.log_message("❌ Prueba de proxies cancelada por el usuario")
                    return

            # Ejecutar pruebas en hilo separado
            def test_thread():
                try:
                    self.log_message(f"🧪 Probando {len(proxies)} proxies...")

                    from utils import ProxyManager
                    working_proxies = ProxyManager.filter_working_proxies(proxies, timeout=5)

                    # Actualizar text area con solo proxies funcionando
                    if working_proxies:
                        self.proxies_text.configure(state="normal")
                        self.proxies_text.delete("1.0", "end")
                        self.proxies_text.insert("1.0", "\n".join(working_proxies))
                        self.proxies_text.configure(state="disabled")
                        self.proxies_count_label.configure(text=f"Proxies funcionando: {len(working_proxies)}")

                        # Guardar proxies funcionando
                        ProxyManager.save_proxies(working_proxies, 'working_proxies')
                        self.log_message(f"✅ {len(working_proxies)} proxies funcionando guardados")

                except Exception as e:
                    self.log_message(f"❌ Error probando proxies: {e}")

            threading.Thread(target=test_thread, daemon=True).start()

        except Exception as e:
            messagebox.showerror("Error", f"Error iniciando test de proxies: {e}")

    def clear_proxies(self):
        """Limpia todos los proxies cargados"""
        try:
            self.proxies_text.configure(state="normal")
            self.proxies_text.delete("1.0", "end")
            self.proxies_text.insert("1.0", "# Proxies se cargan desde archivos\n")
            self.proxies_text.configure(state="disabled")

            self.proxies_count_label.configure(text="Proxies cargados: 0")
            self.log_message("🗑️ Proxies limpiados")

        except Exception as e:
            messagebox.showerror("Error", f"Error limpiando proxies: {e}")

    # ========== MÉTODOS DE CONFIGURACIÓN ==========

    def save_config(self):
        """Guarda la configuración actual"""
        try:
            config_data = {
                'domain': self.domain_entry.get(),
                'pages': int(self.pages_var.get()),
                'country': self.country_var.get(),
                'language': self.language_var.get(),
                'min_delay': int(self.min_delay_var.get()),
                'max_delay': int(self.max_delay_var.get()),
                'proxies': self.proxies_text.get("1.0", "end-1c").strip()
            }
            
            file_path = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(config_data, f, indent=2, ensure_ascii=False)
                messagebox.showinfo("Éxito", "Configuración guardada correctamente")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error guardando configuración: {e}")
            
    def load_config(self):
        """Carga configuración desde archivo"""
        try:
            file_path = filedialog.askopenfilename(
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if file_path:
                with open(file_path, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                
                self.domain_entry.delete(0, "end")
                self.domain_entry.insert(0, config_data.get('domain', ''))
                
                self.pages_var.set(str(config_data.get('pages', 1)))
                self.update_pages_label(self.pages_var.get())
                
                self.country_var.set(config_data.get('country', 'US'))
                self.language_var.set(config_data.get('language', 'en'))
                
                self.min_delay_var.set(str(config_data.get('min_delay', 5)))
                self.max_delay_var.set(str(config_data.get('max_delay', 15)))
                
                self.proxies_text.delete("1.0", "end")
                self.proxies_text.insert("1.0", config_data.get('proxies', ''))
                
                messagebox.showinfo("Éxito", "Configuración cargada correctamente")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error cargando configuración: {e}")
            
    def validate_config(self):
        """Valida la configuración actual"""
        issues = []
        
        if not self.domain_entry.get().strip():
            issues.append("⚠️ Dominio objetivo no especificado")
            
        if int(self.min_delay_var.get()) < 3:
            issues.append("⚠️ Delay mínimo muy bajo (mínimo recomendado: 3s)")
            
        if int(self.max_delay_var.get()) < int(self.min_delay_var.get()):
            issues.append("⚠️ Delay máximo debe ser mayor que delay mínimo")
            
        if not issues:
            messagebox.showinfo("Validación", "✅ Configuración válida")
        else:
            messagebox.showwarning("Validación", "\n".join(issues))
            
    # ========== MÉTODOS DE KEYWORDS ==========
    
    def load_keywords_file(self):
        """Carga keywords desde archivo"""
        try:
            file_path = filedialog.askopenfilename(
                filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv"), ("All files", "*.*")]
            )
            
            if file_path:
                with open(file_path, 'r', encoding='utf-8') as f:
                    keywords = [line.strip() for line in f.readlines() if line.strip()]
                
                self.keywords_text.delete("1.0", "end")
                self.keywords_text.insert("1.0", "\n".join(keywords))
                self.update_keywords_count()
                self.log_message(f"✅ Cargadas {len(keywords)} keywords desde {file_path}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error cargando keywords: {e}")
            
    def edit_keywords_manual(self):
        """Abre ventana para edición manual de keywords"""
        edit_window = ctk.CTkToplevel(self.root)
        edit_window.title("Edición Manual de Keywords")
        edit_window.geometry("600x400")
        edit_window.transient(self.root)
        edit_window.grab_set()
        
        # Text area para edición
        text_area = ctk.CTkTextbox(edit_window, font=ctk.CTkFont(family="Consolas", size=12))
        text_area.pack(fill="both", expand=True, padx=20, pady=20)
        text_area.insert("1.0", self.keywords_text.get("1.0", "end-1c"))
        
        def save_changes():
            self.keywords_text.delete("1.0", "end")
            self.keywords_text.insert("1.0", text_area.get("1.0", "end-1c"))
            self.update_keywords_count()
            edit_window.destroy()
            
        # Botones
        button_frame = ctk.CTkFrame(edit_window)
        button_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkButton(button_frame, text="💾 Guardar", 
                     command=save_changes, fg_color="green").pack(side="right", padx=5)
        ctk.CTkButton(button_frame, text="❌ Cancelar", 
                     command=edit_window.destroy).pack(side="right", padx=5)
        
    def generate_suggestions(self):
        """Genera keywords usando Google Suggest"""
        base_keyword = self.suggest_entry.get().strip()
        if not base_keyword:
            messagebox.showwarning("Advertencia", "Ingresa una keyword base")
            return
            
        def suggest_thread():
            try:
                self.log_message(f"🔍 Generando sugerencias para: '{base_keyword}'")
                
                # Usar el scraper existente o crear uno nuevo
                if not self.scraper:
                    from config.settings import config
                    self.scraper = StealthSerpScraper(config)
                
                suggestions = self.scraper.google_suggest_scraper(
                    base_keyword,
                    country=self.country_var.get(),
                    language=self.language_var.get()
                )
                
                if suggestions:
                    # Añadir sugerencias a la lista actual
                    current_text = self.keywords_text.get("1.0", "end-1c")
                    current_keywords = [k.strip() for k in current_text.split('\n') if k.strip()]
                    
                    # Combinar y eliminar duplicados
                    all_keywords = list(set(current_keywords + suggestions))
                    
                    self.keywords_text.delete("1.0", "end")
                    self.keywords_text.insert("1.0", "\n".join(all_keywords))
                    self.update_keywords_count()
                    
                    self.log_message(f"✅ Generadas {len(suggestions)} sugerencias")
                else:
                    self.log_message("❌ No se encontraron sugerencias")
                    
            except Exception as e:
                self.log_message(f"❌ Error generando sugerencias: {e}")
                
        # Ejecutar en hilo separado
        threading.Thread(target=suggest_thread, daemon=True).start()
        
    def deduplicate_keywords(self):
        """Elimina keywords duplicadas"""
        from utils import KeywordManager
        
        keywords_text = self.keywords_text.get("1.0", "end-1c")
        keywords_list = [k.strip() for k in keywords_text.split('\n') if k.strip()]
        
        unique_keywords = KeywordManager.deduplicate_keywords(keywords_list)
        
        self.keywords_text.delete("1.0", "end")
        self.keywords_text.insert("1.0", "\n".join(unique_keywords))
        self.update_keywords_count()
        
        removed = len(keywords_list) - len(unique_keywords)
        self.log_message(f"🧹 Eliminadas {removed} keywords duplicadas")
        
    def filter_keywords(self):
        """Filtra keywords por criterios"""
        from utils import KeywordManager
        
        keywords_text = self.keywords_text.get("1.0", "end-1c")
        keywords_list = [k.strip() for k in keywords_text.split('\n') if k.strip()]
        
        filtered_keywords = KeywordManager.filter_keywords(keywords_list)
        
        self.keywords_text.delete("1.0", "end")
        self.keywords_text.insert("1.0", "\n".join(filtered_keywords))
        self.update_keywords_count()
        
        removed = len(keywords_list) - len(filtered_keywords)
        self.log_message(f"🚫 Filtradas {removed} keywords")
        
    def save_keywords(self):
        """Guarda keywords en archivo"""
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            
            if file_path:
                keywords_text = self.keywords_text.get("1.0", "end-1c")
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(keywords_text)
                    
                messagebox.showinfo("Éxito", f"Keywords guardadas en {file_path}")
                self.log_message(f"💾 Keywords guardadas en {file_path}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error guardando keywords: {e}")
            
    # ========== MÉTODOS DE SCRAPING ==========
    
    def start_scraping(self):
        """Inicia el proceso de scraping"""
        if not self.keywords_list:
            messagebox.showwarning("Advertencia", "No hay keywords para scrapear")
            return
            
        # Actualizar configuración
        self.update_config_info()
        
        # Cambiar estado de botones
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.is_running = True
        
        # Iniciar scraping en hilo separado
        threading.Thread(target=self.scraping_thread, daemon=True).start()
        
    def stop_scraping(self):
        """Detiene el proceso de scraping"""
        self.is_running = False
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.log_message("⏹️ Scraping detenido por el usuario")
        
    def scraping_thread(self):
        """Hilo principal de scraping"""
        try:
            self.log_message("🚀 Iniciando scraping...")
            
            # Crear scraper con configuración actual
            from config.settings import config
            custom_config = config.copy()
            custom_config.update({
                'MIN_KEYWORD_DELAY': int(self.min_delay_var.get()),
                'MAX_KEYWORD_DELAY': int(self.max_delay_var.get()),
                'PAGES_TO_SCRAPE': int(self.pages_var.get()),
                'DEFAULT_COUNTRY': self.country_var.get(),
                'DEFAULT_LANGUAGE': self.language_var.get()
            })
            
            self.scraper = StealthSerpScraper(custom_config)
            
            # Ejecutar scraping
            target_domain = self.domain_entry.get().strip() or None
            results = self.scraper.batch_position_check(
                self.keywords_list, 
                target_domain, 
                int(self.pages_var.get())
            )
            
            if results and self.is_running:
                self.current_results = results
                self.update_results_table()
                self.update_stats()
                self.log_message(f"✅ Scraping completado: {len(results)} resultados")
                
                # Guardar resultados automáticamente
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                domain_suffix = f"_{target_domain}" if target_domain else ""
                filename = f"positions{domain_suffix}_{timestamp}"
                self.scraper.save_results(results, filename)
                self.log_message(f"💾 Resultados guardados en data/{filename}.csv")
                
            elif not self.is_running:
                self.log_message("❌ Scraping cancelado")
            else:
                self.log_message("❌ No se obtuvieron resultados")
                
        except Exception as e:
            self.log_message(f"❌ Error en scraping: {e}")
        finally:
            # Restaurar estado de botones
            self.start_button.configure(state="normal")
            self.stop_button.configure(state="disabled")
            self.is_running = False
            self.update_progress(0, 1, "Completado")
            
    def update_config_info(self):
        """Actualiza la información de configuración"""
        config_info = f"Configuración actual: {len(self.keywords_list)} keywords | Dominio: {self.domain_entry.get() or 'Todos'}"
        self.config_info_label.configure(text=config_info)
        
    def update_results_table(self):
        """Actualiza la tabla de resultados"""
        # Limpiar tabla existente
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
            
        # Añadir nuevos resultados
        for result in self.current_results:
            self.results_tree.insert("", "end", values=(
                result['keyword'],
                result['position'],
                result['title'][:80] + "..." if len(result['title']) > 80 else result['title'],
                result['domain'],
                result['page']
            ))
            
    def update_stats(self):
        """Actualiza las estadísticas"""
        if not self.current_results:
            return
            
        df = pd.DataFrame(self.current_results)
        total_results = len(df)
        unique_keywords = df['keyword'].nunique()
        avg_position = df['position'].mean()
        
        stats_text = f"Total resultados: {total_results} | Keywords únicas: {unique_keywords} | Posición promedio: {avg_position:.1f}"
        self.stats_label.configure(text=stats_text)
        
    def apply_filter(self):
        """Aplica filtro a la tabla de resultados"""
        filter_text = self.filter_entry.get().lower()
        if not filter_text:
            # Mostrar todos los resultados si no hay filtro
            self.update_results_table()
            return
            
        # Filtrar resultados
        filtered_results = [
            r for r in self.current_results 
            if filter_text in r['keyword'].lower() or 
               filter_text in r['title'].lower() or 
               filter_text in r['domain'].lower()
        ]
        
        # Actualizar tabla con resultados filtrados
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
            
        for result in filtered_results:
            self.results_tree.insert("", "end", values=(
                result['keyword'],
                result['position'],
                result['title'][:80] + "..." if len(result['title']) > 80 else result['title'],
                result['domain'],
                result['page']
            ))
            
    def export_results(self, format_type):
        """Exporta resultados en el formato especificado"""
        if not self.current_results:
            messagebox.showwarning("Advertencia", "No hay resultados para exportar")
            return
            
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=f".{format_type}",
                filetypes=[(f"{format_type.upper()} files", f"*.{format_type}"), ("All files", "*.*")]
            )
            
            if file_path:
                df = pd.DataFrame(self.current_results)
                
                if format_type == "csv":
                    df.to_csv(file_path, index=False, encoding='utf-8')
                elif format_type == "json":
                    df.to_json(file_path, orient='records', indent=2, force_ascii=False)
                elif format_type == "excel":
                    df.to_excel(file_path, index=False)
                    
                messagebox.showinfo("Éxito", f"Resultados exportados a {file_path}")
                self.log_message(f"📤 Resultados exportados a {file_path}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error exportando resultados: {e}")
            
    def generate_analysis(self):
        """Genera análisis avanzado de resultados"""
        if not self.current_results:
            messagebox.showwarning("Advertencia", "No hay resultados para analizar")
            return
            
        try:
            from utils import ResultsAnalyzer
            
            analyzer = ResultsAnalyzer()
            df = pd.DataFrame(self.current_results)
            
            # Limpiar gráficos anteriores
            for ax in [self.ax1, self.ax2, self.ax3, self.ax4]:
                ax.clear()
                
            # Gráfico 1: Distribución de posiciones
            position_counts = df['position'].value_counts().sort_index()
            self.ax1.bar(position_counts.index, position_counts.values, color='skyblue', alpha=0.7)
            self.ax1.set_title('Distribución de Posiciones')
            self.ax1.set_xlabel('Posición')
            self.ax1.set_ylabel('Frecuencia')
            self.ax1.grid(True, alpha=0.3)
            
            # Gráfico 2: Top dominios
            top_domains = df['domain'].value_counts().head(10)
            self.ax2.barh(range(len(top_domains)), top_domains.values, color='lightgreen', alpha=0.7)
            self.ax2.set_yticks(range(len(top_domains)))
            self.ax2.set_yticklabels(top_domains.index)
            self.ax2.set_title('Top 10 Dominios')
            self.ax2.set_xlabel('Frecuencia')
            self.ax2.grid(True, alpha=0.3)
            
            # Gráfico 3: Posiciones por página
            if 'page' in df.columns:
                page_stats = df.groupby('page')['position'].agg(['mean', 'count'])
                self.ax3.bar(page_stats.index, page_stats['count'], color='orange', alpha=0.7, label='Resultados')
                self.ax3_twin = self.ax3.twinx()
                self.ax3_twin.plot(page_stats.index, page_stats['mean'], color='red', marker='o', linewidth=2, label='Posición promedio')
                self.ax3.set_title('Resultados por Página')
                self.ax3.set_xlabel('Página')
                self.ax3.set_ylabel('Resultados')
                self.ax3_twin.set_ylabel('Posición promedio')
                self.ax3.legend(loc='upper left')
                self.ax3_twin.legend(loc='upper right')
                self.ax3.grid(True, alpha=0.3)
            else:
                self.ax3.text(0.5, 0.5, 'No hay datos de páginas', 
                             horizontalalignment='center', verticalalignment='center',
                             transform=self.ax3.transAxes, fontsize=12)
                self.ax3.set_title('Resultados por Página')
                
            # Gráfico 4: Distribución de posiciones (boxplot)
            self.ax4.boxplot(df['position'], vert=False)
            self.ax4.set_title('Distribución de Posiciones')
            self.ax4.set_xlabel('Posición')
            self.ax4.grid(True, alpha=0.3)
            
            # Actualizar canvas
            self.fig.tight_layout(pad=3.0)
            self.canvas.draw()
            
            self.log_message("📊 Análisis generado correctamente")
            
        except Exception as e:
            self.log_message(f"❌ Error generando análisis: {e}")
            
    def update_charts(self):
        """Actualiza los gráficos con los datos actuales"""
        self.generate_analysis()
        
    def run(self):
        """Ejecuta la aplicación"""
        self.root.mainloop()


def main():
    """Función principal para ejecutar la GUI"""
    try:
        # Verificar que los directorios necesarios existan
        for directory in ['data', 'logs']:
            os.makedirs(directory, exist_ok=True)
            
        app = KeywordScraperGUI()
        app.run()
        
    except Exception as e:
        print(f"Error iniciando la GUI: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
