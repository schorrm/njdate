# Takes two years, and runs an aggressive search for dates in between those two years (inclusive).
import njdate.gematria as gematria
import njdate.ej_generic as ej_generic
import string

specpunc = string.punctuation.replace('"','').replace("'","")


def date_aggressor (search_text, begin_year, end_year):
    tokens = search_text.translate(str.maketrans("","",specpunc)).split()
    for search_year in range (begin_year, end_year+1):
        if gematria.YearNoToGematria(search_year) in tokens:
            query = ''.join(search_text.partition(gematria.YearNoToGematria(search_year))[:2])
            return ej_generic.ExtractDate(query)
        if gematria.YearNoToGematria(search_year, False) in tokens:
            query = ''.join(search_text.partition(gematria.YearNoToGematria(search_year, False))[:2])
            return ej_generic.ExtractDate(query)
    return None

def date_aggressor_lamedify (search_text, begin_year, end_year):
    tokens = search_text.translate(str.maketrans("","",specpunc)).split()
    for search_year in range (begin_year, end_year+1):
        if gematria.YearNoToGematria(search_year) in tokens:
            query = ''.join(search_text.partition(gematria.YearNoToGematria(search_year))[:2])
            return ej_generic.ExtractDate(query)
        if gematria.YearNoToGematria(search_year, False) in tokens:
            query = ''.join(search_text.partition(gematria.YearNoToGematria(search_year, False))[:2])
            return ej_generic.ExtractDate(query)
        if gematria.YearNoToGematria(search_year, False, False) + '"ל' in tokens:
            query = ''.join(search_text.partition(gematria.YearNoToGematria(search_year, False, False))[:2])
            return ej_generic.ExtractDate(query)
    return None

# For dropped Tafs etc, so we need to add 400 years after what we've found, etc
def yshift_date_aggressor (search_text, begin_year, end_year, shift=400):
    tokens = search_text.translate(str.maketrans("","",specpunc)).split()
    for search_year in range (begin_year, end_year+1):
        if gematria.YearNoToGematria(search_year) in tokens:
            query = ''.join(search_text.partition(gematria.YearNoToGematria(search_year))[:2])
            return ej_generic.ForceYear(query, search_year+shift)
        if gematria.YearNoToGematria(search_year, False) in tokens:
            query = ''.join(search_text.partition(gematria.YearNoToGematria(search_year, False))[:2])
            return ej_generic.ForceYear(query, search_year+shift)
    return None

def yshift_date_aggressor_lamedify (search_text, begin_year, end_year, shift=400):
    tokens = search_text.translate(str.maketrans("","",specpunc)).split()
    for search_year in range (begin_year, end_year+1):
        if gematria.YearNoToGematria(search_year, False, False) + '"ל' in tokens:
            query = ''.join(search_text.partition(gematria.YearNoToGematria(search_year, False, False))[:2])
            return ej_generic.ForceYear(query, search_year+shift)
    return None
