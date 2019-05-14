from keras.applications.inception_v3 import preprocess_input
from keras.applications.inception_v3 import InceptionV3
from keras.preprocessing import image
from keras.models import Model
from os import listdir
import numpy as np
import h5py
from PIL import Image
import pickle
class FeatureExtractor(object):
	"""docstring for FeatureExacter"""
	def __init__(self, img_path='',base_model=None,name_model=''):
		# super(FeatureExacter, self).__init__()
		self.img_path=img_path
		self.base_model=base_model
		self.name_model=name_model
	def initiate_model(self):
		model=None
		if self.name_model=='InceptionV3':
			model=InceptionV3(include_top=True,weights='imagenet')
			baseModel=Model(model.input, model.layers[-2].output)
		if self.name_model=='VGG16':
			# from applications.vgg16 import VGG16
			model=VGG16(include_top=False,weights='imagenet')
			pass
		self.base_model=baseModel
		pass
	def preprocess_img(self,img_name):
		image_path=(self.img_path)+'/'+img_name
		images=image.load_img(image_path, target_size=(299,299))
		images=image.img_to_array(images)
		images=np.expand_dims(images,axis=0)
		images=preprocess_input(images)
		return images
		pass
	def get_feature(self,image_name):
		if(self.base_model is None):
			return None
		else:
			img=self.preprocess_img(image_name)
			feature=(self.base_model).predict(img)
			feature=np.reshape(feature,feature.shape[1])
			return feature
			pass
		pass
	def get_feature_from_list(self,cluster_i):
		if self.base_model is None:
			return None
		else:
			features=[]
			for image_name in cluster_i:
				ftr=self.get_feature(image_name)
				features.append(ftr)
				pass
			return features
		pass
	def divide_dataset(self):
		all_files=listdir(self.img_path)
		print(all_files)
		cluster=[[],[],[],[]]
		n=len(all_files)
		no_element=int(n/4)
		for i in range(4):
			if (i+1)*no_element <= n:
				cluster[i]=all_files[(i*no_element):((i+1)*no_element)]
			else:
				cluster[i]=all_files[i*no_element:n]
			pass
		return cluster
		pass
	def save_feature(self,save_path,cluster_i):
		encoding_file={}
		features=self.get_feature_from_list(cluster_i)
		all_files=listdir(self.img_path)
		for i,name_img in enumerate(cluster_i):
			encoding_file[name_img]=features[i]
			pass
		pickle.dump(encoding_file,open(save_path,'wb'))
		pass
if __name__ == '__main__':
	featurer=FeatureExtractor(img_path='../Data Set/Flickr8k_image/Flicker8k_Dataset',name_model='InceptionV3')
	featurer.initiate_model()
	cluster=featurer.divide_dataset()
	featurer.save_feature('../Data Set/Image Feature/Train.pickle',cluster[2])
