from bs4 import BeautifulSoup as bs
import requests
import pandas as pd

main_link = 'https://hh.ru'
page = 0
i = 1
df = pd.DataFrame({
    'Name': [],
    'Min salary': [],
    'Max salary': [],
    'Currency': [],
    'URL': [],
    'Source': []
})
# params = {'area': '',
#           'text': 'data science',
#           'page':str(page)}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Accept': '*/*'}

while i:
    params = {'area': '',
              'text': 'data science',
              'page': str(page)}
    response = requests.get(main_link + '/search/vacancy', headers=headers, params=params)
    soup = bs(response.text, 'lxml')
    # print(soup)
    v_list = soup.find('div', {'class': 'vacancy-serp'})
    v_block = v_list.find_all('div', {'class': 'vacancy-serp-item'})
    vacancies = []

    for vacancy in v_block:
        # print(vacancy)
        # print('_________________________________________________________________________________________________')
        min_sal, max_sal, cur, sal, vn, link = None, None, None, None, None, None
        vn = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-title'}).text
        link = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})['href']
        try:
            sal = vacancy.find('div', {'class': 'vacancy-serp-item__sidebar'}) .text.replace('\xa0','')
            if sal.find('т')>0: #re.search('до', sal).group():
                min_sal = sal[sal.find(' ')+1:sal.rfind(' ')]
                max_sal = None
                cur = sal[sal.rfind(' ')+1:]
            elif sal.find('о')>0: #re.search('от', sal).group():
                min_sal = None
                max_sal = sal[sal.find(' ')+1:sal.rfind(' ')]
                cur = sal[sal.rfind(' ')+1:]
            elif sal.find('-')>0: #sal.find('-'):
                min_sal = sal[:sal.find('-')].replace('\xa0','')
                max_sal = sal[sal.find('-')+1:sal.rfind(' '):]
                cur = sal[sal.rfind(' ')+1::]
            else:
                sal = None
        except:
            sal = None
        df = df.append({
            'Name': vn,
            'Min salary': min_sal,
            'Max salary': max_sal,
            'Currency': cur,
            'URL': link,
            'Source': main_link},
            ignore_index=True
        )
    try:
        i = soup.find('a', {'data-qa': 'pager-next'})['href']
    except:
        i = 0
    page += 1

print(df)
