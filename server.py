from flask import Flask
from flask_cors import CORS

from question_generation import generate_questions

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello():
    return 'server active'

f = open('notebooks/sample.txt', 'r')
t = f.read()

@app.route('/generate_questions/<link>')
def generate_questions_route(link):
  # f = open('notebooks/sample.txt', 'r')
  # t = f.read()
  # print(t)
  q = generate_questions(t)
  # print(q)
  print('lol')
  return  q

if __name__ == '__main__':
	app.run(debug=True, port=5001)