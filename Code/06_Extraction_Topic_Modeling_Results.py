from gensim import models, corpora

import logging
import numpy
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import pandas as pd
import time
t0 = time.time()


corpus1 = corpora.MmCorpus("corpus.mm")
dictionary1 = corpora.dictionary.Dictionary.load_from_text("dictionary.dict")

def topics(num_terms=10):
    anzahl_terme = num_terms
    topics1 = [[word for rank, (word, prob) in enumerate(words)]
                          for topic_id, words in model1.show_topics(formatted=False, num_words=anzahl_terme, num_topics=model1.num_topics)]
    topics1_speicherpfad = "topics_%i.csv" % model1.num_topics
    topicnumber=[]
    for i in range(1, model1.num_topics+1,1):
        topicnumber.append("Topic " + str(i))
    wordnumber=[]
    for i in range(1,anzahl_terme+1,1):
        wordnumber.append("Term " + str(i))
    
    pd.DataFrame(topics1, index=topicnumber, columns= wordnumber).to_csv(topics1_speicherpfad, sep=';', decimal=',')
    print("\n\nOverview of topics processed!\n\n")

def doc_topic(corpus):
    corpus1=corpus
    topic_over_doc = [dict(model1[x]) for x in corpus1]
    output_topic_over_doc_speicherpfad = "doc_topic_probability_%i.csv" % model1.num_topics
    topicnumber=[]
    for i in range(1, model1.num_topics+1,1):
        topicnumber.append("Topic " + str(i))
    
    df = pd.read_excel("N:\\Publikationen\\2020 Blockchain in patent management\\Full paper\\02_Analyses\\Discussion Search\\Topic_Modeling\\Input_Data\\ID_Title_Abstract.xlsx")
    documents=df["ID"]

    data=pd.DataFrame(data=topic_over_doc, index = documents)
    pd.DataFrame(data=data).to_csv(output_topic_over_doc_speicherpfad, sep=";", decimal=',', header = topicnumber)
    print("\n\nDocument topic matrix processed!\n\n")
    
def topic_terms():
    topic_terms = model1.state.get_lambda() 
    topic_terms_proba = numpy.apply_along_axis(lambda x: x/x.sum(),1,topic_terms)
    term_topic_proba = numpy.matrix.transpose(topic_terms_proba)
    words = [model1.id2word[i] for i in range(topic_terms_proba.shape[1])]
    matrix_similarity_word_over_topic = "topic_word_probability_%i.csv" % model1.num_topics
    matrix_similarity_topic_over_word = "word_topic_probability_%i.csv" % model1.num_topics
    topicnumber=[]
    for i in range(1, model1.num_topics+1,1):
        topicnumber.append("Topic " + str(i))
        
    pd.DataFrame(topic_terms_proba, index= topicnumber, columns=words).to_csv(matrix_similarity_word_over_topic, sep = ';', decimal=',')
    print("\n\nTopic term matrix processed!\n\n")
    
    pd.DataFrame(term_topic_proba, index= words, columns=topicnumber).to_csv(matrix_similarity_topic_over_word, sep = ';', decimal=',')
    print("\n\nTerm topic matrix processed!\n\n")

def pyldavis():
    """Visualisierung ähnlich wie MDS
    
    To read about the methodology behind pyLDAvis, see `the original
    paper <http://nlp.stanford.edu/events/illvi2014/papers/sievert-illvi2014.pdf>`__,
    which was presented at the `2014 ACL Workshop on Interactive Language
    Learning, Visualization, and
    Interfaces <http://nlp.stanford.edu/events/illvi2014/>`__ in Baltimore
    on June 27, 2014."""
    
    from pyLDAvis import gensim as pygensim
    import pyLDAvis
    pyLDAvis_data =  pygensim.prepare(model1,corpus1, dictionary1, sort_topics=False)
    pyLDAvis.save_html(pyLDAvis_data, 'pyldavis_%i.html' % model1.num_topics)
    print("\n\npyLDAvis processed!\n\n")
    
        
def wordcloud(number_words=200):
    import matplotlib.pyplot as plt
    from wordcloud import WordCloud
    import random
    def grey_color_func():
        return "hsl(0, {0}, %i)".format(random.randint(60, 100))
    def allblack():
        return lambda *args, **kwargs:(0,0,0)
    
    def allgrey():
        return lambda *args, **kwargs:(105,105,105)
    
    for t in range(model1.num_topics):
        plt.figure(figsize=(10,5))
        plt.axis("off")
        plt.title("Topic #" + str(t+1))
        wordcloud = WordCloud(background_color="white", width=2000, height=1000, color_func=allgrey()).fit_words(dict(model1.show_topic(t, number_words)))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.savefig("wordcloud_topic_%i.png" %(t+1), bbox_inches='tight', dpi=1000)
        plt.show()


topic_list=[10,15,20,25,30]
for Topicanzahl in topic_list:

    model1 =  models.LdaModel.load("Topic_Model_%i" %Topicanzahl) 

    topics(num_terms=20)
    doc_topic(corpus=corpus1)
    wordcloud(number_words=20)
    pyldavis()
    
print("\n\nTime needed: %i seconds.\n\n" % (time.time() - t0))