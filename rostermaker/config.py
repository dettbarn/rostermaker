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

    def setrestrictions(self, restr):
        self.restr = restr

    # inspired by https://blender.stackexchange.com/a/1880
    def str(self):
        st = ""
        for attr in vars(self):
            if hasattr(self, attr) and attr != "restr":
                st += ("config.%s = %s" % (attr, getattr(self, attr))) + "\n"
        st += "config.setrestrictions(%s)" % restr.dict
        return st

    # make static so one can call the constructor from here
    def setfromfile(confobj, file):
        config = Config()
        exec(compile(open("input", "rb").read(), "input", 'exec'))