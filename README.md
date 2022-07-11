# How can Blockchain technology support patent management? A systematic literature review

This project contains the data, code and results used in the paper: 

Denter, N., Seeger, F., & Moehrle, M. G. (2022). How can Blockchain technology support patent management? A systematic literature review. International Journal of Information Management, Article 102506. Advance online publication. https://doi.org/10.1016/j.ijinfomgt.2022.102506.

https://www.researchgate.net/publication/359162263_How_can_Blockchain_technology_support_patent_management_A_systematic_literature_review

To reproduce the results, first, you need to download all files in the Data folder.

Then, the code must be executed in ascending order of the sequence number.

The code "01_Bibliographic_results.py" uses the refined article collection (Articles.xlsx) and creates an figure (Figure 3 in the paper) showing (a) the number of each 7D model dimension addressed in the course of time, (b) the number of multiple 7D dimensions addressed in the course of time, (c) the number of each document type addressed in the course of time, and (d) the number of each Blockchain architecture addressed in the course of time. 

The code "02_Venn_Diagram.py" uses the refined article collection (Articles.xlsx) and creates a Venn diagram for the four different databases, i.e., Google Scholar, IEEE Xplore, Scopus, and Web of Science.

This concludes the figures used in the Method and Results section.

The following codes are used for the Validation section.

The code "03_Preprocess_text_and_create_dictionary_and_corpus.py" uses the retrieved titles and abstracts of the Validation articles.xlsx file and preprocesses as well as transforms the data into readable format for subsequent topic modeling. Preprocessing is based on a multitude of different stop word collections contained in the file stop_words_conducted.txt.

The code "04_Topic_Modeling.py" conducts topic modeling on the retrieved and preprocessed patent titles and abstracts.

The code "05_Evaluation_Topic_Modeling.py" computes different evaluation metrics (e.g. perplexity, u_mass coherence) for the calculated topic models.

The code "06_Extraction_Topic_Modeling_Results.py " yields different outcomes of the topic models such as the top 20 words of each topic, the probability of each topic belonging to each document, wordclouds of the top 20 terms of each topics and an interactive mds-plot by using the Python library pyldavis.

Please see the paper for further information.
