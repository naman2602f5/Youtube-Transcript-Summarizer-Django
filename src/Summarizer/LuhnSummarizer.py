from src.Summarizer.BaseSummarizer import BaseSummarizer
import nltk
import heapq
import re
import string


class LuhnSummarizer(BaseSummarizer):
    def summarize(self, text, percent, top_n_words=5, distance=2, number_of_sentences=3):
        percent = int(percent)/100
        original_sentences = [sentence for sentence in nltk.sent_tokenize(text)]

        formatted_sentences = [self.extractive_preprocess(original_sentence) for original_sentence in original_sentences]

        words = [word for sentence in formatted_sentences for word in nltk.word_tokenize(sentence)]

        frequency = nltk.FreqDist(words)
        top_n_words = [word[0] for word in frequency.most_common(top_n_words)]

        sentences_score = self.calculate_sentences_score(formatted_sentences, top_n_words, distance)
        if percent > 0:
            best_sentences = heapq.nlargest(int(len(formatted_sentences) * percent), sentences_score)
        else:
            best_sentences = heapq.nlargest(number_of_sentences, sentences_score)
        best_sentences = [original_sentences[i] for (score, i) in best_sentences]
        summary = ' '.join(best_sentences)
        return summary

    def extractive_preprocess(self, text):

        text = re.sub(r'\s+', ' ', text)

        stopwords = nltk.corpus.stopwords.words('english')

        formatted_text = text.lower()
        tokens = []
        for token in nltk.word_tokenize(formatted_text):
            tokens.append(token)
        tokens = [word for word in tokens if word not in stopwords and word not in string.punctuation]
        formatted_text = ' '.join(element for element in tokens)

        return formatted_text

    def calculate_sentences_score(self, sentences, important_words, distance):
        scores = []
        sentence_index = 0

        for sentence in [nltk.word_tokenize(sentence) for sentence in sentences]:


            word_index = []
            for word in important_words:
                try:
                    word_index.append(sentence.index(word))
                except ValueError:
                    pass

            word_index.sort()

            if len(word_index) == 0:
                continue

            groups_list = []
            group = [word_index[0]]
            i = 1  # 3
            while i < len(word_index):
                if word_index[i] - word_index[i - 1] < distance:
                    group.append(word_index[i])
                else:
                    groups_list.append(group[:])
                    group = [word_index[i]]
                i += 1
            groups_list.append(group)

            max_group_score = 0
            for g in groups_list:
                important_words_in_group = len(g)
                total_words_in_group = g[-1] - g[0] + 1
                score = 1.0 * important_words_in_group ** 2 / total_words_in_group

                if score > max_group_score:
                    max_group_score = score

            scores.append((max_group_score, sentence_index))
            sentence_index += 1

        return scores