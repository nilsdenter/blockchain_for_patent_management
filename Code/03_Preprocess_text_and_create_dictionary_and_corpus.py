import os
from gensim import corpora
import pandas as pd
from time import time
t0 = time()
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
import sys
import re
"""Folders"""

 
#unigram oder bigram oder trigram auswaehlen, andere Begriffe sind nicht erlaubt bzw. muessen noch programmiert werden
semantic_structure = "unigram"

#Fenstergroesse auswaehlen, mindestens semantic_structure + 2
windowsize = 4

#Wenn True werden bigramme wie 'health health' oder trigramme wie 'health care health' eliminiert
no_dublicates = True

#Wenn True dann werden die Begriffe auf ihren Wortstamm mit dem PorterStemmer reduziert
stemming = False

#Wenn True dann werden die Begriffe auf ihre Wortform durch den WordNetLemmatizer reduziert
lemmatizer = True

#Calculate tfidf
calculate_tfidf_manually = True
calculate_tfidf_gensim = False
calculate_df_tdm = False

#Wenn True, dann werden nur die Top Number_tfidf Terme absteigend nach dem Tfidf-Score inkludiert
include_tfidf = False
number_tfidf = 10000

#Minimale Anzahl an Buchstaben in einem Wort
minimal_wordlength = 3

if semantic_structure == "bigram": 
    ngram=2
elif semantic_structure == "trigram":
    ngram=3
elif semantic_structure == "unigram":
    ngram=1
    
elif semantic_structure == "":
    sys.exit("\n\nNo semantic structure declared!\n\n")
else:
    sys.exit("\n\nField semantic structure is not correctly inserted!\n\n")
    

""" Read xlsx file"""
df = pd.read_excel("Validation articles.xlsx", engine = "openpyxl")
titles = list(df["Title"])
abstracts = list(df["Abstract"])


texts_raw = []
count=0
for paper in titles:
    texts_raw.append(paper + " " + abstracts[count])
    count +=1

ids = list(df["ID"])

pd.DataFrame(data=texts_raw, index=ids).to_excel("ID_Title_Abstract.xlsx", header=["Title and Abstract"])

with open("stop_words_conducted.txt" ,"r") as stopwordlist:
    list1 = stopwordlist.read().split('\n')
    stoplist = [i for i in list1 if i != ' ']

characterlst_one_letter = list(set(". , â € “ “ ” ! * ‐ — – ' + 1 2 3 4 5 6 7 8 9 0 # - , ’ ` ‘ ´  's  ’s . % & ; : < > | @ ² ³ / { ( ) [ ] } = ? ß ’s 's".split() + '"'.split() + [" "]))
characterlst_two_letters = list(set("’s 's  ’s ’s 's `s ´s".split()))
stoplist = list(set(stoplist + "ï»¿".split()))
replace_list = {"mncs":"multinational-corporations",
                "mnc":"multinational-corporations", 
                "npes" : "nonpracticing-entities",
                "npe": "nonpracticing-entities",
                "fsa": "firm‐specific-advantages",
                "r&bd":"research-and-business-development",
                "tod": "technology-opportunity-discovery",
                "ccis":"creative-and-cultural-industries",
                "psfs":"professional-service-firms",
                "psf":"professional-service-firms",
                "atp":"advanced-technology-program",
                "iot": "internet-of-things", 
                "etfs":"exchange-traded-funds",
                "mnes":"multinational-enterprises",
                "mne":"multinational-enterprises", 
                "brics":"brics-countries", 
                "sps":"science-technology-park", 
                "nlss": "national-learning-systems" ,
                "nls":"natural-laboratories", 
                "th": "triple-helix-model-of-innovation",
                "lhc": "large-hadron-collider", 
                "smes": "small-and-medium-enterprises", 
                "sme":"small-and-medium-enterprises", 
                "icie": "industry-university-research-collaborative-innovation-efficiency", 
                "icies": "industry-university-research-collaborative-innovation-efficiency",
                "vcs":"venture-capital",
                "vc":"venture-capital",
                "voc":"varieties-of-capitalism",
                "s&t":"science-and-technology",
                "soes": "state-owned enterprise",
                "soe": "state-owned enterprise",
                "stps":"science-technology-park",
                "stp":"science-technology-park", 
                "m&as":"merger-and-acquisition",
                "m&a":"merger-and-acquisition", 
                "wpts": "willingness-to-pay", 
                "wpt": "willingness-to-pay", 
                "r&d": "research-and-development", 
                "alliances":"alliance",
                "u–i": "university–industry", 
                "e-business": "ebusiness",
                "e-businesses": "ebusiness", 
                "e-business.": "ebusiness", 
                "inter-organizational":"interorganizational", 
                "organisational": "organizational", 
                "markets":"market"}
