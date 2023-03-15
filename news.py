from os import getenv

import requests
from dotenv import load_dotenv

load_dotenv()

class NewsFeed:
    """
    Representing multiple news title and links as a single string
    """
    newsapi_api_key = getenv('NEWSAPI_APIKEY')
    BASE_URL = 'https://newsapi.org/v2/everything?'

    def __init__(self, interest, from_date, to_date, language):
        self.interest = interest
        self.from_date = from_date
        self.to_date = to_date
        self.language = language

    def get(self):
        url = (f'{self.BASE_URL}'
               f'q={self.interest}&'
               f'from={self.from_date}&'
               # f'from={self.to_date}'
               f'sortBy=popularity&'
               f'searchIn=title&'
               f'language={self.language}&'
               f'apiKey={self.newsapi_api_key}')

        response = requests.get(url)
        content = response.json()

        articles = content['articles']

        email_body = ''
        article_count = 0

        for article in articles:
            email_body = email_body + article['title'] + '\n' + article['url'] + '\n\n'
            article_count += 1
            if article_count > 10:
                break
        return email_body
