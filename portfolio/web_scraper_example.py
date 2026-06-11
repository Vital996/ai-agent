#!/usr/bin/env python3
"""
Web Scraper Example
Парсит данные с сайта и сохраняет в CSV
"""
import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

def scrape_quotes(url="https://quotes.toscrape.com"):
    """
    Парсит цитаты с сайта и сохраняет в CSV
    
    Использование:
        python3 web_scraper_example.py
    """
    
    print("🕷️  Web Scraper")
    print("=" * 50)
    print(f"Target: {url}")
    print()
    
    try:
        # Шаг 1: Загружаем страницу
        print("📥 Fetching website...")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        print(f"✅ Status: {response.status_code}")
        print()
        
        # Шаг 2: Парсим HTML
        print("🔍 Parsing data...")
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Шаг 3: Извлекаем данные
        quotes = []
        for quote_div in soup.find_all('div', class_='quote'):
            text = quote_div.find('span', class_='text').get_text()
            author = quote_div.find('small', class_='author').get_text()
            
            quotes.append({
                'quote': text,
                'author': author
            })
        
        print(f"✅ Found {len(quotes)} quotes")
        print()
        
        # Шаг 4: Сохраняем в CSV
        output_file = f"quotes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        print(f"💾 Saving to {output_file}...")
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['quote', 'author'])
            writer.writeheader()
            writer.writerows(quotes)
        
        print(f"✅ Saved!")
        print()
        
        # Шаг 5: Показываем результат
        print("📊 Sample data:")
        print("-" * 50)
        for i, quote in enumerate(quotes[:3], 1):
            print(f"{i}. {quote['quote']}")
            print(f"   — {quote['author']}")
            print()
        
        if len(quotes) > 3:
            print(f"... and {len(quotes) - 3} more quotes")
        
        print("-" * 50)
        print(f"📈 Total: {len(quotes)} quotes extracted")
        print(f"💿 File: {output_file}")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == '__main__':
    scrape_quotes()
