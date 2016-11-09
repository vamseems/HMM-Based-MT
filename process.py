import re
matrix = {}
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

		for k in xrange(0, len(english_tokens)):
			english_token = english_tokens[k].split('\\')[0]
			english_pos = english_tokens[k].split('\\')[1]

			for l in xrange(0, len(hindi_tokens)):
				hindi_nothindi = hindi_tokens[l].split('\\')
				if(len(hindi_nothindi)==1):
					
					hindi_pos = re.findall('[A-Z _]{1,}', hindi_tokens[l])
					hindi_token = re.split('[A-Z _]{2,}', hindi_tokens[l])[0]

				else:
					hindi_pos = hindi_tokens[l].split('\\')[1]
					hindi_token = hindi_tokens[l].split('\\')[0]


				# print english_token,english_pos,hindi_token,hindi_pos,i,j

				if english_pos == '.' or english_pos == ',' or hindi_pos == 'RD_PUNC' or hindi_pos == 'RD_SYM':
					continue
		

				try:
				    matrix[english_token][hindi_token] += 1
				except KeyError:
					if english_token in matrix:
						matrix[english_token][hindi_token] = 1
					else:
						matrix[english_token] = {}
						matrix[english_token][hindi_token] = 1