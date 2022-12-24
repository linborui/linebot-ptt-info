from transitions.extensions import GraphMachine
from utils import send_button_message, send_carousel_message
from web_crawler import init_urls, get_pttweb_boards, get_pttweb_articles, get_pttweb_board_articles, get_pttcc_url_from_pttweb

states = ['init', 'hot_articles', 'aritcles', 'hot_boards', 'board_articles', 'links']
transitions = []
sources = {'hot_ariticles': ['init'], 'hot_boards': ['init'], 'aritcles': ['init', 'hot_ariticles'], 'board_articles': ['hot_boards'], 'links': ['articles', 'board_articles', 'links'], 'init': states[:-1]}
for dest in sources:
    transitions.append({'trigger': 'advance', 'source': sources[dest], 'dest': dest, 'conditions': 'is_going_to_' + dest})
transitions.append({'trigger': 'go_back', 'source': 'links', 'dest': 'init'})


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
        self.urls = init_urls()

    def on_enter_init(self, event):
        print('Entering init')
        reply_token = event.reply_token
        buttons = [{'label': "最新文章", 'text': 'Newest Articles'}, {'label': "熱門文章", 'text': 'Hot Articles'}, {'label': "熱門看板", 'text': 'Hot Boards'}]
        send_button_message(reply_token, "PTT非官方資訊站", "選擇即可快速查看熱門資訊", buttons)
    
    def is_going_to_init(self, event):
        text = event.message.text
        return text.lower() == 'menu'
    
    def on_enter_hot_articles(self, event):
        print('Entering Hot Articles')
        reply_token = event.reply_token
        buttons = [{'label': "及時熱門", 'text': 'hot'}, {'label': "今日熱門", 'text': 'today'}, {'label': "昨日熱門", 'text': 'yesterday'}, {'label': "本週熱門", 'text': 'this week'}, {'label': "本月熱門", 'text': 'this month'}, {'label': "回到主選單", 'text': 'menu'}]
        send_button_message(reply_token, "熱門文章", "選擇時間", buttons)

    def is_going_to_hot_articles(self, event):
        text = event.message.text
        return text.lower() == 'hot articles'
    
    def on_enter_hot_boards(self, event):
        print('Entering Hot Boards')
        reply_token = event.reply_token
        self.boards = get_pttweb_boards()
        buttons = []
        for i in range(5):
            buttons.append({'label': self.boards[i]['name'], 'text': self.boards[i]['text']})
        buttons.append({'label': "回到主選單", 'text': 'menu'})
        send_button_message(reply_token, "熱門看板", "選擇看板", buttons)
        
    def is_going_to_hot_boards(self, event):
        text = event.message.text
        return text.lower() == 'hot boards'
    
    def on_enter_aritcles(self, event):
        print('Entering Articles')
        text = event.message.text.lower()
        self.articles = get_pttweb_articles(self.urls[text])
        self.show_articles(event.reply_token)

    def is_going_to_aritcles(self, event):
        text = event.message.text
        return text.lower() in self.urls

    def on_enter_board_articles(self, event):
        print('Entering Board Articles')
        self.show_articles(event.reply_token)

    def is_going_to_board_articles(self, event):
        text = event.message.text
        self.articles = get_pttweb_board_articles(text)
        if self.articles:
            return True
        return False

    def show_articles(self, reply_token):
        titles = []
        for article in self.articles:
            titles.append(article['title'])
        send_carousel_message(reply_token, titles)

    def on_enter_links(self, event):
        print('Entering Links')
        reply_token = event.reply_token
        idx = int(event.message.text) - 1
        article = self.articles[idx]
        buttons = [{'label': "ptt.cc", 'url': get_pttcc_url_from_pttweb(article['url'])}, {'label': "pttweb.cc", 'url': article['url']}, {'label': "回到主選單", 'text': 'menu'}]
        send_button_message(reply_token, article['title'], article['author'], buttons)
        
    def is_going_to_links(self, event):
        text = event.message.text
        try:
            idx = int(text)
            if idx > 0 and idx <= len(self.articles):
                return True
            return False
        except:
            return False
