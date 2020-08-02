
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize



def preprocess(content):
    """
    Preprocesses the text (tokenization, case normalization, stemming, stopword removal)
    :param content:
    :return: prepocessed content
    """
    words_tokenized = word_tokenize(content)

    normalized_words = [w.lower() for w in words_tokenized]

    stop_words = set(stopwords.words('english'))
    filtered = [w for w in normalized_words if w not in stop_words]

    ps = PorterStemmer()
    stemmed_words = [ps.stem(w) for w in filtered]
    
    word_list = [word for word in stemmed_words]

    return word_list

def normalize_and_stem(term):
    """
    Preprocesses the term from the vocabulary
    :param term:
    :return: preprocessed term from the search vocabulary
    """
    term = term.lower()
    ps = PorterStemmer()
    term = ps.stem(term)
    return term

arr = []
def load_larc_vocab():
    
    vocab_file = open("LARC_vocab.txt", "r")
    for line in vocab_file:
        line = line.strip("\n")
        line = str(line)
        arr.append(line)

load_larc_vocab()

def check_unigrams_and_bigrams(content):
    """
    Check for the presence of Unigrams and Bigrams from the vocabulary in the content
    :param content:
    :return:
    """
    preprocessed = preprocess(content)
    flag_and_terms = []
    n = 0
    flag = False
    term = ""
    term1 = ""
    term2 = ""
    for i,term in enumerate(preprocessed):
        for obj in arr:
            try:
                term1, term2 = obj.split(" ")
            except:
                term1 = obj
                term2 = " "

            if term2 == " ":
                term1 = normalize_and_stem(term1)
                if term == term1:
                    print("match found: " + term)
                    flag = True
                    flag_and_terms.append([])
                    flag_and_terms[n].append(flag)
                    flag_and_terms[n].append(term)
                    flag_and_terms[n].append("")# Just so that size of array is consistent
                    n = n + 1
            else:
            
                term1 = normalize_and_stem(term1)
                term2 = normalize_and_stem(term2)

                if term == term1:
                    if preprocessed[i+1] == term2:
                        print("match found: " + term1 + " " + term2)
                        flag = True
                        flag_and_terms.append([])
                        flag_and_terms[n].append(flag)
                        flag_and_terms[n].append(term1)
                        flag_and_terms[n].append(term2)
                        n = n + 1
                    else:
                        continue
    if(flag == False) :
        flag_and_terms.append([])
        print(flag_and_terms)
        flag_and_terms[n].append(flag)
    print(flag_and_terms)
    print(len(flag_and_terms))
    return flag_and_terms
            



   

