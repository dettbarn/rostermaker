#!/usr/local/bin/python3.5

# todo:
# - restrict number of shift changes (F<->S<->N<->F) within shift series (say <= 1) and also within month (say <= 5)
# - make workdays count respect also the vacation days
# - check if the new stuff (count shift changes per series or month) really works. Right now it seems that it doesn't
# - print out in different formats (dat; csv; tex, also make ps and pdf; html)
# - better UI, that is separated from the algorithms (currently, theinput.py can be corrupted easily)

import random as r
import math
import functions
exec(compile(open("functions.py", "rb").read(), "functions.py", 'exec'))
exec(compile(open("input", "rb").read(), "input", 'exec'))
exec(compile(open("roster.py", "rb").read(), "roster.py", 'exec'))

# evaluate input
nqualified=len(qualified)
nregular=len(regular)
ntotal=nqualified+nregular

# initialize vacation days
arrvacqualified=[]
for i in range (0,nqualified):
    arrvacqualified.append("")
arrvacregular=[]
for i in range (0,nregular):
    arrvacregular.append("")

# call this function in theinput.py
setthevacations()

# Calculate the weekend-days
arrwe=[]
for i in range(0,ndays):
    weekday = i % 7
    if weekday==5 or weekday==6:
        arrwe.append(i)

nwedays=len(arrwe)

print("Anzahl Fachkraefte: "+str(nqualified))
print("Anzahl anderer Mitarbeiter: "+str(nregular))
print("Wochenendtage: "+str(arrwe))
print("Anzahl Wochenendtage: "+str(nwedays))

# Initialize roster
roster = Roster(ndays,nshiftsperday,qualified,regular)

ok = False
ntries = 0
print("Starting calculation.")
while (not ok) and ntries<maxntries:
    try:
        ntries+=1
        if(ntries>0):
            roster.makeempty()
        
        
        if ntries%printtrynumbermod == 0:
            print("Try #",str(ntries))
        tryresult = roster.tryfill()
        if tryresult!=0:
            continue
        
        # now check for clashes with restrictions
        clash=False
        
        arr=roster.arr
        for i in qualified:
               if hasfreeweekends(i,arr)<minfreeweekends or roster.findmaxshiftchangesseries(i)>maxshiftchangesperseries or countshiftchangespermonth(i,arr)>maxshiftchangespermonth or countworkdays(i,arr)<minworkdayseachperson*(ndays-getnvacdays(i))/ndays:
                   clash=True
        for i in regular:
            if hasfreeweekends(i,arr)<minfreeweekends or roster.findmaxshiftchangesseries(i)>maxshiftchangesperseries or countshiftchangespermonth(i,arr)>maxshiftchangespermonth or countworkdays(i,arr)<minworkdayseachperson*(ndays-getnvacdays(i))/ndays:
                   clash=True
        if not clash:
            ok=True
    except KeyboardInterrupt:
        print("Calculation stopped by KeyboardInterrupt.")
        break
    except SystemExit:
        print("Calculation stopped by SystemExit.")
        break
    except:
        print("Unknown error occurred during calculation.")
        raise

if ok:
    print("Worked on Try # "+str(ntries)+".")
    roster.print()
    print(roster.getindivschedtable(roster.qualified))
    print(roster.getindivschedtable(roster.regular))
else:
    print("Did not work after "+str(ntries)+" tries.")
    if printfailedoutput==True:
        print("This is what I have:")
        print(roster.getindivschedtable(roster.qualified))
        print(roster.getindivschedtable(roster.regular))
    if printfailreasons==True:
        for i in qualified+regular:
            failstring=""
            if hasfreeweekends(i,roster.arr)<minfreeweekends:
                failstring+="free weekends,"
            if roster.findmaxshiftchangesseries(i)>maxshiftchangesperseries:
                failstring+="shift series,"
            if countshiftchangespermonth(i,roster.arr)>maxshiftchangespermonth:
                failstring+="monthly shift changes,"
            if countworkdays(i,roster.arr)<minworkdayseachperson*(ndays-getnvacdays(i))/ndays:
                failstring+="work days,"
            print(i+" problems: "+failstring)
