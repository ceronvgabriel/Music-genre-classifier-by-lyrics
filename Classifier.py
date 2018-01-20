
# coding: utf-8

# In[12]:

#gaboceron10@gmail.com (2017)

import csv
import os
import random
import re
import numpy as np
import pandas as pd
import time
from sklearn import svm
import matplotlib.pyplot as plt

from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix

#csv fieldnames
fieldnames=['index','song','year','artist','genre','lyrics']
#all available genres
all_genres=['Pop','Hip-Hop','Not Available','Other','Rock','Metal','Country','Jazz','Electronic','Folk','R&B','Indie']
#selected genres to classify
genres=['Pop','Hip-Hop','Rock','Metal','Country','Jazz']


# In[13]:

#this is a load bar, just to show the execution progress of a loop

'''
Use: 

bar=Load_bar(total_iterations)
...
for i in ...
    bar.bar(current_iteration)

Other useful:

import time
start_time = time.time()
...
print("--- %s seconds ---" % (time.time() - start_time))

'''
class Load_bar:
    def __init__(self,total):
        self.total=total
        self.last_perc=0
    def current(self,current):
        perc=current*100/self.total
        if perc == self.last_perc:
            pass
        else:
            load= str(perc)+'%'
            print '{0}\r'.format(load),
            self.last_perc=perc


# In[17]:

with open('best_words.csv') as csvfile:
    reader = csv.reader(csvfile)#El formato del csv tiene un espacio de por medio
    for row in reader:
        b_words=row #there is just one row


# In[18]:

#this step is also part of the feature extraction. we know wich words are features, now we get the features of each song in the dataset

start_time = time.time()

feat_trix=[]
label_trix=[]

with open('lyr_gen_all_sh.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    
    row_count = sum(1 for row in reader) 
    csvfile.seek(0)
    
    bar=Load_bar(row_count)
    for i in range(row_count*100/100): #Extracting features from all dataset
        bar.current(i)
        feat=np.zeros(len(b_words)) #features
        
        if i==0:
            row=next(reader) # to avoid taking the dictionary header as a row
        
        row=next(reader)
        words=re.compile('\w+').findall(row['lyrics'])
        for word in words:
            word=word.lower()
            if word in b_words:
                ind=b_words.index(word)
                feat[ind]=feat[ind]+1
        
        #mag=sum(feat)#Normalization
        #if mag==0:
        #    feat_norm=map(float,feat)
        #else:
        #    feat_norm=[float(x)/mag for x in feat]
            
        feat_trix.append(feat)
        label_trix.append(row['genre'])

print("--- %s seconds ---" % (time.time() - start_time))


# In[ ]:

#saving training matrixes

with open('feat_matrix.csv','w+') as csvfile:
    writer = csv.writer(csvfile)#El formato del csv tiene un espacio de por medio
    for row in feat_trix:
        writer.writerow(row)
print 'end'

with open('label_matrix.csv','w+') as csvfile:
    writer = csv.writer(csvfile)#El formato del csv tiene un espacio de por medio
    writer.writerow(label_trix)
print 'end'


# In[14]:

#loading training matrixes

training_per=70 #here we select the training percentage

feat_trix=[]
label_trix=[]

with open('feat_matrix.csv') as csvfile:
    reader = csv.reader(csvfile)
    
    row_count = sum(1 for row in reader) 
    csvfile.seek(0)
    
    for i in range(row_count*training_per/100):
        feat_trix.append(map(float,next(reader)))
        
with open('label_matrix.csv') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        label_trix=row[:row_count*training_per/100] 
        
print 'end'


# In[15]:

#training the model

start_time = time.time()

clf = svm.SVC(decision_function_shape = "ovr") # Ovo= one vs one / ovr : one vs rest
clf.fit(feat_trix,label_trix)

#saving some memory after training:

del feat_trix
del label_trix

print("--- %s seconds ---" % (time.time() - start_time))


# In[16]:

#loading test matrixes

test_per=20 # we select the test percentage

test_per=100-test_per
feat_test_trix=[]
label_test_trix=[]

with open('feat_matrix.csv') as csvfile: 
    reader = csv.reader(csvfile)
    
    row_count = sum(1 for row in reader)
    csvfile.seek(0)
    
    for i in range(row_count):
        if i >= row_count*test_per/100:
            feat_test_trix.append(map(float,next(reader)))
        else:
            trash=next(reader)
        
with open('label_matrix.csv') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        label_test_trix=row[row_count*test_per/100:] 
        
print 'end'


# In[17]:

#predicting test data

start_time = time.time()

label_predic_trix=clf.predict(feat_test_trix)

print("--- %s seconds ---" % (time.time() - start_time))


# In[18]:

#accuracy score:

accuracy_score(label_test_trix,label_predic_trix)


# In[19]:

#Confucion matrix (number of songs)

confusion_matrix(label_test_trix,label_predic_trix)


# In[20]:

#Confucion matrix (number of songs)

pd.crosstab(pd.Series(label_test_trix),pd.Series(label_predic_trix), rownames=['Actual'], colnames=['Predicted'])


# In[21]:

#Confucion matrix (percentage)

pd.crosstab(pd.Series(label_test_trix),pd.Series(label_predic_trix), rownames=['Actual'], colnames=['Predicted']).apply(lambda r: 100.0 * r/r.sum()) # Columns are true, 


# In[22]:

clf


# In[ ]:



