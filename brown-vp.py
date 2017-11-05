'''This script extracts verb phrases from Brown corpus'''

import nltk
from nltk.corpus import BracketParseCorpusReader
import numpy as np
import scipy
from scipy import spatial
import matplotlib.pyplot as plt
import math

corpus_root = r"all/"
file_pattern= r".*\.mrg"

sw = BracketParseCorpusReader(corpus_root, file_pattern)


trees = sw.parsed_sents()




def filter(tree):
	child_nodes=[child.label() for child in tree if isinstance(child, nltk.Tree)]
	return (tree.label() == 'VP')
   
#	return (tree.label() == 'VP') and ('PP' in [node for node in child_nodes])

all_vp = []
for vp in [subtree for tree in trees for subtree in tree.subtrees(filter)]:
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

		a.append(pps)
	if len(pps) == 2:
		sent = []
		for child in vp:
			for word in child.leaves():
				if '*' not in word:
					if ' 0' not in word:
						if word != '0':
							sent.append(word)
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
for vp in all_vp:
#	print(tok)

	a = []
	a.append(vp[-1])
	pp1 = vp[0][0].split()
	for tok in pp1[:]:
		if tok.startswith('\\'):
			pp1.remove(tok)
	a.append(pp1)
	a.append(vp[2])
	A.append(a)


for vp in all_vp:
	b = []
	b.append(vp[-1])
	pp2=vp[1][0].split()
	for tok in pp2[:]:
		if tok.startswith('\\'):
			pp2.remove(tok)
	b.append(pp2)
	b.append(vp[2])
	B.append(b)


for tok in zip(A, B):
	if len(tok[0][1]) > 1:
		if len(tok[1][1]) > 1:
#			print([tok[0][0], tok[0][1], tok[1][1]])
#			print(' '.join(w for w in tok[0][0]))
#			print(' '.join(w for w in tok[1][1]))
#			print(' '.join(w for w in tok[0][1]))



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
					
print(short_before_long)
print(long_before_short)
print(equal)
print(MP)
print(MT)
print(PT)
print(PM)
print(TM)
print(TP)			

