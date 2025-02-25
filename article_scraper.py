import requests
from bs4 import BeautifulSoup
import nltk
import re

nltk.download('punkt')
from nltk.tokenize import sent_tokenize

def fetch_article(url):
    """Загружает HTML страницы и извлекает основной текст"""
    url = url.strip()  # бля пробелы уберу хуй знает
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Referer": "https://www.google.com",
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            print("Ошибка 404: Страница не найдена. Проверьте правильность URL.")
        elif response.status_code == 403:
            print("Ошибка 403: Доступ запрещён. Попробуйте другой сайт.")
        else:
            print(f"Ошибка HTTP {response.status_code}: {e}")
        return ""
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при загрузке статьи: {e}")
        return ""
    
    soup = BeautifulSoup(response.text, 'html.parser')
    paragraphs = soup.find_all('p')
    text = ' '.join([p.get_text() for p in paragraphs])
    return text if text else "Текст статьи не найден."

def find_sentences_with_keywords(text, keywords):
    """Ищет предложения с ключевыми словами"""
    sentences = sent_tokenize(text)
    found_sentences = [s for s in sentences if any(word.lower() in s.lower() for word in keywords)]
    return found_sentences if found_sentences else ["Ключевые слова не найдены в статье."]

# ссылку на сайт ввести ТОЛЬКО НОРМАЛЬНУЮ ССЫЛКУ ТВАРИ если у меня че то сломается я вас сама всех
url = input("Введите ссылку на статью: ").strip()
keywords = ["АВИАНДР", "Радия-223 хлорид", "Рифаксимин",'IMCIVREE','Эсциталопрам','Афобазол','Баета','Андипал','Алимемазин','Нейромексол','Инозин Пранобекс']

article_text = fetch_article(url)
if article_text:
    result_sentences = find_sentences_with_keywords(article_text, keywords)
    print("\nНайденные предложения:")
    for sentence in result_sentences:
        print("-", sentence)
