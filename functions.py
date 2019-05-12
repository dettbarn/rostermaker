#!/usr/local/bin/python3.5

import random

exec(compile(open("exceptions.py", "rb").read(), "exceptions.py", 'exec'))


# find out if a certain employee is in a certain shiftstring
def isinshift(employee, shiftstring):
    splitted = shiftstring.split(str_sep)
    for i in splitted:
        if i == employee:
            return True
    return False


# find out if a certain employee works on a certain day
def isinday(employee, arr, theday):
    isinday = False
    for ishift in range(0, nshiftsperday):
        if isinshift(employee, arr[theday][ishift]):
            isinday = True
    return isinday


def whatinday(employee, arr, theday):
    if hasvacationthatday(employee, theday):
        return "U"
    for ishift in range(0, nshiftsperday):
        if isinshift(employee, arr[theday][ishift]):
            return shiftnames[ishift]
    return "-"


def setvacation(employee, vacstr):
    for i in range(0, nqualified):
        if qualified[i] == employee:
            arrvacqualified[i] = vacstr
            return 0
    for i in range(0, nregular):
        if regular[i] == employee:
            arrvacregular[i] = vacstr
            return 0
    print(_("Error in setvacation: Employee \"%s\" not found.") % employee)
    return 1


def getvacation(employee):
    for i in range(0, nqualified):
        if qualified[i] == employee:
            return arrvacqualified[i]
    for i in range(0, nregular):
        if regular[i] == employee:
            return arrvacregular[i]
    print(_("Error in getvacation: Employee \"%s\" not found.") % employee)
    return 1


def setthevacations():  # months start with 0 in this definition
    for employee in vacations:
        setvacation(employee, vacations[employee])


def hasvacationthatday(employee, theday):
    strvacdays = getvacation(employee)
    arrvacdays = strvacdays.split(",")
    for vacday in arrvacdays:
        if vacday == str(theday):
            return True
    return False


def getnvacdays(employee):
    vacstr = getvacation(employee)
    splitted = vacstr.split(str_sep)
    return len(splitted)


# does not recognize previous months yet
def isinalllastndays(employee, arr, currentday, ndays):
    if currentday - ndays < 0:
        return False  # because reaches last month, we don't know
    for iday in range(currentday - ndays, currentday):
        if not isinday(employee, arr, iday):
            return False
    return True  # enough days to test, and there hasn't been one day without this employee


# does not recognize previous months yet
# is in all last n days, but not the day before that
def isinexactlyalllastndays(employee, arr, currentday, ndays):
    if currentday - ndays - 1 < 0:
        return False  # because reaches last month, we don't know
    if (isinalllastndays(employee, arr, currentday, ndays) and
       isinday(employee, arr, currentday - ndays - 1)):
        return True
    return False


def addtoshift(employee, shiftstring):
    if shiftstring != "":
        shiftstring += str_sep
    shiftstring += employee
    return shiftstring


def emptyarr(ndays, nshiftsperday):
    arr = []
    for iday in range(0, ndays):
        x = []
        for ishift in range(0, nshiftsperday):
            x.append("")
        arr.append(x)
    return arr


def getindivsched(employee, arr):
    sched = ""
    for i in range(0, ndays):
        sched += str(i + 1) + " " + whatinday(employee, arr, i) + "\n"
    return sched


def hasfreeweekends(employee, arr):
    nfreeweekends = 0
    for i in range(0, nwedays):
        # only check Saturdays that are followed by Sundays within the month
        if i < nwedays - 1 and arrwe[i] + 1 == arrwe[i + 1]:
            if (not isinday(employee, arr, arrwe[i])) and (not isinday(employee, arr, arrwe[i + 1])):
                nfreeweekends += 1
    return nfreeweekends


# returns false if shifts are equal, true if not.
# returns also false if one of shifts is 'undef' or some other non-shift meta-identifier
def isshiftchange(shift1, shift2):
    if ((shift1 in shiftnames) and (shift2 in shiftnames) and shift1 != shift2):
        return True
    else:
        return False


# get last shift, BEFORE the shift currently considered
def getlastshiftname(employee, arr, curday, curshift):
    for ishift in range(curshift, 0):
        if isinshift(employee, arr[iday][ishift]):
            return shiftnames[ishift]
    for iday in range(curday, 0):
        for ishift in range(nshiftsperday, 0):
            if isinshift(employee, arr[iday][ishift]):
                return shiftnames[ishift]
    # reaches beginning of month, still not found, so it's undefined
    return "undef"


# get last day, BEFORE the day currently considered
def getlastday(employee, arr, curday):
    lastday = -1
    for iday in range(0, curday):
        if isinday(employee, arr, iday):
            lastday = iday
    # reaches beginning of month, still not found, so it's undefined
    return lastday


def poplastfilled(arr):
    for iday in range(ndays, 0):
        for ishift in range(nshiftsperday, 0):
            if arr[iday][ishift] != "":
                arr[iday][ishift] == ""
                return arr
#    print("Tried to pop last filled, but array was already empty.")
    return arr


# give a weighted random out of n items, where the array wgtarr supplies the weights for each item
# the output is an integer between 0 and n-1, denoting the randomly chosen item
def weightedrnd(wgtarr):
    newwgtarr = wgtarr
    nwgts = len(newwgtarr)
    if min(newwgtarr) < 0:
        print(_("No negative weights allowed. Assuming all weights to be unity."))
        for i in range(0, nwgts):
            newwgtarr[i] = 1
    elif min(newwgtarr) == 0 and max(newwgtarr) == 0:
        raise AllWeightsZeroException()
    rndval = random.uniform(0, sum(wgtarr))
    cur = rndval
    # go through the array, to find where we have landed
    for i in range(0, nwgts):
        if newwgtarr[i] > cur:
            return i
        else:
            cur -= newwgtarr[i]


# pick randomly an item in a list
def pick(itemarr):
    nitems = len(itemarr)
    return itemarr[random.randrange(0, nitems)]


# pick randomly an item in a list, weighted by wgtarr
def pickweighted(itemarr, wgtarr):
    if len(itemarr) == 0:
        print(_("ERROR: Zero items given."))
        return -1
    elif len(itemarr) != len(wgtarr):
        print(_("ERROR: itemarr and wgtarr have different lengths. I give you the first item."))
        return itemarr[0]
    try:
        return itemarr[weightedrnd(wgtarr)]
    except AllWeightsZeroException:
        raise NonePickableException
        return -1


# Pick randomly an item in a list and return it
# Favorites are supplied with favsarr, each weighted by favwgt
# Others have weight 1
def pickwithfavorites(itemarr, favsarr, favwgt):
    nitems = len(itemarr)
    if nitems == 0:
        print(_("ERROR: Zero items given."))
        return -1
    if favwgt <= 0:
        print(_("ERROR: Favorites must have positive weight."))
    wgtarr = []
    for i in range(0, nitems):
        if itemarr[i] in favsarr:
            wgtarr.append(favwgt)
        else:
            wgtarr.append(1)
    return pickweighted(itemarr, wgtarr)


# Pick randomly an item in a list and return it
# Favorites are supplied with favsarr, each weighted by favwgt
# Others have weight 1
# vetoarr supplies vetoed items (weight 0)
# Veto overrides a weight, i.e. if an item is both in favsarr and vetoarr, weight will be zero
def pickwithfavoritesandvetoes(itemarr, favsarr, favwgt, vetoarr):
    nitems = len(itemarr)
    if nitems == 0:
        print(_("ERROR: Zero items given."))
        return -1
    if favwgt <= 0:
        print(_("ERROR: Favorites must have positive weight."))
    wgtarr = []
    for i in range(0, nitems):
        if itemarr[i] in vetoarr:
            wgtarr.append(0)
        elif itemarr[i] in favsarr:  # only if it's in favsarr but not in vetoarr
            wgtarr.append(favwgt)
        else:  # found in neither favsarr nor in vetoarr
            wgtarr.append(1)
    try:
        return pickweighted(itemarr, wgtarr)
    except NonePickableException:
        return ""


# Favorites, vetoes etc. now nicely arranged in an Priorities object.
def pickwithpriorities(itemarr, prio):
    nitems = len(itemarr)
    if nitems == 0:
        print(_("ERROR: Zero items given."))
        return -1
    wgtarr = []
    for i in range(0, nitems):
        if itemarr[i] in prio.dict.keys():
            wgtarr.append(prio.dict[itemarr[i]])
        else:  # not found in prio
            wgtarr.append(1)
    try:
        return pickweighted(itemarr, wgtarr)
    except NonePickableException:
        return ""


# Check if it would be ok to add this employee (rnd) at this day and shift
def wouldbeok(rnd, arr, iday, ishift):
    if isinshift(rnd, arr[iday][ishift]):
        return False  # already there
    elif (ishift >= 1 and isinshift(rnd, arr[iday][ishift - 1])):
        return False  # already in preceding shift (same day)
    elif (ishift == 0 and isinshift(rnd, arr[iday - 1][ishift + 2])):
        return False  # already in preceding shift (previous day)
    elif (ishift - 2 >= 0 and isinshift(rnd, arr[iday][ishift - 2])):
        return False  # already in two shifts ago, same day
    elif isinalllastndays(rnd, arr, iday, maxdaysinrow):
        return False  # already has maximum shifts in row at this point
    elif hasvacationthatday(rnd, iday):
        return False  # has vacation this day
    elif (isinalllastndays(rnd, arr, iday - 1, ndaysinrowtorequiretwofree) and not isinday(rnd, arr, iday - 1)):
        return False  # had free yesterday, but had a big number of days in row directly before that, which requires two free days
    return True


# space-padded two-digit string for days: " 1"..."31"
def daystr(day):
    if day < 10:
        return " " + str(day)
    return str(day)


# zero-padded two-digit string: "01"..."99"
def twodigit(n):
    if n < 10:
        return "0" + str(n)
    return str(day)


def monthstr(monthno):
    if monthno == 1:
        return _("January")
    elif monthno == 2:
        return _("February")
    elif monthno == 3:
        return _("March")
    elif monthno == 4:
        return _("April")
    elif monthno == 5:
        return _("May")
    elif monthno == 6:
        return _("June")
    elif monthno == 7:
        return _("July")
    elif monthno == 8:
        return _("August")
    elif monthno == 9:
        return _("September")
    elif monthno == 10:
        return _("October")
    elif monthno == 11:
        return _("November")
    elif monthno == 12:
        return _("December")
    raise IllegalMonthException(_("Error in monthstr: Illegal month number."))
    return "undef"


# Only respects the 400-year period.
# Deviations have to be implemented separately
def isleapyear(year):
    if year % 400 == 0:
        return True
    elif year % 100 == 0:
        return False
    elif year % 4 == 0:
        return True
    return False


def ndays(monthno, year):
    if monthno == 1 or monthno == 3 or monthno == 5 or monthno == 7 or monthno == 8 or monthno == 10 or monthno == 12:
        return 31
    elif monthno == 4 or monthno == 6 or monthno == 9 or monthno == 11:
        return 30
    elif monthno == 2:
        if isleapyear(year):
            return 29
        else:
            return 28
    else:
        raise IllegalMonthException(_("Error in ndays: Illegal month number."))
        return -1
