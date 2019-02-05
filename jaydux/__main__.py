import logging
import flask
import requests
import pprint
import os
from .frontpage import render
app = flask.Flask(__name__)


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("jaydux")
[
    logging.getLogger(i).setLevel(logging.WARNING) 
    for i in logging.root.manager.loggerDict.keys()
    if not i == "jaydux"
]

def article(doc):
    title = doc.get("twitter.title","")
    title = title or doc.get("og.title","")
    title = title or doc.get("article.title","")
    title = title or doc.get("fb.title","")
    text = doc.get("twitter.text.title","")
    text = text or doc.get("twitter.description","")
    text = text or doc.get("og.description","")
    text = text or doc.get("article.text","")
    text = text or doc.get("fb.description","")
    img = doc.get("twitter.image","")
    img = img or doc.get("og.image","")
    img = img or doc.get("article.image","")
    img = img or doc.get("fb.image","")
    url = doc.get("twitter.url","")
    url = url or doc.get("og.url","")
    url = url or doc.get("article.url","")
    url = url or doc.get("fb.url","")
    netloc = doc.get("source.netloc")
    return {
        "title": title[0] if isinstance(title, list) else title,
        "img": img[0] if isinstance(img, list) else img,
        "netloc": netloc[0] if isinstance(netloc, list) else netloc,
        "text": " ".join(text) if isinstance(text, list) else text,
        "url": url[0] if isinstance(url, list) else url,
    }

def search(**params):
    params["fl"]=["twitter.*","og.*","source.*", "when.*", "fb.*"]
    params["fq"]=["source.path:*", "when.date:NOW/DAY"]
    response = requests.get(os.environ["SOLRURL"] + "/solr/text/select", params=params)
    result = response.json()
    # cheaper pop from backend
    return list(reversed([article(d) for d in result["response"]["docs"]]))

@app.route("/")
def hello():
    text = flask.request.args.get("q","*")
    return render(search(q=f"text:{text}", rows=800))

if __name__ == '__main__':
    logger.info("starting")
    app.run(host=os.environ["FLASK_HOST"])
    logger.info("stopping")




