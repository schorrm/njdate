alphabet = 'אבגדהוזחטיכלמנסעפצקרשת'
values = [1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100,200,300,400]
rvals = [1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100,200,300,400]
rvals.reverse()

sofits = 'ךםןףץ'
replace_sofits = 'כמנפצ'

yudheh = 'יה'
yudvav = 'יו'

tetvav = 'טו'
tetzayin = 'טז'

mapper = dict(zip(alphabet, values))
numtogem_map = dict(zip(values, alphabet))

def Gematria (req_string):
	for sf, rg in zip (sofits, replace_sofits):
		req_string = req_string.replace(sf, rg)
		
	sum = 0
	
	for c in req_string:
		if c in alphabet:
			sum+=mapper[c]
	
	return sum

# Change: May 30th, 2018: add number to gematria (formatted)

def _NumGemRecursive (number):
	for val in rvals:
		if val <= number:
			return numtogem_map[val] + _NumGemRecursive(number-val)
	return ''

# Format is whether to insert " or ' in string
# if disabled, will return letters only
def NumberToGematria (number, sofit=True, format_quotes=True):
	base_string = _NumGemRecursive(number)

	base_string = base_string.replace(yudheh, tetvav)
	base_string = base_string.replace(yudvav, tetzayin)

	if not format_quotes:
		return base_string

	if len(base_string) > 1:
		lchar = base_string[-1]
		if lchar in replace_sofits and sofit:
			sdict = dict(zip(replace_sofits, sofits))
			lchar = sdict[lchar]

		return base_string[:-1] + '"' + lchar
	return base_string + "'"

def YearNoToGematria (number, sofit=True, format_quotes=True):
	return NumberToGematria(number % 1000, sofit, format_quotes)