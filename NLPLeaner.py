"""
Tokenization : Penn Treebank Tokenization
토큰화 : 주어진 corpus를 Token(단어, 혹은 형태소 등)의 단위로 잘라내는 작업
Grey bot에서는 Penn Treebank 에 의거한 토큰화를 실행함.
"""
import nltk
nltk.download('averaged_perceptron_tagger')


#Treebank tokenization을 위한 library
from nltk.tokenize import TreebankWordTokenizer
#sentence toknization을 위한 library
from nltk.tokenize import sent_tokenize
#품사의 구분을 위해 다음 library를 사용할 수 있음
from nltk.tag import pos_tag

tokenizer=TreebankWordTokenizer()
text="Starting a home-based restaurant may be an ideal. it doesn't have a food chain or restaurant of their own."
print(type(text))
toktext = tokenizer.tokenize(text)
post_text = pos_tag(toktext)
print(toktext)
print(type(toktext))

