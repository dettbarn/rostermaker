import random as r

exec(compile(open("functions.py", "rb").read(), "functions.py", 'exec'))
exec(compile(open("priorities.py", "rb").read(), "priorities.py", 'exec'))


class Roster:
    def __init__(self, ndays, nshiftsperday, qualified, regular):
        self.ndays = ndays
        self.nshiftsperday = nshiftsperday
        self.arr = []
        for iday in range(0, self.ndays):
            x = []
            for ishift in range(0, self.nshiftsperday):
                x.append("")
            (self.arr).append(x)
        self.qualified = qualified
        self.regular = regular

    def makeempty(self):
        for iday in range(0, self.ndays):
            for ishift in range(0, self.nshiftsperday):
                (self.arr)[iday][ishift] = ""

    def print(self):
        print(self.arr)

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
                            if isinalllastndays(employee, self.arr, iday - 1, maxdaysinrow):
                                prio.setweight(employee, 0)
                            elif isinalllastndays(employee, self.arr, iday - 1, maxdaysinrow - 1):
                                prio.setweight(employee, favwgtdimin)
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
