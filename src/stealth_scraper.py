import random
import time
import json
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import undetected_chromedriver as uc
from fake_useragent import UserAgent
import requests
from urllib.parse import quote_plus, urlparse
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import os

class StealthSerpScraper:
    def __init__(self, config):
        self.config = config
        self.session = requests.Session()
        self.ua = UserAgent()
        self.proxies = self.load_proxy_list()
        self.current_proxy_index = 0
        self.results = []
        
        # Configurar logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/scraper.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def load_proxy_list(self):
        """Carga lista de proxies desde configuración"""
        proxies = []
        if self.config.get('PROXIES'):
            for proxy_string in self.config['PROXIES']:
                if proxy_string.strip():
                    proxies.append({
                        'http': f'http://{proxy_string}',
                        'https': f'https://{proxy_string}'
                    })
        return proxies
    
    def get_random_headers(self):
        """Headers realistas y rotativos"""
        accept_languages = [
            'en-US,en;q=0.9',
            'es-ES,es;q=0.9,en;q=0.8',
            'en-GB,en;q=0.9',
            'fr-FR,fr;q=0.9,en;q=0.8'
        ]
        
        headers = {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': random.choice(accept_languages),
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': random.choice(['max-age=0', 'no-cache', 'must-revalidate']),
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Pragma': 'no-cache'
        }
        return headers
    
    def setup_stealth_driver(self):
        """Configura Chrome con máxima anti-detección"""
        options = uc.ChromeOptions()
        
        # Flags anti-detección esenciales
        stealth_flags = [
            '--disable-blink-features=AutomationControlled',
            '--disable-extensions',
            '--no-sandbox',
            '--disable-dev-shm-usage',
            '--disable-gpu',
            '--disable-web-security',
            '--disable-features=VizDisplayCompositor',
            '--disable-background-timer-throttling',
            '--disable-backgrounding-occluded-windows',
            '--disable-renderer-backgrounding',
            '--disable-field-trial-config',
            '--disable-back-forward-cache',
            '--disable-background-networking',
            '--disable-sync',
            '--disable-translate',
            '--disable-ipc-flooding-protection',
            '--disable-hang-monitor',
            '--disable-client-side-phishing-detection',
            '--disable-component-update',
            '--disable-default-apps',
            '--disable-domain-reliability',
            '--disable-features=TranslateUI',
            '--hide-scrollbars',
            '--mute-audio'
        ]
        
        for flag in stealth_flags:
            options.add_argument(flag)
        
        # Randomizar window size
        resolutions = [
            (1366, 768), (1920, 1080), (1440, 900), (1280, 720),
            (1536, 864), (1600, 900), (1024, 768)
        ]
        width, height = random.choice(resolutions)
        options.add_argument(f'--window-size={width},{height}')
        
        # User agent rotativo
        options.add_argument(f'--user-agent={self.ua.random}')
        
        # Proxy rotation
        if self.proxies:
            proxy = self.proxies[self.current_proxy_index % len(self.proxies)]
            proxy_url = proxy['http'].replace('http://', '')
            options.add_argument(f'--proxy-server={proxy_url}')
            self.current_proxy_index += 1
            self.logger.info(f"Using proxy: {proxy_url}")
        
        # Configuraciones adicionales de privacidad
        prefs = {
            "profile.default_content_setting_values": {
                "notifications": 2,
                "media_stream": 2,
                "geolocation": 2
            },
            "profile.managed_default_content_settings": {
                "images": 2
            }
        }
        options.add_experimental_option("prefs", prefs)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        try:
            # Crear driver con undetected-chromedriver
            driver = uc.Chrome(options=options, version_main=None)
            
            # Scripts adicionales anti-detección
            stealth_scripts = """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                });
                
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5],
                });
                
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['en-US', 'en'],
                });
                
                window.chrome = {
                    runtime: {},
                };
                
                Object.defineProperty(navigator, 'permissions', {
                    get: () => ({
                        query: () => Promise.resolve({ state: 'granted' }),
                    }),
                });
                
                delete navigator.__proto__.webdriver;
            """
            
            driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                'source': stealth_scripts
            })
            
            return driver
            
        except Exception as e:
            self.logger.error(f"Error setting up driver: {e}")
            return None
    
    def human_delay(self, min_delay=2, max_delay=8):
        """Delays humanizados con variación"""
        base_delay = random.uniform(min_delay, max_delay)
        # Añadir micro-pausas aleatorias para simular comportamiento humano
        micro_pause = random.uniform(0.1, 0.5)
        total_delay = base_delay + micro_pause
        
        time.sleep(total_delay)
    
    def simulate_human_behavior(self, driver):
        """Simula comportamiento humano real"""
        try:
            # Scroll aleatorio
            scroll_positions = [
                random.randint(100, 300),
                random.randint(400, 600),
                random.randint(200, 400)
            ]
            
            for position in scroll_positions:
                driver.execute_script(f"window.scrollTo(0, {position});")
                time.sleep(random.uniform(0.5, 1.5))
            
            # Movimiento de mouse aleatorio
            actions = ActionChains(driver)
            body = driver.find_element(By.TAG_NAME, "body")
            
            # Varios movimientos de mouse
            for _ in range(random.randint(2, 4)):
                x_offset = random.randint(50, 500)
                y_offset = random.randint(50, 400)
                actions.move_to_element_with_offset(body, x_offset, y_offset)
                actions.pause(random.uniform(0.3, 0.8))
            
            actions.perform()
            
            # Scroll de vuelta arriba
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(random.uniform(0.5, 1.0))
            
        except Exception as e:
            self.logger.warning(f"Error in human behavior simulation: {e}")
    
    def google_suggest_scraper(self, keyword, country='US', language='en'):
        """Scraper de Google Suggest con anti-detección"""
        try:
            # Rotar entre diferentes endpoints
            endpoints = [
                "http://suggestqueries.google.com/complete/search",
                "https://clients1.google.com/complete/search"
            ]
            
            url = random.choice(endpoints)
            
            clients = ['firefox', 'chrome', 'safari', 'toolbar']
            
            params = {
                'client': random.choice(clients),
                'q': keyword,
                'hl': language,
                'gl': country,
                'callback': f'google.sbox.p{random.randint(50, 99)}'
            }
            
            headers = self.get_random_headers()
            
            # Proxy rotation
            proxy = None
            if self.proxies:
                proxy = self.proxies[self.current_proxy_index % len(self.proxies)]
                self.current_proxy_index += 1
            
            # Delay humanizado
            self.human_delay(1, 3)
            
            response = self.session.get(
                url, 
                params=params, 
                headers=headers, 
                proxies=proxy, 
                timeout=10,
                verify=False
            )
            
            if response.status_code == 200:
                content = response.text
                # Procesar respuesta JSONP
                start = content.find('(') + 1
                end = content.rfind(')')
                
                if start > 0 and end > start:
                    json_str = content[start:end]
                    try:
                        data = json.loads(json_str)
                        suggestions = []
                        
                        if len(data) > 1 and isinstance(data[1], list):
                            suggestions = [
                                item[0] if isinstance(item, list) else str(item) 
                                for item in data[1]
                            ]
                        
                        self.logger.info(f"Found {len(suggestions)} suggestions for '{keyword}'")
                        return suggestions
                    except json.JSONDecodeError:
                        self.logger.error(f"JSON decode error for keyword: {keyword}")
                        return []
                else:
                    self.logger.error(f"Invalid response format for keyword: {keyword}")
                    return []
            else:
                self.logger.error(f"HTTP {response.status_code} for keyword: {keyword}")
                return []
                
        except Exception as e:
            self.logger.error(f"Error scraping suggestions for '{keyword}': {e}")
            return []
    
    def serp_scraper_selenium(self, keyword, target_domain=None, pages=1):
        """SERP scraper con Selenium y detección de posiciones"""
        driver = None
        results = []
        
        try:
            driver = self.setup_stealth_driver()
            if not driver:
                return results
            
            self.logger.info(f"Scraping SERP for keyword: '{keyword}'")
            
            for page in range(pages):
                start = page * 10
                search_url = f"https://www.google.com/search?q={quote_plus(keyword)}&start={start}&num=10"
                
                # Delay antes de navegar
                self.human_delay(3, 6)
                
                try:
                    driver.get(search_url)
                    
                    # Verificar si hay CAPTCHA
                    if "captcha" in driver.current_url.lower() or "sorry" in driver.page_source.lower():
                        self.logger.warning("CAPTCHA detected, waiting...")
                        time.sleep(30)
                        continue
                    
                    # Simular comportamiento humano
                    self.simulate_human_behavior(driver)
                    
                    # Esperar a que carguen los resultados
                    WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "h3, .g"))
                    )
                    
                    # Extraer resultados
                    search_containers = driver.find_elements(By.CSS_SELECTOR, "div.g")
                    
                    for i, container in enumerate(search_containers):
                        try:
                            # Buscar título y enlace
                            title_elem = container.find_element(By.CSS_SELECTOR, "h3")
                            link_elem = container.find_element(By.CSS_SELECTOR, "a")
                            
                            title = title_elem.text.strip()
                            url = link_elem.get_attribute("href")
                            
                            if title and url and url.startswith('http'):
                                position = (page * 10) + i + 1
                                domain = urlparse(url).netloc.lower()
                                
                                result = {
                                    'keyword': keyword,
                                    'position': position,
                                    'title': title,
                                    'url': url,
                                    'domain': domain,
                                    'page': page + 1
                                }
                                
                                results.append(result)
                                
                                # Si buscamos un dominio específico y lo encontramos
                                if target_domain and target_domain.lower() in domain:
                                    self.logger.info(f"Found {target_domain} at position {position} for '{keyword}'")
                                
                        except Exception as e:
                            continue
                    
                    self.logger.info(f"Page {page + 1}: Found {len(search_containers)} results")
                    
                    # Delay entre páginas
                    if page < pages - 1:
                        self.human_delay(5, 10)
                        
                except Exception as e:
                    self.logger.error(f"Error scraping page {page + 1}: {e}")
                    continue
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error in SERP scraping: {e}")
            return []
        finally:
            if driver:
                try:
                    driver.quit()
                except:
                    pass
    
    def batch_position_check(self, keywords, target_domain, pages=1):
        """Verifica posiciones para múltiples keywords"""
        all_results = []
        
        self.logger.info(f"Starting batch position check for {len(keywords)} keywords")
        
        for i, keyword in enumerate(tqdm(keywords, desc="Checking positions")):
            self.logger.info(f"Processing keyword {i+1}/{len(keywords)}: '{keyword}'")
            
            results = self.serp_scraper_selenium(keyword, target_domain, pages)
            all_results.extend(results)
            
            # Delay entre keywords para evitar detección
            if i < len(keywords) - 1:
                delay = random.uniform(
                    self.config.get('MIN_KEYWORD_DELAY', 5),
                    self.config.get('MAX_KEYWORD_DELAY', 15)
                )
                self.logger.info(f"Waiting {delay:.1f}s before next keyword...")
                time.sleep(delay)
        
        return all_results
    
    def save_results(self, results, filename=None):
        """Guarda resultados en CSV y JSON"""
        if not results:
            self.logger.warning("No results to save")
            return
        
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        
        if not filename:
            filename = f"keyword_positions_{timestamp}"
        
        # Guardar como CSV
        df = pd.DataFrame(results)
        csv_path = f"data/{filename}.csv"
        df.to_csv(csv_path, index=False, encoding='utf-8')
        
        # Guardar como JSON
        json_path = f"data/{filename}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Results saved to {csv_path} and {json_path}")
        
        # Estadísticas
        total_keywords = len(set([r['keyword'] for r in results]))
        self.logger.info(f"Total keywords processed: {total_keywords}")
        self.logger.info(f"Total positions found: {len(results)}")