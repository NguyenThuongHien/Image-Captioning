import pickle
import numpy as np

# Load all caption of images from caption dataset
def load_capt_data(path):
	txt_data=''
	with open(path,'r') as fr:
		txt_data=fr.read()
	txt_data=txt_data.strip()
	return txt_data
	pass
def split_imgandcapt(document):
	captionIDs=[]
	raw_captions=[]
	for line in document.split('\n'):
		tab=line.split('\t')
		captionIDs.append(tab[0])
		raw_captions.append(tab[1])
		pass
	return captionIDs,raw_captions
	pass
# Clean data via the steps following:
# 	+ Remove punctuation, abundant whitespaces , words containing number or special tokens
# 	+ Lower case
def get_clean_captions(captions):
	clean_caption=[]
	for caption in captions:
		import string
		text=[]
		strg=''
		caption_split=caption.split()
		# remove punctuation, words containing number or special token
		text1=[word for word in caption_split if (not(word in string.punctuation) and word.isalpha())]
		# lower case
		text=[word.lower() for word in text1]
		for word in text:
			strg+=(word+' ')
			pass
		# remove last space
		strg=strg.strip()
		clean_caption.append(strg)
		pass
	return clean_caption
	pass
		
# get all raw captions in caption dataset
def get_imageIDs(captionIDs):
	imageIDs=[]
	for name in captionIDs:
		imageIDs.append(name.split('.')[0])
		pass
	return imageIDs
	pass
def save_captions(imageIDs,clean_captions,path):
	documentary=''
	for i in range(len(imageIDs)):
		line=imageIDs[i]+'\t'+clean_captions[i]+'\n'
		documentary+=line
		pass
	documentary=documentary.strip()
	with open(path,'w') as fw:
		fw.write(documentary)
		pass
	pass
# Create a dictionary for each of caption
def groupby_caption(imageIDs,clean_captions):
	caption_dict={}
	n=len(imageIDs)
	for i in range(n):
		imageID=imageIDs[i]
		if imageID in caption_dict:
			caption_dict[imageID].append(clean_captions[i])
		else:
			caption_dict[imageID]=[clean_captions[i]]
		pass
	return caption_dict
	pass
def save_document(caption_dict,path):
	pickle.dump(caption_dict,open(path,'wb'))
	pass
def getImageID_train(path):
	captionIDs=[]
	with open(path,'r') as fr:
		cptIDs=fr.read()
		pass
	captionIDs=cptIDs.strip().split('\n')
	imgIDs=get_imageIDs(captionIDs)
	return imgIDs
	pass
def saveImageID_train(imgIDs,path):
	sequence=''
	for img in imgIDs:
		sequence+=(img+' ')
		pass
	sequence=sequence.strip()
	with open(path,'w') as fw:
		fw.write(sequence)
		pass
	pass
# Create dictionary about index of each word in captions
def word_to_idx(clean_captions):
	vocabul={}
	# vocab is used to save vocabulary temporarily 
	vocab=[]
	index=-1
	# Create vocabulary
	for caption in clean_captions:
		for word in caption.split():
			if(word in vocabul):
				continue
			index+=1
			# Sort dictionary alphabetically (insertion sort)
			vocabul[word]=index
			vocab.append(word)
			vocab.sort()
		pass
	vocabulary={}
	for i in range(len(vocab)):
		vocabulary[vocab[i]]=i+1
		pass
	return vocabulary,vocab
	pass
def save_idx2word(vocabulary,path):
	idx2word={}
	for key,value in vocabulary.items():
		idx2word[value]=key
		pass
	pickle.dump(idx2word,open(path,'wb'))
	pass
def save_vocabulary(vocabulary,path):
	sequence=''
	for word in vocabulary:
		sequence+=(word+' ')
		pass
	sequence=sequence.strip()
	with open(path,'w') as fw:
		fw.write(sequence)
		pass
	pass
def save_dictionary(vocabulary,path):
	pickle.dump(vocabulary,open(path,'wb'))
	pass
# get index needed to swap in a list
def getIndexInsertion(seqList,lastIdx):
	j=lastIdx
	i=j-1
	while(seqList[j]<seqList[i]):
		i-=1
	return i
	pass
