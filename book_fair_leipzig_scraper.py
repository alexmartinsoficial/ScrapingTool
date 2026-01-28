"""
Leipzig Book Fair 2026 - Scraper Completo de Expositores
Extrai: Nome, País, Responsável, Email, Telefone, Website
Total: 1.397 expositores
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
from datetime import datetime
import re

class LeipzigBookFairScraper:
    
    def __init__(self):
        self.base_url = "https://www.leipziger-buchmesse.de/en/visit/exhibitors-directory/"
        self.exhibitors_data = []
        self.driver = None
        
    def setup_driver(self):
        """Configurar Chrome"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        
    def get_all_exhibitor_urls(self):
        """Passo 1: Obter URLs de todos os expositores"""
        print("🔍 Buscando lista de expositores...")
        
        # Aumentar limite para pegar todos
        url = f"{self.base_url}?limitSearchResults=1500&fair=buchmesse&catalog=EXHIBITOR"
        self.driver.get(url)
        
        # Aguardar carregamento
        time.sleep(5)
        
        # Scroll progressivo para carregar todos
        for i in range(20):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            
        # Extrair todos os links
        exhibitor_links = []
        cards = self.driver.find_elements(By.CSS_SELECTOR, "a[href*='/exhibitors-products/exhibitor/']")
        
        for card in cards:
            url = card.get_attribute("href")
            if url and url not in exhibitor_links:
                exhibitor_links.append(url)
                
        print(f"✅ Encontrados {len(exhibitor_links)} expositores")
        return exhibitor_links
        
    def extract_contact_info(self, url):
        """Passo 2: Extrair dados de contato de cada expositor"""
        try:
            self.driver.get(url)
            time.sleep(2)
            
            data = {
                'url': url,
                'name': '',
                'country': '',
                'contact_person': '',
                'email': '',
                'phone': '',
                'website': '',
                'address': '',
                'hall_stand': ''
            }
            
            # Nome do expositor
            try:
                data['name'] = self.driver.find_element(By.TAG_NAME, "h1").text.strip()
            except:
                pass
                
            # Buscar todas as informações visíveis
            try:
                page_text = self.driver.find_element(By.TAG_NAME, "body").text
                
                # Email (regex)
                emails = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', page_text)
                data['email'] = emails[0] if emails else ''
                
                # Telefone (regex)
                phones = re.findall(r'[\+]?[(]?[0-9]{1,4}[)]?[-\s\.]?[(]?[0-9]{1,4}[)]?[-\s\.]?[0-9]{1,9}', page_text)
                data['phone'] = phones[0] if phones else ''
                
                # Website
                websites = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', page_text)
                data['website'] = websites[0] if websites else ''
                
            except:
                pass
            
            # Buscar campos específicos
            try:
                # País
                country_elem = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Country')]")
                if country_elem:
                    data['country'] = country_elem[0].find_element(By.XPATH, "following-sibling::*").text
            except:
                pass
                
            try:
                # Hall/Stand
                hall_elem = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Hall') or contains(text(), 'Stand')]")
                if hall_elem:
                    data['hall_stand'] = hall_elem[0].text
            except:
                pass
                
            try:
                # Pessoa de contato
                contact_elem = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Contact') or contains(text(), 'Representative')]")
                if contact_elem:
                    data['contact_person'] = contact_elem[0].text
            except:
                pass
            
            return data
            
        except Exception as e:
            print(f"❌ Erro em {url}: {e}")
            return None
            
    def scrape_all(self, max_exhibitors=None):
        """Executar scraping completo"""
        self.setup_driver()
        
        try:
            # 1. Obter todos os URLs
            exhibitor_urls = self.get_all_exhibitor_urls()
            
            if max_exhibitors:
                exhibitor_urls = exhibitor_urls[:max_exhibitors]
            
            # 2. Extrair dados de cada um
            total = len(exhibitor_urls)
            print(f"\n📊 Iniciando extração de {total} expositores...\n")
            
            for i, url in enumerate(exhibitor_urls, 1):
                print(f"[{i}/{total}] Processando: {url.split('/')[-1][:30]}...")
                
                data = self.extract_contact_info(url)
                if data:
                    self.exhibitors_data.append(data)
                
                # Progresso a cada 50
                if i % 50 == 0:
                    print(f"\n✅ {i} expositores processados\n")
                    
                # Pequena pausa para não sobrecarregar
                time.sleep(0.5)
                
            print(f"\n🎉 Scraping concluído! Total: {len(self.exhibitors_data)} expositores")
            
        finally:
            self.driver.quit()
            
    def save_to_excel(self, filename="Leipzig_Book_Fair_2026_Exhibitors.xlsx"):
        """Salvar em Excel"""
        df = pd.DataFrame(self.exhibitors_data)
        
        # Reordenar colunas
        columns_order = ['name', 'country', 'contact_person', 'email', 'phone', 
                        'website', 'address', 'hall_stand', 'url']
        df = df[columns_order]
        
        # Renomear colunas
        df.columns = ['Exhibitor Name', 'Country', 'Contact Person', 'Email', 
                      'Phone', 'Website', 'Address', 'Hall/Stand', 'Profile URL']
        
        # Salvar
        df.to_excel(filename, index=False, engine='openpyxl')
        print(f"\n💾 Arquivo salvo: {filename}")
        
        return df


# EXECUÇÃO
if __name__ == "__main__":
    scraper = LeipzigBookFairScraper()
    
    # TESTE: primeiros 20 expositores
    print("🧪 MODO TESTE - Extraindo 20 expositores...\n")
    scraper.scrape_all(max_exhibitors=20)
    
    # Para rodar TODOS (1397), comentar linha acima e descomentar abaixo:
    # scraper.scrape_all()
    
    # Salvar resultado
    df = scraper.save_to_excel()
    
    # Preview
    print("\n📋 Preview dos dados:")
    print(df.head(10))
    print(f"\nTotal de linhas: {len(df)}")
    print(f"Emails encontrados: {df['Email'].notna().sum()}")
    print(f"Telefones encontrados: {df['Phone'].notna().sum()}")
