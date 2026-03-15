"""
Ramayana Web Scraper - TEST VERSION (Bala Kanda Only)
FIXED: Now correctly fetches the actual content frame
"""

import requests
from bs4 import BeautifulSoup
import json
import time
from pathlib import Path
from typing import List, Dict, Optional
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

BASE_URL = "https://valmikiramayan.net/utf8"
OUTPUT_FILE = "ramayana_data_test.json"
REQUEST_DELAY = 1.5
TIMEOUT = 10

KANDAS = {
    'baala': {'name': 'Bala Kanda', 'sargas': 77, 'prefix': 'bala'},
}


class RamayanaaScraper:
    """Scraper for Ramayana verses from valmikiramayan.net"""
    
    def __init__(self, output_file: str = OUTPUT_FILE):
        self.output_file = output_file
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Educational purposes - Ramayana RAG Project)'
        })
        self.data = {
            'metadata': {
                'source': 'https://valmikiramayan.net/',
                'total_kandas': len(KANDAS),
                'kandas': []
            },
            'kandas': {}
        }
        self.verses_count = 0
    
    def fetch_page(self, url: str) -> Optional[str]:
        """Fetch a single page with error handling"""
        try:
            logger.info(f"Fetching: {url}")
            response = self.session.get(url, timeout=TIMEOUT)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            return None
    
    def extract_verses_from_html(self, html: str, kanda: str, sarga: int) -> List[Dict]:
        """Extract all verses from a single Sarga page"""
        verses = []
        soup = BeautifulSoup(html, 'html.parser')
        
        paragraphs = soup.find_all('p')
        current_verse = {}
        verse_num = 1
        
        for p in paragraphs:
            class_attr = p.get('class', [])
            if not class_attr:
                continue
            
            class_name = class_attr[0] if isinstance(class_attr, list) else class_attr
            text = p.get_text(strip=True)
            
            if not text:
                continue
            
            # Detect verse boundaries
            if 'verloc' in class_name:
                if current_verse:
                    verses.append(current_verse)
                current_verse = {
                    'verse_number': verse_num,
                    'kanda': kanda,
                    'sarga': sarga,
                    'sanskrit': '',
                    'translation': '',
                    'meanings': '',
                    'commentary': ''
                }
                verse_num += 1
            
            elif 'SanSloka' in class_name:
                if current_verse:
                    current_verse['sanskrit'] += text + ' '
            
            elif 'tat' in class_name:
                if current_verse:
                    current_verse['translation'] += text + ' '
            
            elif 'pratipada' in class_name:
                if current_verse:
                    current_verse['meanings'] += text + ' '
            
            elif 'comment' in class_name:
                if current_verse:
                    current_verse['commentary'] += text + ' '
        
        if current_verse and current_verse.get('sanskrit'):
            verses.append(current_verse)
        
        for verse in verses:
            for key in ['sanskrit', 'translation', 'meanings', 'commentary']:
                verse[key] = verse[key].strip()
        
        return verses
    
    def scrape_sarga(self, kanda_key: str, sarga_num: int) -> List[Dict]:
        """Scrape a single Sarga"""
        kanda_info = KANDAS[kanda_key]
        prefix = kanda_info['prefix']
        
        # FIXED: Fetch actual content frame, not frameset
        url = f"{BASE_URL}/{kanda_key}/sarga{sarga_num}/{prefix}sans{sarga_num}.htm"
        
        html = self.fetch_page(url)
        if not html:
            return []
        
        verses = self.extract_verses_from_html(html, kanda_key, sarga_num)
        self.verses_count += len(verses)
        
        time.sleep(REQUEST_DELAY)
        
        return verses
    
    def scrape_kanda(self, kanda_key: str):
        """Scrape all Sargas in a Kanda"""
        kanda_info = KANDAS[kanda_key]
        num_sargas = kanda_info['sargas']
        
        logger.info(f"\n{'='*60}")
        logger.info(f"TEST: Scraping {kanda_info['name']} ({num_sargas} Sargas)")
        logger.info(f"{'='*60}")
        
        kanda_verses = {}
        
        for sarga_num in range(1, num_sargas + 1):
            logger.info(f"Progress: {sarga_num}/{num_sargas}")
            
            verses = self.scrape_sarga(kanda_key, sarga_num)
            if verses:
                kanda_verses[sarga_num] = verses
            else:
                logger.warning(f"No verses found for {kanda_key} Sarga {sarga_num}")
        
        logger.info(f"\n✓ Completed {kanda_info['name']}: {sum(len(v) for v in kanda_verses.values())} verses")
        return kanda_verses
    
    def scrape_all(self):
        """Scrape all Kandas"""
        start_time = time.time()
        logger.info("Starting Ramayana TEST scraping (Bala Kanda only)...")
        
        for kanda_key in KANDAS.keys():
            kanda_verses = self.scrape_kanda(kanda_key)
            self.data['kandas'][kanda_key] = kanda_verses
            self.data['metadata']['kandas'].append({
                'name': KANDAS[kanda_key]['name'],
                'key': kanda_key,
                'sargas': len(kanda_verses)
            })
        
        elapsed = time.time() - start_time
        logger.info(f"\n{'='*60}")
        logger.info(f"✓ TEST scraping complete!")
        logger.info(f"Total verses: {self.verses_count}")
        logger.info(f"Time elapsed: {elapsed:.2f} seconds ({elapsed/60:.2f} minutes)")
        logger.info(f"{'='*60}\n")
    
    def save_to_json(self):
        """Save scraped data to JSON file"""
        try:
            with open(self.output_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            logger.info(f"✓ Test data saved to {self.output_file}")
            logger.info(f"File size: {Path(self.output_file).stat().st_size / 1024:.2f} KB")
        except Exception as e:
            logger.error(f"Error saving to JSON: {e}")


if __name__ == "__main__":
    scraper = RamayanaaScraper()
    
    try:
        scraper.scrape_all()
        scraper.save_to_json()
        logger.info("✓ Test complete! Ready for full scrape.")
        
    except KeyboardInterrupt:
        logger.info("\nInterrupted by user.")
    except Exception as e:
        logger.error(f"Error: {e}")