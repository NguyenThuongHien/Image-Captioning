import numpy as np
from keras.utils import Sequence
from Load Data import Data_Loader
from Generator import My_Generator
import NIC
def main():
	# parameter for init data loader
	root_path='../Data Set/Cleaned Data/'
	doc_path=root_path+'Document Caption.pickle' 
	dict_path=root_path+'Dictionary.pickle'
	vocab_path=root_path+'Vocabulary.txt'
	train_path=root_path+'Index Train.pickle'
	test_path=root_path+'Index Test.pickle'
	data_loader=Data_Loader(doc_path,dict_path,vocab_path,train_path,test_path)
	# parameter to init my generator
	caption_dict=
	img_feature=
	img_name=
	max_length=
	size_vocb=
	no_sample=
	my_generator=My_Generator(caption_dict,img_feature,img_name,max_length,size_vocb,no_sample)
	pass
if __name__ == '__main__':
	main()