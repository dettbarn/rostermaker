import pickle

with open('roster.pkl', 'rb') as roster_file:
    roster = pickle.load(roster_file)

ok = False
ntries = 0
print(_("Starting calculation."))
while (not ok) and ntries < roster.conf.maxntries:
    try:
        ntries += 1
        if(ntries > 0):
            roster.makeempty()
        if ntries % roster.conf.printtrynumbermod == 0:
            print(_("Try #"), str(ntries))
        tryresult = roster.tryfill()
        if tryresult != 0:
            continue
        # now check for clashes with restrictions
        clash = False
        for i in roster.conf.qualified + roster.conf.regular:
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
