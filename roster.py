exec(compile(open("functions.py", "rb").read(), "functions.py", 'exec'))

class Roster:
    def __init__(self,ndays,nshiftsperday,qualified,regular):
        self.ndays = ndays
        self.nshiftsperday = nshiftsperday
        self.arr = []
        for iday in range(0,self.ndays):
            x=[]
            for ishift in range(0,self.nshiftsperday):
                x.append("")
            (self.arr).append(x)
        self.qualified = qualified
        self.regular = regular

    def makeempty(self):
        for iday in range(0,self.ndays):
            x=[]
            for ishift in range(0,self.nshiftsperday):
                (self.arr)[iday][ishift] = ""


    def print(self):
        print(self.arr)

    def getindivschedtable(self,thesemembers):
        schedtab=str(thesemembers)+"\n"
        for iday in range(0,self.ndays):
            schedtab+=daystr(iday+1)+"  "
            for memb in thesemembers:
                schedtab+=" "+whatinday(memb,self.arr,iday)
            schedtab+="\n"
        return schedtab

    def tryfill(self):
        nfails = 0
        for iday in range(0,self.ndays):
            for ishift in range(0,self.nshiftsperday):
                # only fill if empty (i.e. not pre-defined)
                if self.arr[iday][ishift]=="":
                # we assume at first that all staff members are available
                # we also assume that we work at minimum staff
                    kpersons=minpersonspershift
                    kquali=1 #r.randrange(minqualipershift,maxqualipershift+1)
                    kreg=max(0,kpersons-kquali)
                    if iday>=1:
                        favsarr = (self.arr[iday-1][ishift]).split(str_sep)
                    else:
                        favsarr = []
                    for i in range(0,kquali):
                        #rnd=qualified[r.randrange(0,nqualified)]# Old non-weighted averaging
                        # New weighted averaging:
                        rnd = pickwithfavorites(self.qualified,favsarr,favwgt)

                        # this one-shift-of-person-per-day is implicitly assumed here (without using the integer defined above)
                        nfails=0
                        while not wouldbeok(rnd,self.arr,iday,ishift):
                            nfails +=1
                            if nfails>maxnfails:
                                #                               print("Too many fails, will retry")
                                return 1
                            rnd = pickwithfavorites(self.qualified,favsarr,favwgt)
                        self.arr[iday][ishift]=addtoshift(rnd,self.arr[iday][ishift])
                    for i in range(0,kreg):
                        #rnd=regular[r.randrange(0,nregular)] # Old non-weighted averaging
                        # New weighted averaging:
                        rnd = pickwithfavorites(self.regular,favsarr,favwgt)
                        nfails=0
                        # this one-shift-of-person-per-day is implicitly assumed here (without using the integer defined above)
                        while not wouldbeok(rnd,self.arr,iday,ishift):
                            nfails+=1
                            if nfails>maxnfails:
                                #print("Too many fails, will retry")
                                return 2
                            rnd = pickwithfavorites(self.regular,favsarr,favwgt)
                        self.arr[iday][ishift]=addtoshift(rnd,self.arr[iday][ishift])
        return 0

    # find the maximum number of shift changes an employee has in one shift series, in this month
    def findmaxshiftchangesseries(self,employee):
        number=0
        for i in range(0,self.ndays):
            if isinday(employee,self.arr,i):
                nshiftchangesthere=0
                for j in range(i+1,self.ndays):
                    if isinday(employee,self.arr,j):
                        if whatinday(employee,self.arr,j) != whatinday(employee,self.arr,j-1):
                            nshiftchangesthere+=1
                    else:
                        i = j # skip outer for-loop directly to where the inner for-loop has walked
                        number = max(number,nshiftchangesthere) # update this
                        break # break inner for-loop and go on with the month
        #print("Max shift changes series for "+employee+": "+str(number))
        return number
