"""
🔄 Wrapper de Compatibilidad para Search Console API Mejorada

Este wrapper mantiene la interfaz existente mientras usa internamente
el sistema mejorado de autenticación
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from search_console_auth_improved import ImprovedSearchConsoleAuth
from googleapiclient.errors import HttpError


class SearchConsoleAPI:
    """
    Wrapper compatible con el API existente pero usando el sistema mejorado

    Uso:
        # Igual que antes
        sc_api = SearchConsoleAPI()

        # Autenticar (flujo mejorado)
        success, auth_url = sc_api.start_authentication('client_secrets.json', 'Mi Cuenta')
        # Usuario abre auth_url y obtiene código
        sc_api.complete_authentication(code)

        # Resto igual que antes
        sites = sc_api.get_sites()
        data = sc_api.get_search_analytics(...)
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._auth = ImprovedSearchConsoleAuth()

        # Mantener compatibilidad con código existente
        self.service = None
        self.credentials = None

    def start_authentication(
        self,
        client_secrets_file: str,
        account_name: str = None
    ) -> tuple:
        """
        Inicia el flujo de autenticación OAuth

        Returns:
            (success: bool, auth_url_or_message: str)
        """
        return self._auth.authenticate_with_oauth(client_secrets_file, account_name)

    def complete_authentication(self, authorization_code: str) -> bool:
        """Completa la autenticación con el código de autorización"""
        success, message = self._auth.complete_authentication(authorization_code)

        if success:
            self.service = self._auth.service
            self.credentials = self._auth.credentials

        return success

    def is_authenticated(self) -> bool:
        """Verifica si está autenticado"""
        is_auth = self._auth.is_authenticated()

        if is_auth:
            self.service = self._auth.service
            self.credentials = self._auth.credentials

        return is_auth

    def get_sites(self) -> List[Dict]:
        """Obtiene sitios verificados (con caché)"""
        return self._auth.get_verified_sites(use_cache=True)

    def validate_site_url(self, site_url: str) -> tuple:
        """Valida y corrige URL de sitio"""
        return self._auth.validate_site_url(site_url)

    def get_search_analytics(
        self,
        site_url: str,
        start_date: str,
        end_date: str,
        dimensions: List[str] = None,
        filters: List[Dict] = None,
        row_limit: int = 1000
    ) -> Dict:
        """
        Obtiene datos de Search Analytics (método original mantenido)
        """
        try:
            # Validar URL automáticamente
            is_valid, corrected_url = self._auth.validate_site_url(site_url)

            if not is_valid:
                self.logger.error(f"Sitio no válido: {site_url}")
                self.logger.error(corrected_url)  # Mensaje de error con sitios disponibles
                return {}

            # Usar URL corregida
            site_url = corrected_url

            service = self._auth.get_service()

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

            response = service.searchanalytics().query(
                siteUrl=site_url,
                body=request_body
            ).execute()

            rows_count = len(response.get('rows', []))
            self.logger.info(f"✅ Obtenidos {rows_count} registros")

            return response

        except HttpError as e:
            self.logger.error(f"Error HTTP obteniendo analytics: {e}")
            if e.resp.status == 403:
                self.logger.error("Acceso denegado - verifica permisos")
            elif e.resp.status == 400:
                self.logger.error("Solicitud inválida - verifica fechas y parámetros")
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
        """Obtiene resumen del rendimiento del sitio"""
        try:
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=days)

            # Datos generales
            general_data = self.get_search_analytics(
                site_url=site_url,
                start_date=start_date.isoformat(),
                end_date=end_date.isoformat(),
                dimensions=[],
                row_limit=1
            )

            # Top queries y pages
            top_queries = self.get_top_queries(site_url, days, 50)
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

    # ===== Métodos adicionales del sistema mejorado =====

    def get_available_accounts(self) -> List[Dict]:
        """Obtiene cuentas autenticadas disponibles"""
        return self._auth.get_available_accounts()

    def switch_account(self, account_id: str) -> tuple:
        """Cambia a otra cuenta"""
        success, message = self._auth.switch_account(account_id)

        if success:
            self.service = self._auth.service
            self.credentials = self._auth.credentials

        return success, message

    def revoke_current_account(self) -> tuple:
        """Revoca la cuenta activa actual"""
        if not self._auth.current_account_id:
            return False, "No hay cuenta activa"

        return self._auth.revoke_account(self._auth.current_account_id)

    def clear_cache(self):
        """Limpia el caché de datos"""
        self._auth.clear_cache()
        self.logger.info("Caché limpiado")

    def set_cache_ttl(self, seconds: int):
        """Configura el tiempo de vida del caché"""
        self._auth.set_cache_ttl(seconds)

    def get_current_account_info(self) -> Optional[Dict]:
        """Obtiene información de la cuenta activa"""
        if not self._auth.current_account_id:
            return None

        accounts = self._auth.get_available_accounts()

        for account in accounts:
            if account['is_active']:
                return account

        return None
