#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import matplotlib.pyplot as plt
import numpy as np

import sympy
from sympy import symbols
from sympy import lambdify
from sympy import latex
from sympy import solve
from sympy import Eq

x = symbols('x');

def build_cost(slope, inter=0):
    """ Create the total cost curve.
    
    Returns a sympy equation.
    """
    m, x, b = symbols('m x b')
    COST = m*x + b
    return COST.subs(m, slope).subs(b, inter)


# In[ ]:


fixed = build_cost(slope=2, inter=24)
variable = build_cost(slope=4)

# Get where they're equal
EQ = int(solve(Eq(fixed, variable))[0])
FREQ = 'days'

print(f'The cost curves are equal at {EQ}')
print(f'With a use each {FREQ}, it would take {EQ} {FREQ} in order to make money.')

lam_a = lambdify(x, fixed, modules=['numpy'])
lam_b = lambdify(x, variable, modules=['numpy'])

BUF = 20  # Before and after equal
x_vals = np.linspace(EQ-BUF, EQ+BUF, 100)
y_vals1 = lam_a(x_vals)
y_vals2 = lam_b(x_vals)

plt.plot(x_vals, y_vals1, label='With equipment: '  + latex(fixed));
plt.plot(x_vals, y_vals2, label='Buying each day: ' + latex(variable));

plt.axvline(x=EQ, color='green');

plt.title('Cost curves');
plt.legend();


# ### User input
# 
# - Frequency units (day, week, month)
# - Frequency of use (number: 1, 2, 3) times per frequency unit
# - Cost per unit (no capital)
# - Cost per unit (with capital)
# 
# ### Output
# 
# - How many frequency units until they're making money?
# - \[Yes / No\] will you save money if you use this once a day for 500 days?
