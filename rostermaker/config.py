import restrictions as re

# configuration object
# including everything you need for roster calculation
class Config:
    def __init__(self):
        self.shiftnames = []
        self.qualified = []
        self.regular = []
        self.vacations = {}

    # set default values
    # without staff, time/vacations, restrictions
    def setdefault(self):
        self.shiftnames = ["E", "L", "N"]  # early, late, night.
        #                                       3 often implicitly assumed
        self.str_sep = ','  # separator

        # algorithmic finetuning
        self.maxntries = 1000
        self.maxnfails = 1000
        self.favwgt = 10  # favorites' weight, for weighted random picking.
        #                   10 is a good value I think
        self.favwgtdimin = 3  # diminished favorite weight
        self.favwgtaugm = 50  # augmented favorite weight
        self.sclshiftjump = 0.05  # yesterday different shift, scale down
        self.sclshiftchng = 0.4  # previous shift (but not yesterday) different, scale down

        # misc
        self.printtrynumbermod = 100  # print every x'th Try, to show user it's still running
        self.printfailedoutput = False  # print the last output even if the restriction checks fail
        self.setlang = 'en'  # output language

        # debug
        self.printfailreasons = False  # print reasons for calculation fails

    # qualified employees
    def setqualified(self, arr):
        self.qualified = arr

    # regular employees
    def setregular(self, arr):
        self.regular = arr

    # 1 is January, 2 is February, and so on.
    def setmonth(self, monthno):
        self.monthno = monthno

    def setyear(self, year):
        self.year = year

    # 0 is Monday, 1 is Tuesday, ... 6 is Sunday.
    def setmonthstartswith(self, monthstartswith):
        self.monthstartswith = monthstartswith

    def setvacations(self, vacations):
        self.vacations = vacations

    def setvacation(self, employee, emplvac):
        self.vacations[employee] = emplvac

    def setrestrictions(self, dict):
        self.restr = re.Restrictions()
        self.restr._set(dict)

    # inspired by https://blender.stackexchange.com/a/1880
    def str(self):
        st = ""
        for attr in vars(self):
            if hasattr(self, attr) and attr != "restr":
                # string attributes have to be put in quotes
                if attr == 'str_sep' or attr == 'setlang':
                    st += ("config.%s = '%s'" % (attr, getattr(self, attr))) + "\n"
                else:
                    st += ("config.%s = %s" % (attr, getattr(self, attr))) + "\n"
        st += "config.setrestrictions(%s)" % self.restr.dict
        return st

    def writetofile(self,filename):
        f = open(filename,"w+")
        f.write(self.str())
        f.close()

    # make static so one can call the constructor from here
    def setfromfile(filename):
        config = Config()
        f = open(filename, "rb")
        exec(compile(f.read(), filename, 'exec'))
        f.close()
        return config

    def setlanguage(self, language):
        self.setlang = language

    # thanks to https://stackoverflow.com/a/1227325
    def __eq__(self, other):
        if not isinstance(other, Config):
            # don't attempt to compare against unrelated types
            return NotImplemented
        if self.qualified != other.qualified:
            return False
        if self.regular != other.regular:
            return False
        if self.vacations != other.vacations:
            return False
        if self.str_sep != other.str_sep:
            return False
        if self.maxntries != other.maxntries:
            return False
        if self.maxnfails != other.maxnfails:
            return False
        if self.favwgt != other.favwgt:
            return False
        if self.favwgtdimin != other.favwgtdimin:
            return False
        if self.favwgtaugm != other.favwgtaugm:
            return False
        if self.sclshiftjump != other.sclshiftjump:
            return False
        if self.sclshiftchng != other.sclshiftchng:
            return False
        if self.printtrynumbermod != other.printtrynumbermod:
            return False
        if self.printfailedoutput != other.printfailedoutput:
            return False
        if self.setlang != other.setlang:
            return False
        if self.printfailreasons != other.printfailreasons:
            return False
        if self.monthno != other.monthno:
            return False
        if self.year != other.year:
            return False
        if self.monthstartswith != other.monthstartswith:
            return False
        if self.restr.dict != other.restr.dict:
            return False
        return True

    def __ne__(self, other):
        return (not __eq__(self, other))
