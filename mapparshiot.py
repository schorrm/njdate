BERAISHIT = 0
NOACH = 1
LECH_LECHA = 2
VAYERA = 3
CHAYEI_SARAH = 4
TOLDOS = 5
VAYETZEI = 6
VAYISHLACH = 7
VAYESHEV = 8
MIKETZ = 9
VAYIGASH = 10
VAYECHI = 11
SHEMOS = 12
VAERA = 13
BO = 14
BESHALACH = 15
YISRO = 16
MISHPATIM = 17
TERUMA = 18
TETZAVE = 19
KI_TISA = 20
VAYAKHEL = 21
PEKUDEI = 22
VAYIKRA = 23
TZAV = 24
SHEMINI = 25
TAZRIA = 26
METZORA = 27
ACHAREI_MOS = 28
KEDOSHIM = 29
EMOR = 30
BEHAR = 31
BECHUKOSAI = 32
BAMIDBAR = 33
NASO = 34
BEHAALOSCHA = 35
SHELACH = 36
KORACH = 37
CHUKAS = 38
BALAK = 39
PINCHAS = 40
MATOS = 41
MASEI = 42
DEVARIM = 43
VAESCHANAN = 44
EIKEV = 45
REEY = 46
SHOFTIM = 47
KI_TETZEI = 48
KI_TAVO = 49
NITZAVIM = 50
VAYELECH = 51
HAAZINU = 52
VEZOS_HABRACHA = 53

multiname_list = [
	['בראשית'],
	['נח'],
	['לך לך','לך','והיה ברכה'],
	['וירא'],
	['חיי שרה', 'חיי'],
	['תולדות', 'תולדת'],
	['ויצא'],
	['וישלח'],
	['וישב'],
	['מקץ'],
	['ויגש'],
	['ויחי'],
	['שמות'],
	['וארא'],
	['בא'],
	['בשלח'],
	['יתרו'],
	['משפטים','ואלה המשפטים'],
	['תרומה'],
	['תצוה'],
	['כי תשא', 'תשא'],
	['ויקהל'],
	['פקודי', 'ויק"פ', 'ויק"פ במחובר'],
	['ויקרא'],
	['צו'],
	['שמיני'],
	['תזריע'],
	['מצורע'],
	['אחרי מות', 'אחרי'],
	['קדושים'],
	['אמור'],
	['בהר', 'ב"ב במחובר'],
	['בחוקותי', 'בחקותי', 'בחקתי', 'בחוקתי'],
	['במדבר'],
	['נשא'],
	['בהעלותך', 'בהעלתך'],
	['שלח', 'שלח לך'],
	['קרח','קורח'],
	['חקת','חוקת'],
	['בלק'],
	['פנחס', 'פינחס'],
	['מטות', 'ראשי המטות', 'מ"מ במחובר', 'מו"מ במחובר'],
	['מסעי'],
	['דברים'],
	['ואתחנן'],
	['עקב'],
	['ראה'],
	['שופטים'],
	['כי תצא', 'תצא'],
	['כי תבוא', 'תבוא', 'תבא'],
	['נצבים', 'ניצבים', 'נצו"י'],
	['וילך'],
	['האזינו'],
	['וזאת הברכה'] # 'הברכה'?
]


weekday_map = [
	["א'", "ראשון"],
	["ב'", "שני"],
	["ג'", "שלישי"],
	["ד'", "רביעי"],
	["ה'", "חמישי"],
	["ו'", "שישי", "ששי", 'עש"ק', 'ועש"ק'],
	["שבת", 'מוצ"ש', 'מוצש"ק']
]

def getParshaNum (parsha_string):
	parsha_dict = {}
	for i, l in enumerate(multiname_list):
		for pn in l:
			parsha_dict[pn] = i
	
	if parsha_string in parsha_dict.keys():
		return parsha_dict[parsha_string]
	return None
	
def getParshaStrings ():
	namelist = []
	for i, l in enumerate(multiname_list):
		for pn in l:
			namelist.append(pn)
	
	return namelist

def getWeekdayFromString (keystr):
	day_map = {}
	for i, l in enumerate(weekday_map, 1):
		for dn in l:
			day_map[dn] = i
			
	if keystr in day_map.keys():
		return day_map[keystr]
	
	return 0