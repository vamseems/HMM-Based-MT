import re
import operator
import math
n_states=5
matrix = {}
count=0
hindibigram_matrix = {}
english_frequencies={}
hindi_frequencies={}
vertbi_mat={}
for i in xrange(1, 26):
	idx = str(i)
	
	if len(idx) == 1:
		idx = '0' + idx
	
	english = './data/eng_tourism_set' + idx + '.txt'
	hindi = './data/hin_tourism_set' + idx + '.txt'
	
	english_lines = tuple(open(english, 'r'))
	hindi_lines = tuple(open(hindi, 'r'))
	for j in xrange(1, len(english_lines)):
		english_tokens = english_lines[j].split()
		hindi_tokens = hindi_lines[j].split()

		hindi_tokens = hindi_tokens[1:]
		english_tokens = english_tokens[1:]
		flag_hindicount=0
		for k in xrange(0, len(english_tokens)):
			english_token = english_tokens[k].split('\\')[0]
			english_pos = english_tokens[k].split('\\')[1]
			prev = None
			try:
				english_frequencies[english_token]+= 1
			except KeyError:
				english_frequencies[english_token]= 1
			prev = None
			for l in xrange(0, len(hindi_tokens)):
				if flag_hindicount==0:
					hindi_nothindi = hindi_tokens[l].split('\\')
					if(len(hindi_nothindi)==1):
						
						hindi_pos = re.findall('[A-Z _]{1,}', hindi_tokens[l])
						hindi_token = re.split('[A-Z _]{2,}', hindi_tokens[l])[0]

					else:
						hindi_pos = hindi_tokens[l].split('\\')[1]
						hindi_token = hindi_tokens[l].split('\\')[0]


					# print english_token,english_pos,hindi_token,hindi_pos,i,j

					if english_pos == '.' or english_pos == ',' :
						continue
					else:
						try:
							hindi_frequencies[hindi_token]+= 1
						except KeyError:
							hindi_frequencies[hindi_token]= 1
						if prev is not None:
							count+= 1
							try:
								hindibigram_matrix[prev][hindi_token] += 1
							except KeyError:
								if prev in hindibigram_matrix:
									hindibigram_matrix[prev][hindi_token] = 1
								else:
									hindibigram_matrix[prev] = {}
									hindibigram_matrix[prev][hindi_token] = 1
							prev=hindi_token	
						else:
							pass
				if hindi_pos == 'RD_PUNC' or hindi_pos == 'RD_SYM':
						continue
				try:
					matrix[english_token][hindi_token] += 1
				except KeyError:
					if english_token in matrix:
						matrix[english_token][hindi_token] = 1
					else:
						matrix[english_token] = {}
						matrix[english_token][hindi_token] = 1				
			flag_hindicount=1
	for i in matrix:
		if len(matrix[i])>=n_states:
			matrix[i]=dict(sorted(matrix[i].iteritems(), key=operator.itemgetter(1),reverse=True)[:n_states])
# print hindibigram_matrix
test_inp = raw_input("Type some english sentence.")
prev=None
flag=0
def dp(mat,val,test_mat,out,i):
	score=mat[test_mat[val]][i]
	if val==0:
		return mat[test_mat[0]][i]
	else:
		for j in mat[test_mat[val-1]]:
			try:
				no_bigrams=(-(math.log(float(hindibigram_matrix[j][i])/count)))
				# print hindibigram_matrix[j][i]
				# print str(j)+"jndajcn"+str(i)
			except KeyError:
				no_bigrams = -100000000
			if no_bigrams is None:
				no_bigrams = -100000000
			if flag==1:
				score= mat[test_mat[val]][i]+mat[test_mat[val-1]][j]+ no_bigrams
			else:
				value=dp(mat,val-1,test_mat,out,j)
				# print str(value) + "        "+str(val-1)+ "           "+str(j)
				score= mat[test_mat[val]][i]+value+ no_bigrams
			# for k in hindibigram_matrix[j]:
			print j
			out[0]=j
			# print score
			if score > mat[test_mat[val]][i]:
				maximum=score
				out[val]=i
				# print i
				# print i
				if (val-1)==0:
					out[0]=j
		mat[test_mat[val]][i]=score
		return mat[test_mat[val]][i]






		# dp[mat,val-1,test_mat]
def translate(test_inp):
	test_mat= test_inp.split()
	out=[None]*len(test_mat)
	# print test_mat
	for i in test_mat:
		# print i
		vertbi_mat[i]={}
		# print matrix[i]
		# print matrix[i]
		vertbi_mat[i] = matrix[i]
		for j in vertbi_mat[i]:
			# print str(hindi_frequencies[j]) + "jkdbashkdbhks"
			# print j
			vertbi_mat[i][j]= - math.log(float(vertbi_mat[i][j])/hindi_frequencies[j])
	val=len(vertbi_mat)-1
	ind=test_mat[len(test_mat) -1]
	print vertbi_mat
	for i in vertbi_mat[ind]:
		# print vertbi_mat	
		# print test_mat[val]
		prev=None
		dp(vertbi_mat,val,test_mat,out,i)
		flag=1
		# for i in out:
		# 	print i
translate(test_inp)

	# def emission_prob(word):
# 	max= 0
# 	for i in matrix[word]:
# 		print i
# 		hindi_word= i
# 		print matrix[word][i]
# 		print hindi_frequencies[i]
# 		val=float(matrix[word][i])/hindi_frequencies[i]
# 		print val
# 		if max < val:
# 			max=val
# 			hindi_word = i
# 	max= -(math.log(max))
# 	return (max,hindi_word)
# print emission_prob("my")




# print matrix