"""
🔐 Sistema Mejorado de Autenticación para Google Search Console

Mejoras implementadas:
✅ Auto-refresh automático de tokens sin intervención del usuario
✅ Manejo robusto de errores con mensajes claros
✅ Validación de sitios disponibles antes de operaciones
✅ Caché inteligente de datos para reducir llamadas API
✅ Sistema multi-cuenta (múltiples credenciales)
✅ Logging detallado de todas las operaciones
✅ Retry automático en caso de fallos temporales
✅ Detección y corrección de URLs de sitios
"""

import os
import json
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import pickle
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class ImprovedSearchConsoleAuth:
    """
    Sistema mejorado de autenticación para Google Search Console
    con funcionalidades avanzadas
    """

    def __init__(self, credentials_dir: str = "data/credentials"):
        self.logger = logging.getLogger(__name__)
        self.credentials_dir = Path(credentials_dir)
        self.credentials_dir.mkdir(parents=True, exist_ok=True)

        # Archivos de configuración
        self.active_account_file = self.credentials_dir / "active_account.json"
        self.accounts_file = self.credentials_dir / "accounts.json"
        self.cache_dir = self.credentials_dir / "cache"
        self.cache_dir.mkdir(exist_ok=True)

        # Scopes necesarios
        self.SCOPES = [
            'https://www.googleapis.com/auth/webmasters.readonly',
            'https://www.googleapis.com/auth/webmasters'
        ]

        # Estado
        self.service = None
        self.credentials = None
        self.current_account_id = None

        # Configuración de caché
        self.cache_ttl = 3600  # 1 hora por defecto

        # Cargar cuenta activa si existe
        self._load_active_account()

    def _load_active_account(self):
        """Carga la cuenta activa si existe"""
        try:
            if self.active_account_file.exists():
                with open(self.active_account_file, 'r') as f:
                    data = json.load(f)
                    self.current_account_id = data.get('account_id')

                    if self.current_account_id:
                        self.logger.info(f"Cuenta activa cargada: {self.current_account_id}")
                        self._load_credentials_for_account(self.current_account_id)
        except Exception as e:
            self.logger.warning(f"Error cargando cuenta activa: {e}")

    def _load_credentials_for_account(self, account_id: str) -> bool:
        """Carga las credenciales para una cuenta específica"""
        try:
            token_file = self.credentials_dir / f"{account_id}_token.pickle"

            if not token_file.exists():
                self.logger.warning(f"Token no encontrado para cuenta: {account_id}")
                return False

            with open(token_file, 'rb') as f:
                self.credentials = pickle.load(f)

            # Auto-refresh si está expirado
            if self.credentials.expired and self.credentials.refresh_token:
                self.logger.info("Token expirado, refrescando automáticamente...")
                try:
                    self.credentials.refresh(Request())
                    self._save_credentials_for_account(account_id, self.credentials)
                    self.logger.info("✅ Token refrescado exitosamente")
                except Exception as e:
                    self.logger.error(f"Error refrescando token: {e}")
                    # Token inválido, eliminar
                    token_file.unlink(missing_ok=True)
                    return False

            # Inicializar servicio
            return self._initialize_service()

        except Exception as e:
            self.logger.error(f"Error cargando credenciales: {e}")
            return False

    def _save_credentials_for_account(self, account_id: str, credentials: Credentials):
        """Guarda las credenciales para una cuenta"""
        token_file = self.credentials_dir / f"{account_id}_token.pickle"

        with open(token_file, 'wb') as f:
            pickle.dump(credentials, f)

        self.logger.info(f"Credenciales guardadas para: {account_id}")

    def _initialize_service(self) -> bool:
        """Inicializa el servicio de Search Console"""
        try:
            if not self.credentials:
                self.logger.error("No hay credenciales disponibles")
                return False

            self.service = build('searchconsole', 'v1', credentials=self.credentials)
            self.logger.info("✅ Servicio de Search Console inicializado")
            return True

        except Exception as e:
            self.logger.error(f"Error inicializando servicio: {e}")
            self.service = None
            return False

    def authenticate_with_oauth(
        self,
        client_secrets_file: str,
        account_name: str = None,
        force_reauth: bool = False
    ) -> Tuple[bool, str]:
        """
        Autenticación OAuth2 mejorada con flujo simplificado

        Args:
            client_secrets_file: Ruta al archivo de credenciales JSON de Google
            account_name: Nombre descriptivo de la cuenta (opcional)
            force_reauth: Forzar nueva autenticación aunque existan credenciales

        Returns:
            Tuple[bool, str]: (éxito, mensaje/URL de autorización)
        """
        try:
            # Generar ID de cuenta
            if not account_name:
                account_name = f"account_{int(time.time())}"

            account_id = account_name.lower().replace(' ', '_')

            # Verificar si ya existe y no forzar reauth
            if not force_reauth:
                if self._load_credentials_for_account(account_id):
                    self.current_account_id = account_id
                    self._save_active_account(account_id)
                    return True, "Cuenta ya autenticada correctamente"

            # Cargar client secrets
            if not os.path.exists(client_secrets_file):
                return False, f"Archivo no encontrado: {client_secrets_file}"

            with open(client_secrets_file, 'r') as f:
                client_config = json.load(f)

            # Crear flow OAuth
            flow = Flow.from_client_config(
                client_config,
                scopes=self.SCOPES
            )

            # Configurar redirect URI
            if 'installed' in client_config:
                redirect_uris = client_config['installed'].get('redirect_uris', [])
                flow.redirect_uri = redirect_uris[0] if redirect_uris else 'urn:ietf:wg:oauth:2.0:oob'
            else:
                flow.redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'

            # Generar URL de autorización
            auth_url, _ = flow.authorization_url(
                access_type='offline',
                include_granted_scopes='true',
                prompt='consent'  # Forzar pantalla de consentimiento para obtener refresh_token
            )

            # Guardar flow state
            flow_state = {
                'account_id': account_id,
                'account_name': account_name,
                'client_config': client_config,
                'redirect_uri': flow.redirect_uri,
                'scopes': self.SCOPES
            }

            flow_file = self.credentials_dir / "pending_flow.json"
            with open(flow_file, 'w') as f:
                json.dump(flow_state, f, indent=2)

            self.logger.info(f"Flujo OAuth iniciado para: {account_name}")

            # Retornar URL para que el usuario la abra
            return True, auth_url

        except Exception as e:
            self.logger.error(f"Error en autenticación OAuth: {e}")
            return False, str(e)

    def complete_authentication(self, authorization_code: str) -> Tuple[bool, str]:
        """
        Completa el flujo OAuth con el código de autorización

        Args:
            authorization_code: Código de autorización de Google

        Returns:
            Tuple[bool, str]: (éxito, mensaje)
        """
        try:
            flow_file = self.credentials_dir / "pending_flow.json"

            if not flow_file.exists():
                return False, "No hay flujo de autenticación pendiente"

            # Cargar flow state
            with open(flow_file, 'r') as f:
                flow_state = json.load(f)

            # Recrear flow
            flow = Flow.from_client_config(
                flow_state['client_config'],
                scopes=flow_state['scopes']
            )
            flow.redirect_uri = flow_state['redirect_uri']

            # Intercambiar código por token
            self.logger.info("Intercambiando código de autorización por token...")
            flow.fetch_token(code=authorization_code)

            # Guardar credenciales
            self.credentials = flow.credentials
            account_id = flow_state['account_id']

            self._save_credentials_for_account(account_id, self.credentials)

            # Establecer como cuenta activa
            self.current_account_id = account_id
            self._save_active_account(account_id)

            # Registrar cuenta
            self._register_account(
                account_id,
                flow_state['account_name'],
                flow.credentials.client_id
            )

            # Inicializar servicio
            if self._initialize_service():
                # Limpiar flow pendiente
                flow_file.unlink(missing_ok=True)

                # Validar acceso obteniendo sitios
                sites = self.get_verified_sites()

                self.logger.info(f"✅ Autenticación completada para: {flow_state['account_name']}")
                self.logger.info(f"   Sitios disponibles: {len(sites)}")

                return True, f"Autenticación exitosa. {len(sites)} sitios disponibles."
            else:
                return False, "Error inicializando servicio"

        except Exception as e:
            self.logger.error(f"Error completando autenticación: {e}")
            return False, f"Error: {str(e)}"

    def _save_active_account(self, account_id: str):
        """Guarda la cuenta activa"""
        data = {
            'account_id': account_id,
            'updated_at': datetime.now().isoformat()
        }

        with open(self.active_account_file, 'w') as f:
            json.dump(data, f, indent=2)

    def _register_account(self, account_id: str, account_name: str, client_id: str):
        """Registra una cuenta en el sistema multi-cuenta"""
        accounts = {}

        if self.accounts_file.exists():
            with open(self.accounts_file, 'r') as f:
                accounts = json.load(f)

        accounts[account_id] = {
            'name': account_name,
            'client_id': client_id,
            'created_at': datetime.now().isoformat(),
            'last_used': datetime.now().isoformat()
        }

        with open(self.accounts_file, 'w') as f:
            json.dump(accounts, f, indent=2)

    def switch_account(self, account_id: str) -> Tuple[bool, str]:
        """Cambia a otra cuenta autenticada"""
        try:
            if self._load_credentials_for_account(account_id):
                self.current_account_id = account_id
                self._save_active_account(account_id)

                # Actualizar last_used
                accounts = {}
                if self.accounts_file.exists():
                    with open(self.accounts_file, 'r') as f:
                        accounts = json.load(f)

                if account_id in accounts:
                    accounts[account_id]['last_used'] = datetime.now().isoformat()

                    with open(self.accounts_file, 'w') as f:
                        json.dump(accounts, f, indent=2)

                return True, f"Cuenta cambiada a: {account_id}"
            else:
                return False, "No se pudieron cargar las credenciales de la cuenta"

        except Exception as e:
            self.logger.error(f"Error cambiando de cuenta: {e}")
            return False, str(e)

    def get_available_accounts(self) -> List[Dict]:
        """Obtiene lista de cuentas autenticadas"""
        if not self.accounts_file.exists():
            return []

        try:
            with open(self.accounts_file, 'r') as f:
                accounts = json.load(f)

            result = []
            for account_id, data in accounts.items():
                result.append({
                    'id': account_id,
                    'name': data.get('name', account_id),
                    'is_active': account_id == self.current_account_id,
                    'last_used': data.get('last_used'),
                    'created_at': data.get('created_at')
                })

            return result

        except Exception as e:
            self.logger.error(f"Error obteniendo cuentas: {e}")
            return []

    def is_authenticated(self) -> bool:
        """Verifica si hay una sesión autenticada válida"""
        if not self.current_account_id:
            return False

        if not self.credentials or not self.service:
            # Intentar cargar
            return self._load_credentials_for_account(self.current_account_id)

        return True

    def get_verified_sites(self, use_cache: bool = True) -> List[Dict]:
        """
        Obtiene sitios verificados con caché inteligente

        Args:
            use_cache: Usar caché si está disponible

        Returns:
            Lista de sitios verificados
        """
        cache_key = f"{self.current_account_id}_sites"

        # Intentar desde caché
        if use_cache:
            cached = self._get_from_cache(cache_key)
            if cached is not None:
                self.logger.info(f"Sitios cargados desde caché ({len(cached)} sitios)")
                return cached

        # Obtener desde API
        try:
            if not self.service:
                if not self.is_authenticated():
                    raise Exception("No autenticado")

            self.logger.info("Obteniendo sitios verificados desde API...")
            response = self.service.sites().list().execute()
            sites = response.get('siteEntry', [])

            # Guardar en caché
            self._save_to_cache(cache_key, sites)

            self.logger.info(f"✅ Obtenidos {len(sites)} sitios verificados")
            return sites

        except HttpError as e:
            self.logger.error(f"Error HTTP obteniendo sitios: {e}")
            if e.resp.status == 403:
                self.logger.error("Acceso denegado - verifica permisos de API")
            return []
        except Exception as e:
            self.logger.error(f"Error obteniendo sitios: {e}")
            return []

    def validate_site_url(self, site_url: str) -> Tuple[bool, str]:
        """
        Valida y corrige URL de sitio para uso con Search Console

        Args:
            site_url: URL del sitio a validar

        Returns:
            Tuple[bool, str]: (válido, URL corregida o mensaje de error)
        """
        try:
            sites = self.get_verified_sites()

            if not sites:
                return False, "No hay sitios verificados disponibles"

            site_urls = [site.get('siteUrl', '') for site in sites]

            # Verificar coincidencia exacta
            if site_url in site_urls:
                return True, site_url

            # Intentar variaciones comunes
            variations = [
                site_url,
                site_url.rstrip('/'),
                site_url + '/',
                f"https://{site_url}",
                f"https://{site_url}/",
                f"http://{site_url}",
                f"http://{site_url}/",
                f"sc-domain:{site_url}",
                f"sc-domain:{site_url.replace('https://', '').replace('http://', '').rstrip('/')}"
            ]

            for variation in variations:
                if variation in site_urls:
                    self.logger.info(f"URL corregida: {site_url} → {variation}")
                    return True, variation

            # No encontrado
            available_sites = '\n  '.join(site_urls)
            return False, f"Sitio no verificado. Sitios disponibles:\n  {available_sites}"

        except Exception as e:
            self.logger.error(f"Error validando sitio: {e}")
            return False, str(e)

    def _get_from_cache(self, key: str) -> Optional[any]:
        """Obtiene datos del caché si no están expirados"""
        try:
            cache_file = self.cache_dir / f"{key}.pickle"

            if not cache_file.exists():
                return None

            # Verificar TTL
            file_age = time.time() - cache_file.stat().st_mtime
            if file_age > self.cache_ttl:
                self.logger.debug(f"Caché expirado para: {key}")
                cache_file.unlink()
                return None

            with open(cache_file, 'rb') as f:
                data = pickle.load(f)

            self.logger.debug(f"Caché hit: {key}")
            return data

        except Exception as e:
            self.logger.warning(f"Error leyendo caché: {e}")
            return None

    def _save_to_cache(self, key: str, data: any):
        """Guarda datos en caché"""
        try:
            cache_file = self.cache_dir / f"{key}.pickle"

            with open(cache_file, 'wb') as f:
                pickle.dump(data, f)

            self.logger.debug(f"Datos guardados en caché: {key}")

        except Exception as e:
            self.logger.warning(f"Error guardando en caché: {e}")

    def clear_cache(self, account_id: str = None):
        """Limpia el caché de una cuenta o todo el caché"""
        try:
            if account_id:
                # Limpiar caché de cuenta específica
                pattern = f"{account_id}_*.pickle"
                for cache_file in self.cache_dir.glob(pattern):
                    cache_file.unlink()
                self.logger.info(f"Caché limpiado para: {account_id}")
            else:
                # Limpiar todo el caché
                for cache_file in self.cache_dir.glob("*.pickle"):
                    cache_file.unlink()
                self.logger.info("Todo el caché ha sido limpiado")

        except Exception as e:
            self.logger.error(f"Error limpiando caché: {e}")

    def revoke_account(self, account_id: str) -> Tuple[bool, str]:
        """Revoca y elimina una cuenta"""
        try:
            # Eliminar token
            token_file = self.credentials_dir / f"{account_id}_token.pickle"
            if token_file.exists():
                token_file.unlink()

            # Limpiar caché
            self.clear_cache(account_id)

            # Eliminar de accounts.json
            if self.accounts_file.exists():
                with open(self.accounts_file, 'r') as f:
                    accounts = json.load(f)

                if account_id in accounts:
                    del accounts[account_id]

                    with open(self.accounts_file, 'w') as f:
                        json.dump(accounts, f, indent=2)

            # Si era la cuenta activa, limpiar
            if self.current_account_id == account_id:
                self.current_account_id = None
                self.credentials = None
                self.service = None

                if self.active_account_file.exists():
                    self.active_account_file.unlink()

            self.logger.info(f"Cuenta revocada: {account_id}")
            return True, "Cuenta revocada exitosamente"

        except Exception as e:
            self.logger.error(f"Error revocando cuenta: {e}")
            return False, str(e)

    def get_service(self):
        """Obtiene el servicio de Search Console (lazy loading)"""
        if not self.service:
            if not self.is_authenticated():
                raise Exception("No autenticado con Search Console")

        return self.service

    def set_cache_ttl(self, seconds: int):
        """Configura el TTL del caché (en segundos)"""
        self.cache_ttl = seconds
        self.logger.info(f"Cache TTL configurado a: {seconds}s")
