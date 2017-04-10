from urllib import request
from bs4 import BeautifulSoup
import requests

search_news = str(input("Enter the word you are searching for:\n"))

def trade_spider(max_pages):
    page=1
    while(page<=max_pages):
        url = 'http://www.ndtv.com'
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text,"html.parser")
        for link in soup.findAll('a',{'class':'item-title'}):
            href = link.get('href')
            title = link.string
            if title:
                words = title.lower().split()
                for each_word in words:
                    if each_word == search_news:
                        print(href)
                        print(title)
        page += 1

trade_spider(1)



