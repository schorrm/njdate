alphabet = 'אבגדהוזחטיכלמנסעפצקרשת'
values = [1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100,200,300,400]
# rvals = [1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100,200,300,400]
rvals = values.copy()
rvals.reverse()

sofits = 'ךםןףץ'
replace_sofits = 'כמנפצ'

salphabet = alphabet
for r, s in zip(replace_sofits, sofits):
	salphabet = salphabet.replace(r,s)

yudheh = 'יה'
yudvav = 'יו'

taf = 'ת'
tet = 'ט'
vav = 'ו'
zayin = 'ז'

tetvav = 'טו'
tvq    = 'ט"ו'
tetzayin = 'טז'
tzq      = 'ט"ז'

mapper = dict(zip(alphabet, values))
numtogem_map = dict(zip(values, alphabet))
numtogem_map[0] = '' # allows some computational shortcuts
snumtogem_map = dict(zip(values, salphabet))
snumtogem_map[0] = '' # allows some computational shortcuts

def Gematria (req_string):
	for sf, rg in zip (sofits, replace_sofits):
		req_string = req_string.replace(sf, rg)
		
	sum = 0
	
	for c in req_string:
		if c in alphabet:
			sum+=mapper[c]
	
	return sum

# Change: May 30th, 2018: add number to gematria (formatted)
# Format is whether to insert " or ' in string
# if disabled, will return letters only
def NumberToGematria (number, sofit=True, format_quotes=True):
	singles  = number % 10
	hundreds = number // 100 % 4
	tens     = number // 10 % 10
	ntafs    = number // 400
	char_ct = ntafs + (singles is not 0) + (tens is not 0) + (hundreds is not 0)
	tens *= 10
	hundreds *= 100
	usofit = snumtogem_map if sofit else numtogem_map
	if format_quotes:
		if char_ct >= 2:
			if number % 100 in (15, 16):
				return f'{ntafs * taf}{numtogem_map[hundreds]}{tet}"{numtogem_map[singles+1]}'
			elif singles:
				return f'{ntafs * taf}{numtogem_map[hundreds]}{numtogem_map[tens]}"{numtogem_map[singles]}'
			elif tens:
				return f'{ntafs * taf}{numtogem_map[hundreds]}"{usofit[tens]}'
			elif hundreds:
				return f'{ntafs * taf}"{numtogem_map[hundreds]}'
			return f'{(ntafs-1)*taf}"{taf}'
		return f'{ntafs * taf}{numtogem_map[hundreds]}{numtogem_map[tens]}{numtogem_map[singles]}'
	elif number % 100 in (15, 16):
		return f'{ntafs * taf}{numtogem_map[hundreds]}{tet}{numtogem_map[singles+1]}'
	elif singles or not tens:
		return f'{ntafs * taf}{numtogem_map[hundreds]}{numtogem_map[tens]}{numtogem_map[singles]}'
	return f'{ntafs * taf}{numtogem_map[hundreds]}{usofit[tens]}'

# Old recursive method -- simpler to read, much slower
# def _NumGemRecursive (number):
# 	for val in rvals:
# 		if val <= number:
# 			return numtogem_map[val] + _NumGemRecursive(number-val)
# 	return '


def YearNoToGematria (number, sofit=True, format_quotes=True):
	return NumberToGematria(number % 1000, sofit, format_quotes)

	