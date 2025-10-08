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
import os
import sys
from pathlib import Path
import pandas as pd
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
        self.main_keywords_text = None  # Área principal de keywords para scraping

        # Variables para la suite integrada de keywords
        self.analysis_results_text = None
        self.competitiveness_data = []
        self.variants_data = []

        # Variables de keywords relacionadas (integradas)
        self.related_keyword_entry = None
        self.related_text = None
        self.related_count_label = None
        self.add_to_keywords_button = None
        self.related_suggestions = []

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
        self.tab_keywords = self.tabview.add("🔑 KEYWORDS PRO SUITE")
        self.tab_scraping = self.tabview.add("🚀 Scraping")
        self.tab_results = self.tabview.add("📊 Resultados")
        self.tab_reports = self.tabview.add("📋 Informes")
        self.tab_analysis = self.tabview.add("📈 Análisis")

        # Configurar cada pestaña
        self.setup_google_api_tab()
        self.setup_config_tab()
        self.setup_keywords_tab()
        self.setup_scraping_tab()
        self.setup_results_tab()
        self.setup_reports_tab()
        self.setup_analysis_tab()

    def setup_reports_tab(self):
        """Configura la nueva pestaña de informes históricos"""
        main_frame = ctk.CTkFrame(self.tab_reports)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Header
        header_frame = ctk.CTkFrame(main_frame, fg_color=COLORS['surface'])
        header_frame.pack(fill="x", pady=(10, 20))

        title_label = ctk.CTkLabel(header_frame, text="📋 GESTIÓN DE INFORMES E HISTORIAL",
                                  font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack(pady=(20, 5))

        subtitle_label = ctk.CTkLabel(header_frame, text="Accede y administra todos tus informes de scraping generados",
                                     font=ctk.CTkFont(size=12))
        subtitle_label.pack(pady=(0, 20))

        # Panel de estadísticas rápidas
        stats_frame = ctk.CTkFrame(main_frame)
        stats_frame.pack(fill="x", padx=10, pady=(0, 20))

        stats_title = ctk.CTkLabel(stats_frame, text="📊 RESUMEN GENERAL",
                                  font=ctk.CTkFont(size=14, weight="bold"))
        stats_title.pack(anchor="w", pady=(10, 15))

        # Contadores de archivos
        try:
            data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')

            csv_count = 0
            json_count = 0
            total_size_mb = 0.0

            if os.path.exists(data_dir):
                for filename in os.listdir(data_dir):
                    filepath = os.path.join(data_dir, filename)
                    if os.path.isfile(filepath):
                        file_stats = os.stat(filepath)
                        total_size_mb += file_stats.st_size / (1024 * 1024)

                        if filename.endswith('.csv'):
                            csv_count += 1
                        elif filename.endswith('.json'):
                            json_count += 1

            # Mostrar estadísticas
            stats_grid = ctk.CTkFrame(stats_frame)
            stats_grid.pack(pady=(0, 15))

            # CSV files
            csv_frame = ctk.CTkFrame(stats_grid, fg_color=COLORS['info'], height=60)
            csv_frame.pack(side="left", fill="x", expand=True, padx=(0, 5))
            csv_frame.pack_propagate(False)
            ctk.CTkLabel(csv_frame, text="📄 CSV", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(8, 2))
            ctk.CTkLabel(csv_frame, text=str(csv_count), font=ctk.CTkFont(size=20, weight="bold")).pack(pady=(0, 5))

            # JSON files
            json_frame = ctk.CTkFrame(stats_grid, fg_color=COLORS['success'], height=60)
            json_frame.pack(side="left", fill="x", expand=True, padx=(0, 5))
            json_frame.pack_propagate(False)
            ctk.CTkLabel(json_frame, text="🗂️ JSON", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(8, 2))
            ctk.CTkLabel(json_frame, text=str(json_count), font=ctk.CTkFont(size=20, weight="bold")).pack(pady=(0, 5))

            # Total size
            size_frame = ctk.CTkFrame(stats_grid, fg_color=COLORS['warning'], height=60)
            size_frame.pack(side="left", fill="x", expand=True)
            size_frame.pack_propagate(False)
            ctk.CTkLabel(size_frame, text="💾 ESPACIO", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(8, 2))
            ctk.CTkLabel(size_frame, text=f"{total_size_mb:.1f} MB", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(0, 5))

        except Exception as e:
            ctk.CTkLabel(stats_frame, text=f"⚠️ Error obteniendo estadísticas: {str(e)[:50]}").pack(pady=10)

        # Lista de informes
        reports_section = ctk.CTkFrame(main_frame)
        reports_section.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        reports_header = ctk.CTkFrame(reports_section)
        reports_header.pack(fill="x", pady=(10, 5))

        ctk.CTkLabel(reports_header, text="📂 INFORMES DISPONIBLES",
                    font=ctk.CTkFont(size=16, weight="bold")).pack(side="left")

        # Botón de actualizar
        refresh_btn = ctk.CTkButton(reports_header, text="🔄 Actualizar",
                                   command=lambda: self.refresh_reports_tab(), width=100)
        refresh_btn.pack(side="right")

        # Scrollable frame para la lista
        self.reports_scroll = ctk.CTkScrollableFrame(reports_section)
        self.reports_scroll.pack(fill="both", expand=True, pady=(0, 10))

        # Inicializar la lista
        self.refresh_reports_tab()

        # Panel de acciones
        actions_frame = ctk.CTkFrame(main_frame)
        actions_frame.pack(fill="x", padx=10, pady=(0, 10))

        actions_title = ctk.CTkLabel(actions_frame, text="🛠️ ACCIONES DE GESTIÓN",
                                    font=ctk.CTkFont(size=14, weight="bold"))
        actions_title.pack(anchor="w", pady=(10, 15))

        actions_buttons = ctk.CTkFrame(actions_frame)
        actions_buttons.pack(fill="x", pady=(0, 10))

        # Botones de acción
        ctk.CTkButton(actions_buttons, text="🗂️ Abrir Carpeta Data",
                     command=self.open_data_folder, fg_color=COLORS['info']).pack(side="left", padx=(0, 5))

        ctk.CTkButton(actions_buttons, text="🧽 Limpiar Archivos Antiguos",
                     command=self.clean_old_reports, fg_color=COLORS['warning']).pack(side="left", padx=(0, 5))

        ctk.CTkButton(actions_buttons, text="📊 Generar Reporte Consolidado",
                     command=self.generate_consolidated_report, fg_color=COLORS['accent']).pack(side="left")

    def refresh_reports_tab(self):
        """Actualiza la lista de informes en la pestaña de reports"""
        try:
            # Limpiar contenido anterior
            for widget in self.reports_scroll.winfo_children():
                widget.destroy()

            # Obtener archivos
            data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')

            if not os.path.exists(data_dir):
                ctk.CTkLabel(self.reports_scroll, text="📁 La carpeta 'data/' no existe aún").pack(pady=20)
                return

            # Buscar archivos relevantes
            files = []
            for filename in os.listdir(data_dir):
                if filename.endswith(('.csv', '.json')) and not filename.endswith('_resumen.csv'):
                    filepath = os.path.join(data_dir, filename)
                    if os.path.isfile(filepath):
                        file_stats = os.stat(filepath)
                        mod_time = time.ctime(file_stats.st_mtime)
                        file_size = file_stats.st_size

                        # Extraer información del nombre del archivo
                        keywords_info = "Desconocido"
                        if "_scraping" in filename:
                            try:
                                # Extraer número de keywords del nombre
                                parts = filename.split('_scraping')[1].split('_')[0]
                                if parts.isdigit():
                                    keywords_info = f"{parts} keywords"
                            except:
                                pass

                        files.append({
                            'name': filename,
                            'path': filepath,
                            'size': file_size,
                            'modified': mod_time,
                            'type': filename.split('.')[-1].upper(),
                            'keywords': keywords_info
                        })

            # Ordenar por fecha de modificación (más reciente primero)
            files.sort(key=lambda x: x['modified'], reverse=True)

            if not files:
                ctk.CTkLabel(self.reports_scroll, text="📄 No hay informes guardados aún").pack(pady=20)
                return

            # Crear entradas para cada archivo
            for i, file_info in enumerate(files[:15]):  # Máximo 15 archivos
                # Frame del informe
                report_frame = ctk.CTkFrame(self.reports_scroll, fg_color=COLORS['secondary'])
                report_frame.pack(fill="x", pady=(0, 8), padx=10)

                # Información principal
                info_frame = ctk.CTkFrame(report_frame, fg_color="transparent")
                info_frame.pack(fill="x", padx=15, pady=10)

                # Nombre y tipo
                name_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
                name_frame.pack(fill="x", pady=(0, 2))

                file_icon = "📄" if file_info['type'] == 'CSV' else "🗂️"
                ctk.CTkLabel(name_frame, text=f"{file_icon} {file_info['name']}",
                            font=ctk.CTkFont(size=12, weight="bold")).pack(side="left")

                # Tamaño
                size_mb = file_info['size'] / (1024 * 1024)
                ctk.CTkLabel(name_frame, text=f"{size_mb:.2f} MB",
                            font=ctk.CTkFont(size=10)).pack(side="right")

                # Metadatos
                meta_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
                meta_frame.pack(fill="x")

                meta_text = f"📊 {file_info['keywords']} | 📅 {time.strftime('%d/%m/%y %H:%M', time.strptime(file_info['modified']))}"
                ctk.CTkLabel(meta_frame, text=meta_text,
                            font=ctk.CTkFont(size=9), text_color=COLORS['text_secondary']).pack(side="left")

                # Botones de acción
                buttons_frame = ctk.CTkFrame(meta_frame, fg_color="transparent")
                buttons_frame.pack(side="right")

                # Determinar tipo de acción según el archivo
                if file_info['type'] == 'CSV':
                    action_btn = ctk.CTkButton(buttons_frame, text="📊 Cargar en Tabla",
                                              command=lambda f=file_info: self.load_csv_report(f),
                                              height=25, width=110, font=ctk.CTkFont(size=9))
                else:
                    action_btn = ctk.CTkButton(buttons_frame, text="🔍 Ver Contenido",
                                              command=lambda f=file_info: self.view_json_report(f),
                                              height=25, width=110, font=ctk.CTkFont(size=9))

                action_btn.pack(side="left", padx=(0, 3))

                delete_btn = ctk.CTkButton(buttons_frame, text="🗑️ Eliminar",
                                          command=lambda f=file_info: self.delete_report_file(f),
                                          height=25, width=70, font=ctk.CTkFont(size=9),
                                          fg_color=COLORS['error'])
                delete_btn.pack(side="left")

                # Separador visual
                if i < len(files) - 1:
                    separator = ctk.CTkFrame(self.reports_scroll, height=1, fg_color=COLORS['border'])
                    separator.pack(fill="x", padx=10)

        except Exception as e:
            error_label = ctk.CTkLabel(self.reports_scroll, text=f"❌ Error cargando informes: {str(e)[:50]}")
            error_label.pack(pady=20)

    def load_csv_report(self, file_info):
        """Carga un archivo CSV en la tabla de resultados"""
        try:
            df = pd.read_csv(file_info['path'])
            results = df.to_dict('records')

            # Actualizar resultados actuales
            self.current_results = results

            # Actualizar tabla
            self.update_results_table()
            self.update_stats_blocks()

            # Cambiar a pestaña de resultados
            self.tabview.set("📊 Resultados")

            # Mostrar mensaje
            self.results_status_label.configure(text=f"✅ Informe '{file_info['name']}' cargado exitosamente")

            self.log_message(f"📊 Informe CSV cargado: {file_info['name']}")

        except Exception as e:
            messagebox.showerror("Error", f"Error cargando CSV:\n\n{str(e)}")

    def view_json_report(self, file_info):
        """Muestra el contenido de un archivo JSON"""
        try:
            with open(file_info['path'], 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Crear ventana para mostrar el JSON
            json_window = ctk.CTkToplevel(self.root)
            json_window.title(f"Contenido JSON - {file_info['name']}")
            json_window.geometry("700x600")

            # Título
            ctk.CTkLabel(json_window, text=f"📄 {file_info['name']}",
                        font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(20, 10))

            # Área de texto con scrollbar
            text_frame = ctk.CTkFrame(json_window)
            text_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

            text_area = ctk.CTkTextbox(text_frame, font=ctk.CTkFont(family="Consolas", size=10), wrap="none")
            text_area.pack(fill="both", expand=True, padx=10, pady=10)

            # Formatear JSON para mostrar
            formatted_json = json.dumps(data, indent=2, ensure_ascii=False)
            text_area.insert("1.0", formatted_json)
            text_area.configure(state="disabled")

            # Botón cerrar
            ctk.CTkButton(json_window, text="✅ Cerrar", command=json_window.destroy).pack(pady=(0, 20))

        except Exception as e:
            messagebox.showerror("Error", f"Error leyendo JSON:\n\n{str(e)}")

    def delete_report_file(self, file_info):
        """Elimina un archivo de reporte después de confirmación"""
        try:
            if not messagebox.askyesno("Confirmar Eliminación",
                                     f"¿Estás seguro de eliminar el archivo?\n\n{file_info['name']}\n\nEsta acción no se puede deshacer."):
                return

            os.remove(file_info['path'])

            # Actualizar lista
            self.refresh_reports_tab()

            messagebox.showinfo("Eliminación Exitosa",
                              f"Archivo eliminado:\n{file_info['name']}")

            self.log_message(f"🗑️ Archivo eliminado: {file_info['name']}")

        except Exception as e:
            messagebox.showerror("Error", f"Error eliminando archivo:\n\n{str(e)}")

    def open_data_folder(self):
        """Abre la carpeta data/ en el explorador de archivos"""
        try:
            data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')

            if not os.path.exists(data_dir):
                os.makedirs(data_dir)

            # Abrir carpeta según el sistema operativo
            import subprocess
            import platform

            if platform.system() == "Windows":
                subprocess.run(["explorer", data_dir])
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", data_dir])
            else:  # Linux
                subprocess.run(["xdg-open", data_dir])

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir la carpeta:\n\n{str(e)}")

    def clean_old_reports(self):
        """Limpia archivos antiguos de la carpeta data/"""
        try:
            data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')

            if not os.path.exists(data_dir):
                messagebox.showinfo("Información", "La carpeta data/ no existe aún.")
                return

            # Obtener archivos con su fecha de modificación
            files_to_check = []
            current_time = time.time()

            for filename in os.listdir(data_dir):
                filepath = os.path.join(data_dir, filename)
                if os.path.isfile(filepath):
                    file_age_days = (current_time - os.stat(filepath).st_mtime) / (24 * 60 * 60)
                    files_to_check.append((filepath, filename, file_age_days))

            # Filtrar archivos antiguos (más de 30 días)
            old_files = [f for f in files_to_check if f[2] > 30]

            if not old_files:
                messagebox.showinfo("Información",
                                  "No hay archivos antiguos para limpiar.\n\nSe consideran antiguos los archivos con más de 30 días.")
                return

            # Confirmar limpieza
            if not messagebox.askyesno("Confirmar Limpieza",
                                     f"Se encontraron {len(old_files)} archivos antiguos (más de 30 días).\n\n"
                                     f"¿Deseas eliminarlos?\n\n"
                                     f"Archivos a eliminar:\n" +
                                     "\n".join([f"- {f[1]} ({f[2]:.0f} días)" for f in old_files[:10]]) +
                                     ("\n... y más" if len(old_files) > 10 else "")):
                return

            # Eliminar archivos antiguos
            deleted_count = 0
            for filepath, filename, age in old_files:
                try:
                    os.remove(filepath)
                    deleted_count += 1
                    self.log_message(f"🗑️ Archivo antiguo eliminado: {filename}")
                except Exception as e:
                    self.log_message(f"⚠️ Error eliminando {filename}: {str(e)}")

            # Actualizar interfaz
            self.refresh_reports_tab()

            messagebox.showinfo("Limpieza Completada",
                              f"✅ Limpieza completada exitosamente!\n\n"
                              f"📁 Archivos eliminados: {deleted_count}\n"
                              f"💾 Espacio liberado aproximado: {(sum(f[0].__sizeof__() for f in old_files) / (1024*1024)):.1f} MB")

        except Exception as e:
            messagebox.showerror("Error", f"Error durante la limpieza:\n\n{str(e)}")

    def generate_consolidated_report(self):
        """Genera un reporte consolidado con estadísticas generales"""
        try:
            data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')

            if not os.path.exists(data_dir):
                messagebox.showwarning("Advertencia", "No hay carpeta data/ con informes")
                return

            # Recopilar información de todos los CSV
            all_results = []
            csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv') and not f.endswith('_resumen.csv')]

            if not csv_files:
                messagebox.showwarning("Advertencia", "No hay archivos CSV para consolidar")
                return

            consolidated_data = {
                'total_scraping_sessions': len(csv_files),
                'total_files_analyzed': 0,
                'total_results_found': 0,
                'unique_keywords_total': set(),
                'unique_domains_total': set(),
                'avg_position_overall': [],
                'total_cost_estimated': 0.0,
                'sessions_by_date': {}
            }

            for csv_file in csv_files:
                try:
                    filepath = os.path.join(data_dir, csv_file)
                    df = pd.read_csv(filepath)

                    consolidated_data['total_files_analyzed'] += 1
                    consolidated_data['total_results_found'] += len(df)

                    if 'keyword' in df.columns:
                        consolidated_data['unique_keywords_total'].update(df['keyword'].dropna().tolist())

                    if 'domain' in df.columns:
                        consolidated_data['unique_domains_total'].update(df['domain'].dropna().tolist())

                    if 'position' in df.columns:
                        consolidated_data['avg_position_overall'].extend(df['position'].dropna().tolist())

                    # Intentar extraer fecha del nombre del archivo
                    try:
                        date_match = re.search(r'(\d{8})_', csv_file)
                        if date_match:
                            date_str = date_match.group(1)
                            date_formatted = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"
                            if date_formatted not in consolidated_data['sessions_by_date']:
                                consolidated_data['sessions_by_date'][date_formatted] = 0
                            consolidated_data['sessions_by_date'][date_formatted] += 1
                    except:
                        pass

                    # Estimar costo
                    if 'position' in df.columns:
                        positions_count = len(df)
                        consolidated_data['total_cost_estimated'] += (positions_count * 0.005)

                except Exception as e:
                    self.log_message(f"⚠️ Error procesando {csv_file}: {str(e)[:50]}")
                    continue

            # Crear ventana de reporte consolidado
            report_window = ctk.CTkToplevel(self.root)
            report_window.title("📊 Reporte Consolidado")
            report_window.geometry("800x700")
            report_window.transient(self.root)

            # Header
            header_frame = ctk.CTkFrame(report_window)
            header_frame.pack(fill="x", padx=20, pady=(20, 10))

            ctk.CTkLabel(header_frame, text="📊 REPORTE CONSOLIDADO DE SCRAPING",
                        font=ctk.CTkFont(size=18, weight="bold")).pack()

            # Fecha de generación
            ctk.CTkLabel(header_frame, text=f"📅 Generado el {time.strftime('%d/%m/%Y %H:%M:%S')}",
                        font=ctk.CTkFont(size=10)).pack(pady=(5, 0))

            # Contenido
            content_frame = ctk.CTkScrollableFrame(report_window)
            content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

            # SECCIÓN 1: Métricas Generales
            section1_frame = ctk.CTkFrame(content_frame, fg_color="gray15")
            section1_frame.pack(fill="x", pady=(0, 15))

            ctk.CTkLabel(section1_frame, text="📈 MÉTRICAS GENERALES",
                        font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(15, 10))

            # Crear métricas
            metrics_data = [
                ("Sesiones de Scraping", consolidated_data['total_scraping_sessions']),
                ("Archivos Analizados", consolidated_data['total_files_analyzed']),
                ("Resultados Totales", consolidated_data['total_results_found']),
                ("Keywords Únicas", len(consolidated_data['unique_keywords_total'])),
                ("Dominios Únicos", len(consolidated_data['unique_domains_total'])),
                ("Posición Promedio Global", f"{sum(consolidated_data['avg_position_overall']) / len(consolidated_data['avg_position_overall']):.1f}" if consolidated_data['avg_position_overall'] else "N/A"),
                ("Costo Total Estimado", f"${consolidated_data['total_cost_estimated']:.2f}")
            ]

            for label, value in metrics_data:
                metric_frame = ctk.CTkFrame(section1_frame)
                metric_frame.pack(fill="x", padx=20, pady=2)
                ctk.CTkLabel(metric_frame, text=label).pack(side="left")
                ctk.CTkLabel(metric_frame, text=str(value), font=ctk.CTkFont(weight="bold")).pack(side="right")

            # SECCIÓN 2: Actividad por Fecha
            if consolidated_data['sessions_by_date']:
                section2_frame = ctk.CTkFrame(content_frame, fg_color="gray15")
                section2_frame.pack(fill="x", pady=(0, 15))

                ctk.CTkLabel(section2_frame, text="📅 ACTIVIDAD POR FECHA",
                            font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(15, 10))

                sorted_dates = sorted(consolidated_data['sessions_by_date'].items(), key=lambda x: x[0], reverse=True)

                for date, count in sorted_dates[:10]:  # Top 10 fechas
                    date_frame = ctk.CTkFrame(section2_frame)
                    date_frame.pack(fill="x", padx=20, pady=2)
                    ctk.CTkLabel(date_frame, text=date).pack(side="left")
                    ctk.CTkLabel(date_frame, text=f"{count} sesiones", font=ctk.CTkFont(weight="bold")).pack(side="right")

            # Botón de exportar
            export_btn = ctk.CTkButton(report_window, text="💾 Exportar Reporte",
                                     command=lambda: self.export_consolidated_report(consolidated_data),
                                     fg_color=COLORS['success'])
            export_btn.pack(pady=(0, 20))

        except Exception as e:
            messagebox.showerror("Error", f"Error generando reporte consolidado:\n\n{str(e)}")

    def export_consolidated_report(self, consolidated_data):
        """Exporta el reporte consolidado"""
        try:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                initialfile=f"reporte_consolidado_{timestamp}"
            )

            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write("📊 REPORTE CONSOLIDADO DE SCRAPING\n")
                    f.write("=" * 50 + "\n\n")
                    f.write(f"📅 Generado el: {time.strftime('%d/%m/%Y %H:%M:%S')}\n\n")

                    f.write("📈 MÉTRICAS GENERALES:\n")
                    f.write("-" * 30 + "\n")
                    f.write(f"Sesiones de Scraping: {consolidated_data['total_scraping_sessions']}\n")
                    f.write(f"Archivos Analizados: {consolidated_data['total_files_analyzed']}\n")
                    f.write(f"Resultados Totales: {consolidated_data['total_results_found']}\n")
                    f.write(f"Keywords Únicas: {len(consolidated_data['unique_keywords_total'])}\n")
                    f.write(f"Dominios Únicos: {len(consolidated_data['unique_domains_total'])}\n")

                    avg_pos = consolidated_data['avg_position_overall']
                    if avg_pos:
                        f.write(f"Posición Promedio Global: {sum(avg_pos) / len(avg_pos):.1f}\n")
                    else:
                        f.write("Posición Promedio Global: N/A\n")

                    f.write(f"Costo Total Estimado: ${consolidated_data['total_cost_estimated']:.2f}\n\n")

                    if consolidated_data['sessions_by_date']:
                        f.write("📅 ACTIVIDAD POR FECHA:\n")
                        f.write("-" * 30 + "\n")

                        sorted_dates = sorted(consolidated_data['sessions_by_date'].items(),
                                            key=lambda x: x[0], reverse=True)

                        for date, count in sorted_dates:
                            f.write(f"{date}: {count} sesiones\n")

                messagebox.showinfo("Éxito", f"Reporte consolidado exportado:\n\n{file_path}")

        except Exception as e:
            messagebox.showerror("Error", f"Error exportando reporte:\n\n{str(e)}")

    def get_google_suggestions(self, query, country="US", language="en"):
        """Obtiene sugerencias de Google Suggest para una query específica"""
        import requests

        try:
            # URL de Google Suggest API
            url = "https://suggestqueries.google.com/complete/search"

            params = {
                'client': 'firefox',  # o 'chrome', 'firefox', etc.
                'q': query,
                'hl': language.lower(),  # idioma
                'gl': country.upper(),   # país
                'ds': 'yt'  # o vacío para búsqueda general
            }

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0',
                'Accept': '*/*',
                'Accept-Language': f'{language.lower()},{language.lower()};q=0.8,en-US;q=0.5,en;q=0.3',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Cache-Control': 'max-age=0',
            }

            # Hacer la petición
            response = requests.get(url, params=params, headers=headers, timeout=10)

            if response.status_code == 200:
                try:
                    # La respuesta es JSON: ["query", [sugerencias]]
                    data = response.json()
                    if len(data) >= 2 and isinstance(data[1], list):
                        return data[1]  # Lista de sugerencias
                except json.JSONDecodeError:
                    # A veces Google devuelve HTML en lugar de JSON
                    self.log_message("⚠️ Google Suggest devolvió formato inesperado")

            return []

        except Exception as e:
            self.log_message(f"⚠️ Error obteniendo sugerencias: {str(e)[:50]}")
            return []

    def find_related_keywords(self):
        """Busca keywords relacionadas usando Google Suggest API y obtiene sus posiciones reales"""
        keyword = self.related_keyword_entry.get().strip()

        if not keyword:
            messagebox.showwarning("Advertencia", "Ingresa una keyword principal")
            return

        # Validar credenciales de Google API
        if not self.api_key_var.get().strip() or not self.search_engine_id_var.get().strip():
            messagebox.showwarning("Error", "Configura tus credenciales de Google API primero\n\nVe a la pestaña '🔐 Google API'")
            return

        # Limpiar resultados anteriores
        self.clear_related_keywords()

        # Mostrar mensaje de carga
        self.related_text.configure(state="normal")
        self.related_text.insert("1.0", f"🔍 Buscando keywords relacionadas para '{keyword}'...\n\nPaso 1: Obteniendo sugerencias de Google Suggest...")
        self.related_text.configure(state="disabled")

        # Actualizar contador
        self.related_count_label.configure(text="(buscando sugerencias...)")

        def search_thread():
            try:
                self.log_message("="*70)
                self.log_message(f"🔍 SESIÓN DE KEYWORDS RELACIONADAS - '{keyword}'")
                self.log_message("="*70)

                # Paso 1: Obtener sugerencias de Google Suggest
                self.log_message("📝 PASO 1: Obteniendo sugerencias de Google Suggest (GRATIS)")

                self.related_text.configure(state="normal")
                self.related_text.delete("1.0", "end")
                self.related_text.insert("1.0", f"🎯 Keyword base: '{keyword}'\n📅 Fecha: {time.strftime('%d/%m/%Y %H:%M:%S')}\n\n")
                self.related_text.insert("end", "📝 Paso 1: Analizando Google Suggest...\n⏳ Buscando patrones de búsqueda...\n")
                self.related_text.configure(state="disabled")

                all_suggestions = []
                search_variations = [
                    keyword,  # Keyword original
                    f"{keyword} ",  # Con espacio al final
                    f"{keyword} o",  # Variaciones con conectores
                    f"{keyword} c",  # Como, cómo
                    f"{keyword} d",  # De, donde
                    f"{keyword} p",  # Precio, para
                    f"{keyword} q",  # Que, quien
                ]

                # Obtener sugerencias para cada variación
                for i, variation in enumerate(search_variations, 1):
                    self.log_message(f"🔍 Buscando variación {i}/{len(search_variations)}: '{variation}'")

                    try:
                        suggests = self.get_google_suggestions(
                            variation,
                            country=self.country_var.get(),
                            language=self.language_var.get()
                        )

                        if suggests and len(suggests) > 0:
                            # Filtrar sugerencias relevantes
                            relevant = [s for s in suggests if
                                      s.lower().startswith(keyword.lower()) and
                                      s.lower() != keyword.lower() and
                                      len(s) > len(keyword) + 2]  # Mínimo 3 caracteres adicionales

                            all_suggestions.extend(relevant)
                            self.log_message(f"   ✅ Encontradas {len(relevant)} sugerencias relevantes")
                        else:
                            self.log_message(f"   ⚠️ No se encontraron sugerencias para '{variation}'")

                    except Exception as e:
                        self.log_message(f"   ❌ Error en variación '{variation}': {str(e)[:50]}")
                        continue

                # Eliminar duplicados y limpiar
                unique_suggestions = list(set(all_suggestions))
                # Ordenar por relevancia (más cortas primero, luego alfabético)
                unique_suggestions.sort(key=lambda x: (len(x), x.lower()))

                # Limitar a 25 sugerencias máximo para análisis eficiente
                if len(unique_suggestions) > 25:
                    unique_suggestions = unique_suggestions[:25]

                self.log_message(f"✅ PASO 1 COMPLETADO: {len(unique_suggestions)} sugerencias únicas encontradas")
                self.log_message("-"*50)

                # Actualizar UI con resultados del paso 1
                self.related_text.configure(state="normal")
                self.related_text.insert("end", f"\n✅ Paso 1 completado: {len(unique_suggestions)} sugerencias\n\n")
                self.related_text.insert("end", "📊 Sugerencias encontradas:\n")
                for i, sug in enumerate(unique_suggestions[:15], 1):  # Mostrar primeras 15
                    self.related_text.insert("end", f"{i:2d}. {sug}\n")
                if len(unique_suggestions) > 15:
                    self.related_text.insert("end", f"   ... y {len(unique_suggestions)-15} más\n")
                self.related_text.insert("end", "\n")
                self.related_text.configure(state="disabled")

                # Paso 2: Análisis detallado de posiciones
                analyzed_results = []
                if unique_suggestions:
                    self.log_message("🚀 PASO 2: Analizando posiciones reales en Google")
                    self.related_count_label.configure(text=f"(analizando {len(unique_suggestions)} sugerencias...)")

                    self.related_text.configure(state="normal")
                    self.related_text.insert("end", "="*60 + "\n")
                    self.related_text.insert("end", "🚀 Paso 2: Análisis de posiciones en Google\n")
                    self.related_text.insert("end", "⏳ Consultando Google API para obtener posiciones reales...\n\n")
                    self.related_text.configure(state="disabled")

                    # Crear scraper temporal con configuración óptima
                    from config.settings import config
                    temp_config = config.copy()
                    temp_config.update({
                        'PAGES_TO_SCRAPE': 3,  # 3 páginas para cobertura completa
                        'DEFAULT_COUNTRY': self.country_var.get(),
                        'DEFAULT_LANGUAGE': self.language_var.get(),
                        'MIN_KEYWORD_DELAY': 1,  # Delay mínimo para eficiencia
                        'MAX_KEYWORD_DELAY': 2
                    })

                    from stealth_scraper import StealthSerpScraper
                    temp_scraper = StealthSerpScraper(temp_config)

                    target_domain = self.domain_entry.get().strip() or None
                    self.log_message(f"🎯 Dominio objetivo: {target_domain or 'Todos'}")

                    # Procesar en lotes de 4 keywords para mejor rendimiento
                    batch_size = 4
                    total_processed = 0

                    for batch_idx in range(0, len(unique_suggestions), batch_size):
                        batch = unique_suggestions[batch_idx:batch_idx + batch_size]
                        self.log_message(f"📦 Procesando lote {batch_idx//batch_size + 1}: {len(batch)} keywords")

                        try:
                            # Actualizar UI con progreso
                            self.related_text.configure(state="normal")
                            self.related_text.insert("end", f"🔄 Analizando lote {batch_idx//batch_size + 1}: {', '.join(batch[:3])}{'...' if len(batch) > 3 else ''}\n")
                            self.related_text.configure(state="disabled")

                            batch_results = temp_scraper.batch_position_check(
                                batch,
                                target_domain,
                                3  # 3 páginas
                            )

                            if batch_results:
                                analyzed_results.extend(batch_results)
                                total_processed += len(batch_results)
                                self.log_message(f"   ✅ Lote completado: {len(batch_results)} posiciones encontradas")

                                # Mostrar algunos resultados en tiempo real
                                for result in batch_results[:2]:  # Solo primeros 2 por lote
                                    pos = result['position']
                                    emoji = "🥇" if pos == 1 else "🏆" if pos <= 3 else "📈" if pos <= 10 else "📊"
                                    self.related_text.configure(state="normal")
                                    self.related_text.insert("end", f"   {emoji} POS {pos}: {result['keyword'][:40]}...\n")
                                    self.related_text.configure(state="disabled")
                            else:
                                self.log_message(f"   ⚠️ Lote sin resultados")

                        except Exception as e:
                            self.log_message(f"   ❌ Error en lote {batch_idx//batch_size + 1}: {str(e)[:80]}")
                            continue

                    self.log_message(f"✅ PASO 2 COMPLETADO: {total_processed} posiciones analizadas de {len(unique_suggestions)} sugerencias")
                    self.log_message("-"*50)

                # PASO 3: GUARDAR RESULTADOS AUTOMÁTICAMENTE
                self.log_message("💾 PASO 3: Guardando resultados en historial")

                try:
                    # Crear directorio si no existe
                    if not os.path.exists('data'):
                        os.makedirs('data')

                    # Timestamp para archivos únicos
                    timestamp = time.strftime("%Y%m%d_%H%M%S")
                    base_filename = f"keywords_relacionadas_{keyword.replace(' ', '_')}_{timestamp}"

                    # Preparar datos para guardar
                    suggestions_data = []
                    for sug in unique_suggestions:
                        suggestions_data.append({
                            'keyword_base': keyword,
                            'sugerencia': sug,
                            'fecha': time.strftime("%Y-%m-%d %H:%M:%S"),
                            'pais': self.country_var.get(),
                            'idioma': self.language_var.get(),
                            'encontrada_posicion': any(r['keyword'] == sug for r in analyzed_results)
                        })

                    # Guardar sugerencias como CSV
                    suggestions_df = pd.DataFrame(suggestions_data)
                    csv_path = f"data/{base_filename}_sugerencias.csv"
                    suggestions_df.to_csv(csv_path, index=False, encoding='utf-8')

                    # Guardar posiciones analizadas si existen
                    if analyzed_results:
                        positions_df = pd.DataFrame(analyzed_results)
                        # Añadir información adicional
                        positions_df['keyword_base'] = keyword
                        positions_df['fecha_analisis'] = time.strftime("%Y-%m-%d %H:%M:%S")
                        positions_df['pais'] = self.country_var.get()
                        positions_df['idioma'] = self.language_var.get()

                        positions_csv = f"data/{base_filename}_posiciones.csv"
                        positions_df.to_csv(positions_csv, index=False, encoding='utf-8')

                        # También guardar como JSON para compatibilidad
                        positions_json = f"data/{base_filename}_posiciones.json"
                        with open(positions_json, 'w', encoding='utf-8') as f:
                            json.dump(analyzed_results, f, indent=2, ensure_ascii=False)

                        self.log_message(f"💾 Archivos guardados:")
                        self.log_message(f"   📄 {csv_path} ({len(suggestions_data)} sugerencias)")
                        self.log_message(f"   📊 {positions_csv} ({len(analyzed_results)} posiciones)")
                        self.log_message(f"   🗂️  {positions_json}")

                    else:
                        self.log_message(f"💾 Archivo guardado: {csv_path} ({len(suggestions_data)} sugerencias)")

                except Exception as e:
                    self.log_message(f"⚠️ Error guardando archivos: {str(e)[:50]}")

                # PASO 4: MOSTRAR RESULTADOS FINALES
                result_text = f"🎯 ANÁLISIS COMPLETO DE KEYWORDS RELACIONADAS\n"
                result_text += f"📅 Fecha: {time.strftime('%d/%m/%Y %H:%M:%S')}\n"
                result_text += f"🎯 Keyword base: '{keyword}'\n"
                result_text += f"🌍 País: {self.country_var.get()} | Idioma: {self.language_var.get()}\n\n"

                result_text += "="*70 + "\n"
                result_text += "📊 RESUMEN EJECUTIVO\n"
                result_text += "="*70 + "\n"
                result_text += f"🔍 Sugerencias encontradas: {len(unique_suggestions)}\n"
                result_text += f"📈 Posiciones analizadas: {len(analyzed_results)}\n"
                result_text += f"💾 Archivos guardados: ✅ Sí\n"

                if analyzed_results:
                    # Estadísticas detalladas
                    df = pd.DataFrame(analyzed_results)
                    avg_pos = df['position'].mean()
                    best_pos = df['position'].min()
                    worst_pos = df['position'].max()
                    top3_count = len(df[df['position'] <= 3])
                    top10_count = len(df[df['position'] <= 10])
                    top20_count = len(df[df['position'] <= 20])

                    result_text += f"📊 Estadísticas de posiciones:\n"
                    result_text += f"   • Posición promedio: {avg_pos:.1f}\n"
                    result_text += f"   • Mejor posición: {best_pos}\n"
                    result_text += f"   • Peor posición: {worst_pos}\n"
                    result_text += f"   • En Top 3: {top3_count} ({top3_count/len(analyzed_results)*100:.1f}%)\n"
                    result_text += f"   • En Top 10: {top10_count} ({top10_count/len(analyzed_results)*100:.1f}%)\n"
                    result_text += f"   • En Top 20: {top20_count} ({top20_count/len(analyzed_results)*100:.1f}%)\n"
                result_text += "\n"

                # Resultados detallados
                if analyzed_results:
                    result_text += "="*70 + "\n"
                    result_text += "🏆 RESULTADOS COMPLETOS ORDENADOS POR POSICIÓN\n"
                    result_text += "="*70 + "\n"

                    # Ordenar por posición
                    analyzed_results.sort(key=lambda x: x['position'])

                    for i, result in enumerate(analyzed_results, 1):
                        pos = result['position']
                        kw = result['keyword']
                        title = result['title'][:65] + "..." if len(result['title']) > 65 else result['title']
                        domain = result['domain']
                        page = result['page']

                        # Seleccionar emoji según posición
                        if pos == 1:
                            emoji = "🥇"
                        elif pos <= 3:
                            emoji = "🏆"
                        elif pos <= 10:
                            emoji = "📈"
                        elif pos <= 20:
                            emoji = "📊"
                        else:
                            emoji = "🔍"

                        result_text += f"{i:2d}. {emoji} POSICIÓN {pos:2d} | {kw}\n"
                        result_text += f"                       📄 {title}\n"
                        result_text += f"                       🌐 {domain} | Página {page}\n\n"

                # Sugerencias sin analizar
                unanalyzed = [s for s in unique_suggestions if not any(r['keyword'] == s for r in analyzed_results)]
                if unanalyzed:
                    result_text += "="*70 + "\n"
                    result_text += "💡 SUGERENCIAS QUE NO APARECEN EN TOP POSICIONES\n"
                    result_text += "="*70 + "\n"

                    for i, suggestion in enumerate(unanalyzed[:15], 1):
                        result_text += f"{i:2d}. {suggestion}\n"

                    if len(unanalyzed) > 15:
                        result_text += f"   ... y {len(unanalyzed)-15} más sugerencias sin posición\n"

                result_text += "\n" + "="*70 + "\n"
                result_text += "🎯 ACCIONES RECOMENDADAS:\n"
                result_text += "• Revisa las posiciones TOP 3 para oportunidades inmediatas\n"
                result_text += "• Considera las sugerencias sin posición para nichos poco competitivos\n"
                result_text += "• Añade las keywords más relevantes a tu lista principal\n"
                result_text += "• Los datos se guardaron automáticamente en la carpeta 'data/'\n"

                # Actualizar interfaz final
                self.related_text.configure(state="normal")
                self.related_text.delete("1.0", "end")
                self.related_text.insert("1.0", result_text)
                self.related_text.configure(state="disabled")

                # Actualizar estadísticas
                self.related_count_label.configure(text=f"({len(unique_suggestions)} sugerencias | {len(analyzed_results)} posiciones)")

                # Habilitar botón de añadir
                if unique_suggestions:
                    self.add_to_keywords_button.configure(state="normal")
                    self.related_suggestions = unique_suggestions

                # Log final
                self.log_message("✅ ANÁLISIS COMPLETADO EXITOSAMENTE")
                self.log_message(f"📊 Resultado: {len(unique_suggestions)} sugerencias → {len(analyzed_results)} posiciones analadas")
                self.log_message("="*70)

                # Mostrar mensaje de éxito
                messagebox.showinfo("✅ Análisis Completado",
                                  f"¡Análisis de keywords relacionadas completado!\n\n"
                                  f"📝 Sugerencias encontradas: {len(unique_suggestions)}\n"
                                  f"📊 Posiciones analizadas: {len(analyzed_results)}\n"
                                  f"💾 Archivos guardados en carpeta 'data/'\n\n"
                                  f"Puedes usar estos datos en la pestaña de Análisis.")

            except Exception as e:
                error_msg = f"❌ ERROR EN ANÁLISIS DE KEYWORDS RELACIONADAS:\n\n{str(e)}\n\n"
                error_msg += "💡 Verifica:\n"
                error_msg += "• Conexión a internet\n"
                error_msg += "• Credenciales de Google API\n"
                error_msg += "• Cuota diaria de consultas\n"

                self.related_text.configure(state="normal")
                self.related_text.delete("1.0", "end")
                self.related_text.insert("1.0", error_msg)
                self.related_text.configure(state="disabled")

                self.related_count_label.configure(text="(error)")
                self.add_to_keywords_button.configure(state="disabled")

                self.log_message(f"❌ ERROR EN SESIÓN DE KEYWORDS RELACIONADAS: {str(e)[:100]}")
                self.log_message("="*70)

                messagebox.showerror("Error", f"Error durante el análisis:\n\n{str(e)}")

        # Ejecutar en hilo separado
        threading.Thread(target=search_thread, daemon=True).start()

    def add_related_to_keywords(self):
        """Añade las keywords relacionadas a la lista principal usando el sistema unificado"""
        if not hasattr(self, 'related_suggestions') or not self.related_suggestions:
            messagebox.showwarning("Aviso", "No hay sugerencias para añadir")
            return

        # Obtener keywords actuales del sistema unificado
        current_keywords = self.get_current_keywords()

        # Combinar y eliminar duplicados (ignorando mayúsculas/minúsculas)
        all_keywords_set = set(k.lower() for k in current_keywords)
        new_keywords = []

        for suggestion in self.related_suggestions:
            if suggestion.lower() not in all_keywords_set:
                new_keywords.append(suggestion)
            else:
                all_keywords_set.add(suggestion.lower())

        # Añadir nuevas keywords
        if new_keywords:
            combined_keywords = current_keywords + new_keywords

            # Usar el sistema unificado para establecer las keywords
            self.set_current_keywords(combined_keywords)

            success_msg = f"✅ Añadidas {len(new_keywords)} keywords nuevas a la lista principal\n\n📊 Lista actual: {len(combined_keywords)} keywords totales\n\nLas keywords están listas para usar en Scraping."
            messagebox.showinfo("Éxito", success_msg)
            self.log_message(f"✅ Añadidas {len(new_keywords)} keywords relacionadas a la lista")

            # Limpiar sugerencias después de añadir
            self.clear_related_keywords()

        else:
            messagebox.showinfo("Información", "Todas las sugerencias ya estaban en tu lista de keywords principales")

    def clear_related_keywords(self):
        """Limpia el área de keywords relacionadas"""
        self.related_text.configure(state="normal")
        self.related_text.delete("1.0", "end")
        self.related_text.configure(state="disabled")

        self.related_count_label.configure(text="(0 sugerencias)")
        self.add_to_keywords_button.configure(state="disabled")

        # Limpiar sugerencias guardadas
        self.related_suggestions = []

        # Limpiar campo de entrada
        self.related_keyword_entry.delete(0, "end")

    def save_related_keywords(self):
        """Guarda la lista de keywords relacionadas en un archivo"""
        if not hasattr(self, 'related_suggestions') or not self.related_suggestions:
            messagebox.showwarning("Aviso", "No hay sugerencias para guardar")
            return

        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )

            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    # Añadir comentario inicial
                    keyword_principal = self.related_keyword_entry.get().strip()
                    if keyword_principal:
                        f.write(f"# Keywords relacionadas con: {keyword_principal}\n")
                        f.write(f"# Generadas el: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")

                    # Escribir cada sugerencia
                    for suggestion in self.related_suggestions:
                        f.write(f"{suggestion}\n")

                messagebox.showinfo("Éxito", f"Keywords relacionadas guardadas en {file_path}")

                keyword_principal = self.related_keyword_entry.get().strip() or "sin_keword_principal"
                self.log_message(f"💾 Guardadas {len(self.related_suggestions)} keywords relacionadas en {file_path}")

        except Exception as e:
            messagebox.showerror("Error", f"Error guardando keywords relacionadas: {e}")

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
        """NUEVA UI AMPLIAMENTE REDISEÑADA: 50% CONTROLES IZQUIERDA + 50% CONSOLA DESLIZABLE DERECHA"""
        # FRAME PRINCIPAL DIVIDIDO EN DOS COLUMNAS
        main_container = ctk.CTkFrame(self.tab_keywords)
        main_container.pack(fill="both", expand=True)

        # COLUMNA IZQUIERDA (50%): CONTROLES Y BOTONES
        left_panel = ctk.CTkFrame(main_container, fg_color=COLORS['secondary'])
        left_panel.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=10)

        # COLUMNA DERECHA (50%): CONSOLA DESLIZABLE PARA LOGS
        right_panel = ctk.CTkFrame(main_container)
        right_panel.pack(side="right", fill="both", expand=True, padx=(5, 10), pady=10)

        # ===================== PANEL IZQUIERDO: CONTROLES =====================

        # HEADER DEL PANEL IZQUIERDO
        left_header = ctk.CTkFrame(left_panel, fg_color=COLORS['surface'], height=60)
        left_header.pack(fill="x", pady=(10, 15))
        left_header.pack_propagate(False)

        ctk.CTkLabel(left_header, text="🎮 PANEL DE CONTROL",
                    font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(10, 5))

        ctk.CTkLabel(left_header, text="Herramientas • Importación • Procesamiento",
                    font=ctk.CTkFont(size=10), text_color=COLORS['text_secondary']).pack()

        # ÁREA DE BOTONES EN EL PANEL IZQUIERDO - ORGANIZADOS EN COLUMNAS
        buttons_container = ctk.CTkScrollableFrame(left_panel)
        buttons_container.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Sección 1: IMPORTACIÓN DE KEYWORDS
        import_section = ctk.CTkFrame(buttons_container, fg_color=COLORS['primary'])
        import_section.pack(fill="x", pady=(10, 15))

        import_title = ctk.CTkLabel(import_section, text="📥 IMPORTACIÓN DE KEYWORDS",
                                   font=ctk.CTkFont(size=14, weight="bold"),
                                   text_color=COLORS['text_primary'])
        import_title.pack(pady=(10, 15))

        # Grid de botones de importación (2 columnas)
        import_grid = ctk.CTkFrame(import_section, fg_color="transparent")
        import_grid.pack(fill="x", padx=15, pady=(0, 10))

        ctk.CTkButton(import_grid, text="📁 CARGAR TXT/CSV/JSON\n(Archivos Completos)",
                     command=self.load_keywords_file, height=60,
                     fg_color=COLORS['accent'], font=ctk.CTkFont(size=11, weight="bold")).pack(fill="x", pady=(0, 8))

        ctk.CTkButton(import_grid, text="🎯 GOOGLE SUGGEST\n(Generar Ideas)",
                     command=self.generate_suggestions, height=50,
                     fg_color=COLORS['success']).pack(fill="x", pady=(0, 8))

        ctk.CTkButton(import_grid, text="🔄 GENERAR VARIANTES\n(Expansión Inteligente)",
                     command=self.generate_keyword_variants, height=50,
                     fg_color=COLORS['info']).pack(fill="x", pady=(0, 8))

        # Sección 2: PROCESAMIENTO DE KEYWORDS
        process_section = ctk.CTkFrame(buttons_container, fg_color=COLORS['primary'])
        process_section.pack(fill="x", pady=(0, 15))

        process_title = ctk.CTkLabel(process_section, text="⚡ PROCESAMIENTO Y LIMPIEZA",
                                    font=ctk.CTkFont(size=14, weight="bold"),
                                    text_color=COLORS['text_primary'])
        process_title.pack(pady=(10, 15))

        process_grid = ctk.CTkFrame(process_section, fg_color="transparent")
        process_grid.pack(fill="x", padx=15, pady=(0, 10))

        ctk.CTkButton(process_grid, text="🧹 LIMPIEZA AVANZADA\n(Duplicados + Stop Words)",
                     command=self.advanced_keyword_cleaning, height=50,
                     fg_color=COLORS['warning']).pack(fill="x", pady=(0, 8))

        ctk.CTkButton(process_grid, text="📊 ACTUALIZAR ESTADÍSTICAS\n(Análisis General)",
                     command=self.update_keywords_stats, height=50,
                     fg_color=COLORS['secondary']).pack(fill="x", pady=(0, 8))

        ctk.CTkButton(process_grid, text="📈 ANÁLISIS SEO\n(Competitividad)",
                     command=self.analyze_keyword_competitiveness, height=50,
                     fg_color=COLORS['error']).pack(fill="x", pady=(0, 8))

        # Sección 3: SCRAPING DIRECTO
        scraping_section = ctk.CTkFrame(buttons_container, fg_color=COLORS['primary'])
        scraping_section.pack(fill="x", pady=(0, 15))

        scraping_title = ctk.CTkLabel(scraping_section, text="🚀 SCRAPING DIRECTO",
                                     font=ctk.CTkFont(size=14, weight="bold"),
                                     text_color=COLORS['text_primary'])
        scraping_title.pack(pady=(10, 15))

        scraping_grid = ctk.CTkFrame(scraping_section, fg_color="transparent")
        scraping_grid.pack(fill="x", padx=15, pady=(0, 10))

        ctk.CTkButton(scraping_grid, text="🚀 IR A PESTAÑA SCRAPING\n(Con Keywords Actuales)",
                     command=self.go_to_scraping_with_current_keywords, height=50,
                     fg_color=COLORS['accent'], font=ctk.CTkFont(size=12, weight="bold")).pack(fill="x", pady=(0, 8))

        # Sección 4: EXPORTACIÓN
        export_section = ctk.CTkFrame(buttons_container, fg_color=COLORS['primary'])
        export_section.pack(fill="x", pady=(0, 10))

        export_title = ctk.CTkLabel(export_section, text="💾 EXPORTACIÓN AVANZADA",
                                   font=ctk.CTkFont(size=14, weight="bold"),
                                   text_color=COLORS['text_primary'])
        export_title.pack(pady=(10, 15))

        export_grid = ctk.CTkFrame(export_section, fg_color="transparent")
        export_grid.pack(fill="x", padx=15, pady=(0, 10))

        ctk.CTkButton(export_grid, text="📋 EXPORTAR KEYWORDS\n(TXT/CSV/JSON/XML)",
                     command=self.export_keywords_advanced, height=50,
                     fg_color=COLORS['info']).pack(fill="x", pady=(0, 8))

        # ===================== PANEL DERECH0: CONSOLA DESLIZABLE =====================

        # HEADER DE LA CONSOLA
        console_header = ctk.CTkFrame(right_panel, fg_color=COLORS['surface'], height=40)
        console_header.pack(fill="x", pady=(10, 0))
        console_header.pack_propagate(False)

        # Título y botón de toggle
        console_title_frame = ctk.CTkFrame(console_header, fg_color="transparent")
        console_title_frame.pack(fill="x", padx=10)

        # Variable para controlar el estado de la consola (plegada/desplegada)
        self.console_collapsed = ctk.BooleanVar(value=False)

        toggle_btn = ctk.CTkButton(console_title_frame, text="⬇️",
                                  command=self.toggle_console, width=30, height=20,
                                  font=ctk.CTkFont(size=10, weight="bold"))
        toggle_btn.pack(side="left")

        ctk.CTkLabel(console_title_frame, text="📋 CONSOLA DE ACTIVIDAD",
                    font=ctk.CTkFont(size=12, weight="bold")).pack(side="left", padx=10)

        # Menú de opciones para la consola
        console_menu = ctk.CTkFrame(console_title_frame, fg_color="transparent")
        console_menu.pack(side="right")

        ctk.CTkButton(console_menu, text="🧹 Limpiar",
                     command=self.clear_console, width=60, height=20,
                     font=ctk.CTkFont(size=9)).pack(side="left", padx=(0, 5))

        ctk.CTkButton(console_menu, text="💾 Guardar",
                     command=self.save_console_logs, width=60, height=20,
                     font=ctk.CTkFont(size=9)).pack(side="left")

        # ÁREA DE TEXTO DE LA CONSOLA (ESCODIBLE)
        self.console_frame = ctk.CTkFrame(right_panel, fg_color=COLORS['primary'])
        self.console_frame.pack(fill="both", expand=True, padx=10, pady=(5, 10))

        # ÁREA PRINCIPAL DE LA CONSOLA
        self.console_scroll = ctk.CTkScrollableFrame(self.console_frame, fg_color=COLORS['secondary'])
        self.console_scroll.pack(fill="both", expand=True, padx=5, pady=5)

        # Área de texto para logs
        self.console_text = ctk.CTkTextbox(self.console_scroll,
                                          font=ctk.CTkFont(family="Consolas", size=10),
                                          wrap="word")
        self.console_text.pack(fill="both", expand=True, padx=5, pady=5)

        # Inicializar consola con mensaje de bienvenida
        self.clear_console()

        # CONEXIÓN CON EL SISTEMA DE LOGGING GLOBAL
        # El sistema de logging ya está conectado al archivo, ahora también a la consola visual

        # Crear un handler personalizado para la consola visual
        class ConsoleHandler(logging.Handler):
            def __init__(self, console_callback):
                super().__init__()
                self.console_callback = console_callback
                self.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s', datefmt='%H:%M:%S'))

            def emit(self, record):
                try:
                    msg = self.format(record)
                    # Usar after para asegurar que se actualice en el thread principal
                    if hasattr(self.console_callback, 'after'):
                        self.console_callback.after(0, lambda: self.update_console(msg))
                    else:
                        self.update_console(msg)
                except:
                    pass

            def update_console(self, msg):
                try:
                    if hasattr(self.console_callback, 'console_text'):
                        self.console_callback.console_text.insert("end", msg + "\n")
                        self.console_callback.console_text.see("end")
                except:
                    pass

        # Añadir el handler personalizado a los loggers existentes
        console_handler = ConsoleHandler(self)
        console_handler.setLevel(logging.INFO)

        # Conectar con el logger del scraper
        if hasattr(self, 'scraper') and self.scraper and hasattr(self.scraper, 'logger'):
            self.scraper.logger.addHandler(console_handler)

    def toggle_console(self):
        """Alterna entre mostrar/ocultar la consola deslizable"""
        if self.console_collapsed.get():
            # Mostrar consola
            self.console_frame.pack(fill="both", expand=True, padx=10, pady=(5, 10))
            self.console_collapsed.set(False)
            # Cambiar ícono del botón también cambiaría aquí si se quiere
        else:
            # Ocultar consola
            self.console_frame.pack_forget()
            self.console_collapsed.set(True)

    def clear_console(self):
        """Limpia el contenido de la consola"""
        try:
            self.console_text.delete("1.0", "end")
            welcome_msg = f"""🖥️ CONSOLA DE ACTIVIDAD - Keyword Scraper Pro
{'='*60}
📅 {time.strftime('%d/%m/%Y %H:%M:%S')}
🎯 Listo para procesar keywords...

💡 Funciones disponibles:
• Importación de archivos TXT/CSV/JSON
• Generación de sugerencias con Google Suggest
• Creación de variantes long-tail
• Limpieza avanzada de keywords
• Análisis de competitividad SEO
• Scraping con Google API
• Exportación en múltiples formatos

📋 Todos los procesos se mostrarán aquí en tiempo real...
{'='*60}

"""
            self.console_text.insert("1.0", welcome_msg)
            self.console_text.see("end")
        except Exception as e:
            print(f"Error limpiando consola: {e}")

    def save_console_logs(self):
        """Guarda el contenido actual de la consola en un archivo"""
        try:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"consola_logs_{timestamp}.txt"

            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                initialfile=filename
            )

            if file_path:
                content = self.console_text.get("1.0", "end")
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)

                messagebox.showinfo("Éxito", f"Logs de consola guardados en:\n{file_path}")

        except Exception as e:
            messagebox.showerror("Error", f"Error guardando logs: {e}")
        
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

        title_label = ctk.CTkLabel(title_frame, text="🚀 Scraping en Tiempo Real",
                                  font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(side="left")

        # Indicador de estado
        self.scraping_status_label = ctk.CTkLabel(title_frame, text="⏸️ Listo para comenzar",
                                                 font=ctk.CTkFont(size=14, weight="bold"), text_color="orange")
        self.scraping_status_label.pack(side="right")

        # Información de configuración
        config_info = f"📊 Keywords: {len(self.keywords_list)} | 🎯 Dominio: {self.domain_entry.get() or 'Todos'} | 🌍 País: {self.country_var.get()} | 📄 Páginas: {int(self.pages_var.get())}"
        self.config_info_label = ctk.CTkLabel(header_frame, text=config_info, font=ctk.CTkFont(size=11))
        self.config_info_label.pack(anchor="w")

        # Frame de controles principales
        controls_frame = ctk.CTkFrame(main_frame)
        controls_frame.pack(fill="x", padx=10, pady=5)

        # Panel de costos mejorado
        costs_panel = ctk.CTkFrame(controls_frame)
        costs_panel.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(costs_panel, text="💰 Calculadora de Costos Google API", font=ctk.CTkFont(weight="bold")).pack(anchor="w", pady=(10,5))

        # Costos en filas separadas para mejor visualización
        costs_grid = ctk.CTkFrame(costs_panel)
        costs_grid.pack(fill="x", pady=(0, 10))

        # Inicializar contadores de costos
        self.total_consults = 0
        self.total_cost = 0.0
        self.today_consults = 0

        # Contadores visuales
        self.free_consults_label = ctk.CTkLabel(costs_grid, text="🟢 Consultas GRATIS (100/día): 100 restantes",
                                               font=ctk.CTkFont(size=12))
        self.free_consults_label.pack(anchor="w", pady=(0, 5))

        self.paid_consults_label = ctk.CTkLabel(costs_grid, text="🔴 Consultas PAGAS: $0.00",
                                               font=ctk.CTkFont(size=12))
        self.paid_consults_label.pack(anchor="w", pady=(0, 5))

        self.total_cost_label = ctk.CTkLabel(costs_grid, text="💸 Costo total estimado: $0.00",
                                            font=ctk.CTkFont(size=14, weight="bold"))
        self.total_cost_label.pack(anchor="w")

        # Información sobre cuotas
        quota_info = ctk.CTkLabel(costs_panel,
                                 text="ℹ️ 100 consultas gratis por día | $5 por cada 1000 consultas adicionales",
                                 font=ctk.CTkFont(size=10), text_color="gray")
        quota_info.pack(anchor="w", pady=(5, 10))

        # Botones de control mejorados
        buttons_frame = ctk.CTkFrame(controls_frame)
        buttons_frame.pack(fill="x", pady=(0, 10))

        # Botones en dos filas
        control_buttons_top = ctk.CTkFrame(buttons_frame)
        control_buttons_top.pack(fill="x", pady=(0, 5))

        self.start_button = ctk.CTkButton(control_buttons_top, text="🚀 Iniciar Scraping",
                                         command=self.start_scraping, fg_color="green", hover_color="dark green",
                                         height=40, font=ctk.CTkFont(size=12, weight="bold"))
        self.start_button.pack(side="left", padx=(0, 5), fill="x", expand=True)

        self.stop_button = ctk.CTkButton(control_buttons_top, text="⏹️ Detener",
                                        command=self.stop_scraping, fg_color="red", hover_color="dark red",
                                        height=40, font=ctk.CTkFont(size=12, weight="bold"),
                                        state="disabled")
        self.stop_button.pack(side="left")

        control_buttons_bottom = ctk.CTkFrame(buttons_frame)
        control_buttons_bottom.pack(fill="x")

        reset_button = ctk.CTkButton(control_buttons_bottom, text="🔄 Reiniciar Sesión",
                                    command=self.reset_session, fg_color="purple", hover_color="dark purple",
                                    height=35, font=ctk.CTkFont(size=11))
        reset_button.pack(side="left", padx=(0, 5), expand=True)

        test_api_button = ctk.CTkButton(control_buttons_bottom, text="🧪 Probar API",
                                       command=self.test_google_api, fg_color="orange", hover_color="dark orange",
                                       height=35, font=ctk.CTkFont(size=11))
        test_api_button.pack(side="left", padx=(0, 5), expand=True)

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

        self.progress_label = ctk.CTkLabel(progress_info_frame, text="⏸️ Esperando iniciar scraping...",
                                          font=ctk.CTkFont(size=12))
        self.progress_label.pack(side="left")

        # Estadísticas en tiempo real
        self.scraping_stats_label = ctk.CTkLabel(progress_info_frame,
                                                text="Keywords: 0 | Procesadas: 0 | Restantes: 0",
                                                font=ctk.CTkFont(size=10), text_color="gray")
        self.scraping_stats_label.pack(side="right")

        # Botones de control
        button_frame = ctk.CTkFrame(controls_frame)
        button_frame.pack(fill="x", pady=10)

        # Botones en fila: Reiniciar | Test API | Iniciar | Detener
        reset_button = ctk.CTkButton(button_frame, text="🔄 Reiniciar Sesión",
                                    command=self.reset_session,
                                    fg_color="purple", hover_color="dark purple")
        reset_button.pack(side="left", padx=5)

        test_api_button = ctk.CTkButton(button_frame, text="🧪 Probar API",
                                       command=self.test_google_api,
                                       fg_color="orange", hover_color="dark orange")
        test_api_button.pack(side="left", padx=5)

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
        """Configura la pestaña de resultados con bloques de estadísticas y mejor UI"""
        main_frame = ctk.CTkFrame(self.tab_results)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Header con título y información general
        header_frame = ctk.CTkFrame(main_frame)
        header_frame.pack(fill="x", padx=10, pady=(10, 5))

        title_frame = ctk.CTkFrame(header_frame)
        title_frame.pack(fill="x", pady=(0, 5))

        title_label = ctk.CTkLabel(title_frame, text="📊 RESULTADOS E INFORMES",
                                  font=ctk.CTkFont(size=22, weight="bold"))
        title_label.pack(side="left")

        # Información de sesión actual
        session_info = ctk.CTkLabel(title_frame, text="Sesión actual: Sin resultados",
                                   font=ctk.CTkFont(size=12))
        session_info.pack(side="right")
        self.session_info_label = session_info

        # BLOQUES DE ESTADÍSTICAS VISUALES
        stats_blocks_frame = ctk.CTkFrame(main_frame)
        stats_blocks_frame.pack(fill="x", padx=10, pady=(0, 10))

        # Crear grid de 4 bloques principales
        stats_grid = ctk.CTkFrame(stats_blocks_frame)
        stats_grid.pack(fill="x", padx=10, pady=10)

        # Bloque 1: Total de resultados
        self.total_results_block = self.create_stats_block(stats_grid, "📈 TOTAL RESULTADOS",
                                                          "0", "Sin datos", "blue")
        self.total_results_block.pack(side="left", fill="both", expand=True, padx=(0, 5))

        # Bloque 2: Posición promedio
        self.avg_position_block = self.create_stats_block(stats_grid, "🎯 POSICIÓN PROMEDIO",
                                                         "0.0", "Sin datos", "green")
        self.avg_position_block.pack(side="left", fill="both", expand=True, padx=(0, 5))

        # Bloque 3: Mejor posición
        self.best_position_block = self.create_stats_block(stats_grid, "🥇 MEJOR POSICIÓN",
                                                          "N/A", "Sin datos", "orange")
        self.best_position_block.pack(side="left", fill="both", expand=True, padx=(0, 5))

        # Bloque 4: Top 10 %
        self.top10_percentage_block = self.create_stats_block(stats_grid, "📊 EN TOP 10",
                                                             "0%", "Sin datos", "purple")
        self.top10_percentage_block.pack(side="left", fill="both", expand=True)

        # BLOQUES SECUNDARIOS DE MÉTRICAS
        secondary_stats_frame = ctk.CTkFrame(main_frame)
        secondary_stats_frame.pack(fill="x", padx=10, pady=(0, 10))

        secondary_grid = ctk.CTkFrame(secondary_stats_frame)
        secondary_grid.pack(fill="x", padx=10, pady=10)

        # Keywords únicas
        self.unique_keywords_block = self.create_stats_block(secondary_grid, "🔑 KEYWORDS ÚNICAS",
                                                            "0", "Sin datos", "cyan")
        self.unique_keywords_block.pack(side="left", fill="both", expand=True, padx=(0, 5))

        # Dominios únicos
        self.unique_domains_block = self.create_stats_block(secondary_grid, "🌐 DOMINIOS ÚNICOS",
                                                           "0", "Sin datos", "pink")
        self.unique_domains_block.pack(side="left", fill="both", expand=True, padx=(0, 5))

        # Consultas realizadas
        self.queries_used_block = self.create_stats_block(secondary_grid, "🔍 CONSULTAS USADAS",
                                                         "0", "Sin datos", "red")
        self.queries_used_block.pack(side="left", fill="both", expand=True, padx=(0, 5))

        # Costo estimado
        self.cost_estimate_block = self.create_stats_block(secondary_grid, "💰 COSTO ESTIMADO",
                                                          "$0.00", "Sin datos", "gold")
        self.cost_estimate_block.pack(side="left", fill="both", expand=True)

        # LISTADO DE REPORTES HISTÓRICOS
        reports_section = ctk.CTkFrame(main_frame)
        reports_section.pack(fill="x", padx=10, pady=(0, 10))

        reports_title_frame = ctk.CTkFrame(reports_section)
        reports_title_frame.pack(fill="x", padx=10, pady=(10, 5))

        ctk.CTkLabel(reports_title_frame, text="📂 HISTORIAL DE REPORTES",
                    font=ctk.CTkFont(size=16, weight="bold")).pack(side="left")

        # Botón para actualizar lista
        refresh_btn = ctk.CTkButton(reports_title_frame, text="🔄 Actualizar",
                                   command=self.update_reports_list, width=100)
        refresh_btn.pack(side="right")

        # Scrollable frame para lista de reportes
        self.reports_list_frame = ctk.CTkScrollableFrame(reports_section, height=120)
        self.reports_list_frame.pack(fill="x", padx=10, pady=5)

        # Inicializar lista de reportes
        self.update_reports_list()

        # CONTROLES PRINCIPALES
        controls_main_frame = ctk.CTkFrame(main_frame)
        controls_main_frame.pack(fill="x", padx=10, pady=(0, 5))

        # Panel izquierdo - Controles de datos actuales
        current_controls = ctk.CTkFrame(controls_main_frame)
        current_controls.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(current_controls, text="🎯 DATOS ACTUALES:",
                    font=ctk.CTkFont(weight="bold")).pack(anchor="w", pady=(10, 5))

        # Botones para datos actuales
        buttons_frame_current = ctk.CTkFrame(current_controls)
        buttons_frame_current.pack(fill="x", pady=(0, 10))

        ctk.CTkButton(buttons_frame_current, text="📊 Ver Detalles",
                     command=self.show_current_stats_detailed).pack(side="left", padx=(0, 5))
        ctk.CTkButton(buttons_frame_current, text="📈 Ir a Análisis",
                     command=self.go_to_analysis).pack(side="left", padx=(0, 5))
        ctk.CTkButton(buttons_frame_current, text="🧹 Limpiar Resultados",
                     command=self.clear_current_results).pack(side="left")

        # Panel derecho - Exportación
        export_controls = ctk.CTkFrame(controls_main_frame)
        export_controls.pack(side="right", fill="y")

        ctk.CTkLabel(export_controls, text="💾 EXPORTAR:",
                    font=ctk.CTkFont(weight="bold")).pack(anchor="w", pady=(10, 5))

        export_buttons = ctk.CTkFrame(export_controls)
        export_buttons.pack(fill="x", pady=(0, 10))

        ctk.CTkButton(export_buttons, text="📊 CSV",
                     command=lambda: self.export_results("csv")).pack(side="left", padx=(0, 2))
        ctk.CTkButton(export_buttons, text="📋 JSON",
                     command=lambda: self.export_results("json")).pack(side="left", padx=(0, 2))
        ctk.CTkButton(export_buttons, text="📈 Excel",
                     command=lambda: self.export_results("excel")).pack(side="left")

        # TABLA DE RESULTADOS DETALLADA
        table_section = ctk.CTkFrame(main_frame)
        table_section.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        table_header = ctk.CTkFrame(table_section)
        table_header.pack(fill="x", padx=10, pady=(10, 5))

        ctk.CTkLabel(table_header, text="📋 TABLA DETALLADA DE RESULTADOS",
                    font=ctk.CTkFont(size=16, weight="bold")).pack(side="left")

        # Filtros
        filter_frame = ctk.CTkFrame(table_header)
        filter_frame.pack(side="right")

        ctk.CTkLabel(filter_frame, text="🔍 Filtrar:").pack(side="left", padx=(5, 2))
        self.filter_entry = ctk.CTkEntry(filter_frame, placeholder_text="Buscar keyword...", width=200)
        self.filter_entry.pack(side="left", padx=2)
        ctk.CTkButton(filter_frame, text="🎯 Aplicar",
                     command=self.apply_filter).pack(side="left", padx=2)

        # Tabla con scrollbar
        table_frame = ctk.CTkFrame(table_section)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Crear treeview para mostrar resultados con ordenamiento
        columns = ("keyword", "position", "title", "domain", "page")
        self.results_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)

        # Diccionario para controlar el orden de sorting
        self.tree_sort_orders = {}
        self.current_results_backup = []  # Para mantener una copia cuando se ordene

        # Configurar columnas con click para ordenar
        self.setup_treeview_sortable("keyword", "Keyword")
        self.setup_treeview_sortable("position", "Posición")
        self.setup_treeview_sortable("title", "Título")
        self.setup_treeview_sortable("domain", "Dominio")
        self.setup_treeview_sortable("page", "Página")

        self.results_tree.column("keyword", width=180)
        self.results_tree.column("position", width=70)
        self.results_tree.column("title", width=280)
        self.results_tree.column("domain", width=130)
        self.results_tree.column("page", width=50)

        # Scrollbar para la tabla
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=scrollbar.set)

        self.results_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Mensaje de estado inferior
        status_frame = ctk.CTkFrame(main_frame)
        status_frame.pack(fill="x", padx=10, pady=(0, 10))

        self.results_status_label = ctk.CTkLabel(status_frame,
                                                text="⏳ Esperando resultados de scraping...",
                                                font=ctk.CTkFont(size=11))
        self.results_status_label.pack(pady=5)
        
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
        keywords_text = self.keywords_text.get("1.0", "end-1c")
        keywords_list = [k.strip() for k in keywords_text.split('\n') if k.strip()]
        self.keywords_list = keywords_list
        self.keywords_count_label.configure(text=str(len(keywords_list)))

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

    def test_google_api(self):
        """Prueba rápida las credenciales de Google API"""
        self.log_message("🧪 Probando credenciales de Google API...")

        api_key = self.api_key_var.get().strip()
        search_engine_id = self.search_engine_id_var.get().strip()

        if not api_key:
            messagebox.showwarning("Error", "No hay API Key configurada. Ve a la pestaña '🔐 Google API' y configura tus credenciales.")
            return

        if not search_engine_id:
            messagebox.showwarning("Error", "No hay Search Engine ID configurado. Ve a la pestaña '🔐 Google API' y configura tus credenciales.")
            return

        # Validar formato básico
        if not api_key.startswith("AIza"):
            messagebox.showwarning("Error", "La API Key debe comenzar con 'AIza'")
            return

        try:
            import requests
            # Probar una búsqueda simple
            url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={search_engine_id}&q=scraper&q=num=1"
            response = requests.get(url, timeout=10)

            if response.status_code == 200:
                data = response.json()
                if 'items' in data and len(data['items']) > 0:
                    result = data['items'][0]
                    messagebox.showinfo("✅ API Funcionando",
                                      f"✅ Las credenciales funcionan correctamente!\n\n"
                                      f"🔍 Búsqueda de prueba: '{result['title'][:50]}...'\n\n"
                                      f"🏆 Tu scraper está listo para funcionar! 🙌")
                    self.log_message(f"✅ API funcionando - Encontrado: {result['title']}")
                else:
                    messagebox.showinfo("📋 API Válida",
                                      "✅ Las credenciales son válidas pero no encontraron resultados para 'scraper'.\n\n"
                                      "Este es un comportamiento normal - significa que tus credenciales funcionan correctamente.")
                    self.log_message("✅ API válida pero sin resultados de prueba")
            elif response.status_code == 403:
                data = response.json()
                error_msg = data.get('error', {}).get('message', 'Error de autenticación')

                if "DAILY_LIMIT_EXCEEDED" in error_msg or "quota" in error_msg.lower():
                    messagebox.showwarning("⚠️ Límite Alcanzado",
                                         "Has alcanzado el límite diario de la API gratuita (100 consultas).\n\n"
                                         "💡 Puedes:\n"
                                         "• Esperar al día siguiente (se resetean las cuotas)\n"
                                         "• Actualizar a un plan pago de Google\n"
                                         "• Usar diferentes credenciales\n\n"
                                         "Las consultas funcionarán correctamente mañana.")

                else:
                    messagebox.showerror("❌ Error de API",
                                       f"❌ Error de autenticación: {error_msg}\n\n"
                                       "💡 Verifica tus credenciales en la pestaña '🔐 Google API'")
                self.log_message(f"❌ Error de API: {error_msg}")
            else:
                messagebox.showerror("❌ Error HTTP",
                                   f"❌ Error de conexión HTTP {response.status_code}\n\n"
                                   f"{response.text[:200]}")
                self.log_message(f"❌ Error HTTP {response.status_code}")

        except requests.exceptions.RequestException as e:
            messagebox.showerror("❌ Error de Conexión",
                               f"No se pudo conectar con Google API:\n{e}\n\n"
                               "💡 Verifica tu conexión a internet.")
            self.log_message(f"❌ Error de conexión: {e}")
        except Exception as e:
            messagebox.showerror("❌ Error",
                               f"Error desconocido: {e}")
            self.log_message(f"❌ Error inesperado: {e}")

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
        """Carga keywords desde archivo al editor principal"""
        try:
            file_path = filedialog.askopenfilename(
                filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv"), ("JSON files", "*.json"), ("All files", "*.*")]
            )

            if file_path:
                keywords = []

                if file_path.endswith('.csv'):
                    # Cargar desde CSV - buscar columna de keywords
                    import pandas as pd
                    try:
                        df = pd.read_csv(file_path)

                        # Buscar posibles columnas de keywords
                        possible_columns = ['keyword', 'keywords', 'kw', 'query', 'search_term']
                        keyword_col = None

                        for col in possible_columns:
                            if col in df.columns:
                                keyword_col = col
                                break

                        if keyword_col:
                            keywords = df[keyword_col].dropna().astype(str).tolist()
                        else:
                            # Tomar primera columna no numérica
                            for col in df.columns:
                                if df[col].dtype == 'object':
                                    keywords = df[col].dropna().astype(str).tolist()
                                    break

                        if not keywords:
                            keywords = [str(x) for x in df.iloc[:, 0].dropna().tolist()]

                    except Exception as e:
                        messagebox.showerror("Error", f"Error leyendo CSV: {e}")
                        return

                elif file_path.endswith('.json'):
                    # Cargar desde JSON
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)

                        # Buscar array de keywords en diferentes estructuras posibles
                        if isinstance(data, list):
                            keywords = [str(k) for k in data if k]
                        elif isinstance(data, dict):
                            # Buscar posibles claves
                            possible_keys = ['keywords', 'data', 'queries', 'items']
                            for key in possible_keys:
                                if key in data and isinstance(data[key], list):
                                    keywords = [str(k) for k in data[key] if k]
                                    break

                            # Si no encontramos array, intentar con valores
                            if not keywords:
                                keywords = [str(v) for v in data.values() if isinstance(v, (str, int, float))][:50]  # Máximo 50

                    except Exception as e:
                        messagebox.showerror("Error", f"Error leyendo JSON: {e}")
                        return

                else:
                    # Cargar desde archivo de texto plano
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                        # Intentar detectar formato (líneas separadas por \n o ,)
                        if ',' in content and '\n' not in content:
                            # Comma separated
                            keywords = [k.strip() for k in content.split(',') if k.strip()]
                        else:
                            # Line separated
                            keywords = [line.strip() for line in content.split('\n') if line.strip() and not line.strip().startswith('#')]

                # Filtrar y limpiar keywords
                processed_keywords = []
                ignored_lines = 0

                for kw in keywords:
                    clean_kw = kw.strip()
                    if clean_kw and len(clean_kw) >= 2:  # Mínimo 2 caracteres (útiles para SEO)
                        processed_keywords.append(clean_kw)
                    else:
                        ignored_lines += 1

                if processed_keywords:
                    # Establecer las keywords en el editor principal
                    self.set_current_keywords(processed_keywords)

                    # Actualizar estadísticas e integración
                    self.update_integration_status()

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
                                       f"Asegúrate de que el archivo contenga keywords de al menos 2 caracteres."
                                       )

        except Exception as e:
            messagebox.showerror("Error", f"Error cargando archivo:\n\n{str(e)}")
            
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
        
    def reset_session(self):
        """Reinicia la sesión completa - limpia resultados, contadores y formatos"""
        try:
            # Preguntar confirmación
            if not messagebox.askyesno("Reiniciar Sesión",
                                     "¿Estás seguro de reiniciar la sesión?\n\nSe perderán todos los resultados actuales."):
                return

            # Change UI state during reset
            self.scraping_status_label.configure(text="🔄 Reiniciando...", text_color="orange")
            self.progress_label.configure(text="🧹 Limpiando datos...")

            # Stop any running process
            if self.is_running:
                self.is_running = False
                self.log_message("⏹️ Proceso detenido para reiniciar")

            # Limpiar resultados actuales
            self.current_results = []
            self.keywords_list = []

            # Limpiar tablas
            if self.results_tree:
                for item in self.results_tree.get_children():
                    self.results_tree.delete(item)
                self.results_tree.delete(*self.results_tree.get_children())

            # Limpiar campos de keywords
            if self.keywords_text:
                self.keywords_text.delete("1.0", "end")
            self.keywords_count_label.configure(text="0")

            # Limpiar contadores de costos
            self.total_consults = 0
            self.total_cost = 0.0
            self.today_consults = 0
            self.update_cost_display()

            # Limpiar área de logs
            if self.logs_text:
                self.logs_text.configure(state="normal")
                self.logs_text.delete("1.0", "end")
                self.logs_text.insert("1.0", f"🔄 SESIÓN REINICIADA - {time.strftime('%H:%M:%S %d/%m/%Y')}\n")
                self.logs_text.insert("1.0", "="*60 + "\n")
                self.logs_text.configure(state="disabled")

            # Limpiar estadísticas
            if hasattr(self, 'stats_label') and self.stats_label:
                self.stats_label.configure(text="Total resultados: 0 | Keywords únicas: 0 | Posición promedio: 0.0")

            # Limpiar gráficos de análisis
            try:
                if hasattr(self, 'fig') and hasattr(self, 'canvas'):
                    for ax in [self.ax1, self.ax2, self.ax3, self.ax4]:
                        ax.clear()
                    self.canvas.draw()
            except:
                pass

            # Reiniciar barra de progreso
            self.progress_bar.set(0)

            # Limpiar dominio
            if self.domain_entry:
                self.domain_entry.delete(0, "end")

            # Actualizar información de configuración
            self.update_config_info()

            # Reset button states
            self.start_button.configure(state="normal", text="🚀 Iniciar Scraping")
            self.stop_button.configure(state="disabled")

            # Update status labels
            self.scraping_status_label.configure(text="⏸️ Listo para comenzar", text_color="orange")
            self.progress_label.configure(text="Listo para comenzar")
            self.scraping_stats_label.configure(text="Keywords: 0 | Procesadas: 0 | Restantes: 0")

            self.log_message("✅ Sesión reiniciada completamente")
            messagebox.showinfo("Sesión Reiniciada",
                              "¡Sesión reiniciada exitosamente!\n\nResultado y configuración limpiados.")

        except Exception as e:
            self.log_message(f"❌ Error reiniciando sesión: {e}")
            messagebox.showerror("Error", f"Error reiniciando sesión: {e}")

    def stop_scraping(self):
        """Detiene el proceso de scraping"""
        self.is_running = False
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.log_message("⏹️ Scraping detenido por el usuario")
        
    def scraping_thread(self):
        """Hilo principal de scraping con actualizaciones en tiempo real mejoradas"""
        try:
            # Actualizar estado inicial
            self.scraping_status_label.configure(text="⚙️ Configurando...", text_color="blue")
            self.log_message("🚀 Iniciando scraping...")
            time.sleep(0.5)  # Pequeña pausa para mostrar el estado

            # Resetear contadores de sesión actual
            session_consults = 0
            session_cost = 0.0

            # Actualizar estado: creando scraper
            self.scraping_status_label.configure(text="🔧 Creando scraper...", text_color="orange")
            self.progress_label.configure(text="Configurando scraper...")

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

            # Actualizar estado: listo para scrapear
            self.scraping_status_label.configure(text="🚀 Scraping activo", text_color="green")
            self.log_message(f"📋 Preparado para procesar {len(self.keywords_list)} keywords")

            # Ejecutar scraping (esto toma tiempo)
            target_domain = self.domain_entry.get().strip() or None
            self.progress_label.configure(text="🕐 Ejecutando búsquedas en Google...")

            results = self.scraper.batch_position_check(
                self.keywords_list,
                target_domain,
                int(self.pages_var.get())
            )

            if results and self.is_running:
                # Actualizar estado: procesando resultados
                self.scraping_status_label.configure(text="📊 Procesando resultados...", text_color="blue")
                self.progress_label.configure(text="📈 Analizando resultados...")

                self.current_results = results

                # Calcular costos de esta sesión
                pages_scraped = int(self.pages_var.get())
                keywords_count = len(self.keywords_list)
                session_consults = pages_scraped * keywords_count

                # Calcular costo (100 gratis, $5 por cada 1000 adicionales)
                if session_consults <= 100:
                    session_cost = 0.0
                else:
                    paid_consults = session_consults - 100
                    session_cost = (paid_consults / 1000) * 5.0

                # Actualizar contadores globales
                self.today_consults += session_consults
                self.total_consults += session_consults
                self.total_cost += session_cost

                # Actualizar display de costos
                self.update_cost_display()

            # Actualizar interfaz con resultados
            self.update_results_table()
            self.update_stats()

            # Actualizar bloques de estadísticas si están disponibles
            try:
                self.update_stats_blocks()
            except:
                pass  # No hay problema si no existen aún

            # Actualizar estado: completado
            self.scraping_status_label.configure(text="✅ Completado", text_color="green")
            self.progress_label.configure(text="✅ Scraping completado exitosamente")

            self.log_message(f"✅ Scraping completado: {len(results)} resultados encontrados")
            self.log_message(f"💰 Costo de sesión: ${session_cost:.2f} ({session_consults} consultas realizadas)")

            # GENERAR INFORME COMPLETO DESPUÉS DEL SCRAPING
            self.log_message("📊 Generando informe completo después del scraping...")
            self.progress_label.configure(text="📊 Generando informe completo...")

            try:
                # Crear dataframe para análisis más detallado
                results_df = pd.DataFrame(results)
                results_df['fecha_scraping'] = time.strftime("%Y-%m-%d %H:%M:%S")
                results_df['dominio_objetivo'] = target_domain or "Todos"
                results_df['pais'] = self.country_var.get()
                results_df['idioma'] = self.language_var.get()

                # Guardar resultados automáticamente
                self.progress_label.configure(text="💾 Guardando resultados...")
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                domain_suffix = f"_{target_domain.replace('.', '_')}" if target_domain else "_todos"
                base_filename = f"scraping{len(self.keywords_list)}_{domain_suffix}_{timestamp}"

                # Guardar múltiples formatos
                csv_filename = f"{base_filename}.csv"
                self.scraper.save_results(results, csv_filename.replace('.csv', ''))

                # Guardar también como JSON para compatibilidad total
                json_filename = f"data/{base_filename}.json"
                with open(json_filename, 'w', encoding='utf-8') as f:
                    json.dump(results, f, indent=2, ensure_ascii=False)

                # Crear informe resumen en CSV adicional
                summary_data = {
                    'fecha_scraping': time.strftime("%Y-%m-%d %H:%M:%S"),
                    'timestamp': timestamp,
                    'dominio_objetivo': target_domain or "Todos",
                    'keywords_procesadas': len(self.keywords_list),
                    'resultados_encontrados': len(results),
                    'posicion_promedio': results_df['position'].mean() if len(results) > 0 else 0,
                    'mejor_posicion': results_df['position'].min() if len(results) > 0 else 0,
                    'top10_resultados': len(results_df[results_df['position'] <= 10]) if len(results) > 0 else 0,
                    'dominios_unicos': results_df['domain'].nunique() if len(results) > 0 else 0,
                    'consultas_realizadas': session_consults,
                    'costo_estimado': session_cost,
                    'pais': self.country_var.get(),
                    'idioma': self.language_var.get(),
                    'archivo_csv': csv_filename,
                    'archivo_json': json_filename
                }

                summary_df = pd.DataFrame([summary_data])
                summary_filename = f"data/{base_filename}_resumen.csv"
                summary_df.to_csv(summary_filename, index=False)

                self.log_message("💾 INFORME COMPLETO GENERADO:")
                self.log_message(f"   📊 {csv_filename} ({len(results)} resultados)")
                self.log_message(f"   🗂️  {json_filename} ({len(results)} resultados)")
                self.log_message(f"   📋 {summary_filename} (resumen ejecutivo)")

                # Actualizar lista de reportes si está disponible
                try:
                    self.update_reports_list()
                except:
                    pass

                # Cambiar a pestaña de resultados y mostrar información
                self.tabview.set("📊 Resultados")

                # Actualizar información de sesión
                self.session_info_label.configure(text=f"Scraping completado: {len(results)} resultados")

                # Actualizar estado final
                self.results_status_label.configure(text=f"✅ Scraping finalizado - Informe guardado en 'data/{csv_filename}'")

                messagebox.showinfo("✅ Scraping Completado",
                                  f"¡Scraping completado exitosamente!\n\n"
                                  f"📊 Resultados encontrados: {len(results)}\n"
                                  f"🔑 Keywords procesadas: {len(self.keywords_list)}\n"
                                  f"💾 Archivos guardados en carpeta 'data/'\n\n"
                                  f"• {csv_filename}\n"
                                  f"• {json_filename}\n"
                                  f"• {summary_filename}\n\n"
                                  f"Los resultados están disponibles en la pestaña de Resultados.")

            except Exception as e:
                self.log_message(f"⚠️ Error generando informe: {str(e)[:80]}")
                messagebox.showwarning("Aviso", f"El scraping se completó, pero hubo un problema generando el informe:\n\n{str(e)}")

            # Mostrar resumen final
            self.progress_label.configure(text=f"🏆 ¡Completado! {len(results)} posiciones encontradas")
            self.scraping_stats_label.configure(text="Procesadas: 100% | Informe: ✓")

        except Exception as e:
            self.scraping_status_label.configure(text="❌ Error", text_color="red")
            self.progress_label.configure(text="❌ Error durante el scraping")
            self.log_message(f"❌ Error en scraping: {e}")

            # Mostrar mensaje de error
            import tkinter.messagebox as messagebox
            messagebox.showerror("Error en Scraping", f"Ocurrió un error durante el scraping:\n\n{str(e)}")

        finally:
            # Restaurar estado de botones
            self.start_button.configure(state="normal", text="🚀 Iniciar Scraping")
            self.stop_button.configure(state="disabled")
            self.is_running = False
            self.progress_bar.set(0)
            self.scraping_stats_label.configure(text="Listo para nuevo scraping")
            
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
            
    def setup_treeview_sortable(self, col_name, display_name):
        """Configura una columna sortable en Treeview"""
        # Configurar heading con ícono de sort
        def sort_column():
            if col_name in self.tree_sort_orders:
                self.tree_sort_orders[col_name] = not self.tree_sort_orders[col_name]
            else:
                self.tree_sort_orders[col_name] = True

            # Aplicar ordenamiento
            self.sort_treeview_column(col_name, self.tree_sort_orders[col_name])

        self.results_tree.heading(col_name, text=f"{display_name} ▼", command=sort_column)

    # ========== MÉTODOS PARA INTEGRACIÓN ENTRE PESTAÑAS ==========

    def go_to_scraping_with_current_keywords(self):
        """Cambia a pestaña de scraping transfiriendo las keywords actuales"""
        # Obtener keywords del editor principal
        current_keywords = self.get_current_keywords()

        if not current_keywords:
            messagebox.showwarning("Sin Keywords", "No hay keywords en el editor principal.\n\nAgrega keywords primero antes de scrapear.")
            return

        # Cambiar a pestaña de scraping
        self.tabview.set("🚀 Scraping")

        # Confirmar transferencia
        transfer_msg = f"✅ Cambiado a Scraping con {len(current_keywords)} keywords transferidas\n\nPuedes iniciar el scraping directamente."
        messagebox.showinfo("Transferencia Exitosa", transfer_msg)

        self.update_integration_status()
        self.log_message(f"🔄 Transferidas {len(current_keywords)} keywords a pestaña de scraping")

    def copy_keywords_to_scraping(self):
        """Copia las keywords actuales del editor al sistema de scraping sin cambiar pestaña"""
        current_keywords = self.get_current_keywords()

        if not current_keywords:
            messagebox.showwarning("Sin Keywords", "No hay keywords para copiar.")
            return

        # Actualizar keywords para scraping
        self.keywords_list = current_keywords.copy()

        # Mostrar confirmación sin cambiar de pestaña
        self.update_integration_status()

        # Mostrar mensaje breve
        copy_msg = f"📋 Copiadas {len(current_keywords)} keywords al sistema de scraping"
        self.status_integration_label.configure(text="ACTUALIZADO", text_color="white")
        self.status_integration_block.configure(fg_color=COLORS['success'])

        # Resetear después de 3 segundos
        def reset_status():
            time.sleep(3)
            self.root.after(0, lambda: self.status_integration_label.configure(text="LISTO"))
            self.root.after(0, lambda: self.status_integration_block.configure(fg_color=COLORS['accent']))

        threading.Thread(target=reset_status, daemon=True).start()

        self.log_message(f"📋 Copiadas {len(current_keywords)} keywords para scraping")

    def get_current_keywords(self):
        """Obtiene las keywords actuales del editor principal"""
        text = self.main_keywords_text.get("1.0", "end-1c").strip()

        # Si está vacío o solo tiene comentario, obtener del editor secundario
        if not text or text.startswith("#") and len(text.split('\n')) <= 2:
            text = self.keywords_text.get("1.0", "end-1c")

        keywords = [k.strip() for k in text.split('\n') if k.strip() and not k.strip().startswith('#')]
        return keywords

    def set_current_keywords(self, keywords_list):
        """Establece keywords en el editor principal"""
        if keywords_list:
            filtered_keywords = [k for k in keywords_list if k.strip()]
            self.main_keywords_text.delete("1.0", "end")
            self.main_keywords_text.insert("1.0", "\n".join(filtered_keywords))

            # Actualizar estadísticas
            self.update_keywords_stats()
            self.update_integration_status()

    def update_integration_status(self):
        """Actualiza el estado de integración entre pestañas"""
        main_kw = len(self.get_current_keywords())

        # Actualizar contador principal
        if hasattr(self, 'status_editor_count'):
            self.status_editor_count.configure(text=str(main_kw))

        # Actualizar contador de procesadas (por ahora mismo valor)
        if hasattr(self, 'status_processed_count'):
            processed = len([k for k in self.processed_keywords if k in self.get_current_keywords()])
            self.status_processed_count.configure(text=str(processed if processed > 0 else main_kw))

        # Actualizar costo estimado
        if main_kw > 0:
            # Estimar costo básico
            pages = int(self.pages_var.get()) if hasattr(self, 'pages_var') else 1
            estimated_cost = (main_kw * pages * 0.005)  # Costo aproximado
            if estimated_cost <= 0.5:  # Gratis si <= $0.50
                estimated_cost = 0.0

            if hasattr(self, 'status_cost_label'):
                if estimated_cost > 0:
                    self.status_cost_label.configure(text=f"${estimated_cost:.2f}")
                else:
                    self.status_cost_label.configure(text="$0.00")

    # ========== MÉTODOS PARA FUNCIONES NUEVAS EN KEYWORDS ==========

    def advanced_keyword_cleaning(self):
        """Limpieza avanzada de keywords con múltiples opciones"""
        current_keywords = self.get_current_keywords()

        if not current_keywords:
            messagebox.showwarning("Advertencia", "No hay keywords para limpiar")
            return

        def clean_keywords():
            keywords = current_keywords.copy()
            original_count = len(keywords)

            # Limpiar duplicados (ignorando mayúsculas/minúsculas)
            seen = set()
            cleaned = []
            for kw in keywords:
                lower_kw = kw.lower()
                if lower_kw not in seen and lower_kw.strip():
                    cleaned.append(kw)
                    seen.add(lower_kw)

            # Eliminar palabras vacías comunes (stop words) en español e inglés
            stop_words = {
                'spanish': ['el', 'la', 'los', 'las', 'un', 'una', 'unos', 'unas', 'y', 'o', 'pero', 'que', 'como', 'si', 'porque', 'cuando', 'donde', 'quien', 'cual', 'cuales', 'este', 'esta', 'estos', 'estas', 'aquel', 'aquella', 'aquellos', 'aquellas', 'de', 'del', 'al', 'con', 'por', 'para', 'sin', 'sobre', 'tras', 'durante', 'mediante', 'desde', 'hasta', 'a', 'en', 'entre', 'hacia', 'contra', 'desde'],
                'english': ['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'shall', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them', 'this', 'that', 'these', 'those', 'what', 'which', 'who', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very']
            }

            all_stop_words = stop_words['spanish'] + stop_words['english']
            filtered = []
            removed_stop_words = 0

            for kw in cleaned:
                words = re.findall(r'\b\w+\b', kw.lower())
                if not all(word in all_stop_words for word in words):
                    filtered.append(kw)
                else:
                    removed_stop_words += 1

            # Filtrar keywords demasiado cortas (menos de 3 caracteres)
            final_keywords = [kw for kw in filtered if len(kw.strip()) >= 3]
            too_short_removed = len(filtered) - len(final_keywords)

            # Actualizar interfaz con keywords limpias
            if final_keywords:
                self.set_current_keywords(final_keywords)
                self.processed_keywords.extend(final_keywords)
                self.update_integration_status()

                removed_total = original_count - len(final_keywords)
                messagebox.showinfo("Limpieza Completada",
                                  f"✅ Limpieza avanzada completada!\n\n"
                                  f"📊 Keywords originales: {original_count}\n"
                                  f"📋 Keywords finales: {len(final_keywords)}\n"
                                  f"🗑️ Eliminadas: {removed_total}\n"
                                  f"   • Duplicadas: {original_count - len(cleaned)}\n"
                                  f"   • Stop words: {removed_stop_words}\n"
                                  f"   • Muy cortas: {too_short_removed}\n")

                self.log_message(f"🧹 Limpieza avanzada: {original_count} → {len(final_keywords)} keywords")
            else:
                messagebox.showwarning("Sin Keywords", "La limpieza eliminó todas las keywords.\n\nConsidera revisar tus criterios de filtrado.")

        # Ejecutar limpieza
        clean_keywords()

    def sort_treeview_column(self, col_name, reverse=False):
        """Ordena la columna específica del Treeview"""
        # Obtener datos de la tabla
        l = [(self.results_tree.set(k, col_name), k) for k in self.results_tree.get_children('')]

        # Determinar tipo de ordenamiento
        if col_name == 'position':
            # Ordenar numéricamente
            l.sort(key=lambda t: int(t[0]) if t[0].isdigit() else 0, reverse=reverse)
        elif col_name == 'page':
            # Ordenar numéricamente
            l.sort(key=lambda t: int(t[0]) if t[0].isdigit() else 0, reverse=reverse)
        else:
            # Ordenar alfabéticamente
            l.sort(key=lambda t: t[0].lower(), reverse=reverse)

        # Reordenar elementos
        for index, (val, k) in enumerate(l):
            self.results_tree.move(k, '', index)

        # Actualizar ícono del heading
        for col in ['keyword', 'position', 'title', 'domain', 'page']:
            symbol = " ▲" if self.tree_sort_orders.get(col, False) else " ▼"
            display_name = {
                'keyword': 'Keyword',
                'position': 'Posición',
                'title': 'Título',
                'domain': 'Dominio',
                'page': 'Página'
            }.get(col, col)
            self.results_tree.heading(col, text=f"{display_name}{symbol if col == col_name else ' ▼'}")

    def load_previous_report(self):
        """Carga un informe CSV previo para ver históricamente"""
        try:
            # Listar archivos CSV en data/
            data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')

            if not os.path.exists(data_dir):
                messagebox.showwarning("Aviso", "No hay directorio data/ con informes previos")
                return

            csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]

            if not csv_files:
                messagebox.showwarning("Aviso", "No hay archivos CSV en data/")
                return

            # Mostrar diálogo para seleccionar archivo
            report_window = ctk.CTkToplevel(self.root)
            report_window.title("Seleccionar Informe Previo")
            report_window.geometry("400x300")
            report_window.transient(self.root)
            report_window.grab_set()

            title_label = ctk.CTkLabel(report_window, text="📂 Selecciona un informe previo:",
                                     font=ctk.CTkFont(size=16, weight="bold"))
            title_label.pack(pady=(20, 10))

            # Frame con scrollbar para lista de archivos
            files_frame = ctk.CTkScrollableFrame(report_window)
            files_frame.pack(fill="both", expand=True, padx=20, pady=10)

            def load_selected_file(filename):
                try:
                    file_path = os.path.join(data_dir, filename)
                    df = pd.read_csv(file_path)

                    # Convertir a formato compatible con la aplicación
                    results = df.to_dict('records')

                    # Limpiar tabla y agregar nuevos datos
                    for item in self.results_tree.get_children():
                        self.results_tree.delete(item)

                    for result in results:
                        self.results_tree.insert("", "end", values=(
                            result.get('keyword', ''),
                            result.get('position', 0),
                            result.get('title', '')[:80] + "..." if len(result.get('title', '')) > 80 else result.get('title', ''),
                            result.get('domain', ''),
                            result.get('page', 1)
                        ))

                    # Actualizar estadísticas con los datos cargados
                    self.current_results = results
                    self.update_stats()

                    self.log_message(f"✅ Cargado informe previo: {filename} ({len(results)} resultados)")
                    report_window.destroy()

                except Exception as e:
                    messagebox.showerror("Error", f"Error cargando archivo: {e}")

            # Crear botones para cada archivo CSV
            for csv_file in sorted(csv_files, reverse=True):  # Más recientes primero
                file_button = ctk.CTkButton(
                    files_frame,
                    text=f"{csv_file}",
                    command=lambda f=csv_file: load_selected_file(f)
                )
                file_button.pack(fill="x", pady=2)

        except Exception as e:
            messagebox.showerror("Error", f"Error listando archivos: {e}")

    def show_detailed_stats(self):
        """Muestra estadísticas detalladas en una ventana emergente"""
        if not self.current_results:
            messagebox.showwarning("Aviso", "No hay resultados para mostrar estadísticas")
            return

        try:
            df = pd.DataFrame(self.current_results)

            # Ventana de estadísticas
            stats_window = ctk.CTkToplevel(self.root)
            stats_window.title("📊 Estadísticas Detalladas")
            stats_window.geometry("600x500")
            stats_window.transient(self.root)

            # Título
            ctk.CTkLabel(stats_window, text="📈 Estadísticas Detalladas del Scraping",
                        font=ctk.CTkFont(size=18, weight="bold")).pack(pady=20)

            # Frame scrollable con estadísticas
            stats_scroll = ctk.CTkScrollableFrame(stats_window)
            stats_scroll.pack(fill="both", expand=True, padx=20, pady=10)

            # Estadísticas generales
            general_frame = ctk.CTkFrame(stats_scroll)
            general_frame.pack(fill="x", pady=10)

            ctk.CTkLabel(general_frame, text="📊 Estadísticas Generales:",
                        font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=5)

            # Calcular métricas
            total_results = len(df)
            unique_keywords = df['keyword'].nunique()
            avg_position = df['position'].mean() if 'position' in df.columns else 0
            best_position = df['position'].min() if 'position' in df.columns and len(df) > 0 else 0
            worst_position = df['position'].max() if 'position' in df.columns and len(df) > 0 else 0

            metrics = [
                f"Total de resultados: {total_results}",
                f"Keywords únicas: {unique_keywords}",
                f"Posición promedio: {avg_position:.2f}",
                f"Mejor posición: {best_position}",
                f"Peor posición: {worst_position}",
            ]

            for metric in metrics:
                ctk.CTkLabel(general_frame, text=f"• {metric}").pack(anchor="w")

            # Distribucion por posiciones
            if 'position' in df.columns:
                pos_frame = ctk.CTkFrame(stats_scroll)
                pos_frame.pack(fill="x", pady=10)

                ctk.CTkLabel(pos_frame, text="🎯 Distribución por Posiciones:",
                            font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=5)

                # Contar por rangos
                top3 = len(df[df['position'] <= 3])
                top10 = len(df[df['position'] <= 10])
                top20 = len(df[df['position'] <= 20])
                beyond20 = len(df[df['position'] > 20])

                ranges = [
                    f"Top 3: {top3} resultados ({(top3/total_results*100):.1f}%)",
                    f"Top 10: {top10} resultados ({(top10/total_results*100):.1f}%)",
                    f"Top 20: {top20} resultados ({(top20/total_results*100):.1f}%)",
                    f"Beyond 20: {beyond20} resultados ({(beyond20/total_results*100):.1f}%)",
                ]

                for range_info in ranges:
                    ctk.CTkLabel(pos_frame, text=f"• {range_info}").pack(anchor="w")

            # Top dominios
            if 'domain' in df.columns:
                domain_frame = ctk.CTkFrame(stats_scroll)
                domain_frame.pack(fill="x", pady=10)

                ctk.CTkLabel(domain_frame, text="🏆 Top Dominios:",
                            font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=5)

                top_domains = df['domain'].value_counts().head(10)

                for domain, count in top_domains.items():
                    percentage = (count / total_results) * 100
                    ctk.CTkLabel(domain_frame,
                                text=f"• {domain}: {count} resultados ({percentage:.1f}%)").pack(anchor="w")

            # Distribución por páginas
            if 'page' in df.columns:
                page_frame = ctk.CTkFrame(stats_scroll)
                page_frame.pack(fill="x", pady=10)

                ctk.CTkLabel(page_frame, text="📄 Distribución por Páginas:",
                            font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=5)

                page_stats = df['page'].value_counts().sort_index()

                for page, count in page_stats.items():
                    percentage = (count / total_results) * 100
                    ctk.CTkLabel(page_frame,
                                text=f"• Página {page}: {count} resultados ({percentage:.1f}%)").pack(anchor="w")

        except Exception as e:
            messagebox.showerror("Error", f"Error generando estadísticas: {e}")

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

    # ========== MÉTODOS PARA BLOQUES DE ESTADÍSTICAS ==========

    def create_stats_block(self, parent, title, value, subtitle, color):
        """Crea un bloque de estadísticas visual con título, valor y subtítulo"""
        block_frame = ctk.CTkFrame(parent, fg_color=color)

        # Título del bloque
        title_label = ctk.CTkLabel(block_frame, text=title,
                                  font=ctk.CTkFont(size=11, weight="bold"),
                                  text_color="white")
        title_label.pack(anchor="w", padx=8, pady=(8, 2))

        # Valor principal (grande y destacado)
        value_label = ctk.CTkLabel(block_frame, text=str(value),
                                  font=ctk.CTkFont(size=24, weight="bold"),
                                  text_color="white")
        value_label.pack(anchor="center", pady=(2, 2))

        # Subtítulo descriptivo
        subtitle_label = ctk.CTkLabel(block_frame, text=subtitle,
                                     font=ctk.CTkFont(size=9),
                                     text_color="lightgray")
        subtitle_label.pack(anchor="center", padx=8, pady=(2, 8))

        # Retornar el frame completo para poder actualizarlo después
        block_frame.value_label = value_label
        block_frame.subtitle_label = subtitle_label

        return block_frame

    def update_reports_list(self):
        """Actualiza la lista de reportes históricos disponibles"""
        try:
            # Limpiar lista anterior
            for widget in self.reports_list_frame.winfo_children():
                widget.destroy()

            # Listar archivos en data/
            data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')

            if not os.path.exists(data_dir):
                ctk.CTkLabel(self.reports_list_frame, text="📁 No hay carpeta 'data/'").pack(pady=10)
                return

            # Buscar archivos relevantes (.csv y .json)
            files = []
            for filename in os.listdir(data_dir):
                if filename.endswith(('.csv', '.json')):
                    filepath = os.path.join(data_dir, filename)
                    if os.path.isfile(filepath):
                        # Obtener información del archivo
                        file_stats = os.stat(filepath)
                        mod_time = time.ctime(file_stats.st_mtime)
                        file_size = file_stats.st_size

                        files.append({
                            'name': filename,
                            'path': filepath,
                            'size': file_size,
                            'modified': mod_time,
                            'type': filename.split('.')[-1].upper()
                        })

            # Ordenar por fecha de modificación (más reciente primero)
            files.sort(key=lambda x: x['modified'], reverse=True)

            if not files:
                ctk.CTkLabel(self.reports_list_frame, text="📄 No hay reportes guardados").pack(pady=10)
                return

            # Crear un frame por archivo
            for file_info in files[:10]:  # Mostrar máximo 10 archivos
                file_frame = ctk.CTkFrame(self.reports_list_frame)
                file_frame.pack(fill="x", pady=2, padx=5)

                # Información del archivo (en horizontal)
                info_frame = ctk.CTkFrame(file_frame)
                info_frame.pack(fill="x", padx=8, pady=5)

                # Nombre del archivo y tipo
                name_col = ctk.CTkFrame(info_frame)
                name_col.pack(side="left", fill="y")

                ctk.CTkLabel(name_col, text=f"📄 {file_info['name']}",
                            font=ctk.CTkFont(size=11, weight="bold")).pack(anchor="w")

                type_label = ctk.CTkLabel(name_col, text=f"{file_info['type']} • {file_info['size']} bytes",
                                         font=ctk.CTkFont(size=9), text_color="gray")
                type_label.pack(anchor="w")

                # Fecha y botones
                actions_col = ctk.CTkFrame(info_frame)
                actions_col.pack(side="right", fill="y")

                # Fecha de modificación
                date_str = time.strftime("%d/%m %H:%M", time.strptime(file_info['modified']))
                date_label = ctk.CTkLabel(actions_col, text=date_str,
                                         font=ctk.CTkFont(size=9), text_color="gray")
                date_label.pack(anchor="e", pady=(0, 2))

                # Botón de acción
                action_btn = ctk.CTkButton(actions_col, text="▶️ Cargar",
                                          command=lambda f=file_info: self.load_historical_report(f),
                                          height=25, width=80,
                                          font=ctk.CTkFont(size=10))
                action_btn.pack(anchor="e")

        except Exception as e:
            self.log_message(f"⚠️ Error actualizando lista de reportes: {str(e)[:50]}")

    def load_historical_report(self, file_info):
        """Carga un reporte histórico basado en la información del archivo"""
        try:
            filepath = file_info['path']
            filename = file_info['name']

            self.log_message(f"📂 Cargando reporte histórico: {filename}")

            # Cargar según el tipo de archivo
            if filename.endswith('.csv'):
                df = pd.read_csv(filepath)
            elif filename.endswith('.json'):
                df = pd.read_json(filepath)
            else:
                messagebox.showerror("Error", "Tipo de archivo no soportado")
                return

            # Convertir a formato compatible con la aplicación
            results = df.to_dict('records')

            # Actualizar resultados actuales
            self.current_results = results

            # Actualizar tabla de resultados
            self.update_results_table()

            # Actualizar bloques de estadísticas
            self.update_stats_blocks()

            # Actualizar pestaña de análisis
            self.update_charts()

            # Actualizar información de sesión
            if hasattr(self, 'session_info_label'):
                self.session_info_label.configure(text=f"Informe cargado: {filename}")

            # Actualizar estado
            if hasattr(self, 'results_status_label'):
                self.results_status_label.configure(text=f"✅ Reporte '{filename}' cargado exitosamente")

            self.log_message(f"✅ Reporte histórico cargado: {len(results)} resultados")

        except Exception as e:
            messagebox.showerror("Error", f"Error cargando el reporte:\n\n{str(e)}")
            self.log_message(f"❌ Error cargando reporte: {str(e)[:80]}")

    def update_stats_blocks(self):
        """Actualiza todos los bloques de estadísticas con los datos actuales"""
        if not self.current_results:
            # Valores por defecto cuando no hay datos
            self.total_results_block.value_label.configure(text="0")
            self.total_results_block.subtitle_label.configure(text="Sin resultados")

            self.avg_position_block.value_label.configure(text="0.0")
            self.avg_position_block.subtitle_label.configure(text="Sin datos")

            self.best_position_block.value_label.configure(text="N/A")
            self.best_position_block.subtitle_label.configure(text="Sin datos")

            self.top10_percentage_block.value_label.configure(text="0%")
            self.top10_percentage_block.subtitle_label.configure(text="Sin datos")

            self.unique_keywords_block.value_label.configure(text="0")
            self.unique_keywords_block.subtitle_label.configure(text="Sin datos")

            self.unique_domains_block.value_label.configure(text="0")
            self.unique_domains_block.subtitle_label.configure(text="Sin datos")

            self.queries_used_block.value_label.configure(text="0")
            self.queries_used_block.subtitle_label.configure(text="Sin datos")

            self.cost_estimate_block.value_label.configure(text="$0.00")
            self.cost_estimate_block.subtitle_label.configure(text="Sin datos")

            return

        try:
            df = pd.DataFrame(self.current_results)

            # Calcular métricas
            total_results = len(df)
            unique_keywords = df['keyword'].nunique() if 'keyword' in df.columns else 0
            avg_position = df['position'].mean() if 'position' in df.columns else 0
            best_position = df['position'].min() if 'position' in df.columns else 0
            unique_domains = df['domain'].nunique() if 'domain' in df.columns else 0

            # Calcular porcentaje en top 10
            top10_count = len(df[df['position'] <= 10]) if 'position' in df.columns else 0
            top10_percentage = (top10_count / total_results * 100) if total_results > 0 else 0

            # Estimar consultas usadas (basado en posiciones encontradas)
            queries_used = len(df) * 2  # Aproximación conservadora

            # Estimar costo
            cost_estimate = 0.0
            if queries_used > 100:
                paid_queries = queries_used - 100
                cost_estimate = (paid_queries / 1000) * 5.0

            # Actualizar cada bloque
            self.total_results_block.value_label.configure(text=str(total_results))
            self.total_results_block.subtitle_label.configure(text=f"{total_results} posiciones encontradas")

            self.avg_position_block.value_label.configure(text=f"{avg_position:.1f}")
            self.avg_position_block.subtitle_label.configure(text=f"Promedio de posiciones")

            self.best_position_block.value_label.configure(text=str(best_position))
            self.best_position_block.subtitle_label.configure(text=f"Mejor posición alcanzada")

            self.top10_percentage_block.value_label.configure(text=f"{top10_percentage:.1f}%")
            self.top10_percentage_block.subtitle_label.configure(text=f"En Top 10 resultados")

            self.unique_keywords_block.value_label.configure(text=str(unique_keywords))
            self.unique_keywords_block.subtitle_label.configure(text=f"Diferentes keywords")

            self.unique_domains_block.value_label.configure(text=str(unique_domains))
            self.unique_domains_block.subtitle_label.configure(text=f"Dominios únicos encontrados")

            self.queries_used_block.value_label.configure(text=str(queries_used))
            self.queries_used_block.subtitle_label.configure(text=f"Consultas API estimadas")

            self.cost_estimate_block.value_label.configure(text=f"${cost_estimate:.2f}")
            self.cost_estimate_block.subtitle_label.configure(text=f"Costo aproximado")

        except Exception as e:
            self.log_message(f"⚠️ Error actualizando bloques de estadísticas: {str(e)[:80]}")

    def show_current_stats_detailed(self):
        """Muestra estadísticas detalladas de los resultados actuales en ventana emergente"""
        if not self.current_results:
            messagebox.showwarning("Advertencia", "No hay resultados para mostrar estadísticas")
            return

        try:
            # Crear ventana detallada
            stats_window = ctk.CTkToplevel(self.root)
            stats_window.title("📊 Estadísticas Detalladas - Resultados Actuales")
            stats_window.geometry("700x600")
            stats_window.transient(self.root)

            # Título principal
            title_frame = ctk.CTkFrame(stats_window)
            title_frame.pack(fill="x", padx=20, pady=(20, 10))

            ctk.CTkLabel(title_frame, text="📈 ANÁLISIS DETALLADO DE RESULTADOS",
                        font=ctk.CTkFont(size=18, weight="bold")).pack()

            session_info = f"📅 Resultados actuales | {len(self.current_results)} posiciones encontradas"
            ctk.CTkLabel(title_frame, text=session_info,
                        font=ctk.CTkFont(size=12)).pack(pady=(5, 0))

            # Contenido scrollable
            content_frame = ctk.CTkScrollableFrame(stats_window)
            content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

            df = pd.DataFrame(self.current_results)

            # SECCIÓN 1: Métricas Generales
            general_frame = ctk.CTkFrame(content_frame, fg_color="gray15")
            general_frame.pack(fill="x", pady=(0, 15), padx=10)

            ctk.CTkLabel(general_frame, text="📊 MÉTRICAS GENERALES",
                        font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(15, 10))

            # Calcular métricas principales
            total_results = len(df)
            unique_keywords = df['keyword'].nunique() if 'keyword' in df.columns else 0
            unique_domains = df['domain'].nunique() if 'domain' in df.columns else 0
            avg_position = df['position'].mean() if 'position' in df.columns else 0

            # Crear grid de métricas
            metrics_frame = ctk.CTkFrame(general_frame)
            metrics_frame.pack(fill="x", padx=20, pady=(0, 15))

            # Fila 1
            row1 = ctk.CTkFrame(metrics_frame)
            row1.pack(fill="x", pady=(0, 10))

            self.create_metric_card(row1, "📈 Total Resultados", str(total_results),
                                   f"{total_results} posiciones encontradas", "blue")
            self.create_metric_card(row1, "🔑 Keywords Únicas", str(unique_keywords),
                                   f"{unique_keywords} términos diferentes", "green")

            # Fila 2
            row2 = ctk.CTkFrame(metrics_frame)
            row2.pack(fill="x", pady=(0, 10))

            self.create_metric_card(row2, "🌐 Dominios Únicos", str(unique_domains),
                                   f"{unique_domains} websites encontrados", "orange")
            self.create_metric_card(row2, "🎯 Posición Promedio", f"{avg_position:.1f}",
                                   f"Posición media general", "purple")

            # SECCIÓN 2: Distribución por Posiciones
            if 'position' in df.columns:
                positions_frame = ctk.CTkFrame(content_frame, fg_color="gray15")
                positions_frame.pack(fill="x", pady=(0, 15), padx=10)

                ctk.CTkLabel(positions_frame, text="🎯 DISTRIBUCIÓN POR POSICIONES",
                            font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(15, 10))

                # Calcular rangos
                top1 = len(df[df['position'] == 1])
                top3 = len(df[df['position'] <= 3])
                top5 = len(df[df['position'] <= 5])
                top10 = len(df[df['position'] <= 10])
                top20 = len(df[df['position'] <= 20])
                beyond20 = len(df[df['position'] > 20])

                ranges = [
                    ("🥇 Posición 1", top1),
                    ("🏆 Top 3", top3),
                    ("⭐ Top 5", top5),
                    ("📈 Top 10", top10),
                    ("📊 Top 20", top20),
                    ("🔍 Más allá de 20", beyond20)
                ]

                for range_name, count in ranges:
                    percentage = (count / total_results * 100) if total_results > 0 else 0
                    range_frame = ctk.CTkFrame(positions_frame)
                    range_frame.pack(fill="x", padx=20, pady=2)

                    ctk.CTkLabel(range_frame, text=f"{range_name}:",
                                font=ctk.CTkFont(size=12, weight="bold")).pack(side="left")
                    ctk.CTkLabel(range_frame,
                                text=f"{count} resultados ({percentage:.1f}%)").pack(side="right")

            # SECCIÓN 3: Top Dominios
            if 'domain' in df.columns and unique_domains > 0:
                domains_frame = ctk.CTkFrame(content_frame, fg_color="gray15")
                domains_frame.pack(fill="x", pady=(0, 15), padx=10)

                ctk.CTkLabel(domains_frame, text="🏆 TOP DOMINIOS",
                            font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(15, 10))

                top_domains = df['domain'].value_counts().head(10)

                for i, (domain, count) in enumerate(top_domains.items(), 1):
                    percentage = (count / total_results * 100) if total_results > 0 else 0
                    domain_frame = ctk.CTkFrame(domains_frame)
                    domain_frame.pack(fill="x", padx=20, pady=2)

                    rank_emoji = {1: "🥇", 2: "🥈", 3: "🥉"}.get(i, "🏅")
                    ctk.CTkLabel(domain_frame,
                                text=f"{rank_emoji} {domain}").pack(side="left")
                    ctk.CTkLabel(domain_frame,
                                text=f"{count} resultados ({percentage:.1f}%)").pack(side="right")

            # SECCIÓN 4: Recomendaciones
            recommendations_frame = ctk.CTkFrame(content_frame, fg_color="gray15")
            recommendations_frame.pack(fill="x", pady=(0, 15), padx=10)

            ctk.CTkLabel(recommendations_frame, text="🎯 RECOMENDACIONES",
                        font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(15, 10))

            recommendations = []

            if top10 / total_results > 0.5:
                recommendations.append("• ¡Excelente! Más del 50% de tus keywords están en Top 10")
            elif top10 / total_results > 0.3:
                recommendations.append("• Buen resultado: Más del 30% en Top 10")
            else:
                recommendations.append("• Considera optimizar: Menos del 30% en Top 10")

            if unique_domains < 5:
                recommendations.append("• Diversidad limitada: Solo unos pocos dominios dominan")
            elif unique_domains > 20:
                recommendations.append("• Buena diversificación: Muchos dominios diferentes")

            if avg_position < 10:
                recommendations.append("• Muy buen posicionamiento promedio")
            elif avg_position < 20:
                recommendations.append("• Posicionamiento decente, hay oportunidades")
            else:
                recommendations.append("• Posicionamiento requiere mejora significativa")

            for rec in recommendations:
                ctk.CTkLabel(recommendations_frame, text=rec,
                            justify="left").pack(anchor="w", padx=20, pady=2)

            # Botón de cerrar
            close_btn = ctk.CTkButton(stats_window, text="✅ Cerrar",
                                     command=stats_window.destroy)
            close_btn.pack(pady=(0, 20))

        except Exception as e:
            messagebox.showerror("Error", f"Error generando estadísticas detalladas:\n\n{str(e)}")

    def create_metric_card(self, parent, title, value, subtitle, color):
        """Crea una tarjeta de métrica para el análisis detallado"""
        card_frame = ctk.CTkFrame(parent, fg_color=color, height=80)

        # Título
        ctk.CTkLabel(card_frame, text=title,
                    font=ctk.CTkFont(size=12, weight="bold"),
                    text_color="white").pack(pady=(10, 5))

        # Valor grande
        ctk.CTkLabel(card_frame, text=str(value),
                    font=ctk.CTkFont(size=20, weight="bold"),
                    text_color="white").pack()

        # Subtítulo
        ctk.CTkLabel(card_frame, text=subtitle,
                    font=ctk.CTkFont(size=9),
                    text_color="lightgray").pack(pady=(5, 10))

        card_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        return card_frame

    def go_to_analysis(self):
        """Cambia a la pestaña de análisis y actualiza gráficos"""
        try:
            # Cambiar a la pestaña de análisis
            self.tabview.set("📈 Análisis")

            # Actualizar gráficos si hay datos
            if self.current_results:
                self.update_charts()
                self.log_message("📊 Cambiado a pestaña de análisis con gráficos actualizados")
            else:
                self.log_message("📊 Cambiado a pestaña de análisis (sin datos para graficar)")

        except Exception as e:
            self.log_message(f"⚠️ Error cambiando a análisis: {str(e)[:50]}")

    def advanced_keyword_cleaning(self):
        """Limpieza avanzada de keywords con múltiples opciones"""
        if not self.keywords_text.get("1.0", "end-1c").strip():
            messagebox.showwarning("Advertencia", "No hay keywords para limpiar")
            return

        def clean_keywords():
            text = self.keywords_text.get("1.0", "end-1c")
            keywords = [k.strip() for k in text.split('\n') if k.strip()]

            if not keywords:
                return

            original_count = len(keywords)

            # Limpiar duplicados (ignorando mayúsculas/minúsculas)
            seen = set()
            cleaned = []
            for kw in keywords:
                lower_kw = kw.lower()
                if lower_kw not in seen and lower_kw.strip():
                    cleaned.append(kw)
                    seen.add(lower_kw)

            # Eliminar palabras vacías comunes (stop words) en español e inglés
            stop_words = {
                'spanish': ['el', 'la', 'los', 'las', 'un', 'una', 'unos', 'unas', 'y', 'o', 'pero', 'que', 'como', 'si', 'porque', 'cuando', 'donde', 'quien', 'cual', 'cuales', 'este', 'esta', 'estos', 'estas', 'aquel', 'aquella', 'aquellos', 'aquellas', 'de', 'del', 'al', 'con', 'por', 'para', 'sin', 'sobre', 'tras', 'durante', 'mediante', 'desde', 'hasta', 'a', 'en', 'entre', 'hacia', 'contra', 'desde'],
                'english': ['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'shall', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them', 'this', 'that', 'these', 'those', 'what', 'which', 'who', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very']
            }

            all_stop_words = stop_words['spanish'] + stop_words['english']
            filtered = []
            removed_stop_words = 0

            for kw in cleaned:
                words = re.findall(r'\b\w+\b', kw.lower())
                if not all(word in all_stop_words for word in words):
                    filtered.append(kw)
                else:
                    removed_stop_words += 1

            # Filtrar keywords demasiado cortas (menos de 3 caracteres)
            final_keywords = [kw for kw in filtered if len(kw.strip()) >= 3]
            too_short_removed = len(filtered) - len(final_keywords)

            # Actualizar interfaz
            if final_keywords:
                self.keywords_text.delete("1.0", "end")
                self.keywords_text.insert("1.0", "\n".join(final_keywords))

                # Actualizar estadísticas
                self.update_keywords_stats()

                removed_total = original_count - len(final_keywords)
                messagebox.showinfo("Limpieza Completada",
                                  f"✅ Limpieza avanzada completada!\n\n"
                                  f"📊 Keywords originales: {original_count}\n"
                                  f"📋 Keywords finales: {len(final_keywords)}\n"
                                  f"🗑️ Eliminadas: {removed_total}\n"
                                  f"   • Duplicadas: {original_count - len(cleaned)}\n"
                                  f"   • Stop words: {removed_stop_words}\n"
                                  f"   • Muy cortas: {too_short_removed}\n")

                self.log_message(f"🧹 Limpieza avanzada: {original_count} → {len(final_keywords)} keywords")
            else:
                messagebox.showwarning("Sin Keywords", "La limpieza eliminó todas las keywords.\n\nConsidera revisar tus criterios de filtrado.")

        # Ejecutar limpieza
        clean_keywords()

    def analyze_keyword_competitiveness(self):
        """Análisis de competitividad y dificultad SEO de keywords"""
        if not self.keywords_text.get("1.0", "end-1c").strip():
            messagebox.showwarning("Advertencia", "No hay keywords para analizar")
            return

        # Validar credenciales de Google API
        if not self.api_key_var.get().strip() or not self.search_engine_id_var.get().strip():
            messagebox.showwarning("Error", "Configura tus credenciales de Google API primero\n\nVe a la pestaña '🔐 Google API'")
            return

        text = self.keywords_text.get("1.0", "end-1c")
        keywords = [k.strip() for k in text.split('\n') if k.strip()]

        if len(keywords) > 20:
            if not messagebox.askyesno("Demasiadas Keywords",
                                     f"Tienes {len(keywords)} keywords. El análisis de competitividad puede consumir muchos créditos de API (Google).\n\n"
                                     f"Se cobrarán aproximadamente ${((len(keywords) * 10) - 100) / 1000 * 5:.2f} por esta operación.\n\n"
                                     f"¿Quieres continuar de todas formas?"):
                return

        self.log_message("📈 Iniciando análisis de competitividad...")

        def analyze_competitiveness():
            try:
                results = []
                total_cost = 0

                # Proceso por lotes para evitar límites
                batch_size = 5
                for i in range(0, len(keywords), batch_size):
                    batch = keywords[i:i + batch_size]
                    self.log_message(f"📊 Analizando lote {i//batch_size + 1}: {len(batch)} keywords")

                    for keyword in batch:
                        try:
                            # Estimar competitividad basada en volumen de búsqueda aproximado
                            # (En una implementación real, usarías APIs como Keyword Planner o similares)
                            search_volume = self.estimate_search_volume(keyword)
                            competition_score = self.calculate_competition_score(keyword)

                            # Calcular dificultad SEO (0-100)
                            difficulty = min(100, (competition_score * 20) + (len(keyword.split()) * 10))

                            results.append({
                                'keyword': keyword,
                                'estimated_volume': search_volume,
                                'competition': competition_score,
                                'difficulty': difficulty,
                                'opportunity_score': max(0, 100 - difficulty)  # Mayor oportunidad = menor dificultad
                            })

                            # Estimar costo (aproximado)
                            total_cost += 0.01  # Costo estimado por consulta

                        except Exception as e:
                            self.log_message(f"⚠️ Error analizando '{keyword}': {e}")
                            results.append({
                                'keyword': keyword,
                                'estimated_volume': 0,
                                'competition': 5.0,
                                'difficulty': 50.0,
                                'opportunity_score': 50.0
                            })

                    # Pequeña pausa entre lotes
                    time.sleep(0.5)

                # Crear ventana de resultados
                analysis_window = ctk.CTkToplevel(self.root)
                analysis_window.title("📈 Análisis de Competitividad")
                analysis_window.geometry("900x700")
                analysis_window.transient(self.root)

                title_frame = ctk.CTkFrame(analysis_window)
                title_frame.pack(fill="x", padx=20, pady=(20, 10))

                ctk.CTkLabel(title_frame, text="🔍 ANÁLISIS DE COMPETITIVIDAD DE KEYWORDS",
                            font=ctk.CTkFont(size=18, weight="bold")).pack()

                info_frame = ctk.CTkFrame(analysis_window)
                info_frame.pack(fill="x", padx=20, pady=(0, 20))

                summary = f"📊 {len(results)} keywords analizadas | 💰 Costo estimado: ${total_cost:.2f}"
                ctk.CTkLabel(info_frame, text=summary, font=ctk.CTkFont(size=12)).pack(pady=10)

                # Tabla de resultados
                table_frame = ctk.CTkScrollableFrame(analysis_window)
                table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

                # Headers
                headers_frame = ctk.CTkFrame(table_frame)
                headers_frame.pack(fill="x", pady=(0, 5))

                ctk.CTkLabel(headers_frame, text="📝 KEYWORD", width=200, font=ctk.CTkFont(weight="bold")).pack(side="left", padx=5)
                ctk.CTkLabel(headers_frame, text="🔍 VOL.", width=80, font=ctk.CTkFont(weight="bold")).pack(side="left", padx=5)
                ctk.CTkLabel(headers_frame, text="⚔️ COMP.", width=80, font=ctk.CTkFont(weight="bold")).pack(side="left", padx=5)
                ctk.CTkLabel(headers_frame, text="🎯 DIF.", width=80, font=ctk.CTkFont(weight="bold")).pack(side="left", padx=5)
                ctk.CTkLabel(headers_frame, text="💎 OPP.", width=80, font=ctk.CTkFont(weight="bold")).pack(side="left", padx=5)

                # Filas de datos
                for result in results:
                    row_frame = ctk.CTkFrame(table_frame, fg_color=COLORS['surface'])
                    row_frame.pack(fill="x", pady=1)

                    # Colorear según oportunidad
                    opp_score = result['opportunity_score']
                    if opp_score >= 70:
                        color = COLORS['success']
                    elif opp_score >= 50:
                        color = COLORS['warning']
                    else:
                        color = COLORS['error']

                    row_frame.configure(fg_color=color)

                    # Datos
                    ctk.CTkLabel(row_frame, text=result['keyword'][:30], width=200, text_color="white").pack(side="left", padx=5)
                    ctk.CTkLabel(row_frame, text=f"{result['estimated_volume']:,}", width=80, text_color="white").pack(side="left", padx=5)
                    ctk.CTkLabel(row_frame, text=f"{result['competition']:.1f}", width=80, text_color="white").pack(side="left", padx=5)
                    ctk.CTkLabel(row_frame, text=f"{result['difficulty']:.0f}%", width=80, text_color="white").pack(side="left", padx=5)
                    ctk.CTkLabel(row_frame, text=f"{opp_score:.0f}%", width=80, text_color="white").pack(side="left", padx=5)

                # Botones de acción
                buttons_frame = ctk.CTkFrame(analysis_window)
                buttons_frame.pack(fill="x", padx=20, pady=(0, 20))

                ctk.CTkButton(buttons_frame, text="💾 Exportar Análisis",
                             command=lambda: self.export_competitiveness_analysis(results),
                             fg_color=COLORS['info']).pack(side="left", padx=(0, 10))

                ctk.CTkButton(buttons_frame, text="✅ Cerrar",
                             command=analysis_window.destroy).pack(side="right")

                self.log_message(f"✅ Análisis de competitividad completado: ${total_cost:.2f} estimado")

            except Exception as e:
                messagebox.showerror("Error", f"Error en análisis de competitividad:\n\n{str(e)}")

        # Ejecutar análisis
        threading.Thread(target=analyze_competitiveness, daemon=True).start()

    def generate_keyword_variants(self):
        """Genera variantes long-tail y relacionadas de las keywords actuales"""
        if not self.keywords_text.get("1.0", "end-1c").strip():
            messagebox.showwarning("Advertencia", "No hay keywords para generar variantes")
            return

        text = self.keywords_text.get("1.0", "end-1c")
        keywords = [k.strip() for k in text.split('\n') if k.strip()]

        if not keywords:
            return

        self.log_message("🔄 Generando variantes de keywords...")

        def generate_variants():
            variants = []
            original_count = len(keywords)

            # Variantes predefinidas para expandir
            prefixes = ["como", "qué es", "mejor", "precio de", "comprar", "donde", "cuanto cuesta", "tutorial", "guía", "tips"]
            suffixes = ["cercano", "cerca de mi", "en línea", "online", "barato", "económico", "profesional", "2025", "actual"]

            for keyword in keywords:
                variants.append(keyword)  # Mantener original

                # Generar variantes long-tail
                for prefix in prefixes[:3]:  # Limitar para no generar demasiado
                    variants.append(f"{prefix} {keyword}")

                for suffix in suffixes[:2]:  # Limitar para no generar demasiado
                    variants.append(f"{keyword} {suffix}")

                # Variantes con preguntas
                if len(keyword.split()) <= 2:
                    variants.append(f"{keyword} opiniones")
                    variants.append(f"{keyword} reseñas")

            # Eliminar duplicados y limpiar
            unique_variants = list(set(variants))
            final_variants = [v for v in unique_variants if len(v.strip()) >= 4]  # Mínimo 4 caracteres

            # Actualizar interfaz
            self.keywords_text.delete("1.0", "end")
            self.keywords_text.insert("1.0", "\n".join(final_variants))

            # Actualizar estadísticas
            self.update_keywords_stats()

            added = len(final_variants) - original_count
            messagebox.showinfo("Variantes Generadas",
                              f"✅ Variantes de keywords generadas!\n\n"
                              f"🎯 Keywords originales: {original_count}\n"
                              f"🚀 Keywords totales: {len(final_variants)}\n"
                              f"➕ Variantes añadidas: {added}\n")

            self.log_message(f"🔄 Variantes generadas: {original_count} → {len(final_variants)} keywords")

        # Ejecutar generación
        threading.Thread(target=generate_variants, daemon=True).start()

    def export_keywords_advanced(self):
        """Exportación avanzada de keywords con múltiples formatos"""
        if not self.keywords_text.get("1.0", "end-1c").strip():
            messagebox.showwarning("Advertencia", "No hay keywords para exportar")
            return

        text = self.keywords_text.get("1.0", "end-1c")
        keywords = [k.strip() for k in text.split('\n') if k.strip()]

        if not keywords:
            return

        # Ventana de opciones de exportación
        export_window = ctk.CTkToplevel(self.root)
        export_window.title("💾 Exportación Avanzada de Keywords")
        export_window.geometry("500x600")
        export_window.transient(self.root)
        export_window.grab_set()

        ctk.CTkLabel(export_window, text="📋 CONFIGURACIÓN DE EXPORTACIÓN",
                    font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(20, 10))

        # Opciones de formato
        format_frame = ctk.CTkFrame(export_window)
        format_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(format_frame, text="🎨 Formato:",
                    font=ctk.CTkFont(weight="bold")).pack(anchor="w", pady=(10, 5))

        format_options = ["TXT (Lineas)", "CSV (Con estadísticas)", "JSON (Estructurado)", "XML (SEO Friendly)"]
        format_var = ctk.StringVar(value=format_options[0])
        format_combo = ctk.CTkComboBox(format_frame, values=format_options, variable=format_var)
        format_combo.pack(fill="x", pady=(0, 10))

        # Opciones adicionales
        options_frame = ctk.CTkFrame(export_window)
        options_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(options_frame, text="⚙️ Opciones:",
                    font=ctk.CTkFont(weight="bold")).pack(anchor="w", pady=(10, 5))

        uppercase_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(options_frame, text="Convertir a mayúsculas", variable=uppercase_var).pack(anchor="w")

        lowercase_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(options_frame, text="Convertir a minúsculas", variable=lowercase_var).pack(anchor="w")

        sort_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(options_frame, text="Ordenar alfabéticamente", variable=sort_var).pack(anchor="w")

        add_metadata_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(options_frame, text="Incluir metadatos del proyecto", variable=add_metadata_var).pack(anchor="w")

        def perform_export():
            try:
                selected_format = format_var.get()

                # Procesar keywords según opciones
                processed_keywords = keywords.copy()

                if uppercase_var.get():
                    processed_keywords = [kw.upper() for kw in processed_keywords]
                elif lowercase_var.get():
                    processed_keywords = [kw.lower() for kw in processed_keywords]

                if sort_var.get():
                    processed_keywords.sort(key=str.lower)

                # Generar contenido según formato
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                metadata = f"# Keywords Exportadas - Keyword Position Scraper\n# Fecha: {time.strftime('%d/%m/%Y %H:%M:%S')}\n# Total: {len(processed_keywords)} keywords\n\n" if add_metadata_var.get() else ""

                if selected_format == "TXT (Lineas)":
                    content = metadata + "\n".join(processed_keywords)
                    extension = ".txt"
                    filename = f"keywords_export_{timestamp}"

                elif selected_format == "CSV (Con estadísticas)":
                    import csv
                    import io
                    content = metadata
                    content += "Keyword,Longitud,Dificultad Estimada\n"
                    for kw in processed_keywords:
                        length = len(kw)
                        difficulty = "Alta" if length < 3 else "Media" if length < 6 else "Baja"
                        content += f'"{kw}",{length},"{difficulty}"\n'
                    extension = ".csv"
                    filename = f"keywords_analisis_{timestamp}"

                elif selected_format == "JSON (Estructurado)":
                    data = {
                        "export_info": {
                            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                            "total_keywords": len(processed_keywords),
                            "format_version": "1.0"
                        },
                        "keywords": processed_keywords,
                        "stats": {
                            "avg_length": sum(len(kw) for kw in processed_keywords) / len(processed_keywords) if processed_keywords else 0,
                            "unique_keywords": len(set(kw.lower() for kw in processed_keywords))
                        }
                    }
                    import json
                    content = json.dumps(data, indent=2, ensure_ascii=False)
                    extension = ".json"
                    filename = f"keywords_estructurado_{timestamp}"

                elif selected_format == "XML (SEO Friendly)":
                    content = '<?xml version="1.0" encoding="UTF-8"?>\n'
                    content += '<keyword_export>\n'
                    content += f'  <metadata>\n'
                    content += f'    <export_date>{time.strftime("%Y-%m-%d %H:%M:%S")}</export_date>\n'
                    content += f'    <total_keywords>{len(processed_keywords)}</total_keywords>\n'
                    content += f'  </metadata>\n'
                    content += f'  <keywords>\n'
                    for i, kw in enumerate(processed_keywords, 1):
                        content += f'    <keyword id="{i}">\n'
                        content += f'      <text><![CDATA[{kw}]]></text>\n'
                        content += f'      <length>{len(kw)}</length>\n'
                        content += f'    </keyword>\n'
                    content += f'  </keywords>\n'
                    content += f'</keyword_export>'
                    extension = ".xml"
                    filename = f"keywords_seo_{timestamp}"

                # Guardar archivo
                file_path = filedialog.asksaveasfilename(
                    defaultextension=extension,
                    filetypes=[(f"Archivos {extension.upper()}", f"*{extension}"), ("Todos los archivos", "*.*")],
                    initialfile=filename
                )

                if file_path:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)

                    messagebox.showinfo("Éxito", f"Keywords exportadas exitosamente!\n\n📁 Archivo: {file_path}\n📊 Keywords: {len(processed_keywords)}\n🎨 Formato: {selected_format}")

                    export_window.destroy()
                    self.log_message(f"💾 Keywords exportadas: {file_path} ({selected_format})")

            except Exception as e:
                messagebox.showerror("Error", f"Error durante la exportación:\n\n{str(e)}")

        # Botones
        buttons_frame = ctk.CTkFrame(export_window)
        buttons_frame.pack(fill="x", padx=20, pady=20)

        ctk.CTkButton(buttons_frame, text="💾 EXPORTAR",
                     command=perform_export, fg_color=COLORS['success'],
                     height=40).pack(side="left", padx=(0, 10))

        ctk.CTkButton(buttons_frame, text="❌ CANCELAR",
                     command=export_window.destroy, height=40).pack(side="right")

    def estimate_search_volume(self, keyword):
        """Estima volumen de búsqueda basado en complejidad de keyword (simplificada)"""
        # Esta es una estimación muy básica. En la realidad usarías APIs especializadas
        words = len(keyword.split())
        if words == 1:
            base_volume = 1000
        elif words == 2:
            base_volume = 400
        elif words == 3:
            base_volume = 150
        else:
            base_volume = 50

        # Ajustar por longitud
        length_factor = max(0.5, min(2.0, len(keyword) / 20))
        return int(base_volume * length_factor)

    def calculate_competition_score(self, keyword):
        """Calcula puntaje de competencia basado en características de la keyword (simplificada)"""
        # Esta es una estimación muy básica
        score = 3.0  # Base media

        # Más competitiva si es keyword corta y común
        if len(keyword.split()) == 1:
            score += 2.0

        # Más competitiva si contiene palabras de dinero o business
        money_words = ['precio', 'comprar', 'venta', 'negocio', 'dinero', 'cost', 'buy', 'price', '$']
        if any(word in keyword.lower() for word in money_words):
            score += 1.5

        # Menos competitiva si es muy específica/long-tail
        if len(keyword) > 30:
            score -= 1.0

        return max(1.0, min(10.0, score))  # Limitar entre 1 y 10

    def export_competitiveness_analysis(self, results):
        """Exporta el análisis de competitividad"""
        try:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                initialfile=f"analisis_competitividad_{timestamp}"
            )

            if file_path:
                with open(file_path, 'w', encoding='utf-8', newline='') as f:
                    import csv
                    writer = csv.DictWriter(f, fieldnames=['keyword', 'estimated_volume', 'competition', 'difficulty', 'opportunity_score'])
                    writer.writeheader()
                    writer.writerows(results)

                messagebox.showinfo("Éxito", f"Análisis exportado a: {file_path}")
                self.log_message(f"📊 Análisis de competitividad exportado: {file_path}")

        except Exception as e:
            messagebox.showerror("Error", f"Error exportando análisis: {str(e)}")

    def update_keywords_stats(self):
        """Actualiza las estadísticas de keywords en tiempo real"""
        try:
            text = self.keywords_text.get("1.0", "end-1c")
            keywords = [k.strip() for k in text.split('\n') if k.strip()]

            total = len(keywords)
            unique = len(set(kw.lower() for kw in keywords))

            # Estimar dificultad promedio (muy simplificado)
            if keywords:
                avg_difficulty = sum(min(100, len(kw.split()) * 15 + (len(kw) // 5)) for kw in keywords) / len(keywords)
            else:
                avg_difficulty = 0

            # Actualizar bloques
            self.kw_total_label.configure(text=str(total))
            self.kw_analyzed_label.configure(text=str(total))  # Por ahora mismo que total
            self.kw_unique_label.configure(text=str(unique))
            self.kw_difficulty_label.configure(text=f"{avg_difficulty:.0f}%" if avg_difficulty > 0 else "N/A")

            # Actualizar estado
            if total > 0:
                self.keyword_status_label.configure(text=f"✅ Listo: {total} keywords - {unique} únicas - Dificultad promedio: {avg_difficulty:.0f}%")
            else:
                self.keyword_status_label.configure(text="📋 Listo para trabajar con keywords - Una keyword por línea")

        except Exception as e:
            self.keyword_status_label.configure(text="⚠️ Error actualizando estadísticas")

    def clear_current_results(self):
        """Limpia todos los resultados actuales"""
        try:
            # Confirmar acción
            if not messagebox.askyesno("Confirmar Limpieza",
                                     "¿Estás seguro de limpiar todos los resultados actuales?\n\nSe perderán los datos de la sesión actual."):
                return

            # Limpiar datos
            self.current_results = []
            self.keywords_list = []

            # Limpiar tabla
            for item in self.results_tree.get_children():
                self.results_tree.delete(item)

            # Limpiar bloques de estadísticas
            self.update_stats_blocks()

            # Actualizar información de sesión
            self.session_info_label.configure(text="Sesión actual: Sin resultados")

            # Actualizar estado
            self.results_status_label.configure(text="🧹 Resultados limpiados - Sesión reiniciada")

            self.log_message("🧹 Resultados actuales limpiados completamente")

            messagebox.showinfo("Limpieza Completa", "¡Resultados actuales limpiados!\n\nPuedes empezar una nueva sesión.")

        except Exception as e:
            messagebox.showerror("Error", f"Error limpiando resultados:\n\n{str(e)}")

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
