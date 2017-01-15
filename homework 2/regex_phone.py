import re


regex = r'(((\(\d{3}\))|(\d{3}))[ -\.])?(\d{3})[ -\.](\d{4})(( ?(ext.?)|(ex.?)|(x.?))?( \d+))?'



def run(inFile):
	with open(inFile, 'r') as i:
		lines = i.read()

	phone = re.compile(regex)

	processed = phone.sub(r'[\g<0>]', lines)
	matches = phone.finditer(lines)

	with open('output_phone.txt', 'w') as o:
		o.write(processed)

	with open('phone.txt', 'w') as d:
		for match in matches:
			d.write(match.group(0) + '\n')