import stop_list
import math
import re
import sys

# NOTE: for tokenization I used the built in .split(' ') method

regex = re.compile(r'([0-9]+)|([\.,\?\!\(\)\[\]\/])')	# regex used to remove numbers and punctuation
stoplist = stop_list.closed_class_stop_words	# list of stop words

###########################################################################
# FORMULAE
###########################################################################

# INVERSE DOCUMENT FREQUENCY
def idf(i, c):
	n = len(c)	# total number of documents in collection c
	n_i = 0		# number of documents where term i occurs

	for (k, j) in c.items():
		if i in j:
			n_i += 1	# add to n_i the number of times term i occurs in the current document (j)

	if n_i == 0 or n == 0:
		return 0

	res = math.log(n / n_i)
	return res

# TERM FREQUENCY
def tf(i, j):	# find frequency of term i in document j
	return j.count(i)

# COSINE SIMILARITY: following the tf-idf weighted cosine (equation 23.12 in Jurafsky and Martin)
def cosine_similarity(qFeature, dFeature, comp):

	numerator = 0
	denomQ = 0
	denomD = 0

	for (term, score) in qFeature.items():
		denomQ += (score * score)

	if denomQ == 0:	# short circuit
		return 0

	for (term, score) in dFeature.items():
		denomD += (score * score)

	if denomD == 0:	# short circuit
		return 0

	for (term, score) in comp.items():
		if score == 0:
			continue
		numerator += (score * dFeature[term])	# summation (tf(w, q) * tf(w, d) * idf(w)^2)


	denominator = math.sqrt(denomQ) * math.sqrt(denomD)

	return numerator / denominator



###########################################################################


# generate collection of documents from input file
def generate_collection(filepath):
	collection = dict()
	lines = []

	with open(filepath, 'r') as f:
		for line in f:
			lines.append(line)


	isContent = False
	currentDoc = None

	for line in lines:
		if ".I" in line:
			isContent = False
			lst = line.split(' ')
			currentDoc = int(lst[1].replace('\n', ''))
			collection[currentDoc] = []
			continue
		if ".W" in line:
			isContent = True
			continue
		if isContent:
			if ".I" not in line:
				line = regex.sub('', line)
				collection[currentDoc].append(line)
			continue

	for k in collection.iterkeys():
		collection[k] = (' ').join(collection[k])

	return collection


# 2. For each query, create a feature vector representing the words in the query:
def generate_feature_vector(tfScores, idfScores):	# generate map of unique words (and their corresponding tf-idf values) in the document given by docID

	feature_vec = dict()

	for (docid, docvec) in tfScores.items():
		feature_vec[docid] = dict()
		for (term, score) in docvec.items():
			feature_vec[docid][term] = score * idfScores[term]

	return feature_vec


# 3. Compute the IDF scores for each word in the collection of abstracts
def idf_dict(collection):

	scores = dict()	# map of idf scores

	for doc in collection.values():

		for term in doc.split(' '):
			if term == '' or term in stoplist or term in scores:
				continue	# don't add any empty strings, stop words or words that are already present
			scores[term] = idf(term, collection)

	return scores

# 4. Count the number of instances of each non-stop-word in each abstract
def tf_dict(collection):

	scores = dict()

	for (i, w) in collection.items():
		scores[i] = dict()

		for term in w.split(' '):
			if term == '' or term in stoplist or term in scores[i]:
				continue
			scores[i][term] = tf(term, w)

	return scores 	# return nested dictionary mapping a dictionary of unique words and their tf scores to each document id in collection


# run the final program, returns output dict
def final_scores(queryfile, abstractfile):
	abstracts = generate_collection(abstractfile)
	queries = generate_collection(queryfile)

	qTF = tf_dict(queries)
	qIDF = idf_dict(queries)

	aTF = tf_dict(abstracts)
	aIDF = idf_dict(abstracts)

	queryvec = generate_feature_vector(qTF, qIDF)
	abstractvec = generate_feature_vector(aTF, aIDF)

	finalvec = dict()

	for (i, q) in queryvec.items():		# for each query in queryvec

		finalvec[i] = []

		for (j, a) in abstractvec.items():	# for each abstract in abstractvec
			comp = compare_vector(qTF[i], a, aIDF)	# tfidf scores of all common words in both abstract a and query q
			similarity = cosine_similarity(q, a, comp)

			finalvec[i].append((j, similarity))
		finalvec[i] = sorted(finalvec[i], key=lambda x: x[1], reverse=True)

	return finalvec


# generate vector of term scores by comparing a query to an abstract
def compare_vector(qtf, aVec, aidf):	# compare feature vec and abstract vec
	new_vec = dict()				# query vec should just be list of words??
	for (word, score) in qtf.items():
		if word in aVec.keys():
			new_vec[word] = score * aidf[word]
			continue
		new_vec[word] = 0

	return new_vec


####################################################################

queryfile = sys.argv[1]
abstractfile = sys.argv[2]

outputfile = sys.argv[3]

vector = final_scores(queryfile, abstractfile)

with open(outputfile, 'w') as f:
	for (q, vec) in vector.items():
		for (a, sim) in vec:
			f.write("%d %d %f\n" % (q, a, sim))




