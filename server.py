from flask import Flask, request, send_from_directory
from flask_cors import CORS
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from urllib.request import urlopen

from question_generation import generate_questions
from youtube_questions import generate_questions_from_youtube
from linkgen import getLinks

app = Flask(__name__,  static_url_path='', static_folder='static')
CORS(app)


questions = []


@app.route('/')
def hello():
    return 'server active'

@app.route('/roadmap')
def roadmap_route():
  return send_from_directory('views', 'roadmap.html')

@app.route("/roadmap_info")
def linkGen():
  topic = request.args.get('topic')
  return(getLinks(topic))

@app.route('/generate_questions')
def generate_questions_route():
  global questions

  url = request.args.get("url")
  
  parsed_url = urlparse(url)
  if parsed_url.hostname == 'www.youtube.com':
    
    questions = generate_questions_from_youtube(url)
    return 'ok'
  
  elif parsed_url.hostname.startswith('http://127.0.0.1:5001/'):
     return 'unsupported', 400

  html = urlopen(url) 
  soup = BeautifulSoup(html, 'html.parser')
  text = ''.join([i.getText() for i in soup.findAll('p')])

  questions = generate_questions(text[:10240])

  return 'ok'

@app.route('/get_questions')
def get_questions():
  return {
    'questions': questions
  }


if __name__ == '__main__':
	app.run(port=5001)