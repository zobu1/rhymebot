__author__ = 'kai'


import random
import nltk
import pronouncing as pr
nltk.download('universal_tagset')
nltk.download('brown')
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hello', methods=['POST'])

word_to_pos = nltk.ConditionalFreqDist((w.lower(), t) for w, t in nltk.corpus.brown.tagged_words(tagset="universal"))

word_to_pos = {k : max(dict(v), key=dict(v).get) for k, v in dict(word_to_pos).items()}

freqs = nltk.FreqDist([w.lower() for w in nltk.corpus.brown.words()])

def get_phones(sentence):
  phones = []
  for word in sentence.split():
    phones_in_words = pr.phones_for_word(word)
    if not phones_in_words: return f"Unkown word: {word}"
    phones += [phones_in_words[0].split()]
  return phones

def get_pos(sentence):
  sentence = sentence.split()
  pos = []
  for word in sentence:
    word = word.lower()
    if not word in word_to_pos:
      return []
    pos.append(word_to_pos[word])
  return pos

def get_rhymes(search, pos):
  rhymes = set()
  for word in pr.search(search):
    word_pos = get_pos(word)
    if not word_pos:
      continue
    if word_pos[0] == pos:
      rhymes.add(word)
  return rhymes

def get_syllable_count(word):
  pronunciation_list = pr.phones_for_word(word)
  return pr.syllable_count(pronunciation_list[0])

def find_best_rhymes(phones, word, pos):
    search = []
    syllable_count = get_syllable_count(word)
    for i in range(len(phones)-1, -1, -1):
        search.insert(0, phones[i])
        search_str = " ".join(search) + "$"
        words = pr.search(search_str)
        # filter out pos and syllable count
        words = [w for w in words if word_to_pos.get(w, "") == pos and
                                    get_syllable_count(w) == syllable_count and
                                    freqs.get(w, "") != ""]
        if len(words) <= 2:
            words = pr.search(" ".join(search[1:]))
            words = [w for w in words if word_to_pos.get(w, "") == pos and get_syllable_count(w) == syllable_count]
            words = list(set(words))
            words_sorted = sorted(words, key=lambda x: freqs[x.lower()], reverse=True)
            return words_sorted

sentence = input("Please enter a Sentence \n")
sentence_split = sentence.split()
phones = get_phones(sentence)
pos = get_pos(sentence)
rhymed_sentence = []
for i in range(len(sentence.split())):
    try:
        rhymed_sentence.append(random.choice(find_best_rhymes(phones[i], sentence_split[i], pos[i])[:10]))
    except:
        rhymed_sentence.append(sentence_split[i])
rhymed_sentence = " ".join(rhymed_sentence)
print(rhymed_sentence)


if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 3000)
