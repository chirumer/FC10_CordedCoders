from flask import Flask, request
from flask_cors import CORS
from urllib.parse import urlparse
from question_generation import generate_questions
from bs4 import BeautifulSoup
from urllib.request import urlopen

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello():
    return 'server active'

@app.route('/generate_questions')
def generate_questions_route():

  url = request.args.get("url")

  print(url)
  html = urlopen(url) 
  soup = BeautifulSoup(html, 'html.parser')
  text = ''.join([i.getText() for i in soup.findAll('p')])

  return generate_questions(text[:10240])


if __name__ == '__main__':
	app.run(port=5001)