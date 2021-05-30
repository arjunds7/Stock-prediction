import requests as rfq
from twilio.rest import Client

twilio_sid = "use your twilio sid id"
twilio_oath = "use your twilio oath id"
my_twilio = "use your twilio generated phone number"

NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API = "use your api key after sign up"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
API_KEY_S = "use your api key"

parameters_s = {

    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": API_KEY_S

}

response = rfq.get(STOCK_ENDPOINT, params=parameters_s)
response.raise_for_status()
data = response.json()['Time Series (Daily)']
data_list = [value for (key, value) in data.items()]

yesterdays_data = data_list[0]
yesterdays_closing_price = yesterdays_data['4. close']

day_before_yesterdays_data = data_list[1]
day_before_yesterdays_closing_price = day_before_yesterdays_data['4. close']

difference_in_closing_price = (float(yesterdays_closing_price) - float(day_before_yesterdays_closing_price))
up_down = None
if difference_in_closing_price > 0:
    up_down = "⬆"
else:
    up_down = "⬇"

diff_percent = round(difference_in_closing_price / float(yesterdays_closing_price)) * 100
print(diff_percent)

parameters_n = {
    "apiKey": NEWS_API,
    "qInTitle": COMPANY_NAME
}
if abs(diff_percent) >= .1:
    news_response = rfq.get(NEWS_ENDPOINT, params=parameters_n)
    news_response.raise_for_status()
    articles_data = news_response.json()["articles"]
    three_articles = articles_data[:3]
    formatted_article = [f"{COMPANY_NAME} {up_down}%\nHeadline: {articles['title']}.\n" \
                         f"Description: {articles['description']}" for articles in three_articles]
    client = Client(twilio_sid, twilio_oath)
    for article in formatted_article:
        message = client.messages.create(body=article,
                                         from_=my_twilio,
                                         to="phone number to send the message"
                                         )
        print(message.status)
else:
    print("No good news today")