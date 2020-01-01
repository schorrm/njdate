#!/usr/bin/python3

# Basic constants for constructing stuff
alphabet  = 'אבגדהוזחטיכלמנסעפצקרשת'
salphabet = 'אבגדהוזחטיךלםןסעףץקרשת' # with sofits instead
values = [1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100,200,300,400]

sofits = 'ךםןףץ'
replace_sofits = 'כמנפצ'

yudheh = 'יה'
heh = 'ה'
yudvav = 'יו'

taf = 'ת'
tet = 'ט'
vav = 'ו'
zayin = 'ז'

tetvav = 'טו'
tvq    = 'ט"ו'
tetzayin = 'טז'
tzq      = 'ט"ז'
sq = "'"

char_to_num_mapper = dict(zip(alphabet + salphabet, values + values))
numtogem_map = dict(zip(values, alphabet))
numtogem_map[0] = '' # allows some computational shortcuts
snumtogem_map = dict(zip(values, salphabet))
snumtogem_map[0] = '' # allows some computational shortcuts

def Gematria (req_string):
	total = 0
	
	for c in req_string:
		total += char_to_num_mapper.get(c, 0)
	
	return total

# Change: May 30th, 2018: add number to gematria (formatted)
# Format is whether to insert " or ' in string
# if disabled, will return letters only

# List creation routine:
_plain_map = [''] * 1000 # start off with the alphabet
for k, v in numtogem_map.items():
	_plain_map[k] = v

for i in range(500, 1000, 100):
	_plain_map[i] = taf + _plain_map[i - 400]

for i in range(11, 100):
	_plain_map[i] = _plain_map[i - i % 10] + _plain_map[i % 10]

_plain_map[15] = tetvav
_plain_map[16] = tetzayin

for i in range(101, 1000):
	_plain_map[i] = _plain_map[i - i % 100] + _plain_map[i % 100]

_sofit_map = _plain_map.copy()

for i in range(0, 1000, 100):
	for j in [20, 40, 50, 80, 90]:
		_sofit_map[i + j] = _sofit_map[i] + snumtogem_map[j]


# Change: January 1st, 2020: allow prepend heh, and change the whole thing to precalculated
# For now: no prepend w/o format quotes
def NumberToGematria (number, sofit=True, format_quotes=True, prepend_heh=False, quote_heh=False):
	base = _sofit_map[number] if sofit else _plain_map[number]

	if format_quotes:
		if len(base) > 1:
			base = f'{base[:-1]}"{base[-1]}'
		else:
			base = f"{base}'"
	
	return f'{prepend_heh * heh}{quote_heh * sq}{base}'



# # Change: January 1st, 2020: allow prepend heh, and change the whole thing to precalculated
# def NumberToGematria (number, sofit=True, format_quotes=True, prepend_heh=False):
# 	singles  = number % 10
# 	hundreds = number // 100 % 4
# 	tens     = number // 10 % 10
# 	ntafs    = number // 400
# 	char_ct = ntafs + (singles is not 0) + (tens is not 0) + (hundreds is not 0)
# 	tens *= 10
# 	hundreds *= 100
# 	usofit = snumtogem_map if sofit else numtogem_map
# 	if format_quotes:
# 		if char_ct >= 2:
# 			if number % 100 in (15, 16):
# 				return f'{ntafs * taf}{numtogem_map[hundreds]}{tet}"{numtogem_map[singles+1]}'
# 			elif singles:
# 				return f'{ntafs * taf}{numtogem_map[hundreds]}{numtogem_map[tens]}"{numtogem_map[singles]}'
# 			elif tens:
# 				return f'{ntafs * taf}{numtogem_map[hundreds]}"{usofit[tens]}'
# 			elif hundreds:
# 				return f'{ntafs * taf}"{numtogem_map[hundreds]}'
# 			return f'{(ntafs-1)*taf}"{taf}'
# 		return f'{ntafs * taf}{numtogem_map[hundreds]}{numtogem_map[tens]}{numtogem_map[singles]}'
# 	elif number % 100 in (15, 16):
# 		return f'{ntafs * taf}{numtogem_map[hundreds]}{tet}{numtogem_map[singles+1]}'
# 	elif singles or not tens:
# 		return f'{ntafs * taf}{numtogem_map[hundreds]}{numtogem_map[tens]}{numtogem_map[singles]}'
# 	return f'{ntafs * taf}{numtogem_map[hundreds]}{usofit[tens]}'

# Old recursive method -- simpler to read, much slower
# def _NumGemRecursive (number):
# 	for val in rvals:
# 		if val <= number:
# 			return numtogem_map[val] + _NumGemRecursive(number-val)
# 	return '

def YearNoToGematria (number, sofit=True, format_quotes=True, prepend_heh=False, quote_heh=False):
	return NumberToGematria(number % 1000, sofit, format_quotes, prepend_heh, quote_heh)

	