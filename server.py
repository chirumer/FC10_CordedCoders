from flask import Flask, request
from flask_cors import CORS
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from urllib.request import urlopen

from question_generation import generate_questions
from youtube_generation import generate_questions_from_youtube

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello():
    return 'server active'

@app.route('/generate_questions')
def generate_questions_route():

  url = request.args.get("url")

  parsed_url = urlparse(url)
  if parsed_url.hostname == 'www.youtube.com':
    return generate_questions_from_youtube(url)

  html = urlopen(url) 
  soup = BeautifulSoup(html, 'html.parser')
  text = ''.join([i.getText() for i in soup.findAll('p')])

  return generate_questions(text[:10240])


if __name__ == '__main__':
	app.run(port=5001)