import os
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import requests
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class SearchConsoleAPI:
    """Cliente para la API de Google Search Console"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.service = None
        self.credentials = None
        
        # Scopes necesarios para Search Console
        self.SCOPES = [
            'https://www.googleapis.com/auth/webmasters.readonly',
            'https://www.googleapis.com/auth/webmasters'
        ]
        
        # Archivo para almacenar credenciales
        self.credentials_file = "data/search_console_credentials.json"
        self.token_file = "data/search_console_token.json"
    
    def setup_oauth_flow(self, client_config: Dict) -> str:
        """Configura el flujo OAuth y retorna la URL de autorización"""
        try:
            # Para aplicaciones de escritorio, Google usa automáticamente el redirect_uri
            # correcto basándose en el tipo de credenciales. No necesitamos especificarlo.
            flow = Flow.from_client_config(
                client_config,
                scopes=self.SCOPES
            )

            # Configurar redirect_uri manualmente solo si no está en client_config
            if 'installed' in client_config and 'redirect_uris' in client_config['installed']:
                # Usar el primer redirect_uri de las credenciales
                flow.redirect_uri = client_config['installed']['redirect_uris'][0]
            else:
                # Fallback: usar out-of-band para que Google muestre el código
                flow.redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'

            auth_url, _ = flow.authorization_url(
                access_type='offline',
                include_granted_scopes='true'
            )

            # Guardar el client_config ORIGINAL y el redirect_uri para reconstruir después
            self._save_flow_state(client_config, flow.redirect_uri)

            return auth_url

        except Exception as e:
            self.logger.error(f"Error configurando OAuth: {e}")
            raise
    
    def _save_flow_state(self, client_config: Dict, redirect_uri: str):
        """Guarda el estado del flow OAuth"""
        flow_data = {
            'client_config': client_config,  # Guardar el client_config ORIGINAL
            'redirect_uri': redirect_uri,
            'scopes': self.SCOPES
        }

        with open("data/oauth_flow.json", 'w') as f:
            json.dump(flow_data, f, indent=2)
    
    def complete_oauth_flow(self, authorization_code: str) -> bool:
        """Completa el flujo OAuth con el código de autorización"""
        try:
            # Cargar el flow guardado
            if not os.path.exists("data/oauth_flow.json"):
                self.logger.error("No se encontró el archivo de flow guardado")
                return False

            with open("data/oauth_flow.json", 'r') as f:
                flow_data = json.load(f)

            # Validar que tenemos el client_config
            client_config = flow_data.get('client_config')
            if not client_config:
                self.logger.error("client_config no encontrado en flow_data")
                return False

            # Validar que sea una aplicación de escritorio (installed) o web
            if 'installed' not in client_config and 'web' not in client_config:
                self.logger.error(f"Tipo de credencial no válido. Estructura: {list(client_config.keys())}")
                return False

            # Recrear el flow con el client_config original
            flow = Flow.from_client_config(
                client_config,
                scopes=flow_data['scopes']
            )

            # Establecer el redirect_uri
            flow.redirect_uri = flow_data['redirect_uri']

            self.logger.info(f"Intercambiando código por token con redirect_uri: {flow.redirect_uri}")

            # Intercambiar código por token
            flow.fetch_token(code=authorization_code)

            # Guardar credenciales
            self.credentials = flow.credentials
            self._save_credentials()

            # Inicializar servicio
            self._initialize_service()

            self.logger.info("✅ OAuth completado exitosamente")
            return True

        except FileNotFoundError as e:
            self.logger.error(f"Archivo no encontrado: {e}")
            return False
        except json.JSONDecodeError as e:
            self.logger.error(f"Error decodificando JSON: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Error completando OAuth: {e}")
            import traceback
            self.logger.error(traceback.format_exc())
            return False
    
    def _save_credentials(self):
        """Guarda las credenciales OAuth"""
        creds_data = {
            'token': self.credentials.token,
            'refresh_token': self.credentials.refresh_token,
            'token_uri': self.credentials.token_uri,
            'client_id': self.credentials.client_id,
            'client_secret': self.credentials.client_secret,
            'scopes': self.credentials.scopes
        }
        
        with open(self.token_file, 'w') as f:
            json.dump(creds_data, f)
    
    def _load_credentials(self) -> bool:
        """Carga las credenciales guardadas"""
        try:
            if not os.path.exists(self.token_file):
                self.logger.info("No se encontró archivo de credenciales")
                return False

            with open(self.token_file, 'r') as f:
                creds_data = json.load(f)

            self.credentials = Credentials(
                token=creds_data['token'],
                refresh_token=creds_data['refresh_token'],
                token_uri=creds_data['token_uri'],
                client_id=creds_data['client_id'],
                client_secret=creds_data['client_secret'],
                scopes=creds_data['scopes']
            )

            # Refrescar token si es necesario
            if self.credentials.expired:
                self.logger.info("Token expirado, refrescando...")
                try:
                    self.credentials.refresh(Request())
                    self._save_credentials()
                    self.logger.info("Token refrescado exitosamente")
                except Exception as refresh_error:
                    self.logger.error(f"Error refrescando token: {refresh_error}")
                    # Token inválido, eliminar archivo
                    if os.path.exists(self.token_file):
                        os.remove(self.token_file)
                    return False

            return True

        except KeyError as e:
            self.logger.error(f"Datos de credenciales incompletos: {e}")
            return False
        except json.JSONDecodeError:
            self.logger.error("Archivo de credenciales corrupto")
            return False
        except Exception as e:
            self.logger.error(f"Error cargando credenciales: {e}")
            return False
    
    def _initialize_service(self) -> bool:
        """Inicializa el servicio de Search Console"""
        try:
            if not self.credentials:
                self.logger.error("No hay credenciales disponibles")
                return False

            self.service = build('searchconsole', 'v1', credentials=self.credentials)
            self.logger.info("Servicio de Search Console inicializado")
            return True
        except Exception as e:
            self.logger.error(f"Error inicializando servicio: {e}")
            self.service = None
            return False
    
    def is_authenticated(self) -> bool:
        """Verifica si está autenticado"""
        if not self._load_credentials():
            return False
        
        return self._initialize_service()
    
    def get_sites(self) -> List[Dict]:
        """Obtiene la lista de sitios web verificados"""
        try:
            if not self.service:
                if not self.is_authenticated():
                    self.logger.error("No autenticado con Search Console")
                    raise Exception("No autenticado con Search Console")

            self.logger.info("Obteniendo lista de sitios...")
            sites = self.service.sites().list().execute()
            site_list = sites.get('siteEntry', [])
            self.logger.info(f"Obtenidos {len(site_list)} sitios")
            return site_list

        except HttpError as e:
            self.logger.error(f"Error HTTP obteniendo sitios: {e}")
            if e.resp.status == 403:
                self.logger.error("Acceso denegado - verifica permisos de API")
            return []
        except Exception as e:
            self.logger.error(f"Error obteniendo sitios: {e}")
            return []
    
    def get_search_analytics(self, site_url: str, start_date: str, end_date: str,
                           dimensions: List[str] = None, filters: List[Dict] = None,
                           row_limit: int = 1000) -> Dict:
        """Obtiene datos de Search Analytics"""
        try:
            if not self.service:
                if not self.is_authenticated():
                    self.logger.error("No autenticado con Search Console")
                    raise Exception("No autenticado con Search Console")

            if dimensions is None:
                dimensions = ['query', 'page', 'device']

            request_body = {
                'startDate': start_date,
                'endDate': end_date,
                'dimensions': dimensions,
                'rowLimit': row_limit,
                'startRow': 0
            }

            if filters:
                request_body['dimensionFilterGroups'] = [{
                    'filters': filters
                }]

            self.logger.info(f"Obteniendo analytics para {site_url} ({start_date} a {end_date})")
            response = self.service.searchanalytics().query(
                siteUrl=site_url,
                body=request_body
            ).execute()

            rows_count = len(response.get('rows', []))
            self.logger.info(f"Obtenidos {rows_count} registros de analytics")
            return response

        except HttpError as e:
            self.logger.error(f"Error HTTP obteniendo analytics: {e}")
            if e.resp.status == 403:
                self.logger.error("Acceso denegado - verifica que el sitio esté verificado en Search Console")
            elif e.resp.status == 400:
                self.logger.error("Solicitud inválida - verifica las fechas y parámetros")
            return {}
        except Exception as e:
            self.logger.error(f"Error obteniendo analytics: {e}")
            return {}
    
    def get_top_queries(self, site_url: str, days: int = 30, limit: int = 100) -> List[Dict]:
        """Obtiene las consultas principales"""
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)
        
        data = self.get_search_analytics(
            site_url=site_url,
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat(),
            dimensions=['query'],
            row_limit=limit
        )
        
        return data.get('rows', [])
    
    def get_top_pages(self, site_url: str, days: int = 30, limit: int = 100) -> List[Dict]:
        """Obtiene las páginas principales"""
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)
        
        data = self.get_search_analytics(
            site_url=site_url,
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat(),
            dimensions=['page'],
            row_limit=limit
        )
        
        return data.get('rows', [])
    
    def get_query_performance(self, site_url: str, query: str, days: int = 30) -> Dict:
        """Obtiene el rendimiento de una consulta específica"""
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)
        
        filters = [{
            'dimension': 'query',
            'operator': 'equals',
            'expression': query
        }]
        
        data = self.get_search_analytics(
            site_url=site_url,
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat(),
            dimensions=['query', 'page', 'device'],
            filters=filters
        )
        
        return data
    
    def get_site_performance_summary(self, site_url: str, days: int = 30) -> Dict:
        """Obtiene un resumen del rendimiento del sitio"""
        try:
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=days)
            
            # Obtener datos generales
            general_data = self.get_search_analytics(
                site_url=site_url,
                start_date=start_date.isoformat(),
                end_date=end_date.isoformat(),
                dimensions=[],
                row_limit=1
            )
            
            # Obtener top queries
            top_queries = self.get_top_queries(site_url, days, 50)
            
            # Obtener top pages
            top_pages = self.get_top_pages(site_url, days, 50)
            
            # Calcular métricas
            total_clicks = 0
            total_impressions = 0
            total_ctr = 0
            avg_position = 0
            
            if general_data.get('rows'):
                row = general_data['rows'][0]
                total_clicks = row.get('clicks', 0)
                total_impressions = row.get('impressions', 0)
                total_ctr = row.get('ctr', 0) * 100
                avg_position = row.get('position', 0)
            
            return {
                'site_url': site_url,
                'period': f"{start_date} to {end_date}",
                'summary': {
                    'total_clicks': total_clicks,
                    'total_impressions': total_impressions,
                    'average_ctr': round(total_ctr, 2),
                    'average_position': round(avg_position, 1)
                },
                'top_queries': top_queries[:20],
                'top_pages': top_pages[:20],
                'last_updated': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error obteniendo resumen: {e}")
            return {}
    
    def validate_site_access(self, site_url: str) -> bool:
        """Valida que se tenga acceso a un sitio"""
        try:
            sites = self.get_sites()
            site_urls = [site.get('siteUrl', '') for site in sites]
            
            # Verificar URL exacta o con variaciones comunes
            variations = [
                site_url,
                site_url.rstrip('/'),
                f"https://{site_url}",
                f"https://{site_url}/",
                f"http://{site_url}",
                f"http://{site_url}/"
            ]
            
            for variation in variations:
                if variation in site_urls:
                    return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error validando acceso al sitio: {e}")
            return False