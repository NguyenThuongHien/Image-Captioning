import pickle
import numpy as np
from os import listdir
dic={'abjd.jpg':1,'b':2}


sentence='0.36 0.38 0.39'
li=sentence.split()
k=np.asarray(li[1:], dtype='float32')
k=[[1,1],[1,2],[2,3],[1,3]]
so=sorted(k,key=lambda e: e[1])
del k[1]
sentence='nguyen thuong hien ftech'
tk=[token for token in sentence.split()]
seq=['a','b','c']
sentence=' '.join(seq)
count=['a','b','a','b','c','c','c']
from collections import Counter
counter=Counter()
for c in count :
	counter[c]+=1
# print(counter)
a=['a','b','c']
b=[1,2,3,4]
r=zip(b,a)

a=Counter({'a':1,'b':2,'c':3})
b=Counter({'a':2,'b':3})
m=Counter()
m=a|b
d=Counter({'a':2,'b':1})

tp=tuple((2,3))
# print(len(tp))
tr=True
# print(Counter('aaabcc'))
embedding=pickle.load(open('../Data Set/Cleaned Data/Document Caption.pickle','rb'))
# print(embedding)
with open('../Data Set/Cleaned Data/max_length.txt','r') as fr:
  maxlength=fr.read()
maxlength=int(maxlength)
# print(maxlength)
name_img=[[],[],[],[]]
l=[2,3,4,5,6]


def beam_search(candidate,beam_size,max_length,word2idx,idx2word):
    # in_word is index of word input
    first_token='startseq'
    first_token=word2idx[first_token]
    result=[]
    for i in range(max_length):
      all_score=[]
      if i==0:
        zeros=[0 for _ in range(max_length-1)]
        first_seq=[first_token]
        first_seq.extend(zeros)
        yhat=candidate[i]
        top_idx=sorted(range(len(yhat)),key=lambda e:yhat[e],reverse=True)[:beam_size]
        for k in range(beam_size):
          score=yhat[top_idx[k]]
          list_word=[top_idx[k]]
          result.append([list_word,score])
        # print(result)
        continue
      for j in range(beam_size):
        # check whether result[j] have contained end word ('endseq')
        word=idx2word[result[j][0][-1]]
        # if j==0: print(result)
        if word=='endseq':
          all_score.append(result[j])
        # prepare vector index to predict next word
        else:
          input_seq,score=list(result[j])
          zeroes=[0 for _ in range(max_length-len(input_seq))]
          input_seq.extend(zeroes)
          # get probability distribution of each word in ouput
          yhat=candidate[i][j]
          for k in range(len(yhat)):
            tmp_seq=list(result[j][0])
            # print(tmp_seq)
            tmp_seq.append(k)
            new_score=score*yhat[k]
            all_score.append([tmp_seq,new_score])
        pass
      result=sorted(all_score,key=lambda e:e[1],reverse=True)[:beam_size]
      print('result',result)
      pass
    return result
    pass
# test beam search alg
candidate=[[0.1,0.2,0.3,0.4,0.0],
           [[0.4,0.3,0.2,0.1,0.0],[0.3,0.4,0.1,0.2,0.0]],
           [[0.0,0.2,0.3,0.1,0.4],[0.1,0.4,0.2,0.0,0.3]],
           [[0.2,0.4,0.3,0.1,0.0],[0.1,0.3,0.0,0.4,0.2]]
          ]
idx2word={0:'startseq',1:'b',2:'c',3:'d',4:'endseq'}
word2idx={'startseq':0,'b':1,'c':2,'d':3,'endseq':4}
result1=beam_search(candidate,2,4,word2idx,idx2word)
print(result1)