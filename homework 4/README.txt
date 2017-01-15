Anna Fenske (af2570)
Natural Language Processing
Homework 4

CONTENTS:

	hw4.py -------------- main file: 
						   trains HMM tagger, runs Viterbi algorithm on test 
						   file, writes results to output file 
	merged_trainset.pos -- training file used in development: 
						   merged contents of WSJ_02-21.pos and WSJ_24.pos
	WSJ_23.words --------- test file
	af2570.pos ----------- output from testing hw04.py on WSJ_23.words

TO RUN:

	>>> python hw4.py [TRAINING FILE] [TEST FILE] [OUTPUT FILE]

	Example:
	>>> python hw4.py merged_trainset.pos WSJ_23.words af2570.pos

WRITE-UP:
	
	To run this program, see the command given above. hw04.py takes in three 
	files (training, testing, and output files), and writes the tag sequence 
	determined by the Viterbi algorithm implemented in the viterbi function 
	on line 147. Out Of Vocabulary words encountered in the test file are 
	handled using the second strategy provided in the homework description. 
	That is, using the distribution of all words in the training file with 
	count = 1, I developed a likelihood matrix U to apply to unknown words 
	as they were encountered as follows:

	U[tag] = (Number of words with count = 1 with this tag) / (Total occurrences of tag)

ACCURACY:

	Using score.py
	29130 out of 32853 tags correct
	accuracy: 88.667702

RESUBMISSION: Corrected the program to account for capitalization

