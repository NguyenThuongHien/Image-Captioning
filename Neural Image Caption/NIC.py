# Need import Image Featurer
from keras import Dense,Input,LSTM,Dropout,Embedding
from keras.models import Model
import pickle
import numpy as np
class CaptionGenerator(object):
	"""docstring for ClassName"""
	def __init__(self,model_path='',model=None,max_length=34,vocab_size=8000,n_epoch=10,n_batch=20
					,image_featurer=None,cpt_featurer=None,generator=None):
		# super(ClassName, self).__init__()
		self.model_path = model_path
		self.model=model
		self.max_length=max_length
		self.vocab_size=vocab_size
		self.n_epoch = n_epoch
		self.n_batch = n_batch
		self.image_featurer=image_featurer
		self.cpt_featurer=cpt_featurer
		self.generator=generator
	def get_cpt_feature(self):
		feature=self.cpt_featurer.get_feature()
		pass
	# get image feature of new image out of dataset(train & test)
	def get_img_feature(self):
		feature=self.image_featurer.get_feature()
		return feature
		pass
	def build_model(self):
		# input caption part
		# shape_caption=self.max_length*200
		input1=Input(shape=(self.max_length,))
		e=Embedding(self.vocab_size,256,mask_zero=True)(input1)
		x11=Dropout(0.5)(e)
		x12=LSTM(shape=(256))(x11)
		# input image part
		input2=Input(shape=2048)
		x21=Dropout(0.5)(input2)
		x22=Dense(256,activation='relu')(x21)
		# decoder (feed forward) model
		# merge 2 part
		decoder1 = add([x12, x22])
		decoder2 = Dense(256, activation='relu')(decoder1)
		output = Dense(self.vocab_size, activation='softmax')(decoder2)
		# get model
		self.model=Model(inputs=[inputs1, inputs2], outputs=output)
		self.model.compile(loss='categorical_crossentropy', optimizer='adam')
		# plot model
		print(model.summary())
		plot_model(model, to_file='model.png', show_shapes=True)
		pass
	def train(self):
		# Need to improve by using validation
		self.model.fit_generator(generator=self.generator,epochs=self.n_epoch,verbose=1
			,use_multiprocessing=True,workers=16,max_queue_size=32)
		pass
	def greedy_search(self,X_img,word2idx,idx2word):
		first_token='startseq'
		first_token=word2idx[first_token]
		index_seq=[in_word]
		for i in range(self.max_length):
			zeros=[0 for _ in range(self.max_length-len(index_seq))]
			input_seq=[index_seq]
			input_seq=input_seq.extend(zeros)
			# get probability distribution among word of next word
			yhat=self.model.predict([X_img,input_seq])
			# get index of word have max probability
			next_idx=np.argmax(yhat)
			index_seq.append(next_idx+2)
			# check end token 
			if idx2word[next_idx]=='endseq':
				break
			pass
		return index_seq
		pass
	# beam size is 1 => greedy search
	def beam_search(self,beam_size,X_img,word2idx,idx2word):
		# in_word is index of word input
		first_token='startseq'
		first_token=word2idx[first_token]
		result=[]
		for i in range(self.max_length):
			all_score=[]
			if i==0:
				zeros=[0 for _ in range(self.max_length-1)]
				first_seq=[first_token]
				first_seq.extend(zeros)
				yhat=self.model.predict([X_img,first_seq])
				top_idx=sorted(range(len(yhat)),key=lambda e:yhat[e],reverse=True)[:beam_size]
				for k in range(beam_size):
					score=yhat[top_idx[k]]
					list_word=[top_idx[k]+2]
					result.append([list_word,score])
				continue
			for j in range(beam_size):
				# check whether result[j] have contained end word ('endseq')
				word=index2word(result[j][0][-1:])
				if word=='endseq':
					all_score.append(result[j])
				else:
					# prepare vector index to predict next word
					input_seq,score=list(result[j])
					zeros=[0 for _ in range(self.max_length-len(input_seq))]
					input_seq.extend(zeros)
					# get probability distribution of each word in ouput
					yhat=self.model.predict(X_image,input_seq)
					for k in range(len(yhat)):
						tmp_seq=list(result[j][0])
						tmp_seq.append(k+2)
						new_score=score*yhat[k]
						all_score.append([tmp_seq,new_score])
				pass
			result=sorted(all_score,key=lambda e:e[1],reverse=True)[:beam_size]
			pass
		pass
	def predict(self,X_img,beam_size,word2idx,idx2word):
		predicted_seq=[]
		predicted_sentence=''
		if beam_size==1:
			predicted_seq=self.greedy_search(X_img)
		else:
			predicted_seq=self.beam_search(beam_size,X_img,word2idx,idx2word)
		for token in predicted_seq:
			word=index2word(token)
			predicted_seq+=(' '+word) 
		# remove first whitespace in predicted sentence
		predicted_sentence.strip()
		return predicted_sentence
		pass
	def save_model(self):
		self.model.save_weights(self.model_path)
		pass
	def load_model(self):
		self.model.load_weights(self.model_path)
		pass
	def test(self,img_feature_test,beam_size,word2idx,idx2word):
		caption_predict={}
		for img_name,feature in img_feature_test.items():
				predict_seq=self.predict(feature,beam_size,word2idx,idx2word)
				caption_predict[img_name]=predicted_seq
			pass
		return caption_predict
		pass 
	def evaluate(self):
		pass