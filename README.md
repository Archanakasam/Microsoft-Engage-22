# Recommendation Engine
- Import Dataset regarding Articles information from available websites like [kaggle](https://www.kaggle.com), google.scholar.com
- Extract related fields from the Dataset required for the recommendation and convert into Data frame.
- Use TF-IDF Model on the Data frame for the recommendation Engine to work.

## TF-IDF Vectorizer
- Term frequency-inverse document frequency is a text vectorizer that transforms the text into a usable vector. It combines 2 concepts, Term Frequency (TF) and Document Frequency (DF).
- The term frequency is the number of occurrences of a specific term in a document.
- Document frequency is the number of documents containing a specific term.
-  TF-IDF score for term i in document j is 
-       w(i,j) = T.F * I.D.F
- We can implement TF-IDF Model by importing sklearn Package.
-  To Know more about this model, [click this](https://www.geeksforgeeks.org/understanding-tf-idf-term-frequency-inverse-document-frequency). 

