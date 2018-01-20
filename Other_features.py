
# coding: utf-8

# In[2]:

#gaboceron10@gmail.com (2017)

import csv
import os
import random
import re
import numpy as np

#csv fieldnames
fieldnames=['index','song','year','artist','genre','lyrics']
#all available genres
all_genres=['Pop','Hip-Hop','Not Available','Other','Rock','Metal','Country','Jazz','Electronic','Folk','R&B','Indie']
#selected genres to classify
genres=['Pop','Hip-Hop','Rock','Metal','Country','Jazz']


# In[2]:

all_data=[]

w_list=[]
w_count=[]

for g in genres:
    w_list=[]
    w_count=[]
    print 'For '+g
    with open('lyr_gen_'+g+'_sh.csv') as read_file: 
        reader = csv.DictReader(read_file)
        row_count = sum(1 for row in reader)
        read_file.seek(0)
        for i in range(row_count):
            row=next(reader)
            words=re.compile('\w+').findall(row['lyrics'])
            for word in words:
                word=word.lower()
                if word in w_list:
                    plus=w_list.index(word)
                    w_count[plus]=w_count[plus]+1
                else:
                    w_list.append(word)
                    w_count.append(1)
#
    with open('all_words_'+g+'.csv','w+') as csvfile:
        writer = csv.writer(csvfile)#El formato del csv tiene un espacio de por medio
        writer.writerow(w_list)
        writer.writerow(w_count)


# In[46]:

#Run from here
#
#
#

nw_count=[]
nw_list=[]

g=genres[5]

with open('all_words_'+g+'.csv') as csvfile:
    reader = csv.reader(csvfile)
    
    nw_list=next(reader)
    nw_count=map(int,next(reader)) 


# In[47]:

#loading the stop words list
with open('stop_words.csv') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        stop_words=row #there is just one row, with 119 words


# In[48]:

arr = np.array(nw_count)
ind=arr.argsort()[-200:][::-1] # sorting the most used words
b3_words=[]
b3_count=[]

b_words=[]
b_count=[]

for i in ind:
    b3_words.append(nw_list[i])
    b3_count.append(nw_count[i])
    
for j in range(len(b3_words)):
    if b3_words[j] in stop_words: # stop words are ignored
        pass
    else:
        b_words.append(b3_words[j])
        b_count.append(b3_count[j])

b1_words=b_words[:50] #selecting the number of words (features)
b1_count=b_count[:50]


# In[49]:

with open('all_words.csv') as csvfile:
    reader = csv.reader(csvfile)
    
    all_w_list=next(reader)
    all_w_count=map(int,next(reader)) 


# In[50]:

score=[]

for i in range(len(b1_words)):
    plus=all_w_list.index(b1_words[i])
    sc=float(all_w_count[plus])/float(b1_count[i])
    score.append(sc)
print len(score),len(b1_words)


# In[51]:

print g
for i in range(len(b1_words)):
    print b1_words[i],score[i]


# In[52]:

arr = np.array(score)
ind=arr.argsort()


# In[53]:

best_words=[]
for i in ind:
    best_words.append(b1_words[i])


# In[54]:

print g
print best_words[:10]


# In[ ]:



