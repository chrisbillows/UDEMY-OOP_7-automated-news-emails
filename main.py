from datetime import datetime, timedelta
from os import getenv
import time

from dotenv import load_dotenv
import pandas as pd
import yagmail

from news import NewsFeed


load_dotenv()

gmail_login = getenv('GMAIL_LOGIN')
gmail_app_password = getenv('GMAIL_APP_PASSWORD')


def format_date_for_news_api(day):
    return day.strftime("%Y-%m-%d")


while True:
    if datetime.now().hour == 10 and datetime.now().minute == 41:
        df = pd.read_excel("news_feed_users.xlsx")

        for index, row in df.iterrows():
            today = datetime.now()
            yesterday = today - timedelta(days=1)

            user_news_feed = NewsFeed(
                interest=row["interest"],
                from_date=format_date_for_news_api(yesterday),
                to_date=format_date_for_news_api(today),
                language="en",
            )

            email = yagmail.SMTP(user=gmail_login, password=gmail_app_password)
            email.send(
                to=row["email"],
                subject=f"Your daily update on {row['interest']}",
                contents=(
                    f"Hi {row['name']}!\n\n"
                    f"Here are the top 10 news articles today about {row['interest']}:\n\n"
                    f"{user_news_feed.get()}\n\n"
                    f"Lots of love, Chris"
                ),
            )

    time.sleep(60)

