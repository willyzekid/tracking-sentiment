import requests
import xml.etree.ElementTree as ET
import json
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

newslist_url = "https://news.google.com/rss/search?q=contact+tracing&hl=fr&gl=FR&ceid=FR:fr"
api = "https://api.diffbot.com/v3/article"
params = {
    "token" : "...",
    "discussion" : "false",
}

# Get list of articles
r = requests.get(newslist_url)
root = ET.fromstring(r.text)

# Run sentiment analysis (google handles FR / diffbot doesn't)
client = language.LanguageServiceClient()
for item in root.findall('channel/item'):
    params['url'] = item.find('link').text
    r = requests.get(api,params=params)
    data = json.loads(r.text)
    article = data['objects'][0]['title'] + '\n' + data['objects'][0]['text']

    document = types.Document(content=article, language='fr', type=enums.Document.Type.HTML)
    sentiment = client.analyze_sentiment(document=document, encoding_type='UTF8').document_sentiment
    print(data['objects'][0]['title'])
    print("Sentiment: {}, {}".format(sentiment.score, sentiment.magnitude))