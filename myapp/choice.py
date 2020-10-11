from sympy import symbols
from sympy import lambdify
from sympy import latex
from sympy import solve
from sympy import Eq


class Choice:
    """
    Class for representing consumer choices
    """
    def __init__(self, name, slope, inter=0):
        self.name = name
        self.slope = float(slope)
        self.inter = float(inter)
        
    @property
    def eq(self):
        """ Cost equation """
        m, x, b = symbols('m x b')
        COST = m*x + b
        return COST.subs(m, self.slope).subs(b, self.inter)

    @classmethod
    def when_equal(cls, a, b):
        """ Compare 2 choices. """
        solution = solve(Eq(a.eq, b.eq))

        if (len(solution) > 1) | (len(solution) == 0):
            raise ValueError('Rut ro...')

        sol = float(solution[0])
        descr = f'The lines touch at {sol}'

        return {'sol':sol, 
                'descr':descr}