class Evaluator():
	"""docstring for Evaluator"""
	# cand_ref_set: is a dictionary formated as key: candidate sentence , value : reference set
	def __init__(self, candidate_corpus,reference_corpus):
		# super(Evaluator, self).__init__()
		self.candidate_corpus=candidate_corpus
		self.reference_corpus=reference_corpus
	def tokenize(self,sentences):
		word_set=[]
		for sentence in sentences:
			token_sent=[token.strip() for token in sentence.split()]
			word_set.append(token_sent)
		return word_set
		pass
	def get_ngram(self,max_gram,segment):
		from collections import Counter
		n=len(segment)
		count=Counter()
		for gram in range(1,max_gram+1):
			for i in range(n-gram+1):
				ngram=tuple(segment[i:i+gram])
				count[ngram]+=1
			pass
		return count
		pass
	def get_bleu(self,max_gram,smooth=True):
		from collections import Counter
		# all variable name is named acording to paper about blue
		c=0
		r=0
		total_cand_ngram=[0]*max_gram
		total_count_clip=[0]*max_gram
		for cand_set,ref_set in zip(self.candidate_corpus,self.reference_corpus):
			c+=len(cand_set)
			ref_length=[len(ref) for ref in ref_set]
			r+=min(ref_length)
			max_ngram_ref=Counter()
			count_ngram_cand=self.get_ngram(max_gram,cand_set)
			for ref in ref_set:
				max_ngram_ref |= self.get_ngram(max_gram,ref)
			min_match_cand = count_ngram_cand & max_ngram_ref
			# print(max_ngram_ref)
			# print(min_match_cand)
			for key,value in count_ngram_cand.items():
				total_cand_ngram[len(key)-1]+=value
			for key,value in min_match_cand.items():
				total_count_clip[len(key)-1]+=value
			pass
		pn=[0]*max_gram
		if smooth is True:
			for i in range(max_gram):
				pn[i]=float((total_count_clip[i]+1.)/(total_cand_ngram[i]+1.))
		else:
			for i in range(max_gram):
				if total_count_clip[i]==0:
					pn[i]=0.
					return 0.,0.
				else:
					pn[i]=float(total_count_clip[i]/total_cand_ngram[i])
		# print(pn)
		bp=min(1-r/c,0.)
		import math
		precision=1.0/max_gram
		log_sum_pn=0.
		for i in range(max_gram):
			log_sum_pn+=math.log(pn[i])
		precision*=log_sum_pn
		log_bleu=bp+precision
		bleu_score=math.exp(log_bleu)
		return bleu_score,log_bleu
		pass
	# get all n_gram
	# total length of all min ref sentence r
	# total c
	# pn :  total min of same n_gram between candidate and each ref, total n_gram in candidate corpus
def test(candidate_corpus,ref_corpus):
	evaluator=Evaluator(candidate_corpus,ref_corpus)
	bleu=evaluator.get_bleu(4,False)
	print(bleu)
	pass
if __name__ == '__main__':
	cdd=[['the','cat'],['the','cat','is','on','the','mat','a']]
	ref=[[['the','cat','is','on','the','mat'],['the','is','a','cat','on','the','mat']],[['the','cat','is','on','the','mat'],['there','is','a','cat','on','the','mat']]]
	test(cdd,ref)