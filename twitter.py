from tweepy import Stream
import time
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from unidecode import unidecode
import json
from keras.models import load_model
import pandas as pd
import csv
import numpy as np
import matplotlib.pyplot as plt
#consumer key, consumer secret, access token, access secret.
ckey=""
csecret=""
atoken=""
asecret=""

def calctime(a):
    return time.time()-a

words = pd.read_table('glove.6B.50d.txt', sep=" ", index_col=0, header=None, quoting=csv.QUOTE_NONE)
def vec(w):
  return words.loc[w].as_matrix()
words_matrix = words.as_matrix()
print('add')
print(len(words_matrix))
w=[]
f=open('glove.6B.50d.txt',"r+",encoding="utf8")
content=f.readlines()
for i in range(len(content)):
   w.append(content[i].split(' ')[0])
vocab_to_int = dict((c, i+1) for i, c in enumerate(w))
int_to_vocab=dict((i+1, c) for i, c in enumerate(w))

model=load_model('twitter1.h5')
pos=0
neg=0
count=0
comp=0
initime=time.time()
plt.ion()

p=[]
mx=61
class listener(StreamListener):
    def on_data(self, data):
            global initime
            t=int(calctime(initime))
            data = json.loads(data)
            text = unidecode(data['text'])
            print(text)
            wor=[]
            wor=text.split(' ')
            wor=[x.strip(' , ./?@#:;-\t\n\b\0&"').lower() for x in wor]
            eg=np.zeros((1,61),dtype='int32')
            for j in range(len(wor)):
                if wor[j] in w:
                    eg[0][j]=vocab_to_int[wor[j]]
            z=model.predict(eg)[0][0]
            print(z)
            global pos
            global neg
            global comp
            global count
            count+=1
            #comp+=z
            if z>0.52:
                pos+=z
            else:
                neg-=z
            plt.axis([ 0, 200, -50,50])
            plt.xlabel('Time')
            plt.ylabel('Sentiment')
            plt.plot([t],[pos],'go',[t] ,[neg],'ro')
            plt.show()
            plt.pause(0.0001)

            if count==200:
                return False
            else:
                return True

    def on_error(self, status):
            print(status)

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
subject=input('Enter the subject')
if len(p)<=10:
    twitterStream = Stream(auth, listener(count))
    twitterStream.filter(track=[subject],languages=['en'])
    #except KeyError as e:
    #    print(str(e))
    #return(True)
