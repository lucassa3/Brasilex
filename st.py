class SymbolTable():
    def __init__(self):
        self.table = {}

    def get_var(self, varname):
        if varname not in self.table.keys():
            raise ValueError(f"Variable {varname} does not exist!")
        else:
            return self.table[varname]

    def set_var(self, varname, value):     
        self.table[varname] = value