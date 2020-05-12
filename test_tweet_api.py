import urllib
from requests_oauthlib import OAuth1
import requests
import sys
import pandas as pd


def search_tweets(CK, CKS, AT, ATS, word, count, n):
    # 文字列設定
    word += ' exclude:retweets' # RTは除く
    word = urllib.parse.quote_plus(word)
    # リクエスト
    url = "https://api.twitter.com/1.1/search/tweets.json?lang=ja&q="+word+"&count="+str(count)
    auth = OAuth1(CK, CKS, AT, ATS)
    response = requests.get(url, auth=auth)
    data = response.json()['statuses']

    cnt = 0
    tweets = []
    while True:
        if len(data) == 0:
            break
        cnt += 1
        if cnt > n:
            break
        for tweet in data:
            maxid = int(tweet["id"]) - 1
            tweet = {
                "id": tweet["id"],
                "created_at": tweet["created_at"],
                "user": tweet["user"]["name"],
                "user_description": tweet["user"]["description"],
                "text": tweet["text"],
                "retweet_count": tweet["retweet_count"]
                }
            tweets.append(tweet)
        # 2回目以降のリクエスト
        url = "https://api.twitter.com/1.1/search/tweets.json?lang=ja&q="+word+"&count="+str(count)+"&max_id="+str(maxid)
        response = requests.get(url, auth=auth)
        try:
            data = response.json()['statuses']
        except KeyError: # リクエスト回数が上限に達した場合のデータのエラー処理
            print('上限まで検索しました')
            break
    return tweets


def main():
    
    # APIの秘密鍵
    CK = 'XXXX' # コンシューマーキー
    CKS = 'XXXX' # コンシューマーシークレット
    AT = 'XXXX' # アクセストークン
    ATS = 'XXXX' # アクセストークンシークレット

    # 検索時のパラメーター
    word = 'AI' # 検索ワード
    count = 100 # 一回あたりの検索数(最大100/デフォルトは15)
    n = 5 # 検索回数の上限値(最大180/15分でリセット)

    # ツイート検索・テキストの抽出
    tweets = search_tweets(CK, CKS, AT, ATS, word, count, n)
    tweets = pd.DataFrame(tweets)
    tweets.to_csv("./tweets.csv", encoding="utf-8-sig")

if __name__ == '__main__':
    main()
