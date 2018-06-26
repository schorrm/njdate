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

from __future__ import division
from __future__ import unicode_literals

from collections import deque, OrderedDict

from pyluach.dates import HebrewDate
from pyluach.utils import memoize

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

