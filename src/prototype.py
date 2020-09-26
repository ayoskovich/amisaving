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

source = ColumnDataSource(data=dict(
    x=x_vals,
    y1=y_vals1,
    y2=y_vals2
))
p = figure(plot_width=400, plot_height=400)
p.vline_stack(['y1', 'y2'], x='x', source=source)
show(p)


# In[ ]:


x_vals
y_vals1
y_vals2


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

# In[ ]:


from bokeh.io import output_notebook, show
from bokeh.plotting import figure

output_notebook()

fruits = ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries']
counts = [5, 3, 4, 2, 4, 6]

p = figure(x_range=fruits, plot_height=250, title="Fruit counts",
           toolbar_location=None, tools="")

p.vbar(x=fruits, top=counts, width=.9)
show(p)


# In[ ]:


from bokeh.io import output_file, show
from bokeh.plotting import figure

output_notebook()

fruits = ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries']
counts = [5, 3, 4, 2, 4, 6]

# sorting the bars means sorting the range factors
sorted_fruits = sorted(fruits, key=lambda x: counts[fruits.index(x)])

p = figure(x_range=sorted_fruits, plot_height=350, title="Fruit Counts",
           toolbar_location=None, tools="")

p.vbar(x=fruits, top=counts, width=0.9)

p.xgrid.grid_line_color = None
p.y_range.start = 0

show(p)

