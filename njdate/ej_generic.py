# generic extractor. not lpk dependent
import njdate
from njdate import gematria
from njdate.mapmonths import *

from datetime import date, timedelta

from njdate import njparshiot
from njdate import mapparshiot

gg = gematria.Gematria

lpk = 'לפ"ק'
shnat = "שנת"


MONTH_FILLERS = [
	"לחודש",
	"לחודש",
	"לחדש"
]

rishon = 'ראשון'
harishon = 'הראשון'
sheni = 'שני'
hasheni = 'השני'
adar = 'אדר'
rch = 'ר"ח'
shushan = 'שושן'
erach = 'ער"ח'

PARSHA_FILLERS = [
	"לס'",
	"לפ'",
	"פ'",
	"ס'",
	"לסדר",
	"סדר",
	"לפרשת",
	"פרשת"
]

def GetOmer(year, daystr):
	pesach = njdate.JewishDate(year, 8, 15)
	omer_day = gg(daystr) % 49
	fday = pesach.to_date() + timedelta(omer_day)
	return njdate.JewishDate.from_date(fday)

# Params: year, what number of day in selichot
def GetDayInSelichot (year, number):
	rosh_hashana = njdate.JewishDate(year+1, TISHREI, 1)
	yom_selichot = rosh_hashana.getShabbos().addDays(-7)
	if (rosh_hashana.weekday() < 5):
		# If Rosh HaShana falls out on Mon/Tue, then there's an extra week
		yom_selichot = yom_selichot.addDays(-7)
	return yom_selichot.addDays(number)
	
def addDays (jx, num):
	dx = jx.to_date()
	dx = dx + timedelta(num)
	return njdate.JewishDate.from_date(dx)
	
def _ParshaExtractor (heb_date_string, assignment_year):
	parsha_list = mapparshiot.getParshaStrings()
	parsha_list.reverse()
	parsha_list.sort(key=len, reverse=True) # sorts by descending length
	
	for parsha in parsha_list:
		# change: make it more circumspect - only whole parsha name.
		# looking at you, Parshat Bo.
		if parsha in heb_date_string.split():
			parsha_code = mapparshiot.getParshaNum(parsha)
			base_date = njparshiot.calc_parsha(assignment_year, parsha_code)
			if not base_date:
				return njdate.JewishDate(assignment_year, 1, 1)
			split_index = heb_date_string.find(parsha) - 1
			nhds = heb_date_string[:split_index]
			for filler in PARSHA_FILLERS:
				nhds = nhds.replace(filler, '')
			
			if not nhds:
				return base_date
			
			weekday_string = nhds.split()[-1]
			wd_num = mapparshiot.getWeekdayFromString(weekday_string)
			if wd_num:
				return base_date.addDays(wd_num-7)
			return base_date
			
	return njdate.JewishDate(assignment_year, 1, 1)

def ForceYear (heb_date_string, year_v):
	if ("מנחם אב") in heb_date_string:
		heb_date_string = heb_date_string.replace('מנחם אב', 'אב')
	words = heb_date_string.split()
	if (len(words) < 2):
		return njdate.JewishDate(year_v,1,1)
	if (len(words) >= 2):
		if shnat in words[-2]:
			words.pop(-2)
	if (len(words) < 2):
		return njdate.JewishDate(year_v,1,1)
	
	
	if (words[-2] == rishon or words[-2] == sheni or words[-2] == harishon or words[-2] == hasheni):
		if (words[-3] == adar):
			words[-2] = f"{words[-3]} {words[-2]}"
			words.pop(-3)
			
	month = GetMonthLoose(words[-2])
	
	if (len(words) == 2 and month <= 13 and month > 0):
		return njdate.JewishDate(year_v, month, 1)
	# month not found -- check for parsha
	elif month == -1:
		return _ParshaExtractor(heb_date_string, year_v)
		
	elif (len(words) == 2):
		if (month == PESACH):
			return njdate.JewishDate(year_v, 8, 19)
		if (month == SUKKOT):
			return njdate.JewishDate(year_v, 1, 19)			
		if (month == CHANUKAH):
			return njdate.JewishDate(year_v, TEVET, 1)
		if (month == PURIM):
			return njdate.JewishDate(year_v, 7, 14)
		if (month == SHUSHAN_PURIM):
			return njdate.JewishDate(year_v, 7, 15)
	
	if (month == OMER):
		return GetOmer(year_v, words[-3])
		
	if (month <= 13 and month > 0):
		if (words[-3] == rch):
			return njdate.JewishDate(year_v, month, 1)
		if (words[-3] == erach):
			return njdate.JewishDate(year_v, month, 1).addDays(-1)
		day = gg (words[-3])
		if day > 30:
			day = 15
		if (day == 0):
			day = 1
		return njdate.JewishDate(year_v, month, day)

	# Changed: added Selichot

	if (month == SELICHOT):
		day = gg(words[-3])
		working = GetDayInSelichot(year_v, day)
		if working.year != year_v:
			return GetDayInSelichot(year_v, 1)
		return working
		
	if (month == PESACH):
		day = gg(words[-3]) % 7
		if (day == 0):
			day = 1
		return njdate.JewishDate(year_v, 8, 14).addDays(day)
			
	if (month == SUKKOT):
		day = gg(words[-3]) % 10
		if (day == 0):
			day = 1
		return njdate.JewishDate(year_v, 1, 14).addDays(day)
			
	if (month == CHANUKAH):
		day = gg(words[-3]) % 9
		if (day == 0):
			day = 1		
		return njdate.JewishDate(year_v, KISLEV, 24).addDays(day)
		
	if (month == PURIM):
		if (words[-3] == shushan):
			return njdate.JewishDate(year_v, 7, 15)
		return njdate.JewishDate(year_v, 7, 14)
		
	if (month == SHUSHAN_PURIM):
		return njdate.JewishDate(year_v, 7, 15)
		
	return njdate.JewishDate(year_v,1,1)