texts = []

for document in texts_raw:
    documents = []
    document = document.lower()
    document= re.sub(r'[0-9]+', ' ', document)
    document = document.replace("firm‐specific advantages", " firm‐specific-advantages ")
    document = document.replace("multinational corporations", " multinational-corporations ")
    document = document.replace(" mncs ", " multinational-corporations ")
    document = document.replace(" mnc ", " multinational-corporations ")
    document = document.replace(" fsa ", " firm‐specific-advantages ")
    document = document.replace(" psfs ", " professional-service-firms ")
    document = document.replace("nonpracticing entities", " nonpracticing-entities ")
    document = document.replace(" npes ", " nonpracticing-entities ")
    document = document.replace(" npe ", " nonpracticing-entities ")
    document = document.replace("non-practicing", " nonpracticing-entities ")
    document = document.replace("nonpracticing", " nonpracticing-entities ")
    document = document.replace("patent trolls", " patent-trolls ")
    document = document.replace("patent troll", " patent-trolls ")
    document = document.replace(" psf ", " professional-service-firms ")
    document = document.replace(" tod ", " technology-opportunity-discovery ")
    document = document.replace("technology opportunity discovery", " technology-opportunity-discovery ")
    document = document.replace("research and business development", " research-and-business-development ")
    document = document.replace(" r&bd ", " research-and-business-development ")
    document = document.replace("professional service firms", " professional-service-firms ")
    document = document.replace(" etfs ", " exchange-traded-funds ")
    document = document.replace(" advanced technology program ", " advanced-technology-program ")
    document = document.replace(" atp ", " advanced-technology-program ")
    document = document.replace(" creative and cultural industries ", " creative-and-cultural-industries ")
    document = document.replace(" ccis ", " creative-and-cultural-industries ")
    document = document.replace("exchange-traded funds", " exchange-traded-funds ")
    document = document.replace("internet of things", " internet-of-things ")
    document = document.replace(" iot ", " internet-of-things ")
    document = document.replace(" brics ", " brics-countries ")
    document = document.replace(" gvcs ", " global-value-chains ")
    document = document.replace(" gvc ", " global-value-chains ")
    document = document.replace(" spd ", " social-product-development ")
    document = document.replace("social product development", " social-product-development ")
    document = document.replace("global value chains", " global-value-chains ")
    document = document.replace("global value chain", " global-value-chains ")
    document = document.replace("multinational enterprise", " multinational-enterprises ")
    document = document.replace("multinational enterprises", " multinational-enterprises ")
    document = document.replace(" mnes ", " multinational-enterprises ")
    document = document.replace(" mne ", " multinational-enterprises ")
    document = document.replace(" voc ", " varieties-of-capitalism ")
    document = document.replace(" voc ", " varieties-of-capitalism ")
    document = document.replace(" icies ", " industry-university-research-collaborative-innovation-efficiency ")
    document = document.replace(" icie ", " industry-university-research-collaborative-innovation-efficiency ")
    document = document.replace("open innovations", " open-innovation ")
    document = document.replace(" s&t ", " science-and-technology ")
    document = document.replace("open innovation", " open-innovation ")
    document = document.replace(" soes ", " state-owned enterprise ")
    document = document.replace(" soe ", " state-owned enterprise ")
    document = document.replace(" m&as ", " merger-and-acquisition ")
    document = document.replace(" m&a ", " merger-and-acquisition ")
    document = document.replace("mergers and acquisition", " merger-and-acquisition")
    document = document.replace("mergers & acquisition", " merger-and-acquisition")
    document = document.replace("merger and acquisition", " merger-and-acquisition ")
    document = document.replace("merger & acquisition", " merger-and-acquisition ")
    document = document.replace(" r&ds ", " research-and-development ")
    document = document.replace(" r&d ", " research-and-development ")
    document = document.replace("research and development", " research-and-development ")
    document = document.replace("science and technology parks", " science-technology-park ")
    document = document.replace("science and technology park", " science-technology-park ")
    document = document.replace(" stps ", " science-technology-park ")
    document = document.replace(" stp ", " science-technology-park ")
    document = document.replace(" sps ", " science-technology-park ")
    document = document.replace(" jvs ", " joint-venture ")
    document = document.replace(" joint venture ", " joint-venture ")
    document = document.replace(" jv ", " joint-venture ")
    document = document.replace(" th ", " triple-helix-model-of-innovation ")
    document = document.replace("triple helix", " triple-helix-model-of-innovation ")
    document = document.replace(" oi ", " open-innovation ")
    document = document.replace(" nlss ", " national-learning-systems ")
    document = document.replace(" nls ", " natural-laboratories ")
    document = document.replace("initial public-offerings", " initial-public-offering ")
    document = document.replace("initial-public-offerings", " initial-public-offering ")
    document = document.replace("initial public-offering", " initial-public-offering ")
    document = document.replace("initial-public-offering", " initial-public-offering ")
    document = document.replace(" ipos ", " initial-public-offering ")
    document = document.replace(" ipo ", " initial-public-offering ")
    document = document.replace(" cross border ", " cross-border ")
    document = document.replace(" lhc ", " large-hadron-collider ")
    document = document.replace(" wpt ", " willingness-to-pay ")
    document = document.replace(" oem ", " original-equipment-manufacturer ")
    document = document.replace("original equipment manufacturer", " original-equipment-manufacturer ")
    document = document.replace("venture capital", " venture-capital ")
    document = document.replace(" vc ", " venture-capital ")
    document = document.replace("resource-based view", " resource-based-view ")
    document = document.replace("resource—based view" ," resource-based-view ")
    document = document.replace("resource–based view", " resource-based-view ")
    document = document.replace("resource based view", " resource-based-view ")
    document = document.replace("knowledge-based view", " knowledge-based-view ")
    document = document.replace("knowledge—based view", " knowledge-based-view ")
    document = document.replace("knowledge–based view", " knowledge-based-view ")
    document = document.replace("knowledge based view", " knowledge-based-view ")
    document = document.replace("market-based view", " market-based-view ")
    document = document.replace("market—based view", " market-based-view ")
    document = document.replace("market–based view", " market-based-view ")
    document = document.replace("market based view", " market-based-view ")
    document = document.replace("external knowledge", " external-knowledge ")
    document = document.replace("knowledge acquisition", " knowledge-acquisition ")
    document = document.replace("united states of america", " ")
    document = document.replace("united states", " ")
    document = document.replace("intellectual property rights", " intellectual-property-right ")
    document = document.replace("intellectual property right", " intellectual-property-right ")
    document = document.replace(" iprs ", " intellectual-property-right ")
    document = document.replace(" ipr ", " intellectual-property-right ")
    document = document.replace("spin-offs ", " spinoff ")
    document = document.replace("spin—offs", " spinoff ")
    document = document.replace("spin–offs", " spinoff ")
    document = document.replace("spin-off", " spinoff ")
    document = document.replace("spin—off", " spinoff ")
    document = document.replace("spin–off", " spinoff ")
    document = document.replace("spinoffs", " spinoff ")
    document = document.replace(" start-ups ", " startups ")
    document = document.replace(" start-up ", " startups ")
    document = document.replace(" startup ", " startups ")
    document = document.replace(" ksn ", " knowledge-supply-networks ")
    document = document.replace(" knowledge supply networks ", " knowledge-supply-networks ")
    document = document.replace(" knowledge supply network ", " knowledge-supply-networks ")
    document = document.replace(" e‐businesses ", " e‐business ")
    document = document.replace(" markets ", " market ")
    document = document.replace(" technologies ", " technology ")
    document = document.replace(" smes ", " small-and-medium-enterprises ")
    document = document.replace(" sme ", " small-and-medium-enterprises ")
    document = document.replace(" alliances ", " alliance ")
    document = document.split()
    for word in document:
        word_old = word
        word = word.replace(")", " ")
        word = word.replace("(", " ")
        word = word.replace("—", " ")
        if word not in replace_list:
                while len(word)>1 and word[0] in characterlst_one_letter:
                    word = word[1:]
                while len(word)>1 and word[-1] in characterlst_one_letter:
                    word = word[:-1]
                while len(word)>1 and word[-2:] in characterlst_two_letters:
                    word = word[:-2]
                if word not in stoplist and len(word) >= minimal_wordlength:
                    documents.append(word)
                    
        else:
                word_new = word.replace(word, replace_list[word])
                documents.append(word_new)
    texts.append(documents)
        