# Embed a word to vector
# method parameter may be GloVe or Word2vec pretrained model
def load_wordEmbedding_model(model_path,name_model):
	embedding_model={}
	if name_model=='GloVe':
		with open(model_path,'r',encoding='utf-8') as fr:
			for line in fr:
				split_line=line.split()
				word=split_line[0]
				vector=split_line[1:]
				vector=np.array(vector)
				vector.astype(np.float)
				embedding_model[word]=vector
			pass
		pass
	elif name_model=='Word2vec':
		print('uncomplete')
	return embedding_model
	pass
def word_embedding(vocab,embedding_model):
	embedding_dict={}
	embedding_dim=200
	for word in vocab:
		if not(word in embedding_model):
			embedding_dict[word]=np.zeros(embedding_dim)
		else:
			embedding_dict[word]=embedding_model[word]
		pass
	return embedding_dict
	pass
def compute_max_length(caption_dict):
	max_length=0
	for key,value in caption_dict.items():
		for caption in value:
			length=len(caption.split())
			if(length>max_length):
				max_length=length
		pass
	return max_length
	pass
# convert caption to list index of word
def convert_caption(caption_dict,vocabulary,max_length):
	index_caption={}
	for key,value in caption_dict.items():
		list_caption=[]
		for caption in value:
			list_token=[]
			split_caption=caption.split()
			for word in split_caption:
				list_token.append(vocabulary[word])
			list_caption.append(list_token)
			pass
		index_caption[key]=list_caption
	return index_caption
	pass
def save_idx_caption(index_caption,path):
	pickle.dump(index_caption,open(path,'wb'))
	pass
#
def save_idx_train(imgTrain,index_caption,path):
	idx_train={}
	for img_id in imgTrain:
		idx_train[img_id]=index_caption[img_id]
		pass
	pickle.dump(idx_train,open(path,'wb'))
	pass
def save_wordembedding(embedding_dict,path):
	pickle.dump(embedding_dict,open(path,'wb'))
	pass
def save_embedding_model(embedding_model,path):
	pickle.dump(embedding_model,open(path,'wb'))
	pass
def save_max_length(max_length,path):
	with open(path,'w') as fw:
		fw.write(str(max_length))
	pass
if __name__=='__main__':
	data=load_capt_data('../Data Set/Flickr8k_text/Flickr8k.token.txt')
	# print(data)
	captionIDs,raw_captions=split_imgandcapt(data)
	imageIDs=get_imageIDs(captionIDs)
	clean_captions=get_clean_captions(raw_captions)
	# save_path='../Data Set/Cleaned Data/Clean_Caption.txt'
	# save_captions(imageIDs,clean_captions,save_path)
	imgTrain=getImageID_train('../Data Set/Flickr8k_text/Flickr_8k.trainImages.txt')
	# saveImageID_train(imgTrain,'../Data Set/Cleaned Data/ImageIdTrain.txt')
	caption_dict=groupby_caption(imageIDs,clean_captions)
	max_length=compute_max_length(caption_dict)
	save_max_length(max_length,'../Data Set/Cleaned Data/max_length.txt')
	vocabulary,vocab=word_to_idx(clean_captions)
	# save_vocabulary(vocab,'../Data Set/Cleaned Data/Vocabulary.txt')
	# save_document(caption_dict,'../Data Set/Cleaned Data/Document Caption.pickle')
	# save_dictionary(vocabulary,'../Data Set/Cleaned Data/Dictionary.pickle')
	# embedding_model=load_wordEmbedding_model('../Pretrained Model/glove.twitter.27B/glove.twitter.27B.200d.txt','GloVe')
	# embedding_dict=word_embedding(vocab,embedding_model)
	# save_wordembedding(embedding_dict,'../Data Set/Cleaned Data/Embedding Dictionary.pickle')
	index_caption=convert_caption(caption_dict,vocabulary,max_length)
	# save_idx_caption(index_caption,'../Data Set/Cleaned Data/Index Caption.pickle')
	# save_idx_train(imgTrain,index_caption,'../Data Set/Cleaned Data/Index Train.pickle')
	imgTest=getImageID_train('../Data Set/Flickr8k_text/Flickr_8k.testImages.txt')
	# saveImageID_train(imgTrain,'../Data Set/Cleaned Data/ImageIdTest.txt')
	# save_idx_train(imgTrain,index_caption,'../Data Set/Cleaned Data/Index Test.pickle')