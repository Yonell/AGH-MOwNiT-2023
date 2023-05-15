import xml.etree.ElementTree as ET
import multiprocessing as mp
import numpy as np
import scipy as sp
import math
import pickle


class PoorWikipedia():
    titles = None
    texts = None
    all_words = None
    frequencies = None
    database_path = None
    feature_matrix = None

    def __init__(self, database_path):
        self.database_path = database_path
        if self.database_path[-1] == '/':
            self.database_path = self.database_path[:-1]
        pass

    def get_titles_and_texts_from_xml(self, filename):
        tree = ET.parse(self.database_path + "/" + filename)
        root = tree.getroot()
        titles = []
        texts = []
        title_to_append = None
        text_to_append = None
        for child in root:
            for subchild in child:
                # print(subchild.tag, subchild.attrib)
                if (subchild.tag == '{http://www.mediawiki.org/xml/export-0.10/}title'):
                    title_to_append = subchild.text
                if (subchild.tag == '{http://www.mediawiki.org/xml/export-0.10/}revision'):
                    for subsubchild in subchild:
                        if (subsubchild.tag == '{http://www.mediawiki.org/xml/export-0.10/}text'):
                            if (subsubchild.text is not None):
                                if len(subsubchild.text) >= 1000:
                                    titles.append(title_to_append)
                                    texts.append(subsubchild.text)

        self.titles = titles
        self.texts = texts

    def get_titles_and_texts_from_pickle(self):
        with open(self.database_path + "/titles.pickle", 'rb') as f:
            self.titles = pickle.load(f)
            f.close()
        with open(self.database_path + "/texts.pickle", 'rb') as f:
            self.texts = pickle.load(f)
            f.close()

    def process_word(self, word, permitted_symbols):
        words = []
        word = word.lower()
        for i, symbol in enumerate(word):
            if symbol in permitted_symbols:
                continue
            else:
                word = word.replace(symbol, ' ')
        words = word.split()
        return words

    def get_all_words(self, titles, texts):
        word_frequency = dict()
        permitted_symbols = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        i = 0
        for text in texts:
            if i % 1024 == 0:
                print(i)
            if text is None:
                continue
            for word in text.split():
                for actual_word in self.process_word(word, permitted_symbols):
                    if actual_word in word_frequency:
                        word_frequency[actual_word] += 1
                    else:
                        word_frequency[actual_word] = 1
            i += 1
        i = 0
        for title in titles:
            if i % 1024 == 0:
                print(i)
            if title is None:
                continue
            for word in title.split():
                for actual_word in self.process_word(word, permitted_symbols):
                    if actual_word in word_frequency:
                        word_frequency[actual_word] += 1
                    else:
                        word_frequency[actual_word] = 1
            i += 1
        result1, result2 = list(word_frequency.keys()), [word_frequency[i] for i in word_frequency.keys()]
        sorted_result = sorted(zip(result1, result2), key=lambda x: x[1], reverse=True)
        self.all_words, self.frequencies = [i[0] for i in sorted_result], [i[1] for i in sorted_result]
        return

    def save_words_and_frequencies(self, all_words, frequencies, filename):
        with open(self.database_path + "/" + filename, 'w') as f:
            for i in range(len(all_words)):
                f.write(all_words[i] + ' ' + str(frequencies[i]) + '\n')
        return

    def process_bag_of_words(self, max_words=10000):
        i = 0
        while i < len(self.all_words):
            if len(self.all_words[i]) < 3:
                self.all_words.pop(i)
                self.frequencies.pop(i)
            else:
                i += 1
        self.all_words = self.all_words[43:max_words]
        self.frequencies = self.frequencies[43:max_words]
        return

    def create_feature_vector(self, title, text):
        feature_vector = np.zeros(len(self.all_words))
        permitted_symbols = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        for word in title.split():
            for actual_word in self.process_word(word, permitted_symbols):
                if actual_word in self.all_words:
                    feature_vector[self.all_words.index(actual_word)] += 1
        for word in text.split():
            for actual_word in self.process_word(word, permitted_symbols):
                if actual_word in self.all_words:
                    feature_vector[self.all_words.index(actual_word)] += 1
        return feature_vector

    def create_feature_matrix(self):
        pool = mp.Pool(mp.cpu_count() - 1)
        results = [
            pool.apply_async(self.create_feature_vector, args=(self.all_words, self.titles[i], self.texts[i])) for i
            in
            range(len(self.titles))]
        j = 0
        for i in results:
            if j % 1024 == 0:
                print(j)
            i.wait()
            j += 1
        self.feature_matrix = np.array([i.get() for i in results])
        self.feature_matrix = self.feature_matrix.T
        self.feature_matrix = sp.sparse.coo_matrix(self.feature_matrix)
        return

    def multiply_by_idf(self):
        self.feature_matrix = self.feature_matrix.tocsr()
        word_in_document = self.feature_matrix.sum(axis=1)
        idf = sp.sparse.csr_array([math.log(self.feature_matrix.shape[1] / i) for i in word_in_document]).T
        self.feature_matrix = self.feature_matrix.multiply(idf)
        return

    def create_normalized_bag_of_words_from_array_of_strings(self, array_of_strings):
        result_vector = sp.sparse.csr_matrix([0] * len(self.all_words))
        for i in array_of_strings:
            if i in self.all_words:
                result_vector[0, self.all_words.index(i)] += 1
        result_vector = result_vector / np.linalg.norm(result_vector.toarray())
        return result_vector

    def create_correlation_vector(self, slowa):
        self.feature_matrix = self.feature_matrix.tocsr()
        correlation_vector = slowa * self.feature_matrix
        correlation_vector = (correlation_vector / np.linalg.norm(slowa.toarray()))
        correlation_vector /= sp.sparse.linalg.norm(self.feature_matrix, axis=0)
        return correlation_vector

    def return_k_best_articles_indexies(self, correlation_vector, k):
        return np.argsort(correlation_vector)[0, -k:].tolist()[0]

    def return_k_best_articles(self, string_arg, k):
        array_of_strings = string_arg.split()
        slowa = self.create_normalized_bag_of_words_from_array_of_strings(array_of_strings)
        correlation_vector = self.create_correlation_vector(slowa)
        return [self.titles[i] for i in self.return_k_best_articles_indexies(correlation_vector, k)]

    def return_k_best_articles_with_text(self, string_arg, k):
        if self.texts is None:
            raise Exception("Texts are not loaded")
        if self.titles is None:
            raise Exception("Titles are not loaded")
        if self.all_words is None:
            raise Exception("Words are not loaded")
        if self.frequencies is None:
            raise Exception("Frequencies are not loaded")
        if self.feature_matrix is None:
            raise Exception("Feature matrix is not loaded")
        if self.database_path is None:
            raise Exception("Database path is not loaded")
        array_of_strings = string_arg.split()
        slowa = self.create_normalized_bag_of_words_from_array_of_strings(array_of_strings)
        correlation_vector = self.create_correlation_vector(slowa)
        return [(self.titles[i], self.texts[i]) for i in self.return_k_best_articles_indexies(correlation_vector, k)]

    def save_feature_matrix(self, filename):
        sp.sparse.save_npz(self.database_path + "/" + filename, self.feature_matrix, compressed=True)
        return

    def load_feature_matrix(self, filename):
        self.feature_matrix = sp.sparse.load_npz(self.database_path + "/" + filename)
        return

    def save_all_words_with_frequencies(self, filename):
        with open(self.database_path + "/" + filename, 'w') as f:
            for i in range(len(self.all_words)):
                f.write(self.all_words[i] + ' ' + str(self.frequencies[i]) + '\n')
        return

    def load_all_words_with_frequencies(self, filename):
        list1 = []
        list2 = []
        with open(self.database_path + "/" + filename, 'r') as f:
            for line in f:
                word1, word2 = line.split()
                list1.append(word1)
                list2.append(int(word2))
        self.all_words = list1
        self.frequencies = list2
        return

    def low_rank_approximation(self, k):
        u, s, v = sp.sparse.linalg.svds(self.feature_matrix, k=k)
        u = sp.sparse.csr_matrix(u)
        s = sp.sparse.diags(s)
        v = sp.sparse.csr_matrix(v)
        self.feature_matrix = u@s@v

        return
