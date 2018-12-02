class SymbolTable():
    def __init__(self):
        self.table = {}
        self.father = None

    def get_var(self, varname):
        if varname not in self.table.keys():
            if self.father:
                return self.father.get_var(varname)
            else:
                raise ValueError(f"Variable {varname} does not exist!")
        else:
            return self.table[varname]

    def set_var(self, varname, value, on_father=False):
        if varname not in self.table.keys():
            if self.father:
                if self.father.set_var(varname, value, on_father=True):
                    return True
        else:
            self.table[varname] = value
            return True

        if not on_father:
            self.table[varname] = value
