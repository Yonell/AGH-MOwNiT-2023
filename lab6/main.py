import xml.etree.ElementTree as ET
from ctypes import Array
import multiprocessing as mp
import numpy as np
import scipy as sp
import math
import pickle
import PoorWikipedia


if __name__ == '__main__':
    pw = PoorWikipedia.PoorWikipedia('simplewiki')
    print("Getting titles and texts...")
    pw.get_titles_and_texts_from_pickle()
    print("Getting all words...")
    pw.load_all_words_with_frequencies('processed_words_with_frequencies.txt')
    print("Creating term-document matrix...")
    pw.load_feature_matrix('term_document_matrix_idf.npz')
    pw.feature_matrix.eliminate_zeros()
    print("Low rank approximation...")
    pw.low_rank_approximation(9950)
    print("Saving low rank approximation...")
    pw.save_feature_matrix('term_document_matrix_lra9950.npz')
    print("Creating normalized bag of words...")
    input_str = input()
    while input_str != 'q':
        for i in pw.return_k_best_articles_with_text(input_str, 10):
            print(i[0])
            print(i[1])
            print('-----------------' * 4)
            print()
        input_str = input()
