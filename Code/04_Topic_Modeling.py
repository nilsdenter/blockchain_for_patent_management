from gensim import models, corpora
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from time import time
t0 = time()

hyperparameter_alpha = "auto"                                   
hyperparameter_beta = "auto"
hyperparameter_alpha = 0.1                                   
hyperparameter_beta = 0.1                                    
Anzahl_Iterationen = 20000                                               
Minimale_Wahrscheinlichkeit = 0                                         
corpus = corpora.MmCorpus("./corpus.mm")                                   
dictionary = corpora.dictionary.Dictionary.load_from_text("./dictionary.dict")     
min=5
max=100
step=5
for topics in range(min,max+1,step):
    lda = models.ldamodel.LdaModel(random_state = 0, alpha= hyperparameter_alpha, eta= hyperparameter_beta, corpus = corpus, id2word = dictionary, num_topics =topics, passes = 20, iterations = Anzahl_Iterationen, minimum_probability = Minimale_Wahrscheinlichkeit, eval_every=1)
    lda.save("Topic_Model_%i" %topics)
    del lda

print("\n\nTime needed: %i seconds.\n\n" % (time() - t0))