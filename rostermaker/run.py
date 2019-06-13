import sys
import gettext as gt

# import functions
# from roster import Roster

try:
    exec(compile(open("input", "rb").read(), "input", 'exec'))
except FileNotFoundError:
    sys.exit("No input file found. Aborting.")
exec(compile(open("functions.py", "rb").read(), "functions.py", 'exec'))
exec(compile(open("roster.py", "rb").read(), "roster.py", 'exec'))

# set locale
langs = ['de']  # all translations we support
langs_en = ['en'] + langs
if setlang in langs:
    lang = gt.translation('all', localedir='../locales', languages=[setlang])
    lang.install()
elif setlang != 'en':
    str_langs_en = ', '.join(langs_en)
    errp1 = "Language '%s' not supported." % setlang
    errp2 = "Only available: %s." % str_langs_en
    errp3 = "Continuing in English."
    print(' '.join([errp1, errp2, errp3]))
else:  # fall back to default English
    _ = gt.gettext


# evaluate input
nqualified = len(qualified)
nregular = len(regular)
ntotal = nqualified + nregular


arrvacqualified = []
for i in range(0, nqualified):
    arrvacqualified.append("")
arrvacregular = []
for i in range(0, nregular):
    arrvacregular.append("")

# Initialize roster
roster = Roster(nshiftsperday, qualified, regular, monthno, year)
roster.setvacations(vacations)

# Calculate the weekend-days
arrwe = []
for i in range(0, roster.ndays):
    weekday = (monthstartswith + i) % 7
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
while (not ok) and ntries < maxntries:
    try:
        ntries += 1
        if(ntries > 0):
            roster.makeempty()
        if ntries % printtrynumbermod == 0:
            print(_("Try #"), str(ntries))
        tryresult = roster.tryfill()
        if tryresult != 0:
            continue
        # now check for clashes with restrictions
        clash = False
        for i in qualified + regular:
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
    if printfailedoutput is True:
        print(_("This is what I have:"))
        roster.printfull()
    if printfailreasons is True:
        for i in qualified + regular:
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