import sys

def trainHMM(filepath):

	# HMM Matrices
	B = dict()			# probabilities of a certain word being given a certain tag
	A = dict()			# transition probabilities
	Q = []				# sequence of states

	# Raw Data
	wordOcc = dict()	# number of occurrences of each word
	tagOcc = dict()		# number of occurrences of each tag
	pairOcc = dict()	# number of occurrences of each word, tag pairing (nested)
	biOcc = dict()		# number of occurrences of each TAG bigram (nested, [prev][current] = freq)

	wt = [("", "START")]

	with open(filepath, 'r') as f:

		for line in f:
			spl = line.split()

			if len(spl) > 0:
				wt.append((spl[0].lower(), spl[1]))
				continue

			wt.append(("", "END"))	# space between sentences
			wt.append(("", "START"))

	prev = "START"

	for (word, tag) in wt:

		if word not in wordOcc:
			wordOcc[word] = 0

		if tag not in tagOcc:
			tagOcc[tag] = 0

		if word not in pairOcc:
			pairOcc[word] = dict()
			pairOcc[word][tag] = 0
		elif tag not in pairOcc[word]:
			pairOcc[word][tag] = 0

		if prev not in biOcc:
			biOcc[prev] = dict()
			biOcc[prev][tag] = 0
		elif tag not in biOcc[prev]:
			biOcc[prev][tag] = 0

		wordOcc[word] += 1
		tagOcc[tag] += 1
		pairOcc[word][tag] += 1
		biOcc[prev][tag] += 1

		prev = tag

	# set probabilities based on raw data collected from training corpus

	# likelihood matrix (word -> tag probabilities)
	for (tag, freq) in tagOcc.items():

		if tag not in B:
			B[tag] = dict()

		for (word, tags) in pairOcc.items():
			if tag not in tags:
				B[tag][word] = 0
				continue
			B[tag][word] = float(tags[tag]) / freq

	# transition probability matrix (transition probabilities)
	for (prev, tags) in biOcc.items():

		if prev not in A:
			A[prev] = dict()

		for tag in tagOcc.iterkeys():

			if tag not in tags:
				A[prev][tag] = 0
				continue
			prob = float(tags[tag]) / tagOcc[prev]

			A[prev][tag] = prob

	# tag list
	Q = ["START"]
	for tag in tagOcc.iterkeys():
		if tag == "START" or tag == "END":
			continue
		Q.append(tag)
	Q.append("END")
	
	# words with frequency = 1 (for OOV handling)
	U = dict()
	for (word, freq) in wordOcc.items():
		if freq == 1:
			for tag in pairOcc[word].iterkeys():
				if tag not in U:
					U[tag] = 0
				U[tag] += 1

	for (tag, freq) in tagOcc.items():
		if tag not in U:
			U[tag] = float(0)
			continue

		prob = float(U[tag]) / freq
		U[tag] = prob 

	return [Q, A, B, U]

def test(filepath, hmm):

	vt = []
	wt = []

	with open(filepath, 'r') as f:

		for line in f:

			if line != "\n":
				wt.append(line.rstrip('\n'))
				continue

			vt.extend(viterbi(wt, hmm))
			vt.append("")
			wt = []

		if len(wt) > 0:
			vt.extend(viterbi(wt, hmm))

	return vt

def viterbi(observations, hmm):

	Q = hmm[0]	# set of N states
	A = hmm[1]	# transition probability matrix
	B = hmm[2]	# sequence of observation likelihoods
	U = hmm[3]	# "likelihood" probabilities for UNKNOWN_WORD (OOV handling)
	O = observations

	T = len(O) - 1

	V = dict()	# viterbi matrix
	BP = dict()	# backpointer

	for state in Q[1:-1]:
		V[state] = dict()
		BP[state] = dict()

		# OOV handling
		if O[0].lower() not in B[state]:
			V[state][O[0]] = A["START"][state] * U[state]
		else:
			# if word in vocabulary
			V[state][O[0]] = A["START"][state] * B[state][O[0].lower()]

		BP[state][O[0]] = 0

	for (i, word) in enumerate(O):

		if i < 1 or i > T:
			continue

		for state in Q[1:-1]:
			maxval = 0
			argmax = ("", 0)

			for s in V.iterkeys():

				val = V[s][O[i - 1]] * A[s][state]

				# OOV handling
				if word.lower() not in B[state]:
					if val * U[state] > maxval:
						maxval = val * U[state]
				else:
					if val * B[state][word.lower()] > maxval:
						maxval = val * B[state][word.lower()]

				if val >= argmax[1]:
					argmax = (s, val)

			V[state][word] = maxval
			BP[state][word] = argmax[0]

	# termination step

	fMax = ("", 0)

	for state in V.iterkeys():
		if V[state][O[T]] * A[state]["END"] >= fMax[1]:
			fMax = (state, V[state][O[T]] * A[state]["END"])

	V["END"] = dict()
	BP["END"] = dict()

	V["END"][O[T]] = fMax[1]
	BP["END"][O[T]] = fMax[0]

	path = []

	temp = BP["END"][O[T]]

	for obs in reversed(O):
		path.append((obs, temp))
		newState = BP[temp][obs]
		temp = newState

	finalPath = reversed(path)
	return finalPath

def run(trainfile, testfile, outputfile):

	hmm = trainHMM(trainfile)

	testArr = test(testfile, hmm)

	with open(outputfile, 'w') as o:
		for e in testArr:
			if e == "":
				o.write("\n")
				continue

			o.write("%s\t%s\n" % (e[0], e[1]))

trainfile = sys.argv[1]
testfile = sys.argv[2]
outfile = sys.argv[3]

run(trainfile, testfile, outfile)


