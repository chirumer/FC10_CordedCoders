#mindmap-gen

import os
import openai
import json

from dotenv import load_dotenv
load_dotenv()

openai.api_type = "azure"
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT") 
openai.api_version = "2023-03-15-preview"
openai.api_key = os.getenv("AZURE_OPENAI_KEY")

def generate_questions(topic):
    pr = """
    create a roadmap of youtube videos along with links to learn %s
    in a json format
    example 
    {'difficulty':[
    {'title':title, 'video link':video link}]}
    """ % topic
    response = openai.ChatCompletion.create(
    engine="gpt35_1", # engine = "deployment_name".
    messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": pr},
        ]
    )
    return(response['choices'][0]['message']['content'])

def removenoise(parseddata):
    newparse = parseddata[parseddata.find("{"):(len(parseddata)-parseddata[::-1].find('}'))]
    newparse = json.loads(newparse)

    return newparse

def getLinks(topic):
  rawjson = generate_questions(topic)
  rawjson = removenoise(rawjson)
  return rawjson