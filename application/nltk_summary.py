import nltk
# nltk.download()
# nltk.download('all')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from string import punctuation

punctuation += '\n'


def nltk_summary(headline, text):
    stopWords = set(stopwords.words("english"))
    head = nltk.word_tokenize(headline)
    doc = nltk.word_tokenize(text)
    head_frequencies = {}
    word_frequencies = {}
    for word in head:
        if word not in stopWords:
            if word not in punctuation:
                if word not in word_frequencies.keys():
                    if word not in word_frequencies.keys():
                        head_frequencies[word] = 1
                    else:
                        head_frequencies[word] += 1
    for word in doc:
        if word not in stopWords:
            if word not in punctuation:
                if word not in word_frequencies.keys():
                    if word in head_frequencies.keys():
                        if word not in word_frequencies.keys():
                            word_frequencies[word] = 10
                        else:
                            word_frequencies[word] += 10
                    else:
                        if word not in word_frequencies.keys():
                            word_frequencies[word] = 1
                        else:
                            word_frequencies[word] += 1
    max_frequency = max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word] = word_frequencies[word] / max_frequency
    sentence_tokens = nltk.sent_tokenize(text)
    sentence_score = {}
    for sent in sentence_tokens:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if sent not in sentence_score.keys():
                    sentence_score[sent] = word_frequencies[word]
                else:
                    sentence_score[sent] += word_frequencies[word]
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
        final_summary += sent + ' '
    return final_summary



print(nltk_summary("headline", "A teacher, also called a schoolteacher or formally an educator, is a person who helps students to acquire knowledge, competence, or virtue. Informally the role of teacher may be taken on by anyone (e.g.when showing a colleague how to perform a specific task). In some countries, teaching young people of school age may be carried out in an informal setting, such as within the family (homeschooling), rather than in a formal setting such as a school or college. Some other professions may involve a significant amount of teaching (e.g. youth worker, pastor).In most countries, formal teaching of students is usually carried out by paid professional teachers. This article focuses on those who are employed, as their main role, to teach others in a formal education context, such as at a school or other place of initial formal education or training."));

