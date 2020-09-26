from datetime import datetime

import priorities as p

from functions import *

# gettext fallback
try:
    _
except NameError:
    def _(s): return s


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
        nqualified = len(self.qualified)
        nregular = len(self.regular)
        self.arrvacqualified = []
        self.arrvacregular = []
        for i in range(0, nqualified):
            self.arrvacqualified.append("")
        for i in range(0, nregular):
            self.arrvacregular.append("")

    def setvacation(self, employee, vacstr):
        nqualified = len(self.qualified)
        nregular = len(self.regular)
        for i in range(0, nqualified):
            if self.qualified[i] == employee:
                self.arrvacqualified[i] = vacstr
                return 0
        for i in range(0, nregular):
            if self.regular[i] == employee:
                self.arrvacregular[i] = vacstr
                return 0
        print(_("Error in setvacation: Employee \"%s\" not found.") % employee)
        return 1

    def getvacation(self, employee):
        nqualified = len(self.qualified)
        nregular = len(self.regular)
        for i in range(0, nqualified):
            if self.qualified[i] == employee:
                return self.arrvacqualified[i]
        for i in range(0, nregular):
            if self.regular[i] == employee:
                return self.arrvacregular[i]
        print(_("Error in getvacation: Employee \"%s\" not found.") % employee)
        return 1

    # months start with 0 in this definition
    def setvacations(self, vacations):
        for employee in vacations:
            self.setvacation(employee, vacations[employee])

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

    supportedformats = ["out", "csv", "tex", "html", "xml", "json"]
    nl = "\n"  # default linebreak convention

    # export in all supported file formats
    def exportfull(self, prefix, folder="."):
        self.exports(prefix, Roster.supportedformats, folder)

    def exports(self, prefix, fileformats, folder="."):
        for fileformat in fileformats:
            self.export(prefix, fileformat, folder)

    def export(self, prefix, fileformat, folder="."):
        if fileformat not in Roster.supportedformats:
            print(_("Error: file format \"%s\" not supported. Exporting generic .out file.") % fileformat)
            fileformat = "out"
        stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        ym = str(self.conf.year) + "-" + twodigit(self.conf.monthno)
        f = open(folder + "/" + prefix + "_" + ym + "_" + stamp
                 + "." + fileformat, "w+")
        nl = Roster.nl
        if fileformat == "out":
            f.write(self.getheadline() + nl)
            f.write(self.getfullschedtable() + nl)
        if fileformat == "csv":
            f.write("# " + self.getheadline() + nl)
            f.write(self.getseptable(self.qualified + self.regular, ',') + nl)
        if fileformat == "tex":
            f.write("\\documentclass[10pt]{article}" + nl)
            f.write("\\usepackage[margin=2cm]{geometry}" + nl)
            f.write("\\title{" + self.getheadline() + "}" + nl)
            f.write("\\begin{document}" + nl)
            f.write("\\maketitle" + nl)
            f.write("\\begin{table}[ht]" + nl)
            f.write("\\centering" + nl)
            f.write("\\begin{tabular}{")
            f.write("r")  # day number right-aligned
            for i in (self.qualified + self.regular):
                f.write("c")
            f.write("}" + nl)
            f.write(" & ".join([""] + self.qualified + self.regular)
                    + " \\\\" + nl)
            f.write("\\hline" + nl)
            for i in range(0, self.ndays):
                f.write(self.getseprow(self.qualified + self.regular,
                                       i, " & ", " \\\\" + nl))
            f.write("\\end{tabular}" + nl)
            f.write("\\end{table}" + nl)
            f.write("\\end{document}" + nl)
        if fileformat == "html":
            f.write("<html>" + nl)
            f.write("<head>" + nl)
            f.write("<title>" + self.getheadline() + "</title>" + nl)
            f.write("</head>" + nl)
            f.write("<body>" + nl)
            f.write("<h1>" + self.getheadline() + "</h1>" + nl)
            f.write("<table>" + nl)
            f.write("<thead><th>")
            f.write("</th><th>".join([""] + self.qualified + self.regular)
                    + "</th></thead>" + nl)
            for i in range(0, self.ndays):
                f.write("<tr><td>")
                f.write(self.getseprow(self.qualified + self.regular,
                                       i, "</td><td>", "</td></tr>" + nl))
            f.write("</table>" + nl)
            f.write("</body>" + nl)
            f.write("</html>" + nl)
        if fileformat == "xml":
            t1 = "    "
            t2 = t1 + t1
            t3 = t1 + t1 + t1
            t4 = t1 + t1 + t1 + t1
            c = self.conf
            f.write("<roster month=" + str(c.monthno)
                    + " year=" + str(c.year) + ">" + nl)
            for i in range(0, self.ndays):
                f.write(t1 + "<day number=" + str(i + 1) + ">" + nl)
                for ishift in range(0, self.nshiftsperday):
                    f.write(t2 + "<shift type='"
                            + c.shiftnames[ishift] + "'>" + nl)
                    f.write(t3 + "<employee>" + nl + t4)
                    emplsep = (nl + t3 + "</employee>" + nl
                               + t3 + "<employee>" + nl + t4)
                    f.write(emplsep.join((self.arr[i][ishift])
                                         .split(self.conf.str_sep)) + nl)
                    f.write(t3 + "</employee>" + nl)
                    f.write(t2 + "</shift>" + nl)
                f.write(t1 + "</day>" + nl)
            f.write("</roster>" + nl)
        if fileformat == "json":
            t1 = "    "
            t2 = t1 + t1
            t3 = t1 + t1 + t1
            t4 = t1 + t1 + t1 + t1
            c = self.conf
            f.write("{" + nl)
            f.write(t1 + "\"roster\": {" + nl)
            f.write(t2 + "\"month\": " + str(c.monthno))
            f.write(", \"year\": " + str(c.year))
            f.write(", \"days\": [" + nl)
            for i in range(0, self.ndays):
                f.write(t3 + "{ \"number\": " + str(i + 1))
                f.write(", \"shifts\": [" + nl)
                for ishift in range(0, self.nshiftsperday):
                    f.write(t4 + "{ \"type\": \""
                            + c.shiftnames[ishift] + "\"")
                    f.write(", \"employees\": [ { \"employee\": \"")
                    emplsep = "\" }, { \"employee\": \""
                    f.write(emplsep.join((self.arr[i][ishift]).split(','))
                            + "\" } ] }")
                    if ishift < self.nshiftsperday - 1:
                        f.write(",")
                    f.write(nl)
                f.write(t3 + "] }")
                if i < self.ndays - 1:
                    f.write(",")
                f.write(nl)
            f.write(t2 + "]" + nl)
            f.write(t1 + "}" + nl)
            f.write("}" + nl)
        f.close()

    def getheadline(self):
        str_headline = _("---  %s %d roster  ---")
        return str_headline % (monthstr(self.monthno), self.year)

    def getfullschedtable(self):
        return self.getindivschedtable(self.qualified + self.regular)

    def getindivschedtable(self, thesemembers):
        schedtab = str(thesemembers) + Roster.nl
        for iday in range(0, self.ndays):
            schedtab += daystr(iday + 1) + "  "
            for memb in thesemembers:
                schedtab += " " + self.whatinday(memb, iday)
            schedtab += Roster.nl
        return schedtab

    def getseprow(self, thesemembers, iday, sep, end):
        row = ""
        row += daystr(iday + 1)
        for memb in thesemembers:
            row += sep + self.whatinday(memb, iday)
        row += end
        return row

    def getseptable(self, thesemembers, sep):
        pref = _("# (day)" + sep)
        table = pref + sep.join(self.qualified + self.regular) + Roster.nl
        for iday in range(0, self.ndays):
            table += self.getseprow(thesemembers, iday, sep, Roster.nl)
        return table

    def tryfill(self):
        c = self.conf
        r = c.restr
        for iday in range(0, self.ndays):
            for ishift in range(0, self.nshiftsperday):
                # only fill if empty (i.e. not pre-defined)
                if self.arr[iday][ishift] == "":
                    # we assume at first that all staff members are available
                    # we also assume that we work at minimum staff
                    kpersons = r.dict["minpersonspershift"]
                    kquali = 1
                    # kquali = r.randrange(minqualipershift,
                    #                      maxqualipershift + 1)
                    kreg = max(0, kpersons - kquali)
                    # first generate favorites and vetoes arrays
                    prio = p.Priorities()
                    if iday >= 1:
                        onedayago = ((self.arr[iday - 1][ishift])
                                     .split(c.str_sep))
                        for employee in onedayago:
                            # person only favorite
                            #   if not in all last (maxdaysinrow) days,
                            #   else vetoed.
                            if self.isinalllastndays(employee, iday,
                                                     r.dict["maxdaysinrow"]):
                                prio.setweight(employee, 0)
                            elif self.isinalllastndays(employee, iday,
                                                       (r.dict["maxdaysinrow"]
                                                        - 1)):
                                prio.setweight(employee, c.favwgtdimin)
                            elif self.isinexactlyalllastndays(employee,
                                                              iday, 2):
                                prio.setweight(employee, c.favwgtaugm)
                            elif self.isinexactlyalllastndays(employee,
                                                              iday, 1):
                                prio.setweight(employee, c.favwgtaugm)
                            else:
                                prio.setweight(employee, c.favwgt)
                        for employee in (self.qualified + self.regular):
                            lastshiftname = getlastshiftname(employee,
                                                             self.arr,
                                                             iday, ishift,
                                                             self.conf)
                            if lastshiftname != c.shiftnames[ishift]:
                                # Scale weight down if would be shift change
                                lastday = self.getlastday(employee, iday)
                                if lastday >= 0 and iday - lastday == 1:
                                    prio.scaleweight(employee, c.sclshiftjump)
                                else:
                                    prio.scaleweight(employee, c.sclshiftchng)
                    for i in range(0, kquali):
                        # weighted averaging:
                        rnd = pickwithpriorities(self.qualified, prio)
                        # this one-shift-of-person-per-day rule
                        # is implicitly assumed here
                        # (without using the integer defined above)
                        nfails = 0
                        while not self.wouldbeok(rnd, iday, ishift):
                            nfails += 1
                            if nfails > c.maxnfails:
                                return 1
                            rnd = pickwithpriorities(self.qualified, prio)
                        oldstr = self.arr[iday][ishift]
                        self.arr[iday][ishift] = addtoshift(rnd, oldstr,
                                                            self.conf)
                    for i in range(0, kreg):
                        # weighted averaging:
                        rnd = pickwithpriorities(self.regular, prio)
                        nfails = 0
                        # this one-shift-of-person-per-day rule
                        # is implicitly assumed here
                        # (without using the integer defined above)
                        while not self.wouldbeok(rnd, iday, ishift):
                            nfails += 1
                            if nfails > c.maxnfails:
                                return 2
                            rnd = pickwithpriorities(self.regular, prio)
                        oldstr = self.arr[iday][ishift]
                        self.arr[iday][ishift] = addtoshift(rnd, oldstr,
                                                            self.conf)
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
        r = self.conf.restr
        clashesarr = []
        if self.hasfreeweekends(employee) < r.dict["minfreeweekends"]:
            clashesarr += [_("free weekends")]
        if (self.findmaxshiftchangesseries(employee)
           > r.dict["maxshiftchangesperseries"]):
            clashesarr += [_("shift series")]
        if (self.countshiftchangespermonth(employee)
                > r.dict["maxshiftchangespermonth"]):
            clashesarr += [_("monthly shift changes")]
        availabledays = self.ndays - self.getnvacdays(employee)
        mindays_corr = (r.dict["minworkdayseachperson"]
                        * availabledays / self.ndays)
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
                if isshiftchange(lastshiftname, thisshiftname, self.conf):
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
        for ishift in range(0, self.nshiftsperday):
            if isinshift(employee, self.arr[theday][ishift], self.conf):
                isinday = True
        return isinday

    def whatinday(self, employee, theday):
        if self.hasvacationthatday(employee, theday):
            return "U"
        for ishift in range(0, self.conf.restr.dict["nshiftsperday"]):
            if isinshift(employee, self.arr[theday][ishift], self.conf):
                return self.conf.shiftnames[ishift]
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
        dic = self.conf.restr.dict
        if isinshift(rnd, self.arr[iday][ishift], self.conf):
            return False  # already there
        elif (ishift >= 1 and isinshift(rnd,
                                        self.arr[iday][ishift - 1],
                                        self.conf)):
            return False  # already in preceding shift (same day)
        elif (ishift == 0 and isinshift(rnd,
                                        self.arr[iday - 1][ishift + 2],
                                        self.conf)):
            return False  # already in preceding shift (previous day)
        elif (ishift - 2 >= 0 and isinshift(rnd,
                                            self.arr[iday][ishift - 2],
                                            self.conf)):
            return False  # already in two shifts ago, same day
        elif self.isinalllastndays(rnd, iday,
                                   dic["maxdaysinrow"]):
            return False  # already has maximum shifts in row at this point
        elif self.hasvacationthatday(rnd, iday):
            return False  # has vacation this day
        elif self.isinalllastndays(rnd, iday - 1,
                                   dic["ndaysinrowtorequiretwofree"]):
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
        arrwe = self.getwedays()
        nwedays = self.getnwedays()
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
            sched += str(i + 1) + " " + self.whatinday(employee, i) + Roster.nl
        return sched

    def hasvacationthatday(self, employee, theday):
        strvacdays = self.getvacation(employee)
        arrvacdays = strvacdays.split(self.conf.str_sep)
        for vacday in arrvacdays:
            if vacday == str(theday):
                return True
        return False

    def getnvacdays(self, employee):
        vacstr = self.getvacation(employee)
        splitted = vacstr.split(self.conf.str_sep)
        return len(splitted)

    def setconf(self, conf):
        self.conf = conf

    # Get weekend days of the month
    def getwedays(self):
        arrwe = []
        for i in range(0, self.ndays):
            weekday = (self.conf.monthstartswith + i) % 7
            if weekday == 5 or weekday == 6:
                arrwe.append(i)
        return arrwe

    # Get number of weekend days of the month
    def getnwedays(self):
        return len(self.getwedays())
