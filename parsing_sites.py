from requests import get
from bs4 import BeautifulSoup
def empty(): return ''
def fl():

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }
    card_class = 'card-lenta-new'
    title_class = 'b-post__title'
    description_class = 'b-post__txt'
    start_page = 1
    status_200 = True
    while status_200:
        request_str =  rf'https://www.fl.ru/projects/page-{start_page}/'
        #отпрвить запрос
        response = get(request_str,headers = headers)
        code = response.status_code
        if code != 200:
            status_200 = False
        else:
            html = response.text
            soup = BeautifulSoup(html,'html.parser')
            cards = soup.find_all(class_=card_class)
            for card in cards:
                print(card.text)
                print(start_page)
            start_page += 1
    
    return f'всего просмотрено страниц {start_page}'
SITES = {
    r'https://profi.ru/': empty,
    r'https://www.fl.ru/': fl,
    r'https://www.weblancer.net/': empty,
    r'https://freelance.ru/': empty,
    r'https://kwork.ru/': empty,
    r'https://www.utest.com/': empty,
    r'https://www.guru.com/pro/': empty,#нужен логин
    r'https://www.freelancer.com': empty,
    r'https://freelancer.testlio.com/': empty,#нужен логин
    r'https://freelance.habr.com/': empty,
}