# TODO: make much faster, this is an issue
def ExtractDate (heb_date_string, earliest=5000, latest=5800):
	if ("מנחם אב") in heb_date_string:
		heb_date_string = heb_date_string.replace('מנחם אב', 'אב')
	words = heb_date_string.split()
	if (len(words) < 1):
		return None
	
	if (len(words) >= 2):
		if shnat in words[-2]:
			words.pop(-2)
		
	# last is year.
	year_s = words[-1]
	year_v = gg(year_s)
	
	if (len(words) < 2):
		
		year_v = year_v % earliest + earliest
		return njdate.JewishDate(year_v,1,1)

	# For protection from aggressor overuse, w/ SA junk making it in:
	if words[-2] in ["סי'", 'סימן', "בסי'", "בסימן"]:
		return None
	
	# New addition: sanity check on extract, using range.
	# If we have a result that is too low, and also,
	# the prior word isn't a month / other date word AND after adding the prior word
	# we now have a suitable gematria, we think it is a bigram year.

	if ((year_v + 5000 < earliest) and 
		(gg(words[-2]) + year_v + 5000 in range(earliest, latest+1)) and
		(GetMonthLoose(words[-2]) == -1) and
		(words[-2] not in mapparshiot.getParshaStrings())
		):
		year_v += gg(words[-2])

	year_v += 5000

	if year_v not in range( earliest, latest + 1 ):
		return None
	
	if (len(words) > 3) and (words[-2] == rishon or words[-2] == sheni or words[-2] == harishon or words[-2] == hasheni):
		if (words[-3] == adar):
			words[-2] = f"{words[-3]} {words[-2]}"
			words.pop(-3)
			
	month = GetMonthLoose(words[-2])
	
	if (len(words) == 2 and month <= 13 and month > 0):
		return njdate.JewishDate(year_v, month, 1)
	# month not found -- check for parsha
	elif month == -1:
		return _ParshaExtractor(heb_date_string, year_v)
		
	elif (len(words) == 2):
		if (month == PESACH):
			return njdate.JewishDate(year_v, 8, 19)
		if (month == SUKKOT):
			return njdate.JewishDate(year_v, 1, 19)			
		if (month == CHANUKAH):
			return njdate.JewishDate(year_v, TEVET, 1)
		if (month == PURIM):
			return njdate.JewishDate(year_v, 7, 14)
		if (month == SHUSHAN_PURIM):
			return njdate.JewishDate(year_v, 7, 15)
	
	if (month == OMER):
		return GetOmer(year_v, words[-3])
		
	if (month <= 13 and month > 0):
		if (words[-3] == rch):
			return njdate.JewishDate(year_v, month, 1)
		if (words[-3] == erach):
			return njdate.JewishDate(year_v, month, 1).addDays(-1)
		day = gg (words[-3])
		if day > 30:
			day = 15
		if (day == 0):
			day = 1
		return njdate.JewishDate(year_v, month, day)

		# Changed: added Selichot

	if (month == SELICHOT):
		day = gg(words[-3])
		working = GetDayInSelichot(year_v, day)
		if working.year != year_v:
			return GetDayInSelichot(year_v, 1)
		return working
		
	if (month == EREV_PESACH):
		return njdate.JewishDate(year_v, 8, 14)
	if (month == EREV_SUKKOT):
		return njdate.JewishDate(year_v, 1, 14)
		
	if (month == PESACH):
		day = gg(words[-3]) % 7
		if (day == 0):
			day = 1
		return addDays(njdate.JewishDate(year_v, 8, 14), day)
			
	if (month == SUKKOT):
		day = gg(words[-3]) % 10
		if (day == 0):
			day = 1
		return addDays(njdate.JewishDate(year_v, 1, 14), day)
			
	if (month == CHANUKAH):
		day = gg(words[-3]) % 9
		if (day == 0):
			day = 1		
		return addDays(njdate.JewishDate(year_v, KISLEV, 24), day)
		
	if (month == PURIM):
		if (words[-3] == shushan):
			return njdate.JewishDate(year_v, 7, 15)
		return njdate.JewishDate(year_v, 7, 14)
		
	if (month == SHUSHAN_PURIM):
		return njdate.JewishDate(year_v, 7, 15)
		
	return njdate.JewishDate(year_v,1,1)
