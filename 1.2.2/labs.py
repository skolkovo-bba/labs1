class Value:
    var: float
    err: float

    @property
    def absolute_error(self):
        return self.err

    @property
    def relative_error(self):
        if abs(self.var) < 0.00000001:
            return 0.0
        else:
            return abs(self.err / self.var)

    def __init__(self, var, err=0.0):
        self.var = float(var)
        self.err = abs(err)

    def __str__(self):
        return f"({'{:6f}'.format(self.var)}\u00B1{'{:6f}'.format(self.err)})"
    
    
    def __int__(self):
        return int(self.var)

    def __float__(self):
        return self.var


    def __pos__(self):
        return self

    def __neg__(self):
        return Value(-self.var, self.err)

    def __abs__(self):
        return Value(abs(self.var), self.err)

    def __round__(self, ndigits=None):
        return Value(round(self.var, ndigits), round(self.err, ndigits))


    def __add__(self, other):
        if isinstance(other, Value):
            return Value(self.var + other.var, self.err + other.err)
        elif isinstance(other, int) or isinstance(other, float):
            return Value(self.var + other, self.err)
        else:
            raise TypeError

    def __radd__(self, other):
        if isinstance(other, Value):
            return Value(self.var + other.var, self.err + other.err)
        if isinstance(other, int) or isinstance(other, float):
            return Value(self.var + other, self.err)
        else:
            raise TypeError
    
    def __iadd__(self, other):
        self = self + other


    def __sub__(self, other):
        if isinstance(other, Value):
            return Value(self.var - other.var, self.err + other.err)
        elif isinstance(other, int) or isinstance(other, float):
            return Value(self.var - other, self.err)
        else:
            raise TypeError
    
    def __rsub__(self, other):
        if isinstance(other, Value):
            return other - self
        elif isinstance(other, int) or isinstance(other, float):
            return Value(other - self.var, self.err)
        else:
            raise TypeError
    
    def __isub__(self, other):
        self = self - other
    

    def __mul__(self, other):
        with open("out.txt", "w+") as f:
            f.write(f"mul {self}, {other}\n")
        if isinstance(other, Value):
            return Value(self.var * other.var, (self.var * other.var) * ((self.relative_error ** 2 + other.relative_error ** 2) ** 0.5))
        elif isinstance(other, int) or isinstance(other, float):
            return Value(self.var * other, self.err * other * self.relative_error)
        else:
            raise TypeError
    
    def __rmul__(self, other):
        with open("out.txt", "w+") as f:
            f.write(f"what {self}, {other}\n")
        if isinstance(other, int) or isinstance(other, float):
            return Value(self.var * other, self.err * other * self.relative_error)
        else:
            raise TypeError
    
    def __imul__(self, other):
        self = self * other


    def __truediv__(self, other):
        if isinstance(other, Value):
            return Value(self.var / other.var, (self.var / other.var) * ((self.relative_error ** 2 + other.relative_error ** 2) ** 0.5))
        elif isinstance(other, int) or isinstance(other, float):
            return Value(self.var / other, (self.var / other) * self.relative_error)
        else:
            raise TypeError
    
    def __rtruediv__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Value(other / self.var, (other / self.var) * self.relative_error)
        else:
            raise TypeError

    def __itruediv__(self, other):
        self = self / other
  

    def __pow__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Value(self.var ** other, self.var ** (other - 1) * other * self.err)
        else:
            raise TypeError
    

    def __lt__(self, other):
        return self.var < other.var
    
    def __gt__(self, other):
        return self.var > other.var
    

    def __hash__(self):
        return hash(self.var) * int("1" + "0" * int(len(str(hash(self.var))))) + hash(self.err)

def series_err(var):
    def f(var):
        return Value(var, next(f.it))

    f.it = iter(var)
    return f

def const_err(err):
    def f(var):
        return Value(var, err)

    return f

def get_err(x: Value):
    if isinstance(x, Value):
        return x.err
    elif isinstance(x, int) or isinstance(x, float):
        return float(0)
    else:
        raise TypeError

def get_var(x: Value):
    if isinstance(x, Value):
        return x.var
    elif isinstance(x, int) or isinstance(x, float):
        return float(x)
    else:
        raise TypeError