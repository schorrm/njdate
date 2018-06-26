from njdate.gematria import Gematria as gg
from njdate.mapmonths import *
from datetime import date, timedelta
import jewish
from njdate import ej_generic

lpk = 'לפ"ק'
shnat = "שנת"
lechodes = "לחדש"

rishon = 'ראשון'
sheni = 'שני'
adar = 'אדר'
rch = 'ר"ח'

def GetOmer(year, daystr):
	pesach = jewish.JewishDate(year, 8, 15)
	omer_day = gg(daystr) % 49
	fday = pesach.to_date() + timedelta(omer_day)
	return jewish.JewishDate.from_date(fday)
	
def addDays (jx, num):
	dx = jx.to_date()
	dx = dx + timedelta(num)
	return jewish.JewishDate.from_date(dx)

def ExtractDate (heb_date_string, earliest=5000, latest=5800):
	if lpk not in heb_date_string:
		return None
	if len (heb_date_string.split()) < 2:
		return None
	query = heb_date_string.partition(lpk)[0]
	if not query:
		return None
	return ej_generic.ExtractDate(query, earliest, latest)

def ForceYear (heb_date_string, year_v):
	if lpk not in heb_date_string:
		return None
	if len (heb_date_string.split()) < 2:
		return None
	query = heb_date_string.partition(lpk)[0]
	if not query:
		return None
	return ej_generic.ForceYear(query, year_v)	

def DeprecatedExtractDate (heb_date_string, earliest=5000, latest=5800):
	# We expect a לפ"ק in the string. we work backwards from there.
	heb_date_string = heb_date_string.replace('לפ"ק.', 'לפ"ק ')
	heb_date_string = heb_date_string.replace('לפ"ק:', 'לפ"ק ')
	heb_date_string = heb_date_string.replace('לפ"ק,', 'לפ"ק ')
	words = heb_date_string.split()
	if (len(words) < 2):
		return None
	if lpk not in words:
		return None
	splitind = words.index(lpk)
	words = words[:splitind]
	query = ' '.join(words)
	return ej_generic.ExtractDate(query)