if stemming:
    from nltk.stem import PorterStemmer
    ps = PorterStemmer()
    texts = [[ps.stem(word) for word in document] for document in texts]

if lemmatizer:
    from nltk.stem import WordNetLemmatizer
    lemmatizer = WordNetLemmatizer() 
    texts = [[lemmatizer.lemmatize(word) for word in document] for document in texts]
    
if not semantic_structure == "unigram": 
    from nltk.util import skipgrams
    texts = [list(skipgrams(line,ngram,windowsize-2)) for line in texts]
    
"""Bigramm Funktion"""
if semantic_structure == "bigram":  
    texts_new=[]
    if no_dublicates:
        for doc in texts:
            text_new=[]
            for item in doc:
                if item[0]!=item[1]:
                    l = [item[0], item[1]]
                    l.sort()
                    text_new.append("{0}_{1}".format(l[0], l[1]))   
            texts_new.append(text_new)
    else:
        for doc in texts:
            text_new=[]
            for item in doc:
                l = [item[0], item[1]]
                l.sort()
                text_new.append("{0}_{1}".format(l[0], l[1]))
            texts_new.append(text_new)
    texts = [*texts_new]
    del texts_new
    
elif semantic_structure == "trigram":
    texts_new=[]
    if no_dublicates:
        for doc in texts:
        
            text_new  = [("{0}_{1}_{2}".format(item[0], item[1], item[2])) for item in doc if item[0] != item[1] or item[1] != item[2] or item[0] != item[2]]        
            texts_new.append(text_new)
    else:
        for doc in texts:
            text_new  = [("{0}_{1}_{2}".format(item[0], item[1], item[2])) for item in doc]        
            texts_new.append(text_new)
    texts = [*texts_new]
    del text_new
    del texts_new

"""Save preprocessed texts"""

pd.DataFrame(data=[" ".join(d) for d in texts], index=ids).to_csv("Preprocessed_Title_Abstract.csv", sep=";", header=["Preprocessed Title and Abstract"])

    
"""Save texts for c_v coherence measurement"""
import pickle

with open("texts_for_cv_coherence.txt", "wb") as fp:   #Pickling
    pickle.dump(texts, fp)
print(texts[-5:])

"""Dictionary"""
dictionary = corpora.Dictionary(texts)
dictionary.save_as_text("dictionary.dict")

"""Corpus"""
corpus = [dictionary.doc2bow(item) for item in texts]
corpora.MmCorpus.serialize("corpus.mm", corpus)

print("\n\n{0} text documents with {1} unique and {2} total {3}s processed!\n\n".format(dictionary.num_docs, len(dictionary), dictionary.num_pos, semantic_structure))

print("\n\nProcessing time: %i seconds!\n\n" % (time() - t0))