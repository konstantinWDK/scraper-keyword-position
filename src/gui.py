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
from datetime import datetime
import matplotlib
matplotlib.use('TkAgg')  # Configurar backend antes de importar pyplot
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
from report_methods import ReportMethods
from PIL import Image
import re
from collections import Counter

# Añadir directorio padre al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import Config, config
from stealth_scraper import StealthSerpScraper
from project_manager import ProjectManager
from gui_hybrid_extensions import HybridGUIExtensions
from search_console_api import SearchConsoleAPI

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

class KeywordScraperGUI(ReportMethods, HybridGUIExtensions):
    def run(self):
        """Inicia el loop principal de la interfaz gráfica"""
        self.root.mainloop()
        
    def create_new_project(self):
        """Crea un nuevo proyecto con los datos del formulario"""
        try:
            # Obtener datos del formulario
            project_name = self.project_name_entry.get().strip()
            project_domain = self.project_domain_entry.get().strip()
            project_sc_property = self.project_sc_property_entry.get().strip()
            
            # Validar datos
            if not project_name:
                messagebox.showerror("Error", "El nombre del proyecto es obligatorio")
                return
                
            if not project_domain:
                messagebox.showerror("Error", "El dominio principal es obligatorio")
                return
                
            # Crear proyecto usando el ProjectManager
            try:
                project_id = self.project_manager.create_project(
                    name=project_name,
                    domain=project_domain,
                    description="",
                    search_console_property=project_sc_property
                )
                
                # Limpiar formulario
                self.project_name_entry.delete(0, 'end')
                self.project_domain_entry.delete(0, 'end')
                self.project_sc_property_entry.delete(0, 'end')
                
                # Actualizar lista de proyectos
                self.refresh_projects_list()
                
                messagebox.showinfo("Éxito", f"Proyecto '{project_name}' creado correctamente")
                
                # Establecer como proyecto activo
                data = self.project_manager.load_projects()
                data["active_project"] = project_id
                self.project_manager.save_projects(data)
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo crear el proyecto: {str(e)}")
                
        except Exception as e:
            self.log_message(f"❌ Error creando proyecto: {str(e)}", "error")
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
            
    def edit_selected_project(self):
        """Edita el proyecto seleccionado"""
        try:
            selection = self.projects_tree.selection()
            if not selection:
                messagebox.showwarning("Advertencia", "Selecciona un proyecto para editar")
                return

            # Obtener datos del proyecto seleccionado
            item = self.projects_tree.item(selection[0])
            project_name = item['values'][0]
            
            # Buscar proyecto completo
            projects = self.project_manager.get_all_projects()
            project = None
            for project_id, p in projects.items():
                if p['name'] == project_name:
                    project = p
                    break

            if not project:
                messagebox.showerror("Error", "No se encontró el proyecto")
                return

            # Crear ventana de edición
            self.show_edit_project_dialog(project)

        except Exception as e:
            self.log_message(f"❌ Error editando proyecto: {str(e)}")
            messagebox.showerror("Error", f"Error editando proyecto:\n\n{str(e)}")
            
    def show_edit_project_dialog(self, project):
        """Muestra el diálogo de edición de proyecto"""
        edit_window = ctk.CTkToplevel(self.root)
        edit_window.title(f"Editar Proyecto: {project['name']}")
        edit_window.geometry("500x400")
        edit_window.transient(self.root)

        # Centrar ventana
        edit_window.update_idletasks()
        x = (edit_window.winfo_screenwidth() // 2) - (500 // 2)
        y = (edit_window.winfo_screenheight() // 2) - (400 // 2)
        edit_window.geometry(f"500x400+{x}+{y}")

        # Esperar a que la ventana sea visible antes de hacer grab_set (fix para Linux)
        edit_window.wait_visibility()
        edit_window.grab_set()

        main_frame = ctk.CTkFrame(edit_window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Título
        ctk.CTkLabel(main_frame, text=f"✏️ Editar Proyecto", 
                    font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(0, 20))

        # Campos de edición
        ctk.CTkLabel(main_frame, text="Nombre:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", pady=(0, 5))
        name_entry = ctk.CTkEntry(main_frame, width=400)
        name_entry.pack(pady=(0, 10))
        name_entry.insert(0, project['name'])

        ctk.CTkLabel(main_frame, text="Dominio:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", pady=(0, 5))
        domain_entry = ctk.CTkEntry(main_frame, width=400)
        domain_entry.pack(pady=(0, 10))
        domain_entry.insert(0, project['domain'])
        
    def delete_selected_project(self):
        """Elimina el proyecto seleccionado"""
        try:
            selection = self.projects_tree.selection()
            if not selection:
                messagebox.showwarning("Advertencia", "Selecciona un proyecto para eliminar")
                return

            # Obtener datos del proyecto
            item = self.projects_tree.item(selection[0])
            project_name = item['values'][0]

            # Confirmar eliminación
            if not messagebox.askyesno("Confirmar", 
                                     f"¿Estás seguro de que quieres eliminar el proyecto '{project_name}'?\n\n"
                                     "Esta acción no se puede deshacer."):
                return

            # Buscar y eliminar proyecto
            projects = self.project_manager.get_all_projects()
            for project in projects.values():
                if project['name'] == project_name:
                    if self.project_manager.delete_project(project['id']):
                        self.refresh_projects_list()
                        self.refresh_projects_dropdown()
                        self.log_message(f"✅ Proyecto '{project_name}' eliminado")
                        messagebox.showinfo("Éxito", f"Proyecto '{project_name}' eliminado correctamente")
                    else:
                        messagebox.showerror("Error", "No se pudo eliminar el proyecto")
                    break

        except Exception as e:
            self.log_message(f"❌ Error eliminando proyecto: {str(e)}")
            messagebox.showerror("Error", f"Error eliminando proyecto:\n\n{str(e)}")
            
    def export_project_data(self):
        """Exporta los datos del proyecto seleccionado"""
        try:
            selection = self.projects_tree.selection()
            if not selection:
                messagebox.showwarning("Advertencia", "Selecciona un proyecto para exportar")
                return

            # Obtener proyecto
            item = self.projects_tree.item(selection[0])
            project_name = item['values'][0]
            
            projects = self.project_manager.get_all_projects()
            project = None
            for project_id, p in projects.items():
                if p['name'] == project_name:
                    project = p
                    break

            if not project:
                messagebox.showerror("Error", "No se encontró el proyecto")
                return

            # Seleccionar archivo de destino
            from tkinter import filedialog
            filename = filedialog.asksaveasfilename(
                title="Exportar Proyecto",
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                initialfile=f"proyecto_{project['name'].replace(' ', '_')}.json"
            )

            if filename:
                import json
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(project, f, indent=2, ensure_ascii=False)
                
                self.log_message(f"✅ Proyecto '{project_name}' exportado a {filename}")
                messagebox.showinfo("Éxito", f"Proyecto exportado correctamente a:\n{filename}")

        except Exception as e:
            self.log_message(f"❌ Error exportando proyecto: {str(e)}")
            messagebox.showerror("Error", f"Error exportando proyecto:\n\n{str(e)}")
            
    def filter_reports_by_project(self, selected_project=None):
        """Filtra los informes por el proyecto seleccionado"""
        try:
            if not selected_project:
                selected_project = self.reports_project_filter.get()

            # Filtrar lista de informes
            self.refresh_reports_list(project_filter=selected_project)

        except Exception as e:
            self.log_message(f"❌ Error filtrando informes: {str(e)}")
            
    def sync_current_project_sc(self):
        """Sincroniza el proyecto actual con Search Console"""
        try:
            selected_project = self.reports_project_filter.get()
            
            if selected_project == "Todos los proyectos":
                messagebox.showinfo("Info", "Selecciona un proyecto específico para sincronizar con Search Console")
                return
            
            # Buscar el proyecto
            projects = self.project_manager.get_all_projects()
            project = None
            for project_id, p in projects.items():
                if p['name'] == selected_project:
                    project = p
                    break
            
            if not project:
                messagebox.showerror("Error", "No se encontró el proyecto seleccionado")
                return
            
            # Ejecutar sincronización en hilo separado
            import threading
            
            def sync_thread():
                try:
                    self.log_message(f"🔄 Iniciando sincronización con Search Console para '{selected_project}'...")
                    
                    # Obtener datos de Search Console
                    if project.get('search_console_property'):
                        sc_data = self.search_console_api.get_data(project['search_console_property'])
                        
                        if sc_data:
                            # Actualizar proyecto con datos de Search Console
                            project['search_console_data'] = sc_data
                            project['last_updated'] = datetime.now().isoformat()
                            
                            # Guardar cambios
                            self.project_manager.update_project(project['id'], project)

                            self.log_message(f"✅ Sincronización completada para '{selected_project}'")
                            self.root.after(0, lambda: messagebox.showinfo("Éxito", f"Datos de Search Console sincronizados para '{selected_project}'"))
                        else:
                            self.log_message(f"⚠️ No se pudieron obtener datos de Search Console para '{selected_project}'")
                            self.root.after(0, lambda: messagebox.showwarning("Advertencia", "No se pudieron obtener datos de Search Console"))
                    else:
                        self.log_message("⚠️ API de Search Console no configurada")
                        self.root.after(0, lambda: messagebox.showwarning("Advertencia", "API de Search Console no configurada"))
                        
                except Exception as e:
                    error_msg = f"Error sincronizando con Search Console: {str(e)}"
                    self.log_message(f"❌ {error_msg}")
                    self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
            
            # Iniciar hilo de sincronización
            sync_thread = threading.Thread(target=sync_thread, daemon=True)
            sync_thread.start()
            
        except Exception as e:
            self.log_message(f"❌ Error iniciando sincronización: {str(e)}")
            messagebox.showerror("Error", f"Error iniciando sincronización:\n\n{str(e)}")
            
    def update_reports_project_dropdown(self):
        """Actualiza el dropdown de proyectos en la pestaña de informes"""
        try:
            projects = self.project_manager.get_all_projects()
            project_names = ["Todos los proyectos"] + [p['name'] for p in projects.values()]
            
            self.reports_project_dropdown.configure(values=project_names)
            if not self.reports_project_filter.get():
                self.reports_project_filter.set("Todos los proyectos")
                
        except Exception as e:
            self.log_message(f"❌ Error actualizando dropdown de proyectos: {str(e)}")
        
    def sync_search_console(self):
        """Sincroniza datos con Google Search Console"""
        try:
            active_project = self.project_manager.get_active_project()
            if not active_project:
                messagebox.showwarning("Advertencia", "No hay proyecto activo seleccionado")
                return

            if not active_project.get('search_console_property'):
                messagebox.showwarning("Advertencia", 
                                     "El proyecto no tiene configurada una propiedad de Search Console")
                return

            # Mostrar diálogo de progreso
            progress_window = ctk.CTkToplevel(self.root)
            progress_window.title("Sincronizando con Search Console")
            progress_window.geometry("400x200")
            progress_window.transient(self.root)

            # Centrar ventana
            progress_window.update_idletasks()
            x = (progress_window.winfo_screenwidth() // 2) - (200)
            y = (progress_window.winfo_screenheight() // 2) - (100)
            progress_window.geometry(f"400x200+{x}+{y}")

            # Esperar a que la ventana sea visible antes de hacer grab_set (fix para Linux)
            progress_window.wait_visibility()
            progress_window.grab_set()

            progress_frame = ctk.CTkFrame(progress_window)
            progress_frame.pack(fill="both", expand=True, padx=20, pady=20)

            ctk.CTkLabel(progress_frame, text="🔄 Sincronizando datos...", 
                        font=ctk.CTkFont(size=16, weight="bold")).pack(pady=20)

            progress_label = ctk.CTkLabel(progress_frame, text="Conectando con Search Console...")
            progress_label.pack(pady=10)

            progress_bar = ctk.CTkProgressBar(progress_frame, width=300)
            progress_bar.pack(pady=10)
            progress_bar.set(0)

            def sync_data():
                try:
                    property_url = active_project['search_console_property']
                    
                    # Actualizar progreso
                    progress_label.configure(text="Obteniendo datos de rendimiento...")
                    progress_bar.set(0.3)
                    progress_window.update()

                    # Obtener datos de Search Console
                    from datetime import datetime, timedelta
                    end_date = datetime.now().date()
                    start_date = end_date - timedelta(days=30)

                    performance_data = self.search_console_api.get_search_analytics(
                        site_url=property_url,
                        start_date=start_date.isoformat(),
                        end_date=end_date.isoformat()
                    )

                    progress_label.configure(text="Procesando datos...")
                    progress_bar.set(0.6)
                    progress_window.update()

                    if performance_data:
                        # Obtener rows de la respuesta
                        rows = performance_data.get('rows', [])

                        # Guardar datos en el proyecto
                        sc_data = {
                            'last_sync': datetime.now().isoformat(),
                            'performance_data': rows[:100],  # Limitar a 100 registros
                            'total_clicks': sum(row.get('clicks', 0) for row in rows),
                            'total_impressions': sum(row.get('impressions', 0) for row in rows),
                            'avg_ctr': sum(row.get('ctr', 0) for row in rows) / len(rows) if rows else 0,
                            'avg_position': sum(row.get('position', 0) for row in rows) / len(rows) if rows else 0
                        }

                        # Actualizar proyecto
                        update_data = {'search_console_data': sc_data}
                        self.project_manager.update_project(active_project['id'], update_data)

                        progress_label.configure(text="¡Sincronización completada!")
                        progress_bar.set(1.0)
                        progress_window.update()

                        self.log_message(f"✅ Datos de Search Console sincronizados para {active_project['name']}")
                        
                        # Cerrar ventana después de 2 segundos
                        progress_window.after(2000, progress_window.destroy)
                        messagebox.showinfo("Éxito", 
                                          f"Datos sincronizados correctamente:\n\n"
                                          f"• Clicks: {sc_data['total_clicks']:,}\n"
                                          f"• Impresiones: {sc_data['total_impressions']:,}\n"
                                          f"• CTR promedio: {sc_data['avg_ctr']:.2%}\n"
                                          f"• Posición promedio: {sc_data['avg_position']:.1f}")
                    else:
                        progress_window.destroy()
                        messagebox.showwarning("Advertencia", "No se encontraron datos en Search Console")

                except Exception as e:
                    progress_window.destroy()
                    self.log_message(f"❌ Error sincronizando Search Console: {str(e)}")
                    messagebox.showerror("Error", f"Error sincronizando con Search Console:\n\n{str(e)}")

            # Ejecutar sincronización en hilo separado
            import threading
            sync_thread = threading.Thread(target=sync_data)
            sync_thread.daemon = True
            sync_thread.start()

        except Exception as e:
            self.log_message(f"❌ Error iniciando sincronización: {str(e)}")
            messagebox.showerror("Error", f"Error iniciando sincronización:\n\n{str(e)}")

    def check_search_console_auth(self):
        """Verifica el estado de autenticación de Search Console"""
        try:
            if self.search_console_api.is_authenticated():
                self.sc_auth_status.configure(text="🟢 Autenticado correctamente", text_color=COLORS['success'])
                self.sc_auth_button.configure(state="disabled")
                self.sc_disconnect_button.configure(state="normal")
                self.log_message("✅ Search Console: autenticado")
            else:
                self.sc_auth_status.configure(text="⚪ No autenticado", text_color=COLORS['text_secondary'])
                self.sc_auth_button.configure(state="normal")
                self.sc_disconnect_button.configure(state="disabled")
        except Exception as e:
            self.log_message(f"⚠️ Error verificando autenticación: {str(e)}")

    def authenticate_search_console(self):
        """Inicia el flujo de autenticación OAuth para Search Console"""
        try:
            # Crear ventana de diálogo
            auth_window = ctk.CTkToplevel(self.root)
            auth_window.title("Autenticación Google Search Console")
            auth_window.geometry("600x400")
            auth_window.transient(self.root)

            # Centrar ventana
            auth_window.update_idletasks()
            x = (auth_window.winfo_screenwidth() // 2) - 300
            y = (auth_window.winfo_screenheight() // 2) - 200
            auth_window.geometry(f"600x400+{x}+{y}")

            # Esperar a que la ventana sea visible antes de hacer grab_set (fix para Linux)
            auth_window.wait_visibility()
            auth_window.grab_set()

            main_frame = ctk.CTkFrame(auth_window)
            main_frame.pack(fill="both", expand=True, padx=20, pady=20)

            ctk.CTkLabel(main_frame, text="🔐 Autenticación OAuth 2.0",
                        font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(0, 10))

            # Instrucciones
            instructions = """Para autenticarte con Google Search Console necesitas:

1. Crear credenciales OAuth 2.0 en Google Cloud Console
2. Descargar el archivo JSON de credenciales
3. Seleccionarlo en el botón de abajo

Pasos detallados:
• Ve a https://console.cloud.google.com/
• APIs y servicios → Credenciales
• Crear credenciales → ID de cliente de OAuth 2.0
• Tipo de aplicación: Aplicación de escritorio
• Descarga el JSON de credenciales

No necesitas configurar URIs manualmente para apps de escritorio."""

            ctk.CTkLabel(main_frame, text=instructions, justify="left",
                        wraplength=550, font=ctk.CTkFont(size=11)).pack(pady=10)

            # Botón para seleccionar archivo
            def select_credentials():
                from tkinter import filedialog
                file_path = filedialog.askopenfilename(
                    title="Seleccionar archivo de credenciales OAuth",
                    filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
                )

                if file_path:
                    try:
                        import json
                        with open(file_path, 'r') as f:
                            client_config = json.load(f)

                        # Iniciar flujo OAuth
                        auth_url = self.search_console_api.setup_oauth_flow(client_config)

                        # Mostrar URL de autorización
                        url_label.configure(text=f"URL de autorización generada")
                        url_text.configure(state="normal")
                        url_text.delete("1.0", "end")
                        url_text.insert("1.0", auth_url)
                        url_text.configure(state="disabled")

                        # Abrir URL en navegador
                        import webbrowser
                        webbrowser.open(auth_url)

                        code_frame.pack(fill="x", pady=10)
                        self.log_message("🔐 Flujo OAuth iniciado - autoriza en el navegador")

                    except Exception as e:
                        messagebox.showerror("Error", f"Error al procesar credenciales:\n{str(e)}")

            ctk.CTkButton(main_frame, text="📁 Seleccionar Credenciales OAuth",
                         command=select_credentials, fg_color=COLORS['accent'],
                         width=250, height=40).pack(pady=10)

            # URL de autorización
            url_label = ctk.CTkLabel(main_frame, text="")
            url_label.pack(pady=(10, 5))

            url_text = ctk.CTkTextbox(main_frame, height=60, wrap="word")
            url_text.pack(fill="x", pady=5)
            url_text.configure(state="disabled")

            # Campo para código de autorización - Layout horizontal
            code_frame = ctk.CTkFrame(main_frame)
            code_frame.pack(fill="x", pady=10)

            instructions_label = ctk.CTkLabel(
                code_frame,
                text="📋 Copia el código completo de la URL (incluye el prefijo '4/')\n"
                     "Ejemplo: 4/0AVGzR1CtRfcRq9ThHAL7vF-QT8eh-izR5I9YTxb3y-QmprV2B7HStVjlBHclvralQZN0RA",
                font=ctk.CTkFont(size=11, weight="bold"),
                justify="left"
            )
            instructions_label.pack(anchor="w", pady=(5, 10), padx=10)

            # Frame horizontal para entrada y botón
            input_button_frame = ctk.CTkFrame(code_frame, fg_color="transparent")
            input_button_frame.pack(fill="x", pady=5, padx=10)

            code_entry = ctk.CTkEntry(
                input_button_frame,
                placeholder_text="Ej: 4/0AVGzR1CtRfcRq9..."
            )
            code_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

            def complete_auth():
                code = code_entry.get().strip()
                if not code:
                    messagebox.showwarning("Advertencia", "Por favor ingresa el código de autorización")
                    return

                self.log_message("🔄 Completando autenticación OAuth...")

                if self.search_console_api.complete_oauth_flow(code):
                    messagebox.showinfo("Éxito", "¡Autenticación completada correctamente!")
                    self.check_search_console_auth()
                    auth_window.destroy()
                    self.log_message("✅ Autenticación OAuth completada")
                else:
                    error_msg = ("No se pudo completar la autenticación.\n\n"
                                "Posibles causas:\n"
                                "• El código es incorrecto o expiró\n"
                                "• Las credenciales no son de tipo 'Aplicación de escritorio'\n"
                                "• El archivo JSON está corrupto\n\n"
                                "Revisa los logs para más detalles.")
                    messagebox.showerror("Error", error_msg)
                    self.log_message("❌ Error completando autenticación - revisa logs/scraper.log")

            ctk.CTkButton(
                input_button_frame,
                text="✅ Completar Autenticación",
                command=complete_auth,
                fg_color=COLORS['success'],
                width=200
            ).pack(side="left")

        except Exception as e:
            messagebox.showerror("Error", f"Error en autenticación:\n{str(e)}")
            self.log_message(f"❌ Error en autenticación OAuth: {str(e)}")

    def disconnect_search_console(self):
        """Desconecta y elimina las credenciales de Search Console"""
        try:
            import os
            if messagebox.askyesno("Confirmar", "¿Deseas desconectar Search Console?\n\nSe eliminarán las credenciales almacenadas."):
                # Eliminar archivos de tokens
                token_file = "data/search_console_token.json"
                flow_file = "data/oauth_flow.json"

                if os.path.exists(token_file):
                    os.remove(token_file)
                if os.path.exists(flow_file):
                    os.remove(flow_file)

                self.search_console_api.credentials = None
                self.search_console_api.service = None

                self.check_search_console_auth()
                messagebox.showinfo("Éxito", "Desconectado de Search Console")
                self.log_message("🔌 Search Console desconectado")
        except Exception as e:
            messagebox.showerror("Error", f"Error al desconectar:\n{str(e)}")

    def on_project_selected(self, selection):
        """Maneja la selección de un proyecto"""
        try:
            if not selection:
                return
            
            # Extraer nombre del proyecto de la selección
            project_name = selection.split(" (")[0]
            
            # Buscar y establecer proyecto activo
            projects = self.project_manager.get_all_projects()
            for project in projects.values():
                if project['name'] == project_name:
                    self.project_manager.set_active_project(project['id'])
                    self.update_project_info(project)
                    self.log_message(f"✅ Proyecto activo: {project['name']}")
                    break

        except Exception as e:
            self.log_message(f"❌ Error seleccionando proyecto: {str(e)}")
            
    def view_project_reports(self):
        """Muestra los informes del proyecto activo"""
        try:
            active_project = self.project_manager.get_active_project()
            if not active_project:
                messagebox.showwarning("Advertencia", "No hay proyecto activo seleccionado")
                return

            # Cambiar a la pestaña de informes
            self.notebook.set("Informes")
            self.log_message(f"📊 Mostrando informes del proyecto: {active_project['name']}")
            
        except Exception as e:
            self.log_message(f"❌ Error mostrando informes: {str(e)}")

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

        # Inicializar gestores
        self.project_manager = ProjectManager()
        self.search_console_api = SearchConsoleAPI()

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
        self.restart_button = None
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

        self.tab_projects = self.tabview.add("🏢 Proyectos")
        self.tab_config = self.tabview.add("⚙️ Configuración")
        self.tab_keywords = self.tabview.add("🔑 Keywords")
        self.tab_my_rankings = self.tabview.add("🏆 Mi Ranking")
        self.tab_scraping = self.tabview.add("🚀 Scraping")
        self.tab_results = self.tabview.add("📊 Resultados")
        self.tab_reports = self.tabview.add("📋 Informes")
        self.tab_analysis = self.tabview.add("📈 Análisis")
        self.tab_search_console = self.tabview.add("🔍 Search Console")

        # Configurar cada pestaña
        self.setup_projects_tab()
        self.setup_config_tab()
        self.setup_keywords_tab()
        self.setup_my_rankings_tab()
        self.setup_scraping_tab()
        self.setup_results_tab()
        self.setup_reports_tab()
        self.setup_analysis_tab()
        self.setup_search_console_tab()
        self.setup_hybrid_tab()  # Pestaña híbrida

    def log_message(self, message, level="info"):
        """Añade mensaje a los logs con formato mejorado"""
        try:
            if self.logs_text is None:
                # Si logs_text no está inicializado, solo imprimir en consola
                timestamp = time.strftime("%H:%M:%S")
                print(f"[{timestamp}] {message}")
                return
                
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
        except Exception as e:
            # Si hay algún error, al menos imprimir en consola
            print(f"Error en log_message: {e}")
            print(f"Mensaje original: {message}")

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

    def setup_projects_tab(self):
        """Configura la pestaña de gestión de proyectos"""
        main_frame = ctk.CTkScrollableFrame(self.tab_projects)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Título principal
        title_label = ctk.CTkLabel(main_frame, text="🏢 Gestión de Proyectos",
                                  font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack(pady=(0, 20))

        # Selector de proyecto activo
        project_selector_frame = ctk.CTkFrame(main_frame)
        project_selector_frame.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(project_selector_frame, text="📂 Proyecto Activo:", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=15, pady=(15, 5))

        # Dropdown para seleccionar proyecto
        self.active_project_var = ctk.StringVar()
        self.project_dropdown = ctk.CTkComboBox(
            project_selector_frame,
            variable=self.active_project_var,
            command=self.on_project_selected,
            width=400
        )
        self.project_dropdown.pack(anchor="w", padx=15, pady=(0, 15))

        # Información del proyecto activo
        self.project_info_frame = ctk.CTkFrame(project_selector_frame)
        self.project_info_frame.pack(fill="x", padx=15, pady=(0, 15))

        self.project_info_label = ctk.CTkLabel(
            self.project_info_frame,
            text="No hay proyecto seleccionado",
            font=ctk.CTkFont(size=12)
        )
        self.project_info_label.pack(pady=10)

        # Botones de acción rápida
        actions_frame = ctk.CTkFrame(project_selector_frame)
        actions_frame.pack(fill="x", padx=15, pady=(0, 15))

        ctk.CTkButton(actions_frame, text="🔄 Actualizar", 
                     command=self.refresh_projects_dropdown, width=120).pack(side="left", padx=(10, 5), pady=10)
        ctk.CTkButton(actions_frame, text="📊 Ver Informes", 
                     command=self.view_project_reports, width=120).pack(side="left", padx=5, pady=10)
        ctk.CTkButton(actions_frame, text="🔗 Search Console", 
                     command=self.sync_search_console, width=140).pack(side="left", padx=5, pady=10)

        # Sección de crear nuevo proyecto
        create_frame = ctk.CTkFrame(main_frame)
        create_frame.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(create_frame, text="➕ Crear Nuevo Proyecto", 
                    font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(15, 10))

        # Formulario de creación
        form_frame = ctk.CTkFrame(create_frame)
        form_frame.pack(fill="x", padx=15, pady=(0, 15))

        # Nombre del proyecto
        ctk.CTkLabel(form_frame, text="Nombre del Proyecto:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=(10, 5))
        self.project_name_entry = ctk.CTkEntry(form_frame, placeholder_text="Ej: Mi Sitio Web Principal")
        self.project_name_entry.pack(fill="x", padx=10, pady=(0, 10))

        # Dominio
        ctk.CTkLabel(form_frame, text="Dominio:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=(0, 5))
        self.project_domain_entry = ctk.CTkEntry(form_frame, placeholder_text="Ej: misitio.com")
        self.project_domain_entry.pack(fill="x", padx=10, pady=(0, 10))

        # Descripción
        ctk.CTkLabel(form_frame, text="Descripción (opcional):", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=(0, 5))
        self.project_description_entry = ctk.CTkEntry(form_frame, placeholder_text="Descripción del proyecto...")
        self.project_description_entry.pack(fill="x", padx=10, pady=(0, 10))

        # Propiedad de Search Console
        ctk.CTkLabel(form_frame, text="URL de Search Console (opcional):", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=(0, 5))
        self.project_sc_property_entry = ctk.CTkEntry(form_frame, placeholder_text="https://misitio.com/")
        self.project_sc_property_entry.pack(fill="x", padx=10, pady=(0, 15))

        # Botón crear
        ctk.CTkButton(form_frame, text="🚀 Crear Proyecto", 
                     command=self.create_new_project, 
                     fg_color=COLORS['accent'], width=200).pack(pady=(0, 15))

        # Lista de proyectos existentes
        projects_list_frame = ctk.CTkFrame(main_frame)
        projects_list_frame.pack(fill="both", expand=True)

        ctk.CTkLabel(projects_list_frame, text="📋 Proyectos Existentes", 
                    font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(15, 10))

        # Tabla de proyectos
        self.projects_tree_frame = ctk.CTkFrame(projects_list_frame)
        self.projects_tree_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        # Crear treeview para proyectos
        projects_columns = ("name", "domain", "keywords", "reports", "last_updated")
        self.projects_tree = ttk.Treeview(self.projects_tree_frame, columns=projects_columns, show="headings", height=8)

        # Configurar columnas
        self.projects_tree.heading("name", text="Nombre")
        self.projects_tree.heading("domain", text="Dominio")
        self.projects_tree.heading("keywords", text="Keywords")
        self.projects_tree.heading("reports", text="Informes")
        self.projects_tree.heading("last_updated", text="Última Actualización")

        self.projects_tree.column("name", width=200)
        self.projects_tree.column("domain", width=150)
        self.projects_tree.column("keywords", width=80, anchor="center")
        self.projects_tree.column("reports", width=80, anchor="center")
        self.projects_tree.column("last_updated", width=150)

        # Scrollbar para la tabla
        projects_scrollbar = ttk.Scrollbar(self.projects_tree_frame, orient="vertical", command=self.projects_tree.yview)
        self.projects_tree.configure(yscrollcommand=projects_scrollbar.set)

        self.projects_tree.pack(side="left", fill="both", expand=True)
        projects_scrollbar.pack(side="right", fill="y")

        # Botones de gestión
        management_frame = ctk.CTkFrame(projects_list_frame)
        management_frame.pack(fill="x", padx=15, pady=(0, 15))

        ctk.CTkButton(management_frame, text="✏️ Editar", 
                     command=self.edit_selected_project, width=100).pack(side="left", padx=(10, 5), pady=10)
        ctk.CTkButton(management_frame, text="🗑️ Eliminar", 
                     command=self.delete_selected_project, 
                     fg_color="#dc3545", width=100).pack(side="left", padx=5, pady=10)
        ctk.CTkButton(management_frame, text="📤 Exportar", 
                     command=self.export_project_data, width=100).pack(side="left", padx=5, pady=10)

        # Cargar proyectos existentes
        self.refresh_projects_list()
        self.refresh_projects_dropdown()

#######

    def setup_config_tab(self):
        """Configura la pestaña de configuración centralizada"""
        main_frame = ctk.CTkScrollableFrame(self.tab_config)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Título principal
        title_label = ctk.CTkLabel(main_frame, text="⚙️ Configuración Centralizada",
                                  font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack(pady=(0, 20))

        # === SECCIÓN GOOGLE CUSTOM SEARCH API ===
        api_frame = ctk.CTkFrame(main_frame)
        api_frame.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(api_frame, text="🔐 Google Custom Search API",
                    font=ctk.CTkFont(size=18, weight="bold")).pack(anchor="w", padx=15, pady=(15, 10))

        # Campos de configuración de API
        config_frame = ctk.CTkFrame(api_frame)
        config_frame.pack(fill="x", padx=15, pady=(0, 15))

        ctk.CTkLabel(config_frame, text="🔑 Google API Key:", font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        self.api_key_var = ctk.StringVar()
        api_key_entry = ctk.CTkEntry(config_frame, textvariable=self.api_key_var, show="*", width=400)
        api_key_entry.pack(fill="x", pady=(5, 10))

        ctk.CTkLabel(config_frame, text="🔍 Search Engine ID:", font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        self.search_engine_id_var = ctk.StringVar()
        se_id_entry = ctk.CTkEntry(config_frame, textvariable=self.search_engine_id_var, width=400)
        se_id_entry.pack(fill="x", pady=(5, 10))

        ctk.CTkButton(config_frame, text="💾 Guardar Configuración API",
                     command=self.save_google_config, fg_color=COLORS['success']).pack(pady=10)


        sc_frame = ctk.CTkFrame(main_frame)
        sc_frame.pack(fill="x", pady=(0, 20))
        ctk.CTkLabel(sc_frame, text="🔗 Google Search Console", font=ctk.CTkFont(size=18, weight="bold")).pack(anchor="w", padx=15, pady=(15, 5))

        # Estado de autenticación
        self.sc_auth_status = ctk.CTkLabel(sc_frame, text="⚪ No autenticado", font=ctk.CTkFont(size=14))
        self.sc_auth_status.pack(anchor="w", padx=15, pady=10)

        # Botones OAuth
        sc_buttons_frame = ctk.CTkFrame(sc_frame)
        sc_buttons_frame.pack(fill="x", padx=15, pady=(0, 15))

        self.sc_auth_button = ctk.CTkButton(sc_buttons_frame, text="🔐 Autenticar con Google",
                                            command=self.authenticate_search_console,
                                            fg_color=COLORS['info'], width=200)
        self.sc_auth_button.pack(side="left", padx=(0, 5))

        self.sc_disconnect_button = ctk.CTkButton(sc_buttons_frame, text="🔌 Desconectar",
                                                  command=self.disconnect_search_console,
                                                  fg_color=COLORS['error'], width=120, state="disabled")
        self.sc_disconnect_button.pack(side="left")

        # Verificar estado al inicio
        self.check_search_console_auth()

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
        main_frame = ctk.CTkScrollableFrame(self.tab_scraping)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # === SECCIÓN CONFIGURACIÓN DEL SCRAPER ===
        config_section = ctk.CTkFrame(main_frame)
        config_section.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(config_section, text="⚙️ Configuración del Scraper",
                    font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=15, pady=(15, 5))

        # Configuración del scraper - Layout más compacto
        scraper_frame = ctk.CTkFrame(config_section)
        scraper_frame.pack(fill="x", padx=15, pady=(0, 15))

        # Primera fila: Dominio y páginas
        row1 = ctk.CTkFrame(scraper_frame, fg_color="transparent")
        row1.pack(fill="x", pady=(0, 10))

        # Dominio objetivo
        domain_frame = ctk.CTkFrame(row1, fg_color="transparent")
        domain_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))
        ctk.CTkLabel(domain_frame, text="Dominio objetivo:").pack(anchor="w", pady=(0, 2))
        self.domain_entry = ctk.CTkEntry(domain_frame, placeholder_text="ejemplo.com", height=32)
        self.domain_entry.pack(fill="x")

        # Páginas a scrapear
        pages_frame = ctk.CTkFrame(row1, fg_color="transparent")
        pages_frame.pack(side="right", padx=(0, 0))
        ctk.CTkLabel(pages_frame, text="Páginas:").pack(anchor="w", pady=(0, 2))
        pages_controls = ctk.CTkFrame(pages_frame, fg_color="transparent")
        pages_controls.pack(fill="x")
        self.pages_var = ctk.DoubleVar(value=1.0)
        pages_slider = ctk.CTkSlider(pages_controls, from_=1, to=10, number_of_steps=9, variable=self.pages_var, command=self.update_pages_label, width=100, height=16)
        pages_slider.pack(side="left", padx=(0, 8))
        self.pages_label = ctk.CTkLabel(pages_controls, text="1 págs", font=ctk.CTkFont(size=10))
        self.pages_label.pack(side="right")

        # Segunda fila: País, idioma y delays
        row2 = ctk.CTkFrame(scraper_frame, fg_color="transparent")
        row2.pack(fill="x", pady=(0, 5))

        # País
        country_frame = ctk.CTkFrame(row2, fg_color="transparent")
        country_frame.pack(side="left", padx=(0, 10))
        ctk.CTkLabel(country_frame, text="País:").pack(anchor="w", pady=(0, 2))
        self.country_var = ctk.StringVar(value="US")
        country_combo = ctk.CTkComboBox(country_frame, values=["US", "ES", "FR", "DE", "IT", "UK", "BR", "MX"], variable=self.country_var, width=80, height=28)
        country_combo.pack()

        # Idioma
        lang_frame = ctk.CTkFrame(row2, fg_color="transparent")
        lang_frame.pack(side="left", padx=(0, 10))
        ctk.CTkLabel(lang_frame, text="Idioma:").pack(anchor="w", pady=(0, 2))
        self.language_var = ctk.StringVar(value="en")
        language_combo = ctk.CTkComboBox(lang_frame, values=["en", "es", "fr", "de", "it", "pt", "ru"], variable=self.language_var, width=80, height=28)
        language_combo.pack()

        # Delays
        delays_frame = ctk.CTkFrame(row2, fg_color="transparent")
        delays_frame.pack(side="left", padx=(0, 10))
        ctk.CTkLabel(delays_frame, text="Delays (seg):", font=ctk.CTkFont(size=10)).pack(anchor="w", pady=(0, 2))
        delays_inputs = ctk.CTkFrame(delays_frame, fg_color="transparent")
        delays_inputs.pack()
        min_delay_entry = ctk.CTkEntry(delays_inputs, placeholder_text="Min", width=45, height=28)
        min_delay_entry.pack(side="left", padx=(0, 3))
        self.min_delay_var = ctk.StringVar(value="5")
        min_delay_entry.configure(textvariable=self.min_delay_var)
        max_delay_entry = ctk.CTkEntry(delays_inputs, placeholder_text="Max", width=45, height=28)
        max_delay_entry.pack(side="left")
        self.max_delay_var = ctk.StringVar(value="15")
        max_delay_entry.configure(textvariable=self.max_delay_var)

        # Línea separadora
        ctk.CTkLabel(main_frame, text="-"*60).pack(pady=10)

        # Título principal con información de estado
        header_frame = ctk.CTkFrame(main_frame)
        header_frame.pack(fill="x", pady=(0, 5))

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
        self.stop_button.pack(side="left", padx=(5, 0))

        self.restart_button = ctk.CTkButton(buttons_frame, text="🔄 Reiniciar", command=self.restart_scraping, fg_color="#FF6B35", hover_color="#E55A2B", height=40, font=ctk.CTkFont(size=12, weight="bold"), state="disabled")
        self.restart_button.pack(side="left", padx=(5, 0))

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

        # Panel de archivos guardados
        files_section = ctk.CTkFrame(main_frame)
        files_section.pack(fill="x", padx=10, pady=(0, 10))

        files_header = ctk.CTkFrame(files_section)
        files_header.pack(fill="x", padx=10, pady=(10, 5))

        ctk.CTkLabel(files_header, text="📁 ARCHIVOS GUARDADOS", font=ctk.CTkFont(size=16, weight="bold")).pack(side="left")
        
        # Botón para actualizar lista de archivos
        ctk.CTkButton(files_header, text="🔄 Actualizar", 
                     command=self.refresh_saved_files_list, 
                     fg_color=COLORS['accent'], width=100).pack(side="right", padx=(10, 0))

        # Tabla de archivos guardados
        files_frame = ctk.CTkFrame(files_section)
        files_frame.pack(fill="x", padx=10, pady=5)

        # Crear treeview para mostrar archivos guardados
        files_columns = ("filename", "date", "size", "keywords", "results")
        self.files_tree = ttk.Treeview(files_frame, columns=files_columns, show="headings", height=6)

        # Configurar columnas de archivos
        self.files_tree.heading("filename", text="Archivo")
        self.files_tree.heading("date", text="Fecha")
        self.files_tree.heading("size", text="Tamaño")
        self.files_tree.heading("keywords", text="Keywords")
        self.files_tree.heading("results", text="Resultados")

        self.files_tree.column("filename", width=200)
        self.files_tree.column("date", width=120)
        self.files_tree.column("size", width=80, anchor="center")
        self.files_tree.column("keywords", width=80, anchor="center")
        self.files_tree.column("results", width=80, anchor="center")

        # Scrollbar para la tabla de archivos
        files_scrollbar = ttk.Scrollbar(files_frame, orient="vertical", command=self.files_tree.yview)
        self.files_tree.configure(yscrollcommand=files_scrollbar.set)

        # Evento de doble clic para cargar archivo
        self.files_tree.bind("<Double-1>", self.on_file_double_click)

        self.files_tree.pack(side="left", fill="x", expand=True)
        files_scrollbar.pack(side="right", fill="y")

        # Estado de archivos guardados
        self.results_status_label = ctk.CTkLabel(files_section, text="📁 Cargando archivos...", 
                                               font=ctk.CTkFont(size=12))
        self.results_status_label.pack(pady=(5, 10))

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
        """Configura la nueva pestaña de informes históricos con funcionalidad completa"""
        main_frame = ctk.CTkScrollableFrame(self.tab_reports)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Título principal
        title_frame = ctk.CTkFrame(main_frame)
        title_frame.pack(fill="x", padx=10, pady=(10, 20))
        
        ctk.CTkLabel(title_frame, text="📋 GESTIÓN DE INFORMES E HISTORIAL", 
                    font=ctk.CTkFont(size=24, weight="bold")).pack(pady=15)
        
        ctk.CTkLabel(title_frame, text="Accede, visualiza y administra todos tus informes de scraping generados", 
                    font=ctk.CTkFont(size=12), text_color=COLORS['text_secondary']).pack(pady=(0, 10))

        # Selector de proyecto para filtrar informes
        project_filter_frame = ctk.CTkFrame(main_frame)
        project_filter_frame.pack(fill="x", padx=10, pady=(0, 20))
        
        ctk.CTkLabel(project_filter_frame, text="🏢 Filtrar por Proyecto:", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=15, pady=(15, 5))
        
        # Dropdown para filtrar por proyecto
        self.reports_project_filter = ctk.StringVar()
        self.reports_project_dropdown = ctk.CTkComboBox(
            project_filter_frame,
            variable=self.reports_project_filter,
            command=self.filter_reports_by_project,
            width=400
        )
        self.reports_project_dropdown.pack(anchor="w", padx=15, pady=(0, 15))

        # Panel de estadísticas rápidas
        stats_frame = ctk.CTkFrame(main_frame)
        stats_frame.pack(fill="x", padx=10, pady=(0, 20))
        
        stats_title = ctk.CTkLabel(stats_frame, text="📊 Estadísticas del Proyecto", 
                                  font=ctk.CTkFont(size=16, weight="bold"))
        stats_title.pack(pady=(15, 10))
        
        # Grid de métricas
        metrics_grid = ctk.CTkFrame(stats_frame)
        metrics_grid.pack(fill="x", padx=15, pady=(0, 15))
        
        # Configurar grid
        metrics_grid.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Métricas individuales
        self.total_sessions_label = ctk.CTkLabel(metrics_grid, text="0\nSesiones Totales", 
                                               font=ctk.CTkFont(size=14, weight="bold"),
                                               fg_color=COLORS['accent'], corner_radius=8)
        self.total_sessions_label.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        self.total_keywords_label = ctk.CTkLabel(metrics_grid, text="0\nKeywords Analizadas", 
                                               font=ctk.CTkFont(size=14, weight="bold"),
                                               fg_color=COLORS['success'], corner_radius=8)
        self.total_keywords_label.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        self.avg_position_label = ctk.CTkLabel(metrics_grid, text="0.0\nPosición Promedio", 
                                             font=ctk.CTkFont(size=14, weight="bold"),
                                             fg_color=COLORS['info'], corner_radius=8)
        self.avg_position_label.grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        
        self.top_10_rate_label = ctk.CTkLabel(metrics_grid, text="0%\nRate Top 10", 
                                            font=ctk.CTkFont(size=14, weight="bold"),
                                            fg_color=COLORS['warning'], corner_radius=8)
        self.top_10_rate_label.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        # Métricas de Search Console (si están disponibles)
        sc_metrics_grid = ctk.CTkFrame(stats_frame)
        sc_metrics_grid.pack(fill="x", padx=15, pady=(10, 15))
        sc_metrics_grid.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        self.sc_clicks_label = ctk.CTkLabel(sc_metrics_grid, text="0\nClicks (SC)", 
                                          font=ctk.CTkFont(size=14, weight="bold"),
                                          fg_color="#4285f4", corner_radius=8)
        self.sc_clicks_label.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        self.sc_impressions_label = ctk.CTkLabel(sc_metrics_grid, text="0\nImpresiones (SC)", 
                                               font=ctk.CTkFont(size=14, weight="bold"),
                                               fg_color="#34a853", corner_radius=8)
        self.sc_impressions_label.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        self.sc_ctr_label = ctk.CTkLabel(sc_metrics_grid, text="0.0%\nCTR (SC)", 
                                       font=ctk.CTkFont(size=14, weight="bold"),
                                       fg_color="#fbbc04", corner_radius=8)
        self.sc_ctr_label.grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        
        self.sc_position_label = ctk.CTkLabel(sc_metrics_grid, text="0.0\nPosición (SC)", 
                                            font=ctk.CTkFont(size=14, weight="bold"),
                                            fg_color="#ea4335", corner_radius=8)
        self.sc_position_label.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        # Botones de acción principales
        actions_frame = ctk.CTkFrame(main_frame)
        actions_frame.pack(fill="x", padx=10, pady=(0, 20))
        
        actions_title = ctk.CTkLabel(actions_frame, text="🛠️ Acciones Rápidas", 
                                   font=ctk.CTkFont(size=16, weight="bold"))
        actions_title.pack(pady=(15, 10))
        
        buttons_frame = ctk.CTkFrame(actions_frame)
        buttons_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        ctk.CTkButton(buttons_frame, text="🔄 Actualizar Lista", 
                     command=self.refresh_reports_list, 
                     fg_color=COLORS['accent'], width=150).pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(buttons_frame, text="📊 Reporte Consolidado", 
                     command=self.generate_consolidated_report, 
                     fg_color=COLORS['success'], width=150).pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(buttons_frame, text="🔗 Sincronizar SC", 
                     command=self.sync_current_project_sc, 
                     fg_color="#4285f4", width=150).pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(buttons_frame, text="🗂️ Abrir Carpeta", 
                     command=self.open_reports_folder, 
                     fg_color=COLORS['info'], width=150).pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(buttons_frame, text="🧹 Limpiar Antiguos", 
                     command=self.cleanup_old_reports, 
                     fg_color=COLORS['warning'], width=150).pack(side="left")

        # Lista de reportes con información detallada
        reports_list_frame = ctk.CTkFrame(main_frame)
        reports_list_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        list_title = ctk.CTkLabel(reports_list_frame, text="📋 Informes Disponibles", 
                                font=ctk.CTkFont(size=16, weight="bold"))
        list_title.pack(pady=(15, 10))
        
        # Scrollable frame para la lista de reportes
        self.reports_scrollable = ctk.CTkScrollableFrame(reports_list_frame, height=400)
        self.reports_scrollable.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Inicializar el sistema de reportes
        self.init_report_system()
        
        # Cargar reportes existentes
        self.refresh_reports_list()
        
        # Cargar archivos guardados
        self.refresh_saved_files_list()
        
        # Actualizar dropdown de proyectos
        self.update_reports_project_dropdown()

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
            # Verificar que matplotlib y FigureCanvasTkAgg estén disponibles
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
            
            # Configurar matplotlib si está disponible
            self.fig, ((self.ax1, self.ax2), (self.ax3, self.ax4)) = plt.subplots(2, 2, figsize=(12, 8))
            self.fig.tight_layout(pad=3.0)
            self.canvas = FigureCanvasTkAgg(self.fig, self.chart_frame)
            self.canvas.get_tk_widget().pack(fill="both", expand=True)
            self.matplotlib_available = True
            
            # Mostrar mensaje de éxito
            ctk.CTkLabel(self.chart_frame, text="📊 Gráficos listos - Haz clic en 'Generar Análisis' para ver los resultados", 
                        font=ctk.CTkFont(size=14), text_color="green").pack(pady=20)
            
        except ImportError as e:
            # Si matplotlib no está instalado
            self.chart_frame.pack_forget()
            self.chart_frame = ctk.CTkFrame(main_frame)
            self.chart_frame.pack(fill="both", expand=True, padx=10, pady=5)
            
            # Detectar sistema operativo para mostrar instrucciones apropiadas
            import platform
            system = platform.system().lower()
            
            if system == "windows":
                install_msg = "pip install matplotlib"
            elif system == "darwin":  # macOS
                install_msg = "pip install matplotlib\no\nbrew install python-tk"
            else:  # Linux
                install_msg = "sudo apt install python3-tk\no\npip install matplotlib"
            
            ctk.CTkLabel(self.chart_frame, text=f"📋 Los gráficos aparecerán aquí después de generar el análisis\n\n⚠️ NOTA: Para activar gráficos instala:\n{install_msg}", justify="center").pack(expand=True)
            print(f"⚠️ Matplotlib no disponible: {e}")
            self.matplotlib_available = False
            
        except Exception as e:
            # Otros errores de configuración
            print(f"⚠️ Error configurando matplotlib: {e}")
            self.matplotlib_available = False
            ctk.CTkLabel(self.chart_frame, text="⚠️ Error configurando gráficos. Reinicia la aplicación.",
                        font=ctk.CTkFont(size=14), text_color="orange").pack(expand=True)

    def setup_search_console_tab(self):
        """Configura la pestaña de Search Console"""
        main_frame = ctk.CTkScrollableFrame(self.tab_search_console)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Título
        ctk.CTkLabel(main_frame, text="🔍 Google Search Console - Keywords y Métricas",
                    font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(0, 20))

        # Frame de selector de proyecto
        selector_frame = ctk.CTkFrame(main_frame)
        selector_frame.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(selector_frame, text="📂 Selecciona un proyecto:",
                    font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=15, pady=(15, 5))

        # Dropdown de proyectos
        self.sc_project_var = ctk.StringVar()
        self.sc_project_dropdown = ctk.CTkComboBox(
            selector_frame,
            variable=self.sc_project_var,
            command=self.on_sc_project_selected,
            width=400
        )
        self.sc_project_dropdown.pack(anchor="w", padx=15, pady=(0, 15))

        # Info del proyecto seleccionado
        self.sc_project_info = ctk.CTkLabel(selector_frame, text="", font=ctk.CTkFont(size=12))
        self.sc_project_info.pack(anchor="w", padx=15, pady=(0, 10))

        # Botón para ver sitios disponibles
        ctk.CTkButton(selector_frame, text="🌐 Ver Mis Sitios en Search Console",
                     command=self.show_available_sites,
                     fg_color=COLORS['info'], width=280, height=35).pack(anchor="w", padx=15, pady=(0, 15))

        # Frame de configuración
        config_frame = ctk.CTkFrame(main_frame)
        config_frame.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(config_frame, text="⚙️ Configuración de consulta:",
                    font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=15, pady=(15, 10))

        # Selector de rango de fechas
        date_frame = ctk.CTkFrame(config_frame)
        date_frame.pack(fill="x", padx=15, pady=(0, 10))

        ctk.CTkLabel(date_frame, text="📅 Últimos:").pack(side="left", padx=(10, 5))
        self.sc_days_var = ctk.StringVar(value="30")
        days_options = ["7", "30", "90", "180"]
        ctk.CTkComboBox(date_frame, values=days_options, variable=self.sc_days_var, width=100).pack(side="left", padx=5)
        ctk.CTkLabel(date_frame, text="días").pack(side="left", padx=(0, 10))

        # Límite de resultados
        limit_frame = ctk.CTkFrame(config_frame)
        limit_frame.pack(fill="x", padx=15, pady=(0, 15))

        ctk.CTkLabel(limit_frame, text="📊 Límite de resultados:").pack(side="left", padx=(10, 5))
        self.sc_limit_var = ctk.StringVar(value="100")
        limit_options = ["50", "100", "250", "500", "1000"]
        ctk.CTkComboBox(limit_frame, values=limit_options, variable=self.sc_limit_var, width=100).pack(side="left", padx=5)

        # Botones de acción
        actions_frame = ctk.CTkFrame(config_frame)
        actions_frame.pack(fill="x", padx=15, pady=(0, 15))

        ctk.CTkButton(actions_frame, text="🔄 Obtener Keywords",
                     command=self.load_sc_keywords,
                     fg_color=COLORS['accent'], width=180, height=40).pack(side="left", padx=(10, 5))

        ctk.CTkButton(actions_frame, text="💾 Exportar a CSV",
                     command=self.export_sc_data,
                     fg_color=COLORS['success'], width=150, height=40).pack(side="left", padx=5)

        ctk.CTkButton(actions_frame, text="🔄 Sincronizar y Guardar",
                     command=self.sync_and_save_sc_data,
                     fg_color=COLORS['info'], width=180, height=40).pack(side="left", padx=5)

        # Frame de resumen
        self.sc_summary_frame = ctk.CTkFrame(main_frame)
        self.sc_summary_frame.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(self.sc_summary_frame, text="📈 Resumen de Métricas",
                    font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=15, pady=(15, 10))

        # Labels para métricas
        metrics_container = ctk.CTkFrame(self.sc_summary_frame)
        metrics_container.pack(fill="x", padx=15, pady=(0, 15))

        self.sc_total_clicks_label = ctk.CTkLabel(metrics_container, text="Total Clicks: -",
                                                  font=ctk.CTkFont(size=14))
        self.sc_total_clicks_label.pack(side="left", padx=20, pady=10)

        self.sc_total_impressions_label = ctk.CTkLabel(metrics_container, text="Total Impresiones: -",
                                                       font=ctk.CTkFont(size=14))
        self.sc_total_impressions_label.pack(side="left", padx=20, pady=10)

        self.sc_avg_ctr_label = ctk.CTkLabel(metrics_container, text="CTR Promedio: -",
                                             font=ctk.CTkFont(size=14))
        self.sc_avg_ctr_label.pack(side="left", padx=20, pady=10)

        self.sc_avg_position_label = ctk.CTkLabel(metrics_container, text="Posición Promedio: -",
                                                  font=ctk.CTkFont(size=14))
        self.sc_avg_position_label.pack(side="left", padx=20, pady=10)

        # Frame de tabla
        table_frame = ctk.CTkFrame(main_frame)
        table_frame.pack(fill="both", expand=True, pady=(0, 20))

        ctk.CTkLabel(table_frame, text="🔑 Keywords de Search Console",
                    font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=15, pady=(15, 10))

        # Crear tabla
        columns = ("query", "clicks", "impressions", "ctr", "position")
        self.sc_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)

        self.sc_tree.heading("query", text="Keyword/Query")
        self.sc_tree.heading("clicks", text="Clicks")
        self.sc_tree.heading("impressions", text="Impresiones")
        self.sc_tree.heading("ctr", text="CTR (%)")
        self.sc_tree.heading("position", text="Posición Promedio")

        self.sc_tree.column("query", width=400)
        self.sc_tree.column("clicks", width=100, anchor="center")
        self.sc_tree.column("impressions", width=120, anchor="center")
        self.sc_tree.column("ctr", width=100, anchor="center")
        self.sc_tree.column("position", width=120, anchor="center")

        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.sc_tree.yview)
        self.sc_tree.configure(yscrollcommand=scrollbar.set)

        self.sc_tree.pack(side="left", fill="both", expand=True, padx=15, pady=(0, 15))
        scrollbar.pack(side="right", fill="y", pady=(0, 15))

        # Cargar proyectos en dropdown
        self.refresh_sc_projects_dropdown()

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

    def update_config_info(self):
        """Actualiza la configuración del scraper con los valores actuales de la interfaz"""
        try:
            # Actualizar configuración de Google API
            config.GOOGLE_API_KEY = self.api_key_var.get().strip()
            config.GOOGLE_SEARCH_ENGINE_ID = self.search_engine_id_var.get().strip()
            config.USE_GOOGLE_API = self.use_api_var.get()
            
            # Actualizar configuración de scraping
            if hasattr(self, 'pages_var'):
                config.PAGES_TO_SCRAPE = int(self.pages_var.get())
            if hasattr(self, 'country_var'):
                config.COUNTRY = self.country_var.get()
            if hasattr(self, 'language_var'):
                config.LANGUAGE = self.language_var.get()
            if hasattr(self, 'min_delay_var'):
                config.MIN_DELAY = float(self.min_delay_var.get())
            if hasattr(self, 'max_delay_var'):
                config.MAX_DELAY = float(self.max_delay_var.get())
            
            self.log_message("⚙️ Configuración actualizada correctamente")
            
        except Exception as e:
            self.log_message(f"⚠️ Error actualizando configuración: {e}", "warning")

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
        self.restart_button.configure(state="disabled")
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
        self.restart_button.configure(state="normal")
        
    def restart_scraping(self):
        """Reinicia el proceso de scraping"""
        if self.is_running:
            self.stop_scraping()
            # Esperar un momento para que se detenga completamente
            self.root.after(1000, self.start_scraping)
        else:
            self.start_scraping()
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
                int(self.pages_var.get()),
                stop_callback=lambda: not self.is_running
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
                
                # Auto-save results when scraping completes
                if hasattr(self.scraper, 'save_results'):
                    try:
                        session_id = self.scraper.save_results(results)
                        if session_id:
                            self.log_message(f"💾 Resultados guardados automáticamente - Sesión: {session_id}")
                            # Refresh reports list if the reports tab is active
                            if hasattr(self, 'refresh_reports_list'):
                                self.root.after(1000, self.refresh_reports_list)
                    except Exception as e:
                        self.log_message(f"⚠️ Error guardando resultados: {str(e)}")
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
            self.restart_button.configure(state="normal")
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
            messagebox.showwarning("Advertencia", "No hay resultados para analizar.\n\nPrimero debes realizar un scraping en la pestaña '🚀 Scraping' para obtener datos.")
            return

        try:
            import matplotlib.pyplot as plt
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

            # Debug: Mostrar información de los datos
            self.log_message(f"📊 Generando análisis con {len(self.current_results)} resultados")
            
            # Limpiar gráficos anteriores
            self.fig.clear()
            self.fig, ((self.ax1, self.ax2), (self.ax3, self.ax4)) = plt.subplots(2, 2, figsize=(12, 8))

            df = pd.DataFrame(self.current_results)
            
            # Debug: Mostrar columnas disponibles
            self.log_message(f"📋 Columnas disponibles: {list(df.columns)}")

            # Gráfico 1: Distribución de posiciones
            if 'position' in df.columns and not df['position'].empty:
                position_counts = df['position'].value_counts().sort_index()
                if not position_counts.empty:
                    self.ax1.bar(position_counts.index, position_counts.values, color='skyblue', alpha=0.7)
                    self.ax1.set_title('Distribución de Posiciones')
                    self.ax1.set_xlabel('Posición')
                    self.ax1.set_ylabel('Frecuencia')
                    self.ax1.grid(True, alpha=0.3)
                else:
                    self.ax1.text(0.5, 0.5, 'Sin datos de posiciones', ha='center', va='center', transform=self.ax1.transAxes)
                    self.ax1.set_title('Distribución de Posiciones - Sin datos')
            else:
                self.ax1.text(0.5, 0.5, 'Columna "position" no encontrada', ha='center', va='center', transform=self.ax1.transAxes)
                self.ax1.set_title('Distribución de Posiciones - Sin datos')

            # Gráfico 2: Top dominios
            if 'domain' in df.columns and not df['domain'].empty:
                top_domains = df['domain'].value_counts().head(10)
                if not top_domains.empty:
                    self.ax2.barh(range(len(top_domains)), top_domains.values, color='lightgreen', alpha=0.7)
                    self.ax2.set_yticks(range(len(top_domains)))
                    self.ax2.set_yticklabels(top_domains.index, fontsize=8)
                    self.ax2.set_title('Top 10 Dominios')
                    self.ax2.set_xlabel('Frecuencia')
                    self.ax2.grid(True, alpha=0.3)
                else:
                    self.ax2.text(0.5, 0.5, 'Sin datos de dominios', ha='center', va='center', transform=self.ax2.transAxes)
                    self.ax2.set_title('Top 10 Dominios - Sin datos')
            else:
                self.ax2.text(0.5, 0.5, 'Columna "domain" no encontrada', ha='center', va='center', transform=self.ax2.transAxes)
                self.ax2.set_title('Top 10 Dominios - Sin datos')

            # Gráfico 3: Distribución por páginas
            if 'page' in df.columns and not df['page'].empty:
                page_stats = df['page'].value_counts().sort_index()
                if not page_stats.empty:
                    self.ax3.bar(page_stats.index, page_stats.values, color='orange', alpha=0.7)
                    self.ax3.set_title('Resultados por Página')
                    self.ax3.set_xlabel('Página')
                    self.ax3.set_ylabel('Resultados')
                    self.ax3.grid(True, alpha=0.3)
                else:
                    self.ax3.text(0.5, 0.5, 'Sin datos de páginas', ha='center', va='center', transform=self.ax3.transAxes)
                    self.ax3.set_title('Resultados por Página - Sin datos')
            else:
                self.ax3.text(0.5, 0.5, 'Columna "page" no encontrada', ha='center', va='center', transform=self.ax3.transAxes)
                self.ax3.set_title('Resultados por Página - Sin datos')

            # Gráfico 4: Boxplot de posiciones
            if 'position' in df.columns and not df['position'].empty:
                positions = df['position'].dropna()
                if len(positions) > 0:
                    self.ax4.boxplot(positions, vert=False)
                    self.ax4.set_title('Boxplot de Posiciones')
                    self.ax4.set_xlabel('Posición')
                    self.ax4.grid(True, alpha=0.3)
                else:
                    self.ax4.text(0.5, 0.5, 'Sin datos válidos de posiciones', ha='center', va='center', transform=self.ax4.transAxes)
                    self.ax4.set_title('Boxplot de Posiciones - Sin datos')
            else:
                self.ax4.text(0.5, 0.5, 'Columna "position" no encontrada', ha='center', va='center', transform=self.ax4.transAxes)
                self.ax4.set_title('Boxplot de Posiciones - Sin datos')

            # Actualizar canvas
            self.fig.tight_layout(pad=3.0)
            self.canvas.draw()

            self.log_message("📊 Análisis generado correctamente")

        except Exception as e:
            self.log_message(f"❌ Error generando análisis: {str(e)}")
            messagebox.showerror("Error", f"Error generando análisis:\n\n{str(e)}")

    def refresh_saved_files_list(self):
        """Actualiza la lista de archivos guardados en la pestaña de resultados"""
        try:
            # Limpiar tabla actual
            for item in self.files_tree.get_children():
                self.files_tree.delete(item)

            # Buscar archivos CSV y JSON en el directorio data
            data_dir = Path("data")
            if not data_dir.exists():
                return

            files_info = []
            
            # Buscar archivos CSV
            for csv_file in data_dir.glob("*.csv"):
                try:
                    # Obtener información del archivo
                    stat = csv_file.stat()
                    size_mb = stat.st_size / (1024 * 1024)
                    date_modified = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M")
                    
                    # Leer archivo para obtener estadísticas
                    import pandas as pd
                    df = pd.read_csv(csv_file)
                    keywords_count = len(df['keyword'].unique()) if 'keyword' in df.columns else 0
                    results_count = len(df)
                    
                    files_info.append({
                        'filename': csv_file.name,
                        'date': date_modified,
                        'size': f"{size_mb:.1f} MB",
                        'keywords': keywords_count,
                        'results': results_count,
                        'path': str(csv_file)
                    })
                except Exception as e:
                    self.log_message(f"⚠️ Error leyendo {csv_file.name}: {e}")

            # Ordenar por fecha (más reciente primero)
            files_info.sort(key=lambda x: x['date'], reverse=True)

            # Añadir archivos a la tabla
            for file_info in files_info:
                self.files_tree.insert("", "end", values=(
                    file_info['filename'],
                    file_info['date'],
                    file_info['size'],
                    file_info['keywords'],
                    file_info['results']
                ))

            # Actualizar estado
            if files_info:
                total_files = len(files_info)
                total_keywords = sum(f['keywords'] for f in files_info)
                total_results = sum(f['results'] for f in files_info)
                self.results_status_label.configure(
                    text=f"📁 {total_files} archivos encontrados | {total_keywords} keywords | {total_results} resultados totales"
                )
            else:
                self.results_status_label.configure(text="📁 No se encontraron archivos guardados")

        except Exception as e:
            self.log_message(f"❌ Error actualizando lista de archivos: {e}")
            self.results_status_label.configure(text="❌ Error cargando archivos")

    def on_file_double_click(self, event):
        """Maneja el doble clic en la tabla de archivos guardados para cargar su contenido"""
        try:
            # Obtener el elemento seleccionado
            selection = self.files_tree.selection()
            if not selection:
                return

            # Obtener los valores del elemento seleccionado
            item = self.files_tree.item(selection[0])
            filename = item['values'][0]  # Primera columna es el nombre del archivo
            
            # Construir la ruta completa del archivo
            file_path = Path("data") / filename
            
            if not file_path.exists():
                messagebox.showerror("Error", f"El archivo {filename} no existe")
                return

            # Cargar y mostrar el contenido del archivo
            self.load_file_content_to_table(file_path)
            
            # Actualizar mensaje de estado
            self.log_message(f"📂 Archivo cargado: {filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error cargando el archivo:\n\n{str(e)}")
            self.log_message(f"❌ Error cargando archivo: {e}")

    def load_file_content_to_table(self, file_path):
        """Carga el contenido de un archivo CSV en la tabla detallada de resultados"""
        try:
            # Leer el archivo CSV
            df = pd.read_csv(file_path)
            
            # Limpiar la tabla actual
            for item in self.results_tree.get_children():
                self.results_tree.delete(item)
            
            # Verificar que el archivo tenga las columnas esperadas
            expected_columns = ['keyword', 'position', 'title', 'domain', 'page']
            available_columns = [col for col in expected_columns if col in df.columns]
            
            if not available_columns:
                messagebox.showwarning("Advertencia", 
                    f"El archivo no contiene las columnas esperadas: {', '.join(expected_columns)}")
                return
            
            # Cargar datos en la tabla
            for _, row in df.iterrows():
                values = []
                for col in expected_columns:
                    if col in df.columns:
                        values.append(str(row[col]) if pd.notna(row[col]) else "")
                    else:
                        values.append("")
                
                self.results_tree.insert("", "end", values=values)
            
            # Actualizar estadísticas
            total_results = len(df)
            unique_keywords = len(df['keyword'].unique()) if 'keyword' in df.columns else 0
            
            # Actualizar el estado en la interfaz
            status_text = f"📊 {total_results} resultados cargados | {unique_keywords} keywords únicas"
            
            # Buscar y actualizar la etiqueta de estado de la tabla (si existe)
            if hasattr(self, 'table_status_label'):
                self.table_status_label.configure(text=status_text)
            
            self.log_message(f"✅ Contenido cargado: {total_results} resultados de {file_path.name}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error procesando el archivo:\n\n{str(e)}")
            self.log_message(f"❌ Error procesando archivo: {e}")

    # ========== MÉTODOS DE GESTIÓN DE PROYECTOS ==========

    def refresh_projects_list(self):
        """Actualiza la lista de proyectos en la tabla"""
        try:
            # Limpiar tabla actual
            for item in self.projects_tree.get_children():
                self.projects_tree.delete(item)

            # Obtener proyectos (es un dict con project_id: project_data)
            projects_dict = self.project_manager.get_all_projects()

            for project_id, project in projects_dict.items():
                # Contar keywords y reportes
                keywords_count = len(project.get('keywords', []))
                reports_count = len(project.get('reports', []))
                
                # Formatear fecha
                last_updated = project.get('last_updated', 'N/A')
                if last_updated != 'N/A':
                    try:
                        from datetime import datetime
                        dt = datetime.fromisoformat(last_updated.replace('Z', '+00:00'))
                        last_updated = dt.strftime("%Y-%m-%d %H:%M")
                    except:
                        pass
                
                # Insertar en la tabla
                self.projects_tree.insert("", "end", values=(
                    project['name'],
                    project['domain'],
                    keywords_count,
                    reports_count,
                    last_updated
                ))

            self.log_message(f"📋 Lista de proyectos actualizada: {len(projects_dict)} proyectos")
            
        except Exception as e:
            self.log_message(f"❌ Error actualizando lista de proyectos: {str(e)}")

    def refresh_projects_dropdown(self):
        """Actualiza el dropdown de selección de proyectos"""
        try:
            projects_dict = self.project_manager.get_all_projects()
            project_names = [f"{p['name']} ({p['domain']})" for p in projects_dict.values()]

            self.project_dropdown.configure(values=project_names)

            # Establecer proyecto activo si existe
            active_project = self.project_manager.get_active_project()
            if active_project:
                active_name = f"{active_project['name']} ({active_project['domain']})"
                if active_name in project_names:
                    self.active_project_var.set(active_name)
                    self.update_project_info(active_project)

        except Exception as e:
            self.log_message(f"❌ Error actualizando dropdown de proyectos: {str(e)}")

    def update_project_info(self, project):
        """Actualiza la información del proyecto activo mostrada"""
        try:
            if not project:
                info_text = "No hay proyecto seleccionado"
            else:
                keywords_count = len(project.get('keywords', []))
                reports_count = len(project.get('reports', []))

                info_text = f"""📋 Proyecto Activo: {project['name']}
🌐 Dominio: {project['domain']}
📝 Descripción: {project.get('description', 'Sin descripción')}
🔑 Keywords: {keywords_count}
📊 Reportes: {reports_count}
🔗 Search Console: {project.get('search_console_property', 'No configurado')}"""
            
            self.project_info_label.configure(text=info_text)

        except Exception as e:
            self.log_message(f"❌ Error actualizando info del proyecto: {str(e)}")
            self.project_info_label.configure(text="Error cargando información del proyecto")

    # ========== MÉTODOS DE SEARCH CONSOLE ==========

    def refresh_sc_projects_dropdown(self):
        """Actualiza el dropdown de proyectos en la pestaña de Search Console"""
        try:
            projects_dict = self.project_manager.get_all_projects()
            project_names = [f"{p['name']} ({p['domain']})" for p in projects_dict.values()]

            self.sc_project_dropdown.configure(values=project_names)

            # Si hay un proyecto activo, seleccionarlo
            active_project = self.project_manager.get_active_project()
            if active_project:
                active_name = f"{active_project['name']} ({active_project['domain']})"
                if active_name in project_names:
                    self.sc_project_var.set(active_name)
                    self.on_sc_project_selected(active_name)

        except Exception as e:
            self.log_message(f"❌ Error actualizando dropdown de SC: {str(e)}")

    def on_sc_project_selected(self, selection):
        """Maneja la selección de un proyecto en Search Console"""
        try:
            if not selection:
                return

            # Extraer nombre del proyecto
            project_name = selection.split(" (")[0]

            # Buscar proyecto
            projects_dict = self.project_manager.get_all_projects()
            selected_project = None

            for pid, project in projects_dict.items():
                if project['name'] == project_name:
                    selected_project = project
                    break

            if selected_project:
                sc_property = selected_project.get('search_console_property', 'No configurado')
                self.sc_project_info.configure(
                    text=f"🔗 URL de Search Console: {sc_property}"
                )
                self.current_sc_project = selected_project
            else:
                self.sc_project_info.configure(text="❌ Proyecto no encontrado")
                self.current_sc_project = None

        except Exception as e:
            self.log_message(f"❌ Error seleccionando proyecto SC: {str(e)}")

    def show_available_sites(self):
        """Muestra los sitios disponibles en Search Console"""
        try:
            # Verificar autenticación
            if not self.search_console_api.is_authenticated():
                messagebox.showwarning("Advertencia",
                                     "Debes autenticarte con Search Console primero.\n\n"
                                     "Ve a '⚙️ Configuración' → 'Google Search Console'")
                return

            self.log_message("🔄 Obteniendo lista de sitios de Search Console...")

            # Obtener sitios
            sites = self.search_console_api.get_sites()

            if not sites:
                messagebox.showinfo("Sin Sitios",
                                  "No se encontraron sitios en tu cuenta de Search Console.\n\n"
                                  "Posibles causas:\n"
                                  "• No tienes sitios verificados\n"
                                  "• La cuenta usada no tiene acceso a sitios\n\n"
                                  "Ve a https://search.google.com/search-console y verifica un sitio.")
                self.log_message("⚠️ No se encontraron sitios en Search Console")
                return

            # Crear ventana para mostrar sitios
            sites_window = ctk.CTkToplevel(self.root)
            sites_window.title("Mis Sitios en Search Console")
            sites_window.geometry("700x500")
            sites_window.transient(self.root)

            # Centrar ventana
            sites_window.update_idletasks()
            x = (sites_window.winfo_screenwidth() // 2) - 350
            y = (sites_window.winfo_screenheight() // 2) - 250
            sites_window.geometry(f"700x500+{x}+{y}")

            # Esperar a que la ventana sea visible antes de hacer grab_set (fix para Linux)
            sites_window.wait_visibility()
            sites_window.grab_set()

            main_frame = ctk.CTkFrame(sites_window)
            main_frame.pack(fill="both", expand=True, padx=20, pady=20)

            ctk.CTkLabel(main_frame, text="🌐 Sitios Disponibles en Search Console",
                        font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(0, 10))

            # Mostrar proyecto seleccionado si existe
            selected_project_text = ""
            if hasattr(self, 'current_sc_project') and self.current_sc_project:
                selected_project_text = f"\n\n📂 Proyecto seleccionado: {self.current_sc_project['name']}"

            ctk.CTkLabel(main_frame,
                        text=f"Estos son los {len(sites)} sitios a los que tienes acceso.\n"
                             "Haz clic en '✅ Usar este sitio' para asignarlo al proyecto seleccionado.\n"
                             "O copia la URL manualmente con '📋 Copiar URL'."
                             f"{selected_project_text}",
                        font=ctk.CTkFont(size=12),
                        wraplength=650).pack(pady=(0, 20))

            # Frame scrollable para sitios
            sites_scroll = ctk.CTkScrollableFrame(main_frame, height=300)
            sites_scroll.pack(fill="both", expand=True, pady=(0, 10))

            # Mostrar cada sitio
            for i, site in enumerate(sites, 1):
                site_url = site.get('siteUrl', 'N/A')
                permission_level = site.get('permissionLevel', 'N/A')

                site_frame = ctk.CTkFrame(sites_scroll)
                site_frame.pack(fill="x", pady=5, padx=5)

                # Número y URL
                url_label = ctk.CTkLabel(site_frame,
                                        text=f"{i}. {site_url}",
                                        font=ctk.CTkFont(size=13, weight="bold"),
                                        anchor="w")
                url_label.pack(anchor="w", padx=10, pady=(10, 2))

                # Nivel de permiso
                permission_label = ctk.CTkLabel(site_frame,
                                               text=f"   Permiso: {permission_level}",
                                               font=ctk.CTkFont(size=11),
                                               text_color="gray",
                                               anchor="w")
                permission_label.pack(anchor="w", padx=10, pady=(0, 5))

                # Frame para botones
                buttons_frame = ctk.CTkFrame(site_frame)
                buttons_frame.pack(anchor="e", padx=10, pady=(0, 10))

                # Botón para usar este sitio (asignar al proyecto)
                def use_site(url=site_url):
                    try:
                        # Verificar que hay un proyecto seleccionado
                        if not hasattr(self, 'current_sc_project') or not self.current_sc_project:
                            messagebox.showwarning("Advertencia",
                                                 "Primero selecciona un proyecto en el dropdown de arriba.")
                            return

                        # Actualizar proyecto con la URL
                        project_id = self.current_sc_project['id']
                        updates = {'search_console_property': url}
                        self.project_manager.update_project(project_id, updates)

                        # Actualizar UI
                        self.sc_project_info.configure(text=f"🔗 URL de Search Console: {url}")
                        self.current_sc_project['search_console_property'] = url

                        # Cerrar ventana
                        sites_window.destroy()

                        # Mostrar confirmación
                        messagebox.showinfo("✅ Sitio Asignado",
                                          f"URL asignada correctamente al proyecto:\n\n"
                                          f"Proyecto: {self.current_sc_project['name']}\n"
                                          f"URL: {url}\n\n"
                                          f"Ya puedes obtener las keywords!")

                        self.log_message(f"✅ URL de SC asignada a proyecto '{self.current_sc_project['name']}': {url}")

                    except Exception as e:
                        messagebox.showerror("Error", f"Error asignando sitio:\n\n{str(e)}")
                        self.log_message(f"❌ Error asignando sitio: {str(e)}")

                # Botón para copiar URL
                def copy_url(url=site_url):
                    sites_window.clipboard_clear()
                    sites_window.clipboard_append(url)
                    messagebox.showinfo("Copiado", f"URL copiada al portapapeles:\n\n{url}")

                ctk.CTkButton(buttons_frame, text="✅ Usar este sitio",
                            command=use_site,
                            fg_color=COLORS['success'],
                            width=150, height=28).pack(side="left", padx=5)

                ctk.CTkButton(buttons_frame, text="📋 Copiar URL",
                            command=copy_url,
                            width=120, height=28).pack(side="left", padx=5)

            # Botón cerrar
            ctk.CTkButton(main_frame, text="Cerrar",
                         command=sites_window.destroy,
                         width=120).pack(pady=(10, 0))

            self.log_message(f"✅ Encontrados {len(sites)} sitios en Search Console")

        except Exception as e:
            self.log_message(f"❌ Error obteniendo sitios: {str(e)}")
            messagebox.showerror("Error", f"Error obteniendo sitios:\n\n{str(e)}")

    def load_sc_keywords(self):
        """Carga las keywords de Search Console para el proyecto seleccionado"""
        try:
            # Verificar autenticación
            if not self.search_console_api.is_authenticated():
                messagebox.showwarning("Advertencia",
                                     "Debes autenticarte con Search Console primero.\n\n"
                                     "Ve a '⚙️ Configuración' → 'Google Search Console'")
                return

            # Verificar proyecto seleccionado
            if not hasattr(self, 'current_sc_project') or not self.current_sc_project:
                messagebox.showwarning("Advertencia", "Selecciona un proyecto primero")
                return

            # Verificar que el proyecto tenga URL de Search Console
            sc_property = self.current_sc_project.get('search_console_property')
            if not sc_property:
                messagebox.showwarning("Advertencia",
                                     "Este proyecto no tiene configurada una URL de Search Console.\n\n"
                                     "Ve a '🏢 Proyectos' y edita el proyecto para agregar la URL.")
                return

            self.log_message(f"🔄 Obteniendo keywords de Search Console para {self.current_sc_project['name']}...")

            # Obtener parámetros
            days = int(self.sc_days_var.get())
            limit = int(self.sc_limit_var.get())

            # Obtener datos
            queries = self.search_console_api.get_top_queries(sc_property, days=days, limit=limit)

            if not queries:
                messagebox.showinfo("Sin datos",
                                  "No se encontraron datos de Search Console.\n\n"
                                  "Posibles causas:\n"
                                  "• La URL del proyecto no coincide con la de Search Console\n"
                                  "• No hay datos en el rango de fechas seleccionado\n"
                                  "• El sitio no está verificado en Search Console")
                self.log_message("⚠️ No se encontraron datos de Search Console")
                return

            # Limpiar tabla
            for item in self.sc_tree.get_children():
                self.sc_tree.delete(item)

            # Calcular métricas totales
            total_clicks = 0
            total_impressions = 0
            total_ctr = 0
            total_position = 0

            # Llenar tabla
            for row in queries:
                query = row['keys'][0] if 'keys' in row else row.get('query', 'N/A')
                clicks = row.get('clicks', 0)
                impressions = row.get('impressions', 0)
                ctr = row.get('ctr', 0) * 100  # Convertir a porcentaje
                position = row.get('position', 0)

                self.sc_tree.insert("", "end", values=(
                    query,
                    clicks,
                    impressions,
                    f"{ctr:.2f}",
                    f"{position:.1f}"
                ))

                total_clicks += clicks
                total_impressions += impressions
                total_ctr += ctr
                total_position += position

            # Actualizar resumen
            count = len(queries)
            avg_ctr = total_ctr / count if count > 0 else 0
            avg_position = total_position / count if count > 0 else 0

            self.sc_total_clicks_label.configure(text=f"Total Clicks: {total_clicks:,}")
            self.sc_total_impressions_label.configure(text=f"Total Impresiones: {total_impressions:,}")
            self.sc_avg_ctr_label.configure(text=f"CTR Promedio: {avg_ctr:.2f}%")
            self.sc_avg_position_label.configure(text=f"Posición Promedio: {avg_position:.1f}")

            self.log_message(f"✅ Cargadas {count} keywords de Search Console")
            self.current_sc_data = queries  # Guardar para exportar

        except Exception as e:
            self.log_message(f"❌ Error cargando keywords de SC: {str(e)}")
            messagebox.showerror("Error", f"Error obteniendo datos:\n\n{str(e)}")

    def export_sc_data(self):
        """Exporta los datos de Search Console a CSV"""
        try:
            if not hasattr(self, 'current_sc_data') or not self.current_sc_data:
                messagebox.showwarning("Advertencia", "No hay datos para exportar.\n\nPrimero obtén las keywords.")
                return

            from tkinter import filedialog
            from datetime import datetime
            import csv

            # Pedir ubicación del archivo
            default_name = f"search_console_{self.current_sc_project['name'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                initialfile=default_name
            )

            if not file_path:
                return

            # Exportar
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Keyword', 'Clicks', 'Impresiones', 'CTR (%)', 'Posición Promedio'])

                for row in self.current_sc_data:
                    query = row['keys'][0] if 'keys' in row else row.get('query', 'N/A')
                    clicks = row.get('clicks', 0)
                    impressions = row.get('impressions', 0)
                    ctr = row.get('ctr', 0) * 100
                    position = row.get('position', 0)

                    writer.writerow([query, clicks, impressions, f"{ctr:.2f}", f"{position:.1f}"])

            messagebox.showinfo("Éxito", f"Datos exportados correctamente a:\n\n{file_path}")
            self.log_message(f"✅ Datos exportados a {file_path}")

        except Exception as e:
            self.log_message(f"❌ Error exportando datos: {str(e)}")
            messagebox.showerror("Error", f"Error exportando:\n\n{str(e)}")

    def sync_and_save_sc_data(self):
        """Sincroniza y guarda los datos de Search Console en el proyecto"""
        try:
            from datetime import datetime

            # Verificar que hay datos cargados
            if not hasattr(self, 'current_sc_data') or not self.current_sc_data:
                messagebox.showwarning("Advertencia",
                                     "No hay datos cargados.\n\nPrimero obtén las keywords.")
                return

            # Guardar datos en el proyecto
            sc_data = {
                'queries': self.current_sc_data[:100],  # Guardar top 100
                'total_queries': len(self.current_sc_data),
                'last_sync': datetime.now().isoformat(),
                'days_range': int(self.sc_days_var.get())
            }

            self.project_manager.update_search_console_data(
                self.current_sc_project['id'],
                sc_data
            )

            messagebox.showinfo("Éxito",
                              f"Datos sincronizados y guardados en el proyecto.\n\n"
                              f"• {len(self.current_sc_data)} keywords obtenidas\n"
                              f"• Top 100 guardadas en el proyecto")

            self.log_message(f"✅ Datos de SC guardados en proyecto {self.current_sc_project['name']}")

        except Exception as e:
            self.log_message(f"❌ Error sincronizando datos: {str(e)}")
            messagebox.showerror("Error", f"Error sincronizando:\n\n{str(e)}")


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
