import requests
from bs4 import BeautifulSoup
import json
import os
from typing import List, Dict

def scrape_countries() -> List[Dict]:
    """
    Парсит информацию о странах с сайта
    Returns: список словарей с информацией о странах
    """
    url = "https://www.scrapethissite.com/pages/simple/"
    
    try:
        print("Загружаем страницу...")
        response = requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        response.raise_for_status()
        
        print("Парсим данные...")
        soup = BeautifulSoup(response.content, 'html.parser')
        
        countries = []
        country_cards = soup.find_all('div', class_='col-md-4 country')
        
        for card in country_cards:
            # Извлекаем название страны
            country_element = card.find('h3', class_='country-name')
            country_name = country_element.get_text(strip=True) if country_element else "Неизвестно"
            
            # Извлекаем столицу
            capital_element = card.find('span', class_='country-capital')
            capital = capital_element.get_text(strip=True) if capital_element else "Неизвестно"
            
            # Извлекаем дополнительную информацию (опционально)
            population_element = card.find('span', class_='country-population')
            population = population_element.get_text(strip=True) if population_element else "0"
            
            area_element = card.find('span', class_='country-area')
            area = area_element.get_text(strip=True) if area_element else "0"
            
            countries.append({
                'country': country_name,
                'capital': capital,
                'population': int(population) if population.isdigit() else 0,
                'area': float(area) if area.replace('.', '', 1).isdigit() else 0.0
            })
        
        print(f"Найдено {len(countries)} стран")
        return countries
        
    except requests.RequestException as e:
        print(f"Ошибка при загрузке страницы: {e}")
        return []
    except Exception as e:
        print(f"Ошибка при парсинге: {e}")
        return []

def save_to_json(data: List[Dict], filename: str = 'data.json'):
    """Сохраняет данные в JSON файл"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✓ Данные успешно сохранены в файл: {filename}")
        print(f"  Размер файла: {os.path.getsize(filename)} байт")
    except Exception as e:
        print(f"✗ Ошибка при сохранении в JSON: {e}")

def display_countries(countries: List[Dict], limit: int = 10):
    """Выводит страны в консоль в заданном формате"""
    print(f"\nПервые {limit} стран из списка:")
    print("=" * 60)
    
    for i, country in enumerate(countries[:limit], 1):
        print(f"{i:3}. Country: {country['country']:30} Capital: {country['capital']}")
    
    if len(countries) > limit:
        print(f"... и еще {len(countries) - limit} стран")

def main():
    """Основная функция программы"""
    print("=" * 60)
    print("ПАРСЕР ИНФОРМАЦИИ О СТРАНАХ")
    print("=" * 60)
    
    # Парсим данные
    countries = scrape_countries()
    
    if not countries:
        print("Не удалось получить данные. Завершение программы.")
        return
    
    # Выводим первые 10 стран для примера
    display_countries(countries)
    
    # Сохраняем в JSON
    save_to_json(countries)
    
    # Информация о данных
    total_population = sum(country['population'] for country in countries)
    avg_area = sum(country['area'] for country in countries) / len(countries) if countries else 0
    
    print(f"\nСтатистика данных:")
    print(f"• Всего стран: {len(countries)}")
    print(f"• Общая численность населения: {total_population:,}")
    print(f"• Средняя площадь страны: {avg_area:,.2f} км²")
    
    print("\n" + "=" * 60)
    print("Программа успешно завершена!")
    print("Запустите generate_html.py для создания HTML-страницы")
    print("=" * 60)

if __name__ == "__main__":
    main()