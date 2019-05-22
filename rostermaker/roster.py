from datetime import datetime

exec(compile(open("input", "rb").read(), "input", 'exec'))
exec(compile(open("functions.py", "rb").read(), "functions.py", 'exec'))
exec(compile(open("priorities.py", "rb").read(), "priorities.py", 'exec'))


class Roster:
    def __init__(self, nshiftsperday, qualified, regular, monthno, year):
        self.nshiftsperday = nshiftsperday
        self.arr = []
        self.qualified = qualified
        self.regular = regular
        self.monthno = monthno
        self.year = year
        self.ndays = ndays(self.monthno, self.year)
        for iday in range(0, self.ndays):
            x = []
            for ishift in range(0, self.nshiftsperday):
                x.append("")
            (self.arr).append(x)

    def makeempty(self):
        for iday in range(0, self.ndays):
            for ishift in range(0, self.nshiftsperday):
                (self.arr)[iday][ishift] = ""

    def print(self):
        print(self.arr)

    def printtable(self):
        print(self.getheadline())
        print(self.getindivschedtable(self.qualified + self.regular))

    def printfull(self):
        self.print()
        self.printtable()

    def export(self, prefix, fileformat):
        supported = ["out", "csv"]
        if fileformat not in supported:
            print(_("Error: file format \"%s\" not supported. Exporting generic .out file.") % fileformat)
            fileformat = "out"
        stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        ym = str(year) + "-" + twodigit(monthno)
        f = open(prefix + "_" + ym + "_" + stamp + "." + fileformat, "w+")
        if fileformat == "out":
            f.write(self.getheadline() + "\r\n")
            f.write(self.getfullschedtable() + "\r\n")
        if fileformat == "csv":
            f.write("# " + self.getheadline() + "\r\n")
            f.write(self.getseptable(self.qualified + self.regular, ',') + "\r\n")
        f.close()

    def getheadline(self):
        str_headline = _("---  %s %d roster  ---")
        return str_headline % (monthstr(self.monthno), self.year)

    def getfullschedtable(self):
        return self.getindivschedtable(self.qualified + self.regular)

    def getindivschedtable(self, thesemembers):
        schedtab = str(thesemembers) + "\n"
        for iday in range(0, self.ndays):
            schedtab += daystr(iday + 1) + "  "
            for memb in thesemembers:
                schedtab += " " + self.whatinday(memb, iday)
            schedtab += "\n"
        return schedtab

    def getseprow(self, thesemembers, iday, sep):
        row = ""
        row += daystr(iday + 1)
        for memb in thesemembers:
            row += sep + self.whatinday(memb, iday)
        row += "\r\n"
        return row

    def getseptable(self, thesemembers, sep):
        table = _("# (day),") + ','.join(self.qualified + self.regular) + "\r\n"
        for iday in range(0, self.ndays):
            table += self.getseprow(thesemembers, iday, sep)
        return table

    def tryfill(self):
        for iday in range(0, self.ndays):
            for ishift in range(0, self.nshiftsperday):
                # only fill if empty (i.e. not pre-defined)
                if self.arr[iday][ishift] == "":
                    # we assume at first that all staff members are available
                    # we also assume that we work at minimum staff
                    kpersons = minpersonspershift
                    kquali = 1
                    # kquali = r.randrange(minqualipershift, maxqualipershift + 1)
                    kreg = max(0, kpersons - kquali)
                    # first generate favorites and vetoes arrays
                    prio = Priorities()
                    if iday >= 1:
                        onedayago = (self.arr[iday - 1][ishift]).split(str_sep)
                        for employee in onedayago:
                            # person only favorite
                            #   if not in all last (maxdaysinrow) days,
                            #   else vetoed.
                            if self.isinalllastndays(employee, iday, maxdaysinrow):
                                prio.setweight(employee, 0)
                            elif self.isinalllastndays(employee, iday, maxdaysinrow - 1):
                                prio.setweight(employee, favwgtdimin)
                            elif self.isinexactlyalllastndays(employee, iday, 2):
                                prio.setweight(employee, favwgtaugm)
                            elif self.isinexactlyalllastndays(employee, iday, 1):
                                prio.setweight(employee, favwgtaugm)
                            else:
                                prio.setweight(employee, favwgt)
                        for employee in (self.qualified + self.regular):
                            lastshiftname = getlastshiftname(employee, self.arr, iday, ishift)
                            if lastshiftname != shiftnames[ishift]:
                                # Scale weight down if would be shift change
                                lastday = self.getlastday(employee, iday)
                                if lastday >= 0 and iday - lastday == 1:
                                    prio.scaleweight(employee, sclshiftjump)
                                else:
                                    prio.scaleweight(employee, sclshiftchng)
                    for i in range(0, kquali):
                        # weighted averaging:
                        rnd = pickwithpriorities(self.qualified, prio)
                        # this one-shift-of-person-per-day rule
                        # is implicitly assumed here
                        # (without using the integer defined above)
                        nfails = 0
                        while not self.wouldbeok(rnd, iday, ishift):
                            nfails += 1
                            if nfails > maxnfails:
                                return 1
                            rnd = pickwithpriorities(self.qualified, prio)
                        self.arr[iday][ishift] = addtoshift(rnd, self.arr[iday][ishift])
                    for i in range(0, kreg):
                        # weighted averaging:
                        rnd = pickwithpriorities(self.regular, prio)
                        nfails = 0
                        # this one-shift-of-person-per-day rule
                        # is implicitly assumed here
                        # (without using the integer defined above)
                        while not self.wouldbeok(rnd, iday, ishift):
                            nfails += 1
                            if nfails > maxnfails:
                                return 2
                            rnd = pickwithpriorities(self.regular, prio)
                        self.arr[iday][ishift] = addtoshift(rnd, self.arr[iday][ishift])
        return 0

    # find the maximum number of shift changes
    #   that an employee has in one shift series, in this month
    def findmaxshiftchangesseries(self, employee):
        number = 0
        for i in range(0, self.ndays):
            if self.isinday(employee, i):
                nshiftchangesthere = 0
                for j in range(i + 1, self.ndays):
                    if self.isinday(employee, j):
                        thatdayshiftname = self.whatinday(employee, j)
                        prevdayshiftname = self.whatinday(employee, j - 1)
                        if thatdayshiftname != prevdayshiftname:
                            nshiftchangesthere += 1
                    else:
                        i = j  # skip outer for-loop directly to...
                        # ...where the inner for-loop has walked
                        number = max(number, nshiftchangesthere)  # update this
                        break  # break inner for-loop and go on with the month
        return number

    def clashes(self, employee):
        clashesarr = []
        if self.hasfreeweekends(employee) < minfreeweekends:
            clashesarr += [_("free weekends")]
        if self.findmaxshiftchangesseries(employee) > maxshiftchangesperseries:
            clashesarr += [_("shift series")]
        if self.countshiftchangespermonth(employee) > maxshiftchangespermonth:
            clashesarr += [_("monthly shift changes")]
        availabledays = self.ndays - getnvacdays(employee)
        mindays_corr = minworkdayseachperson * availabledays / self.ndays
        if self.countworkdays(employee) < mindays_corr:
            clashesarr += [_("work days")]
        return clashesarr

    def nclashes(self, employee):
        return len(self.clashes(employee))

    # find the total number of shift changes in this month
    # (here, a shift change can be between two shift series as well)
    # (but a shift change is not counted between two months)
    def countshiftchangespermonth(self, employee):
        number = 0
        lastshiftname = 'undef'
        for i in range(0, self.ndays):
            if self.isinday(employee, i):
                thisshiftname = self.whatinday(employee, i)
                if isshiftchange(lastshiftname, thisshiftname):
                    number += 1
                lastshiftname = thisshiftname
        return number

    def countworkdays(self, employee):
        number = 0
        for iday in range(0, self.ndays):
            if self.isinday(employee, iday):
                number += 1
        return number

    # find out if a certain employee works on a certain day
    def isinday(self, employee, theday):
        isinday = False
        for ishift in range(0, nshiftsperday):
            if isinshift(employee, self.arr[theday][ishift]):
                isinday = True
        return isinday

    def whatinday(self, employee, theday):
        if hasvacationthatday(employee, theday):
            return "U"
        for ishift in range(0, nshiftsperday):
            if isinshift(employee, self.arr[theday][ishift]):
                return shiftnames[ishift]
        return "-"

    # does not recognize previous months yet
    def isinalllastndays(self, employee, currentday, ndays):
        if currentday - ndays < 0:
            return False  # because reaches last month, we don't know
        for iday in range(currentday - ndays, currentday):
            if not self.isinday(employee, iday):
                return False
        return True  # enough days to test,
        # and there hasn't been one day without this employee

    # does not recognize previous months yet
    # is in all last n days, but not the day before that
    def isinexactlyalllastndays(self, employee, currentday, ndays):
        if currentday - ndays - 1 < 0:
            return False  # because reaches last month, we don't know
        if self.isinalllastndays(employee, currentday, ndays):
            if self.isinday(employee, currentday - ndays - 1):
                return True
        return False

    # Check if it would be ok to add this employee (rnd) at this day and shift
    def wouldbeok(self, rnd, iday, ishift):
        if isinshift(rnd, self.arr[iday][ishift]):
            return False  # already there
        elif (ishift >= 1 and isinshift(rnd, self.arr[iday][ishift - 1])):
            return False  # already in preceding shift (same day)
        elif (ishift == 0 and isinshift(rnd, self.arr[iday - 1][ishift + 2])):
            return False  # already in preceding shift (previous day)
        elif (ishift - 2 >= 0 and isinshift(rnd, self.arr[iday][ishift - 2])):
            return False  # already in two shifts ago, same day
        elif self.isinalllastndays(rnd, iday, maxdaysinrow):
            return False  # already has maximum shifts in row at this point
        elif hasvacationthatday(rnd, iday):
            return False  # has vacation this day
        elif self.isinalllastndays(rnd, iday - 1, ndaysinrowtorequiretwofree):
            if not self.isinday(rnd, iday - 1):
                return False  # had free yesterday,
                # but had a big number of days in row directly before that,
                # which requires two free days
        return True

    # get last day, BEFORE the day currently considered
    def getlastday(self, employee, curday):
        lastday = -1
        for iday in range(0, curday):
            if self.isinday(employee, iday):
                lastday = iday
        # reaches beginning of month, still not found, so it's undefined
        return lastday

    def hasfreeweekends(self, employee):
        nfreeweekends = 0
        for i in range(0, nwedays):
            # only check Saturdays followed by Sundays within the month
            if i < nwedays - 1 and arrwe[i] + 1 == arrwe[i + 1]:
                if not self.isinday(employee, arrwe[i]):
                    if not self.isinday(employee, arrwe[i + 1]):
                        nfreeweekends += 1
        return nfreeweekends

    def getindivsched(self, employee):
        sched = ""
        for i in range(0, ndays):
            sched += str(i + 1) + " " + self.whatinday(employee, i) + "\n"
        return sched
