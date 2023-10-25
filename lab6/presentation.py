import PoorWikipedia
import time

start = time.time()
searcher = PoorWikipedia.PoorWikipedia('simplewiki')
searcher.get_titles_and_texts_from_pickle()
searcher.load_all_words_with_frequencies('processed_words_with_frequencies.txt')
searcher.load_feature_matrix('term_document_matrix_idf.npz')
end = time.time()

print("Program loaded! Time elapsed:", end - start)

print("Enter your query:", end=' ')
input_str = input()

while input_str != 'q':
    start = time.time()
    for i in searcher.return_k_best_articles_with_text(input_str, 10):
        print(i[0])
        print(i[1])
        print('-----------------'*4)
        print()
    end = time.time()
    print("Time elapsed:", end - start)
    input_str = input()