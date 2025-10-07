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

        # Variables de configuración
        self.api_key_var = ctk.StringVar()
        self.search_engine_id_var = ctk.StringVar()
        self.use_api_var = ctk.BooleanVar(value=True)

        # Variables de configuración de scraper
        self.domain_entry = None
        self.pages_var = ctk.DoubleVar(value=1.0)
        self.country_var = ctk.StringVar(value="US")
        self.language_var = ctk.StringVar(value="en")
        self.min_delay_var = ctk.StringVar(value="5")
        self.max_delay_var = ctk.StringVar(value="15")

        # Variables de resultados
        self.results_tree = None
        self.stats_label = None
        self.logs_text = None
        self.progress_bar = None
        self.progress_label = None
        self.start_button = None
        self.stop_button = None
        self.config_info_label = None
        self.keywords_count_label = None
        self.keywords_text = None
        self.suggest_entry = None

        # Crear directorios necesarios
        for directory in ['data', 'logs', 'config']:
            os.makedirs(directory, exist_ok=True)

        # Configurar layout
        self.setup_gui()

        # Cargar configuraciones existentes al iniciar
        self.load_saved_config()

    def load_saved_config(self):
        """Carga las credenciales guardadas al iniciar"""
        try:
            from config.settings import Config

            # Cargar API Key
            if hasattr(self, 'api_key_var') and Config.GOOGLE_API_KEY:
                self.api_key_var.set(Config.GOOGLE_API_KEY)

            # Cargar Search Engine ID
            if hasattr(self, 'search_engine_id_var') and Config.GOOGLE_SEARCH_ENGINE_ID:
                self.search_engine_id_var.set(Config.GOOGLE_SEARCH_ENGINE_ID)

            # Cargar delays básicos
            if hasattr(self, 'min_delay_var'):
                self.min_delay_var.set(str(Config.MIN_KEYWORD_DELAY))
            if hasattr(self, 'max_delay_var'):
                self.max_delay_var.set(str(Config.MAX_KEYWORD_DELAY))

            if hasattr(self, 'domain_entry') and hasattr(self, 'country_var') and hasattr(self, 'language_var'):
                # Cargar otras opciones si ya fueron configuradas
                self.country_var.set(Config.DEFAULT_COUNTRY)
                self.language_var.set(Config.DEFAULT_LANGUAGE)
                self.update_pages_label(Config.PAGES_TO_SCRAPE)

        except Exception as e:
            # Si hay error cargando config, iniciar con valores vacíos
            self.log_message(f"ℹ️ Configuración inicial: {e}")

    def setup_gui(self):
        """Configura la interfaz gráfica principal"""
        # Crear pestañas principales
        self.tabview = ctk.CTkTabview(self.root)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Crear pestañas
        self.tab_google_api = self.tabview.add("🔐 Google API")
        self.tab_config = self.tabview.add("⚙️ Configuración")
        self.tab_keywords = self.tabview.add("🔑 Keywords")
        self.tab_scraping = self.tabview.add("🚀 Scraping")
        self.tab_results = self.tabview.add("📊 Resultados")
        self.tab_analysis = self.tabview.add("📈 Análisis")
        
        # Configurar cada pestaña
        self.setup_google_api_tab()
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
        
        # Columna derecha - Delays
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

        # Información sobre Google API
        info_frame = ctk.CTkFrame(right_frame)
        info_frame.pack(fill="x", padx=10, pady=10)
        ctk.CTkLabel(info_frame, text="ℹ️ Información del sistema:", font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        info_text = """• Este scraper funciona únicamente con Google API
• Configura las credenciales en la pestaña "🔐 Google API"
• Sin necesidad de proxies ni límites de IP""
"""
        ctk.CTkLabel(info_frame, text=info_text, wraplength=300, justify="left").pack(pady=(5, 0))
        
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
        
    # ========== MÉTODOS DE GOOGLE API ==========

    def setup_google_api_tab(self):
        """Configura la pestaña dedicada de Google API con instrucciones"""
        main_frame = ctk.CTkScrollableFrame(self.tab_google_api)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Título principal
        title_label = ctk.CTkLabel(main_frame, text="🔐 Configuración Google Custom Search API",
                                  font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack(pady=(0, 20))

        # Descripción principal
        description_text = """
                🌐 Este scraper SOLO FUNCIONA con Google Custom Search API
                No usa proxies ni scraping directo - utiliza la API oficial de Google

                💡 Ventajas:
                • Sin límites de IP
                • Mejor precisión
                • Cuotas actualizadas por Google
                • Más confiable"""
        desc_label = ctk.CTkLabel(main_frame, text=description_text,
                                 wraplength=600, justify="left",
                                 font=ctk.CTkFont(size=12))
        desc_label.pack(pady=(0, 30))

        # Paso 1: Crear cuenta en Google Cloud
        step1_frame = ctk.CTkFrame(main_frame)
        step1_frame.pack(fill="x", pady=(0, 20))
        ctk.CTkLabel(step1_frame, text="📋 PASO 1: Crear cuenta Google Cloud",
                    font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", pady=(10, 5))

        step1_text = """• Ve a https://console.cloud.google.com/
        • Crea una cuenta o selecciona un proyecto existente
        • Si es nuevo, necesitarás una tarjeta de crédito (no se cobra sin activar facturación)"""

        step1_label = ctk.CTkLabel(step1_frame, text=step1_text, justify="left")
        step1_label.pack(pady=(0, 10))

        # Botón para abrir enlace
        open_console_btn = ctk.CTkButton(step1_frame, text="🌐 Abrir Google Cloud Console",
                                       command=lambda: self.open_website("https://console.cloud.google.com/"),
                                       fg_color="blue")
        open_console_btn.pack()

        # Paso 2: Habilitar API
        step2_frame = ctk.CTkFrame(main_frame)
        step2_frame.pack(fill="x", pady=(0, 20))
        ctk.CTkLabel(step2_frame, text="🔧 PASO 2: Habilitar Custom Search API",
                    font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", pady=(10, 5))

        step2_text = """• En Google Cloud Console → APIs y servicios → Biblioteca
        • Busca "Custom Search JSON API"
        • Click en "Habilitar" (Enable)"""

        step2_label = ctk.CTkLabel(step2_frame, text=step2_text, justify="left")
        step2_label.pack(pady=(0, 10))

        # Paso 3: Crear credenciales
        step3_frame = ctk.CTkFrame(main_frame)
        step3_frame.pack(fill="x", pady=(0, 20))
        ctk.CTkLabel(step3_frame, text="🔑 PASO 3: Obtener API Key",
                    font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", pady=(10, 5))

        step3_text = """• APIs y servicios → Credenciales
        • "Crear credenciales" → "Clave de API"
        • Copia la clave generada (formato: AIzaSy...)
        • ¡IMPORTANTE! Mantén esta clave segura"""

        step3_label = ctk.CTkLabel(step3_frame, text=step3_text, justify="left")
        step3_label.pack(pady=(0, 10))

        # Paso 4: Crear Custom Search Engine
        step4_frame = ctk.CTkFrame(main_frame)
        step4_frame.pack(fill="x", pady=(0, 20))
        ctk.CTkLabel(step4_frame, text="🚀 PASO 4: Crear Search Engine Personalizado",
                    font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", pady=(10, 5))

        step4_text = """• Ve a https://cse.google.com/
        • "New search engine" (Motor de búsqueda nuevo)
        • Sitios web para buscar: deja vacío para buscar en toda la web
        • Nombre: algo descriptivo como "Position Scraper"
        • Crea el motor y copia el "Search engine ID" (al final de la URL)"""

        step4_label = ctk.CTkLabel(step4_frame, text=step4_text, justify="left")
        step4_label.pack(pady=(0, 10))

        # Botón para abrir Custom Search
        open_cse_btn = ctk.CTkButton(step4_frame, text="🔍 Abrir Custom Search Engine",
                                   command=lambda: self.open_website("https://cse.google.com/"),
                                   fg_color="green")
        open_cse_btn.pack()

        # CONFIGURACIÓN PRINCIPAL
        config_title = ctk.CTkLabel(main_frame, text="🎯 CONFIGURAR TU SCRAPER",
                                  font=ctk.CTkFont(size=18, weight="bold"))
        config_title.pack(pady=(20, 15))

        # Formulario de configuración
        form_frame = ctk.CTkFrame(main_frame)
        form_frame.pack(fill="x", pady=(0, 20))

        # Campo API Key
        api_key_frame = ctk.CTkFrame(form_frame)
        api_key_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(api_key_frame, text="🔑 Google API Key:",
                    font=ctk.CTkFont(weight="bold")).pack(anchor="w")

        api_key_inner = ctk.CTkFrame(api_key_frame)
        api_key_inner.pack(fill="x", pady=5)

        self.api_key_var = ctk.StringVar()
        api_key_entry = ctk.CTkEntry(api_key_inner, textvariable=self.api_key_var,
                                   show="*", width=400, placeholder_text="Ingresa tu API Key...")
        api_key_entry.pack(side="left", padx=(0, 10))

        show_key_btn = ctk.CTkButton(api_key_inner, text="👁️ Mostrar", width=80,
                                    command=self.toggle_api_key_visibility)
        show_key_btn.pack(side="left")

        # Campo Search Engine ID
        se_id_frame = ctk.CTkFrame(form_frame)
        se_id_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(se_id_frame, text="🔍 Search Engine ID:",
                    font=ctk.CTkFont(weight="bold")).pack(anchor="w")

        se_id_inner = ctk.CTkFrame(se_id_frame)
        se_id_inner.pack(fill="x", pady=5)

        self.search_engine_id_var = ctk.StringVar()
        se_id_entry = ctk.CTkEntry(se_id_inner, textvariable=self.search_engine_id_var,
                                 width=400, placeholder_text="Ingresa tu Search Engine ID...")
        se_id_entry.pack(side="left", padx=(0, 10))

        # Botones de acción
        buttons_frame = ctk.CTkFrame(form_frame)
        buttons_frame.pack(fill="x", padx=20, pady=10)

        validate_btn = ctk.CTkButton(buttons_frame, text="✅ Validar Credenciales",
                                   command=self.validate_google_api, fg_color="green",
                                   width=150)
        validate_btn.pack(side="left", padx=(0, 20))

        save_btn = ctk.CTkButton(buttons_frame, text="💾 Guardar Configuración",
                               command=self.save_google_config, fg_color="blue",
                               width=150)
        save_btn.pack(side="left")

        # Información de cuotas
        quota_frame = ctk.CTkFrame(main_frame, fg_color="gray20")
        quota_frame.pack(fill="x", pady=(20, 0))

        quota_title = ctk.CTkLabel(quota_frame, text="📊 INFORMACIÓN DE CUOTAS GOOGLE",
                                 font=ctk.CTkFont(size=16, weight="bold"))
        quota_title.pack(pady=(15, 10))

        quota_text = """🚨 CUOTAS Y LÍMITES:

        • 100 consultas diarias GRATIS
        • $5 por cada 1000 consultas adicionales (cerca de $5 por keyword completa)
        • No hay límites de IP
        • Solo se cobra cuando superas el límite gratuito

        💡 RECOMENDACIONES:
        • Usa la cuenta gratuita para pruebas
        • Solo keywords importantes paguen
        • Monitorea tu uso en Google Cloud Console"""

        quota_label = ctk.CTkLabel(quota_frame, text=quota_text, justify="left",
                                 wraplength=600, font=ctk.CTkFont(size=11))
        quota_label.pack(pady=(0, 15))

    def open_website(self, url):
        """Abre una URL en el navegador por defecto"""
        try:
            import webbrowser
            webbrowser.open(url)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el navegador: {e}")

    def toggle_api_key_visibility(self):
        """Alterna visibilidad/mascarado de la API Key"""
        # Esta es una simplificación, en producción necesitarías acceder al widget real
        messagebox.showinfo("Nota", "La clave se muestra al escribirla normalmente")

    def save_google_config(self):
        """Guarda la configuración de Google API"""
        api_key = self.api_key_var.get().strip()
        search_engine_id = self.search_engine_id_var.get().strip()

        if not api_key:
            messagebox.showwarning("Error", "Debes ingresar la API Key")
            return

        if not search_engine_id:
            messagebox.showwarning("Error", "Debes ingresar el Search Engine ID")
            return

        # Validar formato básico
        if not api_key.startswith("AIza"):
            messagebox.showwarning("Error", "La API Key debe comenzar con 'AIza'")
            return

        # Intentar validar con Google
        if self.validate_google_api():
            # Guardar configuración si la validación pasa
            self.save_config()
            messagebox.showinfo("Éxito",
                              "✅ Configuración de Google API guardada correctamente!\n\nTu scraper está listo para funcionar.")

    # ========== MÉTODOS DE CONFIGURACIÓN ==========

    def toggle_scraping_mode(self):
        """Cambia entre modo scraping directo y API de Google"""
        use_api = self.use_api_var.get()

        if use_api:
            self.log_message("🌐 Cambiado a modo Google API - Sin límites de IP")
            # Ocultar/deshabilitar sección de proxies cuando se usa API
            self.proxies_text.configure(state="disabled")
            self.test_proxies_button.configure(state="disabled")
        else:
            self.log_message("🔧 Cambiado a modo scraping directo - Con proxies")
            # Habilitar sección de proxies
            self.test_proxies_button.configure(state="normal")

    def validate_google_api(self):
        """Valida las credenciales de Google API"""
        api_key = self.api_key_var.get().strip()
        search_engine_id = self.search_engine_id_var.get().strip()

        if not api_key or not search_engine_id:
            messagebox.showwarning("Advertencia", "Ingresa tanto la API Key como el Search Engine ID")
            return False

        try:
            import requests
            # Probar una búsqueda simple
            url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={search_engine_id}&q=test"
            response = requests.get(url, timeout=10)

            if response.status_code == 200:
                messagebox.showinfo("Éxito", "✅ Credenciales válidas - API de Google configurada correctamente")
                self.log_message("✅ API de Google validada correctamente")
                return True
            else:
                error_data = response.json()
                error_msg = error_data.get('error', {}).get('message', 'Error desconocido')
                messagebox.showerror("Error de API", f"Error de validación: {error_msg}")
                return False

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error de conexión", f"Error conectando con Google API: {e}")
            return False

    def save_config(self):
        """Guarda la configuración actual en .env"""
        try:
            # Leer .env existente
            env_file = os.path.join(os.path.dirname(__file__), '..', 'config', '.env')

            env_lines = []
            if os.path.exists(env_file):
                with open(env_file, 'r', encoding='utf-8') as f:
                    env_lines = f.readlines()

            # Actualizar/crear variables de Google API
            api_key = self.api_key_var.get().strip()
            search_engine_id = self.search_engine_id_var.get().strip()

            # Buscar y reemplazar líneas existentes
            updated_lines = []
            google_vars = {
                'GOOGLE_API_KEY': api_key,
                'GOOGLE_SEARCH_ENGINE_ID': search_engine_id,
                'USE_GOOGLE_API': 'true' if self.use_api_var.get() else 'false'
            }

            vars_found = {key: False for key in google_vars}

            for line in env_lines:
                line_strip = line.strip()
                if not line_strip or line_strip.startswith('#'):
                    updated_lines.append(line)
                    continue

                var_name = line_strip.split('=')[0]
                if var_name in google_vars:
                    updated_lines.append(f'{var_name}={google_vars[var_name]}\n')
                    vars_found[var_name] = True
                else:
                    updated_lines.append(line)

            # Agregar variables no encontradas
            for var_name, value in google_vars.items():
                if not vars_found[var_name]:
                    updated_lines.append(f'{var_name}={value}\n')

            # Guardar archivo .env
            with open(env_file, 'w', encoding='utf-8') as f:
                f.writelines(updated_lines)

            # Validar API si está habilitada
            if self.use_api_var.get():
                self.validate_google_api()

            messagebox.showinfo("Éxito", "Configuración guardada en config/.env")
            self.log_message("💾 Configuración guardada correctamente")

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
