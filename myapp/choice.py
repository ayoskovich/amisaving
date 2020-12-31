from sympy import symbols
from sympy import lambdify
from sympy import latex
from sympy import solve
from sympy import Eq
from operator import attrgetter

class Choice:
    """
    Class for representing consumer choices
    """
    def __init__(self, name, slope, inter=0):
        self.name = name
        self.slope = float(slope)
        self.inter = float(inter)

    def __repr__(self):
        return f'Name: {self.name}, Slope: {self.slope}, Int: {self.inter}'
        
    @property
    def eq(self):
        """ Cost equation """
        m, x, b = symbols('m x b')
        COST = m*x + b
        return COST.subs(m, self.slope).subs(b, self.inter)

    @classmethod
    def when_equal(cls, a, b):
        """ Compare 2 choices. """

        # Equal slopes
        if a.slope == b.slope:

          # Same intercepts too
          if (a.inter==0 and b.inter==00):
            return {'sol':{'x':0, 'y':0}, 
                    'descr':'<p class="sol">Choices are the exact same, follow your heart!</p'}

          return {'sol':{'x':0, 'y':0}, 
                  'descr':f'<p class="sol">You always save money without purchasing equipment.</p'}

        solution = solve(Eq(a.eq, b.eq))

        if (len(solution) != 1):
            raise ValueError('Rut ro...')

        sol = float(solution[0])  # xval

        x = symbols('x')
        yval = float(a.eq.subs(x, sol))

        big = max([a,b], key=attrgetter('slope'))
        small = min([a,b], key=attrgetter('slope'))

        if sol <= 0:
          descr = f'<p class="sol">You always save money with {small.name}</p>'
        else:
          descr =  f'<p class="sol">Before {round(sol, 2)} purchases, you save money by {big.name}. '
          descr += f'<br>After {round(sol)} purchases, you save money by {small.name}.</p>'

        return {'sol':{'x':sol, 'y':yval}, 
                'descr':descr,
                'bef':f'You save money when {big.name}',
                'aft':f'You save money when {small.name}'}
