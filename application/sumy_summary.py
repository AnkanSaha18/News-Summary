import sumy
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer


def sumy_summary(text):
    parser = PlaintextParser.from_string(text,Tokenizer("english"))
    lex_summarizer = LexRankSummarizer()
    summary = lex_summarizer(parser.document,3)
    summary_list = [str(sentence) for sentence in summary]
    final_summary = ' '.join(summary_list)
    return final_summary

print(sumy_summary("A teacher, also called a schoolteacher or formally an educator, is a person who helps students to acquire knowledge, competence, or virtue. Informally the role of teacher may be taken on by anyone (e.g.when showing a colleague how to perform a specific task). In some countries, teaching young people of school age may be carried out in an informal setting, such as within the family (homeschooling), rather than in a formal setting such as a school or college. Some other professions may involve a significant amount of teaching (e.g. youth worker, pastor).In most countries, formal teaching of students is usually carried out by paid professional teachers. This article focuses on those who are employed, as their main role, to teach others in a formal education context, such as at a school or other place of initial formal education or training."))