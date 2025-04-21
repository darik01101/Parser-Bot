from requests import get
from key_words import KEY_WORDS
from bs4 import BeautifulSoup
def empty(): return ''
def fl():


    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }
    title_class = 'b-post__title'
    description_class = 'b-post__txt'
    start_page = 1
    status_200 = True
    while status_200:
        request_str =  rf'https://www.fl.ru/projects/page-{start_page}/'
        #отпрвить запрос
        response = get(request_str,headers = headers)
        code = response.status_code
        if code != 200 or start_page == 2:
            status_200 = False
        else:
            cards = []
            html = response.text
            soup = BeautifulSoup(html,'html.parser')
            #for card in cards:
            descriptions = soup.find_all(class_=description_class)
            titles = soup.find_all(class_=title_class)
            
            #print(1,descriptions)
            #print(2,titles)
            for i in range(len(titles)):
                cards.append({
                    #'title':titles[i].get_text(strip=True),
                    'description':descriptions[i].get_text(strip=True),
                })


            start_page += 1
            
            print(cards)
    return f'всего просмотрено страниц {start_page}'
def utest():
    PAYLOAD_FIELDS = [
        'current_user_permissions',
        'type',
        'title',
        'slug',
        'content',
        'start_date',
        'state',
        'published_at',
        'countries'
    ]
    TEST_FIELDS = [
        'title',
        'content'
    ]
    base_url = "https://www.utest.com/api/v1/projects"
    params = {
    # Фильтр: только опубликованные проекты и только рекомендованные
    "filter": '{"state":"published","suggested_projects":true}',

    # Пагинация: страница 1
    "page": 1,

    # Количество проектов на странице
    "per_page": 10,

    # Сортировка: по убыванию даты обновления
    "sort": "-updated_at"
    }
    response = get(base_url, params=params)
    if response.ok:
        data = response.json()
        formatted_data = list(
            map(
                lambda record:
                {k:v for k,v in record.items() if k in PAYLOAD_FIELDS},
                data
            )
        )
        test_data = list(
            map(
                lambda record:
                {k:v for k,v in record.items() if k in TEST_FIELDS},
                formatted_data
            )
        )    
        for record in test_data:
            title = record.get('title').lower()
            content = record.get('content').lower()
            for key_word in KEY_WORDS:
                if key_word.lower() in title or key_word.lower() in content:
                    print('нашли')
                else:
                    print('не нашли')


    else:
        print("Ошибка запроса:", response.status_code, response.text)

SITES = {
    r'https://profi.ru/': empty,
    r'https://www.fl.ru/': empty,#fl,
    r'https://www.weblancer.net/': empty,
    r'https://freelance.ru/': empty,
    r'https://kwork.ru/': empty,
    r'https://www.utest.com/': utest,
    r'https://www.guru.com/pro/': empty,#нужен логин
    r'https://www.freelancer.com': empty,
    r'https://freelancer.testlio.com/': empty,#нужен логин
    r'https://freelance.habr.com/': empty,
}