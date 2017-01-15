punc = [".", ",", "''", "``", "'", "`", "?", "!", ")", "(", "--"]
title = ["Mr.", "Mrs.", "Miss", "Ms.", "Dr.", "Prof.", "Doctor", "Professor"]

def get_features(line, train):	# train = True/False (is this for a training file)

	word = line.split()[0]
	pos = line.split()[1]

	features = dict()

	features["word"] = word
	features["pos"] = pos
	features["punc"] = word in punc
	features["title"] = word in title
	features["cap"] = word[:1].isupper()

	if train:
		features["bio"] = line.split()[2]

	return features

def pass1(filepath, train):
	fset = []

	with open(filepath, 'r') as f:
		for line in f:
			if line != "\n":
				fset.append(get_features(line, train))
				continue
			fset.append("")

	return fset

def pass2(fset):
	set2 = []

	for (i, features) in enumerate(fset):

		if features != "":
			try:
				p = fset[i - 1]
			except IndexError:
				p = "NOPE"

			if p == "":
				features["start"] = True
				features["cap_nonstart"] = False
			elif p != "NOPE":
				features["start"] = False
				features["cap_nonstart"] = features["cap"]
				features["prev_word"] = p["word"]
				features["prev_pos"] = p["pos"]
				features["prev_title"] = p["title"]

			try:
				n = fset[i + 1]
			except IndexError:
				n = "NOPE"

			if n == "":
				features["end"] = True
			elif n != "NOPE":
				features["end"] = False
				features["next_word"] = n["word"]
				features["next_pos"] = n["pos"]

		set2.append(features)
	
	return set2

def pass3(fset):
	set3 = []

	for (i, features) in enumerate(fset):
		if features != "":
			if not features["start"]:
				p = fset[i - 1]
				features["prev_start"] = p["start"]

				if not p["start"]:
					features["prev2_word"] = p["prev_word"]
					features["prev2_pos"] = p["prev_pos"]

			if not features["end"]:
				n = fset[i + 1]
				features["next_end"] = n["end"]

				if not n["end"]:
					features["next2_word"] = n["next_word"]
					features["next2_pos"] = n["next_pos"]

		set3.append(features)
	
	return set3

def train(input_file, output_file):
	train_set1 = pass1(input_file, True)
	train_set2 = pass2(train_set1)
	train_set3 = pass3(train_set2)

	with open(output_file, 'w') as o:
		for features in train_set3:
			if features != "":
				o.write("%s\t" % features["word"])

				for (name, val) in features.items():
					if name != "word" and name != "bio":
						o.write("%s=%s\t" % (name, val))
				o.write("%s" % features["bio"])
			o.write("\n")


def test(input_file, output_file):
	test_set1 = pass1(input_file, False)
	test_set2 = pass2(test_set1)
	test_set3 = pass3(test_set2)

	with open(output_file, 'w') as o:
		for features in test_set3:

			if features != "":
				o.write("%s\t" % features["word"])

				for (name, val) in features.items():
					if name != "word":
						o.write("%s=%s\t" % (name, val))
			o.write("\n")

test('WSJ_23.pos', 'output.chunk')