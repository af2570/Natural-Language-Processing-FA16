Anna Fenske (af2570)
Natural Language Processing, Fall 2016
Homework 6

Output from score.chunk.py on the development corpus:
	
	31686 out of 32853 tags correct
		accuracy: 96.45
	8378 groups in key
	8552 groups in response
	7719 correct groups
		precision:	90.26
		recall:		92.13
		F1:			91.19

Files in this folder:
	hw6.py: 				program for training and testing
	output_features.chunk:	output file from WSJ_23.pos (feature sets)
	output_maxent.chunk: 	output file from WSJ_23.pos (output from runnning MEtag on output.chunk)

Features:

	--Current word features--

	"word"			=> current word (String)
	"pos" 			=> current POS (String)
	"punc" 			=> True if current word is punctuation, False otherwise
	"title" 		=> True if current word is a title (that typically precedes a name), False otherwise
	"cap" 			=> True if current word is capitalized, False otherwise
	"start" 		=> True if current word is the first element of a sentence, False otherwise
	"end" 			=> True if current word is the last element of a sentence, False otherwise
	"cap_nonstart" 	=> True if current word is capitalized AND NOT the first word of a sentence, False otherwise
		I originally had features "month", "name" and "place", which checked for proper nouns, but I found that this is a more effective and more efficient method of checking for proper nouns.

	--Previous/Next word features--

	"prev_
		word"		=> previous word (String)
		pos"		=> previous POS (String)
		title"		=> True if previous word is a title (that typically precedes a name), False otherwise
			This is my method of checking for names.
		start"		=> True if previous word is the first word of a sentence, False otherwise
	"next_
		word"		=> next word (String)
		pos"		=> next POS (String)
		end"		=> True if next word is the last element of a sentence, False otherwise
	"prev2_
		word"		=> word 2 behind the current word (String)
		pos"		=> POS 2 behind the current word (String)
	"next2_
		word"		=> word 2 ahead the current word (String)
		pos"		=> POS 2 ahead the current word (String)

