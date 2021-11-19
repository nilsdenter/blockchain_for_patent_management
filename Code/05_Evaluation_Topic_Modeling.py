from gensim import corpora, models
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import pandas as pd
from time import time
t0 = time()
min=5
max=100
step=5

corpus = corpora.MmCorpus("corpus.mm")
dictionary = corpora.dictionary.Dictionary.load_from_text("dictionary.dict")

def coherence_u_mass():
    topicanzahl=[]
    u_mass = []
    for i in range(min,max+1,step):
        topicanzahl.append(i)
        model = models.LdaModel.load("../Models/Topic_Model_%i" %i)
        u_mass.append(models.CoherenceModel(corpus = corpus, model = model, dictionary = dictionary, coherence='u_mass').get_coherence())
    pd.DataFrame(data=u_mass, index = topicanzahl).to_csv("U_Mass_coherence.csv", sep=';', decimal=',', header=["U_mass"])
    
def perplexity():
    topicanzahl=[]
    perplexity =[]
    logperplexity=[]
    for i in range(min,max+1,step):
        topicanzahl.append(i)
        model = models.LdaModel.load("../Models/Topic_Model_%i" %i)    
        logperp = model.log_perplexity(corpus)
        logperplexity.append(logperp)
        perp = 2**(-logperp)
        perplexity.append(perp)
    
    pd.DataFrame(data=logperplexity, index = topicanzahl).to_csv("Log_Perplexity.csv", sep=';', decimal=',', header=["Log Perplexity"])

def coherence_c_v(texts_file):
    import pickle
    with open(texts_file, "rb") as fp:
        texts = pickle.load(fp) # Unpicklin
    topicanzahl=[]
    cv = []
    for i in range(min,max+1,step):
        topicanzahl.append(i)
        model = models.LdaModel.load("../Models/Topic_Model_%i" %i)        
        cv.append(models.CoherenceModel(texts = texts, model = model, dictionary = dictionary, coherence='c_v', processes=1).get_coherence())   
    pd.DataFrame(data=cv, index = topicanzahl).to_csv("C_v_coherence.csv", sep=';', decimal=',', header=["C_v"])
    
def coherence_c_uci(texts_file):
    import pickle
    with open(texts_file, "rb") as fp:
        texts= pickle.load(fp) # Unpicklin
    topicanzahl=[]
    c_uci = []
    for i in range(min,max+1,step):
        topicanzahl.append(i)
        model = models.LdaModel.load("../Models/Topic_Model_%i" %i)
        c_uci.append(models.CoherenceModel(texts = texts, model = model, dictionary = dictionary, coherence='c_uci', processes=1).get_coherence())
    pd.DataFrame(data=c_uci, index = topicanzahl).to_csv("C_uci_coherence.csv", sep=';', decimal=',', header=["C_uci"])

def coherence_c_npmi(texts_file):
    import pickle
    with open(texts_file, "rb") as fp:
        texts = pickle.load(fp) # Unpicklin
    topicanzahl=[]
    c_npmi = []
    for i in range(min,max+1,step):
        topicanzahl.append(i)
        model = models.LdaModel.load("../Models/Topic_Model_%i" %i)
        c_npmi.append(models.CoherenceModel(texts = texts, model = model, dictionary = dictionary, coherence='c_npmi', processes=1).get_coherence())
    pd.DataFrame(data=c_npmi, index = topicanzahl).to_csv("C_npmi_coherence.csv", sep=';', decimal=',', header=["C_nmpi"])

perplexity()
coherence_u_mass()
coherence_c_v(texts_file='texts_for_cv_coherence.txt')
coherence_c_uci(texts_file='texts_for_cv_coherence.txt')
coherence_c_npmi(texts_file='texts_for_cv_coherence.txt')

print("\n\nTime needed: %i seconds.\n\n" % (time() - t0))