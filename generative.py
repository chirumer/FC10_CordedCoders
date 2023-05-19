from dotenv import load_dotenv
load_dotenv()


import os
import openai
openai.api_type = "azure"
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT") 
openai.api_version = "2023-03-15-preview"
openai.api_key = os.getenv("AZURE_OPENAI_KEY")

prompt_instruction = (
'''

Generate upto 5 MCQ questions of the format
Q) question 
1) option 
2) option 
3) option 
4) option 
A) correct option number

example of format:
Q) Who is husband of Mary?
1) John
2) Joseph
3) Mark
4) Anthony
A) 2

example of format:
Q) Who is daughter of John?
1) Elizabeth
2) Diana
3) Dorothy
4) Mary
A) 1'''
)

def generate_questions(response):
  def clean(t):
    return t[2:].strip()

  questions = []
  question = {}

  for i in response.split('\n'):
    #print(i)
    if i.startswith('Q'):
      if question:
        questions.append(question)
      question = {
          'question': clean(i),
          'choices': []
      }
    elif i.startswith('A'):
      print(i)
      print(clean(i))
      question['answer'] = int(clean(i)[0])-1
    elif i and i[0].isnumeric():
      question['choices'].append(clean(i))
  
  return questions

def form_questions_prompt(transcript):
  response = openai.ChatCompletion.create(
  engine = "gpt35_1",
  messages = [
      { "role": "system", "content": "You are a helpful assistant." },
      { "role": "user", "content": transcript + prompt_instruction },
    ]
  )
  return response['choices'][0]['message']['content']

# # sample chat completion:
# response = openai.ChatCompletion.create(
#     engine="chatgpt",
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant."},
#         {"role": "user", "content": "Does Azure OpenAI support customer managed keys?"},
#         {"role": "assistant", "content": "Yes, customer managed keys are supported by Azure OpenAI."},
#         {"role": "user", "content": "Do other Azure Cognitive Services support this too?"}
#     ]
# )