from flask import Flask, render_template, request, redirect
# from sentiment_analyzer.sentiment_analyzer import TweetAnalyzer
import json
import requests



app = Flask(__name__)

@app.route('/')
def mypage():
    text = request.args.get('text')
    myvar = get_tweets(text)
    return render_template('index.html', b=text, c=myvar)


@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    processed_text = text.upper()
    return processed_text    

@app.route('/my-form', methods = ['POST'])
def my_form():

    return render_template('my-form.html')

def analyse(comment):
    with open("good_words.txt", "r") as f:
        good_words = f.readlines()

    with open("bad_words.txt", "r") as f:
        bad_words = f.readlines()
        bw = [x.strip() for x in bad_words]
        gw = [x.strip() for x in good_words]

    comment = comment.replace("#", "")
    comment = comment.replace("@", "")
    
    current_tweet = comment.split()
    gc = 0   
    bc = 0
    for j in range(0, len(current_tweet)):
        current_word = current_tweet[j].lower() 
        if current_word in gw:
            gc += 1
        elif current_word in bw:
            bc += 1
        if gc > bc:
            sentiment = 'good'
        elif gc < bc:
            sentiment = 'bad'
        else:
            sentiment = 'inconclusive'
    return sentiment

def get_tweets(searchitem):
    # Input: searchitem (str)
    # Output: tweets (list)
    url = 'https://api.twitter.com/1.1/search/tweets.json?q=%23{}&result_type=recent'.format(searchitem)
    headers = {'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAAOWX9QAAAAAAHDplLmMG%2BcFK24Vr4mvELNXnZIA%3DoR2TI1D33PB7k9siZAF7xG1KM1ki7w6V1VVfpX9Y3rxsSZrTzC'}
    res = requests.get(url, headers=headers)

    # {'sentiment': 'asdlkjf', 'tweet': 'asdkljfs'}
    tweets = []


    for status in res.json()['statuses']:
        tweet_obj = {}
        tweet = status['text']
        sentiment = analyse(tweet)
        tweet_obj['tweet']= tweet
        tweet_obj['sentiment']=sentiment
        tweets.append(tweet_obj)
    return tweets

  
if __name__ == '__main__':
    app.run()