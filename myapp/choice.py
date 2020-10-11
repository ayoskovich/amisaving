from sympy import symbols
from sympy import lambdify
from sympy import latex
from sympy import solve
from sympy import Eq


class Choice:
    """
    Class for representing consumer choices
    """
    def __init__(self, name, slope, inter):
        self.name = name
        self.slope = slope
        self.inter = inter
        
    @property
    def eq(self):
        """ Cost equation """
        m, x, b = symbols('m x b')
        COST = m*x + b
        return COST.subs(m, self.slope).subs(b, self.inter)

    def __repr__(self):
        return f'{self.name}, s:{self.slope}, i:{self.inter}'
    
    def __add__(self, other):
        return self.slope + other.slope
    
    @classmethod
    def when_equal(cls, a, b):
        """ Compare 2 choices. """
        solution = solve(Eq(a.eq, b.eq))

        if len(solution) == 1:
            return solution[0]
        if len(solution) > 1:
            return 'Solution is not unique'
        elif len(solution) == 0:
            return 'There is no solution...'