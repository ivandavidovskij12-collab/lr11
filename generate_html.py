import json
import os
from datetime import datetime

def load_countries_from_json(filename: str = 'data.json') -> list:
    """Загружает данные из JSON файла"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✓ Загружено {len(data)} стран из {filename}")
        return data
    except FileNotFoundError:
        print(f"✗ Файл {filename} не найден. Сначала запустите main.py")
        print("  Запустите: python main.py")
        return []
    except json.JSONDecodeError as e:
        print(f"✗ Ошибка чтения JSON файла {filename}: {e}")
        return []

def generate_html(countries: list) -> str:
    """Генерирует HTML код страницы"""
    
    # Подсчет статистики
    total_countries = len(countries)
    total_population = sum(c.get('population', 0) for c in countries)
    avg_population = total_population // total_countries if total_countries > 0 else 0
    
    html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Страны мира - Каталог стран</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
            min-height: 100vh;
            padding: 20px;
            color: #333;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            overflow: hidden;
        }}
        
        header {{
            background: linear-gradient(90deg, #1a2980, #26d0ce);
            color: white;
            padding: 40px 20px;
            text-align: center;
        }}
        
        h1 {{
            font-size: 2.8rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }}
        
        h1 i {{
            color: #FFD700;
            margin-right: 15px;
        }}
        
        .stats-bar {{
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-top: 25px;
            flex-wrap: wrap;
        }}
        
        .stat-item {{
            background: rgba(255, 255, 255, 0.2);
            padding: 15px 25px;
            border-radius: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 1.1rem;
        }}
        
        .stat-item i {{
            font-size: 1.5rem;
            color: #FFD700;
        }}
        
        .table-container {{
            padding: 30px;
            overflow-x: auto;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            border-spacing: 0;
            background: white;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            border-radius: 10px;
            overflow: hidden;
        }}
        
        thead {{
            background: linear-gradient(90deg, #4b6cb7, #182848);
            color: white;
        }}
        
        th {{
            padding: 20px 15px;
            text-align: left;
            font-size: 1.1rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 600;
        }}
        
        th i {{
            margin-right: 10px;
        }}
        
        th:first-child {{
            border-top-left-radius: 10px;
        }}
        
        th:last-child {{
            border-top-right-radius: 10px;
        }}
        
        tbody tr {{
            border-bottom: 1px solid #e0e0e0;
            transition: all 0.3s ease;
        }}
        
        tbody tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}
        
        tbody tr:hover {{
            background-color: #e3f2fd;
            transform: translateY(-2px);
            box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
        }}
        
        td {{
            padding: 18px 15px;
            font-size: 1rem;
        }}
        
        .country-name {{
            font-weight: 600;
            color: #2c3e50;
            font-size: 1.05rem;
        }}
        
        .capital-name {{
            color: #3498db;
            font-weight: 500;
        }}
        
        .population {{
            color: #27ae60;
            font-weight: 500;
            text-align: right;
        }}
        
        .area {{
            color: #e74c3c;
            font-weight: 500;
            text-align: right;
        }}
        
        .number {{
            color: #7f8c8d;
            font-weight: bold;
            text-align: center;
            width: 60px;
        }}
        
        footer {{
            background: #2c3e50;
            color: white;
            padding: 40px 20px;
            text-align: center;
        }}
        
        .source-link {{
            display: inline-flex;
            align-items: center;
            gap: 12px;
            background: linear-gradient(90deg, #ff7e5f, #feb47b);
            color: white;
            text-decoration: none;
            padding: 16px 35px;
            border-radius: 50px;
            font-weight: bold;
            font-size: 1.1rem;
            transition: all 0.3s ease;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
            margin-bottom: 20px;
        }}
        
        .source-link:hover {{
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
            background: linear-gradient(90deg, #ff9966, #ff5e62);
        }}
        
        .timestamp {{
            color: #bdc3c7;
            font-size: 0.95rem;
            margin-top: 15px;
        }}
        
        /* Адаптивность */
        @media (max-width: 768px) {{
            h1 {{
                font-size: 2rem;
            }}
            
            .container {{
                margin: 10px;
            }}
            
            th, td {{
                padding: 12px 8px;
                font-size: 0.9rem;
            }}
            
            .table-container {{
                padding: 15px;
            }}
            
            .stats-bar {{
                flex-direction: column;
                align-items: center;
                gap: 15px;
            }}
        }}
        
        /* Анимация */
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        tbody tr {{
            animation: fadeIn 0.5s ease forwards;
            opacity: 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1><i class="fas fa-globe-americas"></i>Страны мира</h1>
            <p>Полный каталог стран с информацией о столицах, населении и площади</p>
            
            <div class="stats-bar">
                <div class="stat-item">
                    <i class="fas fa-flag"></i>
                    <span>Стран: <strong>{total_countries}</strong></span>
                </div>
                <div class="stat-item">
                    <i class="fas fa-users"></i>
                    <span>Население: <strong>{total_population:,}</strong></span>
                </div>
                <div class="stat-item">
                    <i class="fas fa-chart-line"></i>
                    <span>В среднем: <strong>{avg_population:,}</strong> чел./страна</span>
                </div>
            </div>
        </header>
        
        <div class="table-container">
            <table>
                <thead>
                    <tr>
                        <th><i class="fas fa-hashtag"></i>№</th>
                        <th><i class="fas fa-flag"></i>Страна</th>
                        <th><i class="fas fa-landmark"></i>Столица</th>
                        <th><i class="fas fa-users"></i>Население</th>
                        <th><i class="fas fa-mountain"></i>Площадь (км²)</th>
                    </tr>
                </thead>
                <tbody>"""
    
    # Генерируем строки таблицы
    for i, country in enumerate(countries, 1):
        population = country.get('population', 0)
        area = country.get('area', 0.0)
        
        # Форматируем числа
        population_fmt = f"{population:,}" if population > 0 else "-"
        area_fmt = f"{area:,.1f}" if area > 0 else "-"
        
        html += f"""
                    <tr style="animation-delay: {i*0.02}s">
                        <td class="number">{i}</td>
                        <td class="country-name">{country['country']}</td>
                        <td class="capital-name">{country['capital']}</td>
                        <td class="population">{population_fmt}</td>
                        <td class="area">{area_fmt}</td>
                    </tr>"""
    
    html += f"""
                </tbody>
            </table>
        </div>
        
        <footer>
            <a href="https://www.scrapethissite.com/pages/simple/" 
               target="_blank" 
               rel="noopener noreferrer"
               class="source-link">
                <i class="fas fa-external-link-alt"></i>
                Источник данных: ScrapeThisSite.com
            </a>
            <div class="timestamp">
                <i class="far fa-clock"></i>
                Данные обновлены: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')} |
                Сгенерировано программой на Python
            </div>
        </footer>
    </div>
    
    <script>
        // Анимация при прокрутке
        document.addEventListener('DOMContentLoaded', function() {{
            const observerOptions = {{
                threshold: 0.1,
                rootMargin: '0px 0px -50px 0px'
            }};
            
            const observer = new IntersectionObserver((entries) => {{
                entries.forEach(entry => {{
                    if (entry.isIntersecting) {{
                        entry.target.style.animationPlayState = 'running';
                    }}
                }});
            }}, observerOptions);
            
            document.querySelectorAll('tbody tr').forEach(row => {{
                observer.observe(row);
            }});
        }});
    </script>
</body>
</html>"""
    
    return html

def save_html(html_content: str, filename: str = 'index.html'):
    """Сохраняет HTML в файл"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"✓ HTML страница сохранена в файл: {filename}")
        print(f"  Размер файла: {os.path.getsize(filename):,} байт")
        print(f"  Откройте файл {filename} в браузере для просмотра")
    except Exception as e:
        print(f"✗ Ошибка при сохранении HTML: {e}")

def main():
    """Основная функция генератора HTML"""
    print("=" * 60)
    print("ГЕНЕРАТОР HTML СТРАНИЦЫ СО СТРАНАМИ")
    print("=" * 60)
    
    # Загружаем данные
    countries = load_countries_from_json()
    
    if not countries:
        print("\nЗапустите сначала парсер:")
        print("python main.py")
        return
    
    # Генерируем HTML
    print("\nГенерируем HTML страницу...")
    html_content = generate_html(countries)
    
    # Сохраняем HTML
    save_html(html_content)
    
    print("\n" + "=" * 60)
    print("✓ HTML страница успешно создана!")
    print("=" * 60)

if __name__ == "__main__":
    main()