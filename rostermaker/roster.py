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
        supported = ["out"]
        if fileformat not in supported:
            print(_("Error: file format \"%s\" not supported. Exporting generic .out file.") % fileformat)
            fileformat = "out"
        stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        ym = str(year) + "-" + twodigit(monthno)
        f = open(prefix + "_" + ym + "_" + stamp + "." + fileformat, "w+")
        if fileformat == "out":
            f.write(self.getheadline() + "\r\n")
            f.write(self.getfullschedtable() + "\r\n")
        f.close()

    def getheadline(self):
        return _("---  %s %d roster  ---") % (monthstr(self.monthno), self.year)

    def getfullschedtable(self):
        return self.getindivschedtable(self.qualified + self.regular)

    def getindivschedtable(self, thesemembers):
        schedtab = str(thesemembers) + "\n"
        for iday in range(0, self.ndays):
            schedtab += daystr(iday + 1) + "  "
            for memb in thesemembers:
                schedtab += " " + whatinday(memb, self.arr, iday)
            schedtab += "\n"
        return schedtab

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
                            if isinalllastndays(employee, self.arr, iday, maxdaysinrow):
                                prio.setweight(employee, 0)
                            elif isinalllastndays(employee, self.arr, iday, maxdaysinrow - 1):
                                prio.setweight(employee, favwgtdimin)
                            elif isinexactlyalllastndays(employee, self.arr, iday, 2):
                                prio.setweight(employee, favwgtaugm)
                            elif isinexactlyalllastndays(employee, self.arr, iday, 1):
                                prio.setweight(employee, favwgtaugm)
                            else:
                                prio.setweight(employee, favwgt)
                        for employee in (self.qualified + self.regular):
                            lastshiftname = getlastshiftname(employee, self.arr, iday, ishift)
                            if lastshiftname != shiftnames[ishift]:
                                # Scale weight down if would be shift change
                                lastday = getlastday(employee, self.arr, iday)
                                if lastday >= 0 and iday - lastday == 1:
                                    prio.scaleweight(employee, sclshiftjump)
                                else:
                                    prio.scaleweight(employee, sclshiftchng)
                    for i in range(0, kquali):
                        # weighted averaging:
                        rnd = pickwithpriorities(self.qualified, prio)
                        # this one-shift-of-person-per-day is implicitly assumed here
                        # (without using the integer defined above)
                        nfails = 0
                        while not wouldbeok(rnd, self.arr, iday, ishift):
                            nfails += 1
                            if nfails > maxnfails:
                                return 1
                            rnd = pickwithpriorities(self.qualified, prio)
                        self.arr[iday][ishift] = addtoshift(rnd, self.arr[iday][ishift])
                    for i in range(0, kreg):
                        # weighted averaging:
                        rnd = pickwithpriorities(self.regular, prio)
                        nfails = 0
                        # this one-shift-of-person-per-day is implicitly assumed here
                        # (without using the integer defined above)
                        while not wouldbeok(rnd, self.arr, iday, ishift):
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
            if isinday(employee, self.arr, i):
                nshiftchangesthere = 0
                for j in range(i + 1, self.ndays):
                    if isinday(employee, self.arr, j):
                        thatdayshiftname = whatinday(employee, self.arr, j)
                        prevdayshiftname = whatinday(employee, self.arr, j - 1)
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
        if hasfreeweekends(employee, self.arr) < minfreeweekends:
            clashesarr += [_("free weekends")]
        if self.findmaxshiftchangesseries(employee) > maxshiftchangesperseries:
            clashesarr += [_("shift series")]
        if self.countshiftchangespermonth(employee) > maxshiftchangespermonth:
            clashesarr += [_("monthly shift changes")]
        if self.countworkdays(employee) < minworkdayseachperson * (self.ndays - getnvacdays(employee)) / self.ndays:
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
            if isinday(employee, self.arr, i):
                thisshiftname = whatinday(employee, self.arr, i)
                if isshiftchange(lastshiftname, thisshiftname):
                    number += 1
                lastshiftname = thisshiftname
        return number

    def countworkdays(self, employee):
        number = 0
        for iday in range(0, self.ndays):
            if isinday(employee, self.arr, iday):
                number += 1
        return number
