import tweepy
import requests
from bs4 import BeautifulSoup
import time
import os
from flask import Flask, render_template, request, redirect

# Twitter API credentials

consumer_key=os.getenv('CONSUMER_KEY')
consumer_secret=os.getenv('CONSUMER_SECRET')
access_key=os.getenv('ACCESS_KEY')
access_secret=os.getenv('ACCESS_SECRET')

# Twitter API setup and authentication

auth=tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api=tweepy.API(auth)

app = Flask(__name__)


#Home Route
@app.route('/')
def index():
    return 'Setting up the Twitter bot'

#retrieves mention data from twitter
@app.route('/webhook', methods=['POST'])
def webhook():
    #retrieve the mention data from twitter
    data=request.get_json()
    text=data['text'].lower()
    username=data['user']['screen_name']
    mention_id=data['id_str']
    print(text)

    if '@bugzerobot' in text and ('hacker' in text or 'cybersecurity' in text):
        #scrapping the data from twitter for the latest news with the keyword 'hacker' or 'cybersecurity'
        query = 'hacker' if 'hacker' in text else 'cybersecurity'
        tweets=api.search_tweets(query, + ' -filter:retweets', lang='en', result_type='recent', count=5)
        #creating a list of tweets
        news=[]
        for tweet in tweets:
            text=tweet.text.strip()
            link='https://twitter.com/'+tweet.user.screen_name+'/status/'+tweet.id_str

            news.append({'text':text, 'link':link})

        #creating a string of tweets
        news_string=''
        for i in range(len(news)):
            news_string+=str(i+1)+'. '+news[i]['text']+' '+news[i]['link']+' '

        #replying to the mention with the latest news
        api.update_status('@' + username + ' Here are the latest news on ' + query + ':', mention_id)
        for article in news:
            api.update_status(article['text'] + ' ' + article['link'], mention_id)
        
    return 'success', 200

if __name__ == '__main__':
    app.run(debug=True)


