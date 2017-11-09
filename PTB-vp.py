'''This script extracts verb phrases with two PP obliques from Penn treebank'''

import nltk
from nltk.corpus import BracketParseCorpusReader
import numpy as np
import scipy
from scipy import spatial
import matplotlib.pyplot as plt
import math
import re
import sys
import csv

corpus_root = r"all/"
file_pattern= r".*\.mrg"

sw = BracketParseCorpusReader(corpus_root, file_pattern)


trees = sw.parsed_sents()




def give(t):
	return t.label() == 'VP'

all_vp = []

for tree in trees:
	for vp in tree.subtrees(give):
		children = []
		pps = []
		pp = []
		for child in vp:
			if 'PP' in child.label():
				np = []
				labels = []
				for tok in child:
					labels.append(tok.label())
					if 'NP' in tok.label():
						np.append(tok.label())
				if len(np) >= 1:
					if 'VB' not in labels[0]:
						pps.append(child.label())
			
		if len(pps) == 2:
			a = []
			sent=[]
			verb_phrase = []
			for word in tree.leaves():
				if '*' not in word:
					if ' 0' not in word:
						if word != '0':
							sent.append(word)
			for child in vp:
				
				if 'PP' in child.label():
					np = []
					labels = []
					for tok in child:
						labels.append(tok.label())
						if 'NP' in tok.label():
							np.append(tok.label())
					if len(np) >= 1:
						if 'VB' not in labels[0]:
							pp = []
							for word in child.leaves():
								if '*' not in word:
									if ' 0' not in word:
										if word != '0':
											pp.append(word)
							new_pp = ' '.join(word for word in pp)
							a.append([new_pp, len(pp)])
							verb_phrase.append([new_pp, len(pp)])
				else:
					
					for word in child.leaves():
						if '*' not in word:
							if ' 0' not in word:
								if word != '0':
									verb_phrase.append([word])

			a.append(pps)
			a.append(verb_phrase)
			a.append(sent)
			all_vp.append(a)


short_before_long = 0
long_before_short = 0
equal = 0
MP = 0
MT = 0
PT = 0
PM = 0
TM = 0
TP = 0


A=[]
B=[]
for tok in all_vp:
	vp = []
	for item in tok[3]:
		vp.append(item[0])
	new_vp = ' '.join(word for word in vp)
	reverse_vp = []
	pps = []
	for item in tok[3]:
		if len(item) !=1:
			pps.append(item)
	pp1_id, pp2_id = tok[3].index(pps[0]), tok[3].index(pps[1])
	tok[3][pp1_id], tok[3][pp2_id] = tok[3][pp2_id], tok[3][pp1_id]
	for item in tok[3]:
		reverse_vp.append(item[0])

	new_reverse_vp = ' '.join(word for word in reverse_vp)

	sent = ' '.join(word for word in tok[-1])
	new_sent = re.sub(new_vp, new_reverse_vp, sent)
	tok.append(new_sent.split())
#	print([sent, new_vp, new_reverse_vp])
#	print(new_sent)

for tok in all_vp:
	a = []
	for item in tok[-1][:]:
		if item.startswith('\\'):
			tok[-1].remove(item)
	a.append(tok[-1])
	pp1 = tok[0][0].split()
	for item in pp1[:]:
		if item.startswith('\\'):
			pp1.remove(item)
	a.append(pp1)
	a.append(tok[2])
	for item in tok[-2][:]:
		if item.startswith('\\'):
			tok[-2].remove(item)
	a.append(tok[-2])
	A.append(a)



for tok in all_vp:
	b = []
	for item in tok[-1][:]:
		if item.startswith('\\'):
			tok[-1].remove(item)
	b.append(tok[-1])
	pp2=tok[1][0].split()
	for item in pp2[:]:
		if item.startswith('\\'):
			pp2.remove(item)
	b.append(pp2)
	b.append(tok[2])
	for item in tok[-2][:]:
		if item.startswith('\\'):
			tok[-2].remove(item)
	b.append(tok[-2])
	B.append(b)

header = ['Sentence', 'Reverse_sentence', 'PP1', 'PP2', 'PP1-len', 'PP2-len']

with open(sys.argv[1] + '-vp-data.csv', 'w')  as data:
	writer = csv.writer(data)
	writer.writerow(header)

	for tok in zip(A, B):
		if len(tok[0][1]) > 1:
			if len(tok[1][1]) > 1:

				reverse_sent = ' '.join(w for w in tok[0][0])
				reverse_sent = re.sub(r'-LCB-', '(', reverse_sent)
				reverse_sent = re.sub(r'-LRB', '(', reverse_sent)
				reverse_sent = re.sub(r'-RRB-', ')', reverse_sent)
				reverse_sent = re.sub(r'-RCB-', ')', reverse_sent)

				sent = ' '.join(w for w in tok[0][-1])
				sent = re.sub(r'-LCB-', '(', sent)
				sent = re.sub(r'-LRB', '(', sent)
				sent = re.sub(r'-RRB-', ')', sent)
				sent = re.sub(r'-RCB-', ')', sent)


				pp1 = ' '.join(w for w in tok[0][1])
				pp1 = re.sub(r'-LCB-', '(', pp1)
				pp1 = re.sub(r'-LRB', '(', pp1)
				pp1 = re.sub(r'-RRB-', ')', pp1)
				pp1 = re.sub(r'-RCB-', ')', pp1)

				pp2 = ' '.join(w for w in tok[1][1])
				pp2 = re.sub(r'-LCB-', '(', pp2)
				pp2 = re.sub(r'-LRB', '(', pp2)
				pp2 = re.sub(r'-RRB-', ')', pp2)
				pp2 = re.sub(r'-RCB-', ')', pp2)

				writer.writerow([reverse_sent, sent, pp1, pp2, len(pp1.split()), len(pp2.split())])

		#		print(reverse_sent)
		#		print(sent)
		#		print(pp1)
		#		print(pp2)

				if len(tok[0][1]) < len(tok[1][1]):
					short_before_long += 1
				if len(tok[0][1]) > len(tok[1][1]):
					long_before_short += 1
				if len(tok[0][1]) == len(tok[1][1]):
					equal += 1
				if tok[0][2] == ['PP-MNR', 'PP-LOC']:
					MP += 1
				if tok[0][2] == ['PP-MNR', 'PP-TMP']:
					MT += 1
				if tok[0][2] == ['PP-LOC', 'PP-TMP']:
					PT += 1
				if tok[0][2] == ['PP-LOC', 'PP-MNR']:
					PM += 1
				if tok[0][2] == ['PP-TMP', 'PP-MNR']:
					TM += 1
				if tok[0][2] == "['PP-TMP', 'PP-LOC']":
					TP += 1


'''					
print(short_before_long)
print(long_before_short)
print(equal)
print(MP)
print(MT)
print(PT)
print(PM)
print(TM)
print(TP)			
'''

		
