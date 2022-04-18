# import libraries
from bs4 import BeautifulSoup as bs
import requests
import re


def get_soup_book(book_title):
    search_book = get_search(book_title)
    print(search_book)
    search_page_soup = get_soup(search_book)
    search_book = find_book(search_page_soup)
    search_href = get_href(search_book)
    book_soup = get_soup(search_href)
    return book_soup


def get_search(search_term):
    """
    Generate url from search term
    """
    template = 'https://www.google.com/search?q={}'
    search_term = f"""{search_term} goodreads"""
    search_term = re.sub(r'[^\w]', ' ', search_term)
    url = search_term.replace(' ', '+')
    return template.format(url)


def get_soup(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
               'Accept-Language': 'en-US, en;q=0.5'}
    page = requests.get(url, headers=headers)
    soup = bs(page.content, 'html.parser')
    return soup


def find_book(soup):
    book = soup.find_all('div', {'class': 'yuRUbf'})
    return book[0]


def get_href(soup):
    book_href = soup.find('a')['href']
    return book_href


def get_description(soup):
    book_description = soup.find_all('div', id="description")
    book_description = book_description[0].find_all('span')
    return book_description[1].text


def get_title(soup):
    book_title = soup.find('h1', class_="gr-h1 gr-h1--serif")
    book_title = book_title.text
    return book_title.lstrip()


def get_author(soup):
    book_author = soup.find('a', {"class" : "authorName"})
    return book_author.text

