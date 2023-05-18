from transformers import *

# Load model, model config and tokenizer via Transformers
custom_config = AutoConfig.from_pretrained('mrm8488/bert-tiny-finetuned-squadv2')
custom_config.output_hidden_states=True
custom_tokenizer = AutoTokenizer.from_pretrained('mrm8488/bert-tiny-finetuned-squadv2')
custom_model = AutoModel.from_pretrained('mrm8488/bert-tiny-finetuned-squadv2', config=custom_config)

from summarizer import Summarizer

bert_tiny_model = Summarizer(custom_model=custom_model, custom_tokenizer=custom_tokenizer)

a = bert_tiny_model(open("sample.txt","r").read())

print(a)