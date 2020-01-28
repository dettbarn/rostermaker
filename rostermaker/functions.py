import random
import gettext
import exceptions as e


# find out if a certain employee is in a certain shiftstring
def isinshift(employee, shiftstring, conf):
    splitted = shiftstring.split(conf.str_sep)
    for i in splitted:
        if i == employee:
            return True
    return False


# Add an employee to a shift string.
# Does not check if already in shift (use isinshift() for that)
def addtoshift(employee, shiftstring, conf):
    if shiftstring != "":
        shiftstring += conf.str_sep
    shiftstring += employee
    return shiftstring


# Construct and return an empty 2D array for a month roster.
def emptyarr(ndays, nshiftsperday):
    arr = []
    for iday in range(0, ndays):
        x = []
        for ishift in range(0, nshiftsperday):
            x.append("")
        arr.append(x)
    return arr


# Get individual schedule for a certain employee.
def getindivsched(employee, arr):
    sched = ""
    for i in range(0, ndays):
        sched += str(i + 1) + " " + whatinday(employee, arr, i) + "\n"
    return sched


# returns false if shifts are equal, true if not.
# returns also false if one of shifts is 'undef'
# or if one is some other non-shift meta-identifier
def isshiftchange(shift1, shift2, conf):
    if shift1 in conf.shiftnames and shift2 in conf.shiftnames:
        if shift1 != shift2:
            return True
    else:
        return False


# get last shift, BEFORE the shift currently considered
def getlastshiftname(employee, arr, curday, curshift, conf):
    for ishift in range(curshift, 0):
        if isinshift(employee, arr[iday][ishift], conf):
            return shiftnames[ishift]
    for iday in range(curday, 0):
        for ishift in range(nshiftsperday, 0):
            if isinshift(employee, arr[iday][ishift], conf):
                return shiftnames[ishift]
    # reaches beginning of month, still not found, so it's undefined
    return "undef"


# Empty the last filled shift in month roster array
def poplastfilled(arr):
    for iday in range(ndays, 0):
        for ishift in range(nshiftsperday, 0):
            if arr[iday][ishift] != "":
                arr[iday][ishift] == ""
                return arr
#    print("Tried to pop last filled, but array was already empty.")
    return arr


# give a weighted random out of n items,
# where the array wgtarr supplies the weights for each item
# the output is an integer between 0 and n-1, denoting the randomly chosen item
def weightedrnd(wgtarr):
    newwgtarr = wgtarr
    nwgts = len(newwgtarr)
    if min(newwgtarr) < 0:
        print(_("No negative weights allowed. Assuming all weights to be unity."))
        for i in range(0, nwgts):
            newwgtarr[i] = 1
    elif min(newwgtarr) == 0 and max(newwgtarr) == 0:
        raise e.AllWeightsZeroException()
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
    except e.AllWeightsZeroException():
        raise e.NonePickableException()
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
# Veto overrides a weight,
# i.e. if an item is both in favsarr and vetoarr, weight will be zero
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
        elif itemarr[i] in favsarr:  # only if in favsarr but not in vetoarr
            wgtarr.append(favwgt)
        else:  # found in neither favsarr nor in vetoarr
            wgtarr.append(1)
    try:
        return pickweighted(itemarr, wgtarr)
    except e.NonePickableException():
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
    except e.NonePickableException():
        return ""


# space-padded two-digit string for days: " 1"..."31"
def daystr(day):
    if day < 10:
        return " " + str(day)
    return str(day)


# zero-padded two-digit string: "01"..."99"
# invalid numbers will be forced in that scheme
def twodigit(n):
    n = round(abs(n))  # force non-negative integer
    if n < 10:
        return "0" + str(n)
    return str(n)[-2:]


# Get name of month with number monthno.
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
    str_illegalMonth = _("Error in monthstr: Illegal month number.")
    raise e.IllegalMonthException(str_illegalMonth)
    return "undef"


# Only respects the 400-year period.
# Gregorian calendar would also be extrapolated back in history
# Deviations have to be implemented separately
def isleapyear(year):
    if year % 400 == 0:
        return True
    elif year % 100 == 0:
        return False
    elif year % 4 == 0:
        return True
    return False


# Get number of days in a month.
# Because of leap-years, this depends also on the year.
def ndays(monthno, year):
    months31 = [1, 3, 5, 7, 8, 10, 12]
    months30 = [4, 6, 9, 11]
    if monthno in months31:
        return 31
    elif monthno in months30:
        return 30
    elif monthno == 2:
        if isleapyear(year):
            return 29
        else:
            return 28
    else:
        str_illegalMonth = _("Error in ndays: Illegal month number.")
        raise e.IllegalMonthException(str_illegalMonth)
        return -1


def promptint(cur, name):
    worked = 0
    while not worked:
        new = input("%s (empty for default %s): " % (name, str(cur)))
        if new == "":
            newint = cur
            break
        try:
            newint = int(new)
        except ValueError:
            print("    %s has to be an integer. Please try again." % name)
            continue
        worked = 1
    return newint

def promptstr(cur, name):
    worked = 0
    while not worked:
        new = input("%s (empty for default %s): " % (name, str(cur)))
        if new == "":
            newstr = cur
            break
        try:
            newstr = str(new)
        except ValueError:
            print("    %s has to be a string. Please try again." % name)
            continue
        worked = 1
    return newstr
