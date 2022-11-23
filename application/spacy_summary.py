import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from bs4 import BeautifulSoup as soup
import requests

nlp = spacy.load('en_core_web_sm')
punctuation += '\n'


def calculate_reading_time(text):
    doc = nlp(text)
    tokens = [token.text for token in doc]
    total_words = len(tokens)
    reading_time = total_words / 110.0
    return "{:.2f}".format(reading_time)


def get_headline_text(url):
    html = requests.get(url)
    bsobj = soup(html.text, 'html.parser')
    headline = bsobj.title.text
    text = ' '.join(map(lambda p: p.text, bsobj.findAll('p')))

    if(len(text) == 0 or len(headline) == 0):
        raise Exception('No Text is found in the provided URL')
    return headline, text


def spacy_summary(headline, text):
    stopwords = list(STOP_WORDS)
    doc = nlp(text)
    head = nlp(headline)
    tokens = [token.text for token in doc]
    head_tokens = [htoken.text for htoken in head]
    head_frequencies = {}
    word_frequencies = {}
    for word in head:
        if word.text.lower() not in stopwords:
            if word.text.lower() not in punctuation:
                if word.text.lower() not in word_frequencies.keys():
                    if word.text not in word_frequencies.keys():
                        head_frequencies[word.text] = 1
                    else:
                        head_frequencies[word.text] += 1
    for word in doc:
        if word.text.lower() not in stopwords:
            if word.text.lower() not in punctuation:
                if word.text.lower() not in word_frequencies.keys():
                    if word.text in head_frequencies.keys():
                        if word.text not in word_frequencies.keys():
                            word_frequencies[word.text] = 10
                        else:
                            word_frequencies[word.text] += 10
                    else:
                        if word.text not in word_frequencies.keys():
                            word_frequencies[word.text] = 1
                        else:
                            word_frequencies[word.text] += 1
    max_frequency = max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word] = word_frequencies[word] / max_frequency
    sentence_tokens = [sent for sent in doc.sents]
    sentence_score = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_score.keys():
                    sentence_score[sent] = word_frequencies[word.text.lower()]
                else:
                    sentence_score[sent] += word_frequencies[word.text.lower()]
    sentence_scores_list = []
    for sent in sentence_score:
        sentence_scores_list.append(sentence_score[sent])
    # sentence_scores_list
    sentence_scores_list.sort(reverse=True)
    sentence_scores_list
    desired_summarized_text_persentage = 0.20
    select_length = int(len(sentence_tokens) * desired_summarized_text_persentage)
    del sentence_scores_list[select_length:]
    summary = []
    for sent in sentence_score:
        if sentence_score[sent] in sentence_scores_list:
            summary.append(sent)
            sentence_scores_list.remove(sentence_score[sent])
    final_summary = ''
    for sent in summary:
        final_summary += sent.text + ' '
    return final_summary
