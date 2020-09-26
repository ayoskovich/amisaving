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

#%config InlineBackend.figure_format='retina'

x = symbols('x');

def build_cost(slope, inter=0):
    """ Create the total cost curve.
    
    Returns a sympy equation.
    """
    m, x, b = symbols('m x b')
    COST = m*x + b
    return COST.subs(m, slope).subs(b, inter)


convert_title = lambda title : "$" + title + "$"


# In[ ]:


FIXED_COST = 24  # Startup costs
VAR_F = 2        # Variable cost if you go with 

VAR_V = 4        # Cost if total variable

fixed = build_cost(slope=VAR_F, inter=FIXED_COST)
variable = build_cost(slope=VAR_V)



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

plt.plot(x_vals, y_vals1, label='With equipment: '  + convert_title(latex(fixed)));
plt.plot(x_vals, y_vals2, label='Buying each day: ' + convert_title(latex(variable)));

plt.axvline(x=EQ, color='green');

plt.title('Cost curves');
plt.legend();
plt.gcf().set_figwidth(12);
plt.gcf().set_figheight(7);


# In[ ]:


from bokeh.models import ColumnDataSource
from bokeh.plotting import figure, output_notebook, show
from bokeh.models import Span

output_notebook()

eq_solve = Span(location=EQ, dimension='height', line_width=2)  # Location where lines intersect

source = ColumnDataSource(data=dict(
    x=x_vals,
    y1=y_vals1,
    y2=y_vals2
))
p = figure(plot_width=400, plot_height=400)


p.line(x='x', y='y1', source=source, color='red', line_width=2)
p.line(x='x', y='y2', source=source, color='green', line_width=2)
p.add_layout(eq_solve)

show(p)


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
