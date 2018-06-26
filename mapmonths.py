TISHREI = 1
HESHVAN = 2
KISLEV = 3
TEVET = 4
SHVAT = 5
ADAR_I = 6
ADAR_II = 7
NISAN = 8
IYAR = 9
SIVAN = 10
TAMUZ = 11
AV = 12
ELUL = 13
SPECIAL_BEHAVIOR = 100
OMER = 101
PESACH = 200
SHAVUOT = 201
ROSH_HASHANAH = 204
YOM_KIPPUR = 205
SUKKOT = 206
CHANUKAH = 207
TZOM_TEN = 208
PURIM = 209
SHUSHAN_PURIM = 210
SELICHOT = 211
EREV_SUKKOT = 212
EREV_PESACH = 213

NOT_A_MONTH = -1


mdict = {
'אב': AV,
'אדר': ADAR_II,
'אייר': IYAR,
'איר': IYAR,
'אלול': ELUL,
'א"ר': ADAR_I,
'א"ש': ADAR_II,
'בעומר': OMER,
'לעומר': OMER,
'חנוכה': CHANUKAH,
'דחנוכה': CHANUKAH,
'העשירי': TZOM_TEN,
'טבת': TEVET,
'כסליו': KISLEV,
'כסלו': KISLEV,
'למב"י': OMER,
'מנחם': AV,
'מרחשוון': HESHVAN,
'מרחשון': HESHVAN,
'מ"ח': HESHVAN,
'חשון': HESHVAN,
'חשוון': HESHVAN,
'ניסן': NISAN,
'סוכות': SUKKOT,
'ע"ס': EREV_SUKKOT,
'ע"פ': EREV_PESACH,
'סיוון': SIVAN,
'סיון': SIVAN,
'פורים': PURIM,
'שושן פורים': SHUSHAN_PURIM,
'פסח': PESACH,
'ראשון': ADAR_I,
'אדר ראשון': ADAR_I,
'אדר הראשון': ADAR_I,
'שבט': SHVAT,
'שני': ADAR_II,
'אדר שני': ADAR_II,
'אדר השני': ADAR_II,
'שנת': NOT_A_MONTH,
'תמוז': TAMUZ,
'סליחות': SELICHOT,
'דסליחות': SELICHOT,
'תשרי': TISHREI
}

def GetMonthLoose (m_str):
	if m_str not in mdict.keys():
		return -1
	return mdict[m_str]
	
def GetMonthStrict (m_str):
	if m_str not in mdict.keys():
		return -1
	if mdict[m_str] > 13:
		return -1
	return mdict[m_str]