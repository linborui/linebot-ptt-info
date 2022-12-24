import os

from linebot import LineBotApi
from linebot.models import TextSendMessage, TemplateSendMessage, ButtonsTemplate, CarouselTemplate, MessageAction, URIAction, CarouselColumn


channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
line_bot_api = LineBotApi(channel_access_token)


def send_text_message(reply_token, text):
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))
    return "OK"

def send_button_message(reply_token, title, text, buttons):
    actions = []
    for button in buttons:
        if 'url' in button:
            actions.append(URIAction(label=button['label'], uri=button['url']))
        else:
            actions.append(MessageAction(label=button['label'], text=button['text']))
    line_bot_api.reply_message(reply_token, TemplateSendMessage(alt_text='Buttons template', template=ButtonsTemplate(title=title, text=text, actions=actions)))
    return "OK"


def send_carousel_message(reply_token, buttons):
    actions = []
    columns = []
    page = 1
    for i in range(len(buttons)):
        actions.append(MessageAction(label=buttons[i], text=str(i+1)))
        if i % 10 == 9 or i == len(buttons) - 1:
            columns.append(CarouselColumn(title=f'Page {page}', text='', actions=actions))
            page += 1
    line_bot_api.reply_message(reply_token, TemplateSendMessage(alt_text='Carousel template', template=CarouselTemplate(columns=columns)))
    return "OK"