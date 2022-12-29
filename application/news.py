from application import spacy_summary
from bs4 import BeautifulSoup as soup
import requests


class news:
    headline = ""
    image_src = ""
    link = ""
    summary = ""


def get_text(url):
    html = requests.get(url)
    bsobj = soup(html.text, 'html.parser')
    text = ' '.join(map(lambda p: p.text, bsobj.findAll('p')))
    return text


def get_news_list(news_category):
    url = ""
    if news_category == "Latest":
        url = 'https://bdnews24.com/collection/111531'
    elif news_category == "International":
        url = 'https://bdnews24.com/neighbours'
    elif news_category == "Education":
        url = 'https://bdnews24.com/education'
    elif news_category == "Economy":
        url = 'https://bdnews24.com/business'
    elif news_category == "Politics":
        url = 'https://bdnews24.com/politics'
    elif news_category == "Sports":
        url = 'https://bdnews24.com/cricket'
    elif news_category == "Lifestyle":
        url = 'https://bdnews24.com/lifestyle'
    elif news_category == "Science":
        url = 'https://bdnews24.com/science'
    elif news_category == "Environment":
        url = 'https://bdnews24.com/environment'

    r = requests.get(url)
    s = soup(r.text, 'html.parser')
    images = s.findAll('img')
    image_src = []
    image_src.append('a')
    for image in images:
        image_src.append(image['src'])
    news_headlines = []
    for headlines in s.findAll('h6', {'class': 'headline-m_headline__3_NhV headline-m_dark__en3hW'}):
        news_headlines.append(headlines.text)
    news_links = []
    for links in s.findAll('a', {'aria-label': 'headline'}):
        news_links.append(links['href'])
    x = len(news_links)
    newslist = []
    for i in range(x):
        newsobj = news()
        newsobj.headline = news_headlines[i]
        newsobj.image_src = image_src[(i + 1) * 2]
        newsobj.link = news_links[i]
        text = get_text(url=newsobj.link)
        newsobj.summary = spacy_summary.spacy_summary(newsobj.headline, text)
        newslist.append(newsobj)
    # for i in range(x):
    #     print(newslist[i].headline, "\n", newslist[i].image_src, "\n", newslist[i].summary, "\n", newslist[i].link,
    #           "\n")

    return newslist
