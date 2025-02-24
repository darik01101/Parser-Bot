import requests
from bs4 import BeautifulSoup

def fetch_data():
    url = "https://ru.wikipedia.org/wiki/"
    
    # Отключаем проверку SSL-сертификатов
    response = requests.get(url, verify=False)
    print(response)
    if response.status_code == 200:
        html = response.text
        print(response.text)
        soup = BeautifulSoup(html, "html.parser")
        quotes = soup.find_all("span", class_="text")
        return [quote.text for quote in quotes[:5]]  # Берем первые 5 цитат
    else:
        return ["Ошибка при получении данных"]

# Вызов функции и вывод результата
quotes = fetch_data()
for quote in quotes:
    print(quote)