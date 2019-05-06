
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize



def preprocess(words_tokenized):
    
    
    stop_words = set(stopwords.words('english'))

    normalized_words = []

    for w in words_tokenized:
        normalized_words.append(w.lower())

    filtered_sentence = []

    for w in normalized_words:
        if w not in stop_words:
            filtered_sentence.append(w)


    ps = PorterStemmer()
    stemmed_words = []

    for w in filtered_sentence:
        stemmed_words.append(ps.stem(w))
    

    word_list = []

    for word in stemmed_words:
        word_list.append(word)
        
    return word_list

def normalize_and_stem(term):
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


def match_unigrams_and_bigrams(preprocessed):
    #The size of the multidimensional array would be the no. of hits in a single page, there will be an array for each hit
    #If the flag is False, the multidimensional array has only one array
    flag_and_terms = []
    
    n = 0
    flag = False
    term = ""
    term1 = ""
    term2 = ""
    for i,term in enumerate(preprocessed):
        for obj in arr:
            #print(obj)
            try:

                term1, term2 = obj.split(" ")
    
            except:
                term1 = obj
                term2 = " "
            #print("term1: %s, term2: %s" % (term1, term2))
            if term2 == " ":
            
                term1 = normalize_and_stem(term1)
                if term == term1:
                    print("match found: " + term)
                    flag = True
                    flag_and_terms.append([])
                    flag_and_terms[n].append(flag)
                    flag_and_terms[n].append(term)
                    flag_and_terms[n].append("")#Just to the sizes of the arrays consistent
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
        #flag_and_terms.append("")
        #flag_and_terms.append("")
    print(flag_and_terms)
    print(len(flag_and_terms))
    return flag_and_terms
            
                


   

