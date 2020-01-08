import sys
import gettext as gt
import calendar

# import functions
# from roster import Roster

exec(compile(open("functions.py", "rb").read(), "functions.py", 'exec'))
exec(compile(open("roster.py", "rb").read(), "roster.py", 'exec'))

from config import Config
import restrictions as re

conf = Config()
conf.setdefault()
conf.setqualified(["A", "B", "C", "D", "E", "F", "G"])
conf.setregular(["a", "b", "c", "d", "e", "f", "g", "h", "i"])
conf.setmonth(1)
conf.setyear(2001)
restr = re.Restrictions()
restr._setall([3, 1, 10, 1, 0, 1, 6, 3, 7, 1, 2, 3])
conf.setrestrictions(restr.dict)
conf.setlanguage('en')

# set locale
langs = ['de']  # all translations we support
langs_en = ['en'] + langs
if conf.setlang in langs:
    lang = gt.translation('all', localedir='../locales', languages=[conf.setlang])
    lang.install()
elif conf.setlang != 'en':
    str_langs_en = ', '.join(langs_en)
    errp1 = "Language '%s' not supported." % conf.setlang
    errp2 = "Only available: %s." % str_langs_en
    errp3 = "Continuing in English."
    print(' '.join([errp1, errp2, errp3]))
else:  # fall back to default English
    _ = gt.gettext


print(_("Roster configuration:"))
conf.setyear(promptint(conf.year, "Year"))
conf.setmonth(promptint(conf.monthno, "Month number"))
conf.setmonthstartswith(calendar.monthrange(conf.year, conf.monthno)[0])
conf.setqualified(promptstr(','.join(conf.qualified), "Qualified employees").split(','))
conf.setregular(promptstr(','.join(conf.regular), "Regular employees").split(','))
print("Please put in the vacation days for each employee.")
print("(List of all employees: %s)" % ','.join(conf.qualified + conf.regular))
emplq = ''
while True:
    empl = input("Next employee (empty for quit): ")
    if empl == '':
        break
    if empl not in (conf.qualified + conf.regular):
        print("Employee %s does not exist. Please try again." % empl)
        continue
    valid = False
    empty = False
    while not valid:
        vacstr1 = input("Vacation days for %s (comma-separated): " % empl)
        if vacstr1 == '':
            vacarr0 = []
            empty = True
            break
        vacarr1 = vacstr1.split(',')
        try:
            valid = True
            vacarr0 = [str(int(x) - 1) for x in vacarr1]
        except ValueError:
            print("Please enter a comma-separated list of days in the month. (empty for none)")
            valid = False
    if empty:
        break
    vacstr0 = ','.join(vacarr0)
    conf.setvacation(empl, vacstr0)


# evaluate input
nqualified = len(conf.qualified)
nregular = len(conf.regular)
ntotal = nqualified + nregular


arrvacqualified = []
for i in range(0, nqualified):
    arrvacqualified.append("")
arrvacregular = []
for i in range(0, nregular):
    arrvacregular.append("")

# Initialize roster
roster = Roster(len(conf.shiftnames), conf.qualified, conf.regular, conf.monthno, conf.year)
roster.setvacations(conf.vacations)
roster.setconf(conf)

# Calculate the weekend-days
arrwe = []
for i in range(0, roster.ndays):
    weekday = (conf.monthstartswith + i) % 7
    if weekday == 5 or weekday == 6:
        arrwe.append(i)
nwedays = len(arrwe)

print(_("Number of qualified employees: %d") % nqualified)
print(_("Number of other employees: %d") % nregular)
print(_("Weekend days: %s") % str(arrwe))
print(_("Number of weekend days: %d") % nwedays)

ok = False
ntries = 0
print(_("Starting calculation."))
while (not ok) and ntries < conf.maxntries:
    try:
        ntries += 1
        if(ntries > 0):
            roster.makeempty()
        if ntries % conf.printtrynumbermod == 0:
            print(_("Try #"), str(ntries))
        tryresult = roster.tryfill()
        if tryresult != 0:
            continue
        # now check for clashes with restrictions
        clash = False
        for i in conf.qualified + conf.regular:
            if roster.nclashes(i) >= 1:
                clash = True
        if not clash:
            ok = True
    except KeyboardInterrupt:
        print(_("Calculation stopped by KeyboardInterrupt."))
        break
    except SystemExit:
        print(_("Calculation stopped by SystemExit."))
        break
    except:
        print(_("Unknown error occurred during calculation."))
        raise

if ok:
    print(_("Worked on try number: # %d.") % ntries)
    roster.printfull()
    exportq = 'y'
    prefix = 'roster'
else:
    print(_("Did not work after %d tries.") % ntries)
    if conf.printfailedoutput is True:
        print(_("This is what I have:"))
        roster.printfull()
    if conf.printfailreasons is True:
        for i in conf.qualified + conf.regular:
            failstring = ', '.join(roster.clashes(i))
            print(_("%s problems: %s") % (i, failstring))
    exportq = "undef"
    while exportq not in ['y', 'n']:
        exportq = input(_("Export though? (y/n)  "))
    prefix = 'failedroster'

if exportq == 'y':
    formatq = input(_("Please enter export formats, comma separated\n(empty for full export): "))
    folderq = input(_("Please enter directory (empty for default): "))
    if folderq == '':
        folderq = '.'  # default export folder
    if formatq == '':
        roster.exportfull(prefix, folderq)
    else:
        roster.exports(prefix, formatq.split(','), folderq)
