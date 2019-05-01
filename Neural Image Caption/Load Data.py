import pickle
class Data_Loader():
	"""docstring for Data_Loader"""
	# doc_path: path to folder contain document that is formated as (img_id: list of index word in each caption)
	# dict_path: dictionary path
	def __init__(self, doc_path, dict_path,vocab_path, train_path, test_path):
		# super(Data_Loader, self).__init__()
		self.doc_path = doc_path
		self.dict_path = dict_path
		self.vocab_path = vocab_path
		self.train_path = train_path
		self.test_path = test_path
		self.document={}
		self.vocabulary=None
		self.dictionary={}
		self.idx2word={}
		self.img_train_ftr={}
		self.img_test_ftr={}
		self.idx_train={}
		self.idx_test={}
	def load_document(self):
		self.document=pickle.load(open(self.doc_path,'rb'))
		pass
	def get_max_length(self,path):
		with open(path,'r') as fr:
			maxlength=fr.read()
		maxlength=int(maxlength)	
		return maxlength
		pass
	def get_vocab_size(self):
		self.vocab_size=len(self.dictionary)
		pass
	def tokenize_caption(self,list_caption):
		token_caption=[]
		for caption in list_caption:
			all_word=caption.split()
			token_caption.append[allword]
			pass
		return token_caption
		pass
	# return a list of index of words in caption
	# name set is train or test
	def get_index_caption(self,name_set):
		if name_set=='train':
			self.idx_train=pickle.load(open(self.train_path,'rb'))
		else:
			self.idx_test=pickle.load(open(self.test_path,'rb'))
		pass
	# word to index
	def get_dictionary(self):
		self.dictionary=pickle.load(open(self.dict_path,'rb'))
		pass
	# index to word
	def get_index2word(self):
		for key,value in self.dictionary.items():
			self.idx2word[value]=key
		pass
	# Create 
	def get_img_feature(self,name_dataset):
		feature_path=''
		if name_dataset=='train':
			feature_path=self.train_path
			self.img_train_ftr=pickle.load(open(feature_path,'rb'))
		else:
			feature_path=self.test_path
			img_test_ftr=pickle.load(open(feature_path,'rb'))
		pass
	def get_img_name(self,path,name):
		with open(path,'r') as fr:
			f=fr.read()
			pass
		img_name=f.strip().split()
		return img_name
		pass
	pass
	# def load_embedding_dict(self,path):
	# 	self.embedding_dict=pickle.load(open(path,'rb'))
	# 	pass
if __name__ == '__main__':
	# test data loader
	root_path='../Data Set/Cleaned Data/'
	doc_path=root_path+'Document Caption.pickle' 
	dict_path=root_path+'Dictionary.pickle'
	vocab_path=root_path+'Vocabulary.txt'
	train_path=root_path+'Index Train.pickle'
	test_path=root_path+'Index Test.pickle'
	data_loader=Data_Loader(doc_path,dict_path,vocab_path,train_path,test_path)
	data_loader.get_dictionary()
	data_loader.get_index2word()
	data_loader.get_index_caption('test')
	print(data_loader.get_img_name('../Data Set/Cleaned Data/ImageIdTest.txt','test'))
	print(data_loader.idx_test)