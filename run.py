#!/usr/local/bin/python3.5

import gettext
exec(compile(open("functions.py", "rb").read(), "functions.py", 'exec'))
exec(compile(open("input", "rb").read(), "input", 'exec'))
exec(compile(open("roster.py", "rb").read(), "roster.py", 'exec'))

# set locale
langs = ['de']  # all translations we support
langs_en = ['en'] + langs
if setlang in langs:
    lang = gettext.translation('run', localedir='locales', languages=[setlang])
    lang.install()
elif setlang != 'en':  # English is default, no need to translate
    str_langs_en = ', '.join(langs_en)
    print("Language '%s' not supported. Only available: %s.  Continuing in English." % (setlang, str_langs_en))


# evaluate input
nqualified = len(qualified)
nregular = len(regular)
ntotal = nqualified + nregular

# initialize vacation days
arrvacqualified = []
for i in range(0, nqualified):
    arrvacqualified.append("")
arrvacregular = []
for i in range(0, nregular):
    arrvacregular.append("")

setthevacations()

# Calculate the weekend-days
arrwe = []
for i in range(0, ndays):
    weekday = i % 7
    if weekday == 5 or weekday == 6:
        arrwe.append(i)

nwedays = len(arrwe)

print(_("Number of qualified employees: %d") % nqualified)
print(_("Number of other employees: %d") % nregular)
print(_("Weekend days: %s") % str(arrwe))
print(_("Number of weekend days: %d") % nwedays)

# Initialize roster
roster = Roster(ndays, nshiftsperday, qualified, regular)

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
else:
    print(_("Did not work after %d tries.") % ntries)
    if printfailedoutput is True:
        print(_("This is what I have:"))
        roster.printfull()
    if printfailreasons is True:
        for i in qualified + regular:
            failstring = ','.join(roster.clashes(i))
            print(_("%s problems: %s") % (i, failstring))
