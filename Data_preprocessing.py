
# coding: utf-8

# In[1]:

#gaboceron10@gmail.com (2017)

import csv
import os
import random

#csv fieldnames
fieldnames=['index','song','year','artist','genre','lyrics']
#all available genres
all_genres=['Pop','Hip-Hop','Not Available','Other','Rock','Metal','Country','Jazz','Electronic','Folk','R&B','Indie']
#selected genres to classify
genres=['Pop','Hip-Hop','Rock','Metal','Country','Jazz']


# In[2]:

# Selecting data, write in new file only if the song belogns to the selected genres and it's lyrics are not empty

with open('lyrics.csv') as read_file, open('lyrics_genres.csv', 'w+') as write_file: 
    writer = csv.DictWriter(write_file, fieldnames, extrasaction='ignore')
    reader = csv.DictReader(read_file)
    writer.writeheader()
    for row in reader:
        if row['genre'] in genres and row['lyrics'] != '': 
            writer.writerow(row)


# In[3]:

#Splitting data by genres, this is done in order to process smaller files and avoid memory problems

for g in genres:
    with open('lyrics_genres.csv') as read_file, open('lyrics_gendre_'+g+'.csv', 'w+') as write_file: 
        writer = csv.DictWriter(write_file, fieldnames, extrasaction='ignore')
        reader = csv.DictReader(read_file)
        writer.writeheader()
        new_index=0
        for row in reader:
            if row['genre'] == g:
                row['index']= new_index
                writer.writerow(row)
                new_index=new_index+1


# In[4]:

#As the dataset is unbalanced,  we count the number of songs for each genre, then the min value is found to uner-sample

with open('lyrics_genres.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    count=[0]*len(genres)
    for row in reader:
        for g in range(len(genres)):
            if row['genre']==genres[g]:
                count[g]=count[g]+1
    print '\nGenres and counting:\n'
    dic_count=dict(zip(genres,count)) #Create dictionary
    print dic_count

min_count=min(count)


# In[5]:

#Under-sampling and shuffling each genre file

for g in genres:
    
    skip=random.sample(range(0, dic_count[g]), dic_count[g]-min_count)

    with open('lyrics_gendre_'+g+'.csv') as read_file, open('lyr_gen_'+g+'_sh.csv', 'w+') as write_file: 
        
        writer = csv.DictWriter(write_file, fieldnames, extrasaction='ignore')# csv.DictWriter(csvfile, fieldnames, restval='', extrasaction='raise', dialect='excel', *args, **kwds)The fieldnames parameter is a sequence of heys that identify the order in qhich values in the dictionary passed to the writerow method are written to the csvfile. if writerow method contauns a key not found in fieldnames, the optional extrasaction parameter indicates what action to writer.writeheader()
        reader = csv.DictReader(read_file)
        writer.writeheader()
        
        all_rows = [row for row in reader] 
        random.shuffle(all_rows)
        
        print 'Im writing, for',g,'skiping',len(skip),'of',dic_count[g],', total rows: ',dic_count[g]-len(skip)
        for r in all_rows:
            if int(r['index']) in skip:
                pass
            else:
                writer.writerow(r)


# In[6]:

# After under-sampling, all the dataset is put together in a single file

all_data=[]

for g in genres:
    print 'For '+g
    with open('lyr_gen_'+g+'_sh.csv') as read_file: 
        reader = csv.DictReader(read_file)
        all_rows = [row for row in reader]
    all_data.extend(all_rows)
random.shuffle(all_data)

with open('lyr_gen_all_sh.csv', 'w+') as write_file:
    writer = csv.DictWriter(write_file, fieldnames, extrasaction='ignore')# csv.DictWriter(csvfile, fieldnames, restval='', extrasaction='raise', dialect='excel', *args, **kwds)The fieldnames parameter is a sequence of heys that identify the order in qhich values in the dictionary passed to the writerow method are written to the csvfile. if writerow method contauns a key not found in fieldnames, the optional extrasaction parameter indicates what action to writer.writeheader()
    writer.writeheader()
    for r in all_data:
        writer.writerow(r)
print 'end'


# In[ ]:




# In[ ]:



