import PoorWikipedia

pw = PoorWikipedia.PoorWikipedia('simplewiki')
print("Getting titles and texts...")
pw.get_titles_and_texts('simplewiki-20230401-pages-articles-multistream.xml')
print("Getting all words...")
pw.load_all_words_with_frequencies('processed_words_with_frequencies.txt')
print("Creating term-document matrix...")
pw.load_feature_matrix('term_document_matrix_idf.npz')
print("Creating normalized bag of words...")
input_str = input()
while input_str != 'q':
    for i in pw.return_k_best_articles_with_text(input_str, 10):
        print(i[0])
        print(i[1])
        print('-----------------'*4)
        print()
    input_str = input()