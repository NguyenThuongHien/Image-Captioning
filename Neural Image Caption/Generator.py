from keras.utils import Sequence
import numpy as np
class Train_Generator(Sequence):
	"""docstring for My_Generator"""
	# caption_dict is formated as imageID :list(caption)	
	# img_feature is formated as imageID : feature vector
	# max_length is maximum length in all captions
	# no_cpi number captions per image
	# max_length is maximum length of captions
	# size_vocb is vocabulary size
	def __init__(self,caption_dict,img_feature,img_name,max_length,size_vocb,no_sample):
		super(My_Generator, self).__init__()
		self.caption_dict=caption_dict
		self.img_feature=img_feature
		self.img_name=img_name
		self.max_length=max_length
		self.size_vocb=size_vocb
		self.no_sample=no_sample
	def __len__(self):
		return ceil(len(caption_dict)/self.no_sample)
		pass
	def __getitem__(self,idx):
		X1=[]
		X2=[]
		X=[]
		Y=[]
		for i in range(idx*self.no_sample,(idx+1)*self.no_sample):
			# get feature
			ftr=self.img_feature[img_id]
			img_id=self.img_name[i]
			# get X1 and Y
			for caption in self.caption_dict[img_id]:
				n=len(caption)
				for i in range(1,n):
					# input X2
					X2.append(ftr)
					# input X1
					in_seq=caption[:i]
					in_zeros=[0 for _ in range(self.max_length-i)]
					inpt=in_seq.extend(in_zeros)
					X1.append(inpt)
					# output Y
					out=caption[i]
					outpt=[0 for _ in range(self.size_vocb)]
					outpt[out-1]=1
					Y.append(outpt)
					pass
				pass
			pass
		X=[X1,X2]
		return X,Y
		pass
class Test_Generator(Sequence):
	"""docstring for Test_Generator"""
	def __init__(self, arg):
		self.arg = arg
	def __getitem__():
		pass