import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import logging

class ProjectManager:
    """Gestor de proyectos para el scraper de keywords"""
    
    def __init__(self):
        self.projects_file = Path("data/projects.json")
        self.projects_dir = Path("data/projects")
        self.logger = logging.getLogger(__name__)
        
        # Crear directorios necesarios
        self.projects_dir.mkdir(parents=True, exist_ok=True)
        
        # Inicializar archivo de proyectos si no existe
        if not self.projects_file.exists():
            self._create_empty_projects_file()
    
    def _create_empty_projects_file(self):
        """Crea un archivo de proyectos vacío"""
        empty_data = {
            "projects": {},
            "active_project": None,
            "created_at": datetime.now().isoformat(),
            "version": "1.0"
        }
        
        with open(self.projects_file, 'w', encoding='utf-8') as f:
            json.dump(empty_data, f, indent=2, ensure_ascii=False)
    
    def load_projects(self) -> Dict:
        """Carga todos los proyectos desde el archivo JSON"""
        try:
            with open(self.projects_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error cargando proyectos: {e}")
            return {"projects": {}, "active_project": None}
    
    def save_projects(self, data: Dict):
        """Guarda los proyectos en el archivo JSON"""
        try:
            data["updated_at"] = datetime.now().isoformat()
            with open(self.projects_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Error guardando proyectos: {e}")
            raise
    
    def create_project(self, name: str, domain: str, description: str = "", 
                      search_console_property: str = "") -> str:
        """Crea un nuevo proyecto"""
        if not name or not domain:
            raise ValueError("El nombre y dominio son obligatorios")
        
        data = self.load_projects()
        
        # Generar ID único
        project_id = f"project_{len(data['projects']) + 1}_{int(datetime.now().timestamp())}"
        
        # Verificar que no exista un proyecto con el mismo nombre
        for pid, project in data['projects'].items():
            if project['name'].lower() == name.lower():
                raise ValueError(f"Ya existe un proyecto con el nombre '{name}'")
        
        # Crear estructura del proyecto
        project_data = {
            "id": project_id,
            "name": name,
            "domain": domain,
            "description": description,
            "search_console_property": search_console_property,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "keywords": [],
            "reports": [],
            "settings": {
                "country": "es",
                "language": "es",
                "pages_to_scrape": 10,
                "delay_between_requests": 2
            },
            "search_console_data": {
                "last_sync": None,
                "queries": [],
                "pages": [],
                "devices": []
            }
        }
        
        # Agregar proyecto
        data['projects'][project_id] = project_data
        
        # Crear directorio del proyecto
        project_dir = self.projects_dir / project_id
        project_dir.mkdir(exist_ok=True)
        
        # Guardar datos
        self.save_projects(data)
        
        self.logger.info(f"Proyecto creado: {name} ({project_id})")
        return project_id
    
    def get_project(self, project_id: str) -> Optional[Dict]:
        """Obtiene un proyecto específico"""
        data = self.load_projects()
        return data['projects'].get(project_id)
    
    def get_all_projects(self) -> Dict[str, Dict]:
        """Obtiene todos los proyectos"""
        data = self.load_projects()
        return data['projects']
    
    def update_project(self, project_id: str, updates: Dict):
        """Actualiza un proyecto existente"""
        data = self.load_projects()
        
        if project_id not in data['projects']:
            raise ValueError(f"Proyecto {project_id} no encontrado")
        
        # Actualizar campos
        for key, value in updates.items():
            if key in data['projects'][project_id]:
                data['projects'][project_id][key] = value
        
        data['projects'][project_id]['updated_at'] = datetime.now().isoformat()
        
        self.save_projects(data)
        self.logger.info(f"Proyecto actualizado: {project_id}")
    
    def delete_project(self, project_id: str):
        """Elimina un proyecto"""
        data = self.load_projects()
        
        if project_id not in data['projects']:
            raise ValueError(f"Proyecto {project_id} no encontrado")
        
        # Eliminar directorio del proyecto
        project_dir = self.projects_dir / project_id
        if project_dir.exists():
            import shutil
            shutil.rmtree(project_dir)
        
        # Eliminar del archivo
        del data['projects'][project_id]
        
        # Si era el proyecto activo, desactivarlo
        if data['active_project'] == project_id:
            data['active_project'] = None
        
        self.save_projects(data)
        self.logger.info(f"Proyecto eliminado: {project_id}")
    
    def set_active_project(self, project_id: str):
        """Establece el proyecto activo"""
        data = self.load_projects()
        
        if project_id and project_id not in data['projects']:
            raise ValueError(f"Proyecto {project_id} no encontrado")
        
        data['active_project'] = project_id
        self.save_projects(data)
        self.logger.info(f"Proyecto activo establecido: {project_id}")
    
    def get_active_project(self) -> Optional[Dict]:
        """Obtiene el proyecto activo"""
        data = self.load_projects()
        active_id = data.get('active_project')
        
        if active_id and active_id in data['projects']:
            return data['projects'][active_id]
        
        return None
    
    def get_active_project_id(self) -> Optional[str]:
        """Obtiene el ID del proyecto activo"""
        data = self.load_projects()
        return data.get('active_project')
    
    def add_keywords_to_project(self, project_id: str, keywords: List[str]):
        """Agrega keywords a un proyecto"""
        data = self.load_projects()
        
        if project_id not in data['projects']:
            raise ValueError(f"Proyecto {project_id} no encontrado")
        
        # Agregar keywords únicas
        existing_keywords = set(data['projects'][project_id]['keywords'])
        new_keywords = [kw for kw in keywords if kw not in existing_keywords]
        
        data['projects'][project_id]['keywords'].extend(new_keywords)
        data['projects'][project_id]['updated_at'] = datetime.now().isoformat()
        
        self.save_projects(data)
        self.logger.info(f"Agregadas {len(new_keywords)} keywords al proyecto {project_id}")
        
        return len(new_keywords)
    
    def get_project_keywords(self, project_id: str) -> List[str]:
        """Obtiene las keywords de un proyecto"""
        project = self.get_project(project_id)
        return project['keywords'] if project else []
    
    def add_report_to_project(self, project_id: str, report_data: Dict):
        """Agrega un reporte a un proyecto"""
        data = self.load_projects()
        
        if project_id not in data['projects']:
            raise ValueError(f"Proyecto {project_id} no encontrado")
        
        report_data['created_at'] = datetime.now().isoformat()
        report_data['project_id'] = project_id
        
        data['projects'][project_id]['reports'].append(report_data)
        data['projects'][project_id]['updated_at'] = datetime.now().isoformat()
        
        self.save_projects(data)
        self.logger.info(f"Reporte agregado al proyecto {project_id}")
    
    def get_project_reports(self, project_id: str) -> List[Dict]:
        """Obtiene los reportes de un proyecto"""
        project = self.get_project(project_id)
        return project['reports'] if project else []
    
    def get_project_directory(self, project_id: str) -> Path:
        """Obtiene el directorio de un proyecto"""
        return self.projects_dir / project_id
    
    def update_search_console_data(self, project_id: str, sc_data: Dict):
        """Actualiza los datos de Search Console para un proyecto"""
        data = self.load_projects()
        
        if project_id not in data['projects']:
            raise ValueError(f"Proyecto {project_id} no encontrado")
        
        data['projects'][project_id]['search_console_data'].update(sc_data)
        data['projects'][project_id]['search_console_data']['last_sync'] = datetime.now().isoformat()
        data['projects'][project_id]['updated_at'] = datetime.now().isoformat()
        
        self.save_projects(data)
        self.logger.info(f"Datos de Search Console actualizados para proyecto {project_id}")