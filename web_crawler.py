import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


ptt_url = 'https://www.ptt.cc/'
pttweb_url = 'https://www.pttweb.cc/'

payload = {
    "from": "/bbs/Gossiping/index.html",
    "yes": "yes"
}
request = requests.Session()
request.post("https://www.ptt.cc/ask/over18", data=payload)


def init_urls():
    urls = {}
    urls['hot'] = urljoin(pttweb_url, '/hot/all')
    urls['today'] = urljoin(pttweb_url, '/hot/all/today')
    urls['yesterday'] = urljoin(pttweb_url, '/hot/all/yesterday')
    urls['this-week'] = urljoin(pttweb_url, '/hot/all/this-week')
    urls['this-month'] = urljoin(pttweb_url, '/hot/all/this-month')
    urls['newest articles'] = urljoin(pttweb_url, '/newest/all')
    return urls


def get_pttweb_boards():
    url = 'https://www.pttweb.cc/bbs/hotboards'
    response = request.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    boards = soup.select('div.e7-list-content')[1].select('a.e7-list-item')
    board_list = []
    for board in boards:
        board_name = board.select('div.e7-board-name')[0].text
        board_list.append({'name': board_name, 'url': urljoin(pttweb_url, board['href'])})
    return board_list


def get_pttweb_articles(url):
    response = request.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    titles = soup.select('div.e7-container')
    articles = []
    for title in titles:
        title_url = title.select('a.e7-article-default')
        text = title.select('span.e7-show-if-device-is-not-xs')
        board = title.select('a.e7-boardName span.e7-link-to-article')
        author = title.select('span.grey--text.e7-link-to-article')
        if text:
            articles.append({'url': urljoin(pttweb_url, title_url[0]['href']), 'title': text[0].text, 'board': board[0].text, 'author': author[0].text})
    return articles


def get_pttweb_board_articles(url):
    response = request.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    titles = soup.select('div.mt-2 div.e7-container')
    articles = []
    for title in titles:
        title_url = title.select('a.e7-article-default')
        text = title.select('span.e7-show-if-device-is-not-xs')
        author = title.select('span.grey--text.e7-link-to-article')
        if text:
            articles.append({'url': urljoin(pttweb_url, title_url[0]['href']), 'title': text[0].text, 'author': author[0].text})
    return articles


def get_pttcc_url_from_pttweb(url):
    response = request.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    link = soup.select('a.externalHref span.f3')[0].text
    return urljoin(ptt_url, link)
