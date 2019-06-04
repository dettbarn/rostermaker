import gettext

_ = gettext.gettext

class Restrictions:
    def __init__(self):
        self.dict = {}
        self.allowed = []
        self.allowed += ["nshiftsperday"]
        self.allowed += ["maxshiftsperday"]
        self.allowed += ["maxdaysinrow"]
        self.allowed += ["minfreeshifts"]
        self.allowed += ["minfreeweekends"]
        self.allowed += ["maxshiftchangesperseries"]
        self.allowed += ["maxshiftchangespermonth"]
        self.allowed += ["minworkdayseachperson"]
        self.allowed += ["ndaysinrowtorequiretwofree"]
        self.allowed += ["minqualipershift"]
        self.allowed += ["maxqualipershift"]
        self.allowed += ["minpersonspershift"]

    def _set(self, setdict):
        self.dict = setdict

    def _setkv(self, key, val):
        self.dict[key] = val

    # the caller has to know all keys in self.allowed in order
    def _setall(self, keyarr):
        for i in range(0, len(self.allowed)):
            self._setkv(self.allowed[i], keyarr[i])

    def tryset(self, key, val):
        if key in self.allowed:
            self._setkv(key, val)
            return 0
        else:
            return 1

    def promptall(self):
        for key in self.allowed:
            self._setkv(key, input(key+": "))

    def print(self):
        print(self.dict)
