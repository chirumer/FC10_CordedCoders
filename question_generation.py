from summarizer import Summarizer
from transformers import logging, AutoConfig, AutoTokenizer, AutoModel
import nltk
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('punkt')
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
import pke
import string
from flashtext import KeywordProcessor
import requests
import re
import random
from pywsd.similarity import max_similarity
from pywsd.lesk import adapted_lesk
from pywsd.lesk import simple_lesk
from pywsd.lesk import cosine_lesk


custom_config = AutoConfig.from_pretrained('mrm8488/bert-tiny-finetuned-squadv2')
custom_config.output_hidden_states=True
custom_tokenizer = AutoTokenizer.from_pretrained('mrm8488/bert-tiny-finetuned-squadv2')
custom_model = AutoModel.from_pretrained('mrm8488/bert-tiny-finetuned-squadv2', config=custom_config)

summarizer_model = Summarizer(custom_model=custom_model, custom_tokenizer=custom_tokenizer)


def get_nouns(text, X=20):
  text = text.lower()
  
  extractor = pke.unsupervised.MultipartiteRank()
  stoplist = list(string.punctuation)
  stoplist += ['-lrb-', '-rrb-', '-lcb-', '-rcb-', '-lsb-', '-rsb-']
  stoplist += stopwords.words('english')
  extractor.load_document(input=text, stoplist=stoplist)

  pos = {'PROPN'}

  extractor.candidate_selection(pos=pos)
  extractor.candidate_weighting(alpha=1.1,
                                  threshold=0.75,
                                  method='average')
  nouns = [i[0] for i in extractor.get_n_best(X) if i[0] in text]

  return nouns

def tokenize_sentences(text):
    sentences = [sent_tokenize(text)]
    sentences = [y for x in sentences for y in x]
    sentences = [sentence.strip() for sentence in sentences if 20 < len(sentence) < 300]
    return sentences

def get_sentences_for_keyword(keywords, sentences):
    keyword_processor = KeywordProcessor()
    keyword_sentences = {}
    for word in keywords:
        keyword_sentences[word] = []
        keyword_processor.add_keyword(word)
    for sentence in sentences:
        keywords_found = keyword_processor.extract_keywords(sentence)
        for key in keywords_found:
            keyword_sentences[key].append(sentence)
    for key in keyword_sentences.keys():
        values = keyword_sentences[key]
        values = sorted(values, key=len, reverse=True)
        keyword_sentences[key] = values
    return keyword_sentences

def unique_keys(keyword_sentence_mapping):
  sent_set = set()
  for key in keyword_sentence_mapping.keys():
    remove_list = []
    for sent in keyword_sentence_mapping[key]:
      if sent not in sent_set:
        sent_set.add(sent)
      else:
        remove_list.append(sent)
    for sent in remove_list:
      keyword_sentence_mapping[key].remove(sent)
  return keyword_sentence_mapping

def get_unique_sentence_mapping(summarized_text):

  sentences = tokenize_sentences(summarized_text)
  keyword_sentence_mapping = get_sentences_for_keyword(get_nouns(summarized_text), sentences)
  keyword_sentence_mapping = unique_keys(keyword_sentence_mapping)
  
  keyword_sentence_mapping = {k: v for k, v in keyword_sentence_mapping.items() if v}
  return keyword_sentence_mapping

def get_distractors_wordnet(syn,word):
    distractors=[]
    word= word.lower()
    orig_word = word
    if len(word.split())>0:
        word = word.replace(" ","_")
    hypernym = syn.hypernyms()
    if len(hypernym) == 0: 
        return distractors
    for item in hypernym[0].hyponyms():
        name = item.lemmas()[0].name()

        if name == orig_word:
            continue
        name = name.replace("_"," ")
        name = " ".join(w.capitalize() for w in name.split())
        if name is not None and name not in distractors:
            distractors.append(name)
    return distractors

def get_wordsense(sent,word):
    word= word.lower()
    
    if len(word.split())>0:
        word = word.replace(" ","_")
    
    
    synsets = wn.synsets(word,'n')
    if synsets:
        wup = max_similarity(sent, word, 'wup', pos='n')
        adapted_lesk_output =  adapted_lesk(sent, word, pos='n')
        lowest_index = min (synsets.index(wup),synsets.index(adapted_lesk_output))
        return synsets[lowest_index]
    else:
        return None

def get_distractors_conceptnet(word):
    word = word.lower()
    original_word= word
    if (len(word.split())>0):
        word = word.replace(" ","_")
    distractor_list = [] 
    url = "http://api.conceptnet.io/query?node=/c/en/%s/n&rel=/r/PartOf&start=/c/en/%s&limit=5"%(word,word)
    obj = requests.get(url).json()

    for edge in obj['edges']:
        link = edge['end']['term'] 

        url2 = "http://api.conceptnet.io/query?node=%s&rel=/r/PartOf&end=%s&limit=10"%(link,link)
        obj2 = requests.get(url2).json()
        for edge in obj2['edges']:
            word2 = edge['start']['label']
            if word2 not in distractor_list and original_word.lower() not in word2.lower():
                distractor_list.append(word2)
                   
    return distractor_list

def generate_questions(full_text):
  result = summarizer_model(full_text, min_length=60, max_length = 500 , ratio = 0.4)
  summarized_text = ''.join(result)

  keyword_sentence_mapping = get_unique_sentence_mapping(summarized_text)

  key_distractor_list = {}
  
  questions = []

  for keyword in keyword_sentence_mapping:
    wordsense = get_wordsense(keyword_sentence_mapping[keyword][0],keyword)
    if wordsense:
      distractors = get_distractors_wordnet(wordsense,keyword)
      if len(distractors) ==0:
        distractors = get_distractors_conceptnet(keyword)
      if len(distractors) != 0:
        key_distractor_list[keyword] = distractors
    else:
      distractors = get_distractors_conceptnet(keyword)
      if len(distractors) != 0:
        key_distractor_list[keyword] = distractors


  for each in key_distractor_list:
    question = {}

    sentence = keyword_sentence_mapping[each][0]
    pattern = re.compile(each, re.IGNORECASE)
    output = pattern.sub( " _______ ", sentence)
    question["question"] = output

    choices = [each.capitalize()] + key_distractor_list[each]
    top4choices = choices[:4]
    random.shuffle(top4choices)
    question["choices"] = top4choices
    question["answer"] = top4choices.index(each.capitalize())

    questions.append(question)
  
  return questions