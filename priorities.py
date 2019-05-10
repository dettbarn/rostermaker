exec(compile(open("exceptions.py", "rb").read(), "exceptions.py", 'exec'))


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
            raise IllegalNegativeException(_("Weights cannot be negative!"))

    def scaleweight(self, key, scale):
        if key not in self.dict.keys():
            self.dict[key] = 1  # init with 1 if needed
        self.dict[key] *= scale

    def getweight(self, key):
        return self.dict[key]
