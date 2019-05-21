"""This module has functions to find the weekly parasha for a given Shabbos.

Attributes
----------
PARSHIOS : list of str
    A list of all of the parsha names starting with Beraishis through V'zos
    Habrocha.

Notes
-----
The algorithm is based on Dr. Irv Bromberg's, University of Toronto at
http://individual.utoronto.ca/kalendis/hebrew/parshah.htm

All parsha names are transliterated into the American Ashkenazik pronunciation.

Further Notes: (May 27, 2018)
This is modified from Meir List's pyluach, the model here is to use the
jewish library by Eitan Mosenkis, and to add other functionality.

(1) Parsha to date.
(2) Hebrew Parsha names.

"""
from collections import deque, OrderedDict

import njdate

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

PARSHIOS = [
    'Beraishis', 'Noach', "Lech L'cha", 'Vayera', 'Chayei Sarah',
    'Toldos', 'Vayetzei', 'Vayishlach', 'Vayeshev', 'Miketz',
    'Vayigash', 'Vayechi', 'Shemos',  "Va'era", 'Bo', 'Beshalach',
    'Yisro',  'Mishpatim', 'Teruma', 'Tetzave', 'Ki Sisa', 'Vayakhel',
    'Pekudei', 'Vayikra', 'Tzav','Shemini', 'Tazria', 'Metzora',
    'Acharei Mos', 'Kedoshim', 'Emor', 'Behar', 'Bechukosai', 'Bamidbar',
    'Naso', "Beha'aloscha", "Shelach", 'Korach', 'Chukas', 'Balak',
    'Pinchas', 'Matos', "Ma'sei", 'Devarim', "Va'eschanan", 'Eikev',
    "R'ey", 'Shoftim', 'Ki Setzei', 'Ki Savo', 'Netzavim', 'Vayelech',
    'Haazinu', "V'zos Habrocha"
    ]


def _parshaless(date, israel=False):
    if israel:
        if (date.month == TISHREI and date.day == 23
            or date.month == NISAN and date.day == 22
            or date.month == SIVAN and date.day == 7):
            return False
    if date.month == TISHREI and date.day in ([1,2,10] + list(range(15, 24))):
        return True
    if date.month == NISAN and date.day in range(15, 23):
        return True
    if date.month == SIVAN and date.day in [6, 7]:
        return True
    return False


# @memoize(maxlen=50)
def _gentable(year, israel=False):
    """Return OrderedDict mapping date of Shabbos to list of parsha numbers.

    The numbers start with Beraishis as 0. Double parshios are represented
    as a list of the two numbers. If there is no Parsha the value is None.
    """
    parshalist = deque([51, 52] + list(range(52)))
    table = OrderedDict()
    leap = njdate.is_leap_year(year)
    pesachday = njdate.JewishDate(year, NISAN, 15).weekday()
    rosh_hashana = njdate.JewishDate(year, TISHREI, 1)
    shabbos = (rosh_hashana.addDays(2)).getShabbos()
    if rosh_hashana.weekday() > 4:
        parshalist.popleft()

    while shabbos.year == year:
        if _parshaless(shabbos, israel):
            table[shabbos] = None
        else:
            parsha = parshalist.popleft()
            table[shabbos] = [parsha,]
            if (
                (parsha == 21 and (njdate.JewishDate(year, NISAN, 14) - shabbos).days // 7 < 3) or
                (parsha in [26, 28] and not leap) or
                (parsha == 31 and not leap and (
                                               not israel or pesachday != 7
                                               )) or
                (parsha == 38 and not israel and pesachday == 5) or
                (parsha == 41 and (njdate.JewishDate(year, AV, 9)-shabbos).days // 7 < 2)  or
                (parsha == 50 and njdate.JewishDate(year+1, TISHREI, 1).weekday() > 4)
                ):  #  If any of that then it's a double parsha.
                table[shabbos].append(parshalist.popleft())
        shabbos = shabbos.addDays(7)
    return table

""" Moshe Schorr, May 21 2019.
getdate_of_parsha, and _gentable_reverse is a huge bottleneck here.
calc_parsha does this faster based on precalculations.
"""

_year_types = {
    (2, 353, False): 0,
    (2, 355, False): 1,
    (2, 383, True): 2,
    (2, 385, True): 3,
    (3, 354, False): 4,
    (3, 384, True): 5,
    (5, 354, False): 6,
    (5, 355, False): 7,
    (5, 383, True): 8,
    (5, 385, True): 9,
    (7, 353, False): 10,
    (7, 355, False): 11,
    (7, 383, True): 12,
    (7, 385, True): 13
 }

_lmap = [[(1, 27), (2, 4), (2, 11), (2, 18), (2, 25), (3, 3), (3, 10), (3, 17), (3, 24), (4, 2), (4, 9), (4, 16), (4, 23), (5, 1), (5, 8), (5, 15), (5, 22), (5, 29), (7, 6), (7, 13), (7, 20), (7, 27), (7, 27), (8, 5), (8, 12), (8, 26), (9, 3), (9, 3), (9, 10), (9, 10), (9, 17), (9, 24), (9, 24), (10, 2), (10, 9), (10, 16), (10, 23), (10, 30), (11, 7), (11, 14), (11, 21), (11, 28), (11, 28), (12, 6), (12, 13), (12, 20), (12, 27), (13, 4), (13, 11), (13, 18), (13, 25), (13, 25), (1, 13)], [(1, 27), (2, 4), (2, 11), (2, 18), (2, 25), (3, 2), (3, 9), (3, 16), (3, 23), (3, 30), (4, 7), (4, 14), (4, 21), (4, 28), (5, 6), (5, 13), (5, 20), (5, 27), (7, 4), (7, 11), (7, 18), (7, 25), (7, 25), (8, 3), (8, 10), (8, 24), (9, 1), (9, 1), (9, 8), (9, 8), (9, 15), (9, 22), (9, 22), (9, 29), (10, 14), (10, 21), (10, 28), (11, 5), (11, 12), (11, 12), (11, 19), (11, 26), (11, 26), (12, 4), (12, 11), (12, 18), (12, 25), (13, 2), (13, 9), (13, 16), (13, 23), (13, 23), (1, 13)], [(1, 27), (2, 4), (2, 11), (2, 18), (2, 25), (3, 3), (3, 10), (3, 17), (3, 24), (4, 2), (4, 9), (4, 16), (4, 23), (5, 1), (5, 8), (5, 15), (5, 22), (5, 29), (6, 6), (6, 13), (6, 20), (6, 27), (7, 4), (7, 11), (7, 18), (7, 25), (8, 3), (8, 10), (8, 24), (9, 1), (9, 8), (9, 15), (9, 22), (9, 29), (10, 14), (10, 21), (10, 28), (11, 5), (11, 12), (11, 12), (11, 19), (11, 26), (11, 26), (12, 4), (12, 11), (12, 18), (12, 25), (13, 2), (13, 9), (13, 16), (13, 23), (13, 23), (1, 13)], [(1, 27), (2, 4), (2, 11), (2, 18), (2, 25), (3, 2), (3, 9), (3, 16), (3, 23), (3, 30), (4, 7), (4, 14), (4, 21), (4, 28), (5, 6), (5, 13), (5, 20), (5, 27), (6, 4), (6, 11), (6, 18), (6, 25), (7, 2), (7, 9), (7, 16), (7, 23), (8, 1), (8, 8), (8, 29), (9, 6), (9, 13), (9, 20), (9, 27), (10, 5), (10, 12), (10, 19), (10, 26), (11, 3), (11, 10), (11, 17), (11, 24), (12, 2), (12, 2), (12, 9), (12, 16), (12, 23), (12, 30), (13, 7), (13, 14), (13, 21), (13, 28), (1, 6), (1, 13)], [(1, 26), (2, 3), (2, 10), (2, 17), (2, 24), (3, 2), (3, 9), (3, 16), (3, 23), (3, 30), (4, 7), (4, 14), (4, 21), (4, 28), (5, 6), (5, 13), (5, 20), (5, 27), (7, 4), (7, 11), (7, 18), (7, 25), (7, 25), (8, 3), (8, 10), (8, 24), (9, 1), (9, 1), (9, 8), (9, 8), (9, 15), (9, 22), (9, 22), (9, 29), (10, 14), (10, 21), (10, 28), (11, 5), (11, 12), (11, 12), (11, 19), (11, 26), (11, 26), (12, 4), (12, 11), (12, 18), (12, 25), (13, 2), (13, 9), (13, 16), (13, 23), (13, 23), (1, 12)], [(1, 26), (2, 3), (2, 10), (2, 17), (2, 24), (3, 2), (3, 9), (3, 16), (3, 23), (3, 30), (4, 7), (4, 14), (4, 21), (4, 28), (5, 6), (5, 13), (5, 20), (5, 27), (6, 4), (6, 11), (6, 18), (6, 25), (7, 2), (7, 9), (7, 16), (7, 23), (8, 1), (8, 8), (8, 29), (9, 6), (9, 13), (9, 20), (9, 27), (10, 5), (10, 12), (10, 19), (10, 26), (11, 3), (11, 10), (11, 17), (11, 24), (12, 2), (12, 2), (12, 9), (12, 16), (12, 23), (12, 30), (13, 7), (13, 14), (13, 21), (13, 28), (1, 5), (1, 12)], [(1, 24), (2, 1), (2, 8), (2, 15), (2, 22), (2, 29), (3, 7), (3, 14), (3, 21), (3, 28), (4, 5), (4, 12), (4, 19), (4, 26), (5, 4), (5, 11), (5, 18), (5, 25), (7, 2), (7, 9), (7, 16), (7, 23), (7, 23), (8, 1), (8, 8), (8, 29), (9, 6), (9, 6), (9, 13), (9, 13), (9, 20), (9, 27), (9, 27), (10, 5), (10, 12), (10, 19), (10, 26), (11, 3), (11, 10), (11, 17), (11, 24), (12, 2), (12, 2), (12, 9), (12, 16), (12, 23), (12, 30), (13, 7), (13, 14), (13, 21), (13, 28), (None,None), (1, 3)], [(1, 24), (2, 1), (2, 8), (2, 15), (2, 22), (2, 29), (3, 6), (3, 13), (3, 20), (3, 27), (4, 4), (4, 11), (4, 18), (4, 25), (5, 3), (5, 10), (5, 17), (5, 24), (7, 1), (7, 8), (7, 15), (7, 22), (7, 29), (8, 7), (8, 14), (8, 28), (9, 5), (9, 5), (9, 12), (9, 12), (9, 19), (9, 26), (9, 26), (10, 4), (10, 11), (10, 18), (10, 25), (11, 2), (11, 9), (11, 16), (11, 23), (12, 1), (12, 1), (12, 8), (12, 15), (12, 22), (12, 29), (13, 6), (13, 13), (13, 20), (13, 27), (None,None), (1, 3)], [(1, 24), (2, 1), (2, 8), (2, 15), (2, 22), (2, 29), (3, 7), (3, 14), (3, 21), (3, 28), (4, 6), (4, 13), (4, 20), (4, 27), (5, 5), (5, 12), (5, 19), (5, 26), (6, 3), (6, 10), (6, 17), (6, 24), (7, 1), (7, 8), (7, 15), (7, 22), (7, 29), (8, 7), (8, 14), (8, 28), (9, 5), (9, 12), (9, 19), (9, 26), (10, 4), (10, 11), (10, 18), (10, 25), (11, 2), (11, 9), (11, 16), (11, 23), (12, 1), (12, 8), (12, 15), (12, 22), (12, 29), (13, 6), (13, 13), (13, 20), (13, 27), (None,None), (1, 3)], [(1, 24), (2, 1), (2, 8), (2, 15), (2, 22), (2, 29), (3, 6), (3, 13), (3, 20), (3, 27), (4, 4), (4, 11), (4, 18), (4, 25), (5, 3), (5, 10), (5, 17), (5, 24), (6, 1), (6, 8), (6, 15), (6, 22), (6, 29), (7, 6), (7, 13), (7, 20), (7, 27), (8, 5), (8, 12), (8, 26), (9, 3), (9, 10), (9, 17), (9, 24), (10, 2), (10, 9), (10, 16), (10, 23), (10, 30), (11, 7), (11, 14), (11, 21), (11, 28), (12, 6), (12, 13), (12, 20), (12, 27), (13, 4), (13, 11), (13, 18), (13, 25), (13, 25), (1, 3)], [(1, 29), (2, 6), (2, 13), (2, 20), (2, 27), (3, 5), (3, 12), (3, 19), (3, 26), (4, 4), (4, 11), (4, 18), (4, 25), (5, 3), (5, 10), (5, 17), (5, 24), (7, 1), (7, 8), (7, 15), (7, 22), (7, 29), (7, 29), (8, 7), (8, 14), (8, 28), (9, 5), (9, 5), (9, 12), (9, 12), (9, 19), (9, 26), (9, 26), (10, 4), (10, 11), (10, 18), (10, 25), (11, 2), (11, 9), (11, 16), (11, 23), (12, 1), (12, 1), (12, 8), (12, 15), (12, 22), (12, 29), (13, 6), (13, 13), (13, 20), (13, 27),
 (None,None), (1, 8)], [(1, 29), (2, 6), (2, 13), (2, 20), (2, 27), (3, 4), (3, 11), (3, 18), (3, 25), (4, 2), (4, 9), (4, 16), (4, 23), (5, 1), (5, 8), (5, 15), (5, 22), (5, 29), (7, 6), (7, 13), (7, 20), (7, 27), (7, 27), (8, 5), (8, 12), (8, 26), (9, 3), (9, 3), (9, 10), (9, 10), (9, 17), (9, 24), (9, 24), (10, 2), (10, 9), (10, 16), (10, 23), (10, 30), (11, 7), (11, 14), (11, 21), (11, 28), (11, 28), (12, 6), (12, 13), (12, 20), (12, 27), (13, 4), (13, 11), (13, 18), (13, 25), (13, 25), (1, 8)], [(1, 29), (2, 6), (2, 13), (2, 20), (2, 27), (3, 5), (3, 12), (3, 19), (3, 26), (4, 4), (4, 11), (4, 18), (4, 25), (5, 3), (5, 10), (5, 17), (5, 24), (6, 1), (6, 8), (6, 15), (6, 22), (6, 29), (7, 6), (7, 13), (7, 20), (7, 27), (8, 5), (8, 12), (8, 26), (9, 3), (9, 10), (9, 17), (9, 24), (10, 2), (10, 9), (10, 16), (10, 23), (10, 30), (11, 7), (11, 14), (11, 21), (11, 28), (11, 28), (12, 6), (12, 13), (12, 20), (12, 27), (13, 4), (13, 11), (13, 18), (13, 25), (13, 25), (1, 8)], [(1, 29), (2, 6), (2, 13), (2, 20), (2, 27), (3, 4), (3, 11), (3, 18), (3, 25), (4, 2), (4, 9), (4, 16), (4, 23), (5, 1), (5, 8), (5, 15), (5, 22), (5, 29), (6, 6), (6, 13), (6, 20), (6, 27), (7, 4), (7, 11), (7, 18), (7, 25), (8, 3), (8, 10), (8, 24), (9, 1), (9, 8), (9, 15), (9, 22), (9, 29), (10, 14), (10, 21), (10, 28), (11, 5), (11, 12), (11, 12), (11, 19), (11, 26), (11, 26), (12, 4), (12, 11), (12, 18), (12, 25), (13, 2), (13, 9), (13, 16), (13, 23), (13, 23), (1, 8)]]

def calc_parsha(year, parsha, israel=False):
    # Step one: ascertain year type
    metonicCycle, metonicYear, molad, tishrei1 = njdate._find_start_of_year(year)
    molad.add_lunar_cycles(njdate.months_in_metonic_year(metonicYear))
    nextTishrei1= njdate._get_first_day_of_year((metonicYear + 1) % 19, molad)
    yearLength = nextTishrei1 - tishrei1
    leapyear   = njdate.is_leap_year(year)
    ytype = _year_types[((tishrei1%7)+1, yearLength, leapyear)]
    month, day = _lmap[ytype][parsha]
    if not month:
        return None
    return njdate.JewishDate(year, month, day)

  
def _gentable_reverse(year, israel=False):
    """Return of parshas to dates they fall out on.

    The numbers start with Beraishis as 0. Double parshios are represented
    as a list of the two numbers. If there is no Parsha the value is None.
    """
    parshalist = deque([51, 52] + list(range(52)))
    table = OrderedDict()
    leap = njdate.is_leap_year(year)
    pesachday = njdate.JewishDate(year, NISAN, 15).weekday()
    rosh_hashana = njdate.JewishDate(year, TISHREI, 1)
    shabbos = rosh_hashana.addDays(2).getShabbos()
    if rosh_hashana.weekday() > 4:
        parshalist.popleft()

    while shabbos.year == year:
        if not _parshaless(shabbos, israel):
            parsha = parshalist.popleft()
            table[parsha] = shabbos
            if (
                (parsha == 21 and (njdate.JewishDate(year, NISAN, 14) - shabbos).days // 7 < 3) or
                (parsha in [26, 28] and not leap) or
                (parsha == 31 and not leap and (
                                                not israel or pesachday != 7
                                                )) or
                (parsha == 38 and not israel and pesachday == 5) or
                (parsha == 41 and (njdate.JewishDate(year, AV, 9)-shabbos).days // 7 < 2)  or
                (parsha == 50 and njdate.JewishDate(year+1, TISHREI, 1).weekday() > 4)
                ):  #  If any of that then it's a double parsha.
                table[parshalist.popleft()] = shabbos
        shabbos = shabbos.addDays(7)
    return table

def _invert_gentable (year, israel=False):
    rdict = {}
    base = _gentable(year, israel)

    for key in base.keys():
        if base[key]:
            for p in base[key]:
                rdict[p] = key

    return rdict

def getdate_of_parsha(year, parsha, israel=False):
    table = _gentable_reverse(year, israel)
    """special case: vayelech year split"""
    if parsha == 51 and 51 not in table.keys():
        table = _gentable_reverse(year+1, israel)
    return table[parsha]
    """ end of my mods"""


def getparsha(date, israel=False):
    """Return the parsha for a given date.

    Returns the parsha for the Shabbos on or following the given
    date.

    Parameters
    ----------
    date : jewishDate
      This date does not have to be a Shabbos.

    israel : bool, optional
      ``True`` if you want the parsha according to the Israel schedule
      (with only one day of Yom Tov). Defaults to ``False``.

    Returns
    -------
    list of ints or ``None``
      A list of the numbers of the parshios for the Shabbos of the given date,
      beginning with 0 for Beraishis, or ``None`` if the Shabbos doesn't
      have a parsha (i.e. it's on Yom Tov).
    """
    shabbos = date.getShabbos()
    table = _gentable(shabbos.year, israel)
    return table[shabbos]


def getparsha_string(date, israel=False):
    """Return the parsha as a string for the given date.

    This function wraps ``getparsha`` returning a the parsha name
    transliterated into English.

    Parameters
    ----------
    date : ``HebrewDate``, ``GregorianDate``, or ``JulianDay``
      This date does not have to be a Shabbos.

    israel : bool, optional
      ``True`` if you want the parsha according to the Israel schedule
      (with only one day of Yom Tov). Defaults to ``False``.

    Returns
    -------
    str or ``None``
      The name of the parsha seperated by a comma and space if it is a
      double parsha or ``None`` if there is no parsha that Shabbos
      (ie. it's yom tov).
    """
    parsha = getparsha(date, israel)
    if parsha is None:
        return None
    name = [PARSHIOS[n] for n in parsha]
    return ', '.join(name)


def iterparshios(year, israel=False):
    """Generate all the parshios in the year.

    Parameters
    ----------
    year : int
      The Hebrew year to get the parshios for.

    israel : bool, optional
      ``True`` if you want the parsha according to the Israel schedule
      (with only one day of Yom Tov). Defaults to ``False``

    Yields
    ------
    str
      A list of the numbers of the parshios for the next Shabbos in the given year.
      Yields ``None`` for a Shabbos that doesn't have its own parsha
      (i.e. it occurs on a yom tov).
    """
    table = _gentable(year, israel)
    for shabbos in table:
        yield table[shabbos]


def parshatable(year, israel=False):
    """Return a table of all the Shabbosos in the year

    Parameters
    ----------
    year : int
      The Hebrew year to get the parshios for.

    israel : bool, optional
      ``True`` if you want the parshios according to the Israel
      schedule (with only one day of Yom Tov). Defaults to ``False``.

    Returns
    -------
    OrderedDict
      An ordered dictionary with the date of each Shabbos
      as the key mapped to the parsha as a list of ints, or ``None`` for a
      Shabbos with no parsha.
    """
    return _gentable(year, israel)

