from summarizer import Summarizer
from summarizer.sbert import SBertSummarizer

#create an instance of the SBERT
model = SBertSummarizer('paraphrase-MiniLM-L6-v2')


def sbert_summary(text):
    return model(text, num_sentences=2)
