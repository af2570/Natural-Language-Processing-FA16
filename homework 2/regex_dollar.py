import re

regex1 = r'((((twen)|(thir)|(for)|(fif)|(six)|(seven)|(eigh)|(nine))ty)([ -]?((one)|(two)|(three)|(four)|(five)|(six)|(seven)|(eight)|(nine))?)|(((thir)|(four)|(fif)|(six)|(seven)|(eigh)|(nine))teen)|((one)|(two)|(three)|(four)|(five)|(six)|(seven)|(eight)|(nine))( hundred)?|((ten)|(eleven)|(twelve)))( thousand)?( (m|b|(tr))illion)?(( dollar(s)?)|( USD))( and \d{1,2} cent(s)?)?'

regex2 = r'((\$ ?[+-]?\d{1,3}(,?\d)*(\.\d{1,2})?(( thousand)|( (m|b|(tr))illion))?)(( dollar(s)?)|( USD))?|([+-]?\d{1,3}(,?\d)*(\.\d{1,2})?)(( thousand)|( (m|b|(tr))illion))?(( dollar(s)?)|( USD)))( and \d{1,2} cent(s)?)?'


def run(inFile):

	with open(inFile, 'r') as i:
		lines = i.read()

	words = re.compile(regex1, flags=re.IGNORECASE)
	num = re.compile(regex2, flags=re.IGNORECASE)

	processed = re.sub(regex1, r'[\g<0>]', lines, flags=re.IGNORECASE)
	processed = re.sub(regex2, r'[\g<0>]', processed, flags=re.IGNORECASE)

	matchesW = words.finditer(lines)
	matchesN = num.finditer(lines)

	with open('output_dollar.txt', 'w') as o:
		o.write(processed)

	with open('dollar.txt', 'w') as d:
		for match in matchesW:
			d.write(match.group(0) + '\n')

		for match in matchesN:
			d.write(match.group(0) + '\n')

