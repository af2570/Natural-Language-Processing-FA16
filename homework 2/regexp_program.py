import re
import sys
import regex_dollar
import regex_phone
regexType = sys.argv[1]
inFile = sys.argv[2]

if regexType == 'dollar':
	regex_dollar.run(inFile)

if regexType == 'phone':
	regex_phone.run(inFile)