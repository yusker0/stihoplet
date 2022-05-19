from msilib.schema import tables
import sqlite3
from bs4 import BeautifulSoup as bs
import requests



db = sqlite3.connect('stihoplet.db')
sql = db.cursor()

# table = """CREATE TABLE IF NOT EXISTS users(
#            id INT UNIQUE,
#            rhyme CHAR(8),
#            str_count INT, 
#            stepSize INT, 
#            stressSyll INT
#         );"""
# sql.execute(table)
# db.commit()
# table = sql.execute("SELECT word, upperID FROM formal").fetchall()
# for word in table:
#     word_text = word[0].lower()
#     syllables = 0
#     for ch in range(len(word_text)):
#         if word_text[ch] in 'аеёиоуэюяы':
#             syllables += 1
#         if ch == word[1]:
#             upperID = syllables
#     sql.execute("UPDATE formal SET syllables_count=?, upperID=? WHERE word=?", (syllables, upperID, word[0]))
# db.commit()

# table = """CREATE TABLE IF NOT EXISTS formal(
#            end CHAR(2),
#            word CHAR(255), 
#            upperID INT,
#            syllables_count INT
#         );"""
# sql.execute(table)
# db.commit()
# url = "https://orthoepic.ru"
# res = requests.get(url)
# alphabet = bs(res.text, 'html.parser').find('nav', {'id' : 'alphabet'}).find_all('a')[28::]
# def parsPage(res):
#     words = bs(res.text, 'html.parser').find('p', class_ = 'list').find_all('a')
#     for word_url in words:
#         res = requests.get(url + word_url['href'])
#         soup = bs(res.text, 'html.parser').find('em')
#         if len(soup.contents)>=2 and len(soup.contents)<=3:
#             word = ''
#             upper_id = -1
#             id = 0
#             for s in soup.contents:
#                 id += len(s.text)
#                 if '<span>' in str(s):
#                     upper_id = id if upper_id == -1 else -2
#                 word += s.text
#             if upper_id >= 0:
#                 sql.execute("INSERT INTO formal (end, word, upperID) VALUES(?, ?, ?)", (word[-2]+word[-1], word, upper_id))
# for letter_url in alphabet:
#     print("---------------" + letter_url['href'] + "---------------")
#     print(1)
#     res = requests.get(url + letter_url['href'])
#     pages = bs(res.text, 'html.parser').find('section', {'id':'pages'}).find_all('li')     
#     parsPage(res)
#     if len(pages) != 0:
#         pages = int(pages[-1].text)
#         for page in range(2, pages+1):
#             print(page)
#             res = requests.get(f"{url}{letter_url['href']}/page{page}")
#             parsPage(res)
#         db.commit()