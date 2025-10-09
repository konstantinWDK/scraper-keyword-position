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