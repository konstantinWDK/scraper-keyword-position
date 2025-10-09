"""
Métodos de gestión de reportes para la GUI del scraper de keywords
"""

import customtkinter as ctk
from tkinter import messagebox
import os
from pathlib import Path


class ReportMethods:
    """Clase con métodos para gestión de reportes"""
    
    def init_report_system(self):
        """Inicializa el sistema de reportes"""
        try:
            from reports import ReportManager
            self.report_manager = ReportManager()
            self.log_message("✅ Sistema de reportes inicializado")
        except Exception as e:
            self.log_message(f"❌ Error inicializando reportes: {e}")
            self.report_manager = None

    def refresh_reports_list(self, project_filter=None):
        """Actualiza la lista de reportes disponibles, opcionalmente filtrada por proyecto"""
        if not self.report_manager:
            self.show_no_reports_message()
            return
            
        try:
            # Limpiar lista actual
            for widget in self.reports_scrollable.winfo_children():
                widget.destroy()
            
            # Obtener todas las sesiones
            sessions = self.report_manager.get_all_sessions()
            
            # Filtrar por proyecto si se especifica
            if project_filter and project_filter != "Todos los proyectos":
                filtered_sessions = []
                
                # Obtener el proyecto seleccionado
                if hasattr(self, 'project_manager'):
                    projects = self.project_manager.get_all_projects()
                    selected_project = None
                    for p in projects:
                        if p['name'] == project_filter:
                            selected_project = p
                            break
                    
                    if selected_project:
                        # Filtrar sesiones que pertenecen al proyecto
                        project_reports = selected_project.get('reports', [])
                        project_report_ids = [r.get('session_id') for r in project_reports if 'session_id' in r]
                        
                        for session in sessions:
                            # Verificar si la sesión pertenece al proyecto por ID o dominio
                            session_id = session.get('session_id')
                            session_domain = session.get('target_domain', '')
                            project_domain = selected_project.get('domain', '')
                            
                            if (session_id in project_report_ids or 
                                (project_domain and session_domain and project_domain in session_domain)):
                                filtered_sessions.append(session)
                        
                        sessions = filtered_sessions
            
            if not sessions:
                self.show_no_reports_message()
                self.update_quick_stats(sessions)
                return
            
            # Mostrar cada sesión como una tarjeta
            for i, session in enumerate(sessions):
                self.create_report_card(session, i)
            
            # Actualizar estadísticas rápidas
            self.update_quick_stats(sessions)
            
            filter_text = f" (filtrado por '{project_filter}')" if project_filter and project_filter != "Todos los proyectos" else ""
            self.log_message(f"📋 Lista actualizada: {len(sessions)} reportes encontrados{filter_text}")
            
        except Exception as e:
            self.log_message(f"❌ Error actualizando lista: {e}")
            self.show_error_message(str(e))

    def create_report_card(self, session, index):
        """Crea una tarjeta visual para cada reporte"""
        from config.settings import COLORS
        
        # Frame principal de la tarjeta
        card_frame = ctk.CTkFrame(self.reports_scrollable)
        card_frame.pack(fill="x", padx=5, pady=5)
        
        # Header de la tarjeta
        header_frame = ctk.CTkFrame(card_frame)
        header_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        # Título con ID de sesión
        title_text = f"📊 Sesión {session['session_id']} - {session.get('target_domain', 'N/A')}"
        title_label = ctk.CTkLabel(header_frame, text=title_text, 
                                 font=ctk.CTkFont(size=14, weight="bold"))
        title_label.pack(side="left", padx=10, pady=8)
        
        # Fecha en el lado derecho
        try:
            from datetime import datetime
            timestamp = datetime.fromisoformat(session['timestamp'].replace('Z', '+00:00'))
            date_text = timestamp.strftime("%d/%m/%Y %H:%M")
        except:
            date_text = session.get('timestamp', 'N/A')[:16]
            
        date_label = ctk.CTkLabel(header_frame, text=f"🕒 {date_text}", 
                                font=ctk.CTkFont(size=11), 
                                text_color=COLORS['text_secondary'])
        date_label.pack(side="right", padx=10, pady=8)
        
        # Métricas de la sesión
        metrics_frame = ctk.CTkFrame(card_frame)
        metrics_frame.pack(fill="x", padx=10, pady=5)
        
        # Grid de métricas
        metrics_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Métricas individuales
        keywords_metric = ctk.CTkLabel(metrics_frame, 
                                     text=f"{session.get('total_keywords', 0)}\nKeywords", 
                                     font=ctk.CTkFont(size=12, weight="bold"),
                                     fg_color=COLORS['accent'], corner_radius=6)
        keywords_metric.grid(row=0, column=0, padx=2, pady=5, sticky="ew")
        
        results_metric = ctk.CTkLabel(metrics_frame, 
                                    text=f"{session.get('total_results', 0)}\nResultados", 
                                    font=ctk.CTkFont(size=12, weight="bold"),
                                    fg_color=COLORS['success'], corner_radius=6)
        results_metric.grid(row=0, column=1, padx=2, pady=5, sticky="ew")
        
        avg_pos_metric = ctk.CTkLabel(metrics_frame, 
                                    text=f"{session.get('average_position', 0):.1f}\nPos. Prom.", 
                                    font=ctk.CTkFont(size=12, weight="bold"),
                                    fg_color=COLORS['info'], corner_radius=6)
        avg_pos_metric.grid(row=0, column=2, padx=2, pady=5, sticky="ew")
        
        top10_metric = ctk.CTkLabel(metrics_frame, 
                                  text=f"{session.get('top_10_count', 0)}\nTop 10", 
                                  font=ctk.CTkFont(size=12, weight="bold"),
                                  fg_color=COLORS['warning'], corner_radius=6)
        top10_metric.grid(row=0, column=3, padx=2, pady=5, sticky="ew")
        
        # Botones de acción
        actions_frame = ctk.CTkFrame(card_frame)
        actions_frame.pack(fill="x", padx=10, pady=(5, 10))
        
        ctk.CTkButton(actions_frame, text="👁️ Ver Detalles", 
                     command=lambda s=session: self.view_report_details(s['session_id']),
                     fg_color=COLORS['accent'], width=100, height=28).pack(side="left", padx=(5, 5))
        
        ctk.CTkButton(actions_frame, text="📊 Generar HTML", 
                     command=lambda s=session: self.generate_html_report(s['session_id']),
                     fg_color=COLORS['success'], width=100, height=28).pack(side="left", padx=5)
        
        ctk.CTkButton(actions_frame, text="📈 Análisis", 
                     command=lambda s=session: self.analyze_session(s['session_id']),
                     fg_color=COLORS['info'], width=100, height=28).pack(side="left", padx=5)
        
        ctk.CTkButton(actions_frame, text="🗑️ Eliminar", 
                     command=lambda s=session: self.delete_report(s['session_id']),
                     fg_color=COLORS['error'], width=80, height=28).pack(side="right", padx=5)

    def show_no_reports_message(self):
        """Muestra mensaje cuando no hay reportes"""
        from config.settings import COLORS
        
        no_reports_frame = ctk.CTkFrame(self.reports_scrollable)
        no_reports_frame.pack(fill="both", expand=True, padx=20, pady=50)
        
        ctk.CTkLabel(no_reports_frame, text="📁", font=ctk.CTkFont(size=48)).pack(pady=(30, 10))
        ctk.CTkLabel(no_reports_frame, text="No hay informes guardados aún", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)
        ctk.CTkLabel(no_reports_frame, text="Ejecuta un scraping para generar tu primer informe", 
                    font=ctk.CTkFont(size=12), text_color=COLORS['text_secondary']).pack(pady=(5, 30))

    def show_error_message(self, error_text):
        """Muestra mensaje de error"""
        from config.settings import COLORS
        
        error_frame = ctk.CTkFrame(self.reports_scrollable)
        error_frame.pack(fill="both", expand=True, padx=20, pady=50)
        
        ctk.CTkLabel(error_frame, text="❌", font=ctk.CTkFont(size=48)).pack(pady=(30, 10))
        ctk.CTkLabel(error_frame, text="Error cargando reportes", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)
        ctk.CTkLabel(error_frame, text=f"Detalles: {error_text}", 
                    font=ctk.CTkFont(size=11), text_color=COLORS['text_secondary']).pack(pady=(5, 30))

    def update_quick_stats(self, sessions):
        """Actualiza las estadísticas rápidas"""
        if not sessions:
            self.total_sessions_label.configure(text="0\nSesiones Totales")
            self.total_keywords_label.configure(text="0\nKeywords Analizadas")
            self.avg_position_label.configure(text="0.0\nPosición Promedio")
            self.top_10_rate_label.configure(text="0%\nRate Top 10")
            return
        
        total_sessions = len(sessions)
        total_keywords = sum(s.get('total_keywords', 0) for s in sessions)
        total_results = sum(s.get('total_results', 0) for s in sessions)
        total_top10 = sum(s.get('top_10_count', 0) for s in sessions)
        
        # Calcular promedios
        avg_position = sum(s.get('average_position', 0) for s in sessions) / total_sessions if total_sessions > 0 else 0
        top10_rate = (total_top10 / total_results * 100) if total_results > 0 else 0
        
        # Actualizar labels
        self.total_sessions_label.configure(text=f"{total_sessions}\nSesiones Totales")
        self.total_keywords_label.configure(text=f"{total_keywords}\nKeywords Analizadas")
        self.avg_position_label.configure(text=f"{avg_position:.1f}\nPosición Promedio")
        self.top_10_rate_label.configure(text=f"{top10_rate:.1f}%\nRate Top 10")

    def view_report_details(self, session_id):
        """Muestra los detalles de un reporte específico"""
        from config.settings import COLORS
        
        if not self.report_manager:
            messagebox.showerror("Error", "Sistema de reportes no disponible")
            return
            
        try:
            session_data = self.report_manager.load_session(session_id)
            if not session_data:
                messagebox.showerror("Error", f"No se pudo cargar la sesión {session_id}")
                return
            
            # Crear ventana de detalles
            details_window = ctk.CTkToplevel(self.root)
            details_window.title(f"Detalles - Sesión {session_id}")
            details_window.geometry("800x600")
            
            # Contenido scrollable
            scroll_frame = ctk.CTkScrollableFrame(details_window)
            scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            # Título
            ctk.CTkLabel(scroll_frame, text=f"📊 Detalles de Sesión {session_id}", 
                        font=ctk.CTkFont(size=20, weight="bold")).pack(pady=(0, 20))
            
            # Información de la sesión
            info_frame = ctk.CTkFrame(scroll_frame)
            info_frame.pack(fill="x", pady=(0, 20))
            
            session_info = session_data.get('session_info', {})
            
            info_text = f"""
📅 Fecha: {session_data.get('timestamp', 'N/A')}
🎯 Dominio objetivo: {session_info.get('target_domain', 'N/A')}
🔍 Keywords totales: {session_data.get('total_keywords', 0)}
📊 Resultados totales: {session_data.get('total_results', 0)}
📈 Posición promedio: {session_data.get('average_position', 0):.2f}
🏆 Resultados Top 10: {session_data.get('top_10_count', 0)}
🥇 Resultados Top 3: {session_data.get('top_3_count', 0)}
🌐 Dominios únicos: {len(session_data.get('domains_found', []))}
            """
            
            ctk.CTkLabel(info_frame, text=info_text, justify="left", 
                        font=ctk.CTkFont(size=12)).pack(padx=20, pady=15)
            
            # Botones de acción
            buttons_frame = ctk.CTkFrame(scroll_frame)
            buttons_frame.pack(fill="x", pady=(0, 10))
            
            ctk.CTkButton(buttons_frame, text="📊 Generar Reporte HTML", 
                         command=lambda: self.generate_html_report(session_id),
                         fg_color=COLORS['success']).pack(side="left", padx=10, pady=10)
            
            ctk.CTkButton(buttons_frame, text="📈 Análisis Detallado", 
                         command=lambda: self.analyze_session(session_id),
                         fg_color=COLORS['info']).pack(side="left", padx=10, pady=10)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error mostrando detalles: {e}")

    def generate_html_report(self, session_id):
        """Genera un reporte HTML para una sesión específica"""
        if not self.report_manager:
            messagebox.showerror("Error", "Sistema de reportes no disponible")
            return
            
        try:
            self.log_message(f"📊 Generando reporte HTML para sesión {session_id}...")
            
            # Generar reporte detallado
            report_data = self.report_manager.generate_detailed_report(session_id)
            
            # Exportar a HTML
            html_path = self.report_manager.export_to_html(report_data, session_id)
            
            self.log_message(f"✅ Reporte HTML generado: {html_path}")
            
            # Preguntar si abrir el archivo
            if messagebox.askyesno("Reporte Generado", 
                                 f"✅ Reporte HTML generado exitosamente!\n\n"
                                 f"📁 Ubicación: {html_path}\n\n"
                                 f"¿Deseas abrir el reporte ahora?"):
                import webbrowser
                webbrowser.open(f"file://{html_path}")
                
        except Exception as e:
            self.log_message(f"❌ Error generando reporte HTML: {e}")
            messagebox.showerror("Error", f"Error generando reporte HTML:\n\n{e}")

    def analyze_session(self, session_id):
        """Realiza análisis detallado de una sesión"""
        if not self.report_manager:
            messagebox.showerror("Error", "Sistema de reportes no disponible")
            return
            
        try:
            self.log_message(f"📈 Analizando sesión {session_id}...")
            
            report_data = self.report_manager.generate_detailed_report(session_id)
            
            # Cambiar a la pestaña de análisis
            self.tabview.set("📈 Análisis")
            
            # Mostrar análisis en la pestaña correspondiente
            self.display_analysis_results(report_data)
            
            self.log_message(f"✅ Análisis completado para sesión {session_id}")
            
        except Exception as e:
            self.log_message(f"❌ Error en análisis: {e}")
            messagebox.showerror("Error", f"Error realizando análisis:\n\n{e}")

    def delete_report(self, session_id):
        """Elimina un reporte específico"""
        if messagebox.askyesno("Confirmar Eliminación", 
                             f"¿Estás seguro de que deseas eliminar el reporte de la sesión {session_id}?\n\n"
                             f"Esta acción no se puede deshacer."):
            try:
                reports_dir = Path("reports")
                deleted_files = 0
                
                # Eliminar JSON
                json_files = list((reports_dir / "json").glob(f"session_{session_id}*.json"))
                for file_path in json_files:
                    file_path.unlink()
                    deleted_files += 1
                
                # Eliminar HTML
                html_files = list((reports_dir / "html").glob(f"report_{session_id}*.html"))
                for file_path in html_files:
                    file_path.unlink()
                    deleted_files += 1
                
                # Eliminar imágenes
                image_files = list((reports_dir / "images").glob(f"*_{session_id}*.png"))
                for file_path in image_files:
                    file_path.unlink()
                    deleted_files += 1
                
                self.log_message(f"🗑️ Eliminados {deleted_files} archivos de la sesión {session_id}")
                
                # Actualizar lista
                self.refresh_reports_list()
                
                messagebox.showinfo("Eliminación Completada", 
                                  f"✅ Reporte eliminado exitosamente!\n\n"
                                  f"🗑️ Archivos eliminados: {deleted_files}")
                
            except Exception as e:
                self.log_message(f"❌ Error eliminando reporte: {e}")
                messagebox.showerror("Error", f"Error eliminando reporte:\n\n{e}")

    def open_reports_folder(self):
        """Abre la carpeta de reportes"""
        try:
            reports_path = os.path.abspath("reports")
            
            if not os.path.exists(reports_path):
                os.makedirs(reports_path, exist_ok=True)
            
            # Abrir carpeta según el sistema operativo
            if os.name == 'nt':  # Windows
                os.startfile(reports_path)
            elif os.name == 'posix':  # Linux/Mac
                import subprocess
                subprocess.run(['xdg-open', reports_path])
            
            self.log_message(f"📂 Carpeta de reportes abierta: {reports_path}")
            
        except Exception as e:
            self.log_message(f"❌ Error abriendo carpeta: {e}")
            messagebox.showerror("Error", f"Error abriendo carpeta de reportes:\n\n{e}")

    def cleanup_old_reports(self):
        """Limpia reportes antiguos"""
        if not self.report_manager:
            messagebox.showerror("Error", "Sistema de reportes no disponible")
            return
            
        if messagebox.askyesno("Limpiar Reportes Antiguos", 
                             "¿Deseas eliminar reportes de más de 30 días?\n\n"
                             "Esta acción no se puede deshacer."):
            try:
                self.report_manager.cleanup_old_reports(days_to_keep=30)
                self.refresh_reports_list()
                self.log_message("🧹 Limpieza de reportes antiguos completada")
                messagebox.showinfo("Limpieza Completada", "✅ Reportes antiguos eliminados exitosamente!")
                
            except Exception as e:
                self.log_message(f"❌ Error en limpieza: {e}")
                messagebox.showerror("Error", f"Error limpiando reportes:\n\n{e}")

    def display_analysis_results(self, report_data):
        """Muestra los resultados del análisis en la pestaña correspondiente"""
        try:
            # Implementar visualización de análisis
            # Por ahora, mostrar mensaje básico
            self.log_message("📈 Análisis mostrado en pestaña de Análisis")
        except Exception as e:
            self.log_message(f"❌ Error mostrando análisis: {e}")