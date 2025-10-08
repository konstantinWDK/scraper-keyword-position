#!/usr/bin/env python3
"""
💎 Interfaz Ultra Moderna para Keyword Position Scraper 2025
🚀 GUI premium usando CustomTkinter con diseño avanzado

Características mejoradas:
• 🎨 Diseño uniforme con colores oscuros profesionales
• 📊 Tablas de resultados con altura máxima y mejor UX
• 🔍 Funciones avanzadas de manipulación de keywords
• 🏆 Interface visualización similar a Neil Patel
• ⚡ Más opciones y controles interactivos
• 📈 Información relevante siempre visible
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import customtkinter as ctk
import threading
import time
import json
import logging
import os
import sys
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')  # Configurar backend antes de importar pyplot
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
from PIL import Image
import re
from collections import Counter

# Añadir directorio padre al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import Config, config
from stealth_scraper import StealthSerpScraper

# Configurar tema ultra moderno
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

# 🎨 Paleta de colores profesionales oscuros
COLORS = {
    'primary': '#1e1e2e',      # Negro azulado profundo
    'secondary': '#2a2a3c',    # Gris oscuro
    'accent': '#7c3aed',       # Púrpura moderno
    'success': '#10b981',      # Verde esmeralda
    'warning': '#f59e0b',      # Ámbar
    'error': '#ef4444',        # Rojo coral
    'info': '#3b82f6',         # Azul cielo
    'surface': '#313244',      # Gris medio
    'text_primary': '#ffffff',
    'text_secondary': '#a1a1aa',
    'text_muted': '#71717a',
    'border': '#404040'
}

class KeywordScraperGUI:
    def run(self):
        """Inicia el loop principal de la interfaz gráfica"""
        self.root.mainloop()

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
        self.processed_keywords = []  # Keywords procesadas que pueden usarse para scraping
        self.keyword_analysis_data = {}  # Datos de análisis de keywords

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

        # Variables para keywords relacionadas
        self.related_keyword_entry = None
        self.related_text = None
        self.related_count_label = None
        self.add_to_keywords_button = None
        self.related_suggestions = []

        # Variables de mi ranking
        self.my_domain_entry = None
        self.my_keywords_base_text = None
        self.my_ranking_results_tree = None
        self.my_ranking_button = None
        self.my_ranking_status = None
        self.suggestion_count_var = None

        # Área principal de keywords para scraping
        self.main_keywords_text = None

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

        self.tab_google_api = self.tabview.add("🔐 Google API")
        self.tab_config = self.tabview.add("⚙️ Configuración")
        self.tab_keywords = self.tabview.add("🔑 Keywords")
        self.tab_my_rankings = self.tabview.add("🏆 Mi Ranking")
        self.tab_scraping = self.tabview.add("🚀 Scraping")
        self.tab_results = self.tabview.add("📊 Resultados")
        self.tab_reports = self.tabview.add("📋 Informes")
        self.tab_analysis = self.tabview.add("📈 Análisis")

        # Configurar cada pestaña
        self.setup_google_api_tab()
        self.setup_config_tab()
        self.setup_keywords_tab()
        self.setup_my_rankings_tab()
        self.setup_scraping_tab()
        self.setup_results_tab()
        self.setup_reports_tab()
        self.setup_analysis_tab()

    def log_message(self, message, level="info"):
        """Añade mensaje a los logs con formato mejorado"""
        self.logs_text.configure(state="normal")

        timestamp = time.strftime("%H:%M:%S")

        # Añadir emojis y colores según nivel
        formatted_message = f"[{timestamp}] {message}"

        # Insertar con colores si es posible
        self.logs_text.insert("end", formatted_message + "\n")

        # Scroll al final
        self.logs_text.see("end")
        self.logs_text.configure(state="disabled")

        # También mostrar en consola para debugging
        print(f"[{timestamp}] {message}")

    def update_progress(self, current, total, message=""):
        """Actualiza la barra de progreso"""
        progress = current / total if total > 0 else 0
        self.progress_bar.set(progress)
        self.progress_label.configure(text=f"{current}/{total} - {message}")

    def update_keywords_count(self):
        """Actualiza el contador de keywords"""
        # Usar el sistema unificado de keywords
        current_keywords = self.get_current_keywords()
        self.keywords_list = current_keywords

        if hasattr(self, 'keywords_count_label'):
            self.keywords_count_label.configure(text=str(len(current_keywords)))

    def update_cost_display(self):
        """Actualiza la visualización de costos"""
        # Calcular consultas gratuitas restantes
        free_remaining = max(0, 100 - self.today_consults)
        free_cost = " - GRATIS 💚"

        # Calcular consultas pagas (solo se paga después del límite gratuito)
        paid_consults = max(0, self.today_consults - 100)
        paid_cost = self.total_cost - (100 * 0.005) if paid_consults > 0 else 0

        # Actualizar etiquetas
        self.free_consults_label.configure(text=f"Consultas gratis (100/día restantes): {free_remaining}{free_cost}")
        self.paid_consults_label.configure(text=f"Consultas pagas: ${paid_cost:.2f}")
        self.total_cost_label.configure(text=f"💸 Costo total: ${self.total_cost:.2f}", font=ctk.CTkFont(weight="bold"))

    # ========== MÉTODOS DE CONFIGURACIÓN DE PESTAÑAS ==========

    def setup_google_api_tab(self):
        """Configura la pestaña dedicada de Google API con instrucciones"""
        main_frame = ctk.CTkScrollableFrame(self.tab_google_api)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Título principal
        title_label = ctk.CTkLabel(main_frame, text="🔐 Configuración Google Custom Search API",
                                  font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack(pady=(0, 20))

        # Campos de configuración
        config_frame = ctk.CTkFrame(main_frame)
        config_frame.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(config_frame, text="🔑 Google API Key:", font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        self.api_key_var = ctk.StringVar()
        api_key_entry = ctk.CTkEntry(config_frame, textvariable=self.api_key_var, show="*", width=400)
        api_key_entry.pack(fill="x", pady=(5, 10))

        ctk.CTkLabel(config_frame, text="🔍 Search Engine ID:", font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        self.search_engine_id_var = ctk.StringVar()
        se_id_entry = ctk.CTkEntry(config_frame, textvariable=self.search_engine_id_var, width=400)
        se_id_entry.pack(fill="x", pady=(5, 10))

        ctk.CTkButton(config_frame, text="💾 Guardar Configuración", command=self.save_google_config).pack(pady=10)

    def setup_config_tab(self):
        """Configura la pestaña de configuración"""
        main_frame = ctk.CTkFrame(self.tab_config)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(main_frame, text="⚙️ Configuración del Scraper", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10)

        # Dominio objetivo
        domain_frame = ctk.CTkFrame(main_frame)
        domain_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(domain_frame, text="Dominio objetivo:").pack(anchor="w")
        self.domain_entry = ctk.CTkEntry(domain_frame, placeholder_text="ejemplo.com")
        self.domain_entry.pack(fill="x", pady=(5, 0))

        # Páginas a scrapear
        pages_frame = ctk.CTkFrame(main_frame)
        pages_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(pages_frame, text="Páginas a scrapear:").pack(anchor="w")
        self.pages_var = ctk.DoubleVar(value=1.0)
        pages_slider = ctk.CTkSlider(pages_frame, from_=1, to=10, number_of_steps=9, variable=self.pages_var, command=self.update_pages_label)
        pages_slider.pack(fill="x", pady=(5, 0))
        self.pages_label = ctk.CTkLabel(pages_frame, text="1 página")
        self.pages_label.pack()

        # País e idioma
        geo_frame = ctk.CTkFrame(main_frame)
        geo_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(geo_frame, text="País:").pack(side="left", padx=(0, 10))
        self.country_var = ctk.StringVar(value="US")
        country_combo = ctk.CTkComboBox(geo_frame, values=["US", "ES", "FR", "DE", "IT", "UK", "BR", "MX"], variable=self.country_var, width=100)
        country_combo.pack(side="left", padx=(0, 20))
        ctk.CTkLabel(geo_frame, text="Idioma:").pack(side="left", padx=(0, 10))
        self.language_var = ctk.StringVar(value="en")
        language_combo = ctk.CTkComboBox(geo_frame, values=["en", "es", "fr", "de", "it", "pt", "ru"], variable=self.language_var, width=100)
        language_combo.pack(side="left")

        # Delays
        delays_frame = ctk.CTkFrame(main_frame)
        delays_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(delays_frame, text="Delays (segundos):", font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        min_delay_frame = ctk.CTkFrame(delays_frame)
        min_delay_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(min_delay_frame, text="Mínimo:").pack(side="left")
        self.min_delay_var = ctk.StringVar(value="5")
        min_delay_entry = ctk.CTkEntry(min_delay_frame, textvariable=self.min_delay_var, width=60)
        min_delay_entry.pack(side="right")

        max_delay_frame = ctk.CTkFrame(delays_frame)
        max_delay_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(max_delay_frame, text="Máximo:").pack(side="left")
        self.max_delay_var = ctk.StringVar(value="15")
        max_delay_entry = ctk.CTkEntry(max_delay_frame, textvariable=self.max_delay_var, width=60)
        max_delay_entry.pack(side="right")

    def setup_keywords_tab(self):
        """Configura la pestaña de keywords"""
        main_frame = ctk.CTkFrame(self.tab_keywords)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(main_frame, text="🔑 Gestión de Keywords", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10)

        # Área de edición de keywords
        keywords_frame = ctk.CTkFrame(main_frame)
        keywords_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(keywords_frame, text="Keywords (una por línea):", font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        self.main_keywords_text = ctk.CTkTextbox(keywords_frame, height=200, font=ctk.CTkFont(family="Consolas", size=11))
        self.main_keywords_text.pack(fill="x", pady=(5, 0))

        # Contador de keywords
        self.keywords_count_label = ctk.CTkLabel(main_frame, text="0 keywords")
        self.keywords_count_label.pack(pady=5)

        # Botones de acción
        buttons_frame = ctk.CTkFrame(main_frame)
        buttons_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(buttons_frame, text="📁 Cargar Archivo", command=self.load_keywords_file).pack(side="left", padx=5)
        ctk.CTkButton(buttons_frame, text="🧹 Limpiar Duplicados", command=self.deduplicate_keywords).pack(side="left", padx=5)
        ctk.CTkButton(buttons_frame, text="💾 Guardar", command=self.save_keywords).pack(side="left", padx=5)

        # Área de keywords relacionadas
        related_frame = ctk.CTkFrame(main_frame)
        related_frame.pack(fill="both", expand=True, padx=10, pady=(10, 0))

        ctk.CTkLabel(related_frame, text="🎯 Keywords Relacionadas", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(10, 5))

        # Campo de entrada para keyword base
        input_frame = ctk.CTkFrame(related_frame)
        input_frame.pack(fill="x", pady=(0, 5))
        self.related_keyword_entry = ctk.CTkEntry(input_frame, placeholder_text="Ingresa keyword principal...")
        self.related_keyword_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        ctk.CTkButton(input_frame, text="🔍 Buscar", command=self.find_related_keywords).pack(side="right")

        # Área de resultados de keywords relacionadas
        self.related_text = ctk.CTkTextbox(related_frame, height=150, wrap="word")
        self.related_text.pack(fill="both", expand=True, pady=(5, 0))
        self.related_text.configure(state="disabled")

        # Contador y botón de añadir
        actions_frame = ctk.CTkFrame(related_frame)
        actions_frame.pack(fill="x", pady=(5, 10))
        self.related_count_label = ctk.CTkLabel(actions_frame, text="(0 sugerencias)")
        self.related_count_label.pack(side="left")
        self.add_to_keywords_button = ctk.CTkButton(actions_frame, text="➕ Añadir a Lista", state="disabled", command=self.add_related_to_keywords)
        self.add_to_keywords_button.pack(side="right")

    def setup_my_rankings_tab(self):
        """Configura la pestaña de análisis 'Mi Ranking' - Keywords donde posiciona mi dominio"""
        main_frame = ctk.CTkFrame(self.tab_my_rankings)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(main_frame, text="🏆 Mi Ranking - Keywords de mi dominio", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=(10, 20))

        # Frame de entrada
        input_frame = ctk.CTkFrame(main_frame)
        input_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(input_frame, text="Mi dominio:", font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        self.my_domain_entry = ctk.CTkEntry(input_frame, placeholder_text="midominio.com")
        self.my_domain_entry.pack(fill="x", pady=(5, 10))

        # Frame para keywords base
        keywords_frame = ctk.CTkFrame(main_frame)
        keywords_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(keywords_frame, text="Keywords base (una por línea):", font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        self.my_keywords_base_text = ctk.CTkTextbox(keywords_frame, height=120, font=ctk.CTkFont(family="Consolas", size=11))
        self.my_keywords_base_text.pack(fill="x", pady=(5, 10))

        # Frame de configuración de sugerencias
        config_frame = ctk.CTkFrame(main_frame)
        config_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(config_frame, text="Número de sugerencias por keyword base:", font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        self.suggestion_count_var = ctk.StringVar(value="5")
        suggestion_count_entry = ctk.CTkEntry(config_frame, textvariable=self.suggestion_count_var, width=80)
        suggestion_count_entry.pack(anchor="w", pady=(5, 0))

        # Información
        info_text = "ℹ️ Introduce tu dominio y algunas keywords base. El scraper generará sugerencias con Google Suggest para cada keyword base y buscará dónde posiciona tu dominio en todas esas keywords."
        ctk.CTkLabel(main_frame, text=info_text, justify="left", wraplength=600).pack(pady=(5, 15))

        # Botón de análisis
        self.my_ranking_button = ctk.CTkButton(main_frame, text="🏆 Analizar Mi Ranking", command=self.analyze_my_rankings, fg_color="#FF6B35", height=40)
        self.my_ranking_button.pack(pady=(0, 15))

        # Estado
        self.my_ranking_status = ctk.CTkLabel(main_frame, text="Listo para analizar")
        self.my_ranking_status.pack(pady=(0, 15))

        # Tabla de resultados
        table_frame = ctk.CTkFrame(main_frame)
        table_frame.pack(fill="both", expand=True, padx=10, pady=(5, 10))

        # Crear treeview para mis rankings
        columns = ("keyword", "position", "title", "url", "suggested_from")
        self.my_ranking_results_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)

        # Configurar columnas
        self.my_ranking_results_tree.heading("keyword", text="Keyword")
        self.my_ranking_results_tree.heading("position", text="Posición")
        self.my_ranking_results_tree.heading("title", text="Título")
        self.my_ranking_results_tree.heading("url", text="URL")
        self.my_ranking_results_tree.heading("suggested_from", text="Basado en")

        self.my_ranking_results_tree.column("keyword", width=150)
        self.my_ranking_results_tree.column("position", width=80, anchor="center")
        self.my_ranking_results_tree.column("title", width=200)
        self.my_ranking_results_tree.column("url", width=250)
        self.my_ranking_results_tree.column("suggested_from", width=120)

        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.my_ranking_results_tree.yview)
        self.my_ranking_results_tree.configure(yscrollcommand=scrollbar.set)
        self.my_ranking_results_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def setup_scraping_tab(self):
        """Configura la pestaña de scraping con interfaz mejorada"""
        main_frame = ctk.CTkFrame(self.tab_scraping)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Título principal con información de estado
        header_frame = ctk.CTkFrame(main_frame)
        header_frame.pack(fill="x", padx=10, pady=(10, 5))

        # Título y estado
        title_frame = ctk.CTkFrame(header_frame)
        title_frame.pack(fill="x", pady=(0, 5))

        title_label = ctk.CTkLabel(title_frame, text="🚀 Scraping en Tiempo Real", font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(side="left")

        # Indicador de estado
        self.scraping_status_label = ctk.CTkLabel(title_frame, text="⏸️ Listo para comenzar", font=ctk.CTkFont(size=14, weight="bold"), text_color="orange")
        self.scraping_status_label.pack(side="right")

        # Información de configuración
        config_info = f"📊 Keywords: {len(self.keywords_list)} | 🎯 Dominio: {self.domain_entry.get() or 'Todos'} | 🌍 País: {self.country_var.get()} | 📄 Páginas: {int(self.pages_var.get())}"
        self.config_info_label = ctk.CTkLabel(header_frame, text=config_info, font=ctk.CTkFont(size=11))
        self.config_info_label.pack(anchor="w")

        # Inicializar variables de costos que usa update_cost_display
        self.total_consults = 0
        self.total_cost = 0.0
        self.today_consults = 0

        # Panel de costos mejorado
        costs_panel = ctk.CTkFrame(main_frame)
        costs_panel.pack(fill="x", padx=10, pady=(0, 10))

        ctk.CTkLabel(costs_panel, text="💰 Calculadora de Costos Google API", font=ctk.CTkFont(weight="bold")).pack(anchor="w", pady=(10,5))

        # Costos en filas separadas para mejor visualización
        costs_grid = ctk.CTkFrame(costs_panel)
        costs_grid.pack(fill="x", pady=(0, 10))

        self.free_consults_label = ctk.CTkLabel(costs_grid, text="🟢 Consultas GRATIS (100/día): 100 restantes", font=ctk.CTkFont(size=12))
        self.free_consults_label.pack(anchor="w", pady=(0, 5))

        self.paid_consults_label = ctk.CTkLabel(costs_grid, text="🔴 Consultas PAGAS: $0.00", font=ctk.CTkFont(size=12))
        self.paid_consults_label.pack(anchor="w", pady=(0, 5))

        self.total_cost_label = ctk.CTkLabel(costs_grid, text="💸 Costo total estimado: $0.00", font=ctk.CTkFont(size=14, weight="bold"))
        self.total_cost_label.pack(anchor="w")

        # Información sobre cuotas
        quota_info = ctk.CTkLabel(costs_panel, text="ℹ️ 100 consultas gratis por día | $5 por cada 1000 consultas adicionales", font=ctk.CTkFont(size=10), text_color="gray")
        quota_info.pack(anchor="w", pady=(5, 10))

        # Botones de control mejorados
        buttons_frame = ctk.CTkFrame(main_frame)
        buttons_frame.pack(fill="x", padx=10, pady=(0, 10))

        self.start_button = ctk.CTkButton(buttons_frame, text="🚀 Iniciar Scraping", command=self.start_scraping, fg_color="green", hover_color="dark green", height=40, font=ctk.CTkFont(size=12, weight="bold"))
        self.start_button.pack(side="left", padx=(0, 5), fill="x", expand=True)

        self.stop_button = ctk.CTkButton(buttons_frame, text="⏹️ Detener", command=self.stop_scraping, fg_color="red", hover_color="dark red", height=40, font=ctk.CTkFont(size=12, weight="bold"), state="disabled")
        self.stop_button.pack(side="left")

        # Barra de progreso mejorada
        progress_frame = ctk.CTkFrame(main_frame)
        progress_frame.pack(fill="x", padx=10, pady=(0, 5))

        ctk.CTkLabel(progress_frame, text="📈 Progreso del Scraping:", font=ctk.CTkFont(weight="bold")).pack(anchor="w")

        self.progress_bar = ctk.CTkProgressBar(progress_frame, height=20)
        self.progress_bar.pack(fill="x", pady=(5, 0))
        self.progress_bar.set(0)

        # Información detallada del progreso
        progress_info_frame = ctk.CTkFrame(progress_frame)
        progress_info_frame.pack(fill="x", pady=(5, 0))

        self.progress_label = ctk.CTkLabel(progress_info_frame, text="⏸️ Esperando iniciar scraping...", font=ctk.CTkFont(size=12))
        self.progress_label.pack(side="left")

        # Estadísticas en tiempo real
        self.scraping_stats_label = ctk.CTkLabel(progress_info_frame, text="Keywords: 0 | Procesadas: 0 | Restantes: 0", font=ctk.CTkFont(size=10), text_color="gray")
        self.scraping_stats_label.pack(side="right")

        # Logs en tiempo real
        logs_frame = ctk.CTkFrame(main_frame)
        logs_frame.pack(fill="both", expand=True, padx=10, pady=5)

        ctk.CTkLabel(logs_frame, text="Logs de Actividad:").pack(anchor="w")
        self.logs_text = ctk.CTkTextbox(logs_frame, font=ctk.CTkFont(family="Consolas", size=11))
        self.logs_text.pack(fill="both", expand=True, pady=5)
        self.logs_text.configure(state="disabled")

    def setup_results_tab(self):
        """Configura la pestaña de resultados con bloques de estadísticas y mejor UI"""
        main_frame = ctk.CTkFrame(self.tab_results)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(main_frame, text="📊 RESULTADOS E INFORMES", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=(10, 20))

        # Información de sesión actual
        session_info = ctk.CTkLabel(main_frame, text="Sesión actual: Sin resultados", font=ctk.CTkFont(size=12))
        session_info.pack(anchor="w", pady=(0, 10))
        self.session_info_label = session_info

        # Tabla de resultados detallada
        table_section = ctk.CTkFrame(main_frame)
        table_section.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        table_header = ctk.CTkFrame(table_section)
        table_header.pack(fill="x", padx=10, pady=(10, 5))

        ctk.CTkLabel(table_header, text="📋 TABLA DETALLADA DE RESULTADOS", font=ctk.CTkFont(size=16, weight="bold")).pack(side="left")

        # Tabla con scrollbar
        table_frame = ctk.CTkFrame(table_section)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Crear treeview para mostrar resultados con ordenamiento
        columns = ("keyword", "position", "title", "domain", "page")
        self.results_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)

        # Configurar columnas
        self.results_tree.heading("keyword", text="Keyword")
        self.results_tree.heading("position", text="Posición")
        self.results_tree.heading("title", text="Título")
        self.results_tree.heading("domain", text="Dominio")
        self.results_tree.heading("page", text="Página")

        self.results_tree.column("keyword", width=180)
        self.results_tree.column("position", width=70, anchor="center")
        self.results_tree.column("title", width=280)
        self.results_tree.column("domain", width=130)
        self.results_tree.column("page", width=50, anchor="center")

        # Scrollbar para la tabla
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=scrollbar.set)

        self.results_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Mensaje de estado inferior
        status_frame = ctk.CTkFrame(main_frame)
        status_frame.pack(fill="x", padx=10, pady=(0, 10))

        self.results_status_label = ctk.CTkLabel(status_frame, text="⏳ Esperando resultados de scraping...", font=ctk.CTkFont(size=11))
        self.results_status_label.pack(pady=5)

    def setup_reports_tab(self):
        """Configura la nueva pestaña de informes históricos"""
        main_frame = ctk.CTkFrame(self.tab_reports)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(main_frame, text="📋 GESTIÓN DE INFORMES E HISTORIAL", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(20, 5))

        ctk.CTkLabel(main_frame, text="Accede y administra todos tus informes de scraping generados", font=ctk.CTkFont(size=12)).pack(pady=(0, 20))

        # Área para lista de reportes (por ahora solo placeholder)
        reports_frame = ctk.CTkScrollableFrame(main_frame, height=300)
        reports_frame.pack(fill="both", expand=True, padx=10, pady=5)

        ctk.CTkLabel(reports_frame, text="📁 No hay informes guardados aún", font=ctk.CTkFont(size=14)).pack(pady=50)

        # Botones de acción
        actions_frame = ctk.CTkFrame(main_frame)
        actions_frame.pack(fill="x", padx=10, pady=(0, 10))

        ctk.CTkButton(actions_frame, text="🗂️ Abrir Carpeta Data", command=self.open_data_folder, fg_color=COLORS['info']).pack(side="left", padx=(0, 5))
        ctk.CTkButton(actions_frame, text="📊 Generar Reporte Consolidado", command=self.generate_consolidated_report, fg_color=COLORS['accent']).pack(side="left", padx=(0, 5))

    def setup_analysis_tab(self):
        """Configura la pestaña de análisis"""
        main_frame = ctk.CTkFrame(self.tab_analysis)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(main_frame, text="📈 Análisis Avanzado", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=(10, 20))

        ctk.CTkButton(main_frame, text="📊 Generar Análisis", command=self.generate_analysis).pack(pady=(0, 20))

        # Placeholder para gráficos
        self.chart_frame = ctk.CTkFrame(main_frame)
        self.chart_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Intentar configurar matplotlib, pero manejar error graciosamente
        self.matplotlib_available = False
        try:
            # Configurar matplotlib si está disponible
            self.fig, ((self.ax1, self.ax2), (self.ax3, self.ax4)) = plt.subplots(2, 2, figsize=(12, 8))
            self.fig.tight_layout(pad=3.0)
            self.canvas = plt.FigureCanvasTkAgg(self.fig, self.chart_frame)
            self.canvas.get_tk_widget().pack(fill="both", expand=True)
            self.matplotlib_available = True
        except Exception as e:
            # Si matplotlib falla, mostrar mensaje y ocultar frame
            self.chart_frame.pack_forget()
            self.chart_frame = ctk.CTkFrame(main_frame)
            self.chart_frame.pack(fill="both", expand=True, padx=10, pady=5)
            ctk.CTkLabel(self.chart_frame, text="📋 Los gráficos aparecerán aquí después de generar el análisis\n\n⚠️ NOTA: Para activar gráficos instala:\nsudo apt install python3-tk", justify="center").pack(expand=True)
            print(f"⚠️ Matplotlib no disponible: {e}")
            self.matplotlib_available = False

    # ========== MÉTODOS DE UTILIDAD ==========

    def update_pages_label(self, value):
        """Actualiza la etiqueta de páginas"""
        pages = int(float(value))
        self.pages_label.configure(text=f"{pages} página{'s' if pages > 1 else ''}")

    def get_current_keywords(self):
        """Obtiene las keywords actuales del editor principal"""
        if not self.main_keywords_text:
            return []
        text = self.main_keywords_text.get("1.0", "end-1c").strip()
        keywords = [k.strip() for k in text.split('\n') if k.strip() and not k.strip().startswith('#')]
        return keywords

    def open_data_folder(self):
        """Abre la carpeta data/ en el explorador de archivos"""
        try:
            data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)
            import subprocess
            import platform
            if platform.system() == "Windows":
                subprocess.run(["explorer", data_dir])
            elif platform.system() == "Darwin":
                subprocess.run(["open", data_dir])
            else:
                subprocess.run(["xdg-open", data_dir])
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir la carpeta:\n\n{str(e)}")

    # ========== MÉTODOS PRINCIPALES ==========

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

        if not api_key.startswith("AIza"):
            messagebox.showwarning("Error", "La API Key debe comenzar con 'AIza'")
            return

        # Intentar validar con Google
        if self.validate_google_api():
            self.save_config()
            messagebox.showinfo("Éxito", "✅ Configuración de Google API guardada correctamente!\n\nTu scraper está listo para funcionar.")

    def validate_google_api(self):
        """Valida las credenciales de Google API"""
        api_key = self.api_key_var.get().strip()
        search_engine_id = self.search_engine_id_var.get().strip()

        if not api_key or not search_engine_id:
            messagebox.showwarning("Advertencia", "Ingresa tanto la API Key como el Search Engine ID")
            return False

        try:
            import requests
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

            messagebox.showinfo("Éxito", "Configuración guardada en config/.env")
            self.log_message("💾 Configuración guardada correctamente")

        except Exception as e:
            messagebox.showerror("Error", f"Error guardando configuración: {e}")

    def generate_consolidated_report(self):
        """Genera un reporte consolidado con estadísticas generales"""
        try:
            messagebox.showinfo("Información", "Esta función estará disponible próximamente.\n\nPor ahora puedes trabajar con la pestaña de Scraping.")
        except Exception as e:
            messagebox.showerror("Error", f"Error generando reporte consolidado:\n\n{str(e)}")

    # ========== MÉTODOS PARA KEYWORDS ==========

    def load_keywords_file(self):
        """Carga keywords desde archivo al editor principal"""
        try:
            file_path = filedialog.askopenfilename(
                filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv"), ("JSON files", "*.json"), ("All files", "*.*")]
            )

            if file_path:
                keywords = []

                if file_path.endswith('.csv'):
                    try:
                        import pandas as pd
                        df = pd.read_csv(file_path)

                        possible_columns = ['keyword', 'keywords', 'kw', 'query', 'search_term']
                        keyword_col = None

                        for col in possible_columns:
                            if col in df.columns:
                                keyword_col = col
                                break

                        if keyword_col:
                            keywords = df[keyword_col].dropna().astype(str).tolist()
                        else:
                            keywords = [str(x) for x in df.iloc[:, 0].dropna().tolist()]

                    except Exception as e:
                        messagebox.showerror("Error", f"Error leyendo CSV: {e}")
                        return

                elif file_path.endswith('.json'):
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)

                        if isinstance(data, list):
                            keywords = [str(k) for k in data if k]
                        elif isinstance(data, dict):
                            possible_keys = ['keywords', 'data', 'queries', 'items']
                            for key in possible_keys:
                                if key in data and isinstance(data[key], list):
                                    keywords = [str(k) for k in data[key] if k]
                                    break

                            if not keywords:
                                keywords = [str(v) for v in data.values() if isinstance(v, (str, int, float))][:50]

                    except Exception as e:
                        messagebox.showerror("Error", f"Error leyendo JSON: {e}")
                        return

                else:
                    # Cargar desde archivo de texto plano
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                        if ',' in content and '\n' not in content:
                            keywords = [k.strip() for k in content.split(',') if k.strip()]
                        else:
                            keywords = [line.strip() for line in content.split('\n') if line.strip() and not line.strip().startswith('#')]

                # Filtrar y limpiar keywords
                processed_keywords = []
                ignored_lines = 0

                for kw in keywords:
                    clean_kw = kw.strip()
                    if clean_kw and len(clean_kw) >= 2:
                        processed_keywords.append(clean_kw)
                    else:
                        ignored_lines += 1

                if processed_keywords:
                    self.set_current_keywords(processed_keywords)
                    self.update_keywords_count()
                    messagebox.showinfo("Archivo Cargado",
                                      f"✅ Archivo cargado exitosamente!\n\n"
                                      f"📁 Archivo: {os.path.basename(file_path)}\n"
                                      f"📊 Keywords válidas: {len(processed_keywords)}\n"
                                      f"🚫 Líneas ignoradas: {ignored_lines}\n\n"
                                      f"Las keywords están listas para usar en Scraping.")

                    self.log_message(f"✅ Cargadas {len(processed_keywords)} keywords válidas desde {file_path}")

                else:
                    messagebox.showerror("Sin Keywords Válidas",
                                       f"No se encontraron keywords válidas en el archivo.\n\n"
                                       f"Se ignoraron {ignored_lines} líneas.\n\n"
                                       f"Asegúrate de que el archivo contenga keywords de al menos 2 caracteres.")

        except Exception as e:
            messagebox.showerror("Error", f"Error cargando archivo:\n\n{str(e)}")

    def set_current_keywords(self, keywords_list):
        """Establece keywords en el editor principal"""
        if not self.main_keywords_text or not keywords_list:
            return
        filtered_keywords = [k for k in keywords_list if k.strip()]
        self.main_keywords_text.delete("1.0", "end")
        self.main_keywords_text.insert("1.0", "\n".join(filtered_keywords))

    def deduplicate_keywords(self):
        """Elimina keywords duplicadas"""
        current_keywords = self.get_current_keywords()
        keywords_list = [k.strip() for k in current_keywords if k.strip()]

        unique_keywords = list(set(keywords_list))

        self.set_current_keywords(unique_keywords)
        self.update_keywords_count()

        removed = len(keywords_list) - len(unique_keywords)
        self.log_message(f"🧹 Eliminadas {removed} keywords duplicadas")

        if removed > 0:
            messagebox.showinfo("Duplicados Eliminados", f"✅ Se eliminaron {removed} keywords duplicadas")
        else:
            messagebox.showinfo("Sin Cambios", "No se encontraron keywords duplicadas")

    def save_keywords(self):
        """Guarda keywords en archivo"""
        try:
            current_keywords = self.get_current_keywords()

            if not current_keywords:
                messagebox.showwarning("Advertencia", "No hay keywords para guardar")
                return

            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )

            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write("\n".join(current_keywords))

                messagebox.showinfo("Éxito", f"Keywords guardadas en {file_path}")
                self.log_message(f"💾 Keywords guardadas en {file_path}")

        except Exception as e:
            messagebox.showerror("Error", f"Error guardando keywords: {e}")

    # ========== MÉTODOS PARA SCRAPING ==========

    def start_scraping(self):
        """Inicia el proceso de scraping con mejor indicadores visuales"""
        if not self.keywords_list:
            messagebox.showwarning("Advertencia", "No hay keywords para scrapear")
            return

        # Validar que tengamos credenciales configuradas
        if not self.api_key_var.get().strip() or not self.search_engine_id_var.get().strip():
            messagebox.showwarning("Error", "Configura tus credenciales de Google API primero\n\nVe a la pestaña '🔐 Google API'")
            return

        # Actualizar configuración
        self.update_config_info()

        # Cambiar estado de interfaz
        self.scraping_status_label.configure(text="🚀 Iniciando...", text_color="green")
        self.progress_label.configure(text="🌀 Inicializando scraper...")
        self.scraping_stats_label.configure(text="Preparando...")

        # Cambiar estado de botones
        self.start_button.configure(state="disabled", text="⏳ Procesando...")
        self.stop_button.configure(state="normal")
        self.is_running = True

        # Limpiar logs anteriores
        self.logs_text.configure(state="normal")
        self.logs_text.insert("end", "\n" + "="*80 + "\n")
        self.logs_text.insert("end", f"🚀 NUEVA SESIÓN DE SCRAPING - {time.strftime('%H:%M:%S %d/%m/%Y')}\n")
        self.logs_text.insert("end", "="*80 + "\n\n")
        self.logs_text.configure(state="disabled")

        # Iniciar scraping en hilo separado
        threading.Thread(target=self.scraping_thread, daemon=True).start()

    def stop_scraping(self):
        """Detiene el proceso de scraping"""
        self.is_running = False
        self.start_button.configure(state="normal", text="🚀 Iniciar Scraping")
        self.stop_button.configure(state="disabled")
        self.log_message("⏹️ Scraping detenido por el usuario")

    def scraping_thread(self):
        """Hilo principal de scraping con actualizaciones en tiempo real mejoradas"""
        try:
            self.scraping_status_label.configure(text="⚙️ Configurando...", text_color="blue")
            self.log_message("🚀 Iniciando scraping...")
            time.sleep(0.5)

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

            self.scraping_status_label.configure(text="🚀 Scraping activo", text_color="green")
            self.log_message(f"📋 Preparado para procesar {len(self.keywords_list)} keywords")

            target_domain = self.domain_entry.get().strip() or None
            self.progress_label.configure(text="🕐 Ejecutando búsquedas en Google...")

            results = self.scraper.batch_position_check(
                self.keywords_list,
                target_domain,
                int(self.pages_var.get())
            )

            if results:
                self.current_results = results
                self.scraping_status_label.configure(text="✅ Completado", text_color="green")
                self.progress_label.configure(text="✅ Scraping completado exitosamente")

                # Calcular costos de esta sesión
                session_consults = len(self.keywords_list) * int(self.pages_var.get())
                self.today_consults += session_consults
                self.total_consults += session_consults
                if session_consults > 100:
                    paid_consults = session_consults - 100
                    self.total_cost += (paid_consults / 1000) * 5.0

                self.update_cost_display()

                self.log_message(f"✅ Scraping completado: {len(results)} resultados encontrados")
            else:
                self.scraping_status_label.configure(text="⚠️ Sin resultados", text_color="orange")
                self.log_message("⚠️ No se encontraron resultados")

        except Exception as e:
            self.scraping_status_label.configure(text="❌ Error", text_color="red")
            self.progress_label.configure(text="❌ Error durante el scraping")
            self.log_message(f"❌ Error en scraping: {e}")

        finally:
            self.start_button.configure(state="normal", text="🚀 Iniciar Scraping")
            self.stop_button.configure(state="disabled")
            self.is_running = False
            self.progress_bar.set(0)
            self.scraping_stats_label.configure(text="Listo para nuevo scraping")

    # ========== MÉTODOS PARA KEYWORDS RELACIONADAS ==========

    def find_related_keywords(self):
        """Busca keywords relacionadas usando el método del scraper para que los logs aparezcan en la consola del scraper"""
        keyword = self.related_keyword_entry.get().strip()

        if not keyword:
            messagebox.showwarning("Advertencia", "Ingresa una keyword principal")
            return

        # Validar credenciales de Google API
        if not self.api_key_var.get().strip() or not self.search_engine_id_var.get().strip():
            messagebox.showwarning("Error", "Configura tus credenciales de Google API primero\n\nVe a la pestaña '🔐 Google API'")
            return

        self.clear_related_keywords()
        self.related_text.configure(state="normal")
        self.related_text.insert("1.0", "🔍 Buscando sugerencias con Google Suggest...\n\n")
        self.related_text.configure(state="disabled")

        def search_thread():
            try:
                # Crear instancia del scraper si no existe (para obtener sugerencias)
                from config.settings import config
                scraper_config = config.copy()
                scraper_config.update({
                    'DEFAULT_COUNTRY': self.country_var.get(),
                    'DEFAULT_LANGUAGE': self.language_var.get()
                })

                scraper = StealthSerpScraper(scraper_config)

                # Buscar sugerencias usando múltiples variaciones del scraper
                search_variations = [
                    keyword, f"{keyword} ", f"{keyword} o", f"{keyword} c",
                    f"{keyword} d", f"{keyword} p", f"{keyword} q"
                ]

                all_suggestions = []

                # Los logs aparecerán automáticamente en la consola del scraper porque estamos usando sus métodos
                for i, variation in enumerate(search_variations, 1):
                    try:
                        # Usar el método del scraper - esto hace que los logs aparezcan en scraper.log y consola
                        suggests = scraper.google_suggest_scraper(
                            variation,
                            country=self.country_var.get(),
                            language=self.language_var.get()
                        )

                        # Filtrar sugerencias relevantes
                        relevant = [s for s in suggests if
                                  s.lower().startswith(keyword.lower()) and
                                  s.lower() != keyword.lower() and
                                  len(s) > len(keyword) + 2]

                        all_suggestions.extend(relevant[:10])  # Máximo 10 por variación

                    except Exception as e:
                        # Error interno - no mostrar en logs de scraper, solo en GUI si es necesario
                        continue

                # Filtrar duplicados y mostrar resultados
                unique_suggestions = list(set(all_suggestions))[:25]  # Máximo 25 total

                self.related_text.configure(state="normal")
                self.related_text.delete("1.0", "end")

                if unique_suggestions:
                    result_text = f"🎯 KEYWORDS RELACIONADAS - '{keyword}'\n"
                    result_text += f"📅 {time.strftime('%d/%m/%Y %H:%M:%S')}\n"
                    result_text += f"📊 Encontradas: {len(unique_suggestions)} sugerencias\n\n"

                    for i, sug in enumerate(unique_suggestions, 1):
                        result_text += f"{i:2d}. {sug}\n"

                    result_text += f"\n💡 Para usar estas keywords, haz click en '➕ Añadir a Lista'"

                    self.related_text.insert("1.0", result_text)
                    self.related_count_label.configure(text=f"({len(unique_suggestions)} sugerencias)")
                    self.add_to_keywords_button.configure(state="normal")
                    self.related_suggestions = unique_suggestions

                    # Log de éxito (esto aparecerá en consola de scraper)
                    scraper.logger.info(f"✅ Encontradas {len(unique_suggestions)} keywords relacionadas")
                else:
                    self.related_text.insert("1.0", f"❌ No se encontraron sugerencias relacionadas para '{keyword}'\n\n💡 Intenta con una keyword más popular o verifica tu conexión.")
                    self.related_count_label.configure(text="(0 sugerencias)")
                    self.add_to_keywords_button.configure(state="disabled")

            except Exception as e:
                # Error general - log en scraper si es posible
                try:
                    scraper.logger.error(f"❌ Error buscando keywords relacionadas: {str(e)[:80]}")
                except:
                    pass  # Si el scraper no se creó, al menos mostramos error en GUI

                self.related_text.configure(state="normal")
                self.related_text.delete("1.0", "end")
                self.related_text.insert("1.0", f"❌ Error durante la búsqueda:\n\n{str(e)}\n\n💡 Verifica tu conexión a internet.")
                self.related_count_label.configure(text="(error)")
                self.add_to_keywords_button.configure(state="disabled")

            finally:
                self.related_text.configure(state="disabled")

        # Ejecutar en hilo separado
        threading.Thread(target=search_thread, daemon=True).start()

    def clear_related_keywords(self):
        """Limpia el área de keywords relacionadas"""
        self.related_text.configure(state="normal")
        self.related_text.delete("1.0", "end")
        self.related_text.configure(state="disabled")
        self.related_count_label.configure(text="(0 sugerencias)")
        self.add_to_keywords_button.configure(state="disabled")
        self.related_suggestions = []
        self.related_keyword_entry.delete(0, "end")

    def add_related_to_keywords(self):
        """Añade las keywords relacionadas a la lista principal"""
        if not self.related_suggestions:
            messagebox.showwarning("Aviso", "No hay sugerencias para añadir")
            return

        current_keywords = self.get_current_keywords()
        existing_keywords = set(kw.lower() for kw in current_keywords)

        new_keywords = []
        for suggestion in self.related_suggestions:
            if suggestion.lower() not in existing_keywords:
                new_keywords.append(suggestion)
                existing_keywords.add(suggestion.lower())

        if new_keywords:
            combined_keywords = current_keywords + new_keywords
            self.set_current_keywords(combined_keywords)
            self.update_keywords_count()

            messagebox.showinfo("Éxito", f"✅ Añadidas {len(new_keywords)} keywords nuevas a la lista")
            self.log_message(f"➕ Añadidas {len(new_keywords)} keywords relacionadas")
            self.clear_related_keywords()
        else:
            messagebox.showinfo("Información", "Todas las sugerencias ya están en tu lista de keywords")

    # ========== MÉTODOS PARA MI RANKING ==========

    def analyze_my_rankings(self):
        """Analiza todas las keywords donde mi dominio posiciona"""
        domain = self.my_domain_entry.get().strip()
        if not domain:
            messagebox.showwarning("Error", "Debes introducir tu dominio")
            return

        # Limpiar http:// y www. si los hay
        domain = domain.replace("http://", "").replace("https://", "").replace("www.", "").split("/")[0]

        base_keywords_text = self.my_keywords_base_text.get("1.0", "end-1c")
        base_keywords = [k.strip() for k in base_keywords_text.split('\n') if k.strip()]

        if not base_keywords:
            messagebox.showwarning("Error", "Debes introducir al menos una keyword base")
            return

        try:
            suggestion_count = int(self.suggestion_count_var.get())
            if suggestion_count < 1 or suggestion_count > 20:
                messagebox.showwarning("Error", "El número de sugerencias debe estar entre 1-20")
                return
        except ValueError:
            messagebox.showwarning("Error", "Número de sugerencias inválido")
            return

        # Cambiar estado del botón
        self.my_ranking_button.configure(state="disabled", text="🔄 Analizando...")
        self.my_ranking_status.configure(text=f"Analizando ranking de: {domain}")

        def analysis_thread():
            try:
                results = []

                # Crear scraper
                from config.settings import config
                scraper_config = config.copy()
                scraper_config.update({
                    'MIN_KEYWORD_DELAY': 3,
                    'MAX_KEYWORD_DELAY': 7,
                    'PAGES_TO_SCRAPE': 3,
                    'DEFAULT_COUNTRY': "US",
                    'DEFAULT_LANGUAGE': "en"
                })

                scraper = StealthSerpScraper(scraper_config)

                # Generar sugestões y buscar
                total_processed = 0
                for base_keyword in base_keywords:
                    try:
                        self.my_ranking_status.configure(text=f"Proceso: {base_keyword}")

                        # Obtener sugerencias usando nuestro método de Google Suggest
                        search_variations = [
                            base_keyword, f"{base_keyword} ", f"{base_keyword} o"
                        ]

                        suggested_keywords = []
                        for variation in search_variations:
                            try:
                                import requests
                                url = "https://suggestqueries.google.com/complete/search"
                                params = {
                                    'client': 'firefox', 'q': variation,
                                    'hl': 'en', 'gl': 'us'
                                }
                                response = requests.get(url, params=params, timeout=5)

                                if response.status_code == 200:
                                    data = response.json()
                                    if len(data) >= 2 and isinstance(data[1], list):
                                        suggests = data[1][:max(1, suggestion_count // len(search_variations))]
                                        suggested_keywords.extend(suggests)
                            except:
                                continue

                        # Eliminar duplicados y añadir keyword base
                        all_keywords = list(set([base_keyword] + suggested_keywords))[:suggestion_count + 1]

                        # Verificar cada keyword
                        for keyword in all_keywords:
                            if keyword.strip():
                                try:
                                    search_results = scraper.single_keyword_position_check(keyword, None, 3)

                                    # Buscar si mi dominio aparece
                                    for result in search_results:
                                        if result['domain'] == domain:
                                            results.append({
                                                'keyword': keyword,
                                                'position': result['position'],
                                                'title': result['title'],
                                                'url': result['url'],
                                                'suggested_from': base_keyword
                                            })
                                            break  # Solo el primero encontrado

                                    total_processed += 1

                                except Exception as e:
                                    self.log_message(f"⚠️ Error analizando '{keyword}': {str(e)[:50]}")
                                    continue

                    except Exception as e:
                        self.log_message(f"❌ Error procesando '{base_keyword}': {str(e)[:50]}")
                        continue

                # Actualizar tabla
                self.root.after(0, lambda: self.update_my_rankings_results(results, domain, total_processed))

            except Exception as e:
                self.root.after(0, lambda: self.show_my_ranking_error(str(e)))
            finally:
                self.root.after(0, lambda: self.restore_my_rankings_button())

        threading.Thread(target=analysis_thread, daemon=True).start()

    def update_my_rankings_results(self, results, domain, total_processed):
        """Actualiza la tabla de resultados de mi ranking"""
        # Limpiar tabla
        for item in self.my_ranking_results_tree.get_children():
            self.my_ranking_results_tree.delete(item)

        # Ordenar por posición
        results_sorted = sorted(results, key=lambda x: x['position'])

        for result in results_sorted:
            self.my_ranking_results_tree.insert("", "end", values=(
                result['keyword'],
                result['position'],
                result['title'][:50] + "..." if len(result['title']) > 50 else result['title'],
                result['url'][:80] + "..." if len(result['url']) > 80 else result['url'],
                result['suggested_from']
            ))

        # Actualizar estado
        if results:
            avg_position = sum(r['position'] for r in results) / len(results)
            self.my_ranking_status.configure(text=f"✅ Completado: {len(results)} keywords encontradas, posición promedio: {avg_position:.1f}")
        else:
            self.my_ranking_status.configure(text=f"❌ No se encontraron posiciones para {domain} en {total_processed} keywords")

    def show_my_ranking_error(self, error_msg):
        """Muestra error en análisis de ranking"""
        self.my_ranking_status.configure(text=f"❌ Error: {error_msg[:50]}...")

    def restore_my_rankings_button(self):
        """Restaura el estado del botón de análisis de mi ranking"""
        self.my_ranking_button.configure(state="normal", text="🏆 Analizar Mi Ranking")

    # ========== MÉTODOS PARA ANÁLISIS ==========

    def generate_analysis(self):
        """Genera análisis avanzado de resultados"""
        if not self.current_results:
            messagebox.showwarning("Advertencia", "No hay resultados para analizar")
            return

        try:
            import matplotlib.pyplot as plt
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

            # Limpiar gráficos anteriores
            self.fig.clear()
            self.fig, ((self.ax1, self.ax2), (self.ax3, self.ax4)) = plt.subplots(2, 2, figsize=(12, 8))

            df = pd.DataFrame(self.current_results)

            # Gráfico 1: Distribución de posiciones
            if 'position' in df.columns:
                position_counts = df['position'].value_counts().sort_index()
                self.ax1.bar(position_counts.index, position_counts.values, color='skyblue', alpha=0.7)
                self.ax1.set_title('Distribución de Posiciones')
                self.ax1.set_xlabel('Posición')
                self.ax1.set_ylabel('Frecuencia')
                self.ax1.grid(True, alpha=0.3)

            # Gráfico 2: Top dominios
            if 'domain' in df.columns:
                top_domains = df['domain'].value_counts().head(10)
                self.ax2.barh(range(len(top_domains)), top_domains.values, color='lightgreen', alpha=0.7)
                self.ax2.set_yticks(range(len(top_domains)))
                self.ax2.set_yticklabels(top_domains.index, fontsize=8)
                self.ax2.set_title('Top 10 Dominios')
                self.ax2.set_xlabel('Frecuencia')
                self.ax2.grid(True, alpha=0.3)

            # Gráfico 3: Distribución por páginas
            if 'page' in df.columns:
                page_stats = df['page'].value_counts().sort_index()
                self.ax3.bar(page_stats.index, page_stats.values, color='orange', alpha=0.7)
                self.ax3.set_title('Resultados por Página')
                self.ax3.set_xlabel('Página')
                self.ax3.set_ylabel('Resultados')
                self.ax3.grid(True, alpha=0.3)

            # Gráfico 4: Boxplot de posiciones
            if 'position' in df.columns:
                self.ax4.boxplot(df['position'], vert=False)
                self.ax4.set_title('Boxplot de Posiciones')
                self.ax4.set_xlabel('Posición')
                self.ax4.grid(True, alpha=0.3)

            # Actualizar canvas
            self.fig.tight_layout(pad=3.0)
            self.canvas.draw()

            self.log_message("📊 Análisis generado correctamente")

        except Exception as e:
            messagebox.showerror("Error", f"Error generando análisis:\n\n{str(e)}")


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
