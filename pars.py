from bs4 import BeautifulSoup as bs
import requests
# f = open('f.txt', 'w', encoding='utf-8')
# url = "http://dict.ruslang.ru/freq.php?act=show&dic=freq_s&title=%D7%E0%F1%F2%EE%F2%ED%FB%E9%20%F1%EF%E8%F1%EE%EA%20%E8%EC%E5%ED%20%F1%F3%F9%E5%F1%F2%E2%E8%F2%E5%EB%FC%ED%FB%F5"

# res = requests.get(url)
# soup = bs(res.text, 'html.parser').find('table').find('table').find_all('tr')[2::]
# for s in soup:
#     f.write(str(bs(str(s), 'html.parser').find_all('td')[1])[4:-5]+'\n')
# f.close()
f = open("dict/bigFormal.txt", 'w', encoding='utf-8')
for page in range(10, 1334):
    url = f"https://slovar.cc/rus/tolk.html?start={(page-1)*100}"
    res = requests.get(url)
    soup = bs(res.text, 'html.parser').find('nav', class_ = "vocab-words-list").find('ul').find_all('a')
    for i in range(len(soup)): 
        word = soup[i].text
        if len(word) >= 3 and not ' ' in word  and not '.' in word and not '(' in word and word[-1] != '-':
            f.write(soup[i].text.lower() + '\n')
f.close()