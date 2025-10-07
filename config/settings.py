import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

class Config:
    # Configuración de proxies
    PROXIES = []
    proxy_count = 1
    while True:
        proxy = os.getenv(f'PROXY_{proxy_count}')
        if proxy:
            PROXIES.append(proxy.strip())
            proxy_count += 1
        else:
            break
    
    # Configuración de delays
    MIN_KEYWORD_DELAY = int(os.getenv('MIN_KEYWORD_DELAY', 5))
    MAX_KEYWORD_DELAY = int(os.getenv('MAX_KEYWORD_DELAY', 15))
    MIN_PAGE_DELAY = int(os.getenv('MIN_PAGE_DELAY', 3))
    MAX_PAGE_DELAY = int(os.getenv('MAX_PAGE_DELAY', 8))
    
    # Configuración de Google
    DEFAULT_COUNTRY = os.getenv('DEFAULT_COUNTRY', 'US')
    DEFAULT_LANGUAGE = os.getenv('DEFAULT_LANGUAGE', 'en')
    PAGES_TO_SCRAPE = int(os.getenv('PAGES_TO_SCRAPE', 1))

    # Configuración de Google API
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', '')
    GOOGLE_SEARCH_ENGINE_ID = os.getenv('GOOGLE_SEARCH_ENGINE_ID', '')
    USE_GOOGLE_API = os.getenv('USE_GOOGLE_API', 'false').lower() == 'true'

    # Configuración de logs
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

    # Configuración de resultados
    SAVE_JSON = os.getenv('SAVE_JSON', 'true').lower() == 'true'
    SAVE_CSV = os.getenv('SAVE_CSV', 'true').lower() == 'true'
    
    # User agents personalizados
    CUSTOM_USER_AGENTS = []
    custom_ua = os.getenv('CUSTOM_USER_AGENTS', '')
    if custom_ua:
        CUSTOM_USER_AGENTS = [ua.strip() for ua in custom_ua.split('\n') if ua.strip()]
    
    @classmethod
    def to_dict(cls):
        """Convierte la configuración a diccionario"""
        return {
            'PROXIES': cls.PROXIES,
            'MIN_KEYWORD_DELAY': cls.MIN_KEYWORD_DELAY,
            'MAX_KEYWORD_DELAY': cls.MAX_KEYWORD_DELAY,
            'MIN_PAGE_DELAY': cls.MIN_PAGE_DELAY,
            'MAX_PAGE_DELAY': cls.MAX_PAGE_DELAY,
            'DEFAULT_COUNTRY': cls.DEFAULT_COUNTRY,
            'DEFAULT_LANGUAGE': cls.DEFAULT_LANGUAGE,
            'PAGES_TO_SCRAPE': cls.PAGES_TO_SCRAPE,
            'GOOGLE_API_KEY': cls.GOOGLE_API_KEY,
            'GOOGLE_SEARCH_ENGINE_ID': cls.GOOGLE_SEARCH_ENGINE_ID,
            'USE_GOOGLE_API': cls.USE_GOOGLE_API,
            'LOG_LEVEL': cls.LOG_LEVEL,
            'SAVE_JSON': cls.SAVE_JSON,
            'SAVE_CSV': cls.SAVE_CSV,
            'CUSTOM_USER_AGENTS': cls.CUSTOM_USER_AGENTS
        }
    
    @classmethod
    def print_config(cls):
        """Imprime la configuración actual"""
        print("🔧 Configuración actual:")
        print(f"   Proxies configurados: {len(cls.PROXIES)}")
        print(f"   Delay entre keywords: {cls.MIN_KEYWORD_DELAY}-{cls.MAX_KEYWORD_DELAY}s")
        print(f"   Páginas a scrapear: {cls.PAGES_TO_SCRAPE}")
        print(f"   País/Idioma: {cls.DEFAULT_COUNTRY}/{cls.DEFAULT_LANGUAGE}")
        print(f"   User agents custom: {len(cls.CUSTOM_USER_AGENTS)}")
        print(f"   Guardar CSV: {cls.SAVE_CSV}")
        print(f"   Guardar JSON: {cls.SAVE_JSON}")

# Crear instancia de configuración
config = Config.to_dict()
