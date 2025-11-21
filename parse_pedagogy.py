import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin

def parse_pedagogy_articles():
    """
    Парсит карточки статей с сайта pedsovet.org
    """
    base_url = "https://pedsovet.org"
    
    try:
        print("🔄 Загружаем страницу...")
        response = requests.get(base_url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        articles_data = []
        
        # Ищем карточки статей
        print("🔍 Ищем карточки статей...")
        cards = soup.find_all(class_=lambda x: x and any(
            word in x for word in ['news', 'article', 'post', 'item', 'card']))
        
        print(f"📊 Найдено потенциальных карточек: {len(cards)}")
        
        for i, card in enumerate(cards, 1):
            try:
                # Ищем заголовок
                title_elem = card.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']) or card.find('a')
                link_elem = card.find('a')
                
                if title_elem and link_elem and link_elem.get('href'):
                    title = title_elem.get_text(strip=True)
                    link = link_elem.get('href')
                    
                    # Пропускаем короткие заголовки и ссылки на соцсети
                    if len(title) > 10 and not any(social in link for social in ['facebook', 'twitter', 'vk']):
                        # Обрабатываем относительные ссылки
                        if link.startswith('/'):
                            link = urljoin(base_url, link)
                        
                        article_data = {
                            'id': i,
                            'title': title,
                            'url': link
                        }
                        articles_data.append(article_data)
                        print(f"✅ Карточка {i}: {title[:60]}...")
                        
            except Exception as e:
                continue
        
        return articles_data
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return []

def save_to_json(data, filename='articles.json'):
    """Сохраняет данные в JSON файл"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"💾 Данные сохранены в {filename}")

def main():
    print("🎓 ПАРСЕР СТАТЕЙ ПО ПЕДАГОГИКЕ")
    print("=" * 40)
    
    articles = parse_pedagogy_articles()
    
    if articles:
        print(f"\n🎯 Успешно собрано: {len(articles)} статей")
        
        # Выводим в консоль
        for article in articles:
            print(f"\n📖 {article['title']}")
            print(f"🔗 {article['url']}")
        
        # Сохраняем в файл
        save_to_json(articles)
    else:
        print("😔 Не удалось собрать данные")

if __name__ == "__main__":
    main()