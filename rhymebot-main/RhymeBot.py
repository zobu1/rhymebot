import nltk
import pronouncing as pr
import random
nltk.download('universal_tagset')
nltk.download('brown')

import random
import nltk
import pronouncing as pr
nltk.download('universal_tagset')
nltk.download('brown')
from flask import Flask, render_template, request

app = Flask(__name__)

word_to_pos = nltk.ConditionalFreqDist((w.lower(), t)
        for w, t in nltk.corpus.brown.tagged_words(tagset="universal"))

word_to_pos = {k : max(dict(v), key=dict(v).get) for k, v in dict(word_to_pos).items()}
freqs = nltk.FreqDist([w.lower() for w in nltk.corpus.brown.words()])

def get_phones(sentence):
  phones = []
  for word in sentence.split():
    phones_in_words = pr.phones_for_word(word)
    if not phones_in_words:
      phones += []
      continue
    phones += [phones_in_words[0].split()]
  return phones

def get_pos(sentence):
  sentence = sentence.split()
  pos = []
  for word in sentence:
    word = word.lower()
    if not word in word_to_pos:
      pos.append("NOUN")
      continue
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
    # special case
    if word == "the": return ["the", "a"]
    if word == "are": return ["are"]
    search = []
    syllable_count = get_syllable_count(word)
    for i in range(len(phones) - 1, -1, -1):
        # if phones[i] in ['T', 'P']:
        #     phones[i] = "(T|P)"
        if phones[i] in ['G', 'B']:
            phones[i] = "(G|B)"
        if phones[i] in ['SH', 'S']:
            phones[i] = "(SH|S)"
        if phones[i] in ['AO1', 'AA1']:
            phones[i] = "(A01|AA1)"
        if phones[i] in ['M', 'N']:
            phones[i] = "(M|N)"

        search.insert(0, phones[i])
        search_str = " ".join(search) + "$"
        words = pr.search(search_str)
        # filter out pos and syllable count
        words = [w for w in words if word_to_pos.get(w, "") == pos and
                 get_syllable_count(w) == syllable_count]
        words = ["".join(dict.fromkeys(w)) for w in words]
        words = list(set(words))
        if len(words) <= 1:
            if i == len(phones) - 1:
                search.insert(0, "")
            search_str = " ".join(search[1:]) + "$"
            words = pr.search(search_str)
            words = [w for w in words if word_to_pos.get(w, "") == pos and get_syllable_count(w) == syllable_count]
            words = list(set(words))
            words_sorted = sorted(words, key=lambda x: freqs[x.lower()], reverse=True)
            return words_sorted
    words = list(set(words))
    words_sorted = sorted(words, key=lambda x: freqs[x.lower()], reverse=True)
    return words_sorted

def find_best_rhymes_2(phones, word, pos):
    # special case
    if word == "the": return ["the", "a"]
    if word == "are": return ["are"]
    search = []
    syllable_count = get_syllable_count(word)
        # if phones[i] in ['T', 'P']:
        #     phones[i] = "(T|P)"
    if len(phones) == 1: return find_best_rhymes(phones, word, pos)
    for i in range(-1, -3, -1):
        if phones[i] in ['G', 'B']:
            phones[i] = "(G|B)"
        if phones[i] in ['SH', 'S']:
            phones[i] = "(SH|S)"
        if phones[i] in ['AO1', 'AA1']:
            phones[i] = "(A01|AA1)"
        if phones[i] in ['M', 'N']:
            phones[i] = "(M|N)"

    total_words = set()
    for search_str in [f"{phones[-2]} {phones[-1]}$", f"{phones[-2]} ([^\s]+) {phones[-1]}$"]:
        words = pr.search(search_str)
        # filter out pos and syllable count
        words = [w for w in words if word_to_pos.get(w, "") == pos and
                                    get_syllable_count(w) == syllable_count]
        words = ["".join(dict.fromkeys(w)) for w in words]
        words = set(words)
        total_words = {*total_words, *words}
    total_words.add(word.lower())
    total_words = list(total_words)
    words_sorted = sorted(total_words, key=lambda x: freqs[x.lower()], reverse=True)
    return words_sorted

from string import punctuation
punctuation = "".join([c for c in punctuation if c != "'"])

def get_random_sentence_rhyme(sentence):
    for p in punctuation:
        sentence = sentence.replace(f"{p}", f" {p} ")
    sentence_split = sentence.split()
    phones = get_phones(sentence)
    pos = get_pos(sentence)
    rhymed_sentence = []
    for i in range(len(sentence.split())):
        try:
            rhymed_sentence.append(random.choice(find_best_rhymes_2(phones[i], sentence_split[i], pos[i])[:10]))
        except:
            if sentence_split[i] in punctuation:
                rhymed_sentence[-1] = rhymed_sentence[-1] + sentence_split[i]
            else:
                rhymed_sentence.append(sentence_split[i])
    rhymed_sentence = " ".join(rhymed_sentence)
    return rhymed_sentence

@app.route('/')
def index():
    print("hi")
    return render_template('index.html')

@app.route('/hello', methods=['POST'])
def hello():
    sentence = request.form["Enter a sentence"]


sentence = input("input a sentence: ")
output = get_random_sentence_rhyme(sentence)
print(output)