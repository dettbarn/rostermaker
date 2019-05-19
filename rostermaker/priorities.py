import exceptions as e
import gettext

_ = gettext.gettext


# weights (values) assigned to employees (keys) in a dictionary structure.
class Priorities:
    def __init__(self):
        self.dict = {}

    def setdict(self, thedict):
        self.dict = thedict

    def setweight(self, key, val):
        if val >= 0:
            self.dict[key] = val
        else:
            raise e.IllegalNegativeException(_("Weights cannot be negative!"))

    def scaleweight(self, key, scale):
        if key not in self.dict.keys():
            self.dict[key] = 1  # init with 1 if needed
        if scale < 0:
            raise e.IllegalNegativeException(_("Weights cannot be negative!"))
        self.dict[key] *= scale

    def getweight(self, key):
        return self.dict[key]

    def isempty(self):
        return not bool(self.dict)

    def max(self):
        if self.isempty():
            str_err = _("Priorities structure is empty!")
            raise e.StructureEmptyException(str_err)
        maximum = 0
        for key in self.dict.keys():
            if self.dict[key] > maximum:
                maximum = self.dict[key]
        return maximum

    def min(self):
        if self.isempty():
            str_err = _("Priorities structure is empty!")
            raise e.StructureEmptyException(str_err)
        first = 1
        for key in self.dict.keys():
            if first:
                minimum = self.dict[key]
            if self.dict[key] < minimum:
                minimum = self.dict[key]
            first = 0
        return minimum
