from newsapi import NewsApiClient
from newsapi.newsapi_exception import NewsAPIException
import json
import sys
import time
from datetime import datetime
import unicodedata

data = json.load(open('data.json'))
NEWSAPI_KEY = data["key"]
REQUEST_SOURCES = data["sources"].__str__()
REQUEST_PAGESIZE = 100

class ArticleObj:
    def __init__(self, source, author, title, description, url, publishedAt):
        self.source = source if source else ""
        self.author = author if author else ""
        self.title = title if title else ""
        self.description = description if description else ""
        self.url = url if url else ""
        self.publishedAt = publishedAt if publishedAt else "" #datetime.strptime(publishedAt, '%Y-%m-%dT%H:%M:%SZ').strftime("%H:%M:%S, %d.%m.%Y")
        self.printed = False
    
    def __eq__(self, other):
        return (self.url == other.url)
    def __lt__(self, other):
        return (self.publishedAt < other.publishedAt)
    def __str__(self):
        self.printed = True
        ret = unicodedata.normalize('NFC', self.title + "\n\t" + self.description + "\n\t" + self.source + " (" + self.author + ", " + self.publishedAt + ")\n\turl: " + self.url + "\n").encode('ascii', 'ignore')
        return ret

newsapi = NewsApiClient(api_key=NEWSAPI_KEY)
headlines = None
articles = list()

sources = newsapi.get_sources()

while( True ):

    try:
        headlines = newsapi.get_top_headlines(sources=REQUEST_SOURCES, page_size=REQUEST_PAGESIZE)
    except NewsAPIException as err:
        print("error\n\tcode: " + err.get_code() + "\n\tstatus: " + err.get_status() + "\n\t" + err.get_message())
        sys.exit()

    for article in headlines["articles"]:
        newArticle = ArticleObj(article["source"]["name"], article["author"], article["title"], article["description"], article["url"], article["publishedAt"])
        if not (newArticle in articles):
            articles.append(newArticle)
    
    articles.sort()

    for articleToPrint in articles:
        if not articleToPrint.printed:
            print(articleToPrint)

    while len(articles) > 200:
        articles.pop(0)

    time.sleep( 90 )
