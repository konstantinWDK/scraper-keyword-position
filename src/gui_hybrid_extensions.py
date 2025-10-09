"""
🎨 Extensiones de GUI para Funcionalidades Híbridas
Añade pestañas y funcionalidades visuales para el sistema híbrido
"""

import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
import webbrowser
import threading
from datetime import datetime, timedelta
from typing import Dict, List
from search_console_wrapper import SearchConsoleAPI
from sc_scraper_sync import SearchConsoleScraperSync
from hybrid_analyzer import HybridAnalyzer
from hybrid_report_generator import HybridReportGenerator


class HybridGUIExtensions:
    """
    Mixin class que añade funcionalidades híbridas a la GUI principal
    """

    def setup_hybrid_tab(self):
        """Configura la pestaña de Análisis Híbrido"""
        # Agregar pestaña si no existe
        if not hasattr(self, 'tab_hybrid'):
            self.tab_hybrid = self.tabview.add("🔄 Híbrido")

        # Frame principal con scroll
        main_frame = ctk.CTkScrollableFrame(self.tab_hybrid)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # === SECCIÓN 1: SINCRONIZACIÓN DE KEYWORDS ===
        sync_frame = ctk.CTkFrame(main_frame)
        sync_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(
            sync_frame,
            text="📥 Sincronización con Search Console",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        # Opciones de sincronización
        sync_options_frame = ctk.CTkFrame(sync_frame)
        sync_options_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(
            sync_options_frame,
            text="Días de datos:"
        ).grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.sync_days_var = ctk.IntVar(value=30)
        days_slider = ctk.CTkSlider(
            sync_options_frame,
            from_=7,
            to=90,
            number_of_steps=11,
            variable=self.sync_days_var
        )
        days_slider.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        self.sync_days_label = ctk.CTkLabel(sync_options_frame, text="30 días")
        self.sync_days_label.grid(row=0, column=2, padx=10, pady=5)

        def update_days_label(value):
            self.sync_days_label.configure(text=f"{int(float(value))} días")

        days_slider.configure(command=update_days_label)

        ctk.CTkLabel(
            sync_options_frame,
            text="Impresiones mínimas:"
        ).grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.min_impressions_var = ctk.StringVar(value="50")
        ctk.CTkEntry(
            sync_options_frame,
            textvariable=self.min_impressions_var,
            width=100
        ).grid(row=1, column=1, padx=10, pady=5, sticky="w")

        self.auto_add_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(
            sync_options_frame,
            text="Añadir automáticamente al proyecto",
            variable=self.auto_add_var
        ).grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        sync_options_frame.grid_columnconfigure(1, weight=1)

        # Botón de sincronización
        sync_button = ctk.CTkButton(
            sync_frame,
            text="🔄 Sincronizar Keywords desde Search Console",
            command=self.sync_keywords_from_sc,
            height=40,
            font=("Arial", 14, "bold")
        )
        sync_button.pack(pady=10)

        self.sync_status_label = ctk.CTkLabel(
            sync_frame,
            text="",
            font=("Arial", 12)
        )
        self.sync_status_label.pack(pady=5)

        # === SECCIÓN 2: ESTRATEGIAS DE SCRAPING ===
        strategy_frame = ctk.CTkFrame(main_frame)
        strategy_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(
            strategy_frame,
            text="🎯 Listas Inteligentes de Scraping",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        # Selector de estrategia
        strategy_select_frame = ctk.CTkFrame(strategy_frame)
        strategy_select_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(
            strategy_select_frame,
            text="Estrategia:"
        ).pack(side="left", padx=10)

        self.strategy_var = ctk.StringVar(value="opportunities")
        strategy_menu = ctk.CTkOptionMenu(
            strategy_select_frame,
            variable=self.strategy_var,
            values=[
                "opportunities (Máximo ROI)",
                "top_volume (Más impresiones)",
                "low_hanging (Quick wins)"
            ],
            width=300
        )
        strategy_menu.pack(side="left", padx=10)

        ctk.CTkLabel(
            strategy_select_frame,
            text="Límite:"
        ).pack(side="left", padx=10)

        self.strategy_limit_var = ctk.StringVar(value="50")
        ctk.CTkEntry(
            strategy_select_frame,
            textvariable=self.strategy_limit_var,
            width=80
        ).pack(side="left", padx=10)

        # Botón para obtener lista
        get_list_button = ctk.CTkButton(
            strategy_frame,
            text="📋 Obtener Lista Inteligente",
            command=self.get_smart_scraping_list,
            height=40,
            font=("Arial", 14, "bold")
        )
        get_list_button.pack(pady=10)

        self.strategy_status_label = ctk.CTkLabel(
            strategy_frame,
            text="",
            font=("Arial", 12)
        )
        self.strategy_status_label.pack(pady=5)

        # === SECCIÓN 3: ANÁLISIS Y REPORTES ===
        analysis_frame = ctk.CTkFrame(main_frame)
        analysis_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(
            analysis_frame,
            text="📊 Análisis Híbrido y Reportes",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        # Botones de análisis
        buttons_frame = ctk.CTkFrame(analysis_frame)
        buttons_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkButton(
            buttons_frame,
            text="🚀 Detectar Oportunidades",
            command=self.detect_opportunities,
            height=40,
            width=250
        ).pack(side="left", padx=10, pady=5)

        ctk.CTkButton(
            buttons_frame,
            text="📝 Encontrar Gaps de Contenido",
            command=self.find_content_gaps,
            height=40,
            width=250
        ).pack(side="left", padx=10, pady=5)

        buttons_frame2 = ctk.CTkFrame(analysis_frame)
        buttons_frame2.pack(fill="x", padx=20, pady=10)

        ctk.CTkButton(
            buttons_frame2,
            text="🔍 Comparar Posiciones SC vs Scraper",
            command=self.compare_positions,
            height=40,
            width=250
        ).pack(side="left", padx=10, pady=5)

        ctk.CTkButton(
            buttons_frame2,
            text="📄 Generar Reporte HTML Completo",
            command=self.generate_hybrid_report,
            height=40,
            width=250,
            fg_color="#10b981"
        ).pack(side="left", padx=10, pady=5)

        # === SECCIÓN 4: RESULTADOS ===
        results_frame = ctk.CTkFrame(main_frame)
        results_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(
            results_frame,
            text="📈 Resultados del Análisis",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        # Tabla de resultados
        self.hybrid_results_tree = ttk.Treeview(
            results_frame,
            columns=("metric", "value", "details"),
            show="headings",
            height=15
        )

        self.hybrid_results_tree.heading("metric", text="Métrica")
        self.hybrid_results_tree.heading("value", text="Valor")
        self.hybrid_results_tree.heading("details", text="Detalles")

        self.hybrid_results_tree.column("metric", width=200)
        self.hybrid_results_tree.column("value", width=150)
        self.hybrid_results_tree.column("details", width=400)

        # Scrollbar
        scrollbar = ttk.Scrollbar(
            results_frame,
            orient="vertical",
            command=self.hybrid_results_tree.yview
        )
        self.hybrid_results_tree.configure(yscrollcommand=scrollbar.set)

        self.hybrid_results_tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")

    def sync_keywords_from_sc(self):
        """Sincroniza keywords desde Search Console"""
        def sync_thread():
            try:
                self.sync_status_label.configure(text="🔄 Sincronizando...")

                # Obtener proyecto activo
                project = self.project_manager.get_active_project()
                if not project:
                    messagebox.showerror("Error", "No hay proyecto activo seleccionado")
                    self.sync_status_label.configure(text="❌ Error: Sin proyecto activo")
                    return

                project_id = project['id']

                # Verificar autenticación de SC
                if not self.search_console_api.is_authenticated():
                    messagebox.showerror(
                        "Error",
                        "No estás autenticado con Search Console.\n"
                        "Ve a la pestaña '🔍 Search Console' para autenticarte."
                    )
                    self.sync_status_label.configure(text="❌ Error: No autenticado")
                    return

                # Crear sync manager
                sync = SearchConsoleScraperSync(self.project_manager)

                # Obtener parámetros
                days = self.sync_days_var.get()
                min_impressions = int(self.min_impressions_var.get())
                auto_add = self.auto_add_var.get()

                # Sincronizar
                result = sync.sync_keywords_to_project(
                    project_id=project_id,
                    days=days,
                    min_impressions=min_impressions,
                    auto_add=auto_add
                )

                if result['success']:
                    total = result['total_sc_keywords']
                    new = result['new_keywords_found']
                    added = result['keywords_added']

                    message = (
                        f"✅ Sincronización completada:\n\n"
                        f"• Keywords en Search Console: {total}\n"
                        f"• Nuevas keywords encontradas: {new}\n"
                        f"• Keywords añadidas: {added}"
                    )

                    self.sync_status_label.configure(
                        text=f"✅ {total} keywords, {new} nuevas, {added} añadidas"
                    )

                    # Mostrar preview de nuevas keywords
                    if result.get('new_keywords_list'):
                        preview = "\n\nTop 10 nuevas keywords:\n"
                        for i, kw in enumerate(result['new_keywords_list'][:10], 1):
                            preview += f"{i}. {kw}\n"
                        message += preview

                    messagebox.showinfo("Sincronización Completada", message)

                else:
                    error_msg = result.get('message', 'Error desconocido')
                    messagebox.showerror("Error", f"Error en sincronización:\n{error_msg}")
                    self.sync_status_label.configure(text=f"❌ Error: {error_msg}")

            except Exception as e:
                messagebox.showerror("Error", f"Error en sincronización:\n{str(e)}")
                self.sync_status_label.configure(text=f"❌ Error: {str(e)}")

        # Ejecutar en thread
        thread = threading.Thread(target=sync_thread, daemon=True)
        thread.start()

    def get_smart_scraping_list(self):
        """Obtiene lista inteligente de keywords para scrapear"""
        def get_list_thread():
            try:
                self.strategy_status_label.configure(text="🔄 Generando lista...")

                # Obtener proyecto activo
                project = self.project_manager.get_active_project()
                if not project:
                    messagebox.showerror("Error", "No hay proyecto activo seleccionado")
                    self.strategy_status_label.configure(text="❌ Error: Sin proyecto activo")
                    return

                project_id = project['id']

                # Verificar autenticación de SC
                if not self.search_console_api.is_authenticated():
                    messagebox.showerror(
                        "Error",
                        "No estás autenticado con Search Console.\n"
                        "Esta funcionalidad requiere datos de Search Console."
                    )
                    self.strategy_status_label.configure(text="❌ Error: No autenticado")
                    return

                # Crear sync manager
                sync = SearchConsoleScraperSync(self.project_manager)

                # Obtener parámetros
                strategy_full = self.strategy_var.get()
                strategy = strategy_full.split(' ')[0]  # Extraer 'opportunities', 'top_volume', etc.
                limit = int(self.strategy_limit_var.get())

                # Obtener lista
                keywords = sync.get_smart_scraping_list(
                    project_id=project_id,
                    strategy=strategy,
                    limit=limit
                )

                if keywords:
                    # Añadir a la pestaña de keywords
                    if hasattr(self, 'keywords_text') and self.keywords_text:
                        current = self.keywords_text.get("1.0", "end-1c")
                        new_keywords = "\n".join(keywords)

                        if current.strip():
                            combined = current + "\n" + new_keywords
                        else:
                            combined = new_keywords

                        self.keywords_text.delete("1.0", "end")
                        self.keywords_text.insert("1.0", combined)

                        self.update_keywords_count()

                    message = (
                        f"✅ Lista generada:\n\n"
                        f"Estrategia: {strategy}\n"
                        f"Keywords obtenidas: {len(keywords)}\n\n"
                        f"Las keywords han sido añadidas a la pestaña '🔑 Keywords'"
                    )

                    self.strategy_status_label.configure(
                        text=f"✅ {len(keywords)} keywords añadidas"
                    )

                    messagebox.showinfo("Lista Generada", message)

                else:
                    messagebox.showwarning(
                        "Sin Resultados",
                        "No se obtuvieron keywords.\n"
                        "Verifica que haya datos en Search Console."
                    )
                    self.strategy_status_label.configure(text="⚠️ Sin resultados")

            except Exception as e:
                messagebox.showerror("Error", f"Error generando lista:\n{str(e)}")
                self.strategy_status_label.configure(text=f"❌ Error: {str(e)}")

        # Ejecutar en thread
        thread = threading.Thread(target=get_list_thread, daemon=True)
        thread.start()

    def detect_opportunities(self):
        """Detecta oportunidades de mejora"""
        def detect_thread():
            try:
                # Limpiar tabla
                for item in self.hybrid_results_tree.get_children():
                    self.hybrid_results_tree.delete(item)

                # Verificar datos
                if not self.current_results:
                    messagebox.showwarning(
                        "Sin Datos",
                        "Primero debes hacer un scraping.\n"
                        "Ve a la pestaña '🚀 Scraping' y ejecuta un análisis."
                    )
                    return

                project = self.project_manager.get_active_project()
                if not project:
                    messagebox.showerror("Error", "No hay proyecto activo")
                    return

                site_url = project.get('search_console_property')
                if not site_url:
                    messagebox.showerror(
                        "Error",
                        "El proyecto no tiene URL de Search Console configurada"
                    )
                    return

                # Obtener datos de SC
                end_date = datetime.now().date()
                start_date = end_date - timedelta(days=30)

                sc_data_response = self.search_console_api.get_search_analytics(
                    site_url=site_url,
                    start_date=start_date.isoformat(),
                    end_date=end_date.isoformat(),
                    dimensions=['query'],
                    row_limit=1000
                )

                if not sc_data_response or 'rows' not in sc_data_response:
                    messagebox.showerror(
                        "Error",
                        "No hay datos disponibles en Search Console"
                    )
                    return

                sc_data = sc_data_response['rows']

                # Analizar
                analyzer = HybridAnalyzer()
                opportunities = analyzer.find_keyword_opportunities(
                    sc_data=sc_data,
                    min_impressions=100,
                    max_position=20.0,
                    min_position=4.0
                )

                # Mostrar en tabla
                for i, opp in enumerate(opportunities[:20], 1):
                    self.hybrid_results_tree.insert(
                        "",
                        "end",
                        values=(
                            f"{i}. {opp['keyword']}",
                            f"Pos: {opp['current_position']:.1f}",
                            f"Impres: {opp['impressions']:,} | Potencial: +{opp['potential_additional_clicks']} clicks/mes | {opp['priority']}"
                        )
                    )

                messagebox.showinfo(
                    "Oportunidades Detectadas",
                    f"Se encontraron {len(opportunities)} oportunidades de mejora.\n\n"
                    f"Mostrando top 20 en la tabla."
                )

            except Exception as e:
                messagebox.showerror("Error", f"Error detectando oportunidades:\n{str(e)}")

        thread = threading.Thread(target=detect_thread, daemon=True)
        thread.start()

    def find_content_gaps(self):
        """Encuentra gaps de contenido"""
        def gaps_thread():
            try:
                # Similar a detect_opportunities pero llama a find_missing_content_gaps
                # ... (implementar similar al anterior)
                messagebox.showinfo("Funcionalidad", "Detectando gaps de contenido...")

            except Exception as e:
                messagebox.showerror("Error", f"Error:\n{str(e)}")

        thread = threading.Thread(target=gaps_thread, daemon=True)
        thread.start()

    def compare_positions(self):
        """Compara posiciones SC vs Scraper"""
        def compare_thread():
            try:
                # Similar a detect_opportunities pero llama a compare_positions
                # ... (implementar similar al anterior)
                messagebox.showinfo("Funcionalidad", "Comparando posiciones...")

            except Exception as e:
                messagebox.showerror("Error", f"Error:\n{str(e)}")

        thread = threading.Thread(target=compare_thread, daemon=True)
        thread.start()

    def generate_hybrid_report(self):
        """Genera reporte HTML completo"""
        def report_thread():
            try:
                if not self.current_results:
                    messagebox.showwarning(
                        "Sin Datos",
                        "Primero debes hacer un scraping con datos disponibles."
                    )
                    return

                project = self.project_manager.get_active_project()
                if not project:
                    messagebox.showerror("Error", "No hay proyecto activo")
                    return

                # Crear análisis completo
                sync = SearchConsoleScraperSync(self.project_manager)
                analysis = sync.analyze_scraping_session_with_sc(
                    project_id=project['id'],
                    scraper_results=self.current_results,
                    save_to_project=True
                )

                if not analysis:
                    messagebox.showerror("Error", "No se pudo generar el análisis")
                    return

                # Generar reporte HTML
                generator = HybridReportGenerator()
                report_path = generator.generate_html_report(
                    analysis=analysis,
                    project_name=project['name']
                )

                if report_path:
                    # Preguntar si abrir
                    result = messagebox.askyesno(
                        "Reporte Generado",
                        f"Reporte HTML generado exitosamente:\n\n"
                        f"{report_path}\n\n"
                        f"¿Deseas abrirlo en tu navegador?"
                    )

                    if result:
                        webbrowser.open(f"file://{report_path}")

                else:
                    messagebox.showerror("Error", "No se pudo generar el reporte HTML")

            except Exception as e:
                messagebox.showerror("Error", f"Error generando reporte:\n{str(e)}")

        thread = threading.Thread(target=report_thread, daemon=True)
        thread.start()
