from flask import Flask, request
from flask_cors import CORS
from urllib.parse import urlparse

from wikipedia_questions import questions_from_wiki_page

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello():
    return 'server active'

f = open('notebooks/sample.txt', 'r')
t = f.read()

@app.route('/generate_questions')
def generate_questions_route():

  url = urlparse(request.args.get("url"))

  if url.hostname.endswith('wikipedia.org'):
    return questions_from_wiki_page(url)

  return 'unsupported'


if __name__ == '__main__':
	app.run(port=5001)