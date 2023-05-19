import wikipedia
from urllib.parse import urlparse
from question_generation import generate_questions

def questions_from_wiki_page(url):
  print(url) 
  
  wiki_id = url.path.split('/')[-1]
  text_content = wikipedia.page(wiki_id).content

  return generate_questions(text_content)