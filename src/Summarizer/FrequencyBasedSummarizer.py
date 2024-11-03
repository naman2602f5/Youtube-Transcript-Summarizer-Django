from src.Summarizer.BaseSummarizer import BaseSummarizer
import nltk
import heapq
import re
import string


class FrequencyBasedSummarizer(BaseSummarizer):
    def summarize(self, result, percent):
        formatted_text = self.extractive_preprocess(result)

        word_frequency = nltk.FreqDist(nltk.word_tokenize(formatted_text))

        highest_frequency = max(word_frequency.values())
        for word in word_frequency.keys():
            word_frequency[word] = (word_frequency[word] / highest_frequency)


        sentence_list = nltk.sent_tokenize(result)
        score_sentences = {}
        for sentence in sentence_list:
            for word in nltk.word_tokenize(sentence.lower()):
                if sentence not in score_sentences.keys():
                    score_sentences[sentence] = word_frequency[word]
                else:
                    score_sentences[sentence] += word_frequency[word]

        n = len(sentence_list)
        per = n * (int(percent) / 100)

        if int(per) == 0:
            per = 1

        best_sentences = heapq.nlargest(int(per), score_sentences, key=score_sentences.get)
        summary = ' '.join(best_sentences)
        return summary

    def extractive_preprocess(self, text):

        text = re.sub(r'\s+', ' ', text)

        # nltk.download('punkt')
        # nltk.download('stopwords')
        stopwords = nltk.corpus.stopwords.words('english')

        formatted_text = text.lower()
        tokens = []
        for token in nltk.word_tokenize(formatted_text):
            tokens.append(token)
        tokens = [word for word in tokens if word not in stopwords and word not in string.punctuation]
        formatted_text = ' '.join(element for element in tokens)

        return formatted_